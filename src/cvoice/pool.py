"""PreparePool: alignment + feature extraction spread over worker processes, one aligner per worker pinned to one device.

Workers start with the 'spawn' method (never fork: no CUDA state is inherited, and CUDA is never initialised in the
parent). Each worker loads its aligner once. Default plan: POOL_WORKERS_PER_GPU workers per visible GPU (feature extraction
is CPU work and the T4 x2 machine has 4 vCPUs), otherwise min(POOL_MAX_CPU_WORKERS, cpu count) CPU workers, one torch thread
each. Overrides: CVOICE_DEVICES ("cuda:0,cuda:1" or "cpu") and CVOICE_WORKERS (an integer).

    with PreparePool(cache_dir=cache) as pool:
        recs = pool.map([make_job(wav, tr) for wav, tr in clips])        # input order, whatever the scheduling

The dashboard, the tests and the one-clip smoke test do not use a pool: `pipeline.run_jobs(jobs, pool=None)` is the plain
in-process path and gives the same results.
"""
from __future__ import annotations

import importlib
import json
import multiprocessing as mp
import os
import subprocess
import time
import traceback
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from pathlib import Path

from . import config as C

DEFAULT_FACTORY = "cvoice.align:load_aligner"  # "module:function"; called as function(device, torch_threads)
_STATE: dict = {}  # per worker process: device, aligner, cache directory


class PoolError(RuntimeError):
    """A pool job failed (the message names the job and the device) or a worker process died."""


# ============================================================================================ worker side
def _init(assign, factory: str, cache_dir, threads: int) -> None:
    _, device = assign.get()
    mod, _, fn = factory.partition(":")
    _STATE.update(device=device, cache=cache_dir, aligner=getattr(importlib.import_module(mod), fn)(device, threads))


def worker_aligner():
    """The aligner of this pool worker (None in any other process: callers then fall back to the in-process default)."""
    return _STATE.get("aligner")


def _run(kind: str, payload, label: str):
    try:
        if kind == "job":
            from .pipeline import detach, execute
            return detach(execute(payload, _STATE["aligner"], _STATE["cache"]))
        fn, args = payload
        return fn(*args)
    except Exception as e:
        raise PoolError(f"{label} failed on {_STATE.get('device')}: {type(e).__name__}: {e}\n{traceback.format_exc()}") from None


# ============================================================================================ device plan
def visible_gpus() -> int:
    """Number of usable GPUs, counted without initialising CUDA: nvidia-smi (or CUDA_VISIBLE_DEVICES), and only when the
    installed torch is a CUDA build."""
    import torch
    if torch.version.cuda is None:
        return 0
    cv = os.environ.get("CUDA_VISIBLE_DEVICES")
    if cv is not None:
        return len([d for d in cv.split(",") if d.strip()])
    try:
        out = subprocess.run(["nvidia-smi", "-L"], capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.TimeoutExpired):
        return 0
    return sum(line.startswith("GPU ") for line in out.splitlines())


def plan(workers: int | None = None, devices: list[str] | None = None) -> tuple[int, list[str]]:
    """(worker count, devices). Arguments beat CVOICE_WORKERS / CVOICE_DEVICES, which beat the defaults."""
    if devices is None and os.environ.get("CVOICE_DEVICES"):
        devices = [d.strip() for d in os.environ["CVOICE_DEVICES"].split(",") if d.strip()]
    if devices is None:
        devices = [f"cuda:{i}" for i in range(visible_gpus())] or ["cpu"]
    if workers is None and os.environ.get("CVOICE_WORKERS"):
        workers = int(os.environ["CVOICE_WORKERS"])
    if workers is None:
        gpu = any(d.startswith("cuda") for d in devices)
        workers = C.POOL_WORKERS_PER_GPU * len(devices) if gpu else min(C.POOL_MAX_CPU_WORKERS, os.cpu_count() or 1)
    if workers < 1 or not devices:
        raise ValueError(f"need at least one worker and one device, got {workers} on {devices}")
    return workers, devices


def gpu_memory_mib() -> list[dict]:
    """[{index, used, total}] in MiB from nvidia-smi (all processes on each GPU); [] without a GPU."""
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=index,memory.used,memory.total", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.TimeoutExpired):
        return []
    rows = [[v.strip() for v in line.split(",")] for line in out.splitlines() if line.strip()]
    return [{"index": int(r[0]), "used": int(r[1]), "total": int(r[2])} for r in rows if len(r) == 3]


# ============================================================================================ parent side
class PreparePool:
    """Worker processes with one aligner each; map() / starmap() return results in input order."""

    def __init__(self, workers: int | None = None, devices: list[str] | None = None, cache_dir: Path | None = None,
                 aligner_factory: str = DEFAULT_FACTORY) -> None:
        self.workers, self.devices = plan(workers, devices)
        self.cache_dir, self.factory = cache_dir, aligner_factory
        self.device_class = "cuda" if any(d.startswith("cuda") for d in self.devices) else "cpu"
        self._ex: ProcessPoolExecutor | None = None
        self._count: Counter = Counter()
        self._seconds = 0.0
        print(f"[pool] {self.workers} worker(s) on {self.devices}", flush=True)

    def _executor(self) -> ProcessPoolExecutor:
        if self._ex is None:
            ctx = mp.get_context("spawn")
            assign = ctx.Queue()
            for i in range(self.workers):
                assign.put((i, self.devices[i % len(self.devices)]))
            self._ex = ProcessPoolExecutor(self.workers, mp_context=ctx, initializer=_init,
                                           initargs=(assign, self.factory, self.cache_dir, C.POOL_TORCH_THREADS))
        return self._ex

    def _gather(self, futures: list, labels: list[str]) -> list:
        out = []
        try:
            for f, label in zip(futures, labels):
                try:
                    out.append(f.result())
                except BrokenProcessPool as e:
                    raise PoolError(f"a worker process died or failed to start while {label} was pending: {e}") from e
        except BaseException:
            for f in futures:
                f.cancel()
            raise
        return out

    def map(self, jobs: list) -> list:
        """Results of pipeline jobs in input order. Duplicate jobs (same kind and key) are computed once."""
        from .pipeline import attach
        if not jobs:
            return []
        t0 = time.time()
        unique: dict = {}
        for j in jobs:
            unique.setdefault((j.kind, j.key), j)  # same content: the first one stands in for the rest
        keys = list(unique)
        labels = [f"job {i} [{k[0]} {k[1]}]" for i, k in enumerate(keys)]
        ex = self._executor()
        done = dict(zip(keys, self._gather([ex.submit(_run, "job", unique[k], lb) for k, lb in zip(keys, labels)], labels)))
        self._count.update(j.kind for j in jobs)
        self._seconds += time.time() - t0
        return [attach(done[(j.kind, j.key)], j) for j in jobs]

    def starmap(self, fn, args: list[tuple]) -> list:
        """[fn(*a) for a in args] in worker processes, input order (fn: a module-level function; used for DSP generation)."""
        if not args:
            return []
        t0 = time.time()
        labels = [f"call {i} [{fn.__name__}]" for i in range(len(args))]
        ex = self._executor()
        out = self._gather([ex.submit(_run, "call", (fn, a), lb) for a, lb in zip(args, labels)], labels)
        self._count["call"] += len(args)
        self._seconds += time.time() - t0
        return out

    def stats(self) -> dict:
        return {"workers": self.workers, "devices": self.devices, "device_class": self.device_class, "jobs": dict(self._count),
                "seconds": round(self._seconds, 1), "gpu_memory_mib": gpu_memory_mib() if self.device_class == "cuda" else []}

    def close(self) -> None:
        """Print one `[pool] {...}` statistics line (the runner reads it; GPU memory is taken while the workers still hold it)
        and stop the workers."""
        print("[pool] " + json.dumps(self.stats(), sort_keys=True), flush=True)
        if self._ex is not None:
            self._ex.shutdown(wait=True, cancel_futures=True)
            self._ex = None

    def __enter__(self) -> "PreparePool":
        return self

    def __exit__(self, *exc) -> None:
        self.close()
