#!/usr/bin/env bash
# Outputs computed after the final evaluation, on a local CPU, from the saved outputs of the final run: no number is measured
# on Kaggle again. The frozen detector is the run's models/detector.json (its sha256 is checked against the final record).
#   1. eval/addendum.{json,md}: python -m cvoice.addendum (re-runs the frozen detector on the saved audio).
#   2. eval/tables_rendered.md: tables.md re-rendered from results.json (python -m cvoice.evaluate render).
#   3. gallery/: the gallery rebuilt with the frozen detector from the saved dataset audio, then copied into the repository.
#
#   scripts/rebuild_after_final.sh [RUN_DIR] [FIRST_FINAL_RESULTS]
# RUN_DIR holds eval/, models/, calibration/ and data/dataset of the final run (default build/work/kaggle_runs/last_run/x).
# CVOICE_CACHE (default build/cache/after_final) keeps the word alignments between runs.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
RUN="${1:-build/work/kaggle_runs/last_run/x}"
FIRST="${2:-docs/evidence_final_32cdd86f3d6e/results.json}"
CACHE="${CVOICE_CACHE:-build/cache/after_final}"
OUT="build/gallery_after_final"
PY=.venv/bin/python

cmp -s "$RUN/models/detector.json" models/detector.json || { echo "the run's detector.json is not the repository's frozen detector" >&2; exit 1; }
mkdir -p "$CACHE"
$PY -m cvoice.addendum --run "$RUN" --first-final "$FIRST" --cache "$CACHE" --workers 4
$PY -m cvoice.evaluate render "$RUN/eval/results.json" "$RUN/eval/tables_rendered.md"
rm -rf "$OUT"
CVOICE_DEVICES=cpu CVOICE_WORKERS=3 $PY -m cvoice.gallery --dataset "$RUN/data/dataset" --models models/detector.json --cache "$CACHE" \
  --eval "$RUN/eval" --out "$OUT" \
  --note "rebuilt after the final evaluation on a local CPU with the frozen detector, from the saved dataset audio and eval outputs of the final run (scripts/rebuild_after_final.sh)"
rm -rf gallery
cp -r "$OUT/gallery" gallery
echo "gallery/ rebuilt from $RUN"
