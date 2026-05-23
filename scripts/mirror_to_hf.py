"""Mirror PUMA community submissions to Hugging Face Dataset Hub.

Reads from the local repo (submissions/, schema/, docs/hf-dataset-card.md)
and pushes to pumaproject/puma-community-submissions.

Idempotent: upload_folder/upload_file only commit files whose content changed.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from huggingface_hub import HfApi

REPO_ID = "pumaproject/puma-community-submissions"
REPO_TYPE = "dataset"

# (local path, path inside HF dataset repo)
FOLDERS = [
    ("submissions", "submissions"),
    ("schema", "schema"),
]
DATASET_CARD_SRC = Path("docs/hf-dataset-card.md")
DATASET_CARD_DST = "README.md"  # HF datasets render README.md as the card


def main() -> int:
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN environment variable not set", file=sys.stderr)
        return 1

    api = HfApi(token=token)
    repo_root = Path(__file__).resolve().parent.parent
    sha = os.environ.get("GITHUB_SHA", "HEAD")[:7]

    something_uploaded = False

    for src_name, dst_name in FOLDERS:
        src_path = repo_root / src_name
        if not src_path.exists() or not any(src_path.iterdir()):
            print(f"SKIP: {src_name}/ is empty or does not exist locally")
            continue
        print(f"UPLOAD: {src_name}/ -> {REPO_ID}:{dst_name}/")
        api.upload_folder(
            folder_path=str(src_path),
            path_in_repo=dst_name,
            repo_id=REPO_ID,
            repo_type=REPO_TYPE,
            commit_message=f"chore: sync {dst_name}/ from puma-community@{sha}",
            ignore_patterns=["*.pyc", "__pycache__/*", ".DS_Store"],
        )
        something_uploaded = True

    card_path = repo_root / DATASET_CARD_SRC
    if card_path.exists():
        print(f"UPLOAD: {DATASET_CARD_SRC} -> {REPO_ID}:{DATASET_CARD_DST}")
        api.upload_file(
            path_or_fileobj=str(card_path),
            path_in_repo=DATASET_CARD_DST,
            repo_id=REPO_ID,
            repo_type=REPO_TYPE,
            commit_message=f"docs: sync dataset card from puma-community@{sha}",
        )
        something_uploaded = True
    else:
        print(f"SKIP: {DATASET_CARD_SRC} does not exist locally")

    if not something_uploaded:
        print("Nothing to upload yet.")
    print("✓ Mirror complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
