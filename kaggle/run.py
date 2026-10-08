#!/usr/bin/env python3
"""cvoice-build: private script kernel, standard compute = Kaggle with two T4 GPUs (a kernel without a GPU works too, slowly). Bootstraps the
locked project environment, then runs

    dataset build -> calibrate -> evaluate -> gallery

with a log, a wall time, a clip count, clips per second and GPU memory per stage. A failed dataset or calibrate stage stops the
run (nothing later can work); a failed evaluate stage does not (the gallery needs only the detector). In every case the run
packages what exists as zip chunks of at most 64 MiB plus SHA256SUMS and STATUS.json in /kaggle/working (the only files left
there) and EXITS 0: the outcome is STATUS.json (`complete`, `failed_stage`, `failed_stages`), because a kernel that exits non-zero
may be marked ERROR and lose its outputs.

Devices: GPUs are detected with nvidia-smi (the runner imports no torch). With a GPU the locked environment is synced with the 'gpu'
extra (torch / torchaudio 2.10.0 from the CUDA 12.6 index), otherwise with the 'cpu' extra; the plan (extra, devices, workers) is
logged, stored in STATUS.json and handed to the stages as CVOICE_DEVICES / CVOICE_WORKERS (existing values win). Each stage runs a
PreparePool with two workers per GPU, or min(4, cpu count) CPU workers; if the GPU torch cannot see CUDA the plan falls back to CPU.
Final evaluation: the evaluate stage gets --final (test split and R2 lockbox, once per config hash; the record
models/final_evaluations.json is taken from the project dataset when it has one and returned in the outputs) when CVOICE_FINAL=1
is in the environment, or, with no CVOICE_FINAL in the environment, when FINAL_DEFAULT below is True. To stage the last run,
set FINAL_DEFAULT = True in this file before the push (CVOICE_FINAL=0 still turns it off).

Mounts (found by name under /kaggle/input): cvoice-project (source, uv.lock, manifest) and optionally cvoice-sources (audio,
transcripts). Without cvoice-sources, the runner downloads the original recordings into /tmp and checks their audio SHA-256;
transcripts are copied from the repository snapshot and checked against data/transcripts/sha256.json.
Push (private, internet on; metadata kaggle/kernel-metadata.json = T4 x2: "enable_gpu": true, "machine_shape": "NvidiaTeslaT4"):

    kaggle kernels push -p kaggle --timeout 7200

Reconstruct with your own Kaggle account, starting with only this code:
1. From the repository root (quote paths with spaces), run:

    scripts/stage_project.sh 'build/cvoice-project'

2. In build/cvoice-project/dataset-metadata.json change id to YOUR_USERNAME/cvoice-project. Upload your own PRIVATE snapshot:

    kaggle datasets create -p 'build/cvoice-project' --dir-mode zip --keep-tabular

   Dataset creation is private by default; do not add --public. For subsequent snapshots use the version command printed by
   stage_project.sh. No access to the author's datasets is needed.
3. In kaggle/kernel-metadata.json set id to YOUR_USERNAME/cvoice-build, dataset_sources to ["YOUR_USERNAME/cvoice-project"]
   (remove electroknight/cvoice-sources) and kernel_sources to YOUR_USERNAME/cvoice-data and YOUR_USERNAME/cvoice-data-vctk
   (see below); keep is_private and enable_internet true. Edit SOURCE_USER_AGENT's contact URL, then run the push command
   above. Each download URL gets at most three attempts within a ten-minute retry deadline; a hash mismatch stops the build.
4. Check STATUS.json: complete must be true, sources.route must be "rebuilt from origins", sources.transcript_source must be
   "repository snapshot", and every audio and transcript check must match.
   Compare dataset_manifest_sha256 (also detector.json report.manifest_sha256) and dataset_counts with the reference run of
   models/detector.json: d67c9cd95b46efb247f10167b57b8288be954efe7df48bc4cc2c786d4f04a50f, with 9 baselines,
   1953 readers, 448 flawed clips and 2410 audio files. File counts here mean audio files, excluding labels.
   SHA256SUMS checks each run's packages; zip hashes and timings need not match another run. Download the output chunks,
   STATUS.json and SHA256SUMS together; scripts/import_run.sh RUN_DIR checks them before importing a complete run.
   The transcript snapshots (one for each transcript in data/sources_manifest.json) and their hashes travel with the project.
   Gutenberg uses the archived plain-text edition.
   Equal counts alone do not establish identical data; a different manifest hash needs investigation.

External research corpora use the kaggle/data/fetch.py kernel and the subsets/licences in docs/research/chain/data/PLAN.md. Set
kaggle/data/kernel-metadata.json id to YOUR_USERNAME/cvoice-data, keep its five public dataset_sources and is_private/enable_internet
true, then run `kaggle kernels push -p kaggle/data`. The build also needs a second output: a copy of that kernel with id
YOUR_USERNAME/cvoice-data-vctk whose entry point calls main(["--only", "vctk"]); the build checks this mount but reads no VCTK audio.
Defaults include priority 2 (CVOICE_PRIORITY2=0 omits it). Check STATUS.json for every completed source and keep manifest.json,
LICENSES.md, fetch.log and every tar part. LibriTTS prominence, VCTK, Accent Archive and LibriStutter need those public mounts, which
the script cannot rebuild; SEP-28k supplies labels only. Outputs stay private; no kernel needs an access grant from the author.

Environment, caches, the copied project and all intermediates live under /tmp; the checkpoint is fetched into /tmp/torch_home and
verified by SHA-256 inside cvoice.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
import zipfile
from email.utils import parsedate_to_datetime
from http.client import HTTPException
from pathlib import Path
from urllib.parse import urlsplit

UV_VERSION = "0.12.3"
PYTHON_VERSION = "3.12"
CHUNK_BYTES = 64 * 1024 * 1024  # zip chunks stay at or below 64 MiB
WORKING = Path(os.environ.get("CVOICE_WORKING", "/kaggle/working"))
INPUT = Path(os.environ.get("CVOICE_INPUT", "/kaggle/input"))
TMP = Path(os.environ.get("CVOICE_TMP", "/tmp/cvoice-work"))
VENV = Path("/tmp/cvoice-venv")

PROJECT = TMP / "project"
DATA = TMP / "data"
CACHE = TMP / "cache"
OUT = TMP / "out"
LOGS = OUT / "logs"
ARCHIVE_PREFIX = "cvoice-build-part"

# Off: the test split and the R2 lockbox are measured once per config hash, so only the staged last run sets this to True.
FINAL_DEFAULT = False
CONTINUE_AFTER_FAILURE = ("evaluate",)  # the gallery needs only the detector and the dataset, not the evaluation tables
STATUS: dict = {"schema": 1, "complete": False, "failed_stage": None, "failed_stages": [], "stages": [], "parts": []}
POOL_PREFIX = "[pool] "  # statistics line printed by cvoice.pool.PreparePool.close()
T0 = time.time()

# Replace this placeholder with a URL through which Wikimedia can contact the operator.
SOURCE_USER_AGENT = "ContrastiveVoice-rebuild-bot/1.0 (https://example.org/EDIT-ME-ContrastiveVoice-contact)"
SOURCE_HOST_INTERVAL = 5.0
SOURCE_RETRY_SECONDS = 600.0
SOURCE_HOST_READY: dict[str, float] = {}
# https://wikitech.wikimedia.org/wiki/Robot_policy permits 25 Mbps over ten-second intervals.
SOURCE_BYTES_PER_SECOND = {"upload.wikimedia.org": 2_500_000}  # 20 Mbps, allowing for chunk boundaries
# Verified 2026-10-02: redirect target is 13,006,021 bytes with the manifest's pinned SHA-256.
# This is another URL for the same upload host, so its cooldown must also apply to redirects.
SOURCE_FALLBACK_URLS = {
    "eisenhower_farewell_1961": (
        "https://commons.wikimedia.org/wiki/Special:Redirect/file/Eisenhower_farewell_address.ogg",
    ),
}


def log(msg: str) -> None:
    print(f"[run {time.time() - T0:7.1f}s] {msg}", flush=True)


def write_status() -> None:
    WORKING.mkdir(parents=True, exist_ok=True)
    (WORKING / "STATUS.json").write_text(json.dumps(STATUS, indent=1, sort_keys=True) + "\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    return h.hexdigest()


# ============================================================================================ bootstrap
def find_mount(name: str) -> Path:
    """Folder of a mounted dataset. Kaggle mounts at /kaggle/input/<name> or /kaggle/input/datasets/<owner>/<name>."""
    for cand in (INPUT / name, *sorted(INPUT.glob(f"*/*/{name}")), *sorted(INPUT.glob(f"*/{name}"))):
        if cand.is_dir():
            return cand
    return INPUT / name  # not mounted: the caller reports the missing path


def source_check(entry: dict, path: Path, expected: str | None, url: str | None = None) -> dict:
    got = sha256_file(path) if path.is_file() else None
    check = {"entry": entry["id"], "file": path.name, "url": url, "sha256": got, "expected_sha256": expected,
             "match": got == expected if expected else None, "bytes": path.stat().st_size if path.is_file() else None}
    STATUS["sources"]["checks"].append(check)
    return check


class SourceWaitExceeded(TimeoutError):
    pass


def wait_for_source_host(url: str, deadline: float) -> None:
    host = urlsplit(url).hostname
    now = time.monotonic()
    delay = max(0.0, SOURCE_HOST_READY.get(host, now) - now)
    if now + delay > deadline:
        raise SourceWaitExceeded(f"{host}: Retry-After / host interval exceeds {SOURCE_RETRY_SECONDS:g}s retry deadline")
    if delay:
        time.sleep(delay)
    SOURCE_HOST_READY[host] = time.monotonic() + SOURCE_HOST_INTERVAL
    log(f"source request: {host}: {url}")


def open_source(request, timeout: float, deadline: float):
    class PacedRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
            if redirected is not None:
                wait_for_source_host(redirected.full_url, deadline)
            return redirected

    return urllib.request.build_opener(PacedRedirect()).open(request, timeout=timeout)


def source_retry_delay(error: Exception, attempt: int) -> float:
    value = error.headers.get("Retry-After", "").strip() if isinstance(error, urllib.error.HTTPError) and error.headers else ""
    if value.isdigit():
        return float(value)
    if value:
        try:
            return max(0.0, parsedate_to_datetime(value).timestamp() - time.time())
        except (ValueError, TypeError, OverflowError):
            pass
    return 5.0 * 2 ** attempt


def copy_source(response, output, url: str) -> None:
    host = urlsplit(response.geturl() if hasattr(response, "geturl") else url).hostname
    rate = SOURCE_BYTES_PER_SECOND.get(host)
    if rate is None:
        shutil.copyfileobj(response, output)
        return
    while True:
        started = time.monotonic()
        block = response.read(64 * 1024)
        if not block:
            return
        output.write(block)
        delay = len(block) / rate - (time.monotonic() - started)
        if delay > 0:
            time.sleep(delay)


def download_source(entry: dict, url: str, path: Path, expected: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + SOURCE_RETRY_SECONDS
    attempts = 0
    for candidate in (url, *SOURCE_FALLBACK_URLS.get(entry["id"], ())):
        request = urllib.request.Request(candidate, headers={"User-Agent": SOURCE_USER_AGENT, "Accept-Encoding": "identity"})
        for attempt in range(3):
            try:
                wait_for_source_host(candidate, deadline)
                attempts += 1
                with open_source(request, timeout=120, deadline=deadline) as response, path.open("wb") as output:
                    copy_source(response, output, candidate)
                    size = response.headers.get("Content-Length")
                if size is not None and path.stat().st_size != int(size):
                    raise OSError("incomplete download")
            except (OSError, HTTPException) as error:
                path.unlink(missing_ok=True)
                last_error = error
                if time.monotonic() >= deadline or isinstance(error, SourceWaitExceeded):
                    break
                delay = source_retry_delay(error, attempt)
                failed_url = error.url if isinstance(error, urllib.error.HTTPError) else candidate
                host = urlsplit(failed_url).hostname
                SOURCE_HOST_READY[host] = max(SOURCE_HOST_READY.get(host, 0), time.monotonic() + delay)
                retry_after = error.headers.get("Retry-After") if isinstance(error, urllib.error.HTTPError) and error.headers else None
                log(f"{entry['id']}: download attempt {attempt + 1} failed: {error}; "
                    f"Retry-After={retry_after!r}; host cooldown {delay:g}s")
                continue
            check = source_check(entry, path, expected, candidate)
            if expected and not check["match"]:
                path.unlink()
                raise RuntimeError(f"{entry['id']}: SHA-256 mismatch for {path.name}: expected {expected}, got {check['sha256']}")
            return
        if time.monotonic() >= deadline:
            break
    source_check(entry, path, expected, candidate)["error"] = str(last_error)
    raise RuntimeError(f"{entry['id']}: download failed after {attempts} attempts: {candidate}: {last_error}") from last_error


def prepare_sources(project: Path) -> Path:
    mount = find_mount("cvoice-sources")
    root = mount if mount.is_dir() else TMP / "sources"
    STATUS["sources"] = {"route": "mounted" if mount.is_dir() else "rebuilt from origins", "path": str(root), "checks": []}
    entries = json.loads((project / "data" / "sources_manifest.json").read_text())["entries"]
    if not mount.is_dir():
        STATUS["sources"]["transcript_source"] = "repository snapshot"
        snapshots = project / "data" / "transcripts"
        hashes = json.loads((snapshots / "sha256.json").read_text())
        for entry in entries:
            name = Path(entry["transcript"]).name
            if name not in hashes:
                raise RuntimeError(f"no repository transcript SHA-256 recorded for {name}")
        for name, expected in sorted(hashes.items()):
            local = snapshots / name
            check = source_check({"id": Path(name).stem}, local, expected)
            check["origin"] = "repository snapshot"
            if not check["match"]:
                raise RuntimeError(f"transcript SHA-256 mismatch for {name}: expected {expected}, got {check['sha256']}")
            target = root / "transcripts" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(local, target)
    transcripts = set()
    for entry in entries:
        if mount.is_dir():
            audio = next(root.rglob(entry["audio_file"]), root / entry["audio_file"])
            source_check(entry, audio, entry["sha256"])
        else:
            download_source(entry, entry["download_url"], root / entry["audio_file"], entry["sha256"])
        if not mount.is_dir() or entry["transcript"] in transcripts:
            continue
        transcripts.add(entry["transcript"])
        local = project / "data" / entry["transcript"]
        target = root / entry["transcript"]
        path = local if entry["transcript_root"] == "repo" else next(root.rglob(target.name), target)
        source_check(entry, path, sha256_file(local) if local.is_file() else None)
    log(f"sources: {STATUS['sources']['route']} ({len(STATUS['sources']['checks'])} file checks)")
    write_status()
    return root


def unpack_project_zips(base: Path, target: Path) -> None:
    """Kaggle `--dir-mode zip` leaves one zip per top-level folder (src.zip, data.zip) next to the loose top-level files. Extract
    every zip into a subfolder named after its stem (zips that already carry that folder name unpack in place) and copy the loose
    files alongside, which rebuilds the project layout."""
    for z in sorted(base.rglob("*.zip")):
        with zipfile.ZipFile(z) as zf:
            prefixed = all(n.split("/")[0] == z.stem for n in zf.namelist())
            zf.extractall(target if prefixed else target / z.stem)
    for f in base.iterdir():
        if f.is_file() and f.suffix != ".zip":
            shutil.copy2(f, target / f.name)


def find_project_root(base: Path) -> Path:
    """The folder under the mounted project dataset that holds pyproject.toml (Kaggle may nest or unpack zips)."""
    for dirpath, _, files in os.walk(base):
        if "pyproject.toml" in files and (Path(dirpath) / "src" / "cvoice").is_dir():
            return Path(dirpath)
    if base.is_dir() and any(base.rglob("*.zip")):
        target = TMP / "unzipped_project"
        shutil.rmtree(target, ignore_errors=True)
        target.mkdir(parents=True)
        unpack_project_zips(base, target)
        return find_project_root(target)
    raise FileNotFoundError(f"no project (pyproject.toml + src/cvoice) under {base}")


def verify_project(root: Path) -> None:
    """Check every file listed in project_sha256.txt (written by scripts/stage_project.sh)."""
    sums = root / "project_sha256.txt"
    if not sums.exists():
        log("no project_sha256.txt: source integrity not checked")
        return
    bad = []
    for line in sums.read_text().splitlines():
        digest, _, name = line.partition("  ")
        if not (root / name).exists() or sha256_file(root / name) != digest:
            bad.append(name)
    if bad:
        raise RuntimeError(f"project files differ from project_sha256.txt: {bad[:5]}")
    log(f"project integrity verified ({len(sums.read_text().splitlines())} files)")


def child_env() -> dict:
    env = dict(os.environ)
    env.update({"OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "NUMBA_NUM_THREADS": "1", "PYTHONHASHSEED": "0",
                "PYTHONUNBUFFERED": "1", "TORCH_HOME": "/tmp/torch_home", "UV_CACHE_DIR": "/tmp/uv-cache", "UV_PYTHON_INSTALL_DIR": "/tmp/uv-python",
                "UV_PYTHON_PREFERENCE": "only-managed", "UV_PROJECT_ENVIRONMENT": str(VENV)})
    env.pop("UV_SYSTEM_PYTHON", None)
    return env


def sh(cmd: list[str], logfile: Path | None = None, cwd: Path | None = None, env: dict | None = None, pool_stats: list | None = None) -> int:
    """Run a command, streaming its output to the console and (optionally) a log file; returns the exit code. Pool statistics
    lines (`[pool] {...}`) are parsed into `pool_stats`."""
    log("$ " + " ".join(cmd))
    out = open(logfile, "a") if logfile else None
    try:
        p = subprocess.Popen(cmd, cwd=cwd, env=env or child_env(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        assert p.stdout is not None
        for line in p.stdout:
            print(line, end="", flush=True)
            if out:
                out.write(line)
            if pool_stats is not None and line.startswith(POOL_PREFIX + "{"):
                try:
                    pool_stats.append(json.loads(line[len(POOL_PREFIX):]))
                except ValueError:
                    pass
        return p.wait()
    finally:
        if out:
            out.close()


# ============================================================================================ devices
def nvidia_smi(args: list[str]) -> str | None:
    """stdout of nvidia-smi, or None when it is missing or fails (no GPU)."""
    try:
        r = subprocess.run(["nvidia-smi", *args], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return r.stdout if r.returncode == 0 else None


def detect_gpus() -> list[dict]:
    """[{index, name, memory_mib}] from nvidia-smi; [] without a usable GPU."""
    out = nvidia_smi(["--query-gpu=index,name,memory.total", "--format=csv,noheader,nounits"])
    gpus = []
    for line in (out or "").splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) == 3 and parts[0].isdigit():
            gpus.append({"index": int(parts[0]), "name": parts[1], "memory_mib": int(float(parts[2])) if parts[2].replace(".", "").isdigit() else None})
    return gpus


def device_plan(gpus: list[dict], cpu_count: int | None, cfg) -> dict:
    """Extra to sync and the pool plan: two workers per GPU (cuda:0, cuda:1, ...), else min(4, cpu count) CPU workers.
    `cfg` supplies POOL_WORKERS_PER_GPU and POOL_MAX_CPU_WORKERS (cvoice.config)."""
    if gpus:
        return {"extra": "gpu", "gpus": [g["name"] for g in gpus], "devices": [f"cuda:{g['index']}" for g in gpus],
                "workers": cfg.POOL_WORKERS_PER_GPU * len(gpus)}
    return {"extra": "cpu", "gpus": [], "devices": ["cpu"], "workers": min(cfg.POOL_MAX_CPU_WORKERS, cpu_count or 1)}


def load_config(project: Path):
    """cvoice.config of the copied project, loaded by path (it needs nothing but the standard library)."""
    spec = importlib.util.spec_from_file_location("cvoice_config", project / "src" / "cvoice" / "config.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def bootstrap() -> None:
    """Copy the project to writable storage, install uv, sync the locked environment (cpu or gpu extra) into a managed Python 3.12."""
    t = time.time()
    LOGS.mkdir(parents=True, exist_ok=True)
    gpus = detect_gpus()
    root = find_project_root(find_mount("cvoice-project"))
    verify_project(root)
    if PROJECT.exists():
        shutil.rmtree(PROJECT)
    shutil.copytree(root, PROJECT)
    log(f"project copied to {PROJECT}")
    prepare_sources(PROJECT)
    plan = device_plan(gpus, os.cpu_count(), load_config(PROJECT))
    STATUS["cpu_count"] = os.cpu_count()
    if sh([sys.executable, "-m", "pip", "install", "--quiet", "--disable-pip-version-check", f"uv=={UV_VERSION}"], LOGS / "bootstrap.log"):
        raise RuntimeError("pip install uv failed")
    if sh([sys.executable, "-m", "uv", "sync", "--locked", "--no-dev", "--group", "build", "--extra", plan["extra"], "--python", PYTHON_VERSION],
          LOGS / "bootstrap.log", PROJECT):
        raise RuntimeError(f"uv sync --locked --extra {plan['extra']} failed")
    STATUS["bootstrap_seconds"] = round(time.time() - t, 1)
    py = VENV / "bin" / "python"
    probe = subprocess.run([str(py), "-c", "import sys, numpy, scipy, torch, torchaudio, parselmouth; print(sys.version.split()[0], numpy.__version__, "
                            "scipy.__version__, torch.__version__, torchaudio.__version__, parselmouth.__version__, torch.cuda.is_available(), "
                            "torch.cuda.device_count())"], capture_output=True, text=True, env=child_env()).stdout.split()
    STATUS["environment"] = dict(zip(("python", "numpy", "scipy", "torch", "torchaudio", "parselmouth"), probe))
    if plan["extra"] == "gpu" and (len(probe) < 8 or probe[6] != "True"):
        plan = {**device_plan([], os.cpu_count(), load_config(PROJECT)), "extra": "gpu", "gpus": plan["gpus"],
                "fallback": "the GPU torch cannot see CUDA: the pool runs on CPU"}
        log(plan["fallback"])
    STATUS["device_plan"] = plan
    for k, v in (("CVOICE_DEVICES", ",".join(plan["devices"])), ("CVOICE_WORKERS", str(plan["workers"]))):
        os.environ.setdefault(k, v)  # an explicit value in the environment wins; child_env() inherits these
    log(f"device plan: extra={plan['extra']} devices={os.environ['CVOICE_DEVICES']} workers={os.environ['CVOICE_WORKERS']} gpus={plan['gpus']}")


# ============================================================================================ stages
def final_requested() -> bool:
    """CVOICE_FINAL=1 / 0 from the environment; FINAL_DEFAULT when it is absent (a Kaggle script kernel has no way to set it)."""
    value = os.environ.get("CVOICE_FINAL")
    return FINAL_DEFAULT if value is None else value == "1"


def stages() -> list[tuple[str, list[str]]]:
    py = str(VENV / "bin" / "python")
    sources = STATUS.get("sources", {}).get("path", str(find_mount("cvoice-sources")))
    det = str(OUT / "models" / "detector.json")
    evaluate = [py, "-m", "cvoice.evaluate", "--dataset", str(DATA), "--models", det, "--cache", str(CACHE), "--out", str(OUT)]
    return [
        ("dataset", [py, "-m", "cvoice.dataset", "build", "--sources", sources, "--out", str(DATA), "--cache", str(CACHE)]),
        ("calibrate", [py, "-m", "cvoice.calibrate", "--dataset", str(DATA), "--cache", str(CACHE), "--out", str(OUT)]),
        ("evaluate", evaluate + (["--final"] if final_requested() else [])),
        ("gallery", [py, "-m", "cvoice.gallery", "--dataset", str(DATA), "--models", det, "--cache", str(CACHE), "--eval", str(OUT / "eval"), "--out", str(OUT)]),
    ]


def seed_final_log() -> None:
    """The record of earlier final evaluations (models/final_evaluations.json of the project dataset) goes beside detector.json,
    where evaluate --final checks it."""
    src = PROJECT / "models" / "final_evaluations.json"
    if src.exists():
        (OUT / "models").mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, OUT / "models" / "final_evaluations.json")
        log("earlier final evaluations carried over from the project dataset")


def stage_numbers(stats: list[dict], seconds: float) -> dict:
    """Clip counts and clips per second of a stage from its pool statistics lines (jobs: prepare / align = recordings aligned,
    emit = full-file emissions, call = clip-generation tasks); GPU memory as the last pool reported it."""
    jobs: dict = {}
    for s in stats:
        for k, v in s.get("jobs", {}).items():
            jobs[k] = jobs.get(k, 0) + v
    clips = jobs.get("prepare", 0) + jobs.get("align", 0)
    mem = next((s["gpu_memory_mib"] for s in reversed(stats) if s.get("gpu_memory_mib")), [])
    return {"jobs": jobs, "clips": clips, "clips_per_second": round(clips / seconds, 3) if seconds > 0 else None, "gpu_memory_mib": mem}


def run_stage(name: str, cmd: list[str]) -> bool:
    forecast = {"dataset": "21–23 min", "calibrate": "19–22 min", "evaluate": "73–87 min with --final, 56–60 min without", "gallery": "1 min"}
    log(f"forecast T4 x2 {name}: {forecast.get(name, '3–4 min packaging/bootstrap')}; based on a measured 101.9 min T4 x2 run plus the test split and the R2 lockbox")
    log(f"=== stage {name}")
    t = time.time()
    stats: list[dict] = []
    code = sh(cmd, LOGS / f"{name}.log", PROJECT, pool_stats=stats)
    seconds = time.time() - t
    entry = {"name": name, "ok": code == 0, "returncode": code, "seconds": round(seconds, 1), **stage_numbers(stats, seconds)}
    STATUS["stages"].append(entry)
    log(f"=== stage {name}: {'ok' if code == 0 else 'FAILED'} in {seconds:.1f} s; {entry['clips']} clips, {entry['clips_per_second']} clips/s, "
        f"GPU memory MiB {entry['gpu_memory_mib']}")
    write_status()
    return code == 0


# ============================================================================================ packaging
def package(parts_dir: Path, sources: list[tuple[str, Path]], limit: int = CHUNK_BYTES) -> list[dict]:
    """Zip the given (archive prefix, directory) trees into chunks of at most `limit` bytes, named
    cvoice-build-part-001.zip ..., and return [{name, bytes, sha256, files}]. A file is never split; room is kept for each
    chunk's central directory."""
    files = [(prefix + "/" + p.relative_to(root).as_posix(), p) for prefix, root in sources if root.exists()
             for p in sorted(root.rglob("*")) if p.is_file()]
    budget = limit - min(256 * 1024, limit // 8)
    parts: list[dict] = []
    state: dict = {"zf": None, "path": None, "files": 0, "bytes": 0}

    def close() -> None:
        if state["zf"] is not None:
            state["zf"].close()
            parts.append({"name": state["path"].name, "bytes": state["path"].stat().st_size, "sha256": sha256_file(state["path"]), "files": state["files"]})
            state["zf"] = None

    for arc, path in files:
        size = path.stat().st_size
        if size + 1024 > budget:
            raise RuntimeError(f"{arc} ({size} bytes) cannot fit a {limit}-byte chunk")
        if state["zf"] is None or state["bytes"] + size + 1024 > budget:
            close()
            state.update(path=parts_dir / f"{ARCHIVE_PREFIX}-{len(parts) + 1:03d}.zip", files=0, bytes=0)
            state["zf"] = zipfile.ZipFile(state["path"], "w", zipfile.ZIP_DEFLATED, compresslevel=6)
        state["zf"].write(path, arc)
        state["zf"].fp.flush()
        state["files"] += 1
        state["bytes"] = state["path"].stat().st_size
    close()
    return parts


def write_sums(directory: Path, names: list[str]) -> None:
    (directory / "SHA256SUMS").write_text("".join(f"{sha256_file(directory / n)}  {n}\n" for n in names))


def finish() -> None:
    """Package whatever exists, then leave only the archives, SHA256SUMS and STATUS.json in the working directory."""
    try:
        for old in WORKING.glob(f"{ARCHIVE_PREFIX}-*.zip"):
            old.unlink()
        sources = [("data/dataset", DATA / "dataset"), ("models", OUT / "models"), ("calibration", OUT / "calibration"), ("eval", OUT / "eval"),
                   ("gallery", OUT / "gallery"), ("logs", LOGS)]
        STATUS["parts"] = package(WORKING, sources)
        manifest = DATA / "dataset" / "manifest.json"
        if manifest.exists():
            STATUS["dataset_counts"] = json.loads(manifest.read_text()).get("counts")
            STATUS["dataset_manifest_sha256"] = sha256_file(manifest)
        det = OUT / "models" / "detector.json"
        if det.exists():
            d = json.loads(det.read_text())
            STATUS["detector"] = {"config_sha256": d["config_sha256"], "h": {r: v["h"] for r, v in d["regimes"].items()},
                                  "pmax_factor": d["report"].get("pmax_factor"),
                                  "gate_violations": {k: len(d["report"][k]["violations"]) for k in ("gates_train", "gates_val")}}
    except Exception:
        STATUS["packaging_error"] = traceback.format_exc()
        log("packaging FAILED\n" + STATUS["packaging_error"])
    STATUS["complete"] = bool(STATUS["stages"]) and all(s["ok"] for s in STATUS["stages"]) and len(STATUS["stages"]) == len(stages()) \
        and "packaging_error" not in STATUS
    STATUS["total_seconds"] = round(time.time() - T0, 1)
    write_status()
    write_sums(WORKING, [p["name"] for p in STATUS["parts"]] + ["STATUS.json"])
    log(f"packaged {len(STATUS['parts'])} chunk(s); complete={STATUS['complete']}")


def main() -> int:
    """Run the stages; always returns 0: the outcome is in STATUS.json."""
    STATUS["final_evaluation"] = final_requested()
    write_status()
    try:
        bootstrap()
        for name, cmd in stages():
            if name == "evaluate" and final_requested():
                seed_final_log()
            if not run_stage(name, cmd):
                STATUS["failed_stages"].append(name)
                STATUS["failed_stage"] = STATUS["failed_stage"] or name
                if name not in CONTINUE_AFTER_FAILURE:
                    break
    except Exception:
        STATUS["failed_stage"] = "bootstrap"
        STATUS["error"] = traceback.format_exc()
        log("bootstrap FAILED\n" + STATUS["error"])
    finish()
    return 0


if __name__ == "__main__":
    main()
    print(f"[run] complete={STATUS['complete']} failed_stage={STATUS['failed_stage']}; exiting 0 (STATUS.json carries the outcome)", flush=True)
    sys.exit(0)
