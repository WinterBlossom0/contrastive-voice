"""Repair ("fix your speech"): each operation on synthetic audio, the caps and the planning rules, and real end-to-end checks."""
import json
import math
from pathlib import Path

import numpy as np
import pytest
from synth import recording

from cvoice import config as C, flaws, repair
from cvoice.features import frame_level_db

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery"
SR = C.SR


@pytest.fixture(scope="module")
def rec():
    return recording(16, pauses={9: 0.8})


def words_of(rec, start=None, end=None) -> list[dict]:
    start = rec.al.start if start is None else start
    end = rec.al.end if end is None else end
    return [{"w": rec.tr.disp[i], "p": [round(float(start[i]), 3), round(float(end[i]), 3)]} for i in range(len(rec.tr))]


def result_of(rec, flaws_: list[dict], **words) -> dict:
    return {"regime": "R1", "words": words_of(rec, **words), "rows": [], "flaws": flaws_}


def finding(dim: str, words, delta: float, participant: float = 0.0, baseline: float = 0.0, **kw) -> dict:
    return {"id": kw.pop("id", f"{dim.lower()}-001"), "dimension": dim, "type": kw.pop("type", "T"), "words": list(words),
            "delta": delta, "participant": participant, "baseline": baseline, "context": kw.pop("context", "sentence 1"),
            "counted": True, "group": None, "pattern": None, **kw}


def word_samples(rec, first: int, last: int) -> tuple[int, int]:
    return int(round(round(float(rec.al.start[first]), 3) * SR)), int(round(round(float(rec.al.end[last]), 3) * SR))


def spread(st: np.ndarray, sl: slice) -> float:
    return float(np.nanpercentile(st[sl], 90) - np.nanpercentile(st[sl], 10))


def test_stretch_lengthens_the_words_and_keeps_audio_before_them(rec):
    out = repair.fix_all(result_of(rec, [finding("D1", (2, 6), -math.log(1.3))]), rec.wav)
    start, end = word_samples(rec, 2, 6)
    assert out.fixes[0].status == repair.APPLIED and out.fixes[0].share == 1.0
    assert np.array_equal(out.audio[:start], rec.wav[:start])
    grown = len(out.audio) - len(rec.wav)
    assert abs(grown - 0.3 * (end - start)) < 0.02 * SR  # in-span gaps shorter than PAUSE_MIN_S are scaled with the speech
    assert np.array_equal(out.audio[-SR // 2:], rec.wav[-SR // 2:])
    assert abs(out.to_edited(rec.al.end[-1]) - (rec.al.end[-1] + grown / SR)) < 1e-6


def test_pause_insert_adds_exactly_the_missing_time(rec):
    out = repair.fix_all(result_of(rec, [finding("D2", (4, 5), -0.5, participant=0.06, baseline=0.56)]), rec.wav)
    assert len(out.audio) - len(rec.wav) == int(round(0.5 * SR))
    point = out.operations[0].start
    assert rec.al.end[4] * SR <= point <= rec.al.start[5] * SR  # inside the aligned gap, never in a word onset
    fade = int(round(C.PAUSE_FADE_S * SR))
    assert np.array_equal(out.audio[:point - fade], rec.wav[:point - fade])


def test_pause_shorten_keeps_the_target_length(rec):
    out = repair.fix_all(result_of(rec, [finding("D2", (9, 10), 0.55, participant=0.75, baseline=0.2)]), rec.wav)
    op = out.operations[0]
    assert op.kind == "pause_shorten"
    assert len(rec.wav) - len(out.audio) == (op.end - op.start) - int(round(0.2 * SR))


def test_gain_changes_only_the_region_is_capped_at_6_db_and_stops_before_clipping(rec):
    out = repair.fix_all(result_of(rec, [finding("D5", (2, 6), -6.0)]), rec.wav)
    start, end = word_samples(rec, 2, 6)
    assert out.fixes[0].status == repair.APPLIED
    assert np.array_equal(out.audio[:start], rec.wav[:start]) and np.array_equal(out.audio[end:], rec.wav[end:])
    middle = slice(start + SR // 10, end - SR // 10)
    rise = 20 * np.log10(np.abs(out.audio[middle]).max() / np.abs(rec.wav[middle]).max())
    assert abs(rise - 6.0) < 0.1
    big = repair.fix_all(result_of(rec, [finding("D5", (2, 6), -12.0)]), rec.wav).fixes[0]
    assert big.status == repair.CAPPED and big.applied == repair.MAX_GAIN_DB and big.share == 0.5
    assert big.partial and big.reason.startswith("partial fix")
    loud_wav = rec.wav * (0.75 / np.abs(rec.wav).max())
    loud = repair.fix_all(result_of(rec, [finding("D5", (2, 6), -6.0)]), loud_wav)
    assert loud.fixes[0].status == repair.CAPPED and "clipping" in loud.fixes[0].reason
    assert np.abs(loud.audio).max() <= repair.MAX_PEAK + 1e-4


def test_pitch_scale_widens_the_range_within_the_frame_limit(rec):
    out = repair.fix_all(result_of(rec, [finding("D3", (2, 6), -0.4, participant=4.0, baseline=6.0)]), rec.wav)
    assert out.fixes[0].status in (repair.APPLIED, repair.CAPPED) and len(out.audio) == len(rec.wav)
    assert 0 < out.peak_st[0] <= repair.MAX_FRAME_ST
    start, end = word_samples(rec, 2, 6)
    fade = int(round(C.SPLICE_FADE_S * SR))
    assert np.array_equal(out.audio[:start - fade], rec.wav[:start - fade]) and np.array_equal(out.audio[end + fade:], rec.wav[end + fade:])
    sl = slice(int(rec.al.start[3] / C.HOP_S), int(rec.al.end[5] / C.HOP_S))
    before, after = repair.ac_semitones(rec.wav), repair.ac_semitones(out.audio)
    assert 1.3 < spread(after, sl) / spread(before, sl) < 1.7


def test_frame_change_limit_clips_and_counts():
    f0 = np.full(10, 100.0)
    stats = {}
    new = repair.limit_change(f0, f0 * 2 ** (np.r_[np.zeros(5), np.full(5, 5.0)] / 12), 3.0, stats)
    assert np.allclose(12 * np.log2(new / f0), np.r_[np.zeros(5), np.full(5, 3.0)])
    assert stats == {"peak_st": 3.0, "clipped": 1.0}


def test_pitch_fix_below_the_audible_change_is_skipped(rec):
    out = repair.fix_all(result_of(rec, [finding("D3", (2, 6), -1.8, participant=0.1, baseline=5.0)]), rec.wav)
    assert out.fixes[0].status == repair.SKIPPED and out.operations == []
    assert "1.5 st" in out.fixes[0].reason and np.array_equal(out.audio, rec.wav)


def test_caps_unfixable_and_disfluency(rec):
    out = repair.fix_all(result_of(rec, [finding("D1", (2, 6), -math.log(3.0), id="a"), finding("D6", (2, 6), -1.0, id="b"),
                                         finding("D9", (8, 12), -0.5, id="c", pattern="WORD_REPETITION"),
                                         finding("D1", (11, 14), math.log(3.0), id="d")]), rec.wav)
    status = {fx.finding: fx for fx in out.fixes}
    assert status["a"].status == repair.CAPPED and status["a"].applied == repair.MAX_SLOW_FACTOR
    assert status["a"].share == round(math.log(1.4) / math.log(3.0), 3) and status["a"].reason.startswith("partial fix")
    assert status["d"].status == repair.CAPPED and status["d"].applied == repair.MIN_FAST_FACTOR
    assert status["b"].status == repair.UNFIXABLE and status["c"].status == repair.UNFIXABLE
    assert [op.finding for op in out.operations] == ["a", "d"]
    assert repair.HARD_SLOW_FACTOR < repair.UNVOICED_STRETCH_LIMIT and repair.MAX_EMPHASIS_FACTOR <= repair.MAX_SLOW_FACTOR


def test_group_member_is_covered_only_when_the_owner_edit_moves_its_measure(rec):
    group = ["d1-001", "d9-002", "d2-003"]
    flaws_ = [finding("D1", (2, 6), -0.3, id="d1-001", group=group),
              finding("D9", (2, 6), -0.3, id="d9-002", group=group, counted=False),
              finding("D2", (6, 7), -0.4, id="d2-003", group=group, counted=False, participant=0.06, baseline=0.46)]
    status = {fx.finding: fx.status for fx in repair.fix_all(result_of(rec, flaws_), rec.wav).fixes}
    assert status == {"d1-001": repair.APPLIED, "d9-002": repair.COVERED, "d2-003": repair.APPLIED}


def test_inserted_pause_is_not_scaled_by_a_later_whole_clip_stretch(rec):
    flaws_ = [finding("D2", (4, 5), -0.5, id="p", participant=0.06, baseline=0.56),
              finding("D1", (0, 15), -math.log(1.3), id="t", context="whole passage")]
    both = repair.fix_all(result_of(rec, flaws_), rec.wav)
    only = repair.fix_all(result_of(rec, flaws_[1:]), rec.wav)
    assert abs((len(both.audio) - len(only.audio)) - 0.5 * SR) < 0.02 * SR


def test_placebo_of_gain_and_pause_operations_is_bit_identical(rec):
    out = repair.fix_all(result_of(rec, [finding("D5", (2, 6), -6.0), finding("D2", (9, 10), 0.55, id="d2-002", participant=0.75, baseline=0.2),
                                         finding("D2", (4, 5), -0.5, id="d2-003", participant=0.06, baseline=0.56)]), rec.wav)
    assert np.array_equal(repair.placebo_audio(out), rec.wav)


def test_pitch_placebo_is_bit_identical_and_a_whole_clip_pitch_edit_keeps_the_pauses(rec):
    out = repair.fix_all(result_of(rec, [finding("D3", (0, 15), -0.4, participant=4.0, baseline=6.0, context="whole passage")]), rec.wav)
    assert out.operations[0].whole_clip and not np.array_equal(out.audio, rec.wav)
    assert np.array_equal(repair.placebo_audio(out), rec.wav)
    pause0, pause1 = out.speaker.pause_spans[9]
    guard = repair.PITCH_SPLICE_PAD_S + C.SPLICE_FADE_S + C.HOP_S
    quiet = slice(int((pause0 + guard) * SR), int((pause1 - guard) * SR))
    assert quiet.stop - quiet.start > SR // 10 and np.array_equal(out.audio[quiet], rec.wav[quiet])
    start, end = word_samples(rec, 2, 6)
    times = np.arange(start, end, C.HOP) / SR
    flat = repair.Operation("pitch_contour", start, end, 0.0, "c", contour=(times, np.zeros(len(times))), words=(2, 6))
    assert np.array_equal(repair.run_operations(out.speaker, [flat])[0], rec.wav)


def test_scaled_operation_is_the_dose_and_zero_is_the_placebo():
    ops = [repair.Operation("stretch", 0, SR, 1.44, "a"), repair.Operation("pause_insert", 5, 5, 0.4, "b"),
           repair.Operation("pause_shorten", 0, SR, 0.2, "c"), repair.Operation("pitch_scale", 0, SR, 2.25, "d"),
           repair.Operation("pitch_contour", 0, SR, 1.0, "e"), repair.Operation("emphasis", 0, SR, (1.44, 2.0, 4.0), "f"),
           repair.Operation("gain", 0, SR, 6.0, "g")]
    half = [op.scaled(0.5).value for op in ops]
    assert np.allclose(np.hstack(half), [1.2, 0.2, 0.6, 1.5, 0.5, 1.2, 1.0, 2.0, 3.0])
    nulls = [op.null().value for op in ops]
    assert nulls == [1.0, 0.0, 1.0, 1.0, 0.0, (1.0, 0.0, 0.0), 0.0]


def test_gain_dose_is_monotone(rec):
    op = repair.fix_all(result_of(rec, [finding("D5", (2, 6), -6.0)]), rec.wav).operations[0]
    sp = repair.speaker(result_of(rec, []), rec.wav)
    start, end = word_samples(rec, 2, 6)
    levels = [frame_level_db(repair.run_operations(sp, [op.scaled(s)])[0])[start // C.HOP + 10:end // C.HOP - 10].mean()
              for s in (0.0, 0.5, 1.0)]
    assert levels[0] < levels[1] < levels[2] and abs((levels[2] - levels[0]) - 6.0) < 0.3


def round_two(rec, first, flaws_):
    """The edited audio of `first` with its own result (word times through the time map) and the round-2 outcome."""
    starts, ends = first.to_edited(rec.al.start, "right"), first.to_edited(rec.al.end, "left")
    return repair.repair(result_of(rec, flaws_, start=starts, end=ends), first.audio, flaws_, prior=first)


def test_second_round_stays_inside_the_hard_caps(rec):
    first = repair.fix_all(result_of(rec, [finding("D1", (2, 6), -math.log(3.0), id="t"), finding("D5", (9, 12), -12.0, id="g")]), rec.wav)
    second = round_two(rec, first, [finding("D1", (2, 6), -math.log(2.0), id="t2"), finding("D5", (9, 12), -6.0, id="g2")])
    status = {fx.finding: fx for fx in second.fixes}
    assert status["t2"].round == 2 and math.isclose(status["t2"].applied, repair.HARD_SLOW_FACTOR / repair.MAX_SLOW_FACTOR)
    assert status["g2"].status == repair.SKIPPED and "already use the whole allowed change" in status["g2"].reason
    assert second.rounds == 2 and len(second.operations) == 3 and second.operations[2].round == 2
    start, end = word_samples(rec, 2, 6)
    total = (second.to_edited(rec.al.end[6]) - second.to_edited(rec.al.start[2], "right")) / ((end - start) / SR)
    assert abs(total - repair.HARD_SLOW_FACTOR) < 0.05
    assert abs(len(second.audio) - len(rec.wav) - (repair.HARD_SLOW_FACTOR - 1) * (end - start)) < 0.03 * SR
    assert len(repair.placebo_audio(second)) == len(rec.wav)


def test_overlapping_fixes_of_one_round_share_the_hard_caps_and_never_reverse(rec):
    flaws_ = [finding("D1", (2, 6), -math.log(3.0), id="t"), finding("D5", (2, 6), -12.0, id="g"),
              finding("D4", (6, 6), -3.0, participant=-2.0, baseline=1.0, id="e"), finding("D5", (5, 8), -12.0, id="g2")]
    out = repair.fix_all(result_of(rec, flaws_), rec.wav)
    status = {fx.finding: fx for fx in out.fixes}
    factor, _, gain = status["e"].applied
    assert math.isclose(status["t"].applied * factor, repair.HARD_SLOW_FACTOR) and gain == 0.0  # word 6 has the 6 dB of g
    assert status["g2"].status == repair.SKIPPED
    spent = repair.Budget(time_max=2.0, time_min=2.0, gain_max=9.0, gain_min=9.0)
    assert repair.time_limits(spent) == (repair.MIN_FAST_FACTOR, 1.0) and repair.gain_limits(spent) == (-15.0, 0.0)


def test_listen_pairs_give_the_region_in_both_recordings(rec):
    out = repair.fix_all(result_of(rec, [finding("D1", (2, 6), -math.log(1.3))]), rec.wav)
    pair = repair.listen_pairs(out, context_s=0.5)[0]
    (a, b), (c, d) = pair["original"], pair["edited"]
    assert pair["words"] == [2, 6] and abs(a - c) < 1e-3 and abs((d - c) / (b - a) - 1.3) < 0.05
    assert pair["original_context"] == [round(a - 0.5, 3), round(b + 0.5, 3)]


# ============================================================================================ real audio (aligner needed)
def gallery_kwargs():
    from cvoice.align import load_aligner
    text = json.loads((GALLERY / "index.json").read_text())["baseline"]["text"]
    return dict(transcript=text, baseline=GALLERY / "audio/reagan_farewell_1989.wav", aligner=load_aligner())


@pytest.mark.slow
def test_gallery_l3a_fix_all_removes_flags_within_the_caps_and_the_placebo_does_not():
    original = json.loads((GALLERY / "results/L3A.json").read_text())
    kwargs = gallery_kwargs()
    out = repair.fix_all(original, GALLERY / "audio/L3A.wav", transcript=kwargs["transcript"])
    check = repair.verify(out, original, kwargs)
    status = {fx.finding: fx for fx in out.fixes}
    assert check["reproduced"]
    assert status["d3-001"].status == repair.SKIPPED  # x1.5 of a 0.07 st range is inaudible
    assert status["d1-003"].status == repair.CAPPED and status["d5-005"].status == repair.CAPPED
    assert "d2-002" in check["removed"] and check["new_findings"] == []
    assert check["score"] > original["scores"]["overall"] + 8  # 86.11 -> 96.17 when written
    assert check["placebo"]["within_tolerance"] and check["placebo"]["new_findings"] == [] and check["placebo"]["removed"] == []
    assert check["alignment"]["word_middles_inside_aligned_word"] == 1.0


@pytest.mark.slow
def test_gallery_r2_contour_widens_a_flat_reading_with_the_reference_melody():
    original = json.loads((GALLERY / "results/greenman_botched.json").read_text())
    kwargs = gallery_kwargs()
    out = repair.fix_all(original, GALLERY / "audio/greenman_botched.wav", pitch_method="contour", transcript=kwargs["transcript"])
    check = repair.verify(out, original, kwargs)
    assert original["regime"] == "R2" and check["reproduced"]
    assert "d3-001" in check["removed"] and check["new_findings"] == []
    assert check["score"] > original["scores"]["overall"] + 20  # 73.6 -> 99.98 when written
    assert check["placebo"]["within_tolerance"] and check["placebo"]["new_findings"] == []
    pitch = check["pitch_check"][0]
    assert pitch["agree"] and pitch["autocorrelation"]["change_st"] > 3 and out.peak_st[0] <= repair.MAX_FRAME_ST + 1e-9


@pytest.mark.slow
def test_over_inflected_real_speech_is_narrowed_toward_the_target():
    """The detector has no flag for a too-wide pitch range, so the finding is written by hand: the identity clip with the
    pitch excursions of words 29-36 doubled by the project's flatten edit at negative strength. When written: range 4.99 st
    widened to 7.24 st, narrowed by 1.1 st (autocorrelation) and 3.1 st (cross-correlation) at the x1/1.5 cap."""
    result = json.loads((GALLERY / "results/identity.json").read_text())
    text = json.loads((GALLERY / "index.json").read_text())["baseline"]["text"]
    wav = repair.load(GALLERY / "audio/identity.wav")
    sp = repair.speaker(result, wav, text)
    first, last = 29, 36
    wide = flaws.flatten_span(wav, *sp.word_span(first, last), strength=-1.0)
    track0, track1 = repair.ac_semitones(wav), repair.ac_semitones(wide)
    target, participant = (repair.median_window_range(t, sp, first, last) for t in (track0, track1))
    assert participant > target + 2
    f = finding("D3", (first, last), repair.range_ln_ratio(target, participant), participant=round(participant, 2),
                baseline=round(target, 2), type="RANGE_WIDE")
    out = repair.fix_all({**result, "flaws": [f]}, wide, transcript=text)
    fix = out.fixes[0]
    assert out.operations[0].value < 1 and fix.status in (repair.APPLIED, repair.CAPPED)
    check = repair.pitch_check(out)[0]
    assert check["agree"] and check["autocorrelation"]["change_st"] < -1.0 and check["cross_correlation"]["change_st"] < -1.0
    assert abs(check["autocorrelation"]["after_st"] - target) < abs(participant - target)
