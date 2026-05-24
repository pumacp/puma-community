"""Create a quarterly snapshot of PUMA Community on Zenodo.

Bundles submissions/, schema/, and the dataset card into a tarball,
creates a Zenodo deposit, uploads the tarball, sets metadata, publishes.

Uses ZENODO_BASE env var to switch between sandbox and production.
"""
from __future__ import annotations

import os
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import requests

ZENODO_BASE = os.environ.get("ZENODO_BASE", "https://zenodo.org/api")
COMMUNITY_ID = "pumacp"


def _quarter_label(ts: datetime) -> str:
    q = (ts.month - 1) // 3 + 1
    return f"{ts.year}-Q{q}"


def _make_tarball(repo_root: Path, dest: Path) -> None:
    with tarfile.open(dest, "w:gz") as tar:
        for entry in ("submissions", "schema"):
            p = repo_root / entry
            if p.exists():
                tar.add(p, arcname=entry)
        for filename, arcname in [
            ("docs/hf-dataset-card.md", "dataset_card.md"),
            ("README.md", "README.md"),
        ]:
            p = repo_root / filename
            if p.exists():
                tar.add(p, arcname=arcname)


def main() -> int:
    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        print("ERROR: ZENODO_TOKEN not set", file=sys.stderr)
        return 1

    headers = {"Authorization": f"Bearer {token}"}
    repo_root = Path(__file__).resolve().parent.parent
    now = datetime.now(timezone.utc)
    quarter = _quarter_label(now)
    sha = os.environ.get("GITHUB_SHA", "HEAD")[:7]

    print(f"Zenodo base: {ZENODO_BASE}")
    print(f"Quarter:     {quarter}")

    with tempfile.TemporaryDirectory() as tmpdir:
        tarball = Path(tmpdir) / f"puma-community-{quarter}.tar.gz"
        _make_tarball(repo_root, tarball)
        size_mb = tarball.stat().st_size / 1024 / 1024
        print(f"Tarball:     {tarball.name} ({size_mb:.2f} MB)")

        # 1. Create empty deposition
        r = requests.post(
            f"{ZENODO_BASE}/deposit/depositions",
            json={}, headers=headers, timeout=60,
        )
        r.raise_for_status()
        deposition = r.json()
        deposition_id = deposition["id"]
        bucket_url = deposition["links"]["bucket"]
        print(f"Deposition:  {deposition_id}")

        # 2. Upload tarball
        with open(tarball, "rb") as f:
            r = requests.put(
                f"{bucket_url}/{tarball.name}",
                data=f, headers=headers, timeout=300,
            )
            r.raise_for_status()
        print(f"Uploaded:    {tarball.name}")

        # 3. Set metadata
        metadata = {
            "metadata": {
                "title": f"PUMA Community Submissions — Snapshot {quarter}",
                "upload_type": "dataset",
                "description": (
                    "<p>Quarterly snapshot of community-contributed benchmark "
                    "results from <a href='https://github.com/pumacp/puma'>PUMA</a>, "
                    "an empirical evaluation platform for local LLM agents on "
                    "Project Management Office (PMO) tasks. Bundles all submissions, "
                    "the JSON schema, and the dataset card as of the snapshot date.</p>"
                    "<p>For the live (non-archival) dataset, see "
                    "<a href='https://huggingface.co/datasets/pumaproject/puma-community-submissions'>"
                    "Hugging Face</a>. For the live leaderboard, see "
                    "<a href='https://huggingface.co/spaces/pumaproject/puma-leaderboard'>"
                    "the PUMA Leaderboard Space</a>.</p>"
                ),
                "creators": [{
                    "name": "PUMA Project Contributors",
                    "affiliation": "Universitat Oberta de Catalunya",
                }],
                "keywords": [
                    "benchmark", "llm-evaluation", "project-management",
                    "local-llm", "sustainability", "issue-triage",
                    "effort-estimation",
                ],
                "communities": [{"identifier": COMMUNITY_ID}],
                "license": "CC-BY-4.0",
                "related_identifiers": [
                    {
                        "identifier": "https://github.com/pumacp/puma-community",
                        "relation": "isSupplementTo",
                        "resource_type": "software",
                    },
                    {
                        "identifier": "https://huggingface.co/datasets/pumaproject/puma-community-submissions",
                        "relation": "isAlternateIdentifier",
                        "resource_type": "dataset",
                    },
                ],
                "notes": f"Generated from puma-community@{sha} on {now.isoformat()}",
            }
        }
        r = requests.put(
            f"{ZENODO_BASE}/deposit/depositions/{deposition_id}",
            json=metadata,
            headers={**headers, "Content-Type": "application/json"},
            timeout=60,
        )
        r.raise_for_status()
        print("Metadata:    set")

        # 4. Publish
        r = requests.post(
            f"{ZENODO_BASE}/deposit/depositions/{deposition_id}/actions/publish",
            headers=headers, timeout=60,
        )
        r.raise_for_status()
        published = r.json()
        doi = published.get("doi") or published.get("metadata", {}).get("doi", "")
        record_url = published.get("links", {}).get("record_html", "")
        print(f"✓ Published: DOI={doi}")
        print(f"             URL={record_url}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
