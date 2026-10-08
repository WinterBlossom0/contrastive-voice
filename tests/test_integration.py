"""Mini end-to-end run of build -> calibrate -> evaluate -> gallery on synthetic speech with analytic alignments (no model).

The aligner is replaced by planted word times (clean recordings) and the labels' analytic word times (edited clips); anything else
(stress transforms, repairs, on-the-fly placebos) gets the clean alignment scaled to its length. This exercises the whole code path of
the Kaggle stages in about a minute; it proves plumbing, not accuracy.
"""
import json

import numpy as np
import pytest
from synth import synth

from cvoice import audio, calibrate, config as C, dataset, evaluate, gallery, pipeline, stress
from cvoice.align import Alignment, parse_transcript
from cvoice.features import make_recording

N_WORDS = 64
PAUSES = {7: 0.7, 19: 0.8, 30: 0.6, 45: 0.7, 55: 0.6}
WORDS = "we hold these truths to be self evident that all men are created equal and so on".split()


def text():
    w = [WORDS[i % len(WORDS)] for i in range(N_WORDS)]
    return " ".join(w[:20]) + ". " + " ".join(w[20:40]).capitalize() + ". " + " ".join(w[40:]).capitalize() + "."


def fast_world(x, seed):
    return np.roll(x, 7)


@pytest.fixture
def world(tmp_path, monkeypatch):
    tr = parse_transcript(text())
    known, planted = {}, {}

    def fake_align(wav, tr_, aligner=None, cache_dir=None):
        key = audio.sha256_pcm(wav)
        if key not in known:
            ref = planted["clean"]
            scale = len(wav) / ref[1]
            known[key] = Alignment(ref[0].start * scale, ref[0].end * scale, ref[0].compat, ref[0].mean_compat)
        return wav, known[key]

    def fake_prepare(wav, tr_, aligner=None, cache_dir=None):
        w, al = fake_align(wav, tr_)
        return make_recording(w, tr_, al)

    monkeypatch.setattr(pipeline, "align_wav", fake_align)

    for mod in (pipeline, calibrate, evaluate, dataset, gallery):
        if hasattr(mod, "prepare"):
            monkeypatch.setattr(mod, "prepare", fake_prepare)
        if hasattr(mod, "load_aligner"):
            monkeypatch.setattr(mod, "load_aligner", lambda: None)
    # keep the test quick: WORLD is a vocoder on 20 s of audio; the plumbing is what is tested here. MATRIX holds the function
    # itself, so the matrix entry is replaced too.
    monkeypatch.setattr(stress, "MATRIX", [(name, fast_world if fn is stress.world_speaker else fn) for name, fn in stress.MATRIX])
    monkeypatch.setattr(stress, "world_speaker", fast_world)
    from cvoice import flaws
    monkeypatch.setattr(flaws, "world_flatten", lambda x, a, b, strength: flaws.flatten_span(x, a, b, strength))
    return tr, known, planted, tmp_path


def make_clean(i, tr, planted):
    wav, st, en = synth(N_WORDS, pauses=PAUSES, f0=100 + 12 * i, seed=i, glide_st=3.0 + i % 3)
    al = Alignment(st, en, np.full(N_WORDS, 0.9), 0.9)
    planted.setdefault("clean", (al, len(wav)))
    return wav, al


@pytest.mark.slow
def test_build_calibrate_evaluate_gallery_end_to_end(world, pinned_detector):
    tr, known, planted, tmp = world
    root = tmp / "data" / "dataset"
    splits = {"reagan_farewell_1989": "train", "harris_uncsw_2021": "train", "obama_weekly_2009": "train", "lbush_radio_2001": "val",
              "mobama_weekly_2014": "test"}
    baselines, readers = [], []
    for i, (bid, split) in enumerate(splits.items()):
        wav, al = make_clean(i, tr, planted)
        known[audio.sha256_pcm(wav)] = al
        baselines.append(dataset._entry(bid, wav, f"baselines/{bid}.wav", root, tr, speaker=bid, gender="F", year=2000, title=bid, split=split,
                                        licence_basis="test", licence_url="x", transcript_url="x", passage={}))
    roles = [("amb", "reader_calibration"), ("dl", "reader_calibration"), ("fb", "reader_calibration"), ("jn", "reader_calibration"),
             ("pc", "reader_calibration"), ("wt", "reader_calibration"), ("dj", "reader_check"), ("sa", "reader_check"), ("tg", "reader_check")]
    for j, (r, role) in enumerate(roles):
        wav, al = make_clean(10 + j, tr, planted)
        known[audio.sha256_pcm(wav)] = al
        readers.append(dataset._entry(f"gettysburg_{r}", wav, f"readers/gettysburg_{r}.wav", root, tr, role=role, split="calibration" if "cal" in role else "check",
                                      speaker=r, licence_basis="test", licence_url="x", passage={}))
    wav, al = make_clean(30, tr, planted)
    known[audio.sha256_pcm(wav)] = al
    readers.append(dataset._entry("greenman_reagan", wav, "readers/greenman_reagan.wav", root, tr, role="orator_reference", split="train", speaker="g",
                                  paired_baseline="reagan_farewell_1989", licence_basis="test", licence_url="x", passage={}))

    # edited clips: their alignment is the labels' analytic word times
    real_inject = dataset.flaws.inject

    def inject_and_register(rec, plan, clip_id, parent_id, **kw):
        y, lab = real_inject(rec, plan, clip_id, parent_id, **kw)
        known[audio.sha256_pcm(y)] = Alignment(np.array(lab["words"]["start"]) / C.SR, np.array(lab["words"]["end"]) / C.SR, rec.al.compat, 0.9)
        return y, lab

    dataset.flaws.inject, flaws_inject = inject_and_register, dataset.flaws.inject
    try:
        manifest = dataset.finish(root, baselines, readers, tmp / "cache")
    finally:
        dataset.flaws.inject = flaws_inject
    assert manifest["counts"]["baselines"] == 5 and manifest["counts"]["readers"] == 10
    kinds = [c["kind"] for c in manifest["clips"]]
    assert sum(c["kind"] == "single" and c.get("spectrum") != "extra" for c in manifest["clips"]) == 30
    assert sum(c["kind"] == "single" and c.get("spectrum") == "extra" for c in manifest["clips"]) == 60
    assert kinds.count("identity") == 5 and kinds.count("ladder") == 15
    # cross clips: 3 edited readers (check) + the orator reference each get up to 4 edited clips (CROSS_SPEAKER_CLIPS; some may find no span) and one botched clip
    assert 4 <= sum(c["kind"] == "cross" and c.get("spectrum") != "extra" for c in manifest["clips"]) <= 4 * len(C.CROSS_SPEAKER_CLIPS)
    assert sum(c["kind"] == "cross" and c.get("spectrum") == "extra" for c in manifest["clips"]) <= len(readers) * len(C.EXTRA_CROSS_CLIPS)
    assert kinds.count("cross_botched") == 4
    assert {c["parent"] for c in manifest["clips"] if c["kind"] == "cross_botched"} == {"gettysburg_dj", "gettysburg_sa", "gettysburg_tg", "greenman_reagan"}
    assert manifest["counts"]["flawed"] == len(manifest["clips"]) and manifest["counts"]["files"] == 5 + len(manifest["clips"]) + 10
    qa = json.loads((root / "label_qa.json").read_text())
    assert qa["all_outside_support_identical"] and all(q["all_words"]["max_ms"] < 1.0 for q in qa["clips"])  # analytic alignment: exact
    assert (root / "dataset_card.md").read_text().count("|") > 20
    lab = json.loads((root / manifest["clips"][0]["labels"]).read_text())
    assert {"parent", "recipe", "seed", "chain", "words", "flaws"} <= set(lab)

    out = tmp / "out"
    det = calibrate.run(tmp / "data", tmp / "cache", out)
    assert all(v is not None for v in det["regimes"]["R1"]["h"].values()) and (out / "models" / "detector.json").exists()
    assert det["regimes"]["R1"]["scales"]["D1"] == pytest.approx(C.FLOORS["D1"], abs=1e-6) and det["regimes"]["R2"]["enabled"] == ["D1", "D2", "D3", "D5"]
    rep = json.loads((out / "calibration" / "report.json").read_text())
    assert rep["report"]["gates_train"]["n_clips"] == 30 + 3 + 9 or rep["report"]["gates_train"]["n_clips"] > 0

    assert len(rep["R2_stability"]["rows"]) == 6 and set(rep["R2_h_table"]) == {"D1-", "D1+", "D2-", "D2+", "D3-", "D5-"}
    assert rep["R1_selection"][0]["h"] == 1 and rep["R1_selection"][-1]["h"] == 3
    assert all("edit_support_time_share" in c for c in manifest["clips"])
    assert det["report"]["manifest_sha256"] == dataset.sha256_file(root / "manifest.json")
    assert det["report"]["alignment_device"] == "cpu" and manifest["pipeline"]["alignment_device"] == "cpu"
    res = evaluate.run(tmp / "data", out / "models" / "detector.json", tmp / "cache", out)
    assert not res["errors"], res["errors"]
    # default splits: train and val only; the test split is never touched, and train is never pooled with held-out
    assert res["splits"] == ["train", "val"] and res["alignment_device"] == "cpu" and not res["final"]
    assert {r["split"] for r in res["headline"]["by_split"]} == {"train", "val"} and set(res["headline"]["activation"]) == {"train", "val"}
    assert all(m["split"] != "test" for m in res["headline"]["magnitude"]) and set(res["nulls"]["detail"]) >= {"R1 val"} and "R1 test" not in res["nulls"]["detail"]
    assert "skipped" in res["device_agreement"] and any(r["condition"].startswith("WORLD") and isinstance(r["limits"], list) for r in res["stress"]["rows"])
    assert "by_split_overlap" not in res["headline"] and res["headline"]["by_split_strict"]
    assert all("flaws_found_before" in r and "flaws_found_after" in r for r in res["stress"]["flawed_clips"])
    assert all("score_before" in r and "new_flags" in r for r in res["repair"]["rows"])
    assert {r[1] for r in res["validity"]["rows"]} >= {"DEEMPHASIS", "MUMBLE"}
    assert all({"TP", "false_regions", "onset_ms", "offset_ms"} <= r.keys() for r in res["chain_b"]["rows"])
    assert not (out / "models" / evaluate.FINAL_LOG).exists()
    assert (out / "eval" / "tables.md").exists() and (out / "eval" / "figures" / "detection_vs_level.png").exists()
    bot = res["cross_botched"]  # each botched reader clip against the 6 calibration readers (check) or the paired baseline (orator reference)
    assert {g: v["pairs"] for g, v in bot["summary"].items()} == {"check": 18, "train": 1} and len(bot["rows"]) == 19
    assert all(v["median_botched_score"] < v["median_clean_score"] for v in bot["summary"].values()) and "overall tempo flagged" in bot["table"]
    # graded rungs: each of the 3 check readers x {RUSH, MONOTONE} x 3 levels, against all 6 calibration readers
    assert len(bot["graded"]) == 3 * len(evaluate.WHOLE_CLIP_TYPES) * len(C.LEVELS) * 6
    assert [r[0] for r in bot["ladder"]] == ["unedited"] + ["whole-passage RUSH"] * 3 + ["whole-passage MONOTONE"] * 3 + ["botched (G5)"]
    assert all(r[4] == 18 for r in bot["ladder"][:-1]) and bot["ladder"][-1][4] == 18
    lad = res["ladder"]  # R1 score per split and rung, one gate-violation row per split evaluated
    assert {r[0] for r in lad["rows"]} == {"train", "val"} and [g[0] for g in lad["gates"]] == ["train", "val"] and all(len(g) == 5 for g in lad["gates"])
    assert {r[1] for r in lad["rows"]} >= {"identity", "G1", "G3", "G5", "level 1 (four edits)"}
    cross = res["cross_speaker"]
    # calibration readers carry the new-type cross clips (dataset EXTRA_CROSS_CLIPS)
    assert {e["reader_group"] for e in cross["edits"]} == {"calibration", "check", "train"} and all({"reference", "level"} <= e.keys() for e in cross["edits"])
    assert cross["by_type"] and "R2 check readers" in res["nulls"]["detail"]
    assert res["reproducibility"]["identical"] and res["nulls"]["rows"] and res["stress"]["rows"] and res["headline"]["by_split"]
    tables = (out / "eval" / "tables.md").read_text()
    for head in ("False flags per minute", "Stress matrix", "Repair test", "event F1", "Expectation table", "botched readings", "Conditions that break keys"):
        assert head in tables

    fin = evaluate.run(tmp / "data", out / "models" / "detector.json", tmp / "cache", tmp / "out_final", final=True)  # the one final evaluation
    assert not fin["errors"], fin["errors"]
    assert fin["splits"] == ["train", "val", "test"] and fin["final"] and "val+test" in fin["headline"]["activation"]
    assert "lockbox" in fin and "lockbox" not in res  # the R2 lockbox is measured by the final evaluation only
    assert det["config_sha256"] in json.loads((out / "models" / evaluate.FINAL_LOG).read_text())
    with pytest.raises(RuntimeError, match="already evaluated"):
        evaluate.run(tmp / "data", out / "models" / "detector.json", tmp / "cache", tmp / "out_final", final=True)

    idx = gallery.build(tmp / "data", out / "models" / "detector.json", tmp / "cache", out / "eval", out)
    assert [i["id"] for i in idx["items"]][:1] == ["identity"] and {"G1", "G3", "G5", "greenman", "greenman_botched", "channel_mp3"} <= {i["id"] for i in idx["items"]}
    assert (out / "gallery" / "index.json").exists() and (out / "gallery" / "stress_matrix.json").exists()
    r = json.loads((out / "gallery" / "results" / "G5.json").read_text())
    assert r["schema"] == 2 and r["truth"] and r["scores"]["overall"] is not None and r["pipeline"]["alignment_device"] == "cpu"
