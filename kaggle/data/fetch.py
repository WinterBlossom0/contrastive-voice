#!/usr/bin/env python3
"""Private cvoice-data script kernel. Outcomes are in STATUS.json; always exit 0.

No Kaggle API calls, installs, credentials or project imports. ZIP members are
retrieved with strict HTTP ranges (including ZIP64 and multipart ZIPs), checked
against their published CRC and size, and never extracted by pathname. Sources
are independent. Outputs: one tar per source, one manifest.json, LICENSES.md and
fetch.log. CVOICE_PRIORITY2=0 disables the second-priority sources.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import email.utils
import hashlib
import importlib.util
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tarfile
import tempfile
import time
import threading
import urllib.error
import urllib.parse
import urllib.request
import wave
import zlib
from pathlib import Path

OUTPUT_LIMIT = 18_000_000_000  # decimal GB; leave 2 GB below Kaggle's limit
TAR_LIMIT = 4_000_000_000
DISK_MARGIN = 256_000_000
METADATA_LIMIT = 32_000_000
MEMBER_LIMIT = 128_000_000
WHOLE_LIMIT = 700_000_000
RANGE_GAP = 262_144
RANGE_LIMIT = 64_000_000
RETRY_WAIT = 240
HOST_INTERVAL = {"zenodo.org": 2.1}
HOST_NEXT = {}
HOST_WAIT = {}
PACE_LOCK = threading.Lock()
RANGE_CACHE = {}
TIMEOUT = 45
PRIORITY2 = os.environ.get("CVOICE_PRIORITY2", "1") == "1"
INPUT = Path("/kaggle/input")
SPEECH_REV = "613968e3b0b789fc33936fb5eba1973176ba7d11"
SPEECH_BASE = f"https://raw.githubusercontent.com/jimbozhang/speechocean762/{SPEECH_REV}/"
EARS_BASE = "https://raw.githubusercontent.com/facebookresearch/ears_dataset/main/"
IA_ITEMS = {
    "gettysburg": (
        "gettysburgaddress_150anniv_1311_librivox", "gettysburg_address_librivox",
        "gettysburg_address4_librivox", "gettysburg_shurtagal_librivox", "gettysburg_johng_librivox",
    ),
    "poetry": ("jabberwocky_librivox", "hope_1907.poem_librivox",
        'at_the_club_1308.poem_librivox',
        'oh_call_it_0912_librivox',
        'old_roller_towel_1103_librivox',
        'evanescence_1107_librivox',
        'sonnet_wet_summer_1207_librivox',
        'road_builders_0807_librivox',
        'before_edgehill_fight_1904.poem_librivox',
        'youths_spring_tribute_1204_librivox',
        'quatrain_khayyam_1202_librivox',
        'toafadedrose_1306_librivox',
        'symphony_yellow_1203_librivox',
        'summer_sun_0806_librivox',
        'song_soldierswives_1208_librivox',
        'word_is_dead_0807_librivox',
        'visionary_1201_librivox',
        'silverfiligree_1104_librivox',
        'near_far_1103_librivox',
        'myshadow_1409.poem_librivox'),
}
EXISTING_READERS = {"amb", "dl", "fb", "jn", "wt", "dj", "sa", "tg", "pc"}
EARS_SPEAKERS = tuple(f"p{i:03d}" for i in range(1, 108))
AVID_SPEAKERS = tuple(range(1, 51))
AVID_TEXT = {1: "We think differently.", 2: "He spoke soothingly.", 3: "They despised foreigners.",
             4: "That is your headache.", 5: "Nevertheless, it's true."}
GETTYSBURG_TEXT = (
    "Four score and seven years ago our fathers brought forth on this continent, a new nation, "
    "conceived in Liberty, and dedicated to the proposition that all men are created equal. "
    "Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived "
    "and so dedicated, can long endure. We are met on a great battle-field of that war. We have come "
    "to dedicate a portion of that field, as a final resting place for those who here gave their lives "
    "that that nation might live. It is altogether fitting and proper that we should do this. "
    "But, in a larger sense, we can not dedicate—we can not consecrate—we can not hallow—this ground. "
    "The brave men, living and dead, who struggled here, have consecrated it, far above our poor power "
    "to add or detract. The world will little note, nor long remember what we say here, but it can "
    "never forget what they did here. It is for us the living, rather, to be dedicated here to the "
    "unfinished work which they who fought here have thus far so nobly advanced. It is rather for us "
    "to be here dedicated to the great task remaining before us—that from these honored dead we take "
    "increased devotion to that cause for which they gave the last full measure of devotion—that we "
    "here highly resolve that these dead shall not have died in vain—that this nation, under God, "
    "shall have a new birth of freedom—and that government of the people, by the people, for the "
    "people, shall not perish from the earth."
)
ZENODO = {"avid": "10524873", "podcastfillers": "7121457", "mdvr": "2867216",
          "lombard": "3736465", "prominence": "10402793"}
# These are output ALLOCATIONS, not claims about observed corpus sizes. They
# include metadata/tar overhead. Measured download sizes are resolved separately.
SOURCES = [
    {"id": "gettysburg", "priority": 1, "reserve": 90_000_000},
    {"id": "poetry", "priority": 1, "reserve": 1_500_000_000},
    {"id": "speechocean", "priority": 1, "reserve": 800_000_000,
     "mount": "tthieu0901/speechocean762"},
    {"id": "ears", "priority": 1, "reserve": 2_700_000_000},
    {"id": "avid", "priority": 1, "reserve": 500_000_000},
    {"id": "disfluencyspeech", "priority": 2, "reserve": 150_000_000},
    {"id": "podcastfillers", "priority": 2, "reserve": 1_500_000_000},
    {"id": "sep28k", "priority": 2, "reserve": 5_000_000},
    {"id": "expresso", "priority": 2, "reserve": 1_500_000_000},
    {"id": "prominence", "priority": 2, "reserve": 900_000_000,
     "mount": "luizfelipebjcosta/libri-tts-train-clean-100"},
    {"id": "vctk", "priority": 2, "reserve": 500_000_000,
     "mount": "kynthesis/vctk-corpus"},
    {"id": "accent", "priority": 2, "reserve": 1_500_000_000,
     "mount": "rtatman/speech-accent-archive"},
    {"id": "mdvr", "priority": 2, "reserve": 250_000_000},
    {"id": "lombard", "priority": 2, "reserve": 500_000_000},
    {"id": "libristutter", "priority": 2, "reserve": 100_000_000,
     "mount": "danimarch/libristutter-unchanged"},
]
CC = "https://creativecommons.org/"
LICENCES = {
    "gettysburg": ("Public domain (item-specific mark/dedication)", CC + "publicdomain/mark/1.0/",
                   '"licenseurl": "http://creativecommons.org/publicdomain/mark/1.0/"'),
    "poetry": ("Public domain (item-specific mark/dedication)", CC + "licenses/publicdomain/",
               '"licenseurl": "http://creativecommons.org/licenses/publicdomain/"'),
    "speechocean": ("CC BY 4.0", CC + "licenses/by/4.0/",
                    "License: Attribution 4.0 International (CC BY 4.0)"),
    "ears": ("CC BY-NC 4.0", CC + "licenses/by-nc/4.0/",
             "Attribution-NonCommercial 4.0 International"),
    "avid": ("CC BY 4.0", CC + "licenses/by/4.0/", '"license": {"id": "cc-by-4.0"}'),
    "disfluencyspeech": ("Apache-2.0", "https://www.apache.org/licenses/LICENSE-2.0",
                         "license: apache-2.0"),
    "podcastfillers": ("Adobe Research License AND episode-specific CC licence",
                       "https://zenodo.org/records/7121457",
                       "For purposes of this License, noncommercial research purposes include academic research and teaching only."),
    "sep28k": ("CC BY-NC 4.0 (labels only)", CC + "licenses/by-nc/4.0/",
               "licensed under the Creative Commons Attribution-NonCommercial 4.0"),
    "expresso": ("CC BY-NC 4.0", CC + "licenses/by-nc/4.0/",
                 "The Expresso dataset is distributed under the [CC BY-NC 4.0]"),
    "prominence": ("CC BY 4.0 (labels and LibriTTS)", CC + "licenses/by/4.0/",
                   '"license": {"id": "cc-by-4.0"}; LibriTTS: Attribution 4.0 International (CC BY 4.0)'),
    "vctk": ("CC BY 4.0", CC + "licenses/by/4.0/",
             "Creative Commons License: Attribution 4.0 International"),
    "accent": ("CC BY-NC-SA 4.0", CC + "licenses/by-nc-sa/4.0/",
               "the contents of this project are made availalbe under the BY-NC-SA 4.0 license from Creative Commons"),
    "mdvr": ("CC BY 4.0", CC + "licenses/by/4.0/", '"license": {"id": "cc-by-4.0"}'),
    "lombard": ("CC BY 4.0", CC + "licenses/by/4.0/", '"license": {"id": "cc-by-4.0"}'),
    "libristutter": ("CC BY-NC 4.0", CC + "licenses/by-nc/4.0/", '"name": "CC BY-NC 4.0"'),
}
AUDIT = []
SOURCE_METADATA = {}
T0 = time.monotonic()
LOGFILE = None


def log(message):
    line = f"[fetch {time.monotonic() - T0:6.1f}s] {message}"
    print(line, flush=True)
    if LOGFILE:
        with LOGFILE.open("a") as f:
            f.write(line + "\n")


def pace(url):
    host = urllib.parse.urlsplit(url).hostname
    with PACE_LOCK:
        time.sleep(max(0, HOST_NEXT.get(host, 0) - time.monotonic()))
        HOST_NEXT[host] = time.monotonic() + HOST_INTERVAL.get(host, 0.1)


class Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        AUDIT.append({"url": req.full_url, "status": code, "redirect": newurl,
                      "time": round(time.monotonic() - T0, 3)})
        pace(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENER = urllib.request.build_opener(Redirects())


def http(url, *, start=None, end=None, head=False, maximum=METADATA_LIMIT, target=None):
    headers = {"User-Agent": "ContrastiveVoice-data/2.0", "Accept-Encoding": "identity"}
    if start is not None:
        headers["Range"] = f"bytes={start}-{end}"
        maximum = end - start + 1
    req = urllib.request.Request(url, headers=headers, method="HEAD" if head else "GET")
    waited = 0
    for attempt in range(5):
        pace(url)
        record = {"url": url, "method": "HEAD" if head else "RANGE" if start is not None else "GET",
                  "time": round(time.monotonic() - T0, 3), "attempt": attempt + 1}
        try:
            with OPENER.open(req, timeout=TIMEOUT) as r:
                record.update(status=r.status, host=urllib.parse.urlsplit(r.url).hostname,
                              headers=dict(r.headers))
                if start is not None and (r.status != 206 or not r.headers.get(
                        "Content-Range", "").startswith(f"bytes {start}-{end}/")):
                    raise ValueError(f"range refused for {url}: HTTP {r.status}")
                if target:
                    with target.open("wb") as f:
                        received = 0
                        while True:
                            chunk = r.read(min(1 << 20, maximum + 1 - received))
                            if not chunk:
                                break
                            f.write(chunk)
                            received += len(chunk)
                            if received > maximum:
                                raise ValueError("oversized download: " + url)
                    body = b""
                else:
                    body = b"" if head else r.read(maximum + 1)
                    received = len(body)
                record.update(reported_size=r.headers.get("Content-Range") or r.headers.get("Content-Length"),
                              received=received)
                if received > maximum or (start is not None and received != maximum):
                    raise ValueError(f"wrong/oversized response for {url}")
                return body, dict(r.headers)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            record.update(error=str(exc))
            delay = 2 ** attempt
            if isinstance(exc, urllib.error.HTTPError):
                record.update(status=exc.code, headers=dict(exc.headers), response=exc.read(2048).decode(errors="replace"))
                if exc.code not in (429, 500, 502, 503, 504) and not (
                        exc.code == 403 and exc.headers.get("X-RateLimit-Remaining") == "0"):
                    raise
                retry = exc.headers.get("Retry-After")
                if retry:
                    try:
                        delay = float(retry)
                    except ValueError:
                        delay = email.utils.parsedate_to_datetime(retry).timestamp() - time.time()
                elif exc.code in (429, 403):
                    delay = max(60 * (2 ** attempt), float(exc.headers.get("X-RateLimit-Reset", 0)) - time.time())
            delay = max(0, delay)
            host = urllib.parse.urlsplit(url).hostname
            if attempt == 4 or waited + delay > RETRY_WAIT or HOST_WAIT.get(host, 0) + delay > RETRY_WAIT:
                raise
            record["retry_wait"] = delay
            # Apply Retry-After to the whole host, including subsequent sources.
            HOST_WAIT[host] = HOST_WAIT.get(host, 0) + delay
            with PACE_LOCK:
                HOST_NEXT[host] = max(HOST_NEXT.get(host, 0), time.monotonic() + delay)
            waited += delay
        finally:
            AUDIT.append(record)
    raise RuntimeError("HTTP request failed")


def api(url):
    return json.loads(http(url)[0])


def check_url(url, known_size=None):
    try:
        _, h = http(url, head=True)
        size = int(h.get("Content-Length", h.get("content-length", 0)))
    except (urllib.error.URLError, ValueError):
        _, h = http(url, start=0, end=1023)
        size = int((h.get("Content-Range") or h.get("content-range")).split("/")[-1])
    if known_size and size and size != known_size:
        raise ValueError(f"published/HTTP size mismatch: {url}: {size} != {known_size}")
    if not size and not known_size:
        raise ValueError(f"no reported size: {url}")
    return size or known_size


def zip_directory(data):
    """Parse the central directory, retaining member size, CRC, disk and offset."""
    entries = []
    i = 0
    while i < len(data):
        v = struct.unpack_from("<4s6H3L5H2L", data, i)
        if v[0] != b"PK\x01\x02" or v[3] & 1:
            raise ValueError("invalid/encrypted ZIP directory")
        nlen, xlen, clen = v[10:13]
        raw_name = data[i + 46:i + 46 + nlen]
        try:
            name = raw_name.decode("utf-8")  # PodcastFillers omits UTF-8 flags on Unicode names.
        except UnicodeDecodeError:
            name = raw_name.decode("cp437")
        size, compressed, offset, disk = v[9], v[8], v[-1], v[13]
        extra = data[i + 46 + nlen:i + 46 + nlen + xlen]
        j = 0
        while j < len(extra):
            tag, n = struct.unpack_from("<HH", extra, j)
            value = extra[j + 4:j + 4 + n]
            j += 4 + n
            if tag == 1:
                q = 0
                if size == 0xffffffff:
                    size = struct.unpack_from("<Q", value, q)[0]
                    q += 8
                if compressed == 0xffffffff:
                    compressed = struct.unpack_from("<Q", value, q)[0]
                    q += 8
                if offset == 0xffffffff:
                    offset = struct.unpack_from("<Q", value, q)[0]
                    q += 8
                if disk == 65535:
                    disk = struct.unpack_from("<L", value, q)[0]
        entries.append({"path": name, "size": size, "compressed": compressed, "offset": offset,
                        "disk": disk, "method": v[4], "crc": v[7]})
        i += 46 + nlen + xlen + clen
    return entries


def segment_read(parts, disk, offset, length):
    chunks = []
    while length:
        part = parts[disk]
        n = min(length, part["size"] - offset)
        if n <= 0:
            raise ValueError("ZIP offset outside segment")
        cached = next(((a, p) for a, b, p in RANGE_CACHE.get(part["url"], [])
                       if a <= offset and offset + n <= b), None)
        if cached:
            a, path = cached
            with path.open("rb") as f:
                f.seek(offset - a)
                chunks.append(f.read(n))
        else:
            chunks.append(http(part["url"], start=offset, end=offset + n - 1)[0])
        length -= n
        disk += 1
        offset = 0
    return b"".join(chunks)


def access_ranges(items, whole=True):
    """Merge nearby members; allow maximal ZIP local-name/extra header lengths."""
    spans, parts = {}, {}
    for item in items:
        if "parts" not in item or "embedded_bytes" in item:
            continue
        disk, offset = item["disk"], item["offset"]
        length = 131_100 + item["compressed"]
        while length and disk < len(item["parts"]):
            part = item["parts"][disk]
            url = part["url"]
            parts[url] = part
            n = min(length, part["size"] - offset)
            spans.setdefault(url, []).append((offset, offset + n))
            length -= n
            disk, offset = disk + 1, 0
    result = []
    for url, ranges in spans.items():
        part = parts[url]
        if whole and len(parts) == 1 and part["size"] <= WHOLE_LIMIT:
            result.append((part, 0, part["size"]))
            continue
        gap = 4_194_304 if whole and urllib.parse.urlsplit(url).hostname == "zenodo.org" else RANGE_GAP
        merged = []
        for a, b in sorted(ranges):
            if merged and a <= merged[-1][1] + gap and b - merged[-1][0] <= RANGE_LIMIT:
                merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
            else:
                merged.append((a, b))
        result.extend((part, a, b) for a, b in merged)
    return result


def prepare_ranges(items, root, whole=True):
    ranges = access_ranges(items, whole)
    total = sum(b - a for _, a, b in ranges)
    if shutil.disk_usage(root).free < total + DISK_MARGIN:
        raise OSError("insufficient disk for merged archive ranges")
    for i, (part, a, b) in enumerate(ranges):
        path = root / f"range-{i}"
        if a == 0 and b == part["size"]:
            http(part["url"], maximum=b, target=path)
            if path.stat().st_size != b or (part.get("md5") and digest(path, "md5") != part["md5"]):
                raise ValueError("whole archive size/hash mismatch")
        else:
            http(part["url"], start=a, end=b - 1, target=path)
        RANGE_CACHE.setdefault(part["url"], []).append((a, b, path))
    return [p for rows in RANGE_CACHE.values() for _, _, p in rows]


def remote_zip(parts):
    last = parts[-1]
    start = max(0, last["size"] - 131072)
    tail = http(last["url"], start=start, end=last["size"] - 1)[0]
    pos = tail.rfind(b"PK\x05\x06")
    if pos < 0:
        raise ValueError("ZIP end record missing")
    e = struct.unpack_from("<4s4H2LH", tail, pos)
    disk, cd_disk, _, count, cd_size, offset = e[1:7]
    if offset == 0xffffffff or cd_size == 0xffffffff or count == 65535:
        loc = struct.unpack_from("<4sLQL", tail, pos - 20)
        z = segment_read(parts, loc[1], loc[2], 56)
        record = struct.unpack("<4sQ2H2L4Q", z)
        cd_disk, count, cd_size, offset = record[5], record[7], record[8], record[9]
    if disk != len(parts) - 1 or cd_size > METADATA_LIMIT:
        raise ValueError("unsupported ZIP segment/directory size")
    entries = zip_directory(segment_read(parts, cd_disk, offset, cd_size))
    if len(entries) != count:
        raise ValueError("ZIP directory count mismatch")
    for entry in entries:
        entry["parts"] = parts
        entry["url"] = parts[entry["disk"]]["url"]
    return entries


def zip_member(item):
    if item["size"] > MEMBER_LIMIT or item["compressed"] > MEMBER_LIMIT:
        raise ValueError(f"member exceeds memory/disk guard: {item['path']}")
    parts, disk, offset = item["parts"], item["disk"], item["offset"]
    h = segment_read(parts, disk, offset, 30)
    v = struct.unpack("<4s5H3L2H", h)
    if v[0] != b"PK\x03\x04":
        raise ValueError("invalid ZIP local header")
    offset += 30 + v[-2] + v[-1]
    while offset >= parts[disk]["size"]:
        offset -= parts[disk]["size"]
        disk += 1
    b = segment_read(parts, disk, offset, item["compressed"])
    if item["method"] == 8:
        decoder = zlib.decompressobj(-15)
        b = decoder.decompress(b, item["size"] + 1)
        if not decoder.eof or decoder.unconsumed_tail:
            raise ValueError("incomplete/oversized deflate member")
    elif item["method"] != 0:
        raise ValueError(f"unsupported ZIP compression {item['method']}")
    if len(b) != item["size"] or zlib.crc32(b) != item["crc"]:
        raise ValueError(f"ZIP size/CRC mismatch: {item['path']}")
    return b


def direct(url, path, size, **fields):
    return {"url": url, "path": path, "size": size, **fields}


def label(url, path=None, size=None, **fields):
    return direct(url, path or urllib.parse.unquote(url.rsplit("/", 1)[-1]),
                  size if size is not None else check_url(url), **fields)


def mount_path(ref):
    owner, name = ref.split("/")
    for p in (INPUT / name, INPUT / "datasets" / owner / name, INPUT / owner / name):
        if p.is_dir():
            return p
    return None


def ia_speaker(item, name):
    stem = Path(name).stem.removesuffix("_128kb")
    if item == "jabberwocky_librivox":
        code = re.sub(r"_?\d+$", "", stem.removeprefix("jabberwocky_carroll_"))
    else:
        code = stem.rsplit("_", 1)[-1]
    return item + ":" + code


def resolve_ia(source):
    audio, labels = [], []
    for item in IA_ITEMS[source]:
        url = "https://archive.org/metadata/" + item
        d = api(url)
        licence_url = d["metadata"].get("licenseurl", "")
        if not any(s in licence_url for s in ("publicdomain", "publicdomain/zero")):
            raise ValueError(f"no public-domain declaration for {item}")
        labels.append(direct(url, item + "-metadata.json", len(json.dumps(d).encode()), embedded=d))
        candidates = [f for f in d["files"] if f["name"].endswith(".mp3") and f.get("source") == "original"]
        # The anniversary's original masters are VBR; prefer its published 128kb files.
        if "150anniv" in item:
            candidates = [f for f in d["files"] if f["name"].endswith("_128kb.mp3")]
            candidates = [f for f in candidates if f["name"].split("_")[-2] not in EXISTING_READERS]
        for f in candidates:
            name = f["name"]
            audio.append(direct("https://archive.org/download/" + item + "/" + urllib.parse.quote(name),
                                item + "/" + name, int(f["size"]), sha1=f.get("sha1"), md5=f.get("md5"),
                                duration=float(f.get("length", 0)),
                                speaker=ia_speaker(item, name),
                                style="volunteer_reading", licence_url=licence_url, label_files=[item + "-metadata.json"]))
            if source == "gettysburg":
                audio[-1]["text"] = GETTYSBURG_TEXT
        if source == "poetry" and len({x["speaker"] for x in audio if x["path"].startswith(item + "/")}) < 10:
            raise ValueError("poem has fewer than ten distinct readers: " + item)
    return audio, labels


def resolve_speech():
    tree_url = f"https://api.github.com/repos/jimbozhang/speechocean762/git/trees/{SPEECH_REV}?recursive=1"
    d = api(tree_url)
    if d.get("truncated"):
        raise ValueError("truncated speechocean repository index")
    tree = [x for x in d["tree"] if x["type"] == "blob"]
    wavs = [x for x in tree if x["path"].lower().endswith(".wav")]
    ids = set()
    for split in ("train", "test"):
        ids.update(row.split()[0] for row in http(SPEECH_BASE + split + "/utt2spk")[0].decode().splitlines())
    wavs = [x for x in wavs if Path(x["path"]).stem in ids]
    if len(wavs) != 5000:
        raise ValueError("speechocean must contain all 5,000 utterances")
    audio = [direct(SPEECH_BASE + x["path"], x["path"], x["size"], git_sha1=x["sha"],
                    speaker=x["path"].split("/")[1], style="scored_reading",
                    label_files=["resource/scores.json", "resource/scores-detail.json"])
             for x in wavs]
    labels = [direct(SPEECH_BASE + x["path"], x["path"], x["size"], git_sha1=x["sha"])
              for x in tree if not x["path"].startswith("WAVE/")]
    return audio, labels


def zenodo_files(source):
    url = "https://zenodo.org/api/records/" + ZENODO[source]
    body = http(url)[0]
    d = json.loads(body)
    SOURCE_METADATA[source] = direct(url, "source-metadata.json", len(body), embedded_bytes=body)
    if source != "podcastfillers" and d["metadata"]["license"]["id"] != "cc-by-4.0":
        raise ValueError("Zenodo licence changed")
    return {f["key"]: {"url": f["links"]["self"], "size": f["size"],
                       "md5": f["checksum"].removeprefix("md5:")} for f in d["files"]}


def resolve_ears():
    releases = api("https://api.github.com/repos/facebookresearch/ears_dataset/releases")
    assets = {a["name"]: a for r in releases for a in r["assets"]}
    def one(spk):
        a = assets[spk + ".zip"]
        entries = remote_zip([{"url": a["browser_download_url"], "size": a["size"]}])
        chosen = [x for x in entries if re.fullmatch(r"p\d+/rainbow_0[1-8]_(regular|fast|slow|loud|whisper)\.wav", x["path"])]
        if len(chosen) != 40:
            raise ValueError(f"incomplete Rainbow styles for {spk}")
        for x in chosen:
            x.update(speaker=spk, style=Path(x["path"]).stem.rsplit("_", 1)[-1], label_files=["transcripts.json"])
        return sorted(chosen, key=lambda x: x["path"])
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        audio = [x for rows in pool.map(one, EARS_SPEAKERS) for x in rows]
    return audio, [label(EARS_BASE + n) for n in ("transcripts.json", "speaker_statistics.json", "LICENSE", "README.md")]


def resolve_avid():
    f = zenodo_files("avid")
    entries = remote_zip([f["AVID.zip"]])
    audio, labels = [], []
    for x in entries:
        name = x["path"]
        m = re.fullmatch(r"AVID/Repository 2/SENT/sp(\d+)_s[12]_sen([1-5])_(soft|normal|loud|veryloud)(?: 2)?\.wav", name)
        if m and int(m[1]) in AVID_SPEAKERS:
            x.update(speaker="sp" + m[1], style=m[3], text=AVID_TEXT[int(m[2])],
                     label_files=["AVID/Repository 2/Metadata_with_labels_SENT.csv", "AVID/Readme.docx"])
            audio.append(x)
        if name in ("AVID/Readme.docx", "AVID/Repository 2/Metadata_with_labels_SENT.csv") or (
                name.startswith("AVID/Calibration_tones/") and name.endswith(".wav")):
            labels.append(x)
    if any(len({(x["text"], x["style"]) for x in audio if x["speaker"] == f"sp{spk}"}) != 20
           for spk in AVID_SPEAKERS):
        raise ValueError("AVID speaker lacks a requested sentence/effort pair")
    if len(audio) != len(AVID_SPEAKERS) * 40:
        raise ValueError("AVID matching sentence quartet missing")
    return sorted(audio, key=lambda x: x["path"]), labels


def resolve_podcast():
    f = zenodo_files("podcastfillers")
    parts = [f[n] for n in ("PodcastFillers.z01", "PodcastFillers.z02", "PodcastFillers.z03", "PodcastFillers.zip")]
    entries = remote_zip(parts)
    csv_item = next(x for x in entries if x["path"] == "PodcastFillers/metadata/PodcastFillers.csv")
    csv_item["embedded_bytes"] = zip_member(csv_item)
    rows = list(csv.DictReader(csv_item["embedded_bytes"].decode("utf-8").splitlines()))
    lookup = {int(Path(x["path"]).stem): x for x in entries
              if "/audio/clip_wav/" in x["path"] and Path(x["path"]).stem.isdigit()}
    chosen = []
    for category in ("Uh", "Um", "Breath", "Repetitions", "Words"):
        selected = [r for r in rows if r["label_full_vocab"] == category][:500]
        for row in selected:
            x = lookup[int(row["pfID"])]
            x.update(style=category, episode=row["podcast_filename"])
            chosen.append(x)
    labels = [x for x in entries if x["path"] in (
        "PodcastFillers/LICENSE_ANNOTATIONS_ADOBE_RESEARCH_LICENSE.txt", "PodcastFillers/LICENSE_AUDIO.csv",
        "PodcastFillers/README.txt", "PodcastFillers/metadata/PodcastFillers.csv")]
    for x in chosen:
        x.update(speaker=None,
                 label_files=["PodcastFillers/metadata/PodcastFillers.csv", "PodcastFillers/LICENSE_AUDIO.csv"])
    if len(chosen) != 2500 or len(labels) != 4:
        raise ValueError("PodcastFillers annotated clip layout changed")
    episodes = sorted((x for x in entries if x["path"].startswith("PodcastFillers/audio/episode_mp3/")
                       and x["path"].endswith(".mp3")), key=lambda x: (x["size"], x["path"]))[:10]
    for x in episodes:
        episode = Path(x["path"]).stem
        matched = [e for e in entries if e["path"].startswith("PodcastFillers/metadata/episode_")
                   and Path(e["path"]).stem == episode and e["size"]]
        if not any("/episode_annotations/" in e["path"] for e in matched):
            raise ValueError("complete episode annotations missing: " + episode)
        labels.extend(matched)
        x.update(style="full_episode", episode=episode, label_files=[e["path"] for e in matched]
                 + ["PodcastFillers/LICENSE_AUDIO.csv"])
    if len(episodes) != 10:
        raise ValueError("ten PodcastFillers episodes unavailable")
    return chosen + episodes, labels


def resolve_zenodo_audio(source):
    f = zenodo_files(source)
    key = "26_29_09_2017_KCL.zip" if source == "mdvr" else "lombardgrid_audio.zip"
    entries = remote_zip([f[key]])
    if source == "mdvr":
        audio = [x for x in entries if "/ReadText/" in x["path"] and x["path"].endswith(".wav")]
        for x in audio:
            x.update(speaker=Path(x["path"]).stem.split("_")[0], style=x["path"].split("/")[-2])
        labels = []
    else:
        audio = [x for x in entries if re.search(r"/s\d+_[lp]_\w+\.wav$", x["path"])]
        for x in audio:
            spk, cond, _ = Path(x["path"]).stem.split("_", 2)
            x.update(speaker=spk, style={"p": "plain", "l": "lombard"}[cond],
                     label_files=["lombardgrid_json.zip", "lombardgrid_alignment.zip"])
        labels = [direct(f[n]["url"], n, f[n]["size"], md5=f[n]["md5"])
                  for n in ("lombardgrid_json.zip", "lombardgrid_alignment.zip")]
    if not audio:
        raise ValueError(source + " selected audio missing")
    return sorted(audio, key=lambda x: x["path"]), labels


def resolve_expresso():
    base = "https://huggingface.co/datasets/ylacombe/expresso/resolve/main/"
    tree = api("https://huggingface.co/api/datasets/ylacombe/expresso/tree/main?recursive=true")
    shards = [direct(base + f["path"], f["path"], f["size"], sha256=f["lfs"]["oid"], parquet=True)
              for f in tree if f["path"].endswith(".parquet")]
    if len(shards) != 12:
        raise ValueError("Expresso read mirror shard layout changed")
    return [], shards + [label(base + "README.md"), label(
        "https://raw.githubusercontent.com/facebookresearch/textlesslib/main/examples/expresso/dataset/README.md",
        "original-README.md")]


def resolve(source):
    name = source["id"]
    if name in IA_ITEMS:
        return resolve_ia(name)
    if name == "speechocean":
        return resolve_speech()
    if name == "ears":
        return resolve_ears()
    if name == "avid":
        return resolve_avid()
    if name == "podcastfillers":
        return resolve_podcast()
    if name in ("mdvr", "lombard"):
        return resolve_zenodo_audio(name)
    if name == "expresso":
        return resolve_expresso()
    if name == "disfluencyspeech":
        base = "https://huggingface.co/datasets/amaai-lab/DisfluencySpeech/resolve/main/"
        tree = api("https://huggingface.co/api/datasets/amaai-lab/DisfluencySpeech/tree/main?recursive=true")
        f = next(x for x in tree if x["path"] == "data/test-00000-of-00001.parquet")
        return [], [direct(base + f["path"], f["path"], f["size"], sha256=f["lfs"]["oid"], parquet=True),
                    label(base + "README.md")]
    if name == "sep28k":
        base = "https://raw.githubusercontent.com/apple/ml-stuttering-events-dataset/main/"
        return [], [label(base + n) for n in ("SEP-28k_labels.csv", "SEP-28k_episodes.csv", "README.md")]
    if name == "prominence":
        f = zenodo_files(name)["libritts-emphasis-annotations.json"]
        return [], [direct(f["url"], "libritts-emphasis-annotations.json", f["size"], md5=f["md5"])]
    if name == "vctk":
        # The verified mirror contains COPYING (18,951 B); no Edinburgh request.
        return [], []
    if name in ("accent", "libristutter"):
        # Verify original licence/access pages even when the Kaggle mount is absent.
        url = {"accent": "https://accent.gmu.edu/",
               "libristutter": "https://borealisdata.ca/api/datasets/:persistentId/?persistentId=doi:10.5683/SP3/NKVOGQ"}[name]
        body = http(url)[0]
        return [], [direct(url, "upstream-licence.txt", len(body), embedded_bytes=body)]
    raise ValueError("unknown source " + name)


def budget_sources(sources, available=OUTPUT_LIMIT):
    accepted, refused = [], []
    for source in sorted(sources, key=lambda s: s["priority"]):
        if source["reserve"] <= available:
            accepted.append(source)
            available -= source["reserve"]
        else:
            refused.append(source)
    return accepted, refused


def dry_plan(sources, resolver=resolve):
    results = []
    for source in sources:
        try:
            audio, labels = resolver(source)
            if source["id"] in SOURCE_METADATA:
                labels.append(SOURCE_METADATA[source["id"]])
            ranges = access_ranges(audio + labels)
            transfer = sum(b - a for _, a, b in ranges) + sum(x.get("compressed", x["size"]) for x in audio + labels
                           if "parts" not in x and not any(k in x for k in ("local", "embedded", "embedded_bytes", "embedded_text")))
            route = "mount preferred; HTTPS fallback" if source["id"] == "speechocean" else (
                "mount required (audio sizes checked on Kaggle)" if source.get("mount") else "HTTPS")
            log(f"{source['id']}: checked; audio={len(audio) if not source.get('mount') or audio else 'on mount'} "
                f"labels={len(labels)} selected-transfer={transfer:,} B output-cap={source['reserve']:,} B; {route}")
            results.append({"source": source["id"], "stage": "resolve", "error": None,
                            "audio": audio, "labels": labels, "selected_transfer": transfer,
                            "archive_requests": len(ranges), "archive_hosts": {h: sum(urllib.parse.urlsplit(p["url"]).hostname == h for p, _, _ in ranges) for h in {urllib.parse.urlsplit(p["url"]).hostname for p, _, _ in ranges}}})
        except Exception as e:
            log(f"{source['id']}: FAILED resolve: {type(e).__name__}: {e}")
            results.append({"source": source["id"], "stage": "resolve", "error": f"{type(e).__name__}: {e}"})
    return results


def digest(path, algorithm="sha256"):
    h = hashlib.new(algorithm)
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def get_item(item, target, mount=None):
    if Path(item["path"]).is_absolute() or ".." in Path(item["path"]).parts:
        raise ValueError("unsafe upstream pathname")
    target.parent.mkdir(parents=True, exist_ok=True)
    local = mount / item["path"] if mount else None
    if item.get("local"):
        local = Path(item["local"])
    if local and local.is_file():
        matches = local.stat().st_size == item["size"]
        if matches and item.get("git_sha1"):
            b = local.read_bytes()
            matches = hashlib.sha1(f"blob {len(b)}\0".encode() + b).hexdigest() == item["git_sha1"]
        if not matches and item.get("git_sha1"):
            AUDIT.append({"url": item["url"], "method": "MOUNT", "path": str(local),
                          "mirror_size": local.stat().st_size, "expected_size": item["size"],
                          "verification": "mirror differs; pinned Git blob fetched"})
            http(item["url"], maximum=item["size"], target=target)
        else:
            shutil.copyfile(local, target)
    elif "embedded" in item:
        target.write_text(json.dumps(item["embedded"], indent=1) + "\n")
        return
    elif "embedded_text" in item:
        target.write_text(item["embedded_text"])
    elif "embedded_bytes" in item:
        target.write_bytes(item["embedded_bytes"])
    elif "parts" in item:
        target.write_bytes(zip_member(item))
    else:
        http(item["url"], maximum=item["size"], target=target)
    if target.stat().st_size != item["size"]:
        raise ValueError("download size mismatch: " + item["path"])
    for algorithm in ("md5", "sha1", "sha256"):
        if item.get(algorithm) and digest(target, algorithm) != item[algorithm]:
            raise ValueError(algorithm + " mismatch: " + item["path"])
    if item.get("git_sha1"):
        b = target.read_bytes()
        if hashlib.sha1(f"blob {len(b)}\0".encode() + b).hexdigest() != item["git_sha1"]:
            raise ValueError("Git blob SHA1 mismatch: " + item["path"])


def convert(original, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-threads", "1",
                    "-i", str(original), "-map", "0:a:0", "-vn", "-ac", "1", "-ar", "16000",
                    "-c:a", "pcm_s16le", str(target)], check=True, capture_output=True, timeout=300)
    with wave.open(str(target)) as f:
        if (f.getnchannels(), f.getframerate(), f.getsampwidth(), f.getcomptype()) != (1, 16000, 2, "NONE"):
            raise ValueError("ffmpeg output is not canonical PCM16")
        return f.getnframes() / 16000


def manifest_entry(source, item, path, duration, audio_path):
    name, licence_url, _ = LICENCES[source]
    return {"source": source, "licence": item.get("licence", name),
            "licence_url": item.get("licence_url", licence_url), "source_url": item["url"],
            "original_path": item["path"], "speaker_id": item.get("speaker"),
            "condition": item.get("style"), "text": item.get("text"), "duration": round(duration, 6),
            "sha256": digest(path), "sha256_basis": "canonical WAV file bytes", "audio_path": audio_path,
            "label_files": item.get("label_files", []), "episode": item.get("episode")}


def tar_size(files):
    # Reserve 2 KiB per file for PAX path/time records, plus data and tar padding.
    size = sum(2560 + ((p.stat().st_size + 511) // 512) * 512 for p in files)
    return ((size + 1024 + 10239) // 10240) * 10240


def pack_tar(root, out, source, limit=TAR_LIMIT):
    files = sorted(p for p in root.rglob("*") if p.is_file())
    if tar_size(files) > limit:
        raise ValueError("source cannot fit one tar")
    name = f"{source}-001.tar"
    target = out / name
    with tarfile.open(target, "w", format=tarfile.PAX_FORMAT) as tf:
        for path in files:
            tf.add(path, arcname=str(path.relative_to(root)), recursive=False)
    if target.stat().st_size > limit:
        raise ValueError("tar exceeded limit")
    return {str(p.relative_to(root)): name for p in files}, [
        {"file": name, "bytes": target.stat().st_size, "sha256": digest(target)}]


def mounted_audio(source, mount, root):
    name = source["id"]
    if mount is None:
        raise FileNotFoundError("required Kaggle dataset not mounted: " + source["mount"])
    audio, labels = [], []
    if name == "prominence":
        annotations = json.loads((root / "labels/libritts-emphasis-annotations.json").read_text())
        by_stem = {}
        for batch in annotations.values():
            for a in batch["annotations"]:
                by_stem[a["stem"]] = " ".join(w[0] for w in a["words"])
        lookup = {p.stem: p for p in mount.rglob("*.wav")}
        missing = sorted(set(by_stem) - set(lookup))
        if missing:
            raise FileNotFoundError(f"LibriTTS mount lacks {len(missing)} annotated utterances, e.g. {missing[:2]}")
        for stem, text in sorted(by_stem.items()):
            p = lookup[stem]
            audio.append(direct("https://www.openslr.org/60/", str(p.relative_to(mount)), p.stat().st_size,
                                local=str(p), speaker=stem.split("_")[0], style="crowd_prominence", text=text,
                                label_files=["libritts-emphasis-annotations.json"]))
    elif name == "accent":
        paths = {p.name: p for p in mount.rglob("*.mp3")}
        english = sorted(n for n in paths if re.fullmatch(r"english\d+\.mp3", n))
        other = sorted(n for n in paths if re.fullmatch(r"[a-z]+\d+\.mp3", n) and n not in english)[:200]
        if not english or len(other) != 200:
            raise FileNotFoundError("Accent Archive native-English/200-other subset incomplete")
        wanted = english + other
        for filename in wanted:
            if filename not in paths:
                raise FileNotFoundError("Accent Archive mount lacks " + filename)
            p = paths[filename]
            audio.append(direct("https://accent.gmu.edu/", str(p.relative_to(mount)), p.stat().st_size,
                                local=str(p), speaker=p.stem, style="shared_paragraph",
                                label_files=["speakers_all.csv", "reading-passage.txt"]))
        labels = list(mount.rglob("speakers_all.csv")) + list(mount.rglob("reading-passage.txt"))
    elif name == "vctk":
        # 001-005 are Stella; Rainbow is 006-024 in this VCTK release.
        mounted = [p for p in mount.rglob("*") if p.is_file()]
        transcripts = {p.stem: p for p in mounted if p.suffix == ".txt"}
        paths = sorted(p for p in mounted if p.suffix.lower() in (".wav", ".flac")
                       and re.fullmatch(r"p\d+_(?:00[6-9]|01[0-9]|02[0-4])(?:_mic1)?", p.stem))
        speakers = {p.stem.split("_")[0] for p in mounted if p.suffix.lower() in (".wav", ".flac")}
        # VCTK lacks some sentences for some speakers (p264 on the Kaggle mirror); a partial passage cannot pair with the others.
        rainbow = {f"{i:03d}" for i in range(6, 25)}
        incomplete = sorted(s for s in speakers if {p.stem.split("_")[1] for p in paths if p.stem.startswith(s + "_")} != rainbow)
        if incomplete:
            log("vctk: skipped speakers without the complete Rainbow passage: " + ", ".join(incomplete))
        paths = [p for p in paths if p.stem.split("_")[0] not in incomplete]
        if not paths:
            raise FileNotFoundError("VCTK mount has no speaker with the complete Rainbow passage")
        for p in paths:
            t = transcripts.get(p.stem.removesuffix("_mic1"))
            if t is None:
                raise FileNotFoundError("VCTK Rainbow transcript missing: " + p.stem)
            labels.append(t)
            audio.append(direct("https://datashare.ed.ac.uk/handle/10283/3443", str(p.relative_to(mount)), p.stat().st_size,
                                local=str(p), speaker=p.stem.split("_")[0], style="rainbow_passage", text=t.read_text().strip(),
                                label_files=[str(t.relative_to(mount))]))
        labels.extend(p for p in mounted if p.name in ("README", "README.txt", "COPYING", "speaker-info.txt"))
        if not any(p.name == "COPYING" for p in labels):
            raise FileNotFoundError("VCTK mirror licence COPYING is missing")
        licence_text = next(p for p in labels if p.name == "COPYING").read_text()
        match = re.search(r"creativecommons\.org/licenses/(by(?:-[a-z]+)*)/(\d\.\d)", licence_text)
        if match:
            slug, version = match.groups()
            url, licence = CC + f"licenses/{slug}/{version}/", "CC " + slug.upper() + " " + version
        elif licence_text.lstrip().startswith("ODC Attribution License (ODC-By)"):
            # The original VCTK-Corpus release carries the ODC-By text without a version; 1.0 is the only ODC-By version.
            url, licence = "https://opendatacommons.org/licenses/by/1-0/", "ODC-By 1.0"
        else:
            raise ValueError("VCTK mirror COPYING has no identifiable licence")
        LICENCES[name] = (licence, url, "Licence text retained from mounted VCTK-Corpus/COPYING.")
        for item in audio:
            item.update(licence=licence, licence_url=url)
    elif name == "libristutter":
        paths = sorted(p for p in mount.rglob("*") if p.suffix.lower() in (".wav", ".flac"))[:100]
        csvs = {p.stem: p for p in mount.rglob("*.csv")}
        for p in paths:
            if p.stem not in csvs:
                raise FileNotFoundError("LibriStutter annotation missing: " + p.stem)
            t = csvs[p.stem]
            labels.append(t)
            audio.append(direct("https://doi.org/10.5683/SP3/NKVOGQ", str(p.relative_to(mount)), p.stat().st_size,
                                local=str(p), speaker=p.stem.split("-")[0], style="synthetic_stutter",
                                label_files=[str(t.relative_to(mount))]))
    if not audio:
        raise ValueError("no selected audio on " + source["mount"])
    return audio, [direct("https://www.kaggle.com/datasets/" + source["mount"], str(p.relative_to(mount)),
                          p.stat().st_size, local=str(p)) for p in labels]


def attach_annotations(source, audio, root):
    if source == "speechocean":
        scores = json.loads((root / "labels/resource/scores.json").read_text())
        for x in audio:
            score = scores[Path(x["path"]).stem]
            x["text"] = score["text"]
    elif source == "ears":
        texts = json.loads((root / "labels/transcripts.json").read_text())
        for x in audio:
            x["text"] = texts[Path(x["path"]).stem]
    elif source == "podcastfillers":
        with (root / "labels/PodcastFillers/metadata/PodcastFillers.csv").open() as f:
            rows = list(csv.DictReader(f))
        lookup = {int(r["pfID"]): r for r in rows}
        with (root / "labels/PodcastFillers/LICENSE_AUDIO.csv").open() as f:
            licences = dict(csv.reader(f))
        for x in audio:
            episode = x["episode"] if x["style"] == "full_episode" else lookup[int(Path(x["path"]).stem)]["podcast_filename"]
            own = licences[episode]
            x.update(licence=own + " AND Adobe Research License", speaker=None, episode=episode)
            slug = {"CC BY 3.0": "by", "CC BY-SA 3.0": "by-sa", "CC BY-ND 3.0": "by-nd"}[own]
            x["licence_url"] = CC + "licenses/" + slug + "/3.0/"


def expresso_style(row_id: str) -> str:
    if "emphasis" in row_id:
        return "emphasis"
    if "_enunciated_" in row_id:
        return "enunciated"
    return "default"


def parquet_audio(path, root, limit, source="disfluencyspeech", offset=0):
    import pyarrow.parquet as pq
    audio = []
    # Check this optional, image-provided library at startup; never install it.
    for batch in pq.ParquetFile(path).iter_batches(batch_size=32):
        for row in batch.to_pylist():
            if limit is not None and len(audio) >= limit:
                return audio
            if source == "expresso" and row["style"] not in ("default", "enunciated", "emphasis") and not re.match(
                    r"ex0[1-4]_(default|enunciated)_", row["id"]):
                continue
            i = offset + len(audio)
            record = row["audio"]
            raw = root / f"parquet-audio-{i}.wav"
            raw.write_bytes(record["bytes"])
            transcript = row["text"] if source == "expresso" else row["transcript_annotated"]
            name = f"utterance-{i:05d}.json"
            (root / "labels" / name).write_text(json.dumps({k: v for k, v in row.items() if k != "audio"}, indent=1))
            if source == "expresso":
                url = "https://huggingface.co/datasets/ylacombe/expresso/resolve/main/" + str(path.relative_to(root / "labels"))
                audio_path = row["id"] + ".wav"
                speaker = row["speaker_id"]
                style = expresso_style(row["id"])
            else:
                url = "https://huggingface.co/datasets/amaai-lab/DisfluencySpeech/resolve/main/data/test-00000-of-00001.parquet"
                audio_path = record.get("path") or str(i)
                speaker = "single_actor"
                style = "acted_disfluent"
            audio.append(direct(url, audio_path, raw.stat().st_size, local=str(raw), speaker=speaker, style=style,
                                text=transcript, label_files=[name]))
    return audio


def source_fetch(source, audio, labels, out, limit=None):
    name, stage = source["id"], "disk"
    result = {"source": name, "complete": False, "stage": stage, "error": None, "files": 0, "parts": []}
    try:
        stage = "dependency"
        if not shutil.which("ffmpeg"):
            raise RuntimeError("ffmpeg is not available")
        if name in ("disfluencyspeech", "expresso") and not importlib.util.find_spec("pyarrow"):
            raise RuntimeError("Kaggle image has no pyarrow; source cannot decode parquet without installing")
        stage = "disk"
        if shutil.disk_usage(out).free < source["reserve"] + DISK_MARGIN:
            raise OSError("insufficient output disk for source reservation")
        if shutil.disk_usage("/tmp").free < source["reserve"] + MEMBER_LIMIT + DISK_MARGIN:
            raise OSError("insufficient /tmp disk for source reservation and intermediates")
        with tempfile.TemporaryDirectory(prefix="cvoice-fetch-", dir="/tmp") as tmp:
            root = Path(tmp)
            stage = "labels"
            mount = mount_path(source["mount"]) if source.get("mount") else None
            selected = audio[:limit] if limit is not None else audio
            cache_files = prepare_ranges(([] if name == "ears" else selected) + labels, root, whole=limit is None)
            audio = [] if name == "expresso" else audio
            for item in labels:
                target = root / "labels" / item["path"]
                if name == "expresso" and item.get("parquet"):
                    if limit is not None and len(audio) >= limit:
                        continue
                    get_item(item, target)
                    audio.extend(parquet_audio(target, root, None if limit is None else limit - len(audio), name, len(audio)))
                    target.unlink()
                else:
                    get_item(item, target, mount if name == "speechocean" else None)
            if name in ("prominence", "vctk", "accent", "libristutter"):
                stage = "mount"
                audio, extra = mounted_audio(source, mount, root)
                for item in extra:
                    get_item(item, root / "labels" / item["path"])
            provenance = [{"path": x["path"], "source_url": x["url"], "used": x.get("local") or (
                           str(mount / x["path"]) if mount and (mount / x["path"]).is_file()
                           and (root / "labels" / x["path"]).read_bytes() == (mount / x["path"]).read_bytes()
                           else x["url"])} for x in labels if not x.get("parquet")]
            if name == "vctk":
                provenance.extend({"path": x["path"], "source_url": x["url"], "used": x["local"]} for x in extra)
            (root / "labels/acquisition.json").write_text(json.dumps(provenance, indent=1))
            if name == "disfluencyspeech":
                stage = "parquet"
                audio = parquet_audio(root / "labels/data/test-00000-of-00001.parquet", root, limit)
            if name == "expresso" and limit is None:
                if {x["speaker"] for x in audio} != {"ex01", "ex02", "ex03", "ex04"}:
                    raise ValueError("Expresso read subset lacks a speaker")
                for speaker in ("ex01", "ex02", "ex03", "ex04"):
                    styles = {x["style"] for x in audio if x["speaker"] == speaker}
                    if not {"default", "enunciated", "emphasis"} <= styles:
                        raise ValueError("Expresso mirror lacks required styles: " + speaker)
            attach_annotations(name, audio, root)
            if limit is not None:
                audio = audio[:limit]
            entries = []
            kept_bytes = tar_size([p for p in (root / "labels").rglob("*") if p.is_file()
                                   and not p.name.endswith(".parquet")])
            stage = "download/convert"
            cached_speaker = None
            for i, item in enumerate(audio):
                if name == "ears" and item["speaker"] != cached_speaker:
                    for path in cache_files:
                        path.unlink()
                    RANGE_CACHE.clear()
                    cached_speaker = item["speaker"]
                    cache_files = prepare_ranges([x for x in audio if x["speaker"] == cached_speaker],
                                                 root, whole=False)
                    log(f"ears: reading styles for {cached_speaker}; completed={i}/{len(audio)}")
                original = root / "input-audio"
                get_item(item, original, mount if name == "speechocean" else None)
                rel = f"audio/{i:05d}.wav"
                target = root / rel
                duration = convert(original, target)
                original.unlink()
                if item.get("local") and Path(item["local"]).is_relative_to(root):
                    Path(item["local"]).unlink()
                entries.append(manifest_entry(name, item, target, duration, rel))
                kept_bytes += 2560 + ((target.stat().st_size + 511) // 512) * 512
                if kept_bytes > source["reserve"]:
                    raise OSError("source exceeds its output allocation")
            if name == "disfluencyspeech":
                # Original transcripts are kept per row; the parquet is an intermediate.
                (root / "labels/data/test-00000-of-00001.parquet").unlink()

            for path in cache_files:
                path.unlink()
            RANGE_CACHE.clear()
            stage = "pack"
            sizes = sum(p.stat().st_size for p in out.iterdir() if p.is_file())
            projected = tar_size([p for p in root.rglob("*") if p.is_file()])
            if sizes + projected > OUTPUT_LIMIT - DISK_MARGIN:
                raise OSError("total output exceeds 18 GB allowance")
            if projected > TAR_LIMIT:
                raise OSError("source cannot fit the required single 4 GB tar")
            mapping, parts = pack_tar(root, out, name)
            for entry in entries:
                entry["archive"] = mapping[entry["audio_path"]]
                entry["label_files"] = [{"archive": mapping["labels/" + p], "path": "labels/" + p}
                                        for p in entry["label_files"]]
            result.update(complete=True, stage="complete", files=len(entries), parts=parts, entries=entries,
                          labels=provenance)
    except Exception as e:
        RANGE_CACHE.clear()
        for p in out.glob(name + "-*.tar"):
            p.unlink()
        result.update(stage=stage, error=f"{type(e).__name__}: {e}")
    log(f"{name}: {'complete' if result['complete'] else 'FAILED ' + result['stage']}; "
        f"files={result['files']}; {result['error'] or 'verified and packed'}")
    return result


def run_sources(plans, worker):
    results = []
    for plan in plans:
        if plan.get("error"):
            results.append({"source": plan["source"], "complete": False, "stage": plan["stage"], "error": plan["error"]})
            continue
        try:
            results.append(worker(plan))
        except Exception as e:
            results.append({"source": plan["source"], "complete": False, "stage": "source", "error": str(e)})
    return results


def main(argv=None):
    global LOGFILE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", choices=[s["id"] for s in SOURCES])
    parser.add_argument("--limit", type=int)
    parser.add_argument("--out", type=Path, default=Path("/kaggle/working"))
    args = parser.parse_args(argv)
    if not args.dry_run:
        args.out.mkdir(parents=True, exist_ok=True)
        LOGFILE = args.out / "fetch.log"
    if args.limit is not None and (args.limit < 1 or not args.only):
        raise ValueError("--limit must be positive and used with --only")
    sources = [s for s in SOURCES if (s["id"] == args.only if args.only else s["priority"] == 1 or PRIORITY2)]
    existing = sum(p.stat().st_size for p in args.out.iterdir() if p.is_file()) if args.out.is_dir() else 0
    sources, refused = budget_sources(sources, OUTPUT_LIMIT - DISK_MARGIN - existing)
    log(f"planned output cap={sum(s['reserve'] for s in sources):,} B; hard total={OUTPUT_LIMIT:,} B; "
        f"priority2={PRIORITY2}; sources={len(sources)}; refused={[s['id'] for s in refused]}")
    log("startup: " + ", ".join(f"{n}={'available' if shutil.which(n) else 'MISSING'}" for n in ("ffmpeg", "ffprobe"))
        + f"; pyarrow={'available' if importlib.util.find_spec('pyarrow') else 'absent (DisfluencySpeech and Expresso need it)'}")
    plans = dry_plan(sources)
    if args.dry_run:
        log(f"dry-run complete: checked={sum(not p['error'] for p in plans)}/{len(plans)}; "
            "no audio payloads downloaded; mounted audio enumerated only on Kaggle")
        return {"dry_run": True, "plans": plans, "audit": AUDIT}
    args.out.mkdir(parents=True, exist_ok=True)
    if any((args.out / f"{s['id']}-001.tar").exists() for s in sources):
        raise FileExistsError("source tar already exists; use a fresh --out directory")
    by_id = {s["id"]: s for s in sources}
    def worker(plan):
        result = source_fetch(by_id[plan["source"]], plan["audio"], plan["labels"], args.out, args.limit)
        # Save progress after every source, including failures.
        interim.append({k: v for k, v in result.items() if k != "entries"})
        (args.out / "STATUS.json").write_text(json.dumps({"complete": False, "sources": interim}, indent=1))
        return result
    interim = []
    results = run_sources(plans, worker)
    entries = [e for r in results for e in r.pop("entries", [])]
    for source in refused:
        results.append({"source": source["id"], "complete": False, "stage": "budget", "error": "output allocation does not fit"})
    status = {"schema": 1, "complete": all(r.get("complete", False) for r in results), "sources": results,
              "completed_sources": [r["source"] for r in results if r.get("complete")],
              "limit": args.limit, "subset_run": bool(args.only or args.limit), "url_checks": AUDIT}
    (args.out / "STATUS.json").write_text(json.dumps(status, indent=1) + "\n")
    (args.out / "manifest.json").write_text(json.dumps(entries, indent=1) + "\n")
    notices = ["# Source licences\n\nPrivate research output. No redistribution. Audio converted to 16 kHz mono PCM16.\n"]
    for source in sources:
        name, url, quote = LICENCES[source["id"]]
        notices.append(f"## {source['id']}\n\n{name}: {url}\n\n> {quote}\n")
    notices.append("Item-specific licence URLs appear in manifest.json. PodcastFillers original Adobe licence and episode licence CSV "
                   "are preserved in its tar; its metadata licence restricts use to academic research and teaching. "
                   "Original source metadata and author/citation notices are retained in the label files.\n")
    (args.out / "LICENSES.md").write_text("\n".join(notices))
    log(f"finished: complete={status['complete']}; audio={len(entries)}; "
        f"output={sum(p.stat().st_size for p in args.out.iterdir() if p.is_file()):,} B")
    return status


if __name__ == "__main__":
    # No exception escapes: a kernel that exits non-zero can lose its otherwise useful outputs.
    try:
        outcome = main()
        if outcome.get("dry_run") and any(p["error"] for p in outcome["plans"]):
            raise SystemExit(1)
    except Exception as exc:
        log(f"FAILED startup: {type(exc).__name__}: {exc}")
        if "--dry-run" not in sys.argv:
            try:
                out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else Path("/kaggle/working")
                out.mkdir(parents=True, exist_ok=True)
                (out / "STATUS.json").write_text(json.dumps({"complete": False, "sources": [],
                    "failures": [{"source": "startup", "stage": "startup", "error": str(exc)}]}, indent=1))
            except Exception:
                pass
    raise SystemExit(0)
