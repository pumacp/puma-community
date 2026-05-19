#!/usr/bin/env python3
"""Mirror an archive of PUMA Community submissions to Zenodo.

Usage::

    python3 scripts/mirror_zenodo.py <archive.zip>

Reads the Zenodo personal access token from ``ZENODO_TOKEN`` and the API base
URL from ``ZENODO_BASE_URL`` (defaults to ``https://zenodo.org/api``; set to
``https://sandbox.zenodo.org/api`` for end-to-end testing without minting a
real DOI).

This script uses only the standard library to keep the runner's dependency
surface minimal. No ``requests``, no ``httpx``.
"""

from __future__ import annotations

import datetime as dt
import json
import logging
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

log = logging.getLogger("mirror_zenodo")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def _request(
    url: str,
    *,
    method: str,
    token: str,
    body: bytes | None = None,
    content_type: str = "application/json",
) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if body is not None:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        log.error("Zenodo %s %s failed: HTTP %d — %s", method, url, exc.code, detail)
        raise
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        log.error("usage: mirror_zenodo.py <archive.zip>")
        return 2
    archive = Path(argv[1])
    if not archive.is_file():
        log.error("archive not found: %s", archive)
        return 1

    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        log.error("ZENODO_TOKEN env var is not set")
        return 1
    base_url = os.environ.get("ZENODO_BASE_URL", "https://zenodo.org/api").rstrip("/")
    log.info("using Zenodo base URL %s", base_url)

    # 1. Create deposition draft.
    log.info("creating deposition draft")
    draft = _request(f"{base_url}/deposit/depositions", method="POST", token=token, body=b"{}")
    deposition_id = draft["id"]
    bucket_url = draft["links"]["bucket"]
    log.info("draft id=%s bucket=%s", deposition_id, bucket_url)

    # 2. Upload the archive to the bucket.
    log.info("uploading %s (%d bytes)", archive.name, archive.stat().st_size)
    with archive.open("rb") as fh:
        _request(
            f"{bucket_url}/{archive.name}",
            method="PUT",
            token=token,
            body=fh.read(),
            content_type="application/octet-stream",
        )

    # 3. Attach metadata.
    snapshot_date = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
    metadata = {
        "metadata": {
            "title": f"PUMA Community submissions snapshot {snapshot_date}",
            "upload_type": "dataset",
            "description": (
                "Snapshot of community-contributed local-LLM benchmark "
                "submissions from the PUMA Community public repository. "
                "Each file conforms to the published submission JSON Schema."
            ),
            "creators": [{"name": "PUMA Community contributors"}],
            "license": "MIT",
            "access_right": "open",
        }
    }
    log.info("attaching metadata")
    _request(
        f"{base_url}/deposit/depositions/{deposition_id}",
        method="PUT",
        token=token,
        body=json.dumps(metadata).encode("utf-8"),
    )

    # 4. Publish.
    log.info("publishing deposition")
    published = _request(
        f"{base_url}/deposit/depositions/{deposition_id}/actions/publish",
        method="POST",
        token=token,
        body=b"",
    )
    doi = published.get("doi", "<unknown>")
    log.info("published: DOI=%s", doi)
    print(doi)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
