#!/usr/bin/env bash
# Copy the outputs of one Kaggle run (the folder holding STATUS.json and the cvoice-build-part-*.zip files) into the
# repository tree: data/dataset/, models/, gallery/, docs/evidence/. Refuses a run that is incomplete or fails its checksums.
# If docs/evidence/ holds a final (test-split) evaluation it is first moved to docs/evidence_final_<config>/.
#
#   scripts/import_run.sh RUN_DIR
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN="$(cd "${1:?usage: scripts/import_run.sh RUN_DIR}" && pwd)"

( cd "$RUN" && sha256sum -c --quiet SHA256SUMS )
python3 -c "import json,sys; s=json.load(open(sys.argv[1])); sys.exit(0 if s.get('complete') and not s.get('failed_stages') else 'run is not complete: '+str(s.get('failed_stages')))" "$RUN/STATUS.json"

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
for z in "$RUN"/*.zip; do unzip -qo "$z" -d "$TMP"; done

# the record of final evaluations only grows: a run whose record lacks an entry of the repository's record is refused
python3 - "$ROOT/models/final_evaluations.json" "$TMP/models/final_evaluations.json" <<'PY'
import json, os, sys
have, new = sys.argv[1:]
if os.path.exists(have) and os.path.exists(new):
    lost = set(json.load(open(have))) - set(json.load(open(new)))
    if lost:
        sys.exit(f"the run's final_evaluations.json lacks earlier final evaluations {sorted(k[:12] for k in lost)}: not imported")
PY

# the evidence of an earlier final (test-split) evaluation is kept beside the new one, with the detector it was run with
if [ -f "$ROOT/docs/evidence/results.json" ]; then
  old="$(python3 -c "import json,sys; r=json.load(open(sys.argv[1])); print(r['detector_config_sha256'][:12] if r.get('final') else '')" "$ROOT/docs/evidence/results.json")"
  if [ -n "$old" ] && [ ! -e "$ROOT/docs/evidence_final_$old" ]; then
    mv "$ROOT/docs/evidence" "$ROOT/docs/evidence_final_$old"
    cp "$ROOT/models/detector.json" "$ROOT/docs/evidence_final_$old/detector.json"
  fi
fi
rm -rf "$ROOT/data/dataset" "$ROOT/gallery" "$ROOT/docs/evidence"
mkdir -p "$ROOT/models" "$ROOT/docs/evidence"
cp -r "$TMP/data/dataset" "$ROOT/data/dataset"
cp -r "$TMP/gallery" "$ROOT/gallery"
cp "$TMP"/models/*.json "$ROOT/models/"
cp -r "$TMP/eval/." "$ROOT/docs/evidence/"
cp -r "$TMP/calibration" "$ROOT/docs/evidence/calibration"
cp "$RUN/STATUS.json" "$ROOT/docs/evidence/STATUS.json"

echo "imported: $(find "$ROOT/data/dataset" -type f | wc -l) dataset files ($(du -sh "$ROOT/data/dataset" | cut -f1)), detector $(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['config_sha256'][:12])" "$ROOT/models/detector.json"), gallery $(ls "$ROOT/gallery/results" | wc -l) examples"
