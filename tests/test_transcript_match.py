"""Partial-mismatch refusal of uploads (align.require_full_match) on planted emissions and synthetic evidence."""
import numpy as np
import pytest
from test_align import planted_logp

from cvoice import config as C, pipeline
from cvoice.align import (MISMATCH_PART, Alignment, TranscriptMismatch, align_emissions, parse_transcript,
                          require_full_match, spread_rate, words_near, worst_window)

READ = parse_transcript("We are met on a great battlefield of that war. We have come to dedicate a portion of that field "
                        "as a final resting place for those who here gave their lives.")


def planted(norm):
    """Emissions of a reading of `norm` (one confident spike block per character)."""
    return planted_logp(tuple(norm))[0]


def refusal(logp, tr):
    with pytest.raises(TranscriptMismatch) as caught:
        require_full_match(align_emissions(logp, tr.norm), tr)
    return caught.value


def test_the_exact_transcript_passes_with_no_evidence():
    al = align_emissions(planted(READ.norm), READ.norm)
    assert require_full_match(al, READ) is al
    assert al.missing.max() < 0.1 and al.extra.max() < 0.1


def test_a_transcript_of_only_the_first_sentence_is_refused_near_its_end():
    first = parse_transcript("We are met on a great battlefield of that war.")
    e = refusal(planted(READ.norm), first)
    assert e.kind == MISMATCH_PART and e.near and set(e.near.split()) <= set(first.disp) and e.at_s is not None


def test_a_sentence_that_was_never_read_is_refused_and_quoted():
    added = parse_transcript(" ".join(READ.disp) + ". And the moon is made of green cheese today.")
    e = refusal(planted(READ.norm), added)
    assert e.kind == MISMATCH_PART and set(e.near.split()) & {"moon", "made", "green", "cheese", "today"}


def test_every_second_word_is_refused():
    e = refusal(planted(READ.norm), parse_transcript(" ".join(READ.disp[::2])))
    assert e.kind == MISMATCH_PART


def test_one_repeated_short_word_in_the_audio_is_not_refused():
    spoken = list(READ.norm[:5]) + [READ.norm[4]] + list(READ.norm[5:])   # "a" read twice
    al = align_emissions(planted(spoken), READ.norm)
    assert require_full_match(al, READ) is al


def test_worst_window_finds_the_largest_sum_and_its_first_frame():
    frames = int(round(1.0 / C.CTC_FRAME_S))
    values = np.zeros(10 * frames)
    values[3 * frames + 5:3 * frames + 8] = 40.0
    total, first = worst_window(values, 1.0)
    assert total == 120.0 and values[first:first + frames].sum() == 120.0 and first <= 3 * frames + 5
    assert worst_window(np.ones(5), 1.0) == (5.0, 0)   # a recording shorter than the window: the whole sum


def test_evidence_just_at_the_limit_passes_and_just_above_is_refused():
    n = 400
    words = parse_transcript("one two three four five six")
    al = Alignment(np.linspace(0, 6, 6), np.linspace(0.5, 6.5, 6), np.ones(6), 1.0, missing=np.zeros(n, np.float32),
                   extra=np.zeros(n, np.float32))
    al.extra[200] = C.MISMATCH_EXTRA_MAX
    assert require_full_match(al, words) is al
    al.extra[201] = 0.5
    with pytest.raises(TranscriptMismatch) as caught:
        require_full_match(al, words)
    assert caught.value.kind == MISMATCH_PART and "extra evidence" in str(caught.value)
    al.extra[:] = 0
    al.missing[50] = C.MISMATCH_MISSING_MAX + 1
    with pytest.raises(TranscriptMismatch, match="missing evidence"):
        require_full_match(al, words)


def test_an_alignment_without_evidence_cannot_pass_the_upload_check():
    al = Alignment(np.zeros(1), np.ones(1), np.ones(1), 1.0)
    with pytest.raises(ValueError, match="no mismatch evidence"):
        require_full_match(al, parse_transcript("word"))


def test_words_near_quotes_from_the_word_at_the_time_or_the_nearest_word():
    al = Alignment(np.arange(8.0), np.arange(8.0) + 0.8, np.ones(8), 1.0)
    assert words_near(al, 1.5) == (1, C.MISMATCH_QUOTE_WORDS)
    assert words_near(al, 2.95) == (3, 2 + C.MISMATCH_QUOTE_WORDS)   # between words 2 and 3, nearer to 3
    assert words_near(al, 20.0) == (7, 7)


class PlantedAligner:
    def __init__(self, logp):
        self.logp, self.calls = logp, 0

    def emissions(self, wav):
        self.calls += 1
        return self.logp


def test_every_reading_of_a_bank_is_checked_and_named():
    other = parse_transcript("Four score and seven years ago our fathers brought forth on this continent a new nation.")
    aligner = PlantedAligner(planted(other.norm + READ.norm))
    wav = np.zeros(16000)
    with pytest.raises(TranscriptMismatch) as caught:
        pipeline.reference_recording(wav, 2, READ, aligner, None, True)
    assert caught.value.roles == ("reference 3",) and caught.value.kind == MISMATCH_PART


def test_an_old_cache_file_without_evidence_is_aligned_again(tmp_path):
    lp = planted(READ.norm)
    aligner = PlantedAligner(lp)
    wav = np.zeros(int(len(lp) * C.CTC_FRAME_S * C.SR))
    _, first = pipeline.align_wav(wav, READ, aligner, tmp_path)
    cache = next(tmp_path.glob("align_*_v2.npz"))
    with np.load(cache) as z:
        old = {k: z[k] for k in z.files if k not in ("missing", "extra")}
    np.savez(cache, **old)
    _, again = pipeline.align_wav(wav, READ, aligner, tmp_path)
    assert aligner.calls == 2
    np.testing.assert_array_equal(again.extra, first.extra)
    _, cached = pipeline.align_wav(wav, READ, aligner, tmp_path)
    assert aligner.calls == 2 and len(cached.missing) == len(lp)


def test_the_self_mode_refuses_a_partial_transcript_before_any_measurement():
    first = parse_transcript("We are met on a great battlefield of that war.")
    lp = planted(READ.norm)
    wav = np.zeros(int(len(lp) * C.CTC_FRAME_S * C.SR))
    with pytest.raises(TranscriptMismatch) as caught:
        pipeline.analyze(wav, first, aligner=PlantedAligner(lp), refuse_mismatch=True)
    assert caught.value.roles == ("participant",) and caught.value.kind == MISMATCH_PART


def test_spread_rate_ignores_the_worst_window_and_counts_the_rest_per_second():
    frames_per_s = int(round(1 / C.CTC_FRAME_S))
    one_phrase = np.zeros(20 * frames_per_s)
    one_phrase[100:110] = 30.0   # a restart: all inside one window
    assert spread_rate(one_phrase) == 0.0
    spread = np.zeros(20 * frames_per_s)
    spread[::frames_per_s] = 15.0   # one uncovered spike per second all through the reading
    exclude = int(round(C.MISMATCH_SPREAD_EXCLUDE_S))
    assert spread_rate(spread) == pytest.approx(15.0 * (20 - exclude) / 20)
