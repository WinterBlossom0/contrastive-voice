import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = ["README.md", "docs/technical.md", "docs/PAPERS.md"]
MARKDOWN_LINK = re.compile(r"\]\(([^)\s]+)\)")
# Code spans that name a repository path; other code spans are commands or identifiers.
PATH_SPAN = re.compile(r"`((?:docs|gallery|models|scripts|src|data|kaggle|tests)/[^`\s]*)`")
# scripts/import_run.sh creates these folders; the README names them as outputs, not as files in the repository.
CREATED_BY_IMPORT = {"docs/evidence/", "data/dataset/"}


def local_targets(document: Path) -> list[Path]:
    text = document.read_text()
    targets = []
    for link in MARKDOWN_LINK.findall(text):
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        targets.append(document.parent / link.split("#")[0])
    # Code spans name paths from the repository root, as the reader runs commands from there.
    targets += [ROOT / span for span in PATH_SPAN.findall(text) if not any(mark in span for mark in "*{<") and span not in CREATED_BY_IMPORT]
    return targets


@pytest.mark.parametrize("name", DOCUMENTS)
def test_every_local_link_resolves(name):
    missing = [str(target.relative_to(ROOT)) for target in local_targets(ROOT / name) if not target.resolve().exists()]
    assert not missing, f"{name} links to missing files: {missing}"
