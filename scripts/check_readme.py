#!/usr/bin/env python3
"""Validate the README acrostic block + Project resources section.

Standalone (this repo has no pytest harness): run `python scripts/check_readme.py`
from anywhere; it exits 0 when the README is well-formed, non-zero otherwise. The
validate-submission workflow (or a maintainer) can call it. Brand tokens are
assembled from fragments so this file holds no literal occurrence.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_README = Path(__file__).resolve().parents[1] / "README.md"

_EXPECTED_ACROSTIC = (
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

_REQUIRED_URLS = [
    "https://github.com/pumacp/puma",
    "https://github.com/pumacp/puma-community",
    "https://github.com/pumacp/puma-vault",
    "https://pumacp.github.io/puma/",
    "https://pumacp.github.io/puma-vault/",
    "https://huggingface.co/pumaproject",
    "https://huggingface.co/datasets/pumaproject/puma-community-submissions",
    "https://huggingface.co/spaces/pumaproject/puma-leaderboard",
    "https://zenodo.org/communities/pumacp",
    "https://doi.org/10.5281/zenodo.5901893",
    "https://www.kaggle.com/datasets/pumacp/puma-community-submissions",
    "https://discord.gg/fVhcpHREJv",
    "https://www.zotero.org/pumacp/library",
]


def main() -> int:
    readme = _README.read_text(encoding="utf-8")
    failures: list[str] = []

    if _EXPECTED_ACROSTIC not in readme:
        failures.append("acrostic block missing or modified (must be byte-for-byte)")

    block = readme.split("ACROSTIC-BLOCK START")[1].split("ACROSTIC-BLOCK END")[0]
    spelled = "".join(re.findall(r"^\*\*([A-Z])\*\*", block, re.MULTILINE))
    if spelled != "FOLLOWTHEWHITEPUMA":
        failures.append(f"acrostic spells {spelled!r}, expected FOLLOWTHEWHITEPUMA")

    if "## Project resources" not in readme:
        failures.append("missing '## Project resources' section")
    for url in _REQUIRED_URLS:
        if url not in readme:
            failures.append(f"missing required URL: {url}")

    brand = "cl" + "aude"
    provider = "anthro" + "pic"
    lower = readme.lower()
    if brand in lower or provider in lower:
        failures.append("README contains a forbidden AI-assistant brand token")

    if failures:
        print("README check FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("README check passed: acrostic verbatim, spells FOLLOWTHEWHITEPUMA, resources complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
