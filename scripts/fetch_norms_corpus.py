"""Download, verify and extract the LibriTTS subsets that models/duration_norms.json is fitted on.

LibriTTS (Zen et al. 2019, arXiv:1904.02882), OpenSLR resource SLR60, https://www.openslr.org/60/ : the page states
"License: CC BY 4.0" (https://creativecommons.org/licenses/by/4.0/). Use requires attribution: cite the paper and name
the source. The audio derives from LibriVox recordings (public domain) and the text from Project Gutenberg.

    python scripts/fetch_norms_corpus.py --dest build/work/norms/corpus [--subsets dev-clean test-clean]

Each archive is checked against the MD5 that the OpenSLR page publishes and the SHA-256 recorded here before it is
extracted. Extraction refuses links, absolute paths and paths outside the destination (tarfile 'data' filter).
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import tarfile
import urllib.request
from pathlib import Path

PAGE = "https://www.openslr.org/60/"
MIRRORS = ("https://www.openslr.org/resources/60", "https://openslr.elda.org/resources/60",
           "https://openslr.trmal.net/resources/60")
ATTEMPTS = 20
ARCHIVES = {
    "dev-clean": {"file": "dev-clean.tar.gz", "md5": "0c3076c1e5245bb3f0af7d82087ee207", "sha256": "da0864e1bd26debed35da8a869dd5c04dfc27682921936de7cff9c8a254dbe1a",
                  "bytes": 1291469655},
    "test-clean": {"file": "test-clean.tar.gz", "md5": "7bed3bdb047c4c197f1ad3bc412db59f", "sha256": "234ea5b25859102a87024a4b9b86641f5b5aaaf1197335c95090cde04fe9a4f5",
                   "bytes": 1230670113},
}


def digests(path: Path) -> tuple[str, str]:
    md5, sha = hashlib.md5(), hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            md5.update(block)
            sha.update(block)
    return md5.hexdigest(), sha.hexdigest()


def verify(path: Path, spec: dict) -> None:
    if path.stat().st_size != spec["bytes"]:
        raise RuntimeError(f"{path.name}: {path.stat().st_size} bytes, expected {spec['bytes']}")
    md5, sha = digests(path)
    if md5 != spec["md5"] or sha != spec["sha256"]:
        raise RuntimeError(f"{path.name}: md5 {md5} / sha256 {sha} differ from the pinned md5 {spec['md5']} / sha256 {spec['sha256']}")


def download(name: str, archives: Path) -> Path:
    spec = ARCHIVES[name]
    path = archives / spec["file"]
    if path.exists() and path.stat().st_size == spec["bytes"]:
        verify(path, spec)
        return path
    archives.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(".part")
    errors = []
    # A stalled connection raises after the socket timeout; the next attempt resumes the partial file (HTTP Range).
    for attempt in range(ATTEMPTS):
        url = f"{MIRRORS[attempt % len(MIRRORS)]}/{spec['file']}"
        have = partial.stat().st_size if partial.exists() else 0
        try:
            print(f"download {url} from byte {have}", flush=True)
            request = urllib.request.Request(url, headers={"Range": f"bytes={have}-"} if have else {})
            with urllib.request.urlopen(request, timeout=60) as response:
                mode = "ab" if have and response.status == 206 else "wb"
                with open(partial, mode) as out:
                    shutil.copyfileobj(response, out, 1 << 22)
            if partial.stat().st_size < spec["bytes"]:
                raise OSError(f"connection closed at byte {partial.stat().st_size} of {spec['bytes']}")
            partial.replace(path)
            verify(path, spec)
            return path
        except (OSError, RuntimeError) as e:
            errors.append(f"{url}: {e}")
            if path.exists():
                path.unlink()  # a complete file that failed verification is not resumed
    raise RuntimeError("no mirror gave a verified archive:\n" + "\n".join(errors))


def extract(path: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(path, "r:gz") as tar:
        tar.extractall(dest, filter="data")


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dest", type=Path, required=True, help="extraction folder (LibriTTS/<subset>/ is created in it)")
    ap.add_argument("--archives", type=Path, default=None, help="folder for the downloaded archives (default: DEST/archives)")
    ap.add_argument("--subsets", nargs="+", default=list(ARCHIVES), choices=list(ARCHIVES))
    ap.add_argument("--verify-only", action="store_true", help="check the archives that are present; no download, no extraction")
    a = ap.parse_args(argv)
    archives = a.archives or a.dest / "archives"
    for name in a.subsets:
        if a.verify_only:
            verify(archives / ARCHIVES[name]["file"], ARCHIVES[name])
            print(f"{name}: verified")
            continue
        path = download(name, archives)
        extract(path, a.dest)
        print(f"{name}: verified and extracted to {a.dest / 'LibriTTS' / name}")


if __name__ == "__main__":
    main()
