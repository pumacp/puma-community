#!/usr/bin/env python3
"""Validate the Pages content + corporate-palette compliance.

Standalone (this repo has no pytest harness): run `python scripts/check_pages.py`
from anywhere; exits 0 when the docs site is well-formed, non-zero otherwise.
Mirrors scripts/check_readme.py. Scope = the pages published by the mkdocs nav.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_DOCS = _ROOT / "docs"

_PUBLIC_DOCS = [
    "index.md",
    "contributing.md",
    "submission-format.md",
    "mirrors-setup.md",
    "notifiers-setup.md",
    "maintainer-guide.md",
    "colab-demo.md",
]

# Lowercase Spanish function words, whole-word, case-sensitive — so acronyms
# like "PARA" (Projects-Areas-Resources-Archives) do not false-trigger.
_SPANISH = [
    "el", "la", "los", "las", "para", "este", "esta", "una", "del",
    "qué", "cómo", "cuál", "función", "propósito", "salida", "comando", "sintaxis",
]

_PALETTE_HEX = ("#000000", "#FFFFFF", "#FAFAFA", "#F5F5F5", "#0D0D0D")
_LANDING_SECTIONS = (
    "What is PUMA Community?",
    "The submission pipeline",
    "Submission format",
    "How to contribute",
    "Resources",
    "Citation",
)

_ACROSTIC = (
    "<!-- PUMA-ACROSTIC-BLOCK START — DO NOT MODIFY — IMMUTABLE -->\n"
    "---\n"
    "**F**ollowing empirical evidence, ICT project management faces triage, estimation, and learning inefficiencies.<br>\n"
    "**O**bserved widely, these persist despite abundant historical data.<br>\n"
    "**L**aying a rigorous foundation requires reproducible benchmarking.<br>\n"
    "**L**everaging labeled datasets enables systematic evaluation of LLM performance.<br>\n"
    "**O**utcomes are compared using quantitative metrics and statistical analysis.<br>\n"
    "**W**ith an incremental design, a minimal viable benchmark is defined.<br>\n"
    "**T**hrough open-source release, results become reproducible and verifiable.<br>\n"
    "**H**ence, the framework supports extensibility across models and tasks.<br>\n"
    "**E**ventually, it enables integration into real organizational settings.<br>\n"
    "**W**ithin ICT environments, recurring inefficiencies hinder effective decision-making.<br>\n"
    "**H**eterogeneous data sources complicate prioritization and estimation processes.<br>\n"
    "**I**n response, this work builds a reproducible LLM-based benchmark.<br>\n"
    "**T**he focus is on issue triage and story-point estimation tasks.<br>\n"
    "**E**valuation follows controlled experiments with statistical validation.<br>\n"
    "**P**rotocols ensure reproducibility through fixed parameters and configurations.<br>\n"
    "**U**sing carbon tracking, the framework measures energy impact.<br>\n"
    "**M**oreover, the MVP delivers a valid and original contribution.<br>\n"
    "**A**ll artefacts are released as open source for replication and extension.<br>\n"
    "---\n"
    "<!-- PUMA-ACROSTIC-BLOCK END -->"
)


def main() -> int:
    fail: list[str] = []
    index = (_DOCS / "index.md").read_text(encoding="utf-8")

    # extra.css palette tokens
    css = (_DOCS / "stylesheets" / "extra.css").read_text(encoding="utf-8").upper()
    for hexv in _PALETTE_HEX:
        if hexv not in css:
            fail.append(f"extra.css missing palette hex {hexv}")

    # mkdocs.yml palette must be monochrome (strip comments first)
    raw = (_ROOT / "mkdocs.yml").read_text(encoding="utf-8").lower()
    body = "\n".join(ln for ln in raw.splitlines() if not ln.lstrip().startswith("#"))
    for tok in ("deep orange", "deep-orange", "amber", "orange"):
        if tok in body:
            fail.append(f"mkdocs.yml palette contains '{tok}'")
    if re.search(r"\bred\b", body):
        fail.append("mkdocs.yml palette contains 'red'")

    # immutable acrostic, byte-for-byte
    if _ACROSTIC not in index:
        fail.append("landing page missing the immutable acrostic block")

    # landing section headings
    for heading in _LANDING_SECTIONS:
        if f"## {heading}" not in index:
            fail.append(f"landing page missing section '{heading}'")

    # no Spanish / Anexo in public docs
    for name in _PUBLIC_DOCS:
        text = (_DOCS / name).read_text(encoding="utf-8")
        if "anexo" in text.lower():
            fail.append(f"{name} contains an Anexo reference")
        for word in _SPANISH:
            if re.search(rf"\b{re.escape(word)}\b", text):
                fail.append(f"{name} contains Spanish word '{word}'")

    if fail:
        print("Pages check FAILED:")
        for f in fail:
            print(f"  - {f}")
        return 1
    print("Pages check passed: monochrome palette, immutable acrostic, sections present, English-only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
