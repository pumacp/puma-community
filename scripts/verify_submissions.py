"""Verify integrity of new/changed submissions via the PUMA Verifier Space.

For each submission JSON in the latest diff (excluding *.verified.json),
calls the private Verifier Space and writes a sidecar <id>.verified.json.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from gradio_client import Client

VERIFIER_SPACE = "pumaproject/puma-verifier"
SUBMISSIONS_DIR = Path("submissions")


def changed_submissions() -> list[Path]:
    """Return submission JSONs added/modified in the latest commit."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD", "--", "submissions/"],
            capture_output=True, text=True, check=True,
        )
        paths = []
        for line in result.stdout.splitlines():
            if line.endswith(".verified.json") or not line.endswith(".json"):
                continue
            p = Path(line)
            if p.exists():
                paths.append(p)
        return paths
    except subprocess.CalledProcessError:
        return [
            p for p in SUBMISSIONS_DIR.glob("*.json")
            if not p.name.endswith(".verified.json")
        ]


def main() -> int:
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN not set", file=sys.stderr)
        return 1

    changes = changed_submissions()
    if not changes:
        print("No new/changed submissions to verify.")
        return 0

    print(f"Found {len(changes)} submission(s) to verify.")
    client = Client(VERIFIER_SPACE, hf_token=token)

    exit_code = 0
    for submission_path in changes:
        print(f"\n→ {submission_path}")
        try:
            with open(submission_path) as f:
                submission = json.load(f)
        except Exception as e:
            print(f"  ERROR reading: {e}")
            exit_code = 1
            continue

        url = submission.get("raw_predictions_url", "")
        declared = submission.get("predictions_summary_hash", "")

        try:
            result = client.predict(url, declared, api_name="/verify")
        except Exception as e:
            print(f"  ERROR calling verifier: {e}")
            exit_code = 1
            continue

        sidecar_path = submission_path.with_name(
            submission_path.stem + ".verified.json"
        )
        with open(sidecar_path, "w") as f:
            json.dump({
                "submission_id": submission.get(
                    "submission_id", submission_path.stem
                ),
                "verified": result["status"] == "verified",
                "status": result["status"],
                "computed_hash": result["computed_hash"],
                "declared_hash": result["declared_hash"],
                "message": result["message"],
                "verifier_space": VERIFIER_SPACE,
            }, f, indent=2)
        print(f"  ✓ status={result['status']} → {sidecar_path}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
