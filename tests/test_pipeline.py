import dataclasses
import json
import math

import numpy as np
import pytest
from synth import local, recording, regime, with_x

from cvoice import config as C, flaws
from cvoice.align import Alignment
from cvoice.detect import KEYS
from cvoice.features import make_recording
from cvoice.compare import compare
from cvoice.detect import decode
from cvoice.pipeline import analyze, canon, differences, dumps, listed_reason, main, rows, scores_block
from cvoice.score import score


@pytest.fixture(scope="module")
def pair():
    """Baseline and a participant with one RUSH L3 span; the participant's alignment is the labels' analytic word times."""
    B = recording(70, pauses={7: 0.7, 19: 0.8, 30: 0.6, 45: 0.7})
    ed = flaws.make_edit(B, "RUSH", 3, (20, 26))
    y, lab = flaws.inject(B, flaws.Plan([ed]), "c", "p", recipe="t", seed=1)
    al = Alignment(np.array(lab["words"]["start"]) / C.SR, np.array(lab["words"]["end"]) / C.SR, B.al.compat, 0.9)
    return B, make_recording(y, B.tr, al), lab


def test_identity_is_flawless_and_scores_100(pair, pinned_detector):
    B, _, _ = pair
    res = analyze(B, B.tr, B, regime="R1", detector=pinned_detector(2.0))
    assert res["flaws"] == [] and res["scores"]["overall"] == 100.0
    assert all(d["score"] == 100.0 for d in res["scores"]["dims"] if d["key"] != "D8")
    assert next(d for d in res["scores"]["dims"] if d["key"] == "D8")["score"] is None  # K6: ending is listed in R1
    assert res["schema"] == 2 and res["regime"] == "R1" and res["truth"] == []


def test_rush_is_flagged_localised_and_explained(pair, pinned_detector):
    B, P, lab = pair
    truth = [{"type": "RUSH", "dimension": "D1", "level": 3, "p": [lab["flaws"][0]["span"][0] / C.SR, lab["flaws"][0]["span"][1] / C.SR]}]
    res = analyze(P, B.tr, B, regime="R1", detector=pinned_detector(2.0), truth=truth,
                  baseline_meta={"id": "b", "title": "t", "audio": "b.wav"}, participant_meta={"id": "p", "audio": "p.wav"})
    rush = [f for f in res["flaws"] if f["type"] == "RUSH" and f["dimension"] == "D1"]
    assert len(rush) == 1
    f = rush[0]
    # A speech-tempo region on the same words is a member of the rush group, not a second finding type.
    assert all(x["group"] and f["id"] in x["group"] for x in res["flaws"] if x["dimension"] == "D9")
    s, e = lab["flaws"][0]["span"][0] / C.SR, lab["flaws"][0]["span"][1] / C.SR
    assert f["p"][0] <= e and f["p"][1] >= s and f["dimension"] == "D1" and f["brief_word"] == "Cadence"
    assert f["delta"] < 0 and f["tolerance_multiple"] > 1 and f["severity"] > 0 and 0 < f["overall_if_fixed"] <= 100
    assert f["overall_if_fixed"] > res["scores"]["overall"] and f["points_lost"] > 0
    for k in ("text", "why", "fix", "context", "measure", "unit", "threshold"):
        assert f[k] not in (None, "")
    assert "relative to the reference rendition" in f["text"] and f["why"].startswith('"')
    d1 = next(d for d in res["scores"]["dims"] if d["key"] == "D1")
    assert d1["score"] < 100 and res["scores"]["overall"] < 100
    assert [{k:v for k,v in t.items() if k not in ("available","detector_status")} for t in res["truth"]] == truth and res["baseline"]["id"] == "b" and res["participant"]["audio"] == "p.wav"
    assert any("Uncalibrated" in n for n in res["notices"])


def test_schema_fields_and_rounding(pair, pinned_detector):
    B, P, _ = pair
    res = analyze(P, B.tr, B, regime="R1", detector=pinned_detector())
    assert set(res) == {"schema", "pipeline", "regime", "baseline", "participant", "words", "map", "hop", "rows", "stress", "flaws", "truth",
                        "scores", "notices", "differences", "detection"}
    assert res["pipeline"]["config_sha256"] == pinned_detector()["config_sha256"] and res["hop"] == 0.01
    assert res["pipeline"]["alignment_device"] == "cpu"
    assert len(res["words"]) == len(B.tr) and set(res["words"][0]) == {"w", "b", "p"}
    assert len(res["map"]["b"]) == len(res["map"]["p"]) and np.all(np.diff(res["map"]["p"]) > 0)
    keys = [r["key"] for r in res["rows"]]
    assert keys[:2] == ["pitch", "energy"] and {"pace", "pauses", "pitch_range", "emphasis", "volume", "clarity"} <= set(keys)
    frame = res["rows"][0]
    assert len(frame["p"]) == len(P.fr) and len(frame["b"]) == len(P.fr) and None in frame["p"]  # unvoiced frames are null
    for v in frame["p"]:
        assert v is None or round(v, 2) == v
    assert res["rows"][2]["tol"] == pytest.approx([2.0 * C.FLOORS["D1"]] * 2, abs=0.01)  # [below, above]
    assert all(round(t, 3) == t for w in res["words"] for t in w["p"] + w["b"])
    assert list(res["scores"]["dims"][0]) == ["brief_word", "key", "label", "note", "score", "scored"] or set(res["scores"]["dims"][0]) == {"key", "label", "brief_word", "score", "scored", "note", "coverage"}


def test_result_json_is_deterministic(pair, pinned_detector):
    B, P, _ = pair
    a = dumps(analyze(P, B.tr, B, regime="R1", detector=pinned_detector()))
    b = dumps(analyze(P, B.tr, B, regime="R1", detector=pinned_detector()))
    assert a == b and "NaN" not in a and "Infinity" not in a
    parsed = json.loads(a)
    assert list(parsed) == sorted(parsed)  # sorted keys
    assert canon({"a": np.float64("nan"), "b": [np.int64(3), np.float32(1.5)], "c": (np.array([np.inf, 1.0]),)}) == {"a": None, "b": [3, 1.5], "c": [[None, 1.0]]}


def test_regimes_enable_different_dimensions(pair, pinned_detector):
    B, P, _ = pair
    r2 = analyze(P, B.tr, B, regime="R2", detector=pinned_detector())
    scored = {d["key"] for d in r2["scores"]["dims"] if d["scored"]}
    assert scored == {"D1", "D2", "D3", "D5"} and any("Regime R2" in n for n in r2["notices"])  # K4: D9 is listed in R2
    reason = listed_reason("R2", "D9")
    assert next(d for d in r2["scores"]["dims"] if d["key"] == "D9")["note"] == "listed, unscored: " + reason
    assert not any("Speech-tempo flags" in n for n in r2["notices"]) and any(reason in n for n in r2["notices"])
    off = pinned_detector()
    off["regimes"]["R2"]["h"] = dict.fromkeys(KEYS)
    res = analyze(P, B.tr, B, regime="R2", detector=off)
    assert res["flaws"] == [] and res["scores"]["overall"] is None and any("No calibrated threshold" in n for n in res["notices"])
    with pytest.raises(ValueError):
        analyze(P, B.tr, B, regime="R3", detector=pinned_detector())


def test_transcript_mismatch_between_recordings_is_refused(pair, pinned_detector):
    B, P, _ = pair
    other = recording(70, text=" ".join(["hold"] * 70))
    with pytest.raises(ValueError, match="transcripts differ"):
        analyze(other, B.tr, B, regime="R1", detector=pinned_detector())


def test_cli_writes_result_json(tmp_path, pair, pinned_detector, monkeypatch):
    from cvoice import audio, detect, pipeline
    B, P, _ = pair
    audio.write_wav(tmp_path / "b.wav", B.wav)
    audio.write_wav(tmp_path / "p.wav", P.wav)
    (tmp_path / "t.txt").write_text(B.tr.text())
    detect.save_detector(pinned_detector(), tmp_path / "d.json")
    monkeypatch.setattr(pipeline, "align_wav", lambda wav, tr, aligner=None, cache_dir=None: (wav, B.al if np.array_equal(wav, B.wav) else P.al))
    main(["--participant", str(tmp_path / "p.wav"), "--baseline", str(tmp_path / "b.wav"), "--transcript", str(tmp_path / "t.txt"),
          "--regime", "R1", "--detector", str(tmp_path / "d.json"), "--out", str(tmp_path / "r.json")])
    assert json.loads((tmp_path / "r.json").read_text())["scores"]["overall"] < 100


def test_mismatch_is_refused_only_when_asked_to(pair, pinned_detector, monkeypatch):
    from cvoice import pipeline
    from cvoice.align import TranscriptMismatch
    B, P, _ = pair
    bad = Alignment(B.al.start, B.al.end, np.full(len(B.tr), 0.01), 0.01)
    monkeypatch.setattr(pipeline, "align_wav", lambda wav, tr, aligner=None, cache_dir=None: (wav, bad))
    det = pinned_detector()
    res = analyze(P.wav, B.tr, B.wav, regime="R1", detector=det)  # internal use: the low compatibility is only recorded
    assert res["schema"] == 2 and any("low aligner confidence" in n for n in res["notices"])
    with pytest.raises(TranscriptMismatch, match="baseline recording: transcript does not match"):
        analyze(P.wav, B.tr, B.wav, regime="R1", detector=det, refuse_mismatch=True)  # upload boundary


def test_whole_clip_flags_are_listed_among_the_flaws_and_scored_in_both_regimes(pair, pinned_detector):
    B, _, _ = pair
    P = dataclasses.replace(B, win_T=B.win_T * 0.5, win_R=0.1 * B.win_R)  # every window twice as fast and nearly flat: no local departure
    for name in ("R1", "R2"):
        res = analyze(P, B.tr, B, regime=name, detector=pinned_detector())
        whole = {f["type"]: f for f in res["flaws"] if f["context"] == "whole passage"}
        assert set(whole) == {"TEMPO_FAST", "RANGE_NARROW"} and all(f["type"] in {"TEMPO_FAST", "RANGE_NARROW", "NATURAL_RUSH"} for f in res["flaws"]), name
        assert whole["TEMPO_FAST"]["dimension"] == "D1" and whole["RANGE_NARROW"]["dimension"] == "D3" and whole["TEMPO_FAST"]["words"] == [0, len(B.tr) - 1]
        dims = {d["key"]: d for d in res["scores"]["dims"]}
        assert dims["D1"]["score"] < 100 and dims["D3"]["score"] < 100 and res["scores"]["overall"] < 100, name
        assert [f["id"] for f in res["flaws"][:2]] == ["d1-001", "d3-002"], name
    assert res["differences"] == []  # flagged whole-clip differences are not listed again


def test_unflagged_whole_clip_differences_are_listed_for_d1_and_d3_without_penalty(base):
    reg = regime("R2", clip={"D1": math.log(1.4), "D3": math.log(2.0)})
    comp = compare(base, base)
    comp.dims["D1"].g = math.log(1.2)  # slower, below the threshold: listed
    comp.dims["D3"].g = math.log(3.0)  # wider pitch range: never flagged, listed
    sc = score(comp, [], reg, C.PMAX_START)
    assert sc.clip == {} and sc.overall == 100
    ds = differences(comp, base, base, reg, [])
    assert [(d["dimension"], d["words"], d["p"], d["b"]) for d in ds] == [("D1", None, None, None), ("D3", None, None, None)]
    assert [d["label"] for d in ds] == ["Slower overall than the reference", "Wider pitch range overall than the reference"]
    assert ds[0]["delta"] == pytest.approx(math.log(1.2), abs=.001) and ds[0]["participant"] == pytest.approx(1.2, abs=.001)
    assert ds[1]["flag_thresholds"] == [-math.log(2.0)] and [d["id"] for d in ds] == ["x1", "x2"]
    assert all('multiple' not in d for d in ds)
    assert all("points" not in d["text"] and "fix" not in d for d in ds)
    comp.dims["D1"].g = math.log(1.5)  # beyond the threshold: a flag, no longer a difference
    assert [d["dimension"] for d in differences(comp, base, base, reg, [])] == ["D3"]
    comp.dims["D1"].g = 0.01  # a negligible difference is not listed
    assert [d["dimension"] for d in differences(comp, base, base, reg, [])] == ["D3"]
    assert differences(comp, base, base, regime("R2", clip={"D1": None, "D3": None}), []) == []  # no fitted whole-clip threshold: nothing to compare


def test_differences_are_largest_runs_without_flagged_units(base, pinned_detector):
    comp = with_x(base, "D5", [(2, 3, -4), (10, 15, -3), (22, 23, -2.5)])
    ds = differences(comp, base, base, pinned_detector()["regimes"]["R2"], [local("D5", 2, 3)])
    assert [d["words"] for d in ds] == [[10, 15], [22, 23]]
    assert [d["id"] for d in ds] == ["x1", "x2"]
    assert ds[0]["flag_thresholds"] == [-4.0]
    assert all("points" not in d["text"] and "fix" not in d and "flaw" not in d["text"] for d in ds)


def test_differences_keep_one_peak_per_contiguous_run(base, pinned_detector):
    comp = with_x(base, "D5", [(12, 13, -6), (14, 17, -1.1), (18, 19, -4)])
    ds = differences(comp, base, base, pinned_detector()["regimes"]["R2"], [])
    assert len(ds) == 1 and ds[0]["words"] == [12, 13]


def test_difference_tier_caps_local_items_at_five(base, pinned_detector):
    comp = with_x(base, "D5", [(i, i, -3) for i in range(1, 39, 5)])
    ds = differences(comp, base, base, pinned_detector()["regimes"]["R2"], [])
    assert len(ds) == C.MAX_DIFFERENCES == 5


def test_r2_positive_pitch_difference_is_displayed_without_a_flag(base, pinned_detector):
    comp = with_x(base, "D3", [(10, 15, math.log(3.0))])
    reg = pinned_detector()["regimes"]["R2"]
    assert decode(comp, reg, base.tr.sentence) == []
    assert differences(comp, base, base, reg, [])[0]["label"].startswith("Wider pitch")


def test_row_tolerances_and_detection_note_use_the_threshold_of_each_direction(base, pinned_detector):
    reg = pinned_detector()["regimes"]["R2"]
    reg["h"].update({"D2-": 3, "D2+": 5, "D3-": None, "D5-": 4})
    comp = compare(base, base)
    by_key = {r["key"]: r for r in rows(comp, base, base, reg)}
    assert by_key["pauses"]["tol"] == [.45, .75] and by_key["volume"]["tol"] == [8.0, None] and by_key["pitch_range"]["tol"] == [None, None]
    assert by_key["emphasis"]["tol"] == [None, None]  # R2 displays it, never flags it
    assert by_key["pace"]["tol"] == pytest.approx([2 * C.FLOORS["D1"]] * 2, abs=.01)
    note = scores_block(score(comp, [], reg, C.PMAX_START), reg, "R2")["detection_note"]
    assert "Pauses −0.45 / +0.75 s" in note and "Volume −8 dB" in note and "Pitch variation flags disabled" in note
    assert next(r for r in rows(comp, base, base, pinned_detector()["regimes"]["R1"]) if r["key"] == "pitch_range")["tol"] == [pytest.approx(2 * C.FLOORS["D3"], abs=.01), None]


def test_insufficient_coverage_is_unscored_and_excluded_from_mean(base, pinned_detector):
    missing = base.win_R.copy()
    missing[:25] = np.nan
    participant = dataclasses.replace(base, win_R=missing)
    res = analyze(participant, base.tr, base, regime="R1", detector=pinned_detector())
    row = next(d for d in res["scores"]["dims"] if d["key"] == "D3")
    assert row["score"] is None and row["note"] == "not scored: too little measurable speech" and row["coverage"] < .5
    assert res["scores"]["overall"] == 100 and res["differences"] == []
    assert next(r for r in res["rows"] if r["key"] == "pitch_range")["coverage"] == row["coverage"]
