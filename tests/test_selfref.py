"""The no-reference mode (regime SELF): self-relative measures, the pluggable text model, the detector file and the
result of pipeline.analyze without a baseline."""
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pytest
from synth import recording

from cvoice import config as C, pipeline, selfref as S
from cvoice.detect import KEYS, config_hash, load_detector as load_reference

ROOT = Path(__file__).resolve().parents[1]
FROZEN_DETECTOR_SHA256 = 'd5935d3f8eeaf928a143b9b04db0c4250604a6c17f5336af87ef124c090758b6'
FINAL_CONFIG = '782d7df7589164fa7d06e10571369a28aaee6149834a346cfbe4d90e3832f092'
TEXT = "We hold these truths, to be self evident. That all men are created equal and so on of the end."


@pytest.fixture(scope="module")
def reading():
    """20 words, three sentences: a comma after word 3, sentence ends after words 7 and 19; pauses at both marks and a
    long pause after the preposition 'on' (boundary 16)."""
    return recording(20, text=TEXT, pauses={3: 0.35, 7: 0.7, 16: 0.9})


class StubNorms:
    """The norms interface of norms.py with phone counts as expected durations (plus speech_bump per word position for
    the measure 'speech') and class names in its own words."""
    def __init__(self, speech_bump=0.0):
        self.calls = []
        self.speech_bump = speech_bump

    def expected_word_log_duration(self, words, punct_after, measure="speech"):
        self.calls.append((measure, list(words)))
        bump = self.speech_bump * np.arange(len(words)) if measure == "speech" else 0.0
        return np.log([S.phone_count(w) for w in words]) + bump

    def pause_class(self, words, punct_after):
        names = []
        for i in range(len(words) - 1):
            if punct_after[i] in (".", "!", "?"):
                names.append("sentence end")
            elif punct_after[i]:
                names.append("other punctuation")
            elif words[i] in ("on", "of", "the"):
                names.append("none inside tight phrase")
            else:
                names.append("none")
        return names

    def pause_quantile(self, cls, seconds):
        return 0.5


def pinned(model, h=1.5):
    """A SELF detector with the design floors as scales and one h for every enabled flag key (tests only)."""
    scales = {k if C.is_event(C.dim_of(k)) else C.dim_of(k): C.FLOORS[C.dim_of(k)] for k in KEYS}
    reg = S.regime(scales, {k: (h if C.dim_of(k) in S.ENABLED else None) for k in KEYS})
    return S.make_detector(model, reg, dict(C.PMAX_START), {"calibrated": False})


def strings(value):
    if isinstance(value, dict):
        for v in value.values():
            yield from strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)
    elif isinstance(value, str):
        yield value


# ============================================================================================ measures
def test_window_time_in_proportion_to_phones_has_no_departure(reading):
    weights = S.word_weights(reading.tr, S.make_model())
    expected = S.window_sum(weights, reading.win)
    x, typical = S._tempo(reading, 0.07 * expected, weights)
    ok = np.isfinite(x)
    assert ok.any() and np.allclose(x[ok], 0.0) and np.allclose(typical[ok], 0.07 * expected[ok])
    slow = 0.07 * expected
    slow[5] *= 2.0
    x, _ = S._tempo(reading, slow, weights)
    assert x[5] == pytest.approx(np.log(2.0)) and np.allclose(np.delete(x, 5)[np.isfinite(np.delete(x, 5))], 0.0)


def test_pause_classes_and_the_speakers_own_class_medians(reading):
    classes = S.pause_classes(reading.tr, S.make_model())
    assert classes[3] == "comma" and classes[7] == "end" and classes[16] == "none"
    tight = S.pause_classes(reading.tr, S.make_model(options={"tight_pauses": True}))
    assert tight[16] == "tight" and tight[15] == "none"  # a preposition opens a tight phrase, an adverb does not
    measure = np.asarray(reading.sil_raw, float)
    expected = S.expected_pauses(measure, classes)
    # one comma boundary only: it takes the median of all punctuated boundaries (comma and sentence end)
    assert expected[3] == pytest.approx(np.median(measure[[3, 7]]))
    assert expected[16] == pytest.approx(np.median(measure[classes == "none"]))


def test_a_long_pause_inside_a_phrase_is_a_countable_lengthened_pause(reading):
    comp = S.self_comparison(reading, S.make_model())
    d2 = comp.dims["D2"]
    assert d2.x[16] > 0.5 and d2.countable[16]
    assert not d2.countable[7]  # a sentence-end pause at the speaker's own typical length is not a departure


def test_self_dims_keep_the_reference_algebra(reading):
    comp = S.self_comparison(reading, S.make_model(position={"D3": [0.0, 0.05, 0.03, -0.15]}))
    for k in ("D1", "D2", "D3", "D5", "D6", "D9"):
        d = comp.dims[k]
        for i in np.flatnonzero(np.isfinite(d.x)):
            assert d.reference(int(i)) == pytest.approx(float(d.b[i]), rel=1e-6, abs=1e-6), (k, i)
    for k in S.ABSENT:
        assert not np.isfinite(comp.dims[k].x).any() and comp.coverage[k] == 0.0


# ============================================================================================ text model plug
def test_norms_text_model_uses_the_norms_object(reading):
    stub = StubNorms()
    phones = S.self_comparison(reading, S.make_model())
    learned = S.self_comparison(reading, S.make_model("norms"), stub)
    assert stub.calls and stub.calls[0][1][0] == "we"  # lower-case vocabulary words
    for k in ("D1", "D9"):
        assert np.allclose(phones.dims[k].x, learned.dims[k].x, equal_nan=True)
    classes = S.pause_classes(reading.tr, S.make_model("norms", options={"tight_pauses": True}), stub)
    assert classes[3] == "comma" and classes[7] == "end" and classes[16] == "tight" and classes[0] == "none"
    assert S.pause_classes(reading.tr, S.make_model("norms"), stub)[16] == "none"  # tight class only with the option


def test_norms_d1_text_model_takes_the_norms_for_d1_only(reading):
    stub = StubNorms(speech_bump=0.05)
    phones = S.self_comparison(reading, S.make_model())
    mixed = S.self_comparison(reading, S.make_model("norms_d1"), stub)
    assert {measure for measure, _ in stub.calls} == {"speech"}
    assert not np.allclose(phones.dims["D1"].x, mixed.dims["D1"].x, equal_nan=True)
    for k in ("D2", "D3", "D5", "D6", "D9"):
        assert np.allclose(phones.dims[k].x, mixed.dims[k].x, equal_nan=True), k
    tight = S.make_model("norms_d1", options={"tight_pauses": True})
    assert list(S.pause_classes(reading.tr, tight, stub)) == list(S.pause_classes(reading.tr, S.make_model(options={"tight_pauses": True})))


def test_norms_text_model_needs_the_norms_file(tmp_path, monkeypatch):
    monkeypatch.setattr(S, "NORMS_PATH", tmp_path / "duration_norms.json")
    S.load_norms.cache_clear()
    with pytest.raises(FileNotFoundError, match="duration_norms.json"):
        S.load_norms()
    with pytest.raises(ValueError, match="text_model"):
        S.make_model("syllables")


# ============================================================================================ detector file
def test_detector_round_trip_and_hash(tmp_path):
    det = pinned(S.make_model(position={"D3": [0.0, 0.0, 0.0, -0.1]}))
    path = tmp_path / "detector_selfref.json"
    S.save_detector(det, path)
    assert S.load_detector(path) == det
    det["regime"]["h"]["D1-"] = 9.0
    path.write_text(json.dumps(det))
    with pytest.raises(ValueError, match="hash"):
        S.load_detector(path)


def test_shipped_self_detector_and_the_frozen_reference_detector():
    det = S.load_detector(S.DEFAULT_DETECTOR)
    assert det["name"] == S.NAME and det["text_model"]["text_model"] in S.TEXT_MODELS
    assert det["regime"]["enabled"] == list(S.ENABLED) and all(v is None for v in det["regime"]["clip"].values())
    # Owner decision: the gettysburg and poetry fit-phase readers enter the false-region budget only.
    readers = det["report"]["readers"]
    assert readers["sources"] == ["gettysburg", "poetry"] and readers["roles"] == ["budget"] and readers["readings"] > 0
    selection = det["report"]["selection"]
    assert selection["null_regions"] <= selection["budget_regions"]
    assert hashlib.sha256((ROOT / "models/detector.json").read_bytes()).hexdigest() == FROZEN_DETECTOR_SHA256
    assert config_hash(load_reference(ROOT / "models/detector.json")) == FINAL_CONFIG


# ============================================================================================ result
def test_self_result_has_the_reference_result_shape_and_no_reference_wording(reading, pinned_detector):
    det = pinned(S.make_model(position={"D3": [0.0, 0.05, 0.03, -0.15]}), h=1.0)
    res = pipeline.analyze(reading, reading.tr, detector=det, participant_meta={"id": "p"})
    ref = pipeline.analyze(reading, reading.tr, reading, regime="R1", detector=pinned_detector())
    assert set(res) == set(ref) and res["regime"] == "SELF"
    assert res["detection"]["reference_mode"] == "none" and res["detection"]["reference_count"] == 0
    assert res["pipeline"]["config_sha256"] == det["selfref_sha256"]
    assert all(w["b"] == w["p"] for w in res["words"]) and res["map"]["b"] == res["map"]["p"]
    rows = {r["key"]: r for r in res["rows"]}
    assert rows["pitch"]["b"] == [None if v is None else 0.0 for v in rows["pitch"]["p"]]
    assert {rows[k]["status"] for k in ("emphasis", "word_time", "ending")} == {"absent"}
    assert res["flaws"], "h 1.0 at the floors flags the planted pause"
    assert {f["dimension"] for f in res["flaws"]} <= set(S.ENABLED)
    for f in res["flaws"]:
        assert f["pattern"] is None and f["evidence"] == [] and f["text"] and f["fix"]
    assert res["scores"]["label"] == "Delivery index relative to your own reading"
    texts = [s for s in strings(res) if re.search("reference", s, re.I)]
    assert texts == [], texts


def test_every_self_flaw_text_avoids_the_word_reference(reading):
    det = pinned(S.make_model(), h=1.0)
    comp = S.self_comparison(reading, det["text_model"])
    from synth import local
    from cvoice import explain
    from cvoice.score import score
    for dim, i0, i1, z in (("D1", 2, 6, -3), ("D1", 2, 6, 3), ("D9", 2, 6, -3), ("D2", 7, 7, -3), ("D2", 16, 16, 3),
                           ("D3", 9, 13, -3), ("D5", 9, 13, -3), ("D6", 9, 13, -3)):
        r = local(dim, i0, i1, z)
        d = comp.dims[dim]
        d.x[r.peak] = float(np.sign(z)) * 3 * S.scale(det["regime"], dim, r.sign)
        d.p[r.peak] = d.p[r.peak] if np.isfinite(d.p[r.peak]) else 0.5
        sc = score(comp, [r], det["regime"], det["score"]["pmax"])
        entry = explain.build(r, comp, reading, reading, det["regime"], sc.masses[0], sc, "", None, True)
        out = S.describe_flaw(entry, r, comp, reading, det["regime"], det["text_model"])
        assert not [s for s in strings(out) if re.search("reference", s, re.I)], (dim, z, out["text"])


def test_listed_context_names_a_long_pause_and_costs_nothing(reading):
    det = pinned(S.make_model(), h=1.0)
    stretched = recording(20, text=TEXT, pauses={3: 0.35, 7: 1.4, 16: 0.2})
    items = S.listed_context(stretched, det)
    pauses = [x for x in items if x["dimension"] == "D2"]
    assert [x["words"] for x in pauses] == [[7, 8]] and all(x["status"] == "listed" for x in items)


def test_a_reading_without_baseline_takes_only_the_self_regime(reading):
    with pytest.raises(ValueError, match="SELF"):
        pipeline.analyze(reading, reading.tr, regime="R1")


# ============================================================================================ frozen outputs (slow: real aligner)
GALLERY = ROOT / "gallery"
MANIFEST = ROOT / "build/work/kaggle_runs/last_run/x/data/dataset/manifest.json"
REPRODUCED = ("identity", "L3A", "G5", "greenman", "natural_rush")


@pytest.mark.slow
@pytest.mark.parametrize("item_id", REPRODUCED)
def test_gallery_results_are_reproduced_unchanged(item_id):
    """The SELF mode is additive: the reference regimes give the shipped gallery results byte for byte (except truth)."""
    if not MANIFEST.exists():
        pytest.skip("dataset manifest not available")
    from cvoice.align import load_aligner, parse_transcript
    from cvoice.gallery import baseline_meta
    index = json.loads((GALLERY / "index.json").read_text())
    item = next(i for i in index["items"] if i["id"] == item_id)
    entry = next(b for b in json.loads(MANIFEST.read_text())["baselines"] if b["id"] == item["baseline"])
    saved = json.loads((GALLERY / item["result"]).read_text())
    res = pipeline.analyze(GALLERY / item["audio"], parse_transcript(entry["text"]), GALLERY / f"audio/{item['baseline']}.wav",
                           regime=item["regime"], detector=load_reference(ROOT / "models/detector.json"), aligner=_aligner(load_aligner),
                           baseline_meta=baseline_meta(entry), participant_meta={"id": item["id"], "title": item["title"], "audio": item["audio"]})
    produced = json.loads(pipeline.dumps(res))
    produced.pop("truth"), saved.pop("truth")
    assert produced == saved


_ALIGNER = []


def _aligner(load):
    if not _ALIGNER:
        _ALIGNER.append(load())
    return _ALIGNER[0]
