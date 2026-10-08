#!/usr/bin/env bash
# Build from any working directory; the six-page limit includes figures and references.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

for command in pandoc tectonic pdfinfo; do
  command -v "$command" >/dev/null || { echo "Required PDF tool missing: $command" >&2; exit 1; }
done
pandoc docs/technical.md -o docs/technical.pdf --pdf-engine=tectonic --resource-path=docs:.
pages="$(pdfinfo docs/technical.pdf | awk '/^Pages:/ {print $2}')"
if [[ ! "$pages" =~ ^[0-9]+$ ]]; then
  echo "Could not read the page count of docs/technical.pdf." >&2
  exit 1
fi
if (( pages > 6 )); then
  echo "PDF rejected: $pages pages; the hackathon maximum is 6 including figures and references." >&2
  exit 1
fi
echo "Built docs/technical.pdf: $pages pages (maximum 6)."
