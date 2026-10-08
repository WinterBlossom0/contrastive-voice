import os

import fake_aligner as fake
import numpy as np
import pytest
from synth import synth

from cvoice import pool as poolmod
from cvoice.align import Alignment, parse_transcript
from cvoice.pipeline import make_job, map_calls, run_jobs
from cvoice.pool import PoolError, PreparePool

FACTORY = "fake_aligner:make"
WORDS = "we hold these truths to be self evident that all men are created equal".split()


def clip(n_words: int, seed: int):
    """(wav, transcript) of a synthetic clip; distinct word counts give distinct lengths, hence distinct fake alignments."""
    wav, _, _ = synth(n_words, seed=seed)
    return wav, parse_transcript(" ".join(WORDS[i % len(WORDS)] for i in range(n_words)))


def jobs():
    return [make_job(*clip(n, n)) for n in (10, 14, 12, 16, 11, 13)]


def same(a, b) -> None:
    """Two Recordings agree on everything the pipeline reads."""
    np.testing.assert_array_equal(a.wav, b.wav)
    for f in ("start", "end", "compat"):
        np.testing.assert_array_equal(getattr(a.al, f), getattr(b.al, f))
    for f in ("L", "E", "f0", "S", "Q"):
        np.testing.assert_array_equal(getattr(a.fr, f), getattr(b.fr, f))
    for f in ("win_T", "win_R", "win_E", "win_Q", "sil"):
        np.testing.assert_array_equal(getattr(a, f), getattr(b, f))  # NaN == NaN here


def test_default_plan_follows_the_visible_gpus_and_the_overrides(monkeypatch):
    monkeypatch.delenv("CVOICE_WORKERS", raising=False)
    monkeypatch.delenv("CVOICE_DEVICES", raising=False)
    monkeypatch.setattr(os, "cpu_count", lambda: 16)
    monkeypatch.setattr(poolmod, "visible_gpus", lambda: 2)
    assert poolmod.plan() == (4, ["cuda:0", "cuda:1"])  # two workers per GPU
    monkeypatch.setattr(poolmod, "visible_gpus", lambda: 0)
    assert poolmod.plan() == (4, ["cpu"])  # min(4, cpu count)
    monkeypatch.setattr(os, "cpu_count", lambda: 2)
    assert poolmod.plan() == (2, ["cpu"])
    monkeypatch.setenv("CVOICE_DEVICES", "cuda:1")
    assert poolmod.plan() == (2, ["cuda:1"])
    monkeypatch.setenv("CVOICE_WORKERS", "3")
    assert poolmod.plan() == (3, ["cuda:1"]) and poolmod.plan(workers=1, devices=["cpu"]) == (1, ["cpu"])
    monkeypatch.setattr(poolmod, "visible_gpus", lambda: (_ for _ in ()).throw(AssertionError("GPUs must not be probed")))
    assert poolmod.plan(devices=["cpu"])[1] == ["cpu"]  # explicit devices: nothing is probed
    with pytest.raises(ValueError):
        poolmod.plan(workers=0, devices=["cpu"])
    assert PreparePool(workers=1, devices=["cuda:0"], aligner_factory=FACTORY).device_class == "cuda"  # no process starts before the first map
    assert PreparePool(workers=1, devices=["cpu"], aligner_factory=FACTORY).device_class == "cpu"


def test_one_cpu_worker_gives_exactly_the_sequential_results():
    js = jobs()
    seq = run_jobs(js, None, fake.make("cpu", 1))
    with PreparePool(workers=1, devices=["cpu"], aligner_factory=FACTORY) as p:
        par = p.map(js)
    assert len(par) == len(seq) == len(js)
    for a, b in zip(par, seq):
        same(a, b)


def test_two_workers_keep_input_order_share_duplicates_cache_and_run_calls(tmp_path):
    js = jobs()
    seq = run_jobs(js, None, fake.make("cpu", 1))
    with PreparePool(workers=2, devices=["cpu", "cpu"], cache_dir=tmp_path, aligner_factory=FACTORY) as p:
        par = p.map(js)
        for a, b in zip(par, seq):
            same(a, b)
        back = p.map(js[::-1] + [js[0]])  # reversed order plus a duplicate: results follow the input, whatever the scheduling
        for a, b in zip(back, seq[::-1] + [seq[0]]):
            same(a, b)
        assert len(list(tmp_path.glob("align_*.npz"))) == len(js)  # the on-disk alignment cache is used by workers
        al = p.map([make_job(js[1].wav, js[1].tr, "align"), make_job(js[2].wav, js[2].tr, "emit")])
        assert isinstance(al[0], Alignment) and np.array_equal(al[0].start, seq[1].al.start)
        np.testing.assert_array_equal(al[1], fake.make("cpu", 1).emissions(js[2].wav))
        assert p.starmap(fake.square, [(i,) for i in range(7)]) == [i * i for i in range(7)]
        assert set(p.starmap(fake.where, [()] * 4)) <= {"cpu"}
        with pytest.raises(PoolError, match=r"call 1 \[square\] failed on cpu: ValueError: negative"):
            p.starmap(fake.square, [(2,), (-1,), (3,)])
        assert map_calls(fake.square, [(3,), (4,)], p) == [9, 16]  # the helper the stages use, with a pool
        stats = p.stats()
    assert stats["jobs"]["prepare"] == len(js) * 2 + 1 and stats["jobs"]["align"] == 1 and stats["jobs"]["emit"] == 1 and stats["workers"] == 2


def test_a_failing_job_surfaces_with_its_name_and_a_dead_worker_is_reported():
    ok = make_job(*clip(10, 1))
    bad_wav = np.zeros(fake.FAIL_LEN)
    bad = make_job(bad_wav, parse_transcript("we hold these"), "prepare")
    with PreparePool(workers=1, devices=["cpu"], aligner_factory=FACTORY) as p:
        with pytest.raises(PoolError) as e:
            p.map([ok, bad])
        assert bad.key in str(e.value) and "planted failure" in str(e.value) and "RuntimeError" in str(e.value) and "cpu" in str(e.value)
    dead = make_job(np.zeros(fake.DIE_LEN), parse_transcript("we hold these"), "prepare")
    with PreparePool(workers=1, devices=["cpu"], aligner_factory=FACTORY) as p:
        with pytest.raises(PoolError, match="worker process died"):
            p.map([dead])


def test_run_jobs_without_a_pool_is_the_plain_in_process_path():
    js = jobs()[:2]
    a = run_jobs(js, None, fake.make("cpu", 1))
    b = [run_jobs([j], None, fake.make("cpu", 1))[0] for j in js]
    for x, y in zip(a, b):
        same(x, y)
    assert run_jobs([], None) == [] and map_calls(fake.square, [(3,), (4,)], None) == [9, 16]


def test_clip_generation_in_a_worker_is_byte_identical_to_in_process():
    from synth import recording

    from cvoice.calibrate import placebo_audio
    B = recording(40, pauses={7: 0.7, 19: 0.8, 30: 0.6})
    direct = placebo_audio(B, "b", 0)
    with PreparePool(workers=1, devices=["cpu"], aligner_factory=FACTORY) as p:
        (remote,) = p.starmap(placebo_audio, [(B, "b", 0)])
    np.testing.assert_array_equal(direct, remote)


class StubDataset:
    """Just enough of Dataset for the device-agreement section: two single clips of one baseline."""

    def __init__(self, pool):
        self.pool = pool
        wav, tr = clip(20, 3)
        self._wav, self._tr = wav, tr
        self._clips = [{"id": f"b__single_L{i}A", "parent": "b", "split": "val"} for i in (1, 2)]

    def clips(self, **where):
        return self._clips

    def entry(self, kind, id_):
        return {"id": id_}

    def wav(self, e):
        return self._wav

    def transcript(self, e):
        return self._tr

    def clip_transcript(self, c):
        return self._tr


def test_device_agreement_skips_on_cpu_and_reports_differences_on_gpu(monkeypatch, pinned_detector):
    from types import SimpleNamespace

    from cvoice import evaluate
    det = pinned_detector(2.0)
    skipped = evaluate.device_section(StubDataset(SimpleNamespace(device_class="cpu", devices=["cpu"])), det, ("train", "val"))
    assert "skipped" in skipped and "no GPU" in skipped["skipped"]
    assert "skipped" in evaluate.device_section(StubDataset(None), det, ("train", "val"))  # in-process run: no pool at all
    monkeypatch.setattr(evaluate, "PreparePool", lambda workers, devices: PreparePool(workers=workers, devices=devices, aligner_factory=FACTORY))
    res = evaluate.device_section(StubDataset(SimpleNamespace(device_class="cuda", devices=["cuda:0", "cuda:1"])), det, ("train", "val"))
    row = res["rows"][0]
    assert row["split"] == "val" and row["gpu_device"] == "cuda:0" and row["clips"] == 2 and row["recordings"] == 3
    assert row["max_word_time_diff_ms"] > 0 and isinstance(row["flags_identical"], bool) and "max word-time difference" in res["table"]
