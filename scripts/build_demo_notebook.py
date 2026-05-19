#!/usr/bin/env python3
"""Build the PUMA Community demo notebook (.ipynb) for Colab.

Generates a paste-and-run notebook that demonstrates how to download the v1
schema, validate a sample submission, inspect metrics and sustainability
data, and browse all PUMA Community submissions via the anonymous GitHub
API.

Usage::

    python3 scripts/build_demo_notebook.py [--output PATH]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCHEMA_RAW_URL = (
    "https://raw.githubusercontent.com/pumacp/puma-community/main/"
    "schema/submission.v1.json"
)
SAMPLE_RAW_URL = (
    "https://raw.githubusercontent.com/pumacp/puma-community/main/"
    "notebooks/sample_submission.json"
)
CONTRIBUTING_URL = (
    "https://github.com/pumacp/puma-community/blob/main/CONTRIBUTING.md"
)


def md(*lines: str) -> dict[str, Any]:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": list(lines),
    }


def code(*lines: str) -> dict[str, Any]:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": list(lines),
    }


def build_notebook() -> dict[str, Any]:
    cells: list[dict[str, Any]] = []

    cells.append(
        md(
            "# PUMA Community — Quick Demo\n",
            "\n",
            "Run-anywhere browser demo: no installation, no tokens, no account required.\n",
        )
    )
    cells.append(
        md(
            "## What you'll learn\n",
            "\n",
            "- How a PUMA submission is structured\n",
            "- How to validate a submission against the v1 schema\n",
            "- How to inspect metrics and sustainability data\n",
            "- How to browse all community submissions\n",
            "- How to submit your own results\n",
        )
    )

    cells.append(
        md(
            "### Step 1: Install dependencies\n",
            "\n",
            "Only `jsonschema` is required; everything else is in the Python "
            "standard library.\n",
        )
    )
    cells.append(code("!pip install --quiet jsonschema==4.23.0\n"))

    cells.append(
        md(
            "### Step 2: Download the v1 schema\n",
            "\n",
            "The schema is hosted in the public repository and can be "
            "fetched anonymously.\n",
        )
    )
    cells.append(
        code(
            "import urllib.request\n",
            "\n",
            f"SCHEMA_URL = '{SCHEMA_RAW_URL}'\n",
            "urllib.request.urlretrieve(SCHEMA_URL, 'submission.v1.json')\n",
            "print('Downloaded schema')\n",
        )
    )

    cells.append(
        md(
            "### Step 3: Load a sample submission\n",
            "\n",
            "This demo uses a deterministic placeholder submission so you can "
            "see what every field looks like in practice. Field paths follow "
            "the schema: top-level run metadata lives under `run_metadata`.\n",
        )
    )
    cells.append(
        code(
            "import json\n",
            "import urllib.request\n",
            "\n",
            f"SAMPLE_URL = '{SAMPLE_RAW_URL}'\n",
            "urllib.request.urlretrieve(SAMPLE_URL, 'sample_submission.json')\n",
            "\n",
            "with open('sample_submission.json') as fh:\n",
            "    submission = json.load(fh)\n",
            "\n",
            "rm = submission['run_metadata']\n",
            "print('submission_id:', submission['submission_id'])\n",
            "print('scenario     :', rm['scenario'])\n",
            "print('model        :', rm['model'])\n",
            "print('strategy     :', rm['strategy'])\n",
            "print('submitter    :', submission['submitter']['name_or_alias'])\n",
        )
    )

    cells.append(
        md(
            "### Step 4: Validate the submission\n",
            "\n",
            "`jsonschema.validate()` raises `ValidationError` on the first "
            "schema-failure and returns `None` on success.\n",
        )
    )
    cells.append(
        code(
            "import json\n",
            "import jsonschema\n",
            "\n",
            "with open('submission.v1.json') as fh:\n",
            "    schema = json.load(fh)\n",
            "\n",
            "jsonschema.validate(submission, schema)\n",
            "print('Submission is valid against schema v1.0.0')\n",
        )
    )

    cells.append(
        md(
            "### Step 5: Inspect metrics and sustainability\n",
            "\n",
            "Only non-null metrics are reported. The schema guarantees at "
            "least one of `f1_macro`, `mae`, or `accuracy` is present.\n",
        )
    )
    cells.append(
        code(
            "print('--- Metrics ---')\n",
            "for key, value in submission['metrics'].items():\n",
            "    if value is None:\n",
            "        continue\n",
            "    print(f'{key:<24s} {value}')\n",
            "\n",
            "print()\n",
            "print('--- Sustainability ---')\n",
            "for key, value in submission['sustainability'].items():\n",
            "    print(f'{key:<24s} {value}')\n",
            "\n",
            "print()\n",
            "print('--- Integrity ---')\n",
            "print('predictions_summary_hash:',\n",
            "      submission['integrity']['predictions_summary_hash'][:12], '...')\n",
        )
    )

    cells.append(
        md(
            "### Step 6: Browse all PUMA Community submissions\n",
            "\n",
            "The GitHub Contents API serves the `submissions/` directory "
            "anonymously. Note: the anonymous rate limit is **60 requests "
            "per hour per IP**; pass a `Authorization` header in production "
            "uses.\n",
        )
    )
    cells.append(
        code(
            "import json\n",
            "import urllib.request\n",
            "\n",
            "req = urllib.request.Request(\n",
            "    'https://api.github.com/repos/pumacp/puma-community/contents/submissions',\n",
            "    headers={'Accept': 'application/vnd.github+json'},\n",
            ")\n",
            "with urllib.request.urlopen(req) as resp:\n",
            "    contents = json.load(resp)\n",
            "\n",
            "files = [c['name'] for c in contents if c['name'].endswith('.json')]\n",
            "print(f'Found {len(files)} submissions:')\n",
            "for f in files[:10]:\n",
            "    print(f'  - {f}')\n",
        )
    )

    cells.append(
        md(
            "### Step 7: Submit your own results\n",
            "\n",
            "The recommended path is the PUMA tool's built-in command "
            "`puma share-results`. It builds the payload from your local "
            "SQLite results, validates the schema, scans for personal data, "
            "computes the integrity hash, forks the repository, creates a "
            "branch, commits the JSON file, and opens the Pull Request — "
            "all in one command.\n",
            "\n",
            f"See [CONTRIBUTING.md]({CONTRIBUTING_URL}) for the full guide, "
            "including the manual submission path for advanced users.\n",
        )
    )

    cells.append(
        md(
            "---\n",
            "\n",
            "**Further reading**\n",
            "\n",
            "- Schema reference: <https://github.com/pumacp/puma-community/blob/main/schema/submission.v1.json>\n",
            "- Wiki: <https://github.com/pumacp/puma-community/wiki>\n",
            "- Maintainer guide: <https://github.com/pumacp/puma-community/blob/main/docs/maintainer-guide.md>\n",
        )
    )

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.11.0"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return notebook


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("notebooks/puma_community_demo.ipynb"),
        help="output path for the generated notebook",
    )
    args = parser.parse_args(argv)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    notebook = build_notebook()
    args.output.write_text(json.dumps(notebook, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {args.output} ({len(notebook['cells'])} cells)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
