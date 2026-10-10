"""Passage selection end to end with planted emissions (no model): the 'audio' is a ramp that tells the fake aligner its offset."""
import numpy as np
import pytest

from cvoice import config as C
from cvoice.align import LABELS, VOCAB, Alignment, TranscriptMismatch, parse_transcript
from cvoice import passages
from cvoice.passages import Group, candidate_windows, locate_many, page_text, select_passages, sentence_anchors, window_of
from cvoice.pipeline import make_job, run_jobs

WPS = 2.5  # words per second of the planted speech
SCALE = 4e6


def locate(fake, wav, official):
    """Sentence anchors of one recording."""
    return locate_many([wav], [official], aligner=fake)[0]


def select_passage(fake, wavs, official, anchor_lists, allowed=None):
    """The best shared window of one group of recordings."""
    return select_passages([Group("", wavs, official, anchor_lists, allowed)], None, fake)[0]


def make_passage(fake, wav, official, anchors, first, last):
    """The passage of sentences first..last of one recording, force-aligned as select_passages does it."""
    tr, crop, off = window_of(wav, official, anchors, first, last)
    a = run_jobs([make_job(crop, tr, "align")], None, fake)[0]
    return passages.passage_from(wav, tr, anchors, first, last, Alignment(a.start + off, a.end + off, a.compat, a.mean_compat))


def official_text():
    letters = "abcdefghijklmnopqrstuvwxyz"
    words = ["".join(letters[(i // 26 ** k) % 26] for k in range(4)) + "e" for i in range(240)]  # unique, so difflib cannot cheat
    return " ".join(" ".join(words[k * 20:(k + 1) * 20]).capitalize() + "." for k in range(12))


def make_fake(tr, drop=(), t0=3.0):
    """wav: ramp encoding the sample index; emissions: planted char spikes of every official word that is spoken."""
    times = {i: (t0 + i / WPS, t0 + i / WPS + 0.32) for i in range(len(tr)) if i not in drop}
    total = t0 + len(tr) / WPS + 3.0
    wav = np.arange(int(total * C.SR)) / SCALE

    def fake_emissions(aligner, w):
        off = int(round(w[0] * SCALE)) / C.SR
        T = (len(w) - 400) // 320 + 1
        lp = np.full((T, len(LABELS)), np.log(1e-4))
        lp[:, 0] = np.log(0.9)
        for i, (a, b) in times.items():
            if b < off or a > off + T * 0.02:
                continue
            word = tr.norm[i]
            for k, ch in enumerate(word):
                f = int(round((a + (k + 0.5) * (b - a) / len(word) - off) / 0.02))
                if 0 <= f < T:
                    lp[f, :] = np.log(1e-4)
                    lp[f, VOCAB[ch]] = np.log(0.95)
            f = int(round((b + 0.06 - off) / 0.02))
            if 0 <= f < T:
                lp[f, :] = np.log(1e-4)
                lp[f, VOCAB["|"]] = np.log(0.95)
        return lp

    class Fake:  # the aligner interface the pipeline uses: .emissions(wav)
        def emissions(self, w):
            return fake_emissions(None, w)

    return wav, times, Fake()


def test_select_passage_finds_the_best_window_forces_alignment_and_cuts_the_clip():
    official = parse_transcript(official_text())
    assert official.n_sentences == 12 and len(official) == 240
    wav, times, fake = make_fake(official, drop=set(range(60, 80)))  # sentence 3 was never spoken
    anchors = locate(fake, wav, official)
    assert [a.eligible for a in anchors] == [True, True, True, False] + [True] * 8 and anchors[3].coverage == 0.0
    ps = select_passage(fake, [wav], official, [anchors])
    p = ps[0]
    s0, s1 = p.meta["sentences"]
    assert s0 > 3 or s1 < 3  # never across the unspoken sentence
    dur = p.meta["source_end_s"] - p.meta["source_start_s"]
    assert C.PASSAGE_S[0] <= dur <= C.PASSAGE_S[1] and p.meta["n_words"] == len(p.tr) == 20 * (s1 - s0 + 1)
    # forced alignment recovered the planted times (within one 20 ms frame) and the clip has CLIP_PAD_S around the words
    w0 = anchors[s0].w0
    assert p.meta["source_start_s"] == pytest.approx(times[w0][0] + 0.32 / len(official.norm[w0]) * 0.5, abs=0.25)
    assert p.meta["clip_offset_s"] == pytest.approx(p.meta["source_start_s"] - C.CLIP_PAD_S, abs=0.03)
    assert p.meta["clip_duration_s"] == pytest.approx(dur + 2 * C.CLIP_PAD_S, abs=0.1) and len(p.wav) == round(p.meta["clip_duration_s"] * C.SR)
    assert p.meta["qa"]["mean_compat"] > 0.8 and p.tr == official.slice(w0, anchors[s1].w1)  # the slice itself, sentence indices included
    assert parse_transcript(p.meta["text"]).norm == p.tr.norm  # the manifest text round-trips


def test_two_recordings_share_the_window_and_restrict_to_sentences_anchored_in_both():
    official = parse_transcript(official_text())
    wavA, _, fakeA = make_fake(official)
    wavB, _, fakeB = make_fake(official, drop=set(range(0, 100)), t0=5.0)  # the second reading starts at sentence 5
    anchors = []
    for wav, fake in ((wavA, fakeA), (wavB, fakeB)):
        anchors.append(locate(fake, wav, official))
    both = passages.candidate_windows(anchors)
    assert both and all(w["first"] >= 5 for w in both)
    only_a = passages.candidate_windows([anchors[0]])
    assert any(w["first"] < 5 for w in only_a)

    for name, wav in (("A", wavA), ("B", wavB)):
        p = make_passage(fakeA if name == "A" else fakeB, wav, official, anchors[0 if name == "A" else 1], both[0]["first"], both[0]["last"])
        assert p.tr.norm == official.slice(anchors[0][both[0]["first"]].w0, anchors[0][both[0]["last"]].w1).norm


def test_a_window_that_does_not_align_is_rejected():
    official = parse_transcript(official_text())
    wav, times, fake = make_fake(official)
    anchors = locate(fake, wav, official)
    other = parse_transcript(" ".join(["zzzz"] * 240))  # the transcript the audio does not read
    with pytest.raises(TranscriptMismatch, match="does not match"):  # passage selection is a trust boundary
        make_passage(fake, wav, other, anchors, 4, 5)
    with pytest.raises(RuntimeError, match="no eligible"):
        select_passage(fake, [wav], official, [[a.__class__(a.k, a.w0, a.w1, 0.0, False, None, None) for a in anchors]])


def test_groups_are_selected_in_rounds_and_a_failing_window_moves_only_its_group_on(monkeypatch):
    official = parse_transcript(official_text())
    wav, _, fake = make_fake(official)
    anchors = locate(fake, wav, official)
    only = set(range(6, 12))
    g1, g2 = Group("one", [wav], official, [anchors]), Group("two", [wav], official, [anchors], allowed=only)
    solo1, solo2 = select_passage(fake, [wav], official, [anchors])[0], select_passage(fake, [wav], official, [anchors], allowed=only)[0]
    second = passages.candidate_windows([anchors], only)[1]
    calls, real = [], passages.passage_from

    def flaky(wav_, tr, anchors_, a, b, al):
        calls.append((a, b))
        if len(calls) == 2:  # round 0, second group
            raise TranscriptMismatch("planted failure")
        return real(wav_, tr, anchors_, a, b, al)

    monkeypatch.setattr(passages, "passage_from", flaky)
    one, two = select_passages([g1, g2], None, fake)
    assert one[0].meta["sentences"] == solo1.meta["sentences"] and two[0].meta["sentences"] == [second["first"], second["last"]]
    assert two[0].meta["sentences"] != solo2.meta["sentences"] and len(calls) == 3  # group one was not retried
    with pytest.raises(RuntimeError, match="gone: no passage window survived.*planted"):
        monkeypatch.setattr(passages, "passage_from", lambda *a: (_ for _ in ()).throw(TranscriptMismatch("planted")))
        select_passages([Group("gone", [wav], official, [anchors])], None, fake, max_tries=2)


def test_page_text_keeps_article_paragraphs_and_strips_gutenberg_boilerplate(tmp_path):
    (tmp_path / "a.html").write_text("<html><head><title>x</title></head><body><nav>one two three four five six seven</nav>"
                                     "<p>Good evening. Today our fellow citizens were attacked.</p><script>var a = 1;</script>"
                                     "<div>short</div><p>We stand together as one nation tonight.</p></body></html>")
    t = page_text(tmp_path / "a.html")
    assert "Good evening" in t and "stand together" in t and "var a" not in t and "one two three" not in t
    assert "short." in t.splitlines()  # a heading gets a full stop so it cannot run into the next sentence
    (tmp_path / "g.txt").write_text("legal\n*** START OF THE PROJECT GUTENBERG EBOOK X ***\nFour score and seven years ago\n*** END OF THE PROJECT GUTENBERG EBOOK X ***\nlicense")
    assert page_text(tmp_path / "g.txt").strip() == "Four score and seven years ago"


def greedy_decode(official, drop=(), t0=0.0, wps=2.5):
    """Greedy-decode stand-in: every official word spoken at wps words per second except the dropped indices."""
    return [{"norm": w, "start": t0 + i / wps, "end": t0 + i / wps + 0.2} for i, w in enumerate(official.norm) if i not in drop]


def test_sentence_anchors_and_window_ranking():
    words = [f"{'abcdefghijkl'[k]}{'mnopqrstuvwx'[i % 12]}{'bcdfghjklmnp'[i // 12 * 3 % 12]}" for k in range(8) for i in range(25)]
    tr = parse_transcript(" ".join(" ".join(words[k * 25:(k + 1) * 25]).capitalize() + "." for k in range(8)))
    assert tr.n_sentences == 8 and len(tr) == 200
    dec = greedy_decode(tr, drop={50 + 3, 50 + 7})  # sentence 2 has two words missing: still >= 80 % anchored
    anchors = sentence_anchors(tr, dec)
    assert all(a.eligible for a in anchors) and anchors[2].coverage == pytest.approx(23 / 25)
    assert anchors[1].start == pytest.approx(25 / 2.5) and anchors[1].end == pytest.approx(49 / 2.5 + 0.2)
    broken = greedy_decode(tr, drop=set(range(100, 125)) | {125})  # sentence 4 gone, sentence 5 loses its first word
    a2 = sentence_anchors(tr, broken)
    assert not a2[4].eligible and not a2[5].eligible and a2[3].eligible
    wins = candidate_windows([a2])
    assert wins and all(20 <= w["durations"][0] <= 40 for w in wins)
    assert all(not (w["first"] <= 4 <= w["last"]) for w in wins)
    best = wins[0]
    assert best["min_coverage"] == max(w["min_coverage"] for w in wins)
    assert candidate_windows([a2], allowed={0, 1, 2}) and all(w["last"] <= 2 for w in candidate_windows([a2], allowed={0, 1, 2}))
    both = candidate_windows([anchors, a2])  # eligible in both recordings only
    assert all(not (w["first"] <= 4 <= w["last"]) for w in both)
