#!/usr/bin/env python3
"""Defense-in-depth: assert the PUBLISHED site exposes no maintainer-only pages
or sensitive references, while those pages remain tracked in git for maintainers.

Builds the mkdocs site to a temp dir (via `python -m mkdocs`) and inspects the
output. If mkdocs is unavailable, falls back to a source-level check (nav +
exclude_docs + index.md). Run: `python scripts/check_no_sensitive_pages.py`.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_DOCS = _ROOT / "docs"

_MAINTAINER_PAGES = ["mirrors-setup", "notifiers-setup", "maintainer-guide"]
_SENSITIVE = [
    "private endpoint",
    "puma-verifier",
    "HF_TOKEN",
    "ZENODO_TOKEN",
    "KAGGLE_KEY",
    "DISCORD_WEBHOOK",
    "TELEGRAM_BOT_TOKEN",
]


def _fail(messages: list[str]) -> int:
    if messages:
        print("Sensitive-pages check FAILED:")
        for m in messages:
            print(f"  - {m}")
        return 1
    print("Sensitive-pages check passed: maintainer pages unpublished, index.html clean, sources preserved.")
    return 0


def main() -> int:
    fail: list[str] = []

    # 1. Maintainer pages must remain on disk (git tracking preserved).
    for page in _MAINTAINER_PAGES:
        if not (_DOCS / f"{page}.md").is_file():
            fail.append(f"maintainer source missing (should stay tracked): docs/{page}.md")

    # 2. Build the site and inspect the published output.
    with tempfile.TemporaryDirectory() as tmp:
        site = Path(tmp) / "site"
        built = subprocess.run(
            [sys.executable, "-m", "mkdocs", "build", "-d", str(site), "--quiet"],
            cwd=_ROOT,
            capture_output=True,
            text=True,
        )
        if built.returncode == 0:
            for page in _MAINTAINER_PAGES:
                if (site / page / "index.html").exists():
                    fail.append(f"maintainer page is PUBLISHED in the built site: {page}/")
            index_html = (site / "index.html").read_text(encoding="utf-8")
            for token in _SENSITIVE:
                if token.lower() in index_html.lower():
                    fail.append(f"published index.html contains sensitive token: '{token}'")
            return _fail(fail)

    # 3. Fallback (no mkdocs): source-level equivalent.
    print("note: mkdocs unavailable — using source-level checks.")
    mkdocs_yml = (_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    for page in _MAINTAINER_PAGES:
        if f"{page}.md" not in mkdocs_yml.split("exclude_docs:")[-1]:
            fail.append(f"{page}.md not in exclude_docs")
        if f"{page}.md" in mkdocs_yml.split("exclude_docs:")[0]:
            fail.append(f"{page}.md still referenced in nav")
    index_md = (_DOCS / "index.md").read_text(encoding="utf-8")
    for token in _SENSITIVE:
        if token.lower() in index_md.lower():
            fail.append(f"docs/index.md contains sensitive token: '{token}'")
    return _fail(fail)


if __name__ == "__main__":
    sys.exit(main())
