"""Verify integrity of newly added submissions via the PUMA Verifier Space.

For each submission JSON added in the latest commit (HEAD~1..HEAD, excluding
*.verified.json), calls the Verifier Space and writes a sidecar
<id>.verified.json only when the Verifier reports ``verified``. Every other
status is logged and no sidecar is written. Existing submission files are
never re-verified.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from gradio_client import Client

VERIFIER_SPACE = "pumaproject/puma-verifier"


def added_submissions() -> list[Path]:
    """Return submission JSONs added in the latest commit.

    Raises ``subprocess.CalledProcessError`` when the diff cannot be computed
    (for example, no parent commit); the caller treats that as a failure
    instead of falling back to every file in ``submissions/``.
    """
    result = subprocess.run(
        [
            "git", "diff", "--name-only", "--diff-filter=A",
            "HEAD~1", "HEAD", "--", "submissions/",
        ],
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


def main() -> int:
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN not set", file=sys.stderr)
        return 1

    try:
        changes = added_submissions()
    except subprocess.CalledProcessError as e:
        print(
            f"ERROR: cannot list submissions added in HEAD~1..HEAD: {e.stderr.strip()}",
            file=sys.stderr,
        )
        return 1
    if not changes:
        print("No newly added submissions to verify.")
        return 0

    print(f"Found {len(changes)} submission(s) to verify.")
    client = Client(VERIFIER_SPACE, token=token)

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

        url = submission.get("raw_predictions_url") or ""
        integrity = submission.get("integrity") or {}
        declared = integrity.get("predictions_summary_hash") or ""

        try:
            result = client.predict(url, declared, api_name="/verify")
        except Exception as e:
            print(f"  ERROR calling verifier: {e}")
            exit_code = 1
            continue

        status = result.get("status")
        if status != "verified":
            print(f"  status={status}: {result.get('message', '')} (no sidecar written)")
            continue

        sidecar_path = submission_path.with_name(
            submission_path.stem + ".verified.json"
        )
        with open(sidecar_path, "w") as f:
            json.dump({
                "submission_id": submission.get(
                    "submission_id", submission_path.stem
                ),
                "verified": True,
                "status": status,
                "computed_hash": result["computed_hash"],
                "declared_hash": result["declared_hash"],
                "message": result["message"],
                "verifier_space": VERIFIER_SPACE,
            }, f, indent=2)
        print(f"  ✓ status={status} → {sidecar_path}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
