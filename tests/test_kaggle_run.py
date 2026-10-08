import hashlib
import importlib.util
import io
import json
import subprocess
from types import SimpleNamespace
import zipfile
from email.utils import formatdate
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("kaggle_run", ROOT / "kaggle" / "run.py")
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)


@pytest.fixture(autouse=True)
def download_clock(monkeypatch):
    clock = SimpleNamespace(now=0.0, sleeps=[])

    def sleep(seconds):
        clock.sleeps.append(seconds)
        clock.now += seconds

    monkeypatch.setattr(run, "time", SimpleNamespace(time=run.time.time, monotonic=lambda: clock.now, sleep=sleep))
    monkeypatch.setattr(run, "SOURCE_HOST_READY", {})
    return clock


def test_kernel_metadata_is_the_private_t4x2_script_kernel():
    m = json.loads((ROOT / "kaggle" / "kernel-metadata.json").read_text())
    assert m["id"] == "electroknight/cvoice-build" and m["kernel_type"] == "script" and m["is_private"] is True
    assert m["enable_internet"] is True and m["enable_gpu"] is True and m["machine_shape"] == "NvidiaTeslaT4" and m["code_file"] == "run.py"
    assert m["dataset_sources"] == ["electroknight/cvoice-sources", "electroknight/cvoice-project"]


T4 = "0, Tesla T4, 15360\n1, Tesla T4, 15360\n"


def test_device_plan_from_nvidia_smi_output(monkeypatch):
    cfg = run.load_config(ROOT)  # the real constants: two workers per GPU, at most four CPU workers
    monkeypatch.setattr(run, "nvidia_smi", lambda args: T4)
    gpus = run.detect_gpus()
    assert [g["name"] for g in gpus] == ["Tesla T4", "Tesla T4"] and gpus[1]["memory_mib"] == 15360
    plan = run.device_plan(gpus, 4, cfg)
    assert plan == {"extra": "gpu", "gpus": ["Tesla T4", "Tesla T4"], "devices": ["cuda:0", "cuda:1"], "workers": 4}
    for out in ("", "No devices were found\n", None):  # no GPU, an empty answer, nvidia-smi missing or failing
        monkeypatch.setattr(run, "nvidia_smi", lambda args, out=out: out)
        assert run.detect_gpus() == []
    assert run.device_plan([], 16, cfg) == {"extra": "cpu", "gpus": [], "devices": ["cpu"], "workers": 4}
    assert run.device_plan([], 2, cfg)["workers"] == 2 and run.device_plan([], None, cfg)["workers"] == 1


def test_nvidia_smi_wrapper_survives_a_missing_binary(monkeypatch):
    def boom(*a, **k):
        raise FileNotFoundError("nvidia-smi")
    monkeypatch.setattr(subprocess, "run", boom)
    assert run.nvidia_smi(["-L"]) is None and run.detect_gpus() == []


def test_package_chunks_stay_under_the_limit_and_keep_every_file(tmp_path):
    rng = np.random.default_rng(0)
    src = tmp_path / "src"
    for i in range(12):
        (src / "d").mkdir(parents=True, exist_ok=True)
        (src / "d" / f"f{i}.bin").write_bytes(rng.integers(0, 256, 90_000, dtype=np.uint8).tobytes())  # incompressible
    out = tmp_path / "out"
    out.mkdir()
    limit = 400_000
    parts = run.package(out, [("data", src), ("none", tmp_path / "missing")], limit)
    assert len(parts) >= 3 and all(p["bytes"] <= limit for p in parts)
    names = []
    for p in parts:
        with zipfile.ZipFile(out / p["name"]) as zf:
            assert zf.testzip() is None
            names += zf.namelist()
    assert sorted(names) == sorted(f"data/d/f{i}.bin" for i in range(12))
    run.write_sums(out, [p["name"] for p in parts])
    assert subprocess.run(["sha256sum", "-c", "SHA256SUMS"], cwd=out, capture_output=True).returncode == 0
    with pytest.raises(RuntimeError, match="cannot fit"):
        (src / "big.bin").write_bytes(b"x" * 500_000)
        run.package(out, [("data", src)], limit)


def test_project_root_discovery_and_integrity_check(tmp_path, monkeypatch):
    subprocess.run([str(ROOT / "scripts" / "stage_project.sh"), str(tmp_path / "upload")], check=True, capture_output=True)
    assert (tmp_path / "upload" / "dataset-metadata.json").exists()
    stage = tmp_path / "upload" / "project"
    assert (stage / "pyproject.toml").exists() and (stage / "uv.lock").exists() and (stage / "data" / "sources_manifest.json").exists()
    hashes = json.loads((ROOT / "data" / "transcripts" / "sha256.json").read_text())
    assert len(hashes) == 11  # ten owner snapshots plus the existing Clinton plain text
    assert json.loads((stage / "data" / "transcripts" / "sha256.json").read_text()) == hashes
    for name, expected in hashes.items():
        assert run.sha256_file(ROOT / "data" / "transcripts" / name) == expected
        assert run.sha256_file(stage / "data" / "transcripts" / name) == expected
    assert not list(stage.rglob("*.wav")) and not (stage / ".venv").exists() and not list(stage.rglob("__pycache__"))
    nested = tmp_path / "mount" / "cvoice-project" / "extra" / "layer"
    nested.parent.mkdir(parents=True)
    stage.rename(nested)
    root = run.find_project_root(tmp_path / "mount" / "cvoice-project")
    assert root == nested
    run.verify_project(root)
    (root / "src" / "cvoice" / "config.py").write_text("tampered\n")
    with pytest.raises(RuntimeError, match="differ"):
        run.verify_project(root)
    with pytest.raises(FileNotFoundError):
        run.find_project_root(tmp_path / "mount" / "empty-does-not-exist")


def test_stage_order_and_commands(monkeypatch):
    monkeypatch.delenv("CVOICE_FINAL", raising=False)
    names = [n for n, _ in run.stages()]
    assert names == ["dataset", "calibrate", "evaluate", "gallery"]
    cmds = dict(run.stages())
    assert cmds["dataset"][1:4] == ["-m", "cvoice.dataset", "build"] and "--sources" in cmds["dataset"]
    assert run.child_env()["OMP_NUM_THREADS"] == "1" and run.child_env()["UV_PYTHON_PREFERENCE"] == "only-managed"
    assert "--final" not in cmds["evaluate"]  # the test split stays unseen unless CVOICE_FINAL=1
    monkeypatch.setenv("CVOICE_FINAL", "1")
    assert "--final" in dict(run.stages())["evaluate"] and "--force" not in dict(run.stages())["evaluate"]


def test_final_default_is_off_and_turns_the_final_evaluation_on_only_without_the_environment_variable(monkeypatch):
    assert run.FINAL_DEFAULT is False  # only the staged last run sets it
    monkeypatch.delenv("CVOICE_FINAL", raising=False)
    monkeypatch.setattr(run, "FINAL_DEFAULT", True)
    assert run.final_requested() and "--final" in dict(run.stages())["evaluate"]
    monkeypatch.setenv("CVOICE_FINAL", "0")
    assert not run.final_requested() and "--final" not in dict(run.stages())["evaluate"]
    monkeypatch.setattr(run, "FINAL_DEFAULT", False)
    monkeypatch.setenv("CVOICE_FINAL", "1")
    assert run.final_requested()


def fresh(monkeypatch, tmp_path):
    """Point the runner at temporary folders with an empty STATUS; returns (working, tmp)."""
    work, tmp = tmp_path / "working", tmp_path / "tmp"
    for name, val in (("WORKING", work), ("TMP", tmp), ("PROJECT", tmp / "project"), ("DATA", tmp / "data"), ("OUT", tmp / "out"), ("LOGS", tmp / "out" / "logs")):
        monkeypatch.setattr(run, name, val)
    monkeypatch.setattr(run, "STATUS", {"schema": 1, "complete": False, "failed_stage": None, "failed_stages": [], "stages": [], "parts": []})
    (tmp / "project").mkdir(parents=True)
    (tmp / "out" / "logs").mkdir(parents=True)
    (tmp / "data" / "dataset").mkdir(parents=True)
    (tmp / "data" / "dataset" / "manifest.json").write_text(json.dumps({"counts": {"files": 3}}))
    monkeypatch.setattr(run, "bootstrap", lambda: None)
    return work, tmp


def source_project(monkeypatch, tmp_path):
    project = tmp_path / "project"
    (project / "data" / "transcripts").mkdir(parents=True)
    snapshots = {"pinned.txt": b"Pinned speech.", "pinned.html": b"<p>Unused archived page.</p>",
                 "speech.html": b"<p>Official speech.</p>",
                 "book.txt": b"*** START OF THE PROJECT GUTENBERG EBOOK X ***\nOfficial book.\n*** END OF THE PROJECT GUTENBERG EBOOK X ***"}
    for name, payload in snapshots.items():
        (project / "data" / "transcripts" / name).write_bytes(payload)
    hashes = {name: hashlib.sha256(payload).hexdigest() for name, payload in snapshots.items()}
    (project / "data" / "transcripts" / "sha256.json").write_text(json.dumps(hashes))
    entries = [{"id": f"speaker{i}", "audio_file": f"speaker{i}.mp3", "sha256": hashlib.sha256(b"audio").hexdigest(),
                "download_url": f"https://example.org/{i}.mp3", "transcript": f"transcripts/{name}",
                "transcript_root": origin, "transcript_url": url}
               for i, (name, origin, url) in enumerate([
                   ("speech.html", "sources", "https://example.org/speech"),
                   ("speech.html", "sources", "https://example.org/speech"),
                   ("pinned.txt", "repo", "https://example.org/pinned"),
                   ("book.txt", "sources", "https://www.gutenberg.org/ebooks/4")])]
    (project / "data" / "sources_manifest.json").write_text(json.dumps({"entries": entries}))
    monkeypatch.setattr(run, "INPUT", tmp_path / "input")
    monkeypatch.setattr(run, "TMP", tmp_path / "tmp")
    monkeypatch.setattr(run, "WORKING", tmp_path / "working")
    monkeypatch.setattr(run, "STATUS", {})
    return project, entries


def test_rebuilt_sources_have_the_build_layout_and_retry_without_network(tmp_path, monkeypatch):
    from cvoice import dataset
    project, entries = source_project(monkeypatch, tmp_path)
    calls = []

    def opener(request, timeout, deadline):
        calls.append(request.full_url)
        assert request.full_url.endswith(".mp3"), "transcripts must never be downloaded"
        if len(calls) == 1:
            raise OSError("temporary failure")
        response = io.BytesIO(b"audio")
        response.headers = {}
        return response

    monkeypatch.setattr(run, "open_source", opener)
    root = run.prepare_sources(project)
    monkeypatch.setattr(dataset, "ROOT", project)
    monkeypatch.setattr(dataset, "MANIFEST", project / "data" / "sources_manifest.json")
    for entry in dataset.load_sources_manifest()["entries"]:
        assert dataset.find_source(root, entry["audio_file"]).read_bytes() == b"audio"
        assert dataset.find_source(root, Path(entry["transcript"]).name).is_file()
    assert dataset.official_text(entries[0], root) == "Official speech."
    assert dataset.official_text(entries[2], root) == "Pinned speech."
    assert dataset.official_text(entries[3], root).strip() == "Official book."
    assert calls == [entries[0]["download_url"], *(e["download_url"] for e in entries)]
    hashes = json.loads((project / "data" / "transcripts" / "sha256.json").read_text())
    for name, expected in hashes.items():
        assert run.sha256_file(root / "transcripts" / name) == expected
    status = json.loads((run.WORKING / "STATUS.json").read_text())["sources"]
    assert status["route"] == "rebuilt from origins" and len(status["checks"]) == 8
    assert status["transcript_source"] == "repository snapshot"
    assert all(c["match"] for c in status["checks"])
    checks = [c for c in status["checks"] if c.get("origin") == "repository snapshot"]
    assert {c["file"]: c["expected_sha256"] for c in checks} == hashes
    assert all(c["url"] is None for c in checks)
    assert dict(run.stages())["dataset"][5] == str(root)


def test_present_sources_mount_skips_download_even_when_nested(tmp_path, monkeypatch):
    project, entries = source_project(monkeypatch, tmp_path)
    mount = run.INPUT / "datasets" / "friend" / "cvoice-sources"
    (mount / "nested").mkdir(parents=True)
    for entry in entries:
        (mount / "nested" / entry["audio_file"]).write_bytes(b"audio")
        (mount / "nested" / Path(entry["transcript"]).name).write_bytes((project / "data" / entry["transcript"]).read_bytes())
    monkeypatch.setattr(run, "open_source", lambda *a, **k: pytest.fail("mounted route downloaded"))
    assert run.prepare_sources(project) == mount
    assert run.STATUS["sources"]["route"] == "mounted"
    assert all(c["match"] for c in run.STATUS["sources"]["checks"] if c["expected_sha256"])


def test_source_download_exhausts_three_attempts_and_honours_retry_after(tmp_path, monkeypatch, download_clock):
    project, _ = source_project(monkeypatch, tmp_path)
    attempts = []

    def opener(request, timeout, deadline):
        attempts.append(download_clock.now)
        raise run.urllib.error.HTTPError(request.full_url, 429, "rate limited", {"Retry-After": "60"}, None)

    monkeypatch.setattr(run, "open_source", opener)
    with pytest.raises(RuntimeError, match="speaker0: download failed after 3 attempts"):
        run.prepare_sources(project)
    assert attempts == [0, 60, 120] and download_clock.sleeps == [60, 60]
    assert "429" in run.STATUS["sources"]["checks"][-1]["error"]
    assert not (run.TMP / "sources" / "speaker0.mp3").exists()


@pytest.mark.parametrize("retry_after", [" 30 ", formatdate(1_700_000_030, usegmt=True)])
def test_source_429_waits_then_succeeds_and_sends_user_agent(tmp_path, monkeypatch, download_clock, retry_after):
    project, _ = source_project(monkeypatch, tmp_path)
    attempts = []
    monkeypatch.setattr(run.time, "time", lambda: 1_700_000_000)

    def opener(request, timeout, deadline):
        attempts.append(download_clock.now)
        assert request.get_header("User-agent") == run.SOURCE_USER_AGENT
        assert "ContrastiveVoice" in run.SOURCE_USER_AGENT and "https://" in run.SOURCE_USER_AGENT
        assert request.get_header("Accept-encoding") == "identity"
        if len(attempts) == 1:
            raise run.urllib.error.HTTPError(request.full_url, 429, "rate limited", {"Retry-After": retry_after}, None)
        response = io.BytesIO(b"audio")
        response.headers = {"Content-Length": "5"}
        return response

    monkeypatch.setattr(run, "open_source", opener)
    run.prepare_sources(project)
    assert attempts[:2] == [0, 30]
    assert download_clock.sleeps[0] == 30
    assert all(check["match"] for check in run.STATUS["sources"]["checks"])


def test_source_host_interval_is_shared_between_entries_but_not_hosts(tmp_path, monkeypatch, download_clock):
    _, entries = source_project(monkeypatch, tmp_path)
    run.STATUS["sources"] = {"checks": []}
    calls = []

    def opener(request, timeout, deadline):
        calls.append((request.host, download_clock.now))
        response = io.BytesIO(b"audio")
        response.headers = {}
        return response

    monkeypatch.setattr(run, "open_source", opener)
    for entry, url in zip(entries, ["https://example.org/a", "https://other.org/b", "https://example.org/c"]):
        run.download_source(entry, url, tmp_path / entry["audio_file"], entry["sha256"])
    assert calls == [("example.org", 0), ("other.org", 0), ("example.org", run.SOURCE_HOST_INTERVAL)]
    assert download_clock.sleeps == [run.SOURCE_HOST_INTERVAL]


def test_source_fallback_after_primary_failure_keeps_the_hash_check(tmp_path, monkeypatch, download_clock):
    project, entries = source_project(monkeypatch, tmp_path)
    fallback = "https://other.org/identical.mp3"
    monkeypatch.setattr(run, "SOURCE_FALLBACK_URLS", {"speaker0": (fallback,)})
    calls = []

    def opener(request, timeout, deadline):
        calls.append(request.full_url)
        if request.full_url == entries[0]["download_url"]:
            raise OSError("primary unavailable")
        response = io.BytesIO(b"audio")
        response.headers = {}
        return response

    monkeypatch.setattr(run, "open_source", opener)
    root = run.prepare_sources(project)
    assert calls[:4] == [entries[0]["download_url"]] * 3 + [fallback]
    assert (root / entries[0]["audio_file"]).read_bytes() == b"audio"
    check = next(c for c in run.STATUS["sources"]["checks"] if c["entry"] == "speaker0")
    assert check["url"] == fallback and check["match"] is True
    assert all(c["match"] for c in run.STATUS["sources"]["checks"])


@pytest.mark.parametrize("retry_after,expected_attempts,expected_wait", [("600", 2, 600), ("601", 1, 0)])
def test_source_retry_deadline_never_shortens_retry_after(tmp_path, monkeypatch, download_clock,
                                                        retry_after, expected_attempts, expected_wait):
    project, _ = source_project(monkeypatch, tmp_path)
    attempts = []

    def opener(request, timeout, deadline):
        attempts.append(download_clock.now)
        raise run.urllib.error.HTTPError(request.full_url, 429, "rate limited", {"Retry-After": retry_after}, None)

    monkeypatch.setattr(run, "open_source", opener)
    with pytest.raises(RuntimeError, match="speaker0: download failed"):
        run.prepare_sources(project)
    assert len(attempts) == expected_attempts and sum(download_clock.sleeps) == expected_wait
    assert sum(download_clock.sleeps) <= run.SOURCE_RETRY_SECONDS


def test_source_redirect_obeys_target_cooldown_and_preserves_user_agent(monkeypatch, download_clock):
    request = run.urllib.request.Request("http://commons.example/file", headers={"User-Agent": run.SOURCE_USER_AGENT})
    target = "http://upload.wikimedia.org/file"
    run.SOURCE_HOST_READY["upload.wikimedia.org"] = 60
    calls = []
    build_opener = run.urllib.request.build_opener

    class Origin(run.urllib.request.HTTPHandler):
        def http_open(self, req):
            calls.append((req.full_url, download_clock.now, req.get_header("User-agent")))
            code = 302 if req.full_url == request.full_url else 200
            response = run.urllib.response.addinfourl(io.BytesIO(b"audio"), {"location": target}, req.full_url, code)
            response.msg = "Found" if code == 302 else "OK"
            return response

    monkeypatch.setattr(run.urllib.request, "build_opener", lambda redirect: build_opener(Origin(), redirect))
    with run.open_source(request, timeout=120, deadline=600) as response:
        assert response.read() == b"audio"
    assert calls == [(request.full_url, 0, run.SOURCE_USER_AGENT), (target, 60, run.SOURCE_USER_AGENT)]
    assert download_clock.sleeps == [60]


def test_wikimedia_media_copy_limits_bandwidth_including_redirects(monkeypatch, download_clock):
    response = io.BytesIO(b"x" * (64 * 1024 * 2 + 17))
    response.geturl = lambda: "https://upload.wikimedia.org/file"
    output = io.BytesIO()
    run.copy_source(response, output, "https://commons.wikimedia.org/redirect")
    assert output.getvalue() == response.getvalue()
    assert len(download_clock.sleeps) == 3
    assert download_clock.now == pytest.approx(len(output.getvalue()) / 2_500_000)


@pytest.mark.parametrize("error", [OSError("connection failed"), TimeoutError("socket timed out")])
def test_source_network_error_and_bad_retry_after_use_backoff(tmp_path, monkeypatch, download_clock, error):
    project, _ = source_project(monkeypatch, tmp_path)
    attempts = []

    def opener(request, timeout, deadline):
        attempts.append(download_clock.now)
        if len(attempts) == 1:
            raise error
        if len(attempts) == 2:
            raise run.urllib.error.HTTPError(request.full_url, 429, "rate limited", {"Retry-After": "invalid"}, None)
        response = io.BytesIO(b"audio")
        response.headers = {}
        return response

    monkeypatch.setattr(run, "open_source", opener)
    run.prepare_sources(project)
    assert attempts[:3] == [0, 5, 15]


def test_source_hash_mismatch_stops_run_names_entry_and_preserves_status(tmp_path, monkeypatch):
    work, _ = fresh(monkeypatch, tmp_path)
    project, _ = source_project(monkeypatch, tmp_path)
    monkeypatch.setattr(run, "WORKING", work)
    monkeypatch.setattr(run, "STATUS", {"stages": [], "parts": [], "failed_stages": [], "failed_stage": None})

    def opener(*args, **kwargs):
        response = io.BytesIO(b"changed recording")
        response.headers = {}
        return response

    monkeypatch.setattr(run, "SOURCE_FALLBACK_URLS", {"speaker0": ("https://other.org/unused",)})
    calls = []

    def checked_opener(request, **kwargs):
        calls.append(request.full_url)
        return opener()

    monkeypatch.setattr(run, "open_source", checked_opener)
    monkeypatch.setattr(run, "bootstrap", lambda: run.prepare_sources(project))
    monkeypatch.setattr(run, "run_stage", lambda *a: pytest.fail("build ran after a hash mismatch"))
    assert run.main() == 0
    status = json.loads((work / "STATUS.json").read_text())
    assert status["complete"] is False and status["failed_stage"] == "bootstrap"
    assert "speaker0: SHA-256 mismatch" in status["error"]
    assert calls == ["https://example.org/0.mp3"]
    assert status["sources"]["checks"][-1]["match"] is False
    assert not (run.TMP / "sources" / "speaker0.mp3").exists()


@pytest.mark.parametrize("name", ["speech.html", "book.txt", "pinned.txt", "pinned.html"])
def test_transcript_hash_mismatch_stops_run_names_file_and_preserves_status(tmp_path, monkeypatch, name):
    work, _ = fresh(monkeypatch, tmp_path)
    project, _ = source_project(monkeypatch, tmp_path)
    monkeypatch.setattr(run, "WORKING", work)
    monkeypatch.setattr(run, "STATUS", {"stages": [], "parts": [], "failed_stages": [], "failed_stage": None})
    (project / "data" / "transcripts" / name).write_text("Changed transcript.")
    monkeypatch.setattr(run, "open_source", lambda *a, **k: pytest.fail("download after transcript mismatch"))
    monkeypatch.setattr(run, "bootstrap", lambda: run.prepare_sources(project))
    monkeypatch.setattr(run, "run_stage", lambda *a: pytest.fail("build ran after transcript mismatch"))
    assert run.main() == 0
    status = json.loads((work / "STATUS.json").read_text())
    assert status["complete"] is False and status["failed_stage"] == "bootstrap"
    assert f"transcript SHA-256 mismatch for {name}" in status["error"]
    assert status["sources"]["transcript_source"] == "repository snapshot"
    check = next(c for c in status["sources"]["checks"] if c["file"] == name)
    assert check["match"] is False and check["sha256"] != check["expected_sha256"]


def test_transcript_without_recorded_hash_stops_rebuild(tmp_path, monkeypatch):
    project, _ = source_project(monkeypatch, tmp_path)
    path = project / "data" / "transcripts" / "sha256.json"
    hashes = json.loads(path.read_text())
    del hashes["speech.html"]
    path.write_text(json.dumps(hashes))
    monkeypatch.setattr(run, "open_source", lambda *a, **k: pytest.fail("download without transcript hash"))
    with pytest.raises(RuntimeError, match="no repository transcript SHA-256 recorded for speech.html"):
        run.prepare_sources(project)


def test_main_stops_at_a_failing_dataset_stage_still_packages_and_exits_zero(tmp_path, monkeypatch):
    import sys
    work, tmp = fresh(monkeypatch, tmp_path)
    py = sys.executable
    monkeypatch.setattr(run, "stages", lambda: [("one", [py, "-c", "print('stage one')"]), ("two", [py, "-c", "import sys; print('boom'); sys.exit(3)"]),
                                                 ("three", [py, "-c", "print('never')"])])
    assert run.main() == 0  # always 0: a non-zero exit may discard the outputs; STATUS.json carries the outcome
    st = json.loads((work / "STATUS.json").read_text())
    assert [s["name"] for s in st["stages"]] == ["one", "two"] and st["failed_stage"] == "two" and st["failed_stages"] == ["two"] and st["complete"] is False
    assert st["stages"][1]["returncode"] == 3 and st["dataset_counts"] == {"files": 3} and st["stages"][0]["seconds"] >= 0
    assert st["dataset_manifest_sha256"] == run.sha256_file(tmp / "data" / "dataset" / "manifest.json")
    assert (tmp / "out" / "logs" / "one.log").read_text().strip() == "stage one" and not (tmp / "out" / "logs" / "three.log").exists()
    assert subprocess.run(["sha256sum", "-c", "SHA256SUMS"], cwd=work, capture_output=True).returncode == 0
    with zipfile.ZipFile(work / st["parts"][0]["name"]) as zf:
        assert {"logs/one.log", "logs/two.log", "data/dataset/manifest.json"} <= set(zf.namelist())
    assert sorted(p.name for p in work.iterdir()) == sorted([*(p["name"] for p in st["parts"]), "SHA256SUMS", "STATUS.json"])


def test_a_failing_evaluate_stage_does_not_skip_the_gallery_and_stage_numbers_come_from_the_pool_lines(tmp_path, monkeypatch):
    import sys
    work, tmp = fresh(monkeypatch, tmp_path)
    py = sys.executable
    pool_line = ('print(\'[pool] {"jobs": {"prepare": 30, "align": 10, "emit": 4}, "gpu_memory_mib": '
                 '[{"index": 0, "used": 1200, "total": 15360}, {"index": 1, "used": 1100, "total": 15360}]}\')')
    monkeypatch.setattr(run, "stages", lambda: [("dataset", [py, "-c", pool_line]), ("calibrate", [py, "-c", "print('ok')"]),
                                                 ("evaluate", [py, "-c", "import sys; sys.exit(1)"]), ("gallery", [py, "-c", "print('gallery ran')"])])
    assert run.main() == 0
    st = json.loads((work / "STATUS.json").read_text())
    assert [s["name"] for s in st["stages"]] == ["dataset", "calibrate", "evaluate", "gallery"]
    assert st["failed_stage"] == "evaluate" and st["failed_stages"] == ["evaluate"] and st["complete"] is False and st["stages"][3]["ok"]
    d = st["stages"][0]
    assert d["jobs"] == {"prepare": 30, "align": 10, "emit": 4} and d["clips"] == 40 and d["clips_per_second"] > 0
    assert [m["used"] for m in d["gpu_memory_mib"]] == [1200, 1100] and st["stages"][1]["clips"] == 0 and st["stages"][1]["gpu_memory_mib"] == []


def test_a_bootstrap_failure_is_recorded_and_still_exits_zero(tmp_path, monkeypatch):
    work, tmp = fresh(monkeypatch, tmp_path)
    monkeypatch.setattr(run, "bootstrap", lambda: (_ for _ in ()).throw(RuntimeError("uv sync --locked --extra gpu failed")))
    monkeypatch.setattr(run, "stages", lambda: [])
    assert run.main() == 0
    st = json.loads((work / "STATUS.json").read_text())
    assert st["failed_stage"] == "bootstrap" and "extra gpu" in st["error"] and st["complete"] is False


def test_the_earlier_final_evaluation_record_is_carried_beside_the_detector(tmp_path, monkeypatch):
    work, tmp = fresh(monkeypatch, tmp_path)
    run.seed_final_log()  # nothing staged: nothing to carry
    assert not (tmp / "out" / "models").exists()
    (tmp / "project" / "models").mkdir()
    (tmp / "project" / "models" / "final_evaluations.json").write_text('{"abc": {"runs": 1}}\n')
    run.seed_final_log()
    assert json.loads((tmp / "out" / "models" / "final_evaluations.json").read_text()) == {"abc": {"runs": 1}}


def test_project_zip_fallback_rebuilds_the_layout(tmp_path, monkeypatch):
    """Kaggle --dir-mode zip: one zip per top-level folder next to the loose files; the zips do not carry their folder name."""
    monkeypatch.setattr(run, "TMP", tmp_path / "tmp")
    mount = tmp_path / "mount" / "cvoice-project"
    mount.mkdir(parents=True)
    for name, files in (("src", {"cvoice/__init__.py": "x\n", "cvoice/config.py": "y\n"}), ("data", {"sources_manifest.json": "{}\n"})):
        with zipfile.ZipFile(mount / f"{name}.zip", "w") as zf:
            for rel, text in files.items():
                zf.writestr(rel, text)
    with zipfile.ZipFile(mount / "extra.zip", "w") as zf:  # a zip that already carries its own folder name unpacks in place
        zf.writestr("extra/readme.txt", "z\n")
    (mount / "pyproject.toml").write_text("[project]\nname='x'\n")
    (mount / "uv.lock").write_text("lock\n")
    root = run.find_project_root(mount)
    assert (root / "pyproject.toml").exists() and (root / "uv.lock").exists() and (root / "src" / "cvoice" / "config.py").exists()
    assert (root / "data" / "sources_manifest.json").exists() and (root / "extra" / "readme.txt").exists() and not list(root.glob("*.zip"))
