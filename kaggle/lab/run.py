#!/usr/bin/env python3
"""Private cvoice-lab script kernel. Restage cvoice-project with src/cvoice/lab before pushing.

Bootstrap helpers are copied from kaggle/run.py; source reconstruction is unnecessary here because
cvoice-data supplies the independent research recordings. Uses the same pinned uv, Python, lock,
managed environment, GPU plan, project checksum verification and child process environment.
Local work: use the repository .venv python -m cvoice.lab --local, never this bootstrap.
No kernel push or other Kaggle API operation occurs in this script. Always exits zero; inspect STATUS.json.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import signal
import threading
import time
import traceback
import zipfile

UV_VERSION = "0.12.3"
PYTHON_VERSION = "3.12"
WORKING = Path(os.environ.get("CVOICE_WORKING", "/kaggle/working"))
INPUT = Path(os.environ.get("CVOICE_INPUT", "/kaggle/input"))
TMP = Path("/tmp/cvoice-lab-bootstrap")
VENV = Path("/tmp/cvoice-venv")
PROJECT = TMP / "project"
LOGS = TMP / "logs"
STATUS = {"schema": 1, "complete": False, "stages": []}
POOL_PREFIX = "[pool] "
T0 = time.time()


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


def find_mount(name: str) -> Path:
    """Folder of a mounted dataset. Kaggle mounts at /kaggle/input/<name> or /kaggle/input/datasets/<owner>/<name>."""
    for cand in (INPUT / name, *sorted(INPUT.glob(f"*/*/{name}")), *sorted(INPUT.glob(f"*/{name}"))):
        if cand.is_dir():
            return cand
    return INPUT / name  # not mounted: the caller reports the missing path


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

def merge_data(mounts: list[Path]) -> Path:
    """One data folder for the lab: cvoice-data and cvoice-data-vctk are separate kernel outputs with distinct tar names."""
    if not mounts:
        raise FileNotFoundError('cvoice-data kernel output (manifest.json and source tars) not mounted')
    if len(mounts) == 1:
        return mounts[0]
    merged = Path('/tmp/cvoice-lab-input')
    merged.mkdir(parents=True, exist_ok=True)
    rows, sources = [], []
    for mount in mounts:
        rows += json.loads((mount / 'manifest.json').read_text())
        status = json.loads((mount / 'STATUS.json').read_text())
        sources += status.get('sources', [])
        for tar in mount.glob('*.tar'):
            link = merged / tar.name
            if link.exists():
                raise FileExistsError(f'two data mounts hold {tar.name}')
            link.symlink_to(tar)
    (merged / 'manifest.json').write_text(json.dumps(rows))
    (merged / 'STATUS.json').write_text(json.dumps({'complete': all(s.get('complete') for s in sources), 'sources': sources,
                                                    'mounts': [str(m) for m in mounts]}))
    log(f'merged data mounts {[m.name for m in mounts]}: {len(rows)} manifest rows')
    return merged


def main():
    WORKING.mkdir(parents=True, exist_ok=True)
    try:
        os.environ['CVOICE_LAB_STARTED'] = str(T0)
        bootstrap()
        saved = next(INPUT.rglob('features.npz'), None)
        if saved is not None:  # a mounted earlier lab output: rerun the tests only, no data or GPU needed
            source, budget = ['--features', str(saved)], 11 * 3600
        else:
            data = merge_data(sorted({p.parent for p in INPUT.rglob('manifest.json') if any(p.parent.glob('*-001.tar'))}))
            source, budget = ['--data', str(data)], 3 * 3600
        command = [str(VENV / 'bin' / 'python'), '-m', 'cvoice.lab', *source, '--out', str(WORKING)]
        log('$ ' + ' '.join(command))
        process = subprocess.Popen(command, cwd=PROJECT, env=child_env(), start_new_session=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        def stop():
            STATUS['budget_timeout'] = True
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        timer = threading.Timer(max(1., budget-(time.time()-T0)), stop)
        timer.daemon = True
        timer.start()
        try:
            with (WORKING / 'lab.log').open('a') as logfile:
                for line in process.stdout:
                    print(line, end='', flush=True)
                    logfile.write(line)
            code = process.wait()
        finally:
            timer.cancel()
        child = json.loads((WORKING / 'STATUS.json').read_text())
        STATUS.update(child)
        STATUS['child_returncode'] = code
        STATUS['complete'] = child.get('complete', False) and code == 0
    except Exception:
        STATUS.update(complete=False, error=traceback.format_exc())
        log(STATUS['error'])
    STATUS['total_seconds'] = time.time() - T0
    write_status()
    return 0


if __name__ == '__main__':
    sys.exit(main())
