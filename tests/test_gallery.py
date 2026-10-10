import pytest

from synth import recording, regime

from cvoice import config as C, gallery, patterns, pipeline
from cvoice.compare import compare
from cvoice.detect import Region, make_detector
from cvoice.events import Run
from cvoice.score import score


def test_gallery_has_an_edited_and_a_botched_other_performance():
    items = {i["id"]: i for i in gallery.items()}
    for id_, clip in (("greenman_edited", "greenman_reagan__x3_L3"), ("greenman_botched", "greenman_reagan__G5")):
        assert items[id_]["group"] == "Other performance" and items[id_]["regime"] == "R2" and items[id_]["clip"] == clip


def _truth(typ, dim, sign, words, al, event="span"):
    span = (float(al.start[words[0]]), float(al.end[words[1]]))
    return {"type": typ, "level": 3, "dim": dim, "sign": sign, "span": span, "event": event, "available": True,
            "secondary": (), "mid": 0.5 * sum(span), "words": list(words), "label_words": list(words)}


def test_truth_markers_use_the_evaluator_match_and_whole_clip_flags(monkeypatch):
    B = recording(40, pauses={7: 0.7, 19: 0.8})
    comp = compare(B, B)
    rush = Region("D1", -1, 5, 9, 7, -5.0, tuple(range(5, 10)))
    run = Run(B, B, comp, [rush], score(comp, [], regime("R1"), C.PMAX_START), "R1", {"D1": -0.4})
    info = patterns.describe(rush, comp, B, B)
    flaws = [{"id": "d1-001", "dimension": "D1", "words": [0, 39], "p": [0.0, 1.0], "context": "whole passage"},
             {"id": "d1-002", "dimension": "D1", "words": info["words"], "p": [round(float(v), 3) for v in info["p"]], "context": "sentence 1"}]
    al = B.al
    edits = [_truth("RUSH", "D1", -1, (5, 9), al),           # local edit: the IoU match of events.match
             _truth("RUSH", "D1", -1, (0, 39), al),          # whole-passage rush: the overall-tempo flag
             _truth("DRAG", "D1", 1, (0, 39), al),           # whole-passage drag: the overall flag is faster, so no match
             _truth("MONOTONE", "D3", -1, (0, 39), al)]      # no overall pitch-range flag
    monkeypatch.setattr(gallery, "truths", lambda lab, **kw: edits)
    monkeypatch.setattr(gallery, "run_pair", lambda *a: run)
    out = gallery.truth_markers({}, B, B, {"regimes": {"R1": regime("R1")}}, "R1", {"flaws": flaws, "differences": []})
    assert [t["finding"] for t in out] == ["d1-002", "d1-001", None, None]
    assert all(t["difference"] is None for t in out) and out[1]["words"] == [0, 39]


def test_truth_markers_name_the_same_change_detection_and_its_duplicates(monkeypatch):
    B = recording(40, pauses={7: 0.7, 19: 0.8})
    comp = compare(B, B)
    d9 = [Region("D9", -1, 5, 8, 6, -5.0, tuple(range(5, 9))), Region("D9", -1, 9, 10, 9, -4.0, (9, 10)),
          Region("D9", -1, 30, 32, 31, -4.0, (30, 31, 32))]
    run = Run(B, B, comp, d9, score(comp, [], regime("R1"), C.PMAX_START), "R1", {})
    edits = [_truth("RUSH", "D1", -1, (5, 9), B.al)]
    monkeypatch.setattr(gallery, "truths", lambda lab, **kw: edits)
    monkeypatch.setattr(gallery, "run_pair", lambda *a: run)
    monkeypatch.setattr(gallery, "finding_ids", lambda *a: {0: "d9-001", 1: "d9-002", 2: "d9-003"})
    duplicates = [{"index": 1, "change": "D1-"}, {"index": 2, "change": "D1-"}]   # region 2 lies away from the edit
    monkeypatch.setattr(gallery, "truth_changes", lambda run, tr, pairs: ({0: 0}, duplicates))
    out = gallery.truth_markers({}, B, B, {"regimes": {"R1": regime("R1")}}, "R1", {"flaws": [], "differences": []})
    assert (out[0]["finding"], out[0]["same_change"], out[0]["duplicate_findings"]) == ("d9-001", True, ["d9-002"])


def test_whole_passage_edit_links_the_whole_passage_difference(monkeypatch):
    B = recording(40, pauses={7: 0.7, 19: 0.8})
    comp = compare(B, B)
    run = Run(B, B, comp, [], score(comp, [], regime("R2"), C.PMAX_START), "R2", {})
    differences = [{"id": "x1", "dimension": "D1", "words": [6, 8], "delta": -0.36},    # local faster span inside the passage
                   {"id": "x2", "dimension": "D1", "words": None, "delta": 0.2},         # whole passage, slower
                   {"id": "x3", "dimension": "D1", "words": None, "delta": -0.47}]       # whole passage, faster
    edits = [_truth("RUSH", "D1", -1, (0, 39), B.al),          # whole-passage rush: the faster whole-passage entry
             _truth("RUSH", "D1", -1, (5, 9), B.al)]           # local rush: the overlapping local entry
    monkeypatch.setattr(gallery, "truths", lambda lab, **kw: edits)
    monkeypatch.setattr(gallery, "run_pair", lambda *a: run)
    out = gallery.truth_markers({}, B, B, {"regimes": {"R2": regime("R2")}}, "R2", {"flaws": [], "differences": differences})
    assert [t["difference"] for t in out] == ["x3", "x1"]


def test_showcase_description_counts_edits_and_states_each_outcome():
    def flaw(typ, excluded=()):
        return {"type": typ, "level": 3, "span": [0, 16000], "words": [0, 2], "evaluation_excluded": list(excluded)}

    def marker(typ, finding=None, difference=None, status="enabled", excluded=None):
        return {"type": typ, "dimension": C.FLAW_REGISTRY[typ]["primary"], "words": [0, 2], "finding": finding, "difference": difference,
                "detector_status": status, "p": [0.0, 1.0], **({"excluded": excluded} if excluded else {})}
    lab = {"flaws": [flaw("NATURAL_RUSH"), flaw("WORD_REPETITION"), flaw("WORD_REPETITION"), flaw("RISING_ENDING"),
                     flaw("LOW_EFFORT", ["realised change below half target or wrong sign"]), {**flaw("FADE"), "placebo": True}]}
    res = {"regime": "R1", "differences": [{"id": "x1", "status": "listed"}], "flaws": [],
           "truth": [marker("NATURAL_RUSH"), marker("WORD_REPETITION", difference="x1", status="unscored"),
                     marker("WORD_REPETITION", status="unscored"), marker("RISING_ENDING", finding="d8-004"),
                     marker("LOW_EFFORT", excluded=["realised change below half target or wrong sign"])]}
    assert gallery.edits_text(lab, res) == (
        "5 edits injected; evaluated: natural rush (missed), word repetition (1 listed entry, 1 not scored), rising ending (found). "
        "1 excluded from evaluation, because the realised change failed the label checks: low effort.")
    assert gallery.edits_text({"flaws": lab["flaws"][:1]}, {"regime": "R1", "differences": [], "flaws": [], "truth": res["truth"][:1]}) == (
        "1 edit injected; evaluated: natural rush (missed).")
    on_excluded = {**res, "truth": [*res["truth"][:4], {**res["truth"][4], "p": [1.0, 2.0], "on_edit": ["d5-001"]}],
                   "flaws": [{"id": "d5-001", "dimension": "D5", "words": [5, 6], "delta": -6.0, "context": "", "p": [1.5, 1.8], "points_lost": 1.25},
                             {"id": "d3-001", "dimension": "D3", "words": [7, 9], "delta": -1.0, "context": "", "p": [1.9, 3.0], "points_lost": 4.0}]}
    assert gallery.edits_text(lab, on_excluded).endswith(
        "1 finding lies on the excluded low effort edit and cost 1.25 points of the delivery index; the evaluation does not count them as false. "
        "1 finding matches no injected edit and cost 4.00 points of the delivery index.")


def test_a_finding_on_a_missed_edit_is_named_and_not_counted_off_truth():
    """A finding of the edit's dimension and direction that shares a word with a missed windowed edit lies on it; the
    evaluation's overlap rule did not match it, so the description says why instead of calling it off-truth."""
    lab = {"flaws": [{"type": "MONOTONE", "level": 3, "span": [0, 16000], "words": [30, 36]}]}
    marker = {"type": "MONOTONE", "dimension": "D3", "words": [30, 36], "finding": None, "difference": None,
              "detector_status": "enabled", "p": [9.11, 11.1]}
    on_edit = {"id": "d3-001", "dimension": "D3", "type": "MONOTONE", "words": [32, 36], "delta": -1.76, "context": "",
               "p": [10.16, 11.04], "points_lost": 0.96}
    res = {"regime": "SELF", "differences": [], "flaws": [on_edit], "truth": [marker]}
    assert gallery.edits_text(lab, res) == ("1 edit injected; evaluated: monotone (missed: a monotone finding lies on the edit but "
                                            "overlaps it by less than the evaluation's 50% rule).")
    assert gallery.off_truth(res) == []
    wider = {**on_edit, "delta": 1.2}  # the other direction lies on the edit's words but is not the edit's change
    assert gallery.off_truth({**res, "flaws": [wider]}) == [wider]
    assert gallery.edits_text(lab, {**res, "flaws": [wider]}).startswith("1 edit injected; evaluated: monotone (missed).")


def test_excluded_edits_get_unmatched_markers_with_their_reasons():
    reason = "realised change below half target or wrong sign"
    lab = {"flaws": [{"type": "LOW_EFFORT", "level": 3, "span": [16000, 32000], "words": [4, 6], "evaluation_excluded": [reason]},
                     {"type": "RISING_ENDING", "level": 3, "span": [48000, 52000], "words": [9, 9], "evaluation_excluded": []}]}
    reg = {"enabled": ["D5", "D8"]}
    out = gallery.excluded_markers(lab, reg)
    assert out == [{"type": "LOW_EFFORT", "dimension": "D5", "level": 3, "available": True, "detector_status": "enabled", "p": [1.0, 2.0],
                    "words": [4, 6], "finding": None, "difference": None, "excluded": [reason], "on_edit": []}]
    picked = gallery.pick_showcase([({"id": "a"}, {"flaws": [{"id": "d5-001", "dimension": "D5"}], "truth": out})],
                                   [next(s for s in gallery.SHOWCASE if s["id"] == "low_effort")])
    assert picked == {}   # an excluded edit never makes an example


def test_showcase_clips_never_take_a_test_clip_and_keep_a_stable_order():
    clips = [{"id": f"b__extra_L{lv}{j}", "kind": "single", "spectrum": "extra", "regime": "R1", "split": split, "levels": [lv]}
             for lv, j, split in ((1, "A", "train"), (3, "B", "val"), (3, "A", "train"), (2, "A", "test"))]
    clips.append({"id": "b__single_L3A", "kind": "single", "spectrum": None, "regime": "R1", "split": "train", "levels": [3]})
    assert [c["id"] for c in gallery.showcase_clips({"clips": clips}, "R1")] == ["b__extra_L3A", "b__extra_L3B", "b__extra_L1A"]


def test_showcase_takes_only_a_finding_matched_to_the_edit():
    spec = next(s for s in gallery.SHOWCASE if s["id"] == "disfluency")
    d7 = {"id": "d7-001", "dimension": "D7"}
    unmatched = {"flaws": [d7], "truth": [{"type": "BLOCK", "finding": None}]}
    matched = {"flaws": [d7], "truth": [{"type": "WORD_REPETITION", "finding": "d7-001"}]}
    picked = gallery.pick_showcase([({"id": "a"}, unmatched), ({"id": "b"}, matched)], [spec])
    assert picked["disfluency"][0]["id"] == "b"
    assert gallery.pick_showcase([({"id": "a"}, unmatched)], [spec]) == {}   # a D7 finding away from the edit is not shown
    assert gallery.pick_showcase([({"id": "c"}, {"flaws": [d7], "truth": []})], [spec]) == {}


def test_natural_rush_showcase_needs_the_label_on_the_matched_finding():
    spec = next(s for s in gallery.SHOWCASE if s["id"] == "natural_rush")
    rush = {"id": "d1-003", "dimension": "D1", "type": "RUSH", "pattern": "NATURAL_RUSH"}
    pause = {"id": "d2-006", "dimension": "D2", "type": "PAUSE_DROPPED", "pattern": None}
    # v11 'subtype': the label sat on a flag inside another edit, and the natural rush itself matched nothing.
    away = {"flaws": [rush, pause], "truth": [{"type": "NATURAL_RUSH", "finding": None}, {"type": "LOW_EFFORT", "finding": None}]}
    # v11 L3A: a time-stretch RUSH edit whose flag carries the label is not a natural-rush edit.
    other_edit = {"flaws": [rush], "truth": [{"type": "RUSH", "finding": "d1-003"}]}
    unlabelled = {"flaws": [pause], "truth": [{"type": "NATURAL_RUSH", "finding": "d2-006"}]}
    assert gallery.pick_showcase([({"id": c}, r) for c, r in (("a", away), ("b", other_edit), ("c", unlabelled))], [spec]) == {}
    own = {**rush, "type": "NATURAL_RUSH", "pattern": None}
    good = {"flaws": [pause, own], "truth": [{"type": "NATURAL_RUSH", "finding": "d1-003"}]}
    assert gallery.pick_showcase([({"id": "a"}, away), ({"id": "d"}, good)], [spec])["natural_rush"][0]["id"] == "d"
    assert gallery.shown(spec, good)[0]["id"] == "d1-003"   # the page opens on this finding, not on the larger pause penalty


def test_left_out_reason_names_the_edit_and_the_needed_finding():
    spec = next(s for s in gallery.SHOWCASE if s["id"] == "natural_rush")
    assert gallery.left_out_reason(spec) == ("no train or val clip has an injected natural rush edit that the evaluation matches "
                                             "to a finding labelled natural rushing")


def test_listed_example_opens_on_a_listed_entry_that_an_edit_links_to():
    res = {"differences": [{"id": "x1", "status": "difference"}, {"id": "x2", "status": "listed"}, {"id": "x3", "status": "listed"}],
           "truth": [{"difference": "x1"}, {"difference": "x3"}, {"difference": None}]}
    assert gallery.listed_focus(res) == "x3"
    assert gallery.listed_focus({**res, "truth": []}) == "x2"
    assert gallery.listed_focus({"differences": [], "truth": []}) is None


def test_listed_example_ranks_candidate_labels_then_listed_edits():
    def res(candidate, hits):
        listed = [{"id": f"x{i}", "status": "listed", "dimension": "D7", "candidate": candidate and i == 0} for i in range(2)]
        return {"flaws": [], "differences": listed, "truth": [{"difference": f"x{i}"} for i in range(hits)]}
    plain = {"flaws": [], "differences": [{"id": "x1", "status": "difference", "dimension": "D1"}], "truth": []}
    picked = gallery.pick_listed([({"id": "p"}, plain), ({"id": "a"}, res(False, 2)), ({"id": "b"}, res(True, 0)), ({"id": "c"}, res(True, 1))])
    assert picked[0]["id"] == "c"
    assert gallery.pick_listed([({"id": "p"}, plain)]) is None


def _reader(id_, role, split, initials=None, text="We are met on a great battlefield of that war."):
    return {"id": id_, "role": role, "split": split, "speaker": id_.upper(), "text": text, "licence_basis": "LibriVox",
            "licence_url": "https://archive.org/x", "source": {"file": f"lv_gettysburg150_{initials or id_.split('_')[1]}.mp3"}}


def _bank_manifest(extra=()):
    readers = [_reader(f"gettysburg_{i}", "reader_calibration", "calibration") for i in ("wt", "dl", "amb", "fb", "pc", "jn")]
    readers += [_reader(f"gettysburg_{i}", "reader_check", "check") for i in ("dj", "sa")]
    readers += [{"id": "greenman_reagan", "role": "orator_reference", "split": "train", "speaker": "John Greenman", "text": "x"},
                {"id": "null_project_lv_gettysburg150_amb", "role": "null_reader", "null_set": "select", "text": "y"}, *extra]
    pool = {"groups": [{"entries": [{"reader_id": "librivox:fb", "null_set": "lockbox"}, {"reader_id": "librivox:dl", "null_set": "fit"}]}]}
    return {"readers": readers, "r2_pool": pool, "clips": []}


def test_bank_takes_calibration_readers_only_in_a_fixed_order():
    m = _bank_manifest([_reader("gettysburg_tx", "reader_calibration", "test"),          # a test-split reading
                        _reader("gettysburg_dj2", "reader_calibration", "calibration", "dj")])   # a check reader's other take
    ids = [r["id"] for r in gallery.bank_readers(m)]
    # fb is in the R2 lockbox; dj, sa (check), tx (test), dj2 (a check reader's identity) and the null-pool rows never enter.
    assert ids == ["gettysburg_amb", "gettysburg_dl", "gettysburg_jn", "gettysburg_pc", "gettysburg_wt"]
    shuffled = {**m, "readers": list(reversed(m["readers"]))}
    assert [r["id"] for r in gallery.bank_readers(shuffled)] == ids


def test_bank_needs_five_readings_of_one_text():
    m = _bank_manifest()
    m["readers"] = [r for r in m["readers"] if r["id"] != "gettysburg_wt"]   # fb is in the lockbox: four remain
    with pytest.raises(ValueError, match="needs 5"):
        gallery.bank_readers(m)
    m = _bank_manifest()
    m["readers"][0] = {**m["readers"][0], "text": "Four score and seven years ago."}
    with pytest.raises(ValueError, match="one text"):
        gallery.bank_readers(m)


def test_bank_index_entry_names_readers_and_licence():
    bank = gallery.bank_readers(_bank_manifest())
    meta = gallery.bank_meta(bank)
    assert meta["id"] == gallery.BANK_ID and meta["audio"] == "audio/gettysburg_amb.wav" and meta["text"] == bank[0]["text"]
    assert [r["id"] for r in meta["references"]] == [r["id"] for r in bank]
    assert all(r["licence"] == "LibriVox public domain" and r["reader"] and r["audio"] == f"audio/{r['id']}.wav" for r in meta["references"])
    assert gallery.baseline_meta(bank[0])["title"] == "GETTYSBURG_AMB: Gettysburg Address (passage)"


def test_consensus_candidates_are_check_reader_clips_never_test():
    m = _bank_manifest()
    bank = gallery.bank_readers(m)

    def clip(id_, parent, split, kind="cross", level=3, baseline="gettysburg_amb"):
        return {"id": id_, "parent": parent, "split": split, "kind": kind, "regime": "R2", "baseline": baseline, "levels": [level]}
    m["clips"] = [clip("gettysburg_dj__x1_L2", "gettysburg_dj", "check", level=2), clip("gettysburg_sa__x2_L3", "gettysburg_sa", "check"),
                  clip("gettysburg_dj__x9_L3", "gettysburg_dj", "test"),                          # test split
                  clip("gettysburg_wt__extra_x1_L3", "gettysburg_wt", "calibration"),             # a bank reader
                  clip("gettysburg_dj__G5", "gettysburg_dj", "check", kind="cross_botched"),      # not a cross clip
                  clip("greenman_reagan__x3_L3", "greenman_reagan", "train", baseline="reagan_farewell_1989")]
    assert [c["id"] for c in gallery.consensus_clips(m, bank)] == ["gettysburg_sa__x2_L3", "gettysburg_dj__x1_L2"]


def test_consensus_example_uses_the_regime_that_the_pipeline_selects():
    det = {"regimes": {"R2": {"name": "single"}, "R2_consensus": {"name": "consensus"}}}
    refs = [recording(12) for _ in range(5)]
    _, mode_det = gallery.mode_detector(refs, det)
    assert mode_det["regimes"]["R2"]["name"] == "consensus" and det["regimes"]["R2"]["name"] == "single"
    B, mode_det = gallery.mode_detector(refs[:4], det)
    assert B is refs[0] and mode_det["regimes"]["R2"]["name"] == "single"
    picked = gallery.pick_showcase([({"id": "a"}, {"flaws": [{"id": "d2-001"}], "truth": [{"type": "PAUSE_INTRUSIVE", "finding": None}]}),
                                    ({"id": "b"}, {"flaws": [{"id": "d1-002"}], "truth": [{"type": "DRAG", "finding": "d1-002"}]})],
                                   [gallery.CONSENSUS_SHOWCASE])
    assert picked["r2_consensus"][0]["id"] == "b"


def test_consensus_result_gives_reference_times_on_the_exemplar_audio():
    # Slower readers move the median word times past the end of the exemplar (the first, fastest reading).
    refs = [recording(40, pauses={7: 0.7, 19: 0.8}, word_s=0.30 * f, gap_s=0.06 * f, seed=k) for k, f in enumerate((1.0, 1.1, 1.2, 1.3, 1.4))]
    you = recording(40, pauses={7: 0.05, 19: 1.6, 30: 0.9}, word_s=0.33, seed=9)
    single, consensus = regime("R2", 1.0), regime("R2", 1.0)
    single["reference_mode"], consensus["reference_mode"] = "single", "consensus5"
    det = make_detector({"R1": regime("R1"), "R2": single, "R2_consensus": consensus}, C.PMAX_START, {"calibrated": False})
    result = pipeline.analyze(you, you.tr, refs[0], regime="R2", detector=det, references=refs)
    exemplar, end = refs[0].al, result["baseline"]["duration"]
    assert result["detection"]["reference_mode"] == "consensus5"
    assert [w["b"] for w in result["words"]] == [[round(float(a), 3), round(float(b), 3)] for a, b in zip(exemplar.start, exemplar.end)]
    assert 0 <= min(result["map"]["b"]) and max(result["map"]["b"]) <= end
    spans = [x for x in result["flaws"] + result["differences"] if x["b"] is not None]
    assert any(x["dimension"] == "D2" for x in spans) and any(x["dimension"] != "D2" for x in spans)
    for x in spans:
        w0, w1 = x["words"]
        lo, hi = (exemplar.end[w0], exemplar.start[w1]) if x["dimension"] == "D2" else (exemplar.start[w0], exemplar.end[w1])
        assert lo - 1e-3 <= x["b"][0] <= x["b"][1] <= hi + 1e-3 <= end + 1e-3, x


def test_index_entries_of_the_build_match_the_shipped_index():
    """The entries that build writes (items, self_description, index_entry) are the shipped gallery/index.json entries: the
    SELF twin directly after its reference version, the two links, and a text exactly on the examples whose baseline the
    index does not carry. Showcase entries take their selection (title, description, focus) from the shipped entry."""
    import json
    g = pipeline.ROOT / "gallery"
    index = json.loads((g / "index.json").read_text())
    specs = {o["id"]: o for o in gallery.items()}
    assert [it["id"] for it in index["items"] if it["id"] in specs] == list(specs)
    single, bank = index["baselines"]
    bundled = {single["id"], *(r["id"] for r in bank["references"])}
    for it in index["items"]:
        res = json.loads((g / it["result"]).read_text())
        spec = specs.get(it["id"], it)
        if spec["regime"] == "SELF":
            spec = {**spec, "description": gallery.self_description(spec, {"flaws": [{"type": t["type"]} for t in res["truth"]]}, res)}
        assert gallery.index_entry(spec, res, it.get("text", "not bundled"), bundled) == it, it["id"]
    items = {it["id"]: it for it in index["items"]}
    assert items["L3A_self"]["text"] == single["text"] and items["L3A"]["self_version"] == "L3A_self"
    manifest = pipeline.ROOT / "build/work/kaggle_runs/last_run/x/data/dataset/manifest.json"
    if manifest.exists():
        baselines = {b["id"]: b for b in json.loads(manifest.read_text())["baselines"]}
        assert items["natural_rush"]["text"] == baselines[items["natural_rush"]["baseline"]]["text"]
