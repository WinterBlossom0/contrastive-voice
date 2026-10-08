"""Dataset build (Kaggle): ingest the staged sources, select passages automatically, cut reader spans, inject flaws, write
labels, a manifest and a label-QA report.

    python -m cvoice.dataset build --sources /kaggle/input/cvoice-sources --out /kaggle/working/data --cache /kaggle/working/cache

Layout under <out>/dataset/: baselines/, flawed/, readers/, labels/, manifest.json, label_qa.json, dataset_card.md.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import __version__
from . import audio, flaws
from . import config as C
from .align import Transcript, parse_transcript
from .features import Recording
from .passages import Group, Passage, locate_many, page_text, select_passages
from .pipeline import ROOT, device_class, make_job, map_calls, run_jobs
from .pool import PreparePool

MANIFEST = ROOT / "data" / "sources_manifest.json"
GETTYSBURG_REFERENCE = "gettysburg_amb"  # B for the cross-speaker flawed pairs (DESIGN 2.3)


def log(msg: str) -> None:
    print(f"[dataset] {msg}", flush=True)


# ============================================================================================ sources
def load_sources_manifest() -> dict:
    return json.loads(MANIFEST.read_text())


def find_source(root: Path, name: str) -> Path:
    """Locate a staged file anywhere under the mounted sources dataset (zip-extracted folders nest)."""
    for dirpath, _, files in os.walk(root):
        if name in files:
            return Path(dirpath) / name
    raise FileNotFoundError(f"{name} not found under {root}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    return h.hexdigest()


def ingest(entry: dict, root: Path) -> tuple[np.ndarray, dict]:
    """Verify the SHA-256 of a staged source, decode (ffmpeg), apply the channel policy, return canonical 16 kHz mono."""
    path = find_source(root, entry["audio_file"])
    got = sha256_file(path)
    if got != entry["sha256"]:
        raise ValueError(f"{entry['id']}: SHA-256 of {path.name} is {got}, the manifest says {entry['sha256']}")
    x, sr = audio.decode(path, timeout=600)
    mono, rule = audio.to_mono(x)
    return audio.canonical(mono, sr), {"file": entry["audio_file"], "sha256": got, "sr_in": sr, "channels": int(x.shape[1]),
                                       "channel_rule": rule, "duration_s": round(len(mono) / sr, 3)}


def official_text(entry: dict, root: Path) -> str:
    """Official transcript page text: staged page, or the copy kept in the repository (entry['transcript_root'])."""
    path = ROOT / "data" / entry["transcript"] if entry["transcript_root"] == "repo" else find_source(root, Path(entry["transcript"]).name)
    return page_text(path)


# ============================================================================================ dataset on disk
@dataclass
class Dataset:
    """A built dataset: manifest plus lazy loading of audio, transcripts and analysed recordings. Recordings are analysed in
    batches (`recs`, `clip_recs`, `prepare_many`): through `pool` when there is one, in this process otherwise."""
    root: Path  # .../dataset
    manifest: dict
    cache: Path | None = None
    pool: object = None
    aligner: object = None
    _recs: dict = field(default_factory=dict)
    _clip_recs: dict = field(default_factory=dict)

    def entry(self, kind: str, id_: str) -> dict:
        for e in self.manifest[kind]:
            if e["id"] == id_:
                return e
        raise KeyError(f"{id_} not in manifest[{kind}]")

    def transcript(self, entry: dict) -> Transcript:
        tr = parse_transcript(entry["text"])
        if "sentence" in entry:  # re-parsing the display text can lose a sentence break (a number-initial sentence)
            if len(entry["sentence"]) != len(tr):
                raise ValueError(f"{entry['id']}: {len(entry['sentence'])} stored sentence indices for {len(tr)} words")
            tr = dataclasses.replace(tr, sentence=tuple(entry["sentence"]))
        return tr

    def wav(self, entry: dict) -> np.ndarray:
        return audio.read_wav(self.root / entry["audio"])

    def prepare_many(self, items: list[tuple[np.ndarray, Transcript]]) -> list[Recording]:
        """Analyse (samples, transcript) pairs in one batch, input order."""
        return run_jobs([make_job(w, tr) for w, tr in items], self.pool, self.aligner, self.cache)

    def load(self, entries: list[dict] = (), clips: list[dict] = ()) -> None:
        """Analyse the manifest entries and stored clips not yet in memory, all in ONE batch (memoised by id)."""
        need_e = list({e["id"]: e for e in entries if e["id"] not in self._recs}.values())
        need_c = list({c["id"]: c for c in clips if c["id"] not in self._clip_recs}.values())
        res = self.prepare_many([(self.wav(e), self.transcript(e)) for e in need_e] + [(self.wav(c), self.clip_transcript(c)) for c in need_c])
        for e, r in zip(need_e, res):
            self._recs[e["id"]] = r
        for c, r in zip(need_c, res[len(need_e):]):
            self._clip_recs[c["id"]] = r

    def recs(self, entries: list[dict]) -> list[Recording]:
        """Analysed recordings of manifest entries (memoised; the missing ones are analysed in one batch)."""
        self.load(entries=entries)
        return [self._recs[e["id"]] for e in entries]

    def rec(self, entry: dict) -> Recording:
        return self.recs([entry])[0]

    def clip_recs(self, clips: list[dict]) -> list[Recording]:
        """Analysed stored clips (memoised by clip id)."""
        self.load(clips=clips)
        return [self._clip_recs[c["id"]] for c in clips]

    def clip_transcript(self, clip: dict) -> Transcript:
        return self.transcript(self.parent_entry(clip))

    def any_entry(self, id_: str) -> dict:
        """A baseline or reader entry by id."""
        for kind in ("baselines", "readers"):
            for e in self.manifest[kind]:
                if e["id"] == id_:
                    return e
        raise KeyError(f"{id_} is neither a baseline nor a reader")

    def parent_entry(self, clip: dict) -> dict:
        return self.any_entry(clip["parent"])

    def labels(self, clip: dict) -> dict:
        from .protocol import label_eligibility
        issues = [q for q in self.manifest.get('realisation_shortfalls', []) if q.get('clip') == clip['id']]
        issues += clip.get('realisation_qa', [])
        if clip.get('kind') != 'extra_botched':
            issues += clip.get('ladder_qa', [])
        return label_eligibility(json.loads((self.root / clip["labels"]).read_text()), issues)

    def clips(self, **where) -> list[dict]:
        return [c for c in self.manifest["clips"] if all(c.get(k) == v for k, v in where.items())]


def load_dataset(root: Path, cache: Path | None = None, pool=None, aligner=None) -> Dataset:
    root = Path(root)
    if (root / "dataset").is_dir():
        root = root / "dataset"
    return Dataset(root, json.loads((root / "manifest.json").read_text()), cache, pool, aligner)


# ============================================================================================ build
def _entry(id_: str, wav: np.ndarray, rel: str, out: Path, tr: Transcript, **extra) -> dict:
    audio.write_wav(out / rel, wav)
    return {"id": id_, "audio": rel, "sha256": audio.sha256_pcm(wav), "duration_s": round(len(wav) / C.SR, 3), "text": tr.text(),
            "n_words": len(tr), "n_sentences": tr.n_sentences, "sentence": list(tr.sentence), **extra}


def build_clean(src: dict, root: Path, out: Path, pool=None, aligner=None, null_readers=None, before_align=None) -> tuple[list[dict], list[dict]]:
    """The clean passages, batch-first: ingest every source, one batch of full-file emissions (passage selection), then one
    force-alignment batch per selection round across all speeches. Returns (nine baselines, the readers: nine Gettysburg
    readings and the Greenman reading of the Reagan passage)."""
    by_id = {e["id"]: e for e in src["entries"]}
    base_entries = [e for e in src["entries"] if e["role"] == "baseline"]
    reader_entries = sorted((e for e in src["entries"] if e["role"] in ("reader_calibration", "reader_check")),
                            key=lambda e: e["id"] != "lv_gettysburg150_amb")  # the reference reader first (ranks the windows)
    greenman = by_id["lv_farewell_reagan"]
    wavs, infos = {}, {}
    for e in base_entries + [greenman] + reader_entries:
        log(f"ingest {e['id']}")
        wavs[e["id"]], infos[e["id"]] = ingest(e, root)
    reader_official = parse_transcript(official_text(reader_entries[0], root), strict=False)
    officials = {e["id"]: parse_transcript(official_text(e, root), strict=False) for e in base_entries}
    officials[greenman["id"]] = officials["reagan_farewell_1989"]
    officials.update({e["id"]: reader_official for e in reader_entries})
    if null_readers is not None:
        for e in reader_entries:
            rid = 'null_project_' + e['id']
            tr = reader_official
            row = _entry(rid, wavs[e['id']], f'readers/{rid}.wav', out, tr, source='gettysburg',
                         speaker_id=e['id'], project_role=e['role'], licence_basis=e['licence_basis'], licence_url=e['licence_url'])
            null_readers.append(row)
    if before_align is not None:
        before_align(null_readers)
    ids = list(wavs)
    log(f"full-file emissions for {len(ids)} recordings")
    anchors = dict(zip(ids, locate_many([wavs[i] for i in ids], [officials[i] for i in ids], pool, aligner)))
    groups = []
    for e in base_entries:  # reagan: candidate windows restricted to sentences anchored in both readings
        members = [e["id"]] + (["lv_farewell_reagan"] if e["id"] == "reagan_farewell_1989" else [])
        groups.append(Group(e["id"], [wavs[m] for m in members], officials[e["id"]], [anchors[m] for m in members]))
        log(f"{e['id']}: {sum(a.eligible for a in anchors[e['id']])}/{len(anchors[e['id']])} sentences eligible in {infos[e['id']]['duration_s']:.0f} s of audio")
    rids = [e["id"] for e in reader_entries]
    groups.append(Group("gettysburg readers", [wavs[i] for i in rids], reader_official, [anchors[i] for i in rids]))
    log(f"passage selection for {len(groups)} groups")
    chosen = select_passages(groups, pool, aligner)
    base_rows: list[dict] = []
    green: dict[str, Passage] = {}
    for e, ps in zip(base_entries, chosen):
        p = ps[0]
        base_rows.append(_entry(e["id"], p.wav, f"baselines/{e['id']}.wav", out, p.tr, speaker=e["speaker"], gender=e["gender"],
                                year=e["year"], title=e["title"], split=e["split"], source=infos[e["id"]], licence_basis=e["licence_basis"],
                                licence_url=e["licence_url"], transcript_url=e["transcript_url"], passage=p.meta))
        if len(ps) == 2:
            green[e["id"]] = ps[1]
            base_rows[-1]["passage_greenman"] = ps[1].meta
        log(f"  {e['id']}: sentences {p.meta['sentences']} {p.meta['n_words']} words {p.meta['clip_duration_s']:.1f} s compat {p.meta['qa']['mean_compat']}")
    reader_rows: list[dict] = []
    for e, p in zip(reader_entries, chosen[-1]):
        rid = "gettysburg_" + e["id"].rsplit("_", 1)[1]
        reader_rows.append(_entry(rid, p.wav, f"readers/{rid}.wav", out, p.tr, role=e["role"], split=e["split"], speaker=e["speaker"],
                                  source=infos[e["id"]], licence_basis=e["licence_basis"], licence_url=e["licence_url"], passage=p.meta))
    for bid, p in green.items():
        e = next(e for e in src["entries"] if e["role"] == "orator_reference")
        reader_rows.append(_entry("greenman_reagan", p.wav, "readers/greenman_reagan.wav", out, p.tr, role="orator_reference",
                                  split="train", speaker=e["speaker"], paired_baseline=bid, licence_basis=e["licence_basis"],
                                  licence_url=e["licence_url"], passage=p.meta))
    return base_rows, reader_rows


def edit_support_share(labels: dict) -> float:
    """Union of clipped edit supports divided by participant samples; inserted silence belongs to its support."""
    end = covered = 0
    spans = sorted((max(0, f["support"][0]), min(labels["n_samples"], f["support"][1])) for f in labels["flaws"])
    spans += [tuple(f["span"]) for f in labels["flaws"] if f["type"] == "PAUSE_INTRUSIVE"]
    for a, b in sorted(spans):
        a, b = max(0, a), min(labels["n_samples"], b)
        covered += max(0, b - max(a, end))
        end = max(end, b)
    return covered / max(labels["n_samples"], 1)


def _clip(kind: str, clip_id: str, y: np.ndarray, labels: dict, out: Path, parent: str, baseline: str, regime: str, split: str, **extra) -> dict:
    audio.write_wav(out / "flawed" / f"{clip_id}.wav", y)
    (out / "labels").mkdir(parents=True, exist_ok=True)
    (out / "labels" / f"{clip_id}.json").write_text(json.dumps(labels, sort_keys=True, separators=(",", ":")) + "\n")
    return {"id": clip_id, "audio": f"flawed/{clip_id}.wav", "labels": f"labels/{clip_id}.json", "sha256": labels["sha256"], "duration_s": round(labels["n_samples"] / C.SR, 3), "kind": kind,
            "parent": parent, "baseline": baseline, "regime": regime, "split": split, "n_flaws": len(labels["flaws"]),
            "edit_support_time_share": round(edit_support_share(labels), 6),
            "levels": sorted({f["level"] for f in labels["flaws"] if f["level"] is not None}),
            "types": [f["type"] for f in labels["flaws"]], "skipped": labels["skipped"], **extra}


def build_baseline_clips(rec: Recording, entry: dict, out: Path) -> list[dict]:
    """Per baseline: 6 single-level clips, 1 identity / placebo clip, ladder clips G1 / G3 / G5 (10 clips)."""
    bid, split = entry["id"], entry["split"]
    rows = []

    def make(clip_id, plan, recipe, kind, **extra):
        seed = flaws.clip_seed(clip_id)
        y, lab = flaws.inject(rec, plan, clip_id, bid, recipe=recipe, seed=seed)
        rows.append(_clip(kind, clip_id, y, lab, out, bid, bid, "R1", split, recipe=recipe, **extra))

    for level in C.LEVELS:
        for j, types in enumerate(C.SINGLE_LEVEL_SETS):
            cid = f"{bid}__single_L{level}{'AB'[j]}"
            make(cid, flaws.plan_clip(rec, [(t, level) for t in types], flaws.clip_seed(cid)), f"single_L{level}{'AB'[j]}", "single", level=level)
    cid = f"{bid}__identity"
    make(cid, flaws.identity_plan(rec, flaws.clip_seed(cid)), "identity", "identity")
    cid = f"{bid}__G1"
    make(cid, flaws.plan_clip(rec, [(C.G1_TYPE, 1)], flaws.clip_seed(cid)), "G1", "ladder", rung=1)
    cid = f"{bid}__G3"
    make(cid, flaws.plan_clip(rec, [(t, 2) for t in C.G3_TYPES], flaws.clip_seed(cid)), "G3", "ladder", rung=3)
    cid = f"{bid}__G5"
    make(cid, flaws.plan_botched(rec, flaws.clip_seed(cid)), "G5", "ladder", rung=5)
    rows += build_extra_clips(rec, entry, out)
    return rows


def build_cross_clips(p0: Recording, ref: Recording, reader: dict, baseline_id: str, out: Path) -> list[dict]:
    """Three cross-speaker flawed clips (one L2, two L3) of a reader against the reference B, and the reader's botched clip
    (the bottom ladder rung G5 for a different speaker)."""
    rows = []
    for n, (level, types) in enumerate(C.CROSS_SPEAKER_CLIPS, 1):
        cid = f"{reader['id']}__x{n}_L{level}"
        seed = flaws.clip_seed(cid)
        plan = flaws.plan_clip(p0, [(t, level) for t in types], seed, ref=ref)
        if not plan.edits:
            rows.append({"id": cid, "kind": "cross", "missing": True, "skipped": plan.skipped})
            continue
        y, lab = flaws.inject(p0, plan, cid, reader["id"], recipe=f"cross_x{n}_L{level}", seed=seed)
        rows.append(_clip("cross", cid, y, lab, out, reader["id"], baseline_id, "R2", reader["split"], recipe=f"cross_x{n}_L{level}", level=level))
    cid = f"{reader['id']}__G5"
    y, lab = flaws.inject(p0, flaws.plan_botched(p0, flaws.clip_seed(cid)), cid, reader["id"], recipe="G5", seed=flaws.clip_seed(cid))
    rows.append(_clip("cross_botched", cid, y, lab, out, reader["id"], baseline_id, "R2", reader["split"], recipe="G5", rung=5))
    rows += build_extra_clips(p0, reader, out, ref=ref, baseline_id=baseline_id)
    return rows



def extra_clip_specs(parent, cross=False):
    if cross:
        return [(f"{parent}__extra_x{j}_L{lv}", lv, ts) for j, (lv, ts) in enumerate(C.EXTRA_CROSS_CLIPS, 1)]
    return [(f"{parent}__extra_L{lv}{'ABCD'[j]}", lv, ts) for lv in C.LEVELS for j, ts in enumerate(C.EXTRA_SINGLE_LEVEL_SETS)]


def extra_realisation_qa(lab):
    issues = []
    for f in lab["flaws"]:
        before_issues = len(issues)
        r, p, typ = f["realised"], f["parameter"], f["type"]
        value = r.get("value")
        if value is None or not np.isfinite(value):
            issues.append({"type": typ, "level": f["level"], 'words': f['words'], 'parent_span': f['parent_span'], "reason": "missing realised measurement"})
            continue
        sign = -1 if typ in ("NATURAL_RUSH", "LOW_EFFORT", "TRAILING_OFF", "FLAT_FINAL_FALL", "REPEATED_CONTOUR") else 1
        starts, ends = lab["parent_words"]["start"], lab["parent_words"]["end"]
        wa, wb = f["words"]
        word_s = (ends[wa] - starts[wa]) / C.SR
        observed = value * sign
        target = None
        if typ == "NATURAL_RUSH":
            target = sum((ev["parent_span"][1] - ev["parent_span"][0]) / C.SR *
                         (1 - (1 / p["speech_rate"] if ev["kind"] == "stretch" else p["pause_kept_fraction"])) for ev in f["events"])
        elif typ == "HESITATION":
            target = word_s * (p["word_duration_factor"] - 1) + p["silence_s"]
        elif typ == "WORD_BY_WORD":
            target = (wb - wa) * p["silence_s"]
        elif typ == "UNEVEN_TEMPO":
            target = float(np.std(f["details"]["word_duration_factors"]))
        elif typ == "WORD_REPETITION":
            target = word_s * p["first_token_duration_factor"] + p["silence_s"]
        elif typ == "SOUND_REPETITION":
            target = p["inserted_copies"] * (word_s * C.ONSET_FRACTION + p["silence_s"])
        elif typ == "BLOCK":
            target = p["silence_s"]
        elif typ == "RHYME_PROLONGATION":
            target = p["added_duration_s"]
        elif typ == "ONSET_PROLONGATION":
            target = p["onset_target_s"] - (f["parent_span"][1] - f["parent_span"][0]) / C.SR
        elif typ == "LOW_EFFORT":
            target = p["attenuation_db"]
        elif typ == "TRAILING_OFF":
            observed = -r["level_slope_change_db_s"]
            target = p["final_attenuation_db"] / ((f["parent_span"][1] - f["parent_span"][0]) / C.SR)
        elif typ == "RISING_ENDING":
            target = p["rise_st"]
            if r.get("final_change_st", 0.) < 1.:
                issues.append({"type": typ, "level": f["level"], "reason": "final contour does not rise by at least 1 st"})
        elif typ == "FLAT_FINAL_FALL":
            target = p["strength"] * r["before_rmse_st"]
        elif typ == "REPEATED_CONTOUR":
            target = p["contour_strength"] * (r["after_rmse_st"] - value)
        if observed <= 0 or (target is not None and observed < 0.5 * target):
            issues.append({"type": typ, "level": f["level"], "reason": "realised change below half target or wrong sign",
                           "value": observed, "target": target})
        if typ == "MISPLACED_EMPHASIS" and (r["function_change_p"] <= 0 or r["stressed_change_p"] >= 0):
            issues.append({"type": typ, "level": f["level"], "reason": "prominence transfer cue has wrong sign"})
        if typ in ("LOW_EFFORT", "TRAILING_OFF"):
            ratio = r["alpha_change_db"] / value if value else 0
            if not 0.4 <= ratio <= 0.7:
                issues.append({"type": typ, "level": f["level"], "reason": "alpha/level coupling outside 0.4–0.7", "ratio": ratio})
        for issue in issues[before_issues:]:
            issue.update(words=f['words'], parent_span=f['parent_span'])
    return issues


def extra_ladder_qa(rows, root):
    groups = {}
    issues = []
    for c in rows:
        if c.get("missing") or c.get("kind") == "extra_botched":
            continue
        lab = json.loads((root / c["labels"]).read_text())
        for f in lab["flaws"]:
            groups.setdefault((c["parent"], f["type"]), []).append((c, f))
    for (parent, typ), entries in groups.items():
        entries.sort(key=lambda cf: cf[1]["level"])
        levels = [f["level"] for _, f in entries]
        if len(levels) < 2:
            continue
        placements = [f["parent_span"] for _, f in entries]
        if any(p != placements[0] for p in placements):
            issues.append({"parent": parent, "type": typ, "reason": "different ladder placements"})
            continue
        sign = -1 if typ in ("NATURAL_RUSH", "LOW_EFFORT", "TRAILING_OFF", "FLAT_FINAL_FALL", "REPEATED_CONTOUR") else 1
        fields = [("value", sign)]
        if typ in ("LOW_EFFORT", "TRAILING_OFF"):
            fields.append(("alpha_change_db", -1))
        if typ == "LOW_EFFORT":
            fields.append(("pitch_change_st", -1))
        if typ == "TRAILING_OFF":
            fields.extend((("level_slope_change_db_s", -1), ("last_word_level_change_db", -1)))
        if typ == "MISPLACED_EMPHASIS":
            fields.extend((("function_change_p", 1), ("stressed_change_p", -1)))
        for measure, direction in fields:
            values = [f["realised"].get(measure) for _, f in entries]
            if any(v is None or not np.isfinite(v) for v in values) or not all(
                    direction * b > direction * a for a, b in zip(values, values[1:])):
                issues.append({"parent": parent, "type": typ, "reason": "non-monotone realised ladder",
                               "field": measure, "levels": levels, "values": values})
    return issues


def build_extra_clips(rec, entry, out, *, ref=None, baseline_id=None, botched=True):
    cross = ref is not None
    rows, plans = [], {}
    def render(cid, level, types, plan, seed, kind):
        requested = [{"type": t, "level": level} for t in types]
        metadata = {"id": cid, "kind": kind, "parent": entry["id"], "baseline": baseline_id or entry["id"],
                    "regime": "R2" if cross else "R1", "split": entry["split"], "level": level,
                    "spectrum": "extra", "requested": requested}
        if not plan.edits:
            rows.append({**metadata, "missing": True, "skipped": plan.skipped})
            return
        y, lab = flaws.inject(rec, plan, cid, entry["id"], recipe=cid.split("__", 1)[1], seed=seed)
        if not lab["flaws"]:
            rows.append({**metadata, "missing": True, "skipped": lab["skipped"]})
            return
        qa = extra_realisation_qa(lab)
        rows.append(_clip(kind, cid, y, lab, out, entry["id"], metadata["baseline"], metadata["regime"], entry["split"],
                          level=level, recipe=lab["recipe"], spectrum="extra", requested=requested, realisation_qa=qa))
    for cid, level, types in extra_clip_specs(entry["id"], cross):
        if types not in plans:
            seed = flaws.clip_seed(f"{entry['id']}:extra:{','.join(types)}")
            plans[types] = flaws.plan_clip(rec, [(t, 2) for t in types], seed, ref=ref), seed
        base, seed = plans[types]
        plan = flaws.Plan([dataclasses.replace(e, level=level, param=flaws.level_param(e.type, level)) for e in base.edits],
                          [{**skip, "level": level} for skip in base.skipped])
        render(cid, level, types, plan, seed, "cross" if cross else "single")
    if botched:
        for family in sorted({C.FLAW_FAMILY[t] for t in C.EXTRA_TYPES}):
            cid = f"{entry['id']}__extra_botched_{family}"
            seed = flaws.clip_seed(cid)
            types = tuple(t for t in C.EXTRA_TYPES if C.FLAW_FAMILY[t] == family) * 2
            taken, edits, skipped = [], [], []
            rng = np.random.default_rng(seed)
            for typ in types:
                cands = flaws.extra_candidates(rec, ref, typ, C.SPAN_WORDS[1] + 2, taken)
                if not cands:
                    skipped.append({"type": typ, "level": 3, "reason": "no eligible disjoint botched placement"})
                    continue
                pos = cands[int(rng.integers(len(cands)))]
                taken.append(pos)
                edits.append(flaws.make_edit(rec, typ, 3, pos))
            render(cid, 3, types, flaws.Plan(edits, skipped), seed, "extra_botched")
    qa = extra_ladder_qa(rows, out)
    for row in rows:
        row["ladder_qa"] = [q for q in qa if row['kind'] != 'extra_botched' and q["parent"] == row["parent"] and
                            q["type"] in [t["type"] for t in row["requested"]]]
    return rows

def label_qa(ds: Dataset, clip: dict, al) -> dict:
    """Compare the re-aligned word boundaries `al` of an edited clip with the analytic labels (self-consistency, not human accuracy)."""
    lab = ds.labels(clip)
    tr = ds.clip_transcript(clip)
    s_an, e_an = np.array(lab["words"]["start"]) / C.SR, np.array(lab["words"]["end"]) / C.SR
    err = np.concatenate([np.abs(al.start - s_an), np.abs(al.end - e_an)]) * 1000.0
    inside = np.zeros(len(tr), dtype=bool)
    for f in lab["flaws"]:
        s, e = f["support"]
        inside |= (al.end * C.SR > s) & (al.start * C.SR < e)
    ei = np.concatenate([np.abs(al.start - s_an)[inside], np.abs(al.end - e_an)[inside]]) * 1000.0
    eo = np.concatenate([np.abs(al.start - s_an)[~inside], np.abs(al.end - e_an)[~inside]]) * 1000.0
    st = lambda a: None if len(a) == 0 else {"median_ms": round(float(np.median(a)), 1), "p90_ms": round(float(np.percentile(a, 90)), 1),
                                              "max_ms": round(float(a.max()), 1), "within_50ms": round(float((a <= 50).mean()), 3)}
    return {"clip": clip["id"], "mean_compat": round(al.mean_compat, 4), "all_words": st(err), "inside_support": st(ei),
            "outside_support": st(eo), "outside_support_identical": lab["outside_support_identical"],
            "inserted_copies": sum(e["kind"] == "copy" for f in lab["flaws"] for e in f.get("events", [])),
            "inserted_silences": sum(e["kind"] == "silence" for f in lab["flaws"] for e in f.get("events", []))}


def write_card(manifest: dict, path: Path) -> None:
    lines = ["# Contrastive Voice dataset", "",
             "Controlled-perturbation dataset for reference-relative delivery analysis. Baselines are public-domain speeches (US government "
             "recordings) and public-domain LibriVox readings; flawed clips are DSP edits of them with analytic labels. No human has "
             "listened to the flawed clips; labels are exact for the edits, not human judgements.", "",
             f"Pipeline version {manifest['pipeline']['version']}. Audio: 16 kHz mono PCM16 WAV.", "",
             "| id | split | speaker | passage (s) | words | licence basis | source |", "|---|---|---|---|---|---|---|"]
    for e in manifest["baselines"] + manifest["readers"]:
        lines.append(f"| {e['id']} | {e['split']} | {e.get('speaker', '')} | {e['duration_s']} | {e['n_words']} | {e['licence_basis']} | "
                     f"{e['licence_url']} |")
    lines += ["", f"Flawed clips: {sum(not c.get('missing') for c in manifest['clips'])} (core and extra single-level, identity / placebo, ladder G1 / G3 / G5, cross-speaker edits, and extra family botched readings); "
              f"files: {manifest['counts']['files']}.", "", "Labels (`labels/<clip>.json`) hold the parent hash, recipe, seed, chain, word alignment "
              "carried through the analytic time map, and per flaw: type, dimension, level, physical magnitude, realised change, expected "
              "secondary dimensions, word span, and half-open sample spans in the clip and in the parent."]
    lines += ["", "Coverage is capped at 35 % edited-word coverage (boundary edits excluded; G5, identity and extra family botched clips exempt).",
              "Edit-support time shares are separate and include boundary edits and release supports.",
              "Recipe names label controlled acoustic departures from the reference rendition; Clarity (spectral-change proxy) does not measure intelligibility.",
              "Scores are a reference-relative delivery index.", "", "| clip | edit-support time share |", "|---|---|"]
    lines += [f"| {c['id']} | {c['edit_support_time_share']:.1%} |" for c in manifest["clips"] if not c.get("missing")]
    from collections import Counter
    counts = Counter((c["split"], f["type"], f["level"]) for c in manifest["clips"]
                     if not c.get("missing") for f in json.loads((path.parent / c["labels"]).read_text())["flaws"] if not f["placebo"])
    lines += ["", "| type | family / primary | secondary | event |", "|---|---|---|---|"]
    lines += [f"| {t} | {r['family']} | {', '.join(r['secondary'])} | {r['event']} |" for t, r in C.FLAW_REGISTRY.items()]
    lines += ["", "| split | type | L1 | L2 | L3 |", "|---|---|---|---|---|"]
    lines += [f"| {sp} | {t} | " + " | ".join(str(counts[(sp, t, lv)]) for lv in C.LEVELS) + " |"
              for sp in sorted({c["split"] for c in manifest["clips"]}) for t in C.FLAW_TYPES]
    lines += ["", "| split | clips | minutes | extra clips | extra minutes |", "|---|---|---|---|---|"]
    for sp in sorted({c["split"] for c in manifest["clips"]}):
        clips = [c for c in manifest["clips"] if c["split"] == sp]
        extra = [c for c in clips if c.get("spectrum") == "extra"]
        lines.append(f"| {sp} | {len(clips)} | {sum(c.get('duration_s', 0) for c in clips) / 60:.2f} | {len(extra)} | {sum(c.get('duration_s', 0) for c in extra) / 60:.2f} |")
    if manifest.get('r2_pool'):
        lines += ['', '| null group | fit | select | lockbox | minutes |', '|---|---|---|---|---|']
        for g in manifest['r2_pool']['groups']:
            lines.append(f"| {g['id']} | " + ' | '.join(str(len(g['sets'][s])) for s in ('fit', 'select', 'lockbox')) +
                         f" | {sum(g['minutes'].values()):.2f} |")
        lines += ['', 'R2 partition SHA-256: ' + manifest['r2_pool']['split_sha256'],
                  manifest['r2_pool']['crop_rule'],
                  'Gettysburg v10 required every sentence endpoint in greedy ASR. The CPU replay of all 19 readers failed this rule despite 89.7–97.4% overall coverage; FOUR was unanchored in 16, EARTH in 15, and the can-not clause failed in 19. The null crop now uses outer passage anchors and overall coverage, then checks alignment.',
                  'EARS readers were seen by the lab and have no lockbox; lockbox source coverage differs from fit. No missing source is assigned a zero false rate. Lockbox preparation is deferred.',
                  '', '| excluded null reading | reason |', '|---|---|']
        lines += [f"| {r['id']} | {r['reason']} |" for r in manifest['r2_pool']['excluded']]
        accent = [r for g in manifest['r2_pool']['groups'] for r in g['entries'] if r.get('source') == 'accent']
        composition = Counter((r.get('first_language','unknown'),r.get('lab_seen',False),r['null_set']) for r in accent)
        lines += ['', 'Accent is stratified by first language and lab-seen status, with integer rounding per stratum. The Accent lockbox includes lab-seen readers to match composition; it is not an unseen-lab estimate.',
                  '', '| first language | lab seen | fit | select | lockbox |', '|---|---|---|---|---|']
        for language, seen in sorted({(r.get('first_language','unknown'),r.get('lab_seen',False)) for r in accent}):
            lines.append(f"| {language} | {seen} | " + ' | '.join(str(composition[language,seen,phase]) for phase in ('fit','select','lockbox')) + ' |')
        pool = manifest['r2_pool']
        lines += ['', '| source | fit/select attempted | excluded | exclusion rate | reasons / rule |', '|---|---|---|---|---|']
        for source, attempted in sorted(pool.get('crop_attempts_by_source', {}).items()):
            excluded = [r for r in pool['excluded'] if r.get('source', r.get('group', '').split(':')[0]) == source and
                        r['reason'].startswith(('text not located:', 'located text failed alignment:'))]
            reasons = dict(Counter(r['reason'] for r in excluded))
            rule = 'whole passage; no text-location exclusion' if source in ('ears', 'accent', 'vctk') else 'spoken introductions/closings removed; failed anchors or alignment are recorded'
            lines.append(f"| {source} | {attempted} | {len(excluded)} | {len(excluded)/attempted:.1%} | {reasons}; {rule} |")
        lines += ['', 'Inventory exclusions (before fit/select crop; separate denominator):',
                  '| source | inventoried readings | inventory exclusions | rate | reasons |', '|---|---|---|---|---|']
        for source, count in sorted(pool.get('inventoried_by_source', {}).items()):
            excluded = [r for r in pool['excluded'] if r.get('group', '').split(':')[0] == source and
                        not r['reason'].startswith(('text not located:', 'located text failed alignment:'))]
            lines.append(f"| {source} | {count} | {len(excluded)} | {len(excluded)/count:.1%} | {dict(Counter(r['reason'] for r in excluded))} |")
        lines += ['', 'Missing independent prompts: ' + json.dumps(pool.get('missing', []), sort_keys=True)]
    from .edits_extra import RECIPE_EVIDENCE
    lines += ["", "Sources: build/work/research/chain/{pace_pauses,disfluency,pitch_emphasis,volume_clarity}/REPORT.md §4; "
              "SYNTHESIS.md §4; alpha coupling from volume_clarity §2.1. Numeric signal gates, jitter, fit tolerances and release are engineering choices.",
              "", "| extra type | family / primary | L1 / L2 / L3 named parameters (s, dB, st, factors) | source / chosen values | approximation / omissions |",
              "|---|---|---|---|---|"]
    for typ in C.EXTRA_TYPES:
        r = C.FLAW_REGISTRY[typ]
        source, approximation = RECIPE_EVIDENCE[typ]
        params = " / ".join(", ".join(f"{k}={v:.6g}" for k, v in p.items()) for p in r["levels"])
        lines.append(f"| {typ} | {r['family']} / {r['primary']} | {params} | {source} | {approximation} |")
    plans = manifest.get("extra_plans", [c for c in manifest["clips"] if c.get("spectrum") == "extra"])
    planned, placed, reasons, measured = Counter(), Counter(), {}, {}
    for c in plans:
        for request in c.get("requested", []):
            planned[(c["regime"], c["split"], request["type"], request["level"])] += 1
        for skip in c.get("skipped", []):
            cell = (c["regime"], c["split"], skip["type"], skip["level"])
            reasons.setdefault(cell, Counter())[skip["reason"]] += 1
    approximations = set()
    for c in manifest["clips"]:
        if c.get("spectrum") != "extra" or c.get("missing"):
            continue
        for f in json.loads((path.parent / c["labels"]).read_text())["flaws"]:
            cell = (c["regime"], c["split"], f["type"], f["level"])
            placed[cell] += 1
            r = f["realised"]
            if r.get("value") is not None:
                measured.setdefault(cell, []).append((r["value"], r["unit"]))
            approximations.add((f["type"], json.dumps(f["approximation"], sort_keys=True)))
    axes = sorted({(c["regime"], c["split"]) for c in plans})
    cells = [(regime, split, t, lv) for regime, split in axes for t in C.EXTRA_TYPES for lv in C.LEVELS]
    lines += ["", "Placement counts include extra family botched instances. Empty cells are retained.",
              "| regime | split | type | level | planned | placed | skipped by reason | placement Wilson 95% |",
              "|---|---|---|---|---|---|---|---|"]
    for cell in cells:
        n, k = planned[cell], placed[cell]
        if n:
            from .uncertainty import wilson
            lo,hi = wilson(k,n)
            interval = f"{lo:.3f}–{hi:.3f}"
        else:
            interval = "unplanned"
        lines.append("| " + " | ".join(map(str, cell)) + f" | {n} | {k} | {dict(reasons.get(cell, {}))} | {interval} |")
    empty = [cell for cell in cells if cell[1] in ("val", "test", "check", "lockbox") and placed[cell] == 0]
    lines += ["", "Empty held-out cells: " + ("; ".join("/".join(map(str, c)) + (" (unplanned)" if not planned[c] else " (skipped)")
                                                       for c in empty) or "none in the supplied trial/build splits"),
              "", "| regime | split | type | level | n | realised median | unit | median bootstrap 95% |",
              "|---|---|---|---|---|---|---|---|"]
    for cell in cells:
        samples = measured.get(cell, [])
        values = np.array([v for v, _ in samples])
        median = f"{np.median(values):.6g}" if len(values) else "missing"
        interval = "insufficient n" if len(values) < 3 else "–".join(f"{v:.6g}" for v in np.percentile(
            np.median(np.random.default_rng(0).choice(values, (1000, len(values))), axis=1), [2.5, 97.5]))
        lines.append("| " + " | ".join(map(str, cell)) + f" | {len(values)} | {median} | {samples[0][1] if samples else '—'} | {interval} |")
    issues = manifest.get("realisation_shortfalls", [dict(q, clip=c["id"]) for c in manifest["clips"]
                                                    for q in c.get("realisation_qa", []) + c.get("ladder_qa", [])])
    lines += ["", "Realisation shortfalls (wrong sign, below half target, coupling, or non-monotone ladder):"]
    lines += ["- " + json.dumps(q, sort_keys=True) for q in issues] or ["- none"]
    lines += ["", "Realised label approximations:"]
    lines += [f"- {t}: {approx}" for t, approx in sorted(approximations)]
    if manifest.get("reader_placement_probe"):
        lines += ["", "R2 planning-only probe; no reader audio rendered. Selection is not acoustic realisation.",
                  "| reader | split | type | planned levels | selected levels | stress fallback / skip |",
                  "|---|---|---|---|---|---|"]
        for r in manifest["reader_placement_probe"]:
            for typ, info in r.get("types", {}).items():
                lines.append(f"| {r['reader']} | {r['split']} | {typ} | {info['requested_levels']} | {info['selected_levels']} | {info['selection'] or info['reason']} |")
            if r.get("reason") or r.get("limitation"):
                lines.append(f"{r['reader']}: {r.get('reason', r.get('limitation'))}")
    lines += ["", "Extra L1–L3 share a placement plan per parent and set; botched family clips use repeated L3 edits and longer windows.",
              "Wrong-sign, below-half-target, missing-measurement and non-monotone edits are excluded from evaluation truth and h selection; counts are reported in a separate shortfall stratum. Coupling warnings alone remain eligible for level-only evaluation.",
              "Burst/continuant signal gates are heuristic; skipped placements record missing acoustic eligibility.",
              f"Total audio minutes (including clean recordings): {manifest['counts']['minutes']}. Filled pauses are excluded."]
    path.write_text("\n".join(lines) + "\n")


def dsp_task(kind: str, rec: Recording, entry: dict, out: Path, ref: Recording | None = None, baseline_id: str | None = None) -> list[dict]:
    """Clip generation of one speech (CPU work; a pool worker runs it): the ten clips of a baseline, or the cross-speaker
    clips of one reader against the reference B."""
    if kind == "extra_cross":
        return build_extra_clips(rec, entry, out, ref=ref, baseline_id=baseline_id)
    return build_baseline_clips(rec, entry, out) if kind == "baseline" else build_cross_clips(rec, ref, entry, baseline_id, out)


def as_null_reader(row: dict, text: str) -> dict:
    """A project reader in the R2 null pool reads the corpus text; its stored word fields belong to the old text."""
    stale = ('sentence', 'n_sentences', 'n_words')
    return {**{k: v for k, v in row.items() if k not in stale}, 'text': text, 'role': 'null_reader'}


def build_null_pool(mount: Path, project_readers: list[dict], root: Path) -> dict:
    from .r2pool import corpus_rows, copy_audio, inventory, reader_id
    from .lab.data import select
    prompts = json.loads(Path(__file__).with_name('null_prompts.json').read_text())
    rows, missing = corpus_rows(mount, prompts)
    raw = json.loads((mount / 'manifest.json').read_text())
    # Lab selection ids are data-only provenance. No measurements or lab verdicts enter this split.
    selected, _, _ = select(raw)
    seen = {reader_id(r) for r in selected if r.get('speaker_id')}
    provenance = json.loads(Path(__file__).with_name('null_lab_readers.json').read_text())
    seen.update(provenance['readers'])
    seen.update(reader_id(r) for r in raw if r['source'] == 'gettysburg')
    seen.update(reader_id(r) for r in project_readers)
    text = next(r['text'] for r in rows if r['source'] == 'gettysburg')
    rows += [as_null_reader(r, text) for r in project_readers]
    pool = inventory(rows, seen)
    pool['lab_provenance'] = provenance
    pool['corpus_manifest_sha256'] = sha256_file(mount / 'manifest.json')
    pool['missing'] = missing
    pool['vctk'] = 'mounted; optional group deferred'
    for g in pool['groups']:
        for r in g['entries']:
            r.update(audio=f"readers/{r['id']}.wav", split=r['null_set'], role='null_reader',
                     n_words=len(parse_transcript(r['text'])))
        if any(g['reference_shortfalls'].values()):
            log(f"R2 {g['id']}: fewer than five distinct references in {g['reference_shortfalls']}; seeded repeated draws")
        log(f"R2 {g['id']}: " + ', '.join(f"{s} {len(g['sets'][s])} readers {g['minutes'][s]:.2f} min" for s in g['sets']))
    log(f"R2 forecast: {pool['expected_alignment_seconds'] / 60:.1f} alignment minutes on T4 x2; "
        f"{len(pool['excluded'])} seeded exclusions; {len(missing)} missing prompts")
    # Written before any selected WAV is read or alignment/measurement is computed.
    (root / 'manifest.json').write_text(json.dumps({'schema': 1, 'r2_pool': pool}, indent=1, sort_keys=True) + '\n')
    copy_audio([r for g in pool['groups'] for r in g['entries'] if r['null_set'] != 'lockbox'], root)
    return pool


def crop_null_readers(root, null_pool, pool=None, aligner=None, phases=('fit', 'select'), write_manifest=True):
    """Locate and cut the texts of the `phases` sets before feature preparation; the build leaves lockbox audio untouched
    (calibrate.lockbox_pool crops it on a copy of the pool, without the manifest, in the final evaluation only)."""
    from .align import Alignment, TranscriptMismatch, require_match
    from .passages import cut_clip, window_of
    from .r2pool import partition_hash
    entries = [r for g in null_pool['groups'] for r in g['entries'] if r['null_set'] in phases]
    null_pool['crop_attempts_by_source'] = dict(Counter(r['source'] for r in entries))
    for r in entries:
        if r['source'] not in ('poetry', 'gettysburg'):
            r.update(clip_offset_s=0., clip_end_s=r['duration_s'], text_location='whole passage file; no crop or ASR exclusion')
    entries = [r for r in entries if r['source'] in ('poetry', 'gettysburg')]
    seconds = sum(r['duration_s'] for r in entries)
    log(f"R2 crop: {len(entries)} readings, {seconds / 60:.1f} source min; expected {seconds * C.R2_ALIGNMENT_SECONDS_PER_AUDIO / 60:.1f} min per emission/alignment pass on T4 x2; sets {', '.join(phases)}")
    for start in range(0, len(entries), C.R2_PREPARE_BATCH):
        batch = entries[start:start + C.R2_PREPARE_BATCH]
        wavs = [audio.read_wav(root / r['audio']) for r in batch]
        trs = [parse_transcript(r['text']) for r in batch]
        anchors = locate_many(wavs, trs, pool, aligner, True)
        jobs, pending = [], []
        for r, wav, tr, hints in zip(batch, wavs, trs, anchors):
            if not hints or not all(a.eligible for a in hints):
                null_pool['excluded'].append({'id': r['id'], 'group': r['group'], 'source': r['source'], 'reason': 'text not located: outer passage anchors or overall coverage below criterion'})
                r['crop_excluded'] = True
                continue
            _, window, offset = window_of(wav, tr, hints, 0, len(hints) - 1)
            jobs.append(make_job(window, tr, 'align'))
            pending.append((r, wav, offset, hints))
        for (r, wav, offset, hints), al in zip(pending, run_jobs(jobs, pool, aligner)):
            try:
                require_match(al)
            except TranscriptMismatch as e:
                null_pool['excluded'].append({'id': r['id'], 'group': r['group'], 'source': r['source'], 'reason': 'located text failed alignment: ' + str(e)})
                r['crop_excluded'] = True
                continue
            source_al = Alignment(al.start + offset, al.end + offset, al.compat, al.mean_compat)
            clip, sample = cut_clip(wav, source_al)
            r.update(source_duration_s=r['duration_s'], source_sha256=r['sha256'],
                     source_start_s=float(source_al.start[0]), source_end_s=float(source_al.end[-1]),
                     clip_offset_s=sample / C.SR, clip_end_s=(sample + len(clip)) / C.SR,
                     duration_s=len(clip) / C.SR, crop_anchor_min_coverage=min(a.coverage for a in hints))
            audio.write_wav(root / r['audio'], clip)
            r['sha256'] = audio.sha256_pcm(clip)
            r['sha256_basis'] = 'pcm'
        log(f"R2 crop: {min(start + len(batch), len(entries))}/{len(entries)} located; {len(null_pool['excluded'])} exclusions")
    null_pool['planned_split_sha256'] = null_pool['split_sha256']
    for g in null_pool['groups']:
        g['entries'] = [r for r in g['entries'] if not r.get('crop_excluded')]
        for phase in g['sets']:
            kept = [r for r in g['entries'] if r['null_set'] == phase]
            g['sets'][phase] = sorted(r['id'] for r in kept)
            g['minutes'][phase] = sum(r['duration_s'] for r in kept) / 60
            g['reference_shortfalls'][phase] = len(kept) if 0 < len(kept) <= C.R2_REFERENCES else 0
    null_pool['split_sha256'] = partition_hash(null_pool['groups'])
    null_pool['crop_rule'] = 'LibriVox poetry/Gettysburg only: outer passage anchors, overall coverage, require_match, first/last word +/- CLIP_PAD_S; EARS/Accent/VCTK whole; lockbox deferred'
    if write_manifest:
        (root / 'manifest.json').write_text(json.dumps({'schema': 1, 'r2_pool': null_pool}, indent=1, sort_keys=True) + '\n')


def prepare_null_readers(ds: Dataset, entries: list[dict], retain=True, keep_audio=False) -> None:
    for start in range(0, len(entries), C.R2_PREPARE_BATCH):
        batch = entries[start:start + C.R2_PREPARE_BATCH]
        ds.recs(batch)
        for e in batch:
            if not retain:
                ds._recs.pop(e['id'], None)
            elif not keep_audio:
                ds._recs[e['id']] = dataclasses.replace(ds._recs[e['id']], wav=None)


def build(sources: Path, out: Path, cache: Path | None, pool=None, aligner=None) -> dict:
    root = Path(out) / "dataset"
    root.mkdir(parents=True, exist_ok=True)
    from .r2pool import find_mount
    mount = find_mount('cvoice-data')
    find_mount('cvoice-data-vctk')  # optional VCTK group is deferred
    planned = []
    baselines, readers = build_clean(load_sources_manifest(), Path(sources), root, pool, aligner, [],
                                    lambda rows: planned.append(build_null_pool(mount, rows, root)))
    null_pool = planned[0]
    return finish(root, baselines, readers, cache, pool, aligner, null_pool)


def finish(root: Path, baselines: list[dict], readers: list[dict], cache: Path | None, pool=None, aligner=None, null_pool=None) -> dict:
    """Flawed clips, cross-speaker clips, manifest, dataset card and label QA for the clean passages already written. Batches:
    every clean recording is analysed at once, the clips of different speeches are generated in parallel, and every clip
    is re-aligned in one batch for label QA. The final manifest is written before QA (QA never decides what exists)."""
    manifest = {"schema": 1, "pipeline": {"version": __version__, "alignment_device": device_class(pool)}, "registry_version": C.REGISTRY_VERSION, "baselines": baselines,
                "readers": readers, "clips": [], "shortfalls": []}
    if null_pool is not None:
        crop_null_readers(root, null_pool, pool, aligner)
        manifest['r2_pool'] = null_pool
        readers.extend(r for g in null_pool['groups'] for r in g['entries'])
    (root / "manifest.json").write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")  # splits fixed before preparation
    ds = Dataset(root, manifest, cache, pool, aligner)
    ds.recs(baselines + [r for r in readers if not r.get('null_set')])
    prepare_null_readers(ds, [r for r in readers if r.get('null_set') in ('fit', 'select')], retain=False)
    ref = ds.rec(ds.entry("readers", GETTYSBURG_REFERENCE))
    tasks = [("baseline", ds.rec(b), b, root) for b in baselines]
    for r in readers:
        if r.get("role") == "reader_check":
            tasks.append(("cross", ds.rec(r), r, root, ref, GETTYSBURG_REFERENCE))
        elif r.get("role") == "reader_calibration":
            tasks.append(("extra_cross", ds.rec(r), r, root, ref, GETTYSBURG_REFERENCE))
        elif r.get("role") == "orator_reference":
            tasks.append(("cross", ds.rec(r), r, root, ds.rec(ds.entry("baselines", r["paired_baseline"])), r["paired_baseline"]))
    log(f"clip generation: {len(tasks)} speeches; expected 5-7 min on T4 x2 (v9: 19 speeches in 294 s)")
    for rows in map_calls(dsp_task, tasks, pool):
        manifest["clips"] += rows
    manifest["extra_plans"] = [{k: c[k] for k in ("id", "parent", "regime", "split", "kind", "requested", "skipped")}
                               for c in manifest["clips"] if c.get("spectrum") == "extra"]
    manifest["realisation_shortfalls"] = [dict(q, clip=c["id"]) for c in manifest["clips"]
                                           for q in c.get("realisation_qa", []) + c.get("ladder_qa", [])]
    manifest["shortfalls"] = [{"clip": c["id"], "skipped": c["skipped"]} for c in manifest["clips"] if c.get("skipped")]
    manifest["clips"] = sorted([c for c in manifest["clips"] if not c.get("missing")], key=lambda c: c["id"])
    manifest["counts"] = {"baselines": len(baselines), "flawed": len(manifest["clips"]), "readers": len(readers),
                          "files": len(baselines) + len(manifest["clips"]) + len(readers),
                          "minutes": round(sum(e["duration_s"] for e in baselines + readers + manifest["clips"] if "duration_s" in e) / 60, 1)}
    (root / "manifest.json").write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
    write_card(manifest, root / "dataset_card.md")
    log(f"label QA: re-aligning {len(manifest['clips'])} clips; expected {len(manifest['clips']) / 8.9:.0f} s on T4 x2 (v9 throughput)")
    als = run_jobs([make_job(ds.wav(c), ds.clip_transcript(c), "align") for c in manifest["clips"]], pool, aligner, cache)
    qa = [label_qa(ds, c, al) for c, al in zip(manifest["clips"], als)]
    (root / "label_qa.json").write_text(json.dumps({"clips": qa, "all_outside_support_identical": all(q["outside_support_identical"] for q in qa)},
                                                   indent=1, sort_keys=True) + "\n")
    log(f"done: {manifest['counts']}; shortfalls: {len(manifest['shortfalls'])}")
    return manifest


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="python -m cvoice.dataset")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="build the dataset from the staged sources")
    b.add_argument("--sources", type=Path, default=Path("/kaggle/input/cvoice-sources"))
    b.add_argument("--out", type=Path, default=ROOT / "data")
    b.add_argument("--cache", type=Path, default=None, help="alignment cache directory (shared with calibrate / evaluate)")
    a = ap.parse_args(argv)
    with PreparePool(cache_dir=a.cache) as pool:
        build(a.sources, a.out, a.cache, pool)


if __name__ == "__main__":
    main()
