"""Dashboard server: upload guards, job flow with a stubbed pipeline, static files, and the Pages site builder.
A real uvicorn server runs in a thread on a free port; the model never loads (analyze is replaced)."""
import asyncio
import json
import socket
import threading
import time
import urllib.error
import urllib.request
import uuid
from types import SimpleNamespace

import numpy as np
import pytest
import uvicorn

from cvoice import app as appmod, audio, config as C, gallery, repair
from cvoice.align import MISMATCH_PART, MISMATCH_SHORT, TranscriptMismatch

TEXT = "we hold these truths to be self evident. That all men are created equal."
BANK_TEXT = "We are met on a great battlefield of that war. We have come to dedicate a portion of that field."


def tone(seconds=2.0):
    t = np.arange(int(seconds * C.SR)) / C.SR
    return audio.quantize(0.3 * np.sin(2 * np.pi * 150 * t))


@pytest.fixture
def server(tmp_path, monkeypatch):
    g = tmp_path / "gallery"
    (g / "audio").mkdir(parents=True)
    audio.write_wav(g / "audio" / "base.wav", tone())
    for k in range(6):   # bank readings of different lengths, so the test can tell them apart
        audio.write_wav(g / "audio" / f"bank{k}.wav", tone(1.0 + 0.1 * k))
    single = {"id": "base", "title": "Base", "audio": "audio/base.wav", "text": TEXT}
    bank = {"id": "bank", "title": "Bank", "audio": "audio/bank0.wav", "text": BANK_TEXT, "mode": "bank",
            "references": [{"id": f"bank{k}", "reader": f"Reader {k}", "audio": f"audio/bank{k}.wav", "licence": "LibriVox public domain"} for k in range(6)]}
    (g / "index.json").write_text(json.dumps({"schema": 1, "baseline": single, "baselines": [{**single, "mode": "single"}, bank], "items": []}))
    det = tmp_path / "detector.json"
    det.write_text("{}")
    seen = {}

    def fake_analyze(mine, tr, ref=None, *, regime, participant_meta, progress, refuse_mismatch, cache_dir, detector=None, baseline_meta=None,
                     references=None):
        for stage in ("align", "features", "compare", "detect"):
            progress(stage)
        seen.update(regime=regime, words=len(tr), mine=len(mine), baseline=(baseline_meta or {}).get("id"), refuse=refuse_mismatch,
                    ref=None if ref is None else len(ref), references=None if references is None else [len(x) for x in references])
        if regime == "SELF":
            detection = {"reference_mode": "none", "reference_count": 0, "references_available": 0}
        else:
            mode = "consensus5" if references and len(references) >= C.CONSENSUS_K else "single"
            detection = {"reference_mode": mode, "reference_count": C.CONSENSUS_K if mode == "consensus5" else 1,
                         "references_available": len(references or [ref])}
        return {"schema": 2, "regime": regime, "participant": participant_meta, "baseline": baseline_meta or {"duration": 2.0}, "detection": detection,
                "flaws": [{"id": "d1-001", "dimension": "D1"}, {"id": "d5-002", "dimension": "D5"}], "scores": {"overall": 90.0}}

    monkeypatch.setattr(appmod, "analyze", fake_analyze)
    monkeypatch.setattr(appmod, "load_detector", lambda path: {})
    monkeypatch.setattr(C, "MAX_UPLOAD_BYTES", 400_000)
    with socket.socket() as sock:  # uvicorn cannot report a port chosen by the OS, so pick a free one first
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    srv = uvicorn.Server(uvicorn.Config(appmod.create_app(g, det, tmp_path / "work"), host="127.0.0.1", port=port, log_level="warning"))
    th = threading.Thread(target=srv.run, daemon=True)
    th.start()
    while not srv.started:
        time.sleep(0.01)
    yield f"http://127.0.0.1:{port}", seen, tmp_path
    srv.should_exit = True
    th.join(5)


def multipart(fields):
    """fields: {name: str | (filename, bytes)}, or a list of (name, value) pairs to repeat a name -> (body, content type)."""
    b = uuid.uuid4().hex
    out = b""
    for name, v in (fields.items() if isinstance(fields, dict) else fields):
        if isinstance(v, tuple):
            out += f'--{b}\r\nContent-Disposition: form-data; name="{name}"; filename="{v[0]}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode() + v[1] + b"\r\n"
        else:
            out += f'--{b}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{v}\r\n'.encode()
    return out + f"--{b}--\r\n".encode(), f"multipart/form-data; boundary={b}"


def call(url, fields=None, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    if fields is not None:
        body, ctype = multipart(fields)
        req = urllib.request.Request(url, data=body, headers={"Content-Type": ctype, **(headers or {})})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, r.read(), r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers


def wav_bytes(tmp_path, name="u.wav", seconds=2.0):
    audio.write_wav(tmp_path / name, tone(seconds))
    return (tmp_path / name).read_bytes()


def own_references(tmp_path, count):
    """count reference uploads of different lengths (1.0, 1.1, ... s), so a test can tell them apart and check their order."""
    return [("baseline_audio", (f"r{k}.wav", wav_bytes(tmp_path, f"r{k}.wav", 1.0 + 0.1 * k))) for k in range(count)]


def wait_done(base, jid):
    for _ in range(300):
        s, body, _ = call(f"{base}/api/jobs/{jid}")
        job = json.loads(body)
        if job["state"] in ("done", "error"):
            return job
        time.sleep(0.05)
    raise AssertionError("job did not finish")


def post_json(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def fake_repair(monkeypatch, gate: threading.Event | None = None) -> list:
    """Replaces the repair calls of app.run_fix with fast stand-ins: the first finding of a fix is applied and removed, any
    other one is unfixable. gate: the fix waits for it, so a test can hold a fix job running. Returns the calls made."""
    calls = []

    def outcome(result, wav, flaws):
        fixes = [repair.Fix(f["id"], f["dimension"], "RUSH", repair.APPLIED, "stretch", 0.8, 0.8, share=1.0) if k == 0 else
                 repair.Fix(f["id"], f["dimension"], "FADE", repair.UNFIXABLE, None, None, None, "record these words again.") for k, f in enumerate(flaws)]
        return SimpleNamespace(audio=wav[: len(wav) // 2], fixes=fixes)

    def fix_finding(result, wav, index, *, pitch_method, transcript):
        if gate is not None:
            gate.wait(10)
        calls.append(("one", index, pitch_method, transcript))
        return outcome(result, wav, [result["flaws"][index]])

    def fix_all(result, wav, *, pitch_method, transcript):
        calls.append(("all", None, pitch_method, transcript))
        return outcome(result, wav, result["flaws"])

    def verify(out, result, kwargs):
        calls.append(("verify", sorted(k for k, v in kwargs.items() if v is not None)))
        first = out.fixes[0].finding
        return {"score_before": 90.0, "score": 95.0, "reproduced": True, "removed": [first], "new_findings": [],
                "remaining": [{"id": f["id"], "now": []} for f in result["flaws"] if f["id"] != first],
                "null_chain": {"within_tolerance": True}, "pitch_check": [], "alignment": {"words_off": []}}

    monkeypatch.setattr(appmod.repair, "fix_finding", fix_finding)
    monkeypatch.setattr(appmod.repair, "fix_all", fix_all)
    monkeypatch.setattr(appmod.repair, "verify", verify)
    monkeypatch.setattr(appmod.repair, "listen_pairs", lambda out, context_s: [
        {"finding": out.fixes[0].finding, "original": [0.5, 1.0], "edited": [0.5, 0.8], "original_context": [0, 1.5], "edited_context": [0, 1.3]}])
    return calls


def finished_analysis(base, tmp, **fields):
    s, body, _ = call(f"{base}/api/analyze", {"audio": ("a.wav", wav_bytes(tmp)), "transcript": TEXT, **fields})
    assert s == 200, body
    jid = json.loads(body)["job_id"]
    assert wait_done(base, jid)["state"] == "done"
    return jid


def test_health_static_and_gallery(server):
    base, _, _ = server
    h = json.loads(call(f"{base}/api/health")[1])
    assert h["ok"] and h["analysis"]["available"] and h["limits"]["max_seconds"] == C.MAX_UPLOAD_S
    assert h["limits"]["max_references"] == C.CONSENSUS_K == 5   # the page copy says "five"
    assert h["limits"]["max_total_bytes"] == appmod.max_request_bytes() and h["flag_limits"] == {}   # the stub detector has no regimes
    assert b"Contrastive Voice" in call(f"{base}/")[1]
    assert json.loads(call(f"{base}/gallery/index.json")[1])["baseline"]["id"] == "base"
    assert call(f"{base}/gallery/..%2f..%2fetc/passwd")[0] == 404


def test_upload_runs_as_r2_and_serves_decoded_audio(server):
    base, seen, tmp = server
    s, body, _ = call(f"{base}/api/analyze", {"audio": ("../../evil.wav", wav_bytes(tmp)), "transcript": TEXT, "baseline_id": "base"})
    assert s == 200
    jid = json.loads(body)["job_id"]
    job = wait_done(base, jid)
    assert job["state"] == "done" and job["stages"] == list(appmod.STAGES)
    assert seen["regime"] == "R2" and seen["baseline"] == "base" and seen["words"] == 14 and seen["refuse"] is True  # uploads refuse a mismatch
    assert seen["references"] is None and job["reference"] == {"reference_mode": "single", "reference_count": 1, "references_available": 1}
    res = json.loads(call(f"{base}{'/' + job['result']}")[1])
    assert res["participant"]["audio"] == f"api/jobs/{jid}/participant.wav" and res["baseline"]["audio"] == "gallery/audio/base.wav"
    s, data, hdr = call(f"{base}/api/jobs/{jid}/participant.wav", headers={"Range": "bytes=0-99"})
    assert s == 206 and len(data) == 100
    assert not (tmp / "evil.wav").exists() and not list((tmp / "work" / jid).glob("*recording*"))   # raw uploads are deleted


def test_uploaded_baseline_is_served_back(server):
    base, seen, tmp = server
    audio_b = wav_bytes(tmp)
    s, body, _ = call(f"{base}/api/analyze", {"audio": ("a.wav", audio_b), "transcript": TEXT, "baseline_audio": ("b.wav", audio_b)})
    jid = json.loads(body)["job_id"]
    assert wait_done(base, jid)["state"] == "done" and seen["baseline"] == "uploaded_baseline" and seen["references"] is None
    assert call(f"{base}/api/jobs/{jid}/baseline.wav")[0] == 200


def test_bank_choice_passes_every_reading_and_states_consensus_mode(server):
    base, seen, tmp = server
    s, body, _ = call(f"{base}/api/analyze", {"audio": ("a.wav", wav_bytes(tmp)), "transcript": BANK_TEXT, "baseline_id": "bank"})
    assert s == 200, body
    job = wait_done(base, json.loads(body)["job_id"])
    assert job["state"] == "done" and seen["baseline"] == "bank"
    assert seen["references"] == [int((1.0 + 0.1 * k) * C.SR) for k in range(6)] and seen["ref"] == seen["references"][0]   # bank order, exemplar first
    assert job["reference"] == {"reference_mode": "consensus5", "reference_count": 5, "references_available": 6}
    res = json.loads(call(f"{base}/{job['result']}")[1])
    assert res["baseline"]["audio"] == "gallery/audio/bank0.wav" and res["detection"]["reference_mode"] == "consensus5"


@pytest.mark.parametrize("count,mode", [(5, "consensus5"), (3, "single")])
def test_own_reference_bank_is_passed_in_upload_order(server, count, mode):
    base, seen, tmp = server
    fields = [("audio", ("a.wav", wav_bytes(tmp))), ("transcript", TEXT), *own_references(tmp, count)]
    s, body, _ = call(f"{base}/api/analyze", fields)
    assert s == 200, body
    jid = json.loads(body)["job_id"]
    job = wait_done(base, jid)
    assert job["state"] == "done" and seen["baseline"] == "uploaded_baseline" and seen["regime"] == "R2"
    assert seen["references"] == [int((1.0 + 0.1 * k) * C.SR) for k in range(count)] and seen["ref"] == seen["references"][0]   # exemplar first
    assert job["reference"]["reference_mode"] == mode and job["reference"]["references_available"] == count
    (tmp / "served.wav").write_bytes(call(f"{base}/api/jobs/{jid}/baseline.wav")[1])
    assert len(audio.read_wav(tmp / "served.wav")) == seen["ref"]   # the page plays the first reference
    assert not list((tmp / "work" / jid).glob("*recording*"))


def test_too_many_own_references_are_refused_in_plain_words(server):
    base, seen, tmp = server
    fields = [("audio", ("a.wav", wav_bytes(tmp))), ("transcript", TEXT), *own_references(tmp, appmod.MAX_REFERENCES + 1)]
    s, body, _ = call(f"{base}/api/analyze", fields)
    assert s == 422 and json.loads(body)["detail"] == "Upload at most 5 reference recordings of the same text."
    assert not seen


def test_each_file_and_the_whole_request_are_size_limited(server):
    base, _, _ = server
    over = [("audio", ("a.wav", b"RIFF" + b"\0" * C.MAX_UPLOAD_BYTES)), ("transcript", TEXT), ("baseline_id", "base")]
    s, body, _ = call(f"{base}/api/analyze", over)   # one file above the per-file limit, the request under the total
    assert s == 413 and json.loads(body)["detail"] == f"Your recording is larger than {C.MAX_UPLOAD_BYTES // 2**20} MB."
    total = appmod.max_request_bytes()
    assert total == C.MAX_UPLOAD_BYTES * (1 + appmod.MAX_REFERENCES)   # room for every file of a full upload at its own limit
    reply = declared_length_reply(base, total + 1)
    assert reply.startswith(b"HTTP/1.1 413") and f"{total // 2**20} MB".encode() in reply


def test_flag_limits_match_the_result_rows_of_the_frozen_detector():
    """The health endpoint's smallest flagged changes per mode equal the row thresholds that the pipeline writes for that mode."""
    from pathlib import Path
    from cvoice.pipeline import DEFAULT_DETECTOR, ROOT
    limits = appmod.upload_limits(DEFAULT_DETECTOR)
    assert set(limits) == {"single", "consensus5"} and all(set(v) == set(appmod.LIMIT_ROWS.values()) for v in limits.values())
    assert limits["consensus5"]["pace"][0] < limits["single"]["pace"][0]   # five readings flag a smaller rush
    assert appmod.upload_limits(Path("missing.json")) == {}
    for name, mode in (("r2_consensus", "consensus5"), ("greenman_botched", "single")):
        path = ROOT / "gallery" / "results" / f"{name}.json"
        if not path.exists():
            continue
        result = json.loads(path.read_text())
        if result["detection"].get("reference_mode") != mode:
            continue
        rows = {r["key"]: r["tol"] for r in result["rows"]}
        assert {k: rows[k] for k in appmod.LIMIT_ROWS.values()} == limits[mode]


@pytest.mark.parametrize("baseline_id,title,text", [("bank", "Bank", TEXT), ("base", "Base", BANK_TEXT)])
def test_bundled_references_refuse_another_text_up_front_in_the_same_words(server, baseline_id, title, text):
    base, seen, tmp = server
    s, body, _ = call(f"{base}/api/analyze", {"audio": ("a.wav", wav_bytes(tmp)), "transcript": text, "baseline_id": baseline_id})
    assert (s, json.loads(body)["detail"]) == (
        422, f"The transcript is not the text of the reference '{title}'. Use that text, or choose another reference.")
    assert not seen


def test_index_without_a_baselines_list_offers_its_one_baseline(tmp_path):
    (tmp_path / "index.json").write_text(json.dumps({"baseline": {"id": "base", "title": "Base", "audio": "audio/base.wav", "text": TEXT}}))
    assert list(appmod.bundled_baselines(tmp_path)) == ["base"]


@pytest.mark.parametrize("fields,status", [
    ({"audio": ("a.m3u", b"#EXTM3U\nhttp://example.com/x\n"), "transcript": TEXT, "baseline_id": "base"}, 415),   # sniffed, never named
    ({"audio": ("a.wav", b"RIFF"), "transcript": "  ", "baseline_id": "base"}, 422),                               # empty transcript
    ({"audio": ("a.wav", b"RIFF"), "transcript": "meet at 10:30 am", "baseline_id": "base"}, 422),             # cannot be spelled (10:30)
    ({"audio": ("a.wav", b"RIFF"), "transcript": TEXT, "baseline_id": "base", "baseline_audio": ("b.wav", b"RIFF")}, 422),  # both
    ({"audio": ("a.wav", b"RIFF"), "transcript": TEXT, "baseline_id": "other"}, 422),                              # unknown baseline
    ({"audio": ("a.wav", b"RIFF"), "baseline_id": "base"}, 422),                                                   # no transcript at all
])
def test_upload_refusals(server, fields, status):
    base, _, _ = server
    s, body, _ = call(f"{base}/api/analyze", fields)
    assert s == status, body
    assert json.loads(body)["detail"]


def declared_length_reply(base, length):
    """The reply to a POST that sends only its headers: a refusal can come from the declared length alone."""
    host, port = base.removeprefix("http://").split(":")
    with socket.create_connection((host, int(port))) as c:
        c.sendall(f"POST /api/analyze HTTP/1.1\r\nHost: x\r\nContent-Type: multipart/form-data; boundary=b\r\nContent-Length: {length}\r\n\r\n".encode())
        c.settimeout(10)
        reply = b""
        chunk = c.recv(4096)
        while chunk:  # the server closes the connection; headers and body can arrive in separate packets
            reply += chunk
            chunk = c.recv(4096)
    return reply


def test_oversize_body_is_413_before_it_is_read_and_unknown_job_404(server):
    base, _, _ = server
    reply = declared_length_reply(base, 999999999)
    assert reply.startswith(b"HTTP/1.1 413") and b"MB" in reply
    assert call(f"{base}/api/jobs/{'0' * 32}")[0] == 404
    assert call(f"{base}/api/jobs/{'0' * 32}/participant.wav")[0] == 404


def test_decode_failure_becomes_a_plain_job_error(server):
    base, _, _ = server
    s, body, _ = call(f"{base}/api/analyze", {"audio": ("a.wav", b"RIFF....WAVEjunk"), "transcript": TEXT, "baseline_id": "base"})
    job = wait_done(base, json.loads(body)["job_id"])
    assert job["state"] == "error" and job["stage"] == "decode"   # the stage that failed
    assert job["error"] == "Your recording could not be read as audio. Use wav, mp3, m4a, ogg, flac or webm."


def failed_upload(base, tmp, monkeypatch, error, fields):
    """The job error when the stubbed pipeline raises `error`."""
    def refuse(*args, **kwargs):
        raise error
    monkeypatch.setattr(appmod, "analyze", refuse)
    s, body, _ = call(f"{base}/api/analyze", {"audio": ("a.wav", wav_bytes(tmp)), "transcript": TEXT, **fields})
    assert s == 200, body
    job = wait_done(base, json.loads(body)["job_id"])
    assert job["state"] == "error"
    return job["error"]


CHECK_TEXT = "Check that the transcript is the exact text you read."


@pytest.mark.parametrize("error,fields,expected", [
    (TranscriptMismatch("baseline recording: x (mean word compatibility 0.035 < 0.1); participant recording: y",
                        roles=("baseline", "participant")), {"baseline_id": "base"},
     f"The words in your recording do not match the transcript. {CHECK_TEXT} The reference reading does not match the transcript either."),
    (TranscriptMismatch("participant recording: 249 frames < 467 needed", MISMATCH_SHORT, 467 * C.CTC_FRAME_S, ("participant",)), {},
     f"Your recording is too short for this transcript: at least 10 seconds of speech is needed. {CHECK_TEXT}"),
    (TranscriptMismatch("baseline recording: x", roles=("baseline",)), {"baseline_id": "base"},
     "The transcript is not the text of the reference 'Base'. Use that text, or choose another reference."),
    (TranscriptMismatch("participant recording: extra evidence 250 nats", MISMATCH_PART, roles=("participant",), at_s=12.4,
                        near="his family live"), {},
     f"Part of the transcript does not match your recording (at about 12 s, near 'his family live'). {CHECK_TEXT}"),
    (TranscriptMismatch("baseline recording: x; participant recording: y", roles=("baseline", "participant")),
     {"baseline_audio": ("b.wav", b"")},
     f"The words in your recording do not match the transcript. {CHECK_TEXT} Your reference recording does not match the transcript either."),
    (TranscriptMismatch("baseline recording: x", roles=("baseline",)), {"baseline_audio": ("b.wav", b"")},
     f"The words in your reference recording do not match the transcript. {appmod.TRANSCRIPT_HINT}"),
    (RuntimeError("index 7 is out of bounds"), {}, appmod.ANALYSIS_FAILED),
])
def test_analysis_errors_name_the_input_in_plain_words(server, monkeypatch, error, fields, expected):
    base, _, tmp = server
    if "baseline_audio" in fields:
        fields = {"baseline_audio": ("b.wav", wav_bytes(tmp, "b.wav"))}
    message = failed_upload(base, tmp, monkeypatch, error, fields)
    assert message == expected
    assert not any(term in message for term in ("compatibility", "frames", "participant", "baseline", "Error", "index 7"))


@pytest.mark.parametrize("kind,expected", [
    (audio.TOO_LONG, f"Your recording is longer than {C.MAX_UPLOAD_S:.0f} s. Use a recording of {C.MAX_UPLOAD_S:.0f} s or less."),
    (audio.TOO_SHORT, "Your recording is shorter than 1 s. Upload a recording of the whole text."),
    (audio.CHANNELS, "Your recording has more than two channels. Use a mono or stereo recording."),
    (audio.UNREADABLE, "Your recording could not be read as audio. Use wav, mp3, m4a, ogg, flac or webm."),
])
def test_audio_refusals_in_plain_words(kind, expected):
    assert appmod.audio_words(audio.AudioError("your recording: technical detail", kind), "Your recording") == expected
    assert appmod.upload_label("reference recording 2") == "Your reference recording 2"


def test_transcript_refusal_in_plain_words(server):
    base, _, _ = server
    s, body, _ = call(f"{base}/api/analyze", {"audio": ("a.wav", b"RIFF"), "transcript": "meet at 10:30 am", "baseline_id": "base"})
    assert (s, json.loads(body)["detail"]) == (422, "The transcript has '10:30', which cannot be read aloud as written. Write it in words.")


def test_report_pdf_is_served_and_named_in_health(server, monkeypatch, tmp_path):
    base, _, _ = server
    h = json.loads(call(f"{base}/api/health")[1])
    assert h["report_url"] == appmod.REPORT_URL == "report" and appmod.REPORT_PDF.is_file()
    s, data, hdr = call(f"{base}/{h['report_url']}")
    assert s == 200 and hdr["content-type"] == "application/pdf" and data.startswith(b"%PDF")
    assert hdr["content-disposition"].startswith("inline")
    monkeypatch.setattr(appmod, "REPORT_PDF", tmp_path / "missing.pdf")
    assert json.loads(call(f"{base}/api/health")[1])["report_url"] is None
    assert call(f"{base}/report")[0] == 404


def test_stage_names_are_plain_words(server):
    base, _, tmp = server
    h = json.loads(call(f"{base}/api/health")[1])
    assert set(h["stage_labels"]) == {*appmod.STAGES, *appmod.FIX_STAGES}
    jid = finished_analysis(base, tmp, baseline_id="base")
    job = json.loads(call(f"{base}/api/jobs/{jid}")[1])
    assert list(job["stage_labels"]) == job["stages"] == list(appmod.STAGES)
    assert all(label[:1].isupper() for label in job["stage_labels"].values())


def test_chunked_body_over_the_cap_is_refused():
    sent = []

    async def inner(scope, receive, send):
        while (await receive())["more_body"]:
            pass

    async def run():
        msgs = iter([{"type": "http.request", "body": b"x" * 60, "more_body": True}, {"type": "http.request", "body": b"x" * 60, "more_body": False}])

        async def receive():
            return next(msgs)

        async def send(m):
            sent.append(m)

        await appmod.BodySizeLimit(inner, 100)({"type": "http", "method": "POST", "headers": []}, receive, send)

    with pytest.raises(appmod.StarletteHTTPException) as e:
        asyncio.run(run())
    assert e.value.status_code == 413


def test_site_builder_copies_page_and_gallery(tmp_path):
    g = tmp_path / "g"
    (g / "results").mkdir(parents=True)
    (g / "index.json").write_text("{}")
    (g / "results" / "x.json").write_text("{}")
    out = tmp_path / "pages"
    gallery.main(["site", str(out), "--gallery", str(g)])
    assert (out / "index.html").exists() and (out / "app.js").exists() and (out / "vendor" / "plotly-cartesian.min.js").exists()
    assert (out / "gallery" / "results" / "x.json").exists() and (out / ".nojekyll").exists()
    assert json.loads((out / "gallery" / "index.json").read_text()) == {"static_mode": True, "report_url": "technical.pdf"}
    assert (out / "technical.pdf").read_bytes() == appmod.REPORT_PDF.read_bytes() and (g / "index.json").read_text() == "{}"
    gallery.site(out, g, tmp_path / "missing.pdf")
    assert json.loads((out / "gallery" / "index.json").read_text())["report_url"] is None and not (out / "technical.pdf").exists()
    with pytest.raises(FileNotFoundError):
        gallery.site(tmp_path / "again", tmp_path / "nothing")


def test_dashboard_script_copies_of_python_strings():
    """app.js matches finding texts and labels exactly, so its copies must equal the Python sources."""
    import re
    from pathlib import Path
    from cvoice import explain
    script = (Path(appmod.__file__).parent / "static" / "app.js").read_text()

    def literal(name):
        return re.search(rf'^const {name} = "([^"]*)";', script, re.M).group(1)

    assert literal("CANDIDATE_TEXT") == explain.CANDIDATE_CLAUSE
    assert literal("SYNTHETIC_TEXT") == explain.SYNTHETIC_ONLY_CLAUSE
    rows = re.search(r"^const LIMIT_ROWS = (\[.*\]);", script, re.M).group(1)
    assert json.loads(rows) == list(appmod.LIMIT_ROWS.values())
    stages = re.search(r"showStages\((\[[^\]]*\]), \"decode\"\)", script).group(1)
    assert tuple(json.loads(stages)) == appmod.STAGES
    fix_stages = re.search(r"^const FIX_STAGES = (\[.*\]);", script, re.M).group(1)
    assert tuple(json.loads(fix_stages)) == appmod.FIX_STAGES
    assert re.search(r'^const SELF_MODE = "([^"]*)";', script, re.M).group(1) == "none"   # pipeline.analyze_self reference_mode


def test_upload_without_a_reference_runs_the_self_mode(server):
    base, seen, tmp = server
    s, body, _ = call(f"{base}/api/analyze", {"audio": ("a.wav", wav_bytes(tmp)), "transcript": TEXT})
    assert s == 200, body
    jid = json.loads(body)["job_id"]
    job = wait_done(base, jid)
    assert job["state"] == "done" and job["kind"] == "analysis" and seen["regime"] == "SELF" and seen["ref"] is None and seen["baseline"] is None
    assert job["reference"] == {"reference_mode": "none", "reference_count": 0, "references_available": 0}
    res = json.loads(call(f"{base}/{job['result']}")[1])
    assert res["regime"] == "SELF" and res["participant"]["audio"] == f"api/jobs/{jid}/participant.wav"
    assert call(f"{base}/api/jobs/{jid}/baseline.wav")[0] == 404   # no reference audio to serve
    h = json.loads(call(f"{base}/api/health")[1])
    assert h["self"]["available"] and h["fix"] == {"available": True, "examples": []}


@pytest.mark.parametrize("body,kind", [({"finding": 1}, "one"), ({"all": True}, "all")])
def test_fix_job_lifecycle(server, monkeypatch, body, kind):
    base, _, tmp = server
    calls = fake_repair(monkeypatch)
    jid = finished_analysis(base, tmp, baseline_id="base")
    s, made = post_json(f"{base}/api/jobs/{jid}/fix", body)
    assert s == 200, made
    job = wait_done(base, made["job_id"])
    assert job["state"] == "done" and job["kind"] == "fix" and job["stages"] == list(appmod.FIX_STAGES), job
    assert calls[0] == (kind, 1 if kind == "one" else None, "own", TEXT)
    assert calls[1] == ("verify", ["baseline", "cache_dir", "detector", "transcript"])   # the analysis's own inputs
    fix = job["fix"]
    assert fix["score_before"] == 90.0 and fix["score_after"] == 95.0 and fix["checks_passed"] and fix["new_findings"] == 0
    assert fix["mode"] == "reference" and fix["caution"] is None and fix["score_change"] == 5.0 and fix["score_change_note"] is None
    assert [c["name"] for c in fix["checks"]] == ["reproduced", "alignment"] and all(c["passed"] and c["label"] for c in fix["checks"])
    assert "placebo" not in json.dumps(fix)
    assert fix["target"] == ("d5-002" if kind == "one" else "all")
    outcomes = {f["finding"]: (f["outcome"], f["reason"]) for f in fix["fixes"]}
    if kind == "one":
        assert outcomes == {"d5-002": ("no_longer_flagged", "")}
    else:
        assert outcomes == {"d1-001": ("no_longer_flagged", ""), "d5-002": ("unfixable", "Record these words again.")}
        assert fix["counts"] == {"no_longer_flagged": 1, "still_flagged": 0, "unfixable": 1, "skipped": 0, "partial": 0, "floor_removed": 0}
    assert all(set(f) >= CONTRACT_FIX_FIELDS for f in fix["fixes"])
    assert fix["listen"][0]["edited_context"] == [0, 1.3]
    assert job["audio"] == f"api/jobs/{made['job_id']}/fixed.wav"
    s, data, hdr = call(f"{base}/{job['audio']}")
    assert s == 200 and hdr["content-type"] == "audio/wav"
    (tmp / "fixed.wav").write_bytes(data)
    assert len(audio.read_wav(tmp / "fixed.wav")) == int(2.0 * C.SR) // 2
    assert call(f"{base}/api/jobs/{made['job_id']}/result.json")[0] == 404   # a fix job has no analysis result


def test_fix_of_a_self_result_reanalyses_without_a_reference(server, monkeypatch):
    base, _, tmp = server
    calls = fake_repair(monkeypatch)
    jid = finished_analysis(base, tmp)
    s, reply = post_json(f"{base}/api/jobs/{jid}/fix", {"all": True, "pitch_method": "contour"})
    assert (s, reply["detail"]) == (422, appmod.CONTOUR_SELF_WORDS) and not calls   # no reference melody without a reference
    s, made = post_json(f"{base}/api/jobs/{jid}/fix", {"all": True})
    assert s == 200
    job = wait_done(base, made["job_id"])
    assert job["state"] == "done"
    assert calls == [("all", None, "own", TEXT), ("verify", ["cache_dir", "transcript"])]
    fix = job["fix"]
    assert fix["mode"] == "self" and fix["caution"] == appmod.SELF_CAUTION and fix["score_change"] is None
    assert fix["score_change_note"] == appmod.SELF_SCORE_WORDS and fix["flags_before"] == 2
    assert not any(f["alt_pitch_available"] for f in fix["fixes"])


def test_one_job_at_a_time_for_analysis_and_fix(server, monkeypatch):
    base, _, tmp = server
    gate = threading.Event()
    fake_repair(monkeypatch, gate)
    jid = finished_analysis(base, tmp, baseline_id="base")
    s, made = post_json(f"{base}/api/jobs/{jid}/fix", {"finding": 0})
    assert s == 200
    try:
        s, busy = post_json(f"{base}/api/jobs/{jid}/fix", {"all": True})
        assert s == 429 and busy["detail"] == appmod.BUSY
        s, body, _ = call(f"{base}/api/analyze", {"audio": ("a.wav", wav_bytes(tmp)), "transcript": TEXT, "baseline_id": "base"})
        assert s == 429 and json.loads(body)["detail"] == appmod.BUSY
        assert json.loads(call(f"{base}/api/jobs/{made['job_id']}")[1])["state"] in ("queued", "running")
    finally:
        gate.set()
    assert wait_done(base, made["job_id"])["state"] == "done"
    s, again = post_json(f"{base}/api/jobs/{jid}/fix", {"all": True})   # the queue is free again
    assert s == 200 and wait_done(base, again["job_id"])["state"] == "done"


@pytest.mark.parametrize("body,status,detail", [
    ({"finding": 2}, 422, "This analysis has no finding number 2."),
    ({"finding": -1}, 422, "This analysis has no finding number -1."),
    ({}, 422, 'Send either {"finding": <number>} or {"all": true}.'),
    ({"finding": 0, "all": True}, 422, 'Send either {"finding": <number>} or {"all": true}.'),
])
def test_bad_fix_requests_are_refused_in_plain_words(server, monkeypatch, body, status, detail):
    base, _, tmp = server
    calls = fake_repair(monkeypatch)
    jid = finished_analysis(base, tmp, baseline_id="base")
    s, reply = post_json(f"{base}/api/jobs/{jid}/fix", body)
    assert (s, reply["detail"]) == (status, detail) and not calls


def test_fix_needs_a_finished_analysis_and_a_known_example(server, monkeypatch):
    base, _, tmp = server
    fake_repair(monkeypatch)
    assert post_json(f"{base}/api/jobs/{'0' * 32}/fix", {"all": True})[0] == 404
    s, body, _ = call(f"{base}/api/analyze", {"audio": ("a.wav", b"RIFF....WAVEjunk"), "transcript": TEXT, "baseline_id": "base"})
    jid = json.loads(body)["job_id"]
    assert wait_done(base, jid)["state"] == "error"
    s, reply = post_json(f"{base}/api/jobs/{jid}/fix", {"all": True})
    assert s == 409 and reply["detail"] == "Only a finished analysis can be fixed."
    s, reply = post_json(f"{base}/api/gallery/nope/fix", {"all": True})
    assert s == 404 and reply["detail"] == "Unknown example."
    assert post_json(f"{base}/api/gallery/..%2fx/fix", {"all": True})[0] >= 400   # never reaches the file system


def test_gallery_source_finds_the_bundled_text_and_bank(tmp_path):
    g = tmp_path
    (g / "results").mkdir()
    for name in ("one", "bank", "other"):
        (g / "results" / f"{name}.json").write_text(json.dumps({"regime": "R2" if name == "bank" else "R1"}))
    bank = {"id": "bank", "title": "Bank", "audio": "audio/r0.wav", "text": BANK_TEXT, "references": [{"id": f"r{k}", "audio": f"audio/r{k}.wav"} for k in range(3)]}
    items = [{"id": "one", "baseline": "base", "audio": "audio/one.wav", "result": "results/one.json"},
             {"id": "bank", "baseline": "r0", "audio": "audio/bank.wav", "result": "results/bank.json"},
             {"id": "other", "baseline": "elsewhere", "audio": "audio/other.wav", "result": "results/other.json"}]
    (g / "index.json").write_text(json.dumps({"baselines": [{"id": "base", "title": "Base", "audio": "audio/base.wav", "text": TEXT}, bank], "items": items}))
    one, banked, other = (appmod.gallery_source(g, it) for it in items)
    assert one == appmod.FixSource(g / "audio/one.wav", g / "results/one.json", TEXT, "R1", g / "audio/base.wav", None)
    assert banked.references == tuple(g / f"audio/r{k}.wav" for k in range(3)) and banked.baseline == g / "audio/r0.wav" and banked.regime == "R2"
    assert other is None and appmod.fixable_examples(g) == ["one", "bank"]
    (g / "results" / "own.json").write_text(json.dumps({"regime": "SELF", "baseline": {"duration": 2.0}}))
    (g / "results" / "texted.json").write_text(json.dumps({"regime": "R1", "baseline": {"audio": "audio/far.wav"}}))
    own = appmod.gallery_source(g, {"id": "own", "audio": "audio/one.wav", "result": "results/own.json", "text": TEXT})
    texted = appmod.gallery_source(g, {"id": "texted", "baseline": "far", "audio": "audio/t.wav", "result": "results/texted.json", "text": TEXT})
    assert own == appmod.FixSource(g / "audio/one.wav", g / "results/own.json", TEXT, "SELF")
    assert texted == appmod.FixSource(g / "audio/t.wav", g / "results/texted.json", TEXT, "R1", g / "audio/far.wav")


CONTRACT_FIX_FIELDS = {"finding", "status", "outcome", "reason", "detail", "share", "covered_by", "flagged_after", "residual",
                       "residual_share", "unit", "floor_removed", "alt_pitch_available", "limit", "round"}


def test_plain_outcome_of_each_fix_status():
    def fix(status, reason="", share=None, cause="", finding="d1-001"):
        return repair.Fix(finding, "D1", "RUSH", status, None, None, None, reason, share, cause=cause)
    capped = fix(repair.CAPPED, "partial fix: ...", 0.52, repair.CAP)
    partial = "52% of the change toward the target was applied. " + appmod.CAUSE_WORDS[repair.CAP]
    assert appmod.plain_outcome(fix(repair.APPLIED, share=1.0), {"d1-001"}) == ("no_longer_flagged", "")
    assert appmod.plain_outcome(capped, {"d1-001"}) == ("no_longer_flagged", partial)   # gone, but only part of the change
    assert appmod.plain_outcome(capped, set()) == ("still_flagged", partial)
    assert appmod.plain_outcome(fix(repair.APPLIED, share=1.0), set()) == ("still_flagged", appmod.STILL_FLAGGED_WORDS)
    assert appmod.plain_outcome(fix(repair.SKIPPED, cause=repair.INAUDIBLE), set()) == ("skipped", appmod.CAUSE_WORDS[repair.INAUDIBLE])
    assert appmod.plain_outcome(fix(repair.SKIPPED, cause=repair.SHARED_CAP), set()) == ("skipped", appmod.CAUSE_WORDS[repair.SHARED_CAP])
    assert appmod.plain_outcome(fix(repair.SKIPPED, cause=repair.FLAT_PITCH), set()) == (
        "skipped", "Your pitch here is too flat to widen enough within natural limits.")
    assert appmod.plain_outcome(fix(repair.UNFIXABLE, "clarity cannot be edited."), set()) == ("unfixable", "Clarity cannot be edited.")
    tiny = fix(repair.CAPPED, "partial fix: ...", 0.023, repair.CAP)   # 2 % of the change: not heard, so not an edit to hear
    assert appmod.plain_outcome(tiny, set()) == ("skipped", appmod.CAUSE_WORDS[repair.INAUDIBLE])
    assert appmod.plain_outcome(tiny, {"d1-001"})[0] == "no_longer_flagged"   # a measured removal is still reported
    assert appmod.plain_outcome(fix(repair.CAPPED, "", appmod.MIN_HEARD_SHARE, repair.CAP), set())[0] == "still_flagged"
    small_owner = fix(repair.CAPPED, share=0.05, cause=repair.CAP, finding="d5-005")
    assert appmod.plain_outcome(fix(repair.COVERED), set(), small_owner) == ("skipped", appmod.CAUSE_WORDS[repair.INAUDIBLE])
    owner = fix(repair.CAPPED, share=0.53, cause=repair.CAP, finding="d5-005")
    assert appmod.plain_outcome(fix(repair.COVERED), {"d1-001"}, owner) == (
        "no_longer_flagged", "The edit of d5-005 also changes this spot; it applied 53% of its change.")
    texts = [*appmod.CAUSE_WORDS.values(), *appmod.LIMIT_WORDS.values(), appmod.SELF_CAUTION, *appmod.CHECK_LABELS.values()]
    assert not any("would sound" in t or "sounds natural" in t or "placebo" in t.lower() for t in texts)


def summary_of(monkeypatch, fixes, report, result, mode="reference", pitch_method="own"):
    monkeypatch.setattr(appmod.repair, "listen_pairs", lambda out, context_s: [])
    return appmod.fix_summary(SimpleNamespace(audio=np.zeros(C.SR), fixes=fixes), report, None, result, mode, pitch_method)


def test_fix_summary_contract(monkeypatch):
    """Residual, floor removals, the reference-melody offer, covered shares and the score change against the checks."""
    flaws = [{"id": "d3-001", "dimension": "D3", "words": [2, 4], "delta": -1.8, "unit": "ln", "context": "s"},
             {"id": "d2-002", "dimension": "D2", "words": [5, 6], "delta": 0.9, "unit": "s", "context": "s"},
             {"id": "d5-003", "dimension": "D5", "words": [6, 8], "delta": -12.0, "unit": "dB", "context": "s", "counted": True},
             {"id": "d4-004", "dimension": "D4", "words": [7, 7], "delta": -2.0, "unit": "p", "context": "s", "counted": False}]
    result = {"regime": "R2", "flaws": flaws}
    after = {"flaws": [{"id": "x"}], "differences": [],
             "rows": [{"key": "volume", "p": [0.0] * 6 + [-2.0, -5.5, -1.0]}, {"key": "pauses", "p": [None] * 8},
                      {"key": "pitch_range", "p": [None, None, -1.2, -1.0, -0.9]}]}
    fixes = [repair.Fix("d3-001", "D3", "MONOTONE", repair.SKIPPED, "pitch_scale", 2.0, None, "skipped: ...", 0.0, cause=repair.FLAT_PITCH),
             repair.Fix("d2-002", "D2", "PAUSE_LONG", repair.APPLIED, "pause_shorten", 0.2, 0.2, "", 1.0),
             repair.Fix("d5-003", "D5", "FADE", repair.CAPPED, "gain", 12.0, 6.0, "partial fix: ...", 0.5, cause=repair.CAP),
             repair.Fix("d4-004", "D4", "FADE", repair.COVERED, None, None, None, "its penalty is charged to d5-003; ...")]
    report = {"score_before": 80.0, "score": 90.0, "reproduced": True, "removed": ["d2-002", "d5-003", "d4-004"], "new_findings": [],
              "remaining": [{"id": "d3-001", "now": []}], "null_chain": {"within_tolerance": True},
              "pitch_check": [{"agree": True}], "alignment": {"words_off": []}, "result": after}
    fix = summary_of(monkeypatch, fixes, report, result)
    by = {f["finding"]: f for f in fix["fixes"]}
    assert by["d3-001"]["outcome"] == "skipped" and by["d3-001"]["alt_pitch_available"] and by["d3-001"]["residual"] == -1.2
    assert by["d2-002"]["floor_removed"] and by["d2-002"]["residual"] is None and by["d2-002"]["reason"] == appmod.FLOOR_WORDS
    assert by["d5-003"]["outcome"] == "no_longer_flagged" and by["d5-003"]["share"] == 0.5 and by["d5-003"]["residual"] == -5.5
    assert by["d5-003"]["residual_share"] == round(5.5 / 12, 3) and by["d5-003"]["limit"] == appmod.LIMIT_WORDS["gain"]
    assert by["d4-004"]["covered_by"] == "d5-003" and by["d4-004"]["share"] == 0.5 and "50%" in by["d4-004"]["reason"]
    assert fix["counts"]["partial"] == 2 and fix["counts"]["floor_removed"] == 1 and fix["flags_after"] == 1
    assert [c["name"] for c in fix["checks"]] == ["reproduced", "alignment", "pitch_trackers"] and fix["score_change"] == 10.0
    contour = summary_of(monkeypatch, fixes, report, result, pitch_method="contour")
    assert not any(f["alt_pitch_available"] for f in contour["fixes"])   # the melody was already the reference's
    unreproduced = summary_of(monkeypatch, fixes, {**report, "reproduced": False}, result)
    assert unreproduced["score_change"] is None and unreproduced["score_change_note"] == appmod.NOT_REPRODUCED_WORDS
    assert not unreproduced["checks"][0]["passed"] and not unreproduced["checks_passed"]
    drifted = summary_of(monkeypatch, fixes, {**report, "null_chain": {"within_tolerance": False}}, result)
    assert drifted["score_change"] is None   # the null chain is part of the reproduction check
    own = summary_of(monkeypatch, fixes, report, result, mode="self")
    assert own["score_change"] is None and own["caution"] == appmod.SELF_CAUTION
    assert not any(f["alt_pitch_available"] for f in own["fixes"])


def test_shipped_gallery_self_example_and_item_texts():
    """The SELF example sits beside its reference version, and every item text reads the words of its result."""
    from cvoice.align import parse_transcript
    from cvoice.pipeline import ROOT
    g = ROOT / "gallery"
    items = {it["id"]: it for it in json.loads((g / "index.json").read_text())["items"]}
    own, ref = items["L3A_self"], items["L3A"]
    assert own["reference_version"] == "L3A" and ref["self_version"] == "L3A_self" and own["audio"] == ref["audio"]
    result = json.loads((g / own["result"]).read_text())
    assert own["regime"] == result["regime"] == "SELF" and result["detection"]["reference_mode"] == "none"
    assert (own["overall"], own["n_flaws"], own["truth"]) == (result["scores"]["overall"], len(result["flaws"]), len(result["truth"]))
    for item in (it for it in items.values() if it.get("text")):
        words = [w["w"] for w in json.loads((g / item["result"]).read_text())["words"]]
        assert list(parse_transcript(item["text"]).disp) == words, item["id"]
    assert {"L3A_self", "natural_rush"} <= set(appmod.fixable_examples(g))


@pytest.mark.slow
def test_real_fix_of_a_gallery_example(tmp_path):
    """The real repair and re-analysis of gallery L3A: one finding and all of them, served as audio."""
    from cvoice.pipeline import ROOT
    g = ROOT / "gallery"
    if not (g / "results" / "L3A.json").exists():
        pytest.skip("no gallery")
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    srv = uvicorn.Server(uvicorn.Config(appmod.create_app(g, work=tmp_path / "work"), host="127.0.0.1", port=port, log_level="warning"))
    th = threading.Thread(target=srv.run, daemon=True)
    th.start()
    while not srv.started:
        time.sleep(0.01)
    base = f"http://127.0.0.1:{port}"
    try:
        assert "L3A" in json.loads(call(f"{base}/api/health")[1])["fix"]["examples"]
        stored = json.loads((g / "results" / "L3A.json").read_text())
        for body in ({"finding": 0}, {"all": True}):
            s, made = post_json(f"{base}/api/gallery/L3A/fix", body)
            assert s == 200, made
            job = None
            for _ in range(1200):
                job = json.loads(call(f"{base}/api/jobs/{made['job_id']}")[1])
                if job["state"] in ("done", "error"):
                    break
                time.sleep(0.25)
            assert job["state"] == "done", job
            fix = job["fix"]
            assert fix["checks"][0] == {"name": "reproduced", "passed": True, "label": appmod.CHECK_LABELS["reproduced"]}
            assert fix["score_before"] == stored["scores"]["overall"]
            assert {f["finding"] for f in fix["fixes"]} == ({stored["flaws"][0]["id"]} if "finding" in body else {f["id"] for f in stored["flaws"]})
            assert all(f["outcome"] in ("no_longer_flagged", "still_flagged", "unfixable", "skipped") for f in fix["fixes"])
            if "all" in body:
                assert fix["score_after"] > fix["score_before"] and fix["listen"]
            s, data, hdr = call(f"{base}/{job['audio']}")
            assert s == 200 and data[:4] == b"RIFF"
    finally:
        srv.should_exit = True
        th.join(5)


@pytest.mark.parametrize("error,count,expected", [
    (TranscriptMismatch("reference 3 recording: missing evidence 140 nats", MISMATCH_PART, roles=("reference 3",), at_s=4.2,
                        near="a portion of that"), 3,
     f"Part of the transcript does not match your reference recording 3 (at about 4 s, near 'a portion of that'). {appmod.TRANSCRIPT_HINT}"),
    (TranscriptMismatch("baseline recording: x", roles=("baseline",)), 2,
     f"The words in your reference recording 1 do not match the transcript. {appmod.TRANSCRIPT_HINT}"),
    (TranscriptMismatch("reference 2 recording: 249 frames < 467 needed", MISMATCH_SHORT, 467 * C.CTC_FRAME_S, ("reference 2",)), 2,
     f"Your reference recording 2 is too short for this transcript: at least 10 seconds of speech is needed. {appmod.TRANSCRIPT_HINT}"),
])
def test_a_refused_reference_of_an_uploaded_bank_is_named(error, count, expected):
    assert appmod.mismatch_words(error, None, count) == expected


def test_unsupported_audio_names_the_file(server):
    base, seen, tmp = server
    text_file = ("notaudio.wav", b"this is a text file, not audio\n" * 10)
    s, body, _ = call(f"{base}/api/analyze", [("audio", text_file), ("transcript", TEXT)])
    assert (s, json.loads(body)["detail"]) == (415, "Your recording could not be read as audio. Use wav, mp3, m4a, ogg, flac or webm.")
    fields = [("audio", ("a.wav", wav_bytes(tmp))), ("transcript", TEXT), *own_references(tmp, 1), ("baseline_audio", text_file)]
    s, body, _ = call(f"{base}/api/analyze", fields)
    assert (s, json.loads(body)["detail"]) == (
        415, "Your reference recording 2 could not be read as audio. Use wav, mp3, m4a, ogg, flac or webm.")
    assert not seen


def test_a_file_above_the_limit_is_named(server):
    base, _, tmp = server
    big = b"RIFF" + b"\0" * C.MAX_UPLOAD_BYTES
    limit = f"is larger than {C.MAX_UPLOAD_BYTES // 2**20} MB."
    fields = [("audio", ("a.wav", wav_bytes(tmp))), ("transcript", TEXT), *own_references(tmp, 1), ("baseline_audio", ("big.wav", big))]
    s, body, _ = call(f"{base}/api/analyze", fields)
    assert (s, json.loads(body)["detail"]) == (413, f"Your reference recording 2 {limit}")
    s, body, _ = call(f"{base}/api/analyze", [("audio", ("a.wav", wav_bytes(tmp))), ("transcript_file", ("t.txt", big))])
    assert (s, json.loads(body)["detail"]) == (413, f"The transcript file {limit}")


def test_a_partial_mismatch_of_a_transcript_with_brackets_explains_them(server, monkeypatch):
    base, _, tmp = server
    error = TranscriptMismatch("participant recording: extra evidence", MISMATCH_PART, roles=("participant",), at_s=3.0, near="we hold")

    def refuse(*args, **kwargs):
        raise error
    monkeypatch.setattr(appmod, "analyze", refuse)
    s, body, _ = call(f"{base}/api/analyze", {"audio": ("a.wav", wav_bytes(tmp)), "transcript": TEXT + " (pause)"})
    job = wait_done(base, json.loads(body)["job_id"])
    assert job["error"] == (f"Part of the transcript does not match your recording (at about 3 s, near 'we hold'). {CHECK_TEXT} "
                            f"{appmod.BRACKET_HINT}")
