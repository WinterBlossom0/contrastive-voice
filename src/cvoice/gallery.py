"""Static gallery (Kaggle): result JSON + audio for the bundled examples of the dashboard, plus gallery/index.json.

    python -m cvoice.gallery --dataset /kaggle/working/data --models /kaggle/working/out/models/detector.json \
        --cache /kaggle/working/cache --eval /kaggle/working/out/eval --out /kaggle/working/out

    python -m cvoice.gallery site OUT_DIR [--gallery DIR]     one folder for GitHub Pages: the static page + the gallery data

Examples (one speech): identity, L1-L3 clips (L3A also without a reference reading: SELF), G1 / G3 / G5, the unedited
Greenman-vs-Reagan pair and one channel condition; then one example per new capability (SHOWCASE) and one R2 example with listed entries, chosen by
rule from the train and val clips. A second bundled text, the Gettysburg passage, carries a reference bank (`bank_readers`) and one
R2 example in consensus mode: a check reader's edited clip against the median of five bank readings. A capability that no clip shows through an evaluator-matched finding is left out and
named in index.json `left_out`; each shown example names the finding it opens on (`focus`). A bundled dataset clip against
its own baseline is R1, the SELF twin has no baseline, and anything else is R2. Each truth marker carries the finding that the evaluation's own matching
assigns to it; an edit that the evaluation excludes has a marker with its exclusion reasons and no match.
"""
from __future__ import annotations

import argparse
import json
import shlex
import shutil
import sys
from pathlib import Path

import numpy as np

from . import audio, patterns, selfref, stress
from . import config as C
from .dataset import GETTYSBURG_REFERENCE, load_dataset, sha256_file
from .detect import decode, key, load_detector
from .evaluate import cross_matches, listed_rank
from .events import Run, match, on_shortfall, run_pair, truth_changes, truths, whole_passage
from .pipeline import ROOT, analyze, detector_status, device_class, dumps, self_detector_status
from .pool import PreparePool
from .r2pool import reader_id
from .reference import select_reference

STATIC = Path(__file__).parent / "static"
GALLERY_BASELINE = "reagan_farewell_1989"
SHOWCASE_SPLITS = ("train", "val")  # never a test clip
SHOWCASE_GROUP = "New flaw families"
BANK_ID = "gettysburg_address"
BANK_TITLE = "Gettysburg Address (passage)"
BANK_LICENCE = "LibriVox public domain"
# Check readers' clips carry the split "check": the development R2 evaluation, never the test split.
CONSENSUS_SPLITS = (*SHOWCASE_SPLITS, "check")
SELF_EXAMPLE = "L3A"  # the example that the gallery also shows graded without a reference reading
SELF_LIMITS = ("Without a reference, some flagged spots may be natural phrasing, and a problem that runs through the whole "
               "reading is not found.")


def _family(name: str) -> set[str]:
    return {t for t, spec in C.FLAW_REGISTRY.items() if spec["family"] == name}


def _labelled(f: dict, t: dict) -> bool:
    """The finding carries the edit's own name as its type, pattern or group pattern."""
    return t["type"] in (f.get("type"), f.get("pattern"), f.get("group_pattern"))


# One R1 example per new capability: an injected edit of `types` whose evaluator-matched finding f passes shows(f, edit).
# `needs` names that finding in the log and in the index note of a left-out example.
SHOWCASE = (
    {"id": "disfluency", "label": "Disfluency", "title": "Disfluency edits: a word-time finding", "needs": "a word-time (D7) finding",
     "types": _family("DISFLUENCY"), "shows": lambda f, t: f["dimension"] == "D7"},
    {"id": "hesitation", "label": "Hesitation group", "title": "Hesitation and word-by-word edits: a finding group",
     "needs": "a finding group with the edit's name", "types": {"HESITATION", "WORD_BY_WORD"},
     "shows": lambda f, t: bool(f.get("group")) and f.get("group_pattern") == t["type"]},
    {"id": "natural_rush", "label": "Natural rushing", "title": "Natural-rushing edit: a finding with that label",
     "needs": "a finding labelled natural rushing", "types": {"NATURAL_RUSH"}, "shows": _labelled},
    {"id": "low_effort", "label": "Low vocal effort", "title": "Low-vocal-effort edit: a finding with that label",
     "needs": "a finding labelled low vocal effort", "types": {"LOW_EFFORT"}, "shows": _labelled},
)


# The R2 consensus example: any injected edit whose evaluator-matched finding exists, against the reference bank.
CONSENSUS_SHOWCASE = {"id": "r2_consensus", "label": "Median of five", "title": "Edited reading vs the median of five readers",
                      "types": set(C.FLAW_REGISTRY), "shows": lambda f, t: True}


def log(msg: str) -> None:
    print(f"[gallery] {msg}", flush=True)


def finding_ids(run: Run, regions: list, reg: dict, flaws: list[dict]) -> dict[int, str]:
    """Finding id of each decoded region. The result keeps no region index, so a region is found by the dimension, words and
    span that the pipeline's own pattern description gives it."""
    local = [f for f in flaws if f["context"] != "whole passage"]
    out = {}
    for j, r in enumerate(regions):
        info = patterns.describe(r, run.comp, run.B, run.P, reg.get("pattern_labels"))
        same = [f for f in local if f["dimension"] == r.dim and f["words"] == [int(w) for w in info["words"]]]
        if same:
            out[j] = min(same, key=lambda f: abs(f["p"][0] - float(info["p"][0])) + abs(f["p"][1] - float(info["p"][1])))["id"]
    return out


def truth_markers(lab: dict, B, P, det: dict, regime: str, res: dict, clean=None, with_excluded: bool = False) -> list[dict]:
    """Injected-truth markers (participant seconds) of a labelled clip, each with the finding that the evaluation matches to it
    (events.match in R1; evaluate.cross_matches against the unedited parent `clean` in R2), else its same-change detection
    (events.truth_changes, flag `same_change`), or None; `duplicate_findings` are the other findings of the same change. A whole-clip flag of the
    edit's dimension and direction matches a whole-clip truth or a whole-passage edit. R2 markers also carry the unscored
    difference of the edit: for a whole-clip truth or a whole-passage edit the whole-passage difference of its dimension and
    direction, else the one that evaluate.listed_rank ranks. with_excluded appends excluded_markers with the findings on them."""
    reg = det["regimes"][regime]
    run = run_pair(B, P, det, regime)
    if clean is None:
        regions, clips = run.regions, set(run.clip)
    else:
        regions, _, clips = cross_matches(run_pair(B, clean, det, regime), run, truths(lab, enabled=reg["enabled"]), reg)
    return run_markers(lab, run, regions, clips, reg, res, lambda dim: detector_status(dim, reg), with_excluded)


def self_truth_markers(lab: dict, P, res: dict, with_excluded: bool = False) -> list[dict]:
    """Truth markers of a SELF result: the matching of truth_markers on the shipped SELF detector's run. No listed entry is
    linked, because a SELF listed entry is context of the reading, not a difference from a reference."""
    det = selfref.load_default()
    reg = det["regime"]
    comp = selfref.self_comparison(P, det["text_model"])
    regions = decode(comp, reg, P.tr.sentence)
    return run_markers(lab, selfref.self_run(P, comp, regions), regions, set(), reg, {**res, "differences": []},
                       lambda dim: self_detector_status(dim, reg), with_excluded)


def run_markers(lab: dict, run: Run, regions: list, clips: set, reg: dict, res: dict, status, with_excluded: bool) -> list[dict]:
    """The markers of truth_markers from a run, its matched regions, its whole-clip flag dimensions `clips` and the regime's
    status of a dimension, status(dim)."""
    tr = truths(lab, enabled=reg["enabled"])
    pairs = match(tr, run.with_regions(regions))
    same_change, duplicates = truth_changes(run.with_regions(regions), tr, pairs)
    ids = finding_ids(run, regions, reg, res["flaws"])
    whole_clip = {f["dimension"]: f["id"] for f in res["flaws"] if f["context"] == "whole passage"}
    out = []
    for i, t in enumerate(tr):
        by_clip = isinstance(same_change.get(i), str)
        if i in pairs:
            finding = ids.get(pairs[i])
        elif by_clip:
            finding = whole_clip.get(t["dim"])
        elif i in same_change:
            finding = ids.get(same_change[i])
        else:
            finding = None
        target = key(t["dim"], t["sign"]) if t["sign"] else None
        shared = sorted({ids[d["index"]] for d in duplicates if d["change"] == target and d["index"] in ids
                         and patterns.within_half_window(regions[d["index"]], t["words"])})
        clip_truth = whole_passage(t, len(run.P.tr))
        if finding is None and clip_truth and t["dim"] in clips and t["sign"] in (0, int(np.sign(run.clip[t["dim"]]))):
            finding = whole_clip.get(t["dim"])
        difference = whole_passage_difference(res["differences"], t) if clip_truth else None
        if difference is None and res["differences"]:
            rank = listed_rank(res["differences"], t)
            difference = None if rank is None else res["differences"][rank - 1]["id"]
        out.append({"type": t["type"], "dimension": t["dim"], "level": t["level"], "available": bool(t["available"]),
                    "detector_status": status(t["dim"]),
                    "p": [round(float(t["span"][0]), 3), round(float(t["span"][1]), 3)], "words": [int(w) for w in t["label_words"]],
                    "finding": finding, "same_change": i in same_change and i not in pairs and not by_clip, "duplicate_findings": shared,
                    "difference": difference})
    if with_excluded:
        out += excluded_markers(lab, reg, regions, ids, status)
    return out


def excluded_markers(lab: dict, reg: dict, regions: list = (), ids: dict[int, str] | None = None, status=None) -> list[dict]:
    """Markers of the injected edits that the evaluation excludes (their realised change failed the label checks), with the
    reasons in `excluded`. They match nothing; they show where an edit changed the recording, so a flag there is explained.
    `on_edit` names the findings (ids: finding_ids of `regions`) that events.on_shortfall, the evaluation's rule, puts on the edit."""
    ids = ids or {}
    status = status or (lambda dim: detector_status(dim, reg))
    return [{"type": t["type"], "dimension": t["dim"], "level": t["level"], "available": bool(t["available"]),
             "detector_status": status(t["dim"]), "p": [round(float(t["span"][0]), 3), round(float(t["span"][1]), 3)],
             "words": [int(w) for w in t["label_words"]], "finding": None, "difference": None, "excluded": list(t["exclusion_reasons"]),
             "on_edit": sorted(ids[j] for j, r in enumerate(regions) if j in ids and on_shortfall(r, [t]))}
            for t in truths(lab, excluded=True, enabled=reg["enabled"])]


def whole_passage_difference(differences: list[dict], t: dict) -> str | None:
    """Id of the whole-passage difference of the edit's dimension and direction (any direction for an unsigned edit), or None."""
    return next((d["id"] for d in differences if d["words"] is None and d["dimension"] == t["dim"]
                 and (t["sign"] == 0 or (d["delta"] > 0) == (t["sign"] > 0))), None)


def showcase_clips(manifest: dict, regime: str) -> list[dict]:
    """Clips that can show a new capability: extra-spectrum edits of the regime from the train or val split, the strongest
    level first, then by id (a stable order for every dataset build)."""
    kinds = ("single",) if regime == "R1" else ("cross", "extra_botched")
    pool = [c for c in manifest["clips"] if c.get("spectrum") == "extra" and c["kind"] in kinds and c["regime"] == regime
            and c["split"] in SHOWCASE_SPLITS]
    return sorted(pool, key=lambda c: (-max(c.get("levels") or [0]), c["id"]))


def shown(spec: dict, res: dict) -> list[dict]:
    """Findings of `res` that show the capability of `spec`: each one is the finding that the evaluation matches to an
    injected edit of the spec's types, and it passes the spec's test for that edit. A finding elsewhere on the clip never
    counts, because the example would then show a cause away from its edit."""
    flaws = {f["id"]: f for f in res["flaws"]}
    return [flaws[t["finding"]] for t in res["truth"]
            if t["type"] in spec["types"] and t["finding"] in flaws and spec["shows"](flaws[t["finding"]], t)]


def pick_showcase(candidates: list[tuple[dict, dict]], specs=SHOWCASE) -> dict[str, tuple[dict, dict]]:
    """Spec id -> (clip, result): per spec the first candidate (in showcase_clips order) that `shown` accepts. A spec that
    no candidate shows has no entry."""
    out = {}
    for spec in specs:
        hit = next(((c, r) for c, r in candidates if shown(spec, r)), None)
        if hit:
            out[spec["id"]] = hit
            log(f"{spec['id']}: {hit[0]['id']}")
    return out


def left_out_reason(spec: dict) -> str:
    names = sorted(t.replace("_", " ").lower() for t in spec["types"])
    edits = names[0] if len(names) == 1 else f"{', '.join(names[:-1])} or {names[-1]}"
    return f"no train or val clip has an injected {edits} edit that the evaluation matches to {spec['needs']}"


def reader_identity(entry: dict) -> str:
    """LibriVox identity of a project Gettysburg reader: r2pool.reader_id of its source file, as its R2 null-pool entry has it."""
    return reader_id({"source": "gettysburg", "speaker_id": Path(entry["source"]["file"]).stem})


def bank_readers(manifest: dict) -> list[dict]:
    """Reference bank of the bundled Gettysburg passage: the project's R2 calibration readers. A reader whose identity is a
    check reader's or sits in the R2 lockbox never enters, nor does a test-split reading. The fit-set readings of the null
    pool read the whole address, a different text from the check clips, so they cannot enter. Order: the dataset's
    cross-speaker reference reader first (display exemplar and single-reference fallback), then by id."""
    project = [r for r in manifest["readers"] if r.get("role") in ("reader_calibration", "reader_check")]
    check = {reader_identity(r) for r in project if r["role"] == "reader_check"}
    lockbox = {e["reader_id"] for g in manifest.get("r2_pool", {}).get("groups", []) for e in g["entries"] if e["null_set"] == "lockbox"}
    bank = [r for r in project if r["role"] == "reader_calibration" and r.get("split") not in ("test", "lockbox")
            and reader_identity(r) not in check | lockbox]
    bank.sort(key=lambda r: (r["id"] != GETTYSBURG_REFERENCE, r["id"]))
    if len(bank) < C.CONSENSUS_K:
        raise ValueError(f"the Gettysburg bank has {len(bank)} calibration readings; consensus mode needs {C.CONSENSUS_K}")
    if len({r["text"] for r in bank}) != 1:
        raise ValueError("the Gettysburg bank readings do not share one text")
    return bank


def bank_meta(bank: list[dict]) -> dict:
    """Index entry of the bank: transcript, the exemplar's audio, and every reading with its reader and licence."""
    return {"id": BANK_ID, "title": BANK_TITLE, "text": bank[0]["text"], "audio": f"audio/{bank[0]['id']}.wav",
            "mode": "bank", "consensus_k": C.CONSENSUS_K,
            "references": [{"id": r["id"], "reader": r["speaker"], "audio": f"audio/{r['id']}.wav", "licence": BANK_LICENCE,
                            "licence_basis": r["licence_basis"], "licence_url": r["licence_url"]} for r in bank]}


def consensus_clips(manifest: dict, bank: list[dict]) -> list[dict]:
    """Candidates of the consensus example: edited cross clips of check readers against the bank's exemplar, never a test
    clip, in showcase_clips order."""
    check = {r["id"] for r in manifest["readers"] if r.get("role") == "reader_check"}
    pool = [c for c in manifest["clips"] if c["kind"] == "cross" and c["regime"] == "R2" and c["split"] in CONSENSUS_SPLITS
            and c["parent"] in check and c["baseline"] == bank[0]["id"]]
    return sorted(pool, key=lambda c: (-max(c.get("levels") or [0]), c["id"]))


def mode_detector(refs: list, det: dict) -> tuple:
    """(reference recording, detector) of the pipeline's reference mode for this bank: the R2 regime is the one that
    select_reference picks, as the evaluation's consensus section does."""
    B, reg, _, _ = select_reference(refs, det, "R2")
    return B, {**det, "regimes": {**det["regimes"], "R2": reg}}


def listed_focus(res: dict) -> str | None:
    """Id of the listed entry that the R2 listed example opens on: the first one an injected edit links to, else the first."""
    listed = [d["id"] for d in res["differences"] if d["status"] == "listed"]
    linked = [t["difference"] for t in res["truth"] if t["difference"] in listed]
    return (linked or listed or [None])[0]


def listed_rank_key(res: dict) -> tuple:
    """R2 example order: a candidate label first, then injected edits found among the listed entries, then listed dimensions."""
    listed = [d for d in res["differences"] if d["status"] == "listed"]
    listed_ids = {d["id"] for d in listed}
    return (any(f.get("candidate") for f in [*res["flaws"], *res["differences"]]),
            sum(t["difference"] in listed_ids for t in res["truth"]), len({d["dimension"] for d in listed}), len(listed))


def pick_listed(candidates: list[tuple[dict, dict]]) -> tuple[dict, dict] | None:
    """The R2 example with listed, unscored entries: the best listed_rank_key, ties by showcase_clips order."""
    with_listed = [(c, r) for c, r in candidates if any(d["status"] == "listed" for d in r["differences"])]
    return max(with_listed, key=lambda cr: listed_rank_key(cr[1]), default=None)


def items() -> list[dict]:
    """Gallery list: id, picker group and label, title, description, source clip (or reader / channel source) and regime."""
    out = [{"id": "identity", "group": "Reference", "label": "Identity", "title": "Identity (placebo chain)", "description": "Every edit recipe run with null parameters: expected delivery index 100 and no acoustic departures.",
            "clip": f"{GALLERY_BASELINE}__identity"}]
    for lv in C.LEVELS:
        for j in "AB":
            out.append({"id": f"L{lv}{j}", "group": f"Level {lv}", "label": f"Set {j}", "title": f"Level {lv} recipe edits, set {j}", "description": f"Four injected recipe edits at level {lv} (see the truth markers).",
                        "clip": f"{GALLERY_BASELINE}__single_L{lv}{j}"})
    out += [{"id": "G1", "group": "Ladder", "label": "G1", "title": "Ladder G1", "description": "One level-1 recipe edit.", "clip": f"{GALLERY_BASELINE}__G1"},
            {"id": "G3", "group": "Ladder", "label": "G3", "title": "Ladder G3", "description": "Three level-2 recipe edits.", "clip": f"{GALLERY_BASELINE}__G3"},
            {"id": "G5", "group": "Ladder", "label": "G5", "title": "Ladder G5 (botched)", "description": "Whole-passage rush and flat pitch, dropped pauses, fades.", "clip": f"{GALLERY_BASELINE}__G5"}]
    for o in out:
        o["regime"] = "R1"
    reference = next(o for o in out if o["id"] == SELF_EXAMPLE)
    reference["self_version"] = f"{SELF_EXAMPLE}_self"
    out.insert(out.index(reference) + 1, self_item(reference))
    out.append({"id": "greenman", "group": "Other performance", "label": "Greenman", "title": "Unedited Greenman reading vs the Reagan recording",
                "description": "A different performance of the same text: regime R2, no injected recipe edits; the flags are reference departures.",
                "clip": None, "regime": "R2", "wav": ("readers", "greenman_reagan")})
    out.append({"id": "greenman_edited", "group": "Other performance", "label": "Greenman edited", "title": "Edited Greenman reading vs Reagan",
                "description": "Two recipe edits, a pause inside a phrase and a volume drop, on a different speaker's reading: regime R2.",
                "clip": "greenman_reagan__x3_L3", "regime": "R2"})
    out.append({"id": "greenman_botched", "group": "Other performance", "label": "Greenman botched", "title": "Botched Greenman reading vs Reagan",
                "description": "Whole-passage rush and flat pitch, dropped pauses, fades, on a different speaker: regime R2.",
                "clip": "greenman_reagan__G5", "regime": "R2"})
    out.append({"id": "channel_mp3", "group": "Channel", "label": "MP3 64 kbit/s", "title": "Channel condition: MP3 64 kbit/s", "description": "The identity clip after an MP3 round trip: expected silent.",
                "clip": None, "regime": "R1", "wav": ("channel", f"{GALLERY_BASELINE}__identity")})
    return out


def self_item(reference: dict) -> dict:
    """The SELF twin of a reference example: the same recording graded without a reference reading. Each of the two names
    the other (self_version, reference_version), and the twin shares the reference version's audio."""
    name = reference["label"][:1].lower() + reference["label"][1:]
    return {"id": reference["self_version"], "group": reference["group"], "label": f"{reference['label']}, no reference",
            "title": f"{reference['title']}, without a reference", "clip": reference["clip"], "regime": selfref.NAME,
            "reference_version": reference["id"],
            "description": f"The {name} recording graded without a reference reading, against the reader's own typical delivery; "
                           f"{name} shows the same recording graded against the reference."}


def item_audio(item: dict) -> str:
    """A SELF twin plays the audio of its reference version."""
    return f"audio/{item.get('reference_version', item['id'])}.wav"


def self_description(item: dict, lab: dict, res: dict) -> str:
    return f"{item['description']} {edits_text(lab, res)} {SELF_LIMITS}"


def index_entry(item: dict, res: dict, text: str, bundled: set[str]) -> dict:
    """The index.json entry of a written example. bundled: the baselines whose text the index carries (the single baseline
    and the bank's readings); an example against any other baseline, or without one (SELF), carries its own text."""
    b = res["baseline"].get("id")
    return {"id": item["id"], "group": item["group"], "label": item["label"], "title": item["title"], "description": item["description"],
            "regime": item["regime"], "result": f"results/{item['id']}.json", "audio": item_audio(item),
            "overall": res["scores"]["overall"], "n_flaws": len(res["flaws"]), "truth": len(res["truth"]),
            **({"baseline": b} if b is not None else {}), **({"text": text} if b not in bundled else {}),
            **{k: item[k] for k in ("focus", "self_version", "reference_version") if item.get(k)}}


# Points are shown at 2 decimals, so a loss below half a hundredth would show as 0.00.
MIN_SHOWN_POINTS = 0.005


def marker_outcome(t: dict, res: dict, linked: set[str]) -> str:
    """What the result shows for one evaluated truth marker; linked: linked_findings(res)."""
    if t["finding"]:
        return "found"
    if t["difference"]:
        differences = {d["id"]: d for d in res["differences"]}
        return "listed entry" if differences[t["difference"]]["status"] == "listed" else "unscored difference"
    if t["detector_status"] != "enabled":
        return "not scored"
    near = near_misses(t, res, linked)
    if near:
        return (f"missed: a {near[0]['type'].replace('_', ' ').lower()} finding lies on the edit but overlaps it by less than "
                f"the evaluation's {C.IOU_MIN:.0%} rule")
    return "missed"


def near_misses(t: dict, res: dict, linked: set[str]) -> list[dict]:
    """Findings that lie on a missed windowed edit (its dimension and direction, a shared word) but that the evaluation's
    overlap rule (events.match) does not match to it and no other marker links."""
    if t["finding"] or t["difference"] or t.get("excluded") or t["detector_status"] != "enabled" or C.is_event(t["dimension"]):
        return []
    sign = C.FLAW_REGISTRY[t["type"]]["sign"]
    w0, w1 = t["words"]
    return [f for f in res["flaws"] if f["id"] not in linked and f["dimension"] == t["dimension"] and f["words"]
            and f["words"][0] <= w1 and f["words"][1] >= w0 and sign in (0, int(np.sign(f["delta"] or 0)))]


def edits_text(lab: dict, res: dict) -> str:
    """The number of injected edits, the outcome of each evaluated edit in `res`, then the excluded edits with the reason. A
    type with several truth markers (several edits, or the boundaries of one edit) gets the count of each outcome."""
    edits = [f for f in lab["flaws"] if not f.get("placebo", False)]
    excluded = [f for f in edits if f.get("evaluation_excluded")]
    linked = linked_findings(res)
    outcomes: dict[str, list[str]] = {}
    for t in res["truth"]:
        if not t.get("excluded"):
            outcomes.setdefault(t["type"].replace("_", " ").lower(), []).append(marker_outcome(t, res, linked))
    parts = []
    for name, seen in outcomes.items():
        counts = {o: seen.count(o) for o in dict.fromkeys(seen)}
        parts.append(f"{name} ({seen[0]})" if len(seen) == 1 else f"{name} ({', '.join(f'{n} {o}' for o, n in counts.items())})")
    text = f"{len(edits)} {'edit' if len(edits) == 1 else 'edits'} injected; evaluated: {', '.join(parts) or 'none'}."
    if excluded:
        names = ", ".join(dict.fromkeys(f["type"].replace("_", " ").lower() for f in excluded))
        text += f" {len(excluded)} excluded from evaluation, because the realised change failed the label checks: {names}."
    flaws = {f["id"]: f for f in res["flaws"]}
    for t in res["truth"]:
        on = [flaws[i] for i in t.get("on_edit", []) if i in flaws]
        lost = sum(f["points_lost"] or 0 for f in on)
        if lost >= MIN_SHOWN_POINTS:
            text += (f" {len(on)} {'finding lies' if len(on) == 1 else 'findings lie'} on the excluded {t['type'].replace('_', ' ').lower()} "
                     f"edit and cost {lost:.2f} points of the delivery index; the evaluation does not count them as false.")
    off = off_truth(res)
    lost = sum(f["points_lost"] or 0 for f in off)
    if lost >= MIN_SHOWN_POINTS:
        whole = sum(f["context"] == "whole passage" for f in off)
        text += (f" {len(off)} {'finding matches' if len(off) == 1 else 'findings match'} no injected edit"
                 + (f" ({whole} of them over the whole passage)" if whole and len(off) > 1 else " (over the whole passage)" if whole else "")
                 + f" and cost {lost:.2f} points of the delivery index"
                 + (("; it is a difference" if len(off) == 1 else "; they are differences") + " between the two readers, not an injected edit."
                    if res["regime"] == "R2" else "."))
    return text


def linked_findings(res: dict) -> set[str]:
    """Findings that a truth marker names: as its finding, a same-change duplicate or a finding on an excluded edit."""
    return {t["finding"] for t in res["truth"]} | {d for t in res["truth"] for d in [*t.get("duplicate_findings", []), *t.get("on_edit", [])]}


def off_truth(res: dict) -> list[dict]:
    """Findings that no truth marker links and that lie on no missed edit (near_misses)."""
    linked = linked_findings(res)
    near = {f["id"] for t in res["truth"] for f in near_misses(t, res, linked)}
    return [f for f in res["flaws"] if f["id"] not in linked | near]


def showcase_item(id_: str, label: str, title: str, clip: dict, ds, res: dict, focus: str | None, group: str = SHOWCASE_GROUP,
                  note: str | None = None) -> dict:
    """Index item of a showcase example; `focus` is the id of the finding or listed entry that the page opens on."""
    who = ds.parent_entry(clip)["speaker"]
    level = max(clip.get("levels") or [0])
    note = note or ("Listed entries are departures shown without flags or points." if clip["regime"] == "R2" else
                    "The truth markers under the transcript name the finding that the evaluation matches to each edit.")
    return {"id": id_, "group": group, "label": label, "title": f"{title} ({who}, level {level})", "clip": clip["id"], "regime": clip["regime"],
            "description": f"{edits_text(ds.labels(clip), res)} {note}", "focus": focus}


def upload_samples(wav):
    """The samples that a re-upload of the written gallery wav gives: the upload path (audio.load_audio) removes the DC offset,
    so a gallery example with an offset would score differently when uploaded again."""
    return audio.canonical(wav, C.SR)


def baseline_meta(b: dict) -> dict:
    """A bank reading has no speech title of its own: it reads the bank's text."""
    return {"id": b["id"], "title": f"{b['speaker']}: {b.get('title') or BANK_TITLE}", "audio": f"audio/{b['id']}.wav"}


def build(dataset: Path, models: Path, cache: Path | None, eval_dir: Path, out: Path, pool=None, aligner=None,
          provenance: dict | None = None) -> dict:
    """Batch-first: every example's audio and every showcase candidate clip is analysed in one pool batch, then each result
    JSON is built from the analysed recordings. Showcase examples are chosen from the candidates by `pick_showcase` and
    `pick_listed`; candidates of other baselines are analysed only for a capability that the gallery baseline cannot show.
    index.json records the inputs (sha256) and `provenance` (the command and a note, from main)."""
    ds = load_dataset(dataset, cache, pool, aligner)
    det = load_detector(models)
    device = device_class(pool)
    base = ds.entry("baselines", GALLERY_BASELINE)
    bank = bank_readers(ds.manifest)
    bundled = {base["id"], *(r["id"] for r in bank)}
    gallery_dir = out / "gallery"
    (gallery_dir / "results").mkdir(parents=True, exist_ok=True)
    (gallery_dir / "audio").mkdir(parents=True, exist_ok=True)
    index = {"schema": 1, "default": "L3A", "baseline": {"id": base["id"], "title": baseline_meta(base)["title"], "audio": f"audio/{base['id']}.wav",
                                                       "text": base["text"]}, "items": []}
    results_path = eval_dir / "results.json"
    index["provenance"] = {**(provenance or {}), "alignment_device": device, "detector_sha256": sha256_file(models),
                           "dataset_manifest_sha256": sha256_file(ds.root / "manifest.json"),
                           "eval_results_sha256": sha256_file(results_path) if results_path.exists() else None}
    written_baselines = set()

    def analyse(item: dict, P, tr_p, clip: dict | None, refs: list | None = None) -> dict:
        """refs: the analysed bank readings (exemplar first); the truth markers then use the reference and regime of the
        mode that the pipeline selects for the bank."""
        meta = {"id": item["id"], "title": item["title"], "audio": item_audio(item)}
        if item["regime"] == selfref.NAME:
            res = analyze(P, tr_p, alignment_device=device, participant_meta=meta)
            res["truth"] = self_truth_markers(ds.labels(clip), P, res, with_excluded=True)
            return res
        b = ds.any_entry(clip["baseline"]) if clip else base
        res = analyze(P, tr_p, ds.rec(b), regime=item["regime"], detector=det, alignment_device=device, baseline_meta=baseline_meta(b),
                      participant_meta=meta, references=refs)
        if clip:
            clean = ds.rec(ds.parent_entry(clip)) if item["regime"] == "R2" else None
            B, mode_det = mode_detector(refs, det) if refs else (ds.rec(b), det)
            lab = ds.labels(clip)
            res["truth"] = truth_markers(lab, B, P, mode_det, item["regime"], res, clean, with_excluded=True)
        return res

    def write(item: dict, wav, res: dict, text: str) -> None:
        """text: the transcript of the example."""
        b = res["baseline"].get("id")  # None: a SELF result has no reference reading
        if b is not None and b not in written_baselines:
            audio.write_wav(gallery_dir / "audio" / f"{b}.wav", ds.wav(ds.any_entry(b)))
            written_baselines.add(b)
        if "reference_version" not in item:
            audio.write_wav(gallery_dir / item_audio(item), wav)
        res = {**res, "participant": {**res["participant"], "id": item["id"], "title": item["title"], "audio": item_audio(item)}}
        (gallery_dir / "results" / f"{item['id']}.json").write_text(dumps(res) + "\n")
        index["items"].append(index_entry(item, res, text, bundled))

    todo = []  # (item, wav, transcript, text, clip of the labels)
    for item in items():
        clip = None
        if item["clip"]:
            clip = next(c for c in ds.manifest["clips"] if c["id"] == item["clip"])
            wav, tr_p, text = upload_samples(ds.wav(clip)), ds.clip_transcript(clip), ds.parent_entry(clip)["text"]
        elif item["wav"][0] == "readers":
            e = ds.entry("readers", item["wav"][1])
            wav, tr_p, text = upload_samples(ds.wav(e)), ds.transcript(e), e["text"]
        else:
            source = next(c for c in ds.manifest["clips"] if c["id"] == item["wav"][1])
            # the stress matrix's MP3 round trip
            wav, tr_p, text = upload_samples(stress.apply(stress.mp3, ds.wav(source), 1)), ds.clip_transcript(source), ds.parent_entry(source)["text"]
        todo.append((item, wav, tr_p, text, clip))
    r1_pool = [c for c in showcase_clips(ds.manifest, "R1") if c["baseline"] == base["id"]]
    r2_pool = [c for c in showcase_clips(ds.manifest, "R2") if c["baseline"] == base["id"]]
    parents = [ds.parent_entry(c) for c in [*(clip for item, _, _, _, clip in todo if clip and item["regime"] == "R2"), *r2_pool]]
    log(f"analysing {len(todo)} examples and {len(r1_pool) + len(r2_pool)} showcase candidates")
    ds.load(entries=[base, *parents])
    recs = ds.prepare_many([(w, tr) for _, w, tr, _, _ in todo])
    for (item, wav, tr_p, text, clip), P in zip(todo, recs):
        log(f"{item['id']} ({item['regime']})")
        res = analyse(item, P, tr_p, clip)
        if item["regime"] == selfref.NAME:
            item = {**item, "description": self_description(item, ds.labels(clip), res)}
        write(item, wav, res, text)

    def prepared(clips: list[dict]) -> list:
        return ds.prepare_many([(upload_samples(ds.wav(c)), ds.clip_transcript(c)) for c in clips])

    def candidates(clips: list[dict], regime: str) -> list[tuple[dict, dict]]:
        return [(c, analyse({"id": c["id"], "title": c["id"], "regime": regime}, P, ds.clip_transcript(c), c))
                for c, P in zip(clips, prepared(clips))]

    chosen = pick_showcase(candidates(r1_pool, "R1"))
    missing = [spec for spec in SHOWCASE if spec["id"] not in chosen]
    if missing:
        wanted = set().union(*(spec["types"] for spec in missing))
        others = [c for c in showcase_clips(ds.manifest, "R1") if c["baseline"] != base["id"] and wanted & set(c["types"])]
        log(f"no {base['id']} clip shows {[s['id'] for s in missing]}: analysing {len(others)} clips of other baselines")
        ds.load(entries=[ds.any_entry(c["baseline"]) for c in others])
        chosen.update(pick_showcase(candidates(others, "R1"), missing))
    left_out = []
    for spec in SHOWCASE:
        if spec["id"] not in chosen:
            reason = left_out_reason(spec)
            log(f"{spec['id']}: {reason} with this detector; example left out")
            left_out.append({"id": spec["id"], "label": spec["label"], "reason": reason})
            continue
        clip, res = chosen[spec["id"]]
        write(showcase_item(spec["id"], spec["label"], spec["title"], clip, ds, res, shown(spec, res)[0]["id"]), upload_samples(ds.wav(clip)), res,
              ds.parent_entry(clip)["text"])
    listed = pick_listed(candidates(r2_pool, "R2"))
    if listed:
        clip, res = listed
        log(f"r2_listed: {clip['id']} (candidate label: {listed_rank_key(res)[0]})")
        write(showcase_item("r2_listed", "Listed entries", "Edited reading vs the reference: listed, not scored entries", clip, ds, res,
                            listed_focus(res), group="Other performance"), upload_samples(ds.wav(clip)), res, ds.parent_entry(clip)["text"])
    else:
        reason = "no train or val R2 clip has a listed entry"
        log(f"r2_listed: {reason} with this detector; example left out")
        left_out.append({"id": "r2_listed", "label": "Listed entries", "reason": reason})
    for r in bank:
        if r["id"] not in written_baselines:
            audio.write_wav(gallery_dir / "audio" / f"{r['id']}.wav", ds.wav(r))
            written_baselines.add(r["id"])
    index["baselines"] = [{**index["baseline"], "mode": "single"}, bank_meta(bank)]
    consensus_candidates = consensus_clips(ds.manifest, bank)
    log(f"r2_consensus: bank {[r['id'] for r in bank]}; analysing {len(consensus_candidates)} check-reader clips")
    ds.load(entries=[*bank, *(ds.parent_entry(c) for c in consensus_candidates)])
    refs = ds.recs(bank)
    spec = CONSENSUS_SHOWCASE
    hit = pick_showcase([(c, analyse({"id": c["id"], "title": c["id"], "regime": "R2"}, P, ds.clip_transcript(c), c, refs))
                         for c, P in zip(consensus_candidates, prepared(consensus_candidates))], [spec]).get(spec["id"])
    if hit:
        clip, res = hit
        note = (f"Compared with the word-by-word median of {res['detection']['reference_count']} of the "
                f"{res['detection']['references_available']} bank readings (reference mode {res['detection']['reference_mode']}); the truth markers "
                "name the finding that the evaluation matches to each edit.")
        write(showcase_item(spec["id"], spec["label"], spec["title"], clip, ds, res, shown(spec, res)[0]["id"], group="Other performance",
                            note=note), upload_samples(ds.wav(clip)), res, ds.parent_entry(clip)["text"])
    else:
        reason = "no check-reader clip has an injected edit that the evaluation matches to a finding against the bank"
        log(f"r2_consensus: {reason} with this detector; example left out")
        left_out.append({"id": spec["id"], "label": spec["label"], "reason": reason})
    index["left_out"] = left_out
    (gallery_dir / "index.json").write_text(json.dumps(index, indent=1, sort_keys=True) + "\n")
    log(f"wrote {len(index['items'])} examples to {gallery_dir}")
    return index


def site(out: Path, gallery: Path) -> None:
    """GitHub Pages folder: the static page (with its vendored scripts) and the gallery data under gallery/."""
    if not (gallery / "index.json").exists():
        raise FileNotFoundError(f"{gallery}/index.json not found: build the gallery first (python -m cvoice.gallery)")
    out.mkdir(parents=True, exist_ok=True)
    shutil.copytree(STATIC, out, dirs_exist_ok=True)
    shutil.rmtree(out / "gallery", ignore_errors=True)  # no stale examples from an earlier build
    shutil.copytree(gallery, out / "gallery")
    (out / ".nojekyll").touch()
    log(f"static site in {out} ({sum(f.is_file() for f in out.rglob('*'))} files)")


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["site"]:
        parser = argparse.ArgumentParser(prog="python -m cvoice.gallery site")
        parser.add_argument("out_dir", type=Path)
        parser.add_argument("--gallery", type=Path, default=ROOT / "gallery")
        args = parser.parse_args(argv[1:])
        return site(args.out_dir, args.gallery)
    parser = argparse.ArgumentParser(prog="python -m cvoice.gallery")
    parser.add_argument("--dataset", type=Path, default=ROOT / "data")
    parser.add_argument("--models", type=Path, default=ROOT / "models" / "detector.json")
    parser.add_argument("--cache", type=Path, default=None)
    parser.add_argument("--eval", type=Path, default=ROOT / "eval")
    parser.add_argument("--out", type=Path, default=ROOT)
    parser.add_argument("--note", default=None, help="provenance note for index.json, e.g. when the gallery is rebuilt after the final evaluation")
    args = parser.parse_args(argv)
    provenance = {"command": "python -m cvoice.gallery " + shlex.join(argv), **({"note": args.note} if args.note else {})}
    with PreparePool(cache_dir=args.cache) as pool:
        build(args.dataset, args.models, args.cache, args.eval, args.out, pool, provenance=provenance)


if __name__ == "__main__":
    main()
