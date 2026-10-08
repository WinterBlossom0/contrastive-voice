import numpy as np
import pytest
from synth import recording

from cvoice import audio, config as C, dataset
from cvoice.align import parse_transcript


def test_ingest_verifies_the_source_hash(tmp_path):
    x = audio.quantize(0.1 * np.sin(2 * np.pi * 220 * np.arange(32000) / C.SR))
    audio.write_wav(tmp_path / "sub" / "s.wav", x)
    good = {"id": "s", "audio_file": "s.wav", "sha256": dataset.sha256_file(tmp_path / "sub" / "s.wav")}
    y, info = dataset.ingest(good, tmp_path)
    assert len(y) == 32000 and info["channel_rule"] == "mono" and info["sr_in"] == 16000
    with pytest.raises(ValueError, match="SHA-256"):
        dataset.ingest({**good, "sha256": "0" * 64}, tmp_path)
    with pytest.raises(FileNotFoundError):
        dataset.find_source(tmp_path, "nope.wav")


def test_sources_manifest_matches_the_design():
    m = dataset.load_sources_manifest()
    ents = {e["id"]: e for e in m["entries"]}
    base = {e["id"]: e["split"] for e in m["entries"] if e["role"] == "baseline"}
    assert base == {"harris_uncsw_2021": "train", "hclinton_tomorrow_2010": "train", "gwbush_911_2001": "train", "obama_weekly_2009": "train",
                    "reagan_farewell_1989": "train", "lbush_radio_2001": "val", "eisenhower_farewell_1961": "val", "mobama_weekly_2014": "test",
                    "nixon_resignation_1974": "test"}
    cal = sorted(e["id"][-2:] for e in m["entries"] if e["role"] == "reader_calibration")
    chk = sorted(e["id"][-2:] for e in m["entries"] if e["role"] == "reader_check")

    assert len(cal) == 6 and len(chk) == 3 and ents["lv_farewell_reagan"]["role"] == "orator_reference"
    assert all(len(e["sha256"]) == 64 for e in m["entries"])
    assert (dataset.ROOT / "data" / ents["hclinton_tomorrow_2010"]["transcript"]).exists()


def test_manifest_keeps_sentence_breaks_that_re_parsing_the_text_loses(tmp_path):
    tr = parse_transcript("The war ended. 1989 was a good year. We went on.")
    assert tr.n_sentences == 3 and parse_transcript(tr.text()).n_sentences == 2  # the number-initial sentence boundary is lost on a round trip
    entry = dataset._entry("x", audio.quantize(np.zeros(16000)), "baselines/x.wav", tmp_path, tr, speaker="s")
    assert entry["sentence"] == list(tr.sentence)
    ds = dataset.Dataset(tmp_path, {"baselines": [entry], "readers": [], "clips": []})
    assert ds.transcript(entry).sentence == tr.sentence and ds.transcript(entry).norm == tr.norm
    with pytest.raises(ValueError, match="stored sentence indices"):
        ds.transcript({**entry, "sentence": entry["sentence"][:-1]})


def test_word_support_and_inserted_pause_time_coverage_are_distinct():
    lab = {"n_samples": 100, "flaws": [{"type": "FADE", "support": [10, 30]},
           {"type": "MUMBLE", "support": [20, 40]}, {"type": "PAUSE_INTRUSIVE", "support": [50, 50], "span": [50, 70]}]}
    assert dataset.edit_support_share(lab) == .5


def test_build_cross_clips_writes_four_cross_edits_and_the_botched_clip_of_each_reader(tmp_path):
    ref = recording(70, pauses={7: 0.7, 19: 0.8, 30: 0.6, 45: 0.7}, f0=100)
    p0 = recording(70, pauses={7: 0.5, 19: 0.9, 30: 0.6, 45: 0.8}, f0=140, word_s=0.34, seed=2)
    rows = dataset.build_cross_clips(p0, ref, {"id": "r1", "split": "check"}, "B", tmp_path)
    assert [r["kind"] for r in rows[:15]] == ["cross"] * 4 + ["cross_botched"] + ["cross"] * 10
    g5 = rows[4]
    assert g5["id"] == "r1__G5" and g5["recipe"] == "G5" and g5["rung"] == 5 and g5["regime"] == "R2"
    assert (g5["parent"], g5["baseline"], g5["split"]) == ("r1", "B", "check") and g5["n_flaws"] > 0
    assert (tmp_path / g5["audio"]).exists() and (tmp_path / g5["labels"]).exists()
    assert sorted(p.name for p in (tmp_path / "flawed").iterdir()) == sorted(r["id"] + ".wav" for r in rows if not r.get("missing"))


def test_extra_composition_has_stable_disjoint_ids_and_required_trials():
    from collections import Counter
    old = {f"s__single_L{lv}{j}" for lv in C.LEVELS for j in "AB"} | {"s__identity", "s__G1", "s__G3", "s__G5"}
    specs = dataset.extra_clip_specs("s")
    assert [cid for cid, _, _ in specs] == [f"s__extra_L{lv}{j}" for lv in C.LEVELS for j in "ABCD"]
    assert not old & {cid for cid, _, _ in specs}
    assert Counter((t, lv) for _, lv, ts in specs for t in ts) == Counter({(t, lv): 1 for t in C.EXTRA_TYPES for lv in C.LEVELS})
    cross = dataset.extra_clip_specs("s", True)
    assert cross == dataset.extra_clip_specs("s", True) and len(cross) == 10
    counts = Counter((t, lv) for _, lv, ts in cross for t in ts)
    assert all(counts[(t, 3)] == 1 for t in C.EXTRA_TYPES)
    assert {t for t in C.EXTRA_TYPES if counts[(t, 2)]} == set(C.EXTRA_TYPES) - {"MISPLACED_EMPHASIS", "REPEATED_CONTOUR", "RISING_ENDING", "FLAT_FINAL_FALL"}
    assert all(2 <= len(ts) <= 3 for _, _, ts in cross)


def test_old_clip_labels_and_pcm_hashes_are_unchanged(tmp_path):
    import hashlib
    import json
    rec = recording(64, text=". ".join(["we hold these truths to be self evident"] * 8) + ".",
                    pauses={7: .7, 19: .8, 30: .6, 45: .7})
    rows = dataset.build_baseline_clips(rec, {"id": "s", "split": "train"}, tmp_path)
    rows += dataset.build_cross_clips(rec, rec, {"id": "r", "split": "check"}, "B", tmp_path)
    expected = GOLDEN_LABELS
    old = [r for r in rows if r.get("spectrum") != "extra"]
    assert {r["id"] for r in old} == set(expected)
    for r in old:
        labels = (tmp_path / r["labels"]).read_bytes()
        assert hashlib.sha256(labels).hexdigest() == expected[r["id"]]
        assert audio.sha256_pcm(audio.read_wav(tmp_path / r["audio"])) == json.loads(labels)["sha256"]
    assert len({r["id"] for r in rows}) == len(rows)


def test_extra_build_labels_copies_qa_duration_and_card(tmp_path):
    from cvoice.align import Alignment
    from cvoice.features import make_recording
    from cvoice import flaws
    rec = recording(64, text=". ".join(["we hold these truths to be self evident"] * 8) + ".",
                    pauses={7: .7, 19: .8, 30: .6, 45: .7}, level=.08)
    x = rec.wav.copy()
    for i in range(64):
        if i % 8 in (3, 6):
            a, b = round(rec.al.start[i] * C.SR), round(rec.al.end[i] * C.SR)
            x[a:b] *= 4
    rec = make_recording(audio.quantize(x), rec.tr, rec.al)
    assert flaws.stress_set(rec)
    entry = {"id": "s", "split": "train"}
    rows = dataset.build_extra_clips(rec, entry, tmp_path, botched=False)
    ds = dataset.Dataset(tmp_path, {"baselines": [{**entry, "text": rec.tr.text()}], "readers": [], "clips": rows})
    seen = set()
    for c in rows:
        lab = ds.labels(c)
        assert len(lab["flaws"]) + len(lab["skipped"]) == len(dict((cid, ts) for cid, _, ts in dataset.extra_clip_specs("s"))[c["id"]])
        delta = 0
        y = audio.read_wav(tmp_path / c["audio"])
        for f in lab["flaws"]:
            seen.add(f["type"])
            assert f["family"] == C.FLAW_FAMILY[f["type"]]
            assert f["parameter"] == C.LEVEL_PARAM[f["type"]][f["level"] - 1]
            assert f["approximation"] and f["realised"]["value"] is not None
            for name in ("span", "support"):
                a, b = f[name]
                assert 0 <= a < b <= lab["n_samples"]
            assert f["inserted_samples"] - f["removed_samples"] == f["duration_delta_samples"]
            if f["type"] == "LOW_EFFORT":
                a, b = f["parent_span"]
                u, v = f["span"]
                expected = 10 * np.log10(np.mean(y[u:v] ** 2) + C.LEVEL_EPS) - 10 * np.log10(np.mean(rec.wav[a:b] ** 2) + C.LEVEL_EPS)
                assert f["realised"]["value"] == pytest.approx(expected, abs=1e-12)
            for e in f["events"]:
                if e["kind"] == "silence":
                    a, b = e["clip_span"]
                    assert b - a == e["output_samples"] and 0 <= a < b <= len(y)
                if e["kind"] == "copy":
                    a, b = e["clip_span"]
                    assert 0 <= a < b <= lab["n_samples"]
                    assert e["pause_span"][0] == b
                    delta += e["pause_span"][1] - a
                else:
                    a, b = e["parent_span"]
                    delta += e["output_samples"] - (b - a)
        assert lab["n_samples"] - len(rec.wav) == delta
        assert sum(f["duration_delta_samples"] for f in lab["flaws"]) == delta
        assert lab["outside_support_identical"]
        al = Alignment(np.array(lab["words"]["start"]) / C.SR, np.array(lab["words"]["end"]) / C.SR, rec.al.compat, .9)
        q = dataset.label_qa(ds, c, al)
        assert q["all_words"]["max_ms"] == 0
        assert q["inserted_copies"] == sum(e["kind"] == "copy" for f in lab["flaws"] for e in f["events"])
        words = sorted(f["words"] for f in lab["flaws"])
        assert all(b + C.EDIT_GAP_WORDS < c for (_, b), (c, _) in zip(words, words[1:]))
        assert sum(b-a+1 for a,b in words) <= C.COVERAGE_CAP * len(rec.tr)
    assert {"WORD_REPETITION", "SOUND_REPETITION"} <= seen
    manifest = {"baselines": [], "readers": [], "clips": rows, "pipeline": {"version": "test"}, "counts": {"files": 12, "minutes": 6}}
    dataset.write_card(manifest, tmp_path / "card.md")
    text = (tmp_path / "card.md").read_text()
    assert all(t in text for t in C.EXTRA_TYPES) and "DISFLUENCY" in text and "ENDINGS" in text and "extra minutes" in text
    again = dataset.build_extra_clips(rec, entry, tmp_path / "repeat", botched=False)
    assert [(r["id"], r["sha256"], r["skipped"]) for r in rows] == [(r["id"], r["sha256"], r["skipped"]) for r in again]


# Pre-extension synthetic build, including label bytes and their PCM hashes.
GOLDEN_LABELS = {
    "s__single_L1A": "e20202e627d6a652045bf8a1be0343842b4de878c16e26b2b5dbf1913bb2f73a",
    "s__single_L1B": "7ba1920edf143103d8a02b942302581759f5d3b9481dbbb2a352bd17064b87d1",
    "s__single_L2A": "3ebe28c7386c919106a5c066424b7937a49da9a9557a21b20c2533dc217253e7",
    "s__single_L2B": "857744de692346a3af4ca2785eaeeb844cda48c473c3eedbbf571285bc77f35c",
    "s__single_L3A": "ea266fef77355f6a9a8537a7bf3081e7e0f99bff27a2d40012f9e1f09822bd89",
    "s__single_L3B": "c2787d8c2ef8f4a55190d6a4342b7dfca24796095bff715060ca243d7160fe1c",
    "s__identity": "51bbfbe848f499426d5cec2628df0372deb7a6ad69ff8bc11d469febfda666d3",
    "s__G1": "82b7589bb0c0f9e04d390fe9f171e15511ab2d7909890f62b08036552ec7bd0e",
    "s__G3": "f5a8b319e34dcb880e0de42fe17e1fe2ff356797a764a5611cc0a5968f38627f",
    "s__G5": "c908f0423d97190f9ce9dec97dcbe63458fc1ff2fefd21c5697f55dd322d858d",
    "r__x1_L2": "3a5805b670c43781224fa705ef098a4c5662af126d0da3ff0f88de868f317e2b",
    "r__x2_L3": "6015a4b43790d818d491c7c73f9007a4bc86c003200bd6f3b3bd229835a73375",
    "r__x3_L3": "a4b45471853e13729f0b46236f3cd764e6f51ccd95b434db266c760d182cf940",
    "r__x4_L3": "b5585ebe031c262183f48b3094952554a33b12e8f89b05a39ac7991c3c4bd56e",
    "r__G5": "1855561914a18c9cf90c02b76a17f6aff57a357618edc7dd59580115b3555d67"
}



def test_extra_all_skipped_during_planning_or_rendering_are_missing(tmp_path, monkeypatch):
    from cvoice import flaws
    rec = recording()
    entry = {"id": "short", "split": "check"}
    def missing_plan(rec, specs, *args, **kwargs):
        return flaws.Plan([], [{"type": t, "level": lv, "reason": "no eligible position"} for t, lv in specs])
    with monkeypatch.context() as patch:
        patch.setattr(flaws, "plan_clip", missing_plan)
        rows = dataset.build_extra_clips(rec, entry, tmp_path / "plan", botched=False)
    assert len(rows) == 12 and all(c["missing"] for c in rows)
    assert not (tmp_path / "plan/flawed").exists()
    def failed_render(rec, plan, *args, **kwargs):
        return rec.wav, {"flaws": [], "skipped": [{"type": e.type, "level": e.level, "reason": "DSP failed"}
                                                  for e in plan.edits] + plan.skipped}
    monkeypatch.setattr(flaws, "inject", failed_render)
    rows = dataset.build_extra_clips(rec, entry, tmp_path / "render", botched=False)
    assert all(c["missing"] for c in rows)
    assert not (tmp_path / "render/flawed").exists()
    manifest = {"pipeline": {"version": "test"}, "baselines": [], "readers": [], "clips": [], "extra_plans": rows,
                "counts": {"files": 0, "minutes": 0}}
    card = tmp_path / "empty.md"
    dataset.write_card(manifest, card)
    text = card.read_text()
    assert "Empty held-out cells:" in text and "R2" not in text
    assert "R1/check/BLOCK/1 (skipped)" in text and "planned | placed" in text and "DSP failed" in text


def test_extra_ladder_qa_detects_a_bad_rung_and_changed_placement(tmp_path):
    import json
    rows = []
    for lv, value in ((1, .2), (2, .1), (3, .6)):
        c = {"id": str(lv), "parent": "p", "kind": "single", "labels": str(lv) + ".json"}
        lab = {"flaws": [{"type": "RHYME_PROLONGATION", "level": lv, "parent_span": [10, 20],
                           "realised": {"value": value}}]}
        (tmp_path / c["labels"]).write_text(json.dumps(lab))
        rows.append(c)
    qa = dataset.extra_ladder_qa(rows, tmp_path)
    assert qa[0]["reason"] == "non-monotone realised ladder" and qa[0]["values"] == [.2, .1, .6]
    path = tmp_path / rows[1]["labels"]
    lab = json.loads(path.read_text())
    lab["flaws"][0]["parent_span"] = [30, 40]
    path.write_text(json.dumps(lab))
    assert dataset.extra_ladder_qa(rows, tmp_path)[0]["reason"] == "different ladder placements"


def test_extra_ladders_share_placements_and_report_nominal_shortfalls(tmp_path):
    import json
    from test_edits_extra import recipe_recording
    rec = recipe_recording()
    rows = dataset.build_extra_clips(rec, {"id": "short", "split": "test"}, tmp_path, botched=False)
    by_type = {}
    for c in rows:
        if c.get("missing"):
            continue
        lab = json.loads((tmp_path / c["labels"]).read_text())
        for f in lab["flaws"]:
            by_type.setdefault(f["type"], []).append((f["parent_span"], lab["seed"]))
    assert all(all(v == vs[0] for v in vs) for vs in by_type.values())
    from cvoice import edits_extra
    _, _, lab = edits_extra.rising_ending(rec, 1, 2)
    assert all(q["reason"] == "final contour does not rise by at least 1 st" for q in dataset.extra_realisation_qa(lab))
    lab["flaws"][0]["realised"]["value"] = .1
    assert "realised change below half target or wrong sign" in {q["reason"] for q in dataset.extra_realisation_qa(lab)}
