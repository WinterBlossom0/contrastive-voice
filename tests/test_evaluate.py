"""Evaluation sections and helpers (cvoice.evaluate), mostly on stubbed datasets; the full run is the slow integration test."""
import dataclasses
import json
import math
from types import SimpleNamespace

import numpy as np
import pytest
from synth import label, local, recording, regime, with_x

from cvoice import calibrate, config as C, dataset, evaluate, stress
from cvoice import evaluate as ev
from cvoice.compare import compare
from cvoice.detect import KEYS, Region, clip_flags, decode, save_detector
from cvoice.events import Run, run_pair
from cvoice.score import score
from cvoice.uncertainty import poisson



def fake_run(regions, clip=None):
    B = recording(40, pauses={7: 0.7, 19: 0.8})
    comp = compare(B, B)
    return Run(B, B, comp, regions, score(comp, [], regime("R1"), C.PMAX_START), "R1", clip or {})


def test_rate_rows_and_markdown_tables():
    assert ev.rate_row("x", 0, 10.0)[-1] == pytest.approx(0.3) and ev.rate_row("x", 2, 4.0)[3] == 0.5 and ev.rate_row("x", 2, 4.0)[-1] is None
    assert ev.md_table(["a", "b"], [[1, None], [0.12345, "z"]]).splitlines()[2:] == ["| 1 |  |", "| 0.123 | z |"]


def test_diff_regions_counts_added_and_removed_flags():
    ra = fake_run([Region("D1", -1, 5, 9, 5, 4.0, (5, 6, 7, 8, 9))])
    rb = fake_run([Region("D1", -1, 6, 10, 6, 4.0, (6, 7, 8, 9, 10)), Region("D5", -1, 20, 22, 20, 4.0, (20, 21, 22))])
    assert ev.diff_regions(ra, rb) == (["D5-"], 0) and ev.diff_regions(rb, ra) == ([], 1)


def test_diff_regions_counts_whole_clip_flags_by_dimension_and_direction():
    a = fake_run([])
    b = fake_run([], {"D1": math.log(1.4)})
    assert ev.diff_regions(a, b) == (["D1+ whole clip"], 0) and ev.diff_regions(b, a) == ([], 1)
    assert ev.diff_regions(b, fake_run([], {"D1": math.log(1.6)})) == ([], 0)  # still flagged, same dimension
    assert ev.diff_regions(b, fake_run([], {"D3": -math.log(3.0)})) == (["D3- whole clip"], 1)


def test_null_flags_list_local_regions_then_whole_clip_flags(base):
    comp = with_x(base, "D5", [(10, 15, -6)])
    comp.dims["D1"].g = math.log(1.5)
    comp.dims["D3"].g = math.log(3.0)  # wider than the reference: never a flag
    null = calibrate.Null("a>b", comp, base.tr.sentence, 1.0)
    assert ev.null_flags(null, regime("R2", 2.0)) == ["D5-", "D1+ whole clip"]
    assert ev.null_flags(null, regime("R2", dict.fromkeys(KEYS), clip={"D1": None, "D3": None})) == []


def test_random_baseline_draws_every_start_position_and_events_stay_on_boundaries():
    n, w = 15, 5
    tr = [{"dim": "D1", "sign": -1, "words": [0, w - 1]}, {"dim": "D2", "sign": -1, "words": [3, 4]}]
    starts, bounds = set(), set()
    for seed in range(400):
        a, b = ev._random_regions(tr, n, np.random.default_rng(seed))
        starts.add(a.i0)
        bounds.add(b.i0)
    assert starts == set(range(n - w + 1)) and bounds == set(range(n - 1))  # the last start (10) is reachable; a boundary never exceeds n - 2


def test_disabled_regime_is_not_reported_as_a_clean_null():
    row = ev.regime_rate_row("R2 held-out", regime("R2", dict.fromkeys(KEYS), enabled=["D1"]), 0, 9.0)
    assert row[1] == "flags disabled" and row[3] is None and row[4] is None
    assert ev.regime_rate_row("R2 held-out", regime("R2", {"D1+": 2.0}, enabled=["D1"]), 0, 9.0)[4] == pytest.approx(3 / 9.0, abs=1e-3)  # one direction is enough


def test_test_split_needs_final_and_a_final_run_is_recorded_once_per_config(tmp_path, pinned_detector):
    with pytest.raises(ValueError, match="--final"):
        ev.run(tmp_path, tmp_path / "detector.json", None, tmp_path, splits=("train", "test"))
    det = pinned_detector(2.0)
    models = tmp_path / "models" / "detector.json"
    models.parent.mkdir()
    from cvoice.detect import save_detector
    manifest = tmp_path / "manifest.json"
    manifest.write_text("{}")
    det["report"]["manifest_sha256"] = dataset.sha256_file(manifest)
    save_detector(det, models)
    ev.final_gate(models, det, ("train", "val", "test"), "cpu", force=False, manifest=manifest)
    log = models.parent / ev.FINAL_LOG
    assert det["config_sha256"] in json.loads(log.read_text())
    with pytest.raises(RuntimeError, match="already evaluated"):
        ev.final_gate(models, det, ("train", "val", "test"), "cpu", force=False, manifest=manifest)
    ev.final_gate(models, det, ("train", "val", "test"), "cpu", force=True, manifest=manifest)
    assert json.loads(log.read_text())[det["config_sha256"]]["runs"] == 2
    assert ev.split_groups(("train", "val")) == [("train", ("train",)), ("val", ("val",))]  # train is never pooled with held-out
    assert ev.split_groups(("train", "val", "test"))[-1] == ("val+test", ("val", "test")) and ev.held_out(("train", "val")) == ("val",)


class CrossStub:
    """Just enough of Dataset for cross_section: one cross clip (a RUSH L3 edit of reader P0) against the reference B."""

    def __init__(self, recs, P, lab):
        self.recs_by_id, self.P, self.lab = recs, P, lab
        self.clip = {"id": "p0__x1_L3", "split": "check", "baseline": "B", "parent": "P0", "regime": "R2"}
        self.manifest = {"readers": [{"id": "B", "role": "reader_calibration"}]}  # the one calibration reader every check clip is paired with

    def clips(self, **where):
        return [self.clip]

    def load(self, entries=(), clips=()):
        pass

    def any_entry(self, id_):
        return {"id": id_}

    def entry(self, kind, id_):
        return {"id": id_}

    def parent_entry(self, clip):
        return {"id": clip["parent"]}

    def recs(self, entries):
        return [self.recs_by_id[e["id"]] for e in entries]

    def rec(self, entry):
        return self.recs_by_id[entry["id"]]

    def clip_recs(self, clips):
        return [self.P]

    def labels(self, clip):
        return self.lab


def test_cross_section_counts_new_flags_by_word_index_and_summarises_per_reader_group(pinned_detector, monkeypatch):
    from cvoice import flaws
    monkeypatch.setattr(ev, "r2_curve", lambda *a: {})  # the operating curve needs the reader clips; the slow integration test runs it
    from cvoice.align import Alignment
    from cvoice.features import make_recording
    B = recording(70, pauses={7: 0.7, 19: 0.8, 30: 0.6, 45: 0.7})
    y, lab = flaws.inject(B, flaws.Plan([flaws.make_edit(B, "RUSH", 3, (20, 26))]), "c", "p", recipe="t", seed=1)
    P = make_recording(y, B.tr, Alignment(np.array(lab["words"]["start"]) / C.SR, np.array(lab["words"]["end"]) / C.SR, B.al.compat, 0.9))
    res = ev.cross_section(CrossStub({"B": B, "P0": B}, P, lab), pinned_detector(2.0), ("train", "val"))
    assert set(res["summary"]) == {"check"} and res["summary"]["check"]["truth"] == 1
    assert res["summary"]["check"]["new"] >= 1 and res["summary"]["check"]["pre_existing"] == 0  # the clean clip has no flag to match
    assert res["summary"]["check"]["detected"] == 1 and "reader group" in res["table"]
    # the same flags exist in the clean clip when it is the edited clip itself: they are pre-existing, whatever the time axes
    res2 = ev.cross_section(CrossStub({"B": B, "P0": P}, P, lab), pinned_detector(2.0), ("train", "val"))
    assert res2["summary"]["check"]["new"] == 0 and res2["summary"]["check"]["pre_existing"] >= 1


def test_cross_pause_direction_uses_boundary_not_word_starts(base, pinned_detector):
    clean = run_pair(base, base, pinned_detector(), "R2")
    raw = base.sil_raw.copy()
    raw[10] += .6
    edited = run_pair(base, dataclasses.replace(base, sil_raw=raw), pinned_detector(), "R2")
    truth = {"type": "PAUSE_INTRUSIVE", "dim": "D2", "words": [10, 11]}
    d = evaluate.edit_direction(clean, edited, truth)
    assert d["x_clean"] == 0 and d["x_edited"] == pytest.approx(.6) and d["direction"] == "away from the reference"
    assert evaluate.edit_direction(edited, clean, truth)["direction"] == "toward the reference (repair control)"


def test_freeze_checks_manifest_even_when_forced_and_records_all_hashes(tmp_path, pinned_detector, monkeypatch):
    manifest = tmp_path / "manifest.json"
    manifest.write_text("{}")
    models = tmp_path / "detector.json"
    project = tmp_path / "project_sha256.txt"
    project.write_text("source ledger")
    monkeypatch.setattr(evaluate, "ROOT", tmp_path)
    det = pinned_detector()
    det["report"]["manifest_sha256"] = dataset.sha256_file(manifest)
    save_detector(det, models)
    evaluate.final_gate(models, det, ("test",), "cpu", False, manifest)
    row = json.loads((tmp_path / evaluate.FINAL_LOG).read_text())[det["config_sha256"]]
    assert row["detector_sha256"] == dataset.sha256_file(models) and row["project_sha256"] == dataset.sha256_file(project)
    assert row["manifest_sha256"] == dataset.sha256_file(manifest)
    manifest.write_text('{"changed": true}')
    with pytest.raises(RuntimeError, match="manifest hash"):
        evaluate.final_gate(models, det, ("test",), "cpu", True, manifest)


def test_evaluate_cli_exits_nonzero_after_written_errors(monkeypatch, tmp_path):
    class Pool:
        def __init__(self, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass
    monkeypatch.setattr(evaluate, "PreparePool", Pool)
    def run(*args):
        (tmp_path / "results.json").write_text('{"errors":{"example":"failed"}}')
        return {"errors": {"example": "failed"}}
    monkeypatch.setattr(evaluate, "run", run)
    with pytest.raises(SystemExit) as e:
        evaluate.main(["--out", str(tmp_path)])
    assert e.value.code == 1 and (tmp_path / "results.json").exists()


def test_chain_a_and_b_render_identical_plans(base, monkeypatch):
    from cvoice import flaws
    def injected(rec, plan, *args, **kw):
        return [(e.type, e.level, e.words, e.a, e.b, e.param) for e in plan.edits]
    monkeypatch.setattr(flaws, "inject", injected)
    for lv in (2, 3):
        assert evaluate.chain_b_clip(base, "s", "RUSH", lv) == evaluate.directional_clip(base, "s", "RUSH", lv)


def test_validity_includes_emphasis_and_spectral_proxy(base, pinned_detector, monkeypatch):
    run = run_pair(base, base, pinned_detector(), "R1")
    lab = label(base, "MUMBLE", (10, 15))
    lab["flaws"] += label(base, "DEEMPHASIS", (12, 12))["flaws"]
    for f in lab["flaws"]:
        f.update(parent_span=f["span"], realised={"value": -.2})
    run.comp.dims["D4"].x[12] = -.2
    class DS:
        def clips(self, **kw): return [{"split": "val"}]
    monkeypatch.setattr(evaluate, "clip_runs", lambda *a: [({"split": "val"}, run, lab)])
    res = evaluate.validity_section(DS(), pinned_detector(), ("val",))
    assert {r[1] for r in res["rows"] if r[3]} == {"MUMBLE", "DEEMPHASIS"}
    assert "recipe setting" in res["table"] and "median of paired ratios" in res["table"]


def test_repair_falls_back_to_l3_fade_and_keeps_failed_attempts(base, pinned_detector, monkeypatch):
    run = run_pair(base, base, pinned_detector(), "R1")
    run.regions = [local("D5", 10, 15)]
    l2 = {"id": "s__single_L2A", "split": "val", "parent": "s", "types": ["FADE"], "level": 2}
    l3 = {**l2, "id": "s__single_L3A", "level": 3}
    class DS:
        pool = None
        def clips(self, **kw): return [l2] if kw["level"] == 2 else [l3]
        def prepare_many(self, items): return [base for _ in items]
    def runs(ds, det, clips):
        return [(c, dataclasses.replace(run, regions=[] if c["level"] == 2 else run.regions), label(base)) for c in clips]
    monkeypatch.setattr(evaluate, "clip_runs", runs)
    monkeypatch.setattr(evaluate, "repair_audio", lambda *args: None)
    res = evaluate.repair_section(DS(), pinned_detector(), ("val",))
    assert res["by_type"]["val"]["FADE"]["n"] == 1 and res["rows"][0]["clip"] == l3["id"]
    assert len(res["rows"][0]["attempts"]) == 2 and all(a["error"] for a in res["rows"][0]["attempts"])
    assert "score before" in res["table"] and "new flags" in res["table"]


def test_null_rates_state_dependence_and_reader_counts(base, pinned_detector, monkeypatch):
    class DS:
        def entry(self, *args): return {"paired_baseline": "s"}
        def recs(self, entries): return [base] * len(entries)
    comp = compare(base, base)
    monkeypatch.setattr(evaluate, "reader_ids", lambda ds, role: ["a", "b"] if role == "reader_calibration" else ["c"])
    monkeypatch.setattr(evaluate, "r1_nulls", lambda *args: [calibrate.Null("s__identity", comp, base.tr.sentence, 1, "val")])
    monkeypatch.setattr(evaluate, "r2_nulls", lambda *args: [calibrate.Null("a>c", comp, base.tr.sentence, 1), calibrate.Null("b>c", comp, base.tr.sentence, 1)])
    out = evaluate.null_section(DS(), pinned_detector(), ("val",))
    assert "observed per comparison-minute" in out["table"] and "R1 unique recordings only" in out["table"]
    assert out["detail"]["R2 check readers"]["unique_recordings"] == 3
    assert "R2 check-reader pairs, not fitted but seen during the detector redesign" in out["table"]
    assert out["detail"]["R2 check readers"]["reader_counts"][0]["comparisons"] == 2


def test_r2_operating_curve_marks_each_flag_keys_own_threshold(base, pinned_detector, monkeypatch):
    det = pinned_detector()
    det["regimes"]["R2"]["h"]["D2+"] = 2.35
    n = calibrate.Null("a>c", compare(base, base), base.tr.sentence, 1)
    monkeypatch.setattr(evaluate, "reader_ids", lambda *args: [])
    monkeypatch.setattr(evaluate, "r2_nulls", lambda *args: [n])
    out = evaluate.r2_curve(None, det, [])
    fitted = [r for r in out["rows"] if r["fitted"] and r["key"] == "D2+"]
    assert len(fitted) == 1 and fitted[0]["h"] == 2.35 and fitted[0]["reader_counts"] == {"c": 0}
    assert fitted[0]["threshold"] == pytest.approx(2.35 * C.FLOORS["D2"])
    assert [r["h"] for r in out["rows"] if r["fitted"] and r["key"] == "D2-"] == [2.0]  # the other direction has its own marked threshold
    assert {r["key"] for r in out["rows"]} == {k for k in KEYS if k[:2] in C.REGIME_DIMS["R2"]}


def test_directional_violation_cause_identifies_labelled_pause_failure(base, pinned_detector, monkeypatch):
    from types import SimpleNamespace
    entry = {"id": "s", "split": "val"}
    class DS:
        manifest = {"baselines": [entry]}
        pool = None
        def load(self, **kw): pass
        def recs(self, entries): return [base]
        def transcript(self, entry): return base.tr
        def prepare_many(self, items): return [w for w, tr in items]
    def clip(rec, bid, typ, lv):
        f = {"dimension": C.FLAW_DIM[typ], "words": [10, 11], "realised": {"value": .6}}
        return np.array([lv, C.FLAW_TYPES.index(typ)]), {"flaws": [f]}
    def pair(B, P, det, regime):
        lv, ix = P
        comp = compare(base, base)
        comp.dims["D2"].x[10] = np.nan if lv == 2 else .6
        value = {1: 90, 2: 100, 3: 70}[lv] if C.FLAW_TYPES[ix] == "PAUSE_INTRUSIVE" else 100 - lv * 10
        return SimpleNamespace(comp=comp, regions=[], clip={}, scored=SimpleNamespace(S=dict.fromkeys(C.DIMS, value)))
    monkeypatch.setattr(evaluate, "directional_clip", clip)
    monkeypatch.setattr(evaluate, "run_pair", pair)
    out = evaluate.directional_section(DS(), pinned_detector(), ("val",))
    assert len(out["violations"]) == 1 and out["violations"][0]["cause"] == "pause not measured at the labelled boundary"
    assert "cause" in out["table"]


@pytest.mark.parametrize("empty", [True, False])
def test_directional_handles_unrealised_edits_and_final_word_hesitation(base, pinned_detector, monkeypatch, empty):
    entry = {"id": "s", "split": "val"}
    class DS:
        manifest = {"baselines": [entry]}
        pool = None
        def load(self, **kw): pass
        def recs(self, entries): return [base]
        def transcript(self, entry): return base.tr
        def prepare_many(self, items): return [base for _ in items]
    def clip(*args):
        f = {"dimension": "D2", "words": [len(base.tr) - 1], "realised": {"value": .3}}
        return base.wav, {"flaws": [] if empty else [f]}
    monkeypatch.setattr(C, "FLAW_TYPES", ("HESITATION",))
    monkeypatch.setattr(evaluate, "directional_clip", clip)
    out = evaluate.directional_section(DS(), pinned_detector(), ("val",))
    assert out["cells"] == (0 if empty else 1)
    assert len(out["skipped"]) == (3 if empty else 0)
    assert not out["violations"]


def _flag_runs(base, pinned_detector, before, after):
    reg = pinned_detector(h=1)["regimes"]["R2"]
    return [Run(base, base, c, decode(c, reg, base.tr.sentence), score(c, [], reg, C.PMAX_START), "R2", {})
            for c in (with_x(base, "D5", before), with_x(base, "D5", after))]


@pytest.mark.parametrize("after, flagged", [([(10, 10, -20), (11, 14, -12)], False),  # the flag was there before the edit and did not grow
                                            ([(10, 10, -20), (11, 14, -30)], True)])  # the region grew stronger over the edited words
def test_cross_section_counts_only_a_new_or_worsened_flag_on_an_edited_word_as_flagged(base, pinned_detector, monkeypatch, after, flagged):
    before = [(10, 10, -20), (11, 14, -12)]
    old, edited = _flag_runs(base, pinned_detector, before, after)
    assert old.regions and edited.regions
    P0, P1 = base, dataclasses.replace(base)
    stub = CrossStub({"B": base, "P0": P0}, P1, label(base, words=(11, 13)))
    monkeypatch.setattr(evaluate, "stored_pair", lambda ds, B, P, *args: edited if P is P1 else old)
    monkeypatch.setattr(evaluate, "r2_curve", lambda *args: {})
    res = evaluate.cross_section(stub, pinned_detector(h=1), ("val", "test"))
    assert res["edits"][0]["flagged"] is flagged and res["edits"][0]["difference_rank"] is None
    assert res["edits"][0]["reference"] == "B" and res["edits"][0]["level"] == 2
    assert res["summary"]["check"]["flagged_or_listed"] == int(flagged)
    assert [r[:6] for r in res["by_type"]] == ([["check", "FADE", 2, res["summary"]["check"]["detected"], 1, 1]] if flagged else [])  # an edit that did not grow is no away-edit


@pytest.fixture
def stress_world(base, pinned_detector, monkeypatch):
    entries = [{"id": sp, "split": sp} for sp in ("val", "test")]
    donors = [*entries, {'id': 'donor', 'split': 'val'}]
    clips = [{"id": sp + "__single", "parent": sp, "split": sp, "level": 2, "types": ["FADE"]} for sp in ("val", "test")]
    refs = [run_pair(base, base, pinned_detector(), "R1") for _ in entries]
    refs[0].regions = [local("D5", 10, 15)]
    class DS:
        manifest = {"baselines": donors}
        pool = None
        def clips(self, **kw):
            return [{"id": kw["parent"] + "__identity"}] if kw.get("kind") == "identity" else clips
        def load(self, **kw): pass
        def recs(self, entries): return [base] * len(entries)
        def clip_recs(self, clips): return [base] * len(clips)
        def entry(self, *args): return {}
        def prepare_many(self, items): return [base] * len(items)
    monkeypatch.setattr(evaluate, "reader_ids", lambda ds, role: ["cal"] if role == "reader_calibration" else ["check"])
    monkeypatch.setattr(evaluate, "stored_pair", lambda *args: run_pair(base, base, pinned_detector(), "R1"))
    monkeypatch.setattr(evaluate, "clip_runs", lambda ds, det, selected: [(c, refs[clips.index(c)], label(base)) for c in selected])
    monkeypatch.setattr(stress, "MATRIX", [("white noise 20 dB SNR", stress.noise)])
    monkeypatch.setattr(stress, 'RANDOM_SEEDS', (1,))
    monkeypatch.setattr(stress, "apply", lambda fn, w, seed: w)
    monkeypatch.setattr(stress, "world_speaker", lambda w, seed: w)
    return DS(), clips, refs


def test_final_summaries_keep_val_and_test_and_their_aggregate(stress_world, pinned_detector, monkeypatch):
    ds, clips, refs = stress_world
    det = pinned_detector()
    trivial = evaluate.trivial_section(ds, det, ("train", "val", "test"))
    assert list(trivial["totals"]) == ["val", "test", "val+test"]
    assert [trivial["totals"][sp]["detector"][0] for sp in trivial["totals"]] == [1, 0, 1]
    stress = evaluate.stress_section(ds, det, ("train", "val", "test"))
    flawed = [r for r in stress["rows"] if r['regime'] == 'R1' and r['split'] != 'check readers' and r['condition'].startswith('white noise')]
    assert [(r["split"], r["flaws_found_before"]) for r in flawed] == [("val", 1), ("test", 0), ("val+test", 1)]
    refs[1].regions = refs[0].regions
    monkeypatch.setattr(evaluate, "repair_audio", lambda *args: None)
    repair = evaluate.repair_section(ds, det, ("train", "val", "test"))
    assert [repair["by_type"][sp]["FADE"]["n"] for sp in repair["by_type"]] == [1, 1, 2]
    for res in (trivial, stress, repair):
        assert "val+test" in res["table"] and "| val |" in res["table"] and "| test |" in res["table"]
        assert "| train |" not in res["table"]


@pytest.mark.parametrize("before, after, expected", [(100, None, None), (None, None, None), (None, float("nan"), None), (0, 10, 10)])
def test_stress_score_change_requires_two_finite_scores(stress_world, base, pinned_detector, monkeypatch, before, after, expected):
    ds, _, refs = stress_world
    for ref in refs:
        ref.scored.overall = before
    ref = run_pair(base, base, pinned_detector(), "R1")
    ref.scored.overall = before
    new = dataclasses.replace(ref, scored=dataclasses.replace(ref.scored, overall=after))
    monkeypatch.setattr(evaluate, "stored_pair", lambda *args: ref)
    monkeypatch.setattr(evaluate, "run_pair", lambda *args: new)
    res = evaluate.stress_section(ds, pinned_detector(), ("val", "test"))
    rows = [r for r in res["rows"] if r["split"] == "val+test" and r["condition"].startswith("white noise")]
    assert len(rows) == 1
    assert all(r["max_abs_delta_score"] == expected and r["missing_score_pairs"] == (2 if expected is None else 0)
               and r["measurable_score_pairs"] == (0 if expected is None else 2) for r in rows)
    assert all(r["abs_score_change"] == expected for r in res["flawed_clips"])
    reader = next(r for r in res["rows"] if r["split"] == "check readers" and r["condition"].startswith("white noise"))
    assert reader["max_abs_delta_score"] == expected and reader["missing_score_pairs"] == int(expected is None)


def test_validity_measures_window_centres_inside_the_edit_span_including_its_edges(base, pinned_detector, monkeypatch):
    run = run_pair(base, base, pinned_detector(), "R1")
    run.comp.dims["D5"].x[10:16] = [-1, -2, -8, -8, -3, np.nan]
    lab = label(base)
    lab["flaws"][0]["parent_span"] = lab["flaws"][0]["span"]
    class DS:
        def clips(self, **kw): return [{"split": "val"}]
    monkeypatch.setattr(evaluate, "clip_runs", lambda *args: [({"split": "val"}, run, lab)])
    res = evaluate.validity_section(DS(), pinned_detector(), ("val",))
    assert res["detail"][0]["detector_measurement"] == -3
    assert "window centres inside the span" in res["table"]


@pytest.mark.parametrize("ratios", [(1.251, 1.249), (1.251, 1 / 1.251)])
def test_device_agreement_flags_include_whole_clip_presence_and_direction(base, pinned_detector, monkeypatch, ratios):
    class Pool:
        def __init__(self, **kw): self.device = kw["devices"][0]
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def map(self, jobs): return [self.device] * len(jobs)
    class DS:
        pool = SimpleNamespace(device_class="cuda", devices=["cuda:0"])
        def clips(self, **kw): return [{"id": sp, "parent": "b", "split": sp} for sp in ("val", "test")]
        def entry(self, *args): return {}
        def wav(self, c): return base.wav
        def transcript(self, c): return base.tr
        def clip_transcript(self, c): return base.tr
    # Preserve the planted alignment on both devices, but place the overall tempo either side of its whole-clip threshold (ln 1.25 in R1).
    monkeypatch.setattr(evaluate, "PreparePool", Pool)
    monkeypatch.setattr(evaluate, "make_job", lambda *args: None)
    gpu, cpu = [SimpleNamespace(al=base.al, device=d) for d in ("cuda:0", "cpu")]
    monkeypatch.setattr(Pool, "map", lambda self, jobs: [gpu if self.device == "cuda:0" else cpu] * len(jobs))
    def pair(B, P, det, regime):
        comp = compare(base, base)
        comp.dims["D1"].g = math.log(ratios[P.device == "cpu"])
        reg = det["regimes"][regime]
        return Run(base, base, comp, [], score(comp, [], reg, C.PMAX_START), regime, clip_flags(comp, reg))
    monkeypatch.setattr(evaluate, "run_pair", pair)
    res = evaluate.device_section(DS(), pinned_detector(), ("val", "test"))
    assert [(r["split"], r["clips"]) for r in res["rows"]] == [("val", 1), ("test", 1), ("val+test", 2)]
    assert all(r["flags_identical"] is False for r in res["rows"])


def test_sample_counts_come_from_evaluated_labels(base, pinned_detector, monkeypatch, tmp_path):
    clips = [{"id": f"{sp}{i}", "parent": f"{sp}{i}", "split": sp} for sp, n in (("train", 5), ("val", 2), ("test", 1)) for i in range(n)]
    class DS:
        root = tmp_path
        def clips(self, **kw): return clips
        def labels(self, c): return label(base)
    monkeypatch.setattr(evaluate, "load_dataset", lambda *args: DS())
    monkeypatch.setattr(evaluate, "load_detector", lambda *args: pinned_detector())
    monkeypatch.setattr(evaluate, "warm", lambda *args: None)
    monkeypatch.setattr(evaluate, "final_gate", lambda *args: None)
    monkeypatch.setattr(evaluate, "figures", lambda *args: [])
    monkeypatch.setattr(evaluate, "SECTIONS", [])
    res = evaluate.run(tmp_path, tmp_path / "detector.json", None, tmp_path, ("train", "val"), final=True)
    assert [res["n"][sp]["trials_per_type_level"]["FADE"]["2"] for sp in res["n"]] == [5, 2, 1, 3]
    assert res["n"]["train"]["trials_per_type_level"]["RUSH"]["2"] == 0
    assert "| train | 5 | 5 | FADE | 2 | 5 |" in (tmp_path / "eval" / "tables.md").read_text()


class BotchedStub:
    """Dataset stand-in for cross_pairs / botched_section: calibration readers cal1, cal2, check reader chk, an orator reference gm
    (paired to baseline ref0); every botched clip is `P1`."""
    pool = None
    manifest = {"readers": [{"id": "cal1", "role": "reader_calibration"}, {"id": "cal2", "role": "reader_calibration"},
                            {"id": "chk", "role": "reader_check"}]}
    _clips = [{"id": "chk__G5", "split": "check", "baseline": "B", "parent": "chk"},
              {"id": "gm__G5", "split": "train", "baseline": "ref0", "parent": "gm"}]

    def __init__(self, base, P1, prepared=None):
        self.recs_by_id = {k: base for k in ("cal1", "cal2", "chk", "gm", "ref0")}
        self.P1, self.prepared, self.base = P1, prepared, base

    def clips(self, **kw):
        assert kw == {"kind": "cross_botched"}
        return self._clips

    def entry(self, kind, id_): return {"id": id_}
    def any_entry(self, id_): return {"id": id_}
    def parent_entry(self, clip): return {"id": clip["parent"]}
    def load(self, **kw): pass
    def recs(self, entries): return [self.recs_by_id[e["id"]] for e in entries]
    def rec(self, entry): return self.recs_by_id[entry["id"]]
    def clip_recs(self, clips): return [self.P1 for _ in clips]
    def labels(self, clip): return label(self.base)
    def prepare_many(self, items): return [self.prepared(w) for w, _ in items]


def test_cross_pairs_pair_a_check_clip_with_every_calibration_reader_and_any_other_clip_with_its_baseline(base, pinned_detector):
    P1 = dataclasses.replace(base, win_T=base.win_T * 0.5)
    pairs = evaluate.cross_pairs(BotchedStub(base, P1), pinned_detector(), BotchedStub._clips)
    assert [(c["id"], ref) for c, ref, *_ in pairs] == [("chk__G5", "cal1"), ("chk__G5", "cal2"), ("gm__G5", "ref0")]
    for _, _, edited, unedited, lab in pairs:
        assert edited.P is P1 and unedited.P is base and edited.B is base and lab["flaws"][0]["type"] == "FADE" and edited.regime == unedited.regime == "R2"


def test_botched_section_compares_each_botched_clip_with_its_references_beside_the_unedited_pair(base, pinned_detector, monkeypatch):
    P1 = dataclasses.replace(base, win_T=base.win_T * 0.5, win_R=0.1 * base.win_R)  # botched: whole passage fast and flat
    monkeypatch.setattr(evaluate, "map_calls", lambda fn, calls, pool: [None] * len(calls))
    out = evaluate.botched_section(BotchedStub(base, P1, lambda w: base), pinned_detector(), ("val",))
    assert [(r["clip"], r["reference"]) for r in out["rows"]] == [("chk__G5", "cal1"), ("chk__G5", "cal2"), ("gm__G5", "ref0")]  # check readers meet every calibration reader
    for r in out["rows"]:
        assert r["clean_score"] == 100.0 and r["clean_flags"] == [] and r["botched_score"] < 100 and r["whole_clip"] == ["D1- whole clip", "D3- whole clip"]
        assert {"D1- whole clip", "D3- whole clip"} <= set(r["botched_flags"]) and all(k == "D9-" or "whole clip" in k for k in r["botched_flags"])
    assert out["summary"]["check"] == {"pairs": 2, "tempo_flagged": 2, "range_flagged": 2, "median_clean_score": 100.0,
                                       "median_botched_score": out["rows"][0]["botched_score"], "max_botched_score": out["rows"][0]["botched_score"]}
    assert out["summary"]["train"]["pairs"] == 1 and "overall tempo flagged" in out["table"] and "chk__G5" in out["table"]


def test_botched_section_graded_rungs_raise_the_whole_clip_flag_of_the_edited_dimension(base, pinned_detector, monkeypatch):
    seen = []
    monkeypatch.setattr(evaluate, "map_calls", lambda fn, calls, pool: [seen.append(c[1:]) or f"{c[2]}{c[3]}" for c in calls])  # stand-in wavs
    def prepared(w):  # only the level-3 edits are strong enough to cross the whole-clip thresholds
        return dataclasses.replace(base, win_T=base.win_T * 0.5) if w == "RUSH3" else dataclasses.replace(base, win_R=0.1 * base.win_R) if w == "MONOTONE3" else base
    out = evaluate.botched_section(BotchedStub(base, base, prepared), pinned_detector(), ("val",))
    assert seen == [("chk", t, lv) for t in ("RUSH", "MONOTONE") for lv in (1, 2, 3)] and len(out["graded"]) == 6 * 2  # check reader x type x level x calibration reader
    rush3 = [g for g in out["graded"] if (g["type"], g["level"]) == ("RUSH", 3)]
    assert len(rush3) == 2 and all(g["flagged"] and "D1- whole clip" in g["flags"] for g in rush3)
    assert not any(g["flagged"] for g in out["graded"] if (g["type"], g["level"]) not in (("RUSH", 3), ("MONOTONE", 3)))
    assert [(r[0], r[1], r[3], r[4]) for r in out["ladder"]] == [("unedited", "", 0, 2)] + [(f"whole-passage {t}", lv, int(lv == 3) * 2, 2) for t in ("RUSH", "MONOTONE") for lv in (1, 2, 3)] + [("botched (G5)", "", 0, 2)]
    assert all(r[5] < 100 for r in out["ladder"][3:4] + out["ladder"][6:7]) and "whole-clip flag raised" in out["table"]


def test_ladder_section_scores_each_rung_per_split_and_counts_gate_violations(pinned_detector, monkeypatch):
    spec = [("identity", "identity", None, None, 99.0), ("single", None, 1, "four", 80.0), ("ladder", "G1", None, None, 95.0),
            ("ladder", "G3", None, None, 97.0), ("ladder", "G5", None, None, 60.0)]
    clips = [{"id": f"s__{i}", "kind": k, "recipe": rc, "level": lv, "parent": "s", "split": "val"} for i, (k, rc, lv, _, _) in enumerate(spec)]
    clips.append({"id": "t__identity", "kind": "identity", "parent": "t", "split": "test"})  # a split that is not evaluated
    scores = {c["id"]: sc for c, (*_, sc) in zip(clips, spec)}
    ds = SimpleNamespace(manifest={"clips": clips})
    monkeypatch.setattr(evaluate, "clip_runs", lambda ds_, det, cl: [(c, SimpleNamespace(scored=SimpleNamespace(overall=scores[c["id"]])), None) for c in cl])
    out = evaluate.ladder_section(ds, pinned_detector(), ("val",))
    assert [(r[0], r[1], r[2], r[4]) for r in out["rows"]] == [("val", "identity", 1, 99.0), ("val", "G1", 1, 95.0), ("val", "level 1 (four edits)", 1, 80.0),
                                                               ("val", "G3", 1, 97.0), ("val", "G5", 1, 60.0)]
    assert out["gates"] == [["val", 1, 1, 1, 1]]  # identity below 100, a level-1 clip below 90, G5 above 50, G1 < G3
    assert "Score gates" in out["table"]


def test_headline_strict_accounting_counts_each_whole_clip_flag_on_a_single_level_clip_as_a_false_positive(base, pinned_detector, monkeypatch):
    clip = {"id": "c", "split": "val", "level": 2, "parent": "s", "kind": "single"}
    run = Run(base, base, compare(base, base), [], score(compare(base, base), [], regime("R1"), C.PMAX_START), "R1", {"D1": math.log(1.4)})
    monkeypatch.setattr(evaluate, "clip_runs", lambda ds, det, cl: [(c, run, label(base)) for c in cl])
    out = evaluate.headline_section(SimpleNamespace(clips=lambda **kw: [clip]), pinned_detector(), ("val",))
    whole = [r for r in out["by_split_strict"] if r["group"] == "whole clip" and r["levels"].startswith("headline")]
    assert [(r["split"], r["tp"], r["fp"]) for r in whole] == [("val", 0, 1)]
    assert not any(r["group"] == "whole clip" for r in out["by_split"])  # the exempt accounting does not carry it


def test_headline_core8_all_and_pending_families(base, pinned_detector, monkeypatch):
    clips = [{"id": t, "split": "val", "level": 2, "parent": "s", "kind": "single", "spectrum": spectrum}
             for t, spectrum in (("FADE", "core8"), ("LOW_EFFORT", "extra"), ("WORD_REPETITION", "extra"), ("RISING_ENDING", "extra"), ("REPEATED_CONTOUR", "extra"))]
    run = Run(base, base, compare(base, base), [], score(compare(base, base), [], regime("R1"), C.PMAX_START), "R1", {})
    monkeypatch.setattr(evaluate, "clip_runs", lambda ds, det, cl: [(c, run, label(base, typ=c["id"])) for c in cl])
    out = evaluate.headline_section(SimpleNamespace(clips=lambda **kw: clips), pinned_detector(), ("val",))
    assert set(out["groups"]) == {"core8", "lab_passed", "synthetic_only"}
    def total(name):
        return next(r for r in out["groups"][name]["by_split_strict"] if r["group"] == "all" and r["levels"].startswith("headline"))
    assert total("core8")["fn"] == 1 and total("synthetic_only")["fn"] == 3
    assert {r["type"] for r in out["no_detector"]} == {"REPEATED_CONTOUR"}
    assert all(r["count"] == 1 and r["status"] == "no detector" for r in out["no_detector"])
    assert 'synthetic_only' in out['table_f1'] and 'unvalidated' in out['table_f1']
    assert out["groups"]["synthetic_only"]["overlap"][0]["truths"] == 3


def test_cross_direction_handles_pending_family_and_new_primary(base, pinned_detector):
    run = run_pair(base, base, pinned_detector(), "R2")
    for typ in ("WORD_REPETITION", "RISING_ENDING", "LOW_EFFORT", "UNEVEN_TEMPO"):
        t = evaluate.truths(label(base, typ=typ, words=(7, 7) if typ == "RISING_ENDING" else (10, 15)))[0]
        row = evaluate.edit_direction(run, run, t)
        assert row["direction"] == ("no detector" if C.FLAW_DIM[typ] not in C.DIMS else "toward the reference (repair control)")


def test_trivial_detector_row_equals_the_strict_headline_row_and_unscored_truths_are_not_misses(base, pinned_detector, monkeypatch):
    det = pinned_detector()
    comp = compare(base, base)
    enabled = tuple(d for d in det["regimes"]["R1"]["enabled"] if d != "D7")  # word time unscored, as after a failed D7 gate
    run = Run(base, base, comp, [], score(comp, [], det["regimes"]["R1"], C.PMAX_START), "R1", {}, det["regimes"]["R1"]["scales"], enabled)
    clips = [{"id": t, "split": "val", "level": 2, "parent": "s", "kind": "single"} for t in ("FADE", "WORD_REPETITION")]
    monkeypatch.setattr(evaluate, "clip_runs", lambda ds, det_, cl: [(c, run, label(base, typ=c["id"])) for c in cl])
    ds = SimpleNamespace(clips=lambda **kw: clips)
    head = evaluate.headline_section(ds, det, ("val",))
    trivial = evaluate.trivial_section(ds, det, ("val",))
    for tier in ("core8", "synthetic_only"):
        row = next(r for r in head["groups"][tier]["by_split_strict"] if r["group"] == "all" and r["levels"].startswith("headline"))
        assert trivial["groups"][tier]["totals"]["val"]["detector"] == [row["tp"], row["fp"], row["fn"]]
    assert trivial["groups"]["synthetic_only"]["totals"]["val"]["detector"][2] == 0  # the D7 truth is not a miss
    assert "reference_free (detector h)" in trivial["groups"]["core8"]["totals"]["val"]


def test_flag_all_flags_every_five_word_window_so_any_five_word_truth_can_match(base):
    regs = evaluate._flag_all(12, ("D1", "D2"))
    windows = [(r.i0, r.i1) for r in regs if r.dim == "D1" and r.sign < 0]
    assert windows == [(i, i + 4) for i in range(8)]
    assert sum(r.dim == "D2" for r in regs) == 2 * 11  # every boundary, both directions


def test_reference_free_comparison_does_not_depend_on_the_reference_reading(base):
    other = recording(40, pauses={7: 0.7, 19: 0.8, 30: 0.9}, word_s=0.36, seed=3)
    P = recording(40, pauses={7: 0.7, 19: 0.8, 25: 0.5}, word_s=0.28, seed=5)
    a, b = evaluate.reference_free(compare(base, P), P), evaluate.reference_free(compare(other, P), P)
    for dim in ("D1", "D2", "D3", "D5", "D6", "D9"):
        assert np.allclose(a.dims[dim].x, b.dims[dim].x, equal_nan=True), dim
    assert np.nanmedian(a.dims["D9"].x) == pytest.approx(0) and np.isnan(a.dims["D1"].g)
    assert a.dims["D2"].x[25] > 0 and a.dims["D2"].countable[25]  # the pause at an unpunctuated boundary stands out against the participant's own pauses
    assert not np.isfinite(a.dims["D4"].x).any()


def stress_records(rates, seeds=1, minutes=2.0):
    return [{"participant_recording": f"r{i}", "minutes": minutes, "added": n, "found_before_ids": [0, 1], "found_before_keys": ["D1-", "D5-"],
             "retained_ids": [0] if i % 2 else [0, 1]} for i, n in enumerate(rates) for _ in range(seeds)]


def test_stress_intervals_cluster_the_seeds_of_one_recording():
    one = evaluate.stress_rate(stress_records([0, 1, 2, 3, 4]), lambda r: r["added"])
    three = evaluate.stress_rate(stress_records([0, 1, 2, 3, 4], seeds=3), lambda r: r["added"])
    assert one["ci95"] == three["ci95"] and one["rate"] == three["rate"] == 1.0
    assert one["ci95"][0] <= one["rate"] <= one["ci95"][1]  # the point value and its interval have one basis
    split = [{**r, "participant_recording": f"{r['participant_recording']}-{k}"} for k, r in enumerate(stress_records([0, 1, 2, 3, 4], seeds=3))]
    assert evaluate.stress_rate(split, lambda r: r["added"])["ci95"] != one["ci95"]  # seeds as independent trials narrow it
    few = evaluate.stress_rate(stress_records([1, 3]), lambda r: r["added"])
    assert few["ci95"] == [None, None] and few["per_cluster"] == {"r0": 0.5, "r1": 1.5}
    zero = evaluate.stress_rate(stress_records([0, 0], seeds=3), lambda r: r["added"])
    assert zero["ci95"] == [0.0, pytest.approx(poisson(0, 4.0)[1], abs=1e-3)]  # one seed per recording is the exposure


def test_stress_retention_counts_only_detections_found_before_and_names_broken_keys():
    records = stress_records([0] * 6, seeds=2)
    whole = evaluate.stress_retention(records)
    assert (whole["retained"], whole["found"], whole["unique_found"], whole["retained_every_seed"]) == (18, 24, 12, 9)
    by_key = {k: evaluate.stress_retention(records, k) for k in ("D1-", "D5-")}
    assert by_key["D1-"]["fraction"] == 1.0 and by_key["D5-"]["fraction"] == 0.5
    chance = [{**r, "found_before_ids": [], "found_before_keys": [], "retained_ids": []} for r in records]
    assert evaluate.stress_retention(chance)["fraction"] is None  # a detection that appears only after the transform is not retention
    added = {"D2-": {"rate": 3.0, "ci95": [2.0, 4.0]}, "D1+": {"rate": 0.05, "ci95": [0.0, 0.2]}, "D1- whole clip": {"rate": 5.0, "ci95": [4.0, 6.0]}}
    limits = evaluate.stress_limits(added, by_key, 0.0625)
    assert len(limits) == 2 and limits[0].startswith("adds D2- regions") and limits[1].startswith("loses D5- detections")


def test_dev_v9_comparison_uses_the_v9_accounting_on_the_v9_keys():
    row = {"group": "all", "split": "train", "levels": "headline (L2+L3)", "tp": 74, "fp": 8, "fn": 6, "f1": 0.914, "same_change_duplicates": 12,
           "every_prediction": {"false_by_key": {"D1-": 3, "D5-": 5, "D9-": 12, "D7+": 2}, "same_change_detections": 1}}
    out = evaluate.dev_v9_change({"groups": {"core8": {"by_split_strict": [row]}}})
    r = out["rows"][0]
    assert (r["current_fp_v9_accounting"], r["current_fp_v9_accounting_v9_keys"], r["current_tp_v9_accounting"]) == (22, 8, 73)
    assert r["v9_keys_fp_change_v9_accounting"] == 8 - 12 and "not a change in false regions" in out["table"]


def test_directional_cause_names_the_moved_penalty_and_a_non_monotone_edit(base, pinned_detector):
    det = pinned_detector()
    clean, rushed = run_pair(base, base, det, "R1"), run_pair(base, base, det, "R1")
    rushed.regions = [local("D1", 10, 14), local("D9", 10, 14)]  # one RUSH change: D1- carries the penalty
    f = {"dimension": "D9", "words": [10, 14], "realised": {"value": -0.5}}
    assert evaluate.directional_cause({1: (clean, f), 2: (rushed, f), 3: (rushed, f)}, False).startswith("penalty charged")
    cells = {lv: (clean, {**f, "realised": {"value": v}}) for lv, v in ((1, -0.7), (2, -0.3), (3, -0.9))}
    assert evaluate.directional_cause(cells, False) == "realised edit not monotone across levels"
    assert evaluate.directional_cause(cells, True) == "pause not measured at the labelled boundary"


def test_natural_rush_realised_is_the_applied_word_time_ratio_from_the_label():
    f = {"type": "NATURAL_RUSH", "events": [{"kind": "stretch", "output_samples": 450, "parent_span": [0, 500]},
                                            {"kind": "stretch", "output_samples": 450, "parent_span": [600, 1100]},
                                            {"kind": "pause_cut", "output_samples": 10, "parent_span": [500, 600]}]}
    assert evaluate.span_realised(None, f) == pytest.approx(math.log(0.9))


def test_r2_limits_state_unmet_budgets_with_the_sources_and_languages_above_them():
    total = {"rate": 0.568, "bootstrap_upper95": 0.65, "budget_status": "not met",
             "by_source": {"accent": {"rate": 0.894}, "ears": {"rate": 0.173}},
             "by_L1": {"arabic": {"rate": 0.99, "readers": 25, "comparison_minutes": 68.9}, "tiny": {"rate": 9.0, "readers": 1, "comparison_minutes": 1.0}}}
    single = {"by_type": [["check", "RUSH", 3, 0, 18, 18, [0, .2]], ["check", "MONOTONE", 3, 17, 18, 18, [.7, 1]]]}
    out = evaluate.r2_limits({"single": single}, {"single": {"select": {"total_local": total}}})
    assert out[0] == "single: check-reader away-edits detected in fewer than 50%: RUSH L3 0/18"
    assert "not met" in out[1] and "accent 0.894/min" in out[1] and "arabic 0.99/min" in out[1] and "ears" not in out[1] and "tiny" not in out[1]
    assert evaluate.budget_limits("x", {"total_local": {**total, "budget_status": "met"}}) == []


def test_lockbox_is_measured_only_by_the_final_evaluation(base, pinned_detector, monkeypatch, tmp_path):
    class DS:
        root = tmp_path
        def clips(self, **kw): return []
        def labels(self, c): return label(base)
    null = {"budget_statement": "0.5/min budget is not met at the point rate", "local_by_key": {},
            "total_local": {"rate": 0.7, "bootstrap_upper95": 0.9, "budget_status": "not met", "by_source": {}, "by_L1": {}}}
    calls = []
    def lockbox(ds, det, *, final):
        calls.append(final)
        return {"set": "lockbox", "modes": {"single": null, "consensus5": null}, "readers_by_source": {"accent": 3}, "comparisons": {"single": 15},
                "excluded": []}
    for name, value in (("load_dataset", lambda *a: DS()), ("load_detector", lambda *a: pinned_detector()), ("warm", lambda *a: None),
                        ("final_gate", lambda *a: None), ("figures", lambda *a: []), ("SECTIONS", []), ("lockbox_null_report", lockbox)):
        monkeypatch.setattr(evaluate, name, value)
    res = evaluate.run(tmp_path, tmp_path / "detector.json", None, tmp_path, ("train", "val"))
    assert "lockbox" not in res and calls == []
    res = evaluate.run(tmp_path, tmp_path / "detector.json", None, tmp_path, ("train", "val"), final=True)
    assert calls == [True] and len(res["lockbox"]["limits"]) == 2
    assert "## R2 lockbox false regions (final evaluation, both modes)" in (tmp_path / "eval" / "tables.md").read_text()
    with pytest.raises(ValueError, match="final"):
        calibrate.lockbox_null_report(DS(), pinned_detector(), final=False)
