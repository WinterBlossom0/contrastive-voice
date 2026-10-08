#!/usr/bin/env bash
# Assemble the 'cvoice-project' dataset folder for `kaggle datasets create` / `version`: OUT_DIR/dataset-metadata.json and
# OUT_DIR/project/ with source, lockfile, manifest and transcripts; no virtual environment, no audio, no tests, no caches.
# (The files sit one level down because Kaggle zips each top-level directory of an upload.) Prints the upload commands.
#
#   scripts/stage_project.sh [OUT_DIR]        (default: build/cvoice-project inside the repository)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOP="${1:-$ROOT/build/cvoice-project}"
OUT="$TOP/project"

[ -f "$ROOT/uv.lock" ] || { echo "uv.lock missing: run 'uv lock' first" >&2; exit 1; }
[ -f "$ROOT/data/sources_manifest.json" ] || { echo "data/sources_manifest.json missing" >&2; exit 1; }

rm -rf "$TOP"
mkdir -p "$OUT/data"
cp "$ROOT/pyproject.toml" "$ROOT/uv.lock" "$OUT/"
[ -f "$ROOT/README.md" ] && cp "$ROOT/README.md" "$OUT/"
cp -r "$ROOT/src" "$OUT/src"
if [ -f "$ROOT/models/final_evaluations.json" ]; then  # the record of earlier final (test-split) evaluations: kaggle/run.py puts it beside detector.json
  mkdir -p "$OUT/models" && cp "$ROOT/models/final_evaluations.json" "$OUT/models/"
fi
cp "$ROOT/data/sources_manifest.json" "$OUT/data/"
cp -r "$ROOT/data/transcripts" "$OUT/data/transcripts"
find "$OUT" -name '__pycache__' -type d -prune -exec rm -rf {} +
find "$OUT" -name '*.pyc' -delete

cat > "$TOP/dataset-metadata.json" <<'JSON'
{"title": "cvoice-project", "id": "electroknight/cvoice-project", "licenses": [{"name": "CC0-1.0"}]}
JSON

# integrity list checked by kaggle/run.py before it copies the project to writable storage
( cd "$OUT" && find . -type f ! -name project_sha256.txt | sed 's|^\./||' | LC_ALL=C sort | xargs sha256sum > project_sha256.txt )

# no audio, no environment
if find "$OUT" \( -name '*.wav' -o -name '*.mp3' -o -name '*.ogg' -o -name '*.webm' -o -name '.venv' \) | grep -q .; then
  echo "audio or a virtual environment leaked into the staged folder" >&2; exit 1
fi
echo "staged $(wc -l < "$OUT/project_sha256.txt") files, $(du -sh "$OUT" | cut -f1), in $OUT"
echo
echo "first upload:  kaggle datasets create  -p '$TOP' --dir-mode zip --keep-tabular"
echo "new version:   kaggle datasets version -p '$TOP' --dir-mode zip --keep-tabular -m 'source snapshot'"
