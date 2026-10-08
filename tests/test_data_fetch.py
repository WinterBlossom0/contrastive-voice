"""Offline checks for the standalone data kernel's nontrivial bookkeeping."""
import importlib.util
import io
import json
import tarfile
import zipfile
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("data_fetch", Path(__file__).parents[1] / "kaggle/data/fetch.py")
fetch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetch)


def test_budget_preserves_priority_and_never_overcommits():
    sources = [{"id": "low", "priority": 2, "reserve": 6},
               {"id": "high", "priority": 1, "reserve": 7},
               {"id": "small", "priority": 2, "reserve": 2}]
    accepted, refused = fetch.budget_sources(sources, 10)
    assert [s["id"] for s in accepted] == ["high", "small"]
    assert [s["id"] for s in refused] == ["low"]
    assert sum(s["reserve"] for s in accepted) <= 10


def test_manifest_records_provenance_and_file_digest(tmp_path):
    p = tmp_path / "audio.wav"
    p.write_bytes(b"test canonical bytes")
    item = {"url": "https://example.test/a.wav", "path": "original.wav", "speaker": "p1",
            "style": "soft", "text": "Hello.", "label_files": ["labels.csv"],
            "licence": "item terms", "licence_url": "https://example.test/licence"}
    entry = fetch.manifest_entry("avid", item, p, 1.2345678, "audio/0.wav")
    assert entry["speaker_id"] == "p1" and entry["condition"] == "soft"
    assert entry["source_url"] == item["url"] and entry["licence"] == "item terms"
    assert entry["duration"] == 1.234568 and entry["sha256"] == fetch.digest(p)
    assert json.loads(json.dumps(entry))["label_files"] == ["labels.csv"]


def test_poetry_repeat_takes_share_one_reader_id():
    assert fetch.ia_speaker("jabberwocky_librivox", "jabberwocky_carroll_add1.mp3") == fetch.ia_speaker(
        "jabberwocky_librivox", "jabberwocky_carroll_add2.mp3")
    assert fetch.ia_speaker("jabberwocky_librivox", "jabberwocky_carroll_sm_2.mp3").endswith(":sm")


def test_tar_is_single_and_padding_is_checked(tmp_path):
    root, out = tmp_path / "source", tmp_path / "out"
    root.mkdir()
    out.mkdir()
    for i in range(3):
        (root / f"{i}.wav").write_bytes(bytes([i]) * 12000)
    with pytest.raises(ValueError, match="one tar"):
        fetch.pack_tar(root, out, "speech", limit=20480)
    assert not list(out.iterdir())
    mapping, parts = fetch.pack_tar(root, out, "speech", limit=51200)
    assert len(parts) == 1 and len(mapping) == 3
    with tarfile.open(out / parts[0]["file"]) as archive:
        for member in archive.getmembers():
            assert archive.extractfile(member).read() == bytes([int(member.name[0])]) * 12000


def test_oversized_file_is_refused_before_tar_write(tmp_path):
    root, out = tmp_path / "source", tmp_path / "out"
    root.mkdir()
    out.mkdir()
    (root / "big.wav").write_bytes(b"x" * 20000)
    with pytest.raises(ValueError, match="cannot fit"):
        fetch.pack_tar(root, out, "speech", limit=10240)
    assert not list(out.iterdir())


def test_dry_plan_from_fake_table_and_resolver_failure(capsys):
    table = [{"id": "a", "priority": 1, "reserve": 100}, {"id": "b", "priority": 2, "reserve": 100}]
    def resolver(source):
        if source["id"] == "b":
            raise OSError("offline")
        return [{"size": 10, "compressed": 4}], [{"size": 2}]
    plan = fetch.dry_plan(table, resolver)
    assert plan[0]["selected_transfer"] == 6 and plan[0]["error"] is None
    assert plan[1]["stage"] == "resolve" and "offline" in plan[1]["error"]
    assert "output-cap=100 B" in capsys.readouterr().out


def test_failure_isolation_including_failed_resolution():
    plans = [{"source": "bad"}, {"source": "unresolved", "stage": "resolve", "error": "403"}, {"source": "good"}]
    def worker(plan):
        if plan["source"] == "bad":
            raise RuntimeError("bad audio")
        return {"source": plan["source"], "complete": True}
    results = fetch.run_sources(plans, worker)
    assert "bad audio" in results[0]["error"]
    assert results[1]["stage"] == "resolve" and results[2]["complete"]


def test_range_zip_extracts_and_checks_crc_across_segments(monkeypatch):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("folder/speech.wav", b"audio" * 500)
    blob = buf.getvalue()
    # The member starts in segment 0 and its compressed data crosses to segment 1.
    cut = 55
    parts = [{"url": "part0", "size": cut}, {"url": "part1", "size": len(blob) - cut}]
    payload = {"part0": blob[:cut], "part1": blob[cut:]}
    monkeypatch.setattr(fetch, "http", lambda url, **kw: (payload[url][kw["start"]:kw["end"] + 1], {}))
    start = blob.index(b"PK\x01\x02")
    stop = blob.index(b"PK\x05\x06")
    item = fetch.zip_directory(blob[start:stop])[0]
    item["parts"] = parts
    assert fetch.zip_member(item) == b"audio" * 500
    item["crc"] ^= 1
    with pytest.raises(ValueError, match="CRC mismatch"):
        fetch.zip_member(item)


def test_source_failure_removes_partial_archive_and_next_source_can_run(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch, "get_item", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("download failed")))
    source = {"id": "avid", "priority": 1, "reserve": 100}
    (tmp_path / "avid-001.tar").write_bytes(b"partial")
    result = fetch.source_fetch(source, [], [{"path": "labels.csv"}], tmp_path)
    assert result["stage"] == "labels" and not result["complete"]
    assert "download failed" in result["error"] and not list(tmp_path.glob("*.tar"))


def test_http_retry_after_paces_the_host_and_logs_failure(monkeypatch):
    import urllib.error
    clock = [0.0]
    monkeypatch.setattr(fetch.time, "monotonic", lambda: clock[0])
    monkeypatch.setattr(fetch.time, "time", lambda: clock[0])
    monkeypatch.setattr(fetch.time, "sleep", lambda n: clock.__setitem__(0, clock[0] + n))
    monkeypatch.setattr(fetch, "HOST_NEXT", {})
    monkeypatch.setattr(fetch, "AUDIT", [])
    class Response(io.BytesIO):
        status = 200
        headers = {"Content-Length": "2"}
        url = "https://zenodo.org/test"
    calls = []
    def open_request(req, timeout):
        calls.append(clock[0])
        if len(calls) == 1:
            raise urllib.error.HTTPError(req.full_url, 429, "limited", {"Retry-After": "61"}, io.BytesIO(b"rate limit"))
        return Response(b"ok")
    monkeypatch.setattr(fetch.OPENER, "open", open_request)
    assert fetch.http("https://zenodo.org/test")[0] == b"ok"
    assert calls[1] - calls[0] >= 61
    assert fetch.AUDIT[0]["status"] == 429 and fetch.AUDIT[0]["response"] == "rate limit"
    assert fetch.AUDIT[0]["retry_wait"] == 61


def test_retry_after_above_budget_never_retries_early(monkeypatch):
    import urllib.error
    monkeypatch.setattr(fetch, "HOST_NEXT", {})
    monkeypatch.setattr(fetch, "AUDIT", [])
    calls = []
    def fail(req, timeout):
        calls.append(req.full_url)
        raise urllib.error.HTTPError(req.full_url, 429, "limited", {"Retry-After": "500"}, io.BytesIO(b"limited"))
    monkeypatch.setattr(fetch.OPENER, "open", fail)
    with pytest.raises(urllib.error.HTTPError):
        fetch.http("https://zenodo.org/test")
    assert len(calls) == 1


def test_merged_ranges_are_reused_and_crc_still_checked(tmp_path, monkeypatch):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("a.wav", b"a" * 500)
        z.writestr("b.wav", b"b" * 500)
    blob = buf.getvalue()
    entries = fetch.zip_directory(blob[blob.index(b"PK\x01\x02"):blob.index(b"PK\x05\x06")])
    part = {"url": "https://zenodo.org/test.zip", "size": len(blob)}
    for e in entries:
        e["parts"] = [part]
    calls = []
    def download(url, **kw):
        calls.append(url)
        kw["target"].write_bytes(blob)
        return b"", {}
    monkeypatch.setattr(fetch, "http", download)
    monkeypatch.setattr(fetch, "RANGE_CACHE", {})
    fetch.prepare_ranges(entries, tmp_path)
    assert len(calls) == 1
    assert [fetch.zip_member(e) for e in entries] == [b"a" * 500, b"b" * 500]
    entries[0]["crc"] ^= 1
    with pytest.raises(ValueError, match="CRC"):
        fetch.zip_member(entries[0])


def test_mirror_revision_mismatch_uses_verified_pinned_blob(tmp_path, monkeypatch):
    expected = b"pinned README\n"
    mirror = tmp_path / "mount"
    mirror.mkdir()
    (mirror / "README.md").write_bytes(b"newer mirror README\n")
    item = {"path": "README.md", "size": len(expected), "url": "https://example.test/pinned",
            "git_sha1": fetch.hashlib.sha1(f"blob {len(expected)}\0".encode() + expected).hexdigest()}
    def download(url, **kw):
        assert url == item["url"]
        kw["target"].write_bytes(expected)
        return b"", {}
    monkeypatch.setattr(fetch, "http", download)
    target = tmp_path / "result"
    fetch.get_item(item, target, mirror)
    assert target.read_bytes() == expected
    item["git_sha1"] = "bad hash"
    with pytest.raises(ValueError, match="Git blob"):
        fetch.get_item(item, target, mirror)


def test_vctk_uses_mirror_copying_and_rainbow_not_stella(tmp_path):
    for n in [1, *range(6, 25), 25]:
        (tmp_path / f"p225_{n:03d}.wav").write_bytes(b"audio")
        (tmp_path / f"p225_{n:03d}.txt").write_text("transcript")
    for n in range(6, 20):
        (tmp_path / f"p264_{n:03d}.wav").write_bytes(b"audio")
        (tmp_path / f"p264_{n:03d}.txt").write_text("transcript")
    (tmp_path / "COPYING").write_text("Creative Commons Attribution 3.0 http://creativecommons.org/licenses/by/3.0/")
    audio, labels = fetch.mounted_audio({"id": "vctk", "mount": "kynthesis/vctk-corpus"}, tmp_path, tmp_path)
    assert len(audio) == 19 and all(x["speaker"] == "p225" for x in audio)
    assert (audio[0]["path"], audio[-1]["path"]) == ("p225_006.wav", "p225_024.wav")
    assert next(x for x in labels if x["path"] == "COPYING")["local"] == str(tmp_path / "COPYING")
    assert all(x["licence"] == "CC BY 3.0" for x in audio)
    (tmp_path / "COPYING").write_text("ODC Attribution License (ODC-By)\n\nThe Licensor ...")
    audio, _ = fetch.mounted_audio({"id": "vctk", "mount": "kynthesis/vctk-corpus"}, tmp_path, tmp_path)
    assert {x["licence"] for x in audio} == {"ODC-By 1.0"}


def test_expresso_parquet_filters_styles_without_overwriting_shard_audio(tmp_path, monkeypatch):
    import sys
    from types import SimpleNamespace
    rows = [{"id": f"ex01_{style}_{i:05d}", "style": style, "speaker_id": "ex01", "text": "read text",
             "audio": {"bytes": bytes([i]), "path": None}}
            for i, style in enumerate(("default", "confused", "emphasis", "enunciated", "default_essentials"))]
    batch = SimpleNamespace(to_pylist=lambda: rows)
    reader = SimpleNamespace(iter_batches=lambda batch_size: [batch])
    pq = SimpleNamespace(ParquetFile=lambda path: reader)
    monkeypatch.setitem(sys.modules, "pyarrow", SimpleNamespace(parquet=pq))
    monkeypatch.setitem(sys.modules, "pyarrow.parquet", pq)
    (tmp_path / "labels").mkdir()
    audio = fetch.parquet_audio(tmp_path / "labels/shard.parquet", tmp_path, None, "expresso", offset=7)
    assert [x["style"] for x in audio] == ["default", "emphasis", "enunciated", "default"]
    assert [(tmp_path / f"parquet-audio-{i}.wav").read_bytes() for i in (7, 8, 9, 10)] == [b"\0", b"\2", b"\3", b"\4"]
    assert all((tmp_path / "labels" / x["label_files"][0]).is_file() for x in audio)
