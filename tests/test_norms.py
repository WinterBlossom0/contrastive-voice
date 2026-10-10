"""Normal word timing from read speech (cvoice.norms): the shipped norms file, its hash check, the direction of the
fitted effects, the letter fallback and the pause classes. No corpus is needed."""
import json

import numpy as np
import pytest

from cvoice import norms as N


@pytest.fixture(scope="module")
def norms():
    return N.load()


def test_shipped_file_loads_with_provenance(norms):
    prov = norms.provenance
    assert "LibriTTS" in prov["corpus"] and "CC BY 4.0" in prov["licence"]
    assert all(len(a["sha256"]) == 64 for a in prov["archives"])
    assert prov["speakers"] > 0 and prov["utterances_kept"] > 0 and prov["words"] > 0
    assert N.DEFAULT_PATH.stat().st_size < 400_000
    assert set(norms.parameters["duration"]) == set(N.MEASURES)
    for model in norms.parameters["duration"].values():
        assert model["objective"] == N.MODEL_OBJECTIVE and list(model["groups"]) == list(N.MODEL_GROUPS)


def test_hash_check_refuses_changed_parameters(tmp_path):
    doc = json.loads(N.DEFAULT_PATH.read_text())
    doc["parameters"]["duration"]["speech"]["beta"][0] += 0.01
    path = tmp_path / "norms.json"
    path.write_text(json.dumps(doc))
    with pytest.raises(N.NormsError, match="SHA-256"):
        N.load(path)
    with pytest.raises(N.NormsError):
        N.load(tmp_path / "missing.json")


@pytest.mark.parametrize("measure", N.MEASURES)
def test_more_phones_take_longer(norms, measure):
    words = ["cat", "cattle", "catalogue", "catastrophe", "and"]
    e = norms.expected_word_log_duration(words, [""] * len(words), measure)
    assert e[0] < e[1] < e[2] < e[3]


@pytest.mark.parametrize("measure", N.MEASURES)
def test_boundary_lengthening(norms, measure):
    def first(mark):
        return norms.expected_word_log_duration(["garden", "was", "green"], [mark, "", "."], measure)[0]
    assert first(",") > first("")
    assert first(".") > first("")


def test_function_word_shorter_than_content_word_of_equal_phones(norms):
    # THE and SEE both have two phones (DH AH0 / S IY1); THE is a function word
    e = norms.expected_word_log_duration(["the", "see", "end"], ["", "", "."])
    assert e[0] < e[1]


def test_relative_scale_is_near_zero_mean_on_a_passage(norms):
    text = ("When the sunlight strikes raindrops in the air, they act as a prism and form a rainbow. The rainbow is a "
            "division of white light into many beautiful colors.")
    from cvoice.align import parse_transcript
    tr = parse_transcript(text)
    for measure in N.MEASURES:
        e = norms.expected_word_log_duration(list(tr.norm), list(tr.punct), measure)
        assert e.shape == (len(tr),) and np.isfinite(e).all()
        assert abs(e.mean()) < 0.4


def test_out_of_dictionary_word_uses_letters_and_is_flagged(norms):
    words = ["Zorbleflax", "Zorb", "cat"]
    assert norms.in_dictionary(words).tolist() == [False, False, True]
    e = norms.expected_word_log_duration(words, ["", "", "."])
    assert np.isfinite(e).all() and e[0] > e[1]
    counts, in_dict = N.phone_counts("ZORBLEFLAX")
    assert not in_dict and counts.sum() >= 7


def test_letter_estimate_is_close_to_the_dictionary_count():
    for word in ("STRENGTH", "MOUNTAIN", "TELEPHONE", "BLACK", "QUESTION"):
        counts, in_dict = N.phone_counts(word)
        assert in_dict
        estimate = N.letter_counts(word)
        assert abs(estimate.sum() - counts.sum()) <= 2, word


def test_pause_classes(norms):
    from cvoice.align import parse_transcript
    tr = parse_transcript("Mr. Smith sat on the mat. Then, it slept -- quietly")
    classes = norms.pause_class(list(tr.norm), list(tr.punct))
    assert len(classes) == len(tr) - 1
    assert classes == ["none", "none", "none", "tight", "tight", "end", "comma", "none", "comma"]


def test_pause_quantiles(norms):
    q = norms.pause_quantile
    for cls in N.PAUSE_CLASSES:
        values = [q(cls, s) for s in (0.0, 0.1, 0.2, 0.5, 1.0, 30.0)]
        assert values == sorted(values) and values[-1] == 1.0
    assert q("end", 0.0) < q("comma", 0.0) < q("none", 0.0)
    assert q("tight", 0.3) > q("comma", 0.3)
    with pytest.raises(ValueError):
        q("other", 0.2)
    with pytest.raises(ValueError):
        q("none", -0.1)


def test_length_mismatch_is_refused(norms):
    with pytest.raises(ValueError):
        norms.expected_word_log_duration(["a", "b"], [""])
    with pytest.raises(ValueError):
        norms.pause_class(["a", "b"], [""])
