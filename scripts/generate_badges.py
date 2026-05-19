#!/usr/bin/env python3
"""Generate badge JSONs for PUMA Community.

Reads all submission files under ``<submissions_dir>`` and emits four
shields.io endpoint JSONs under ``<badges_dir>``::

    submission-count.json   { label: submissions, message: <n>, color: blue }
    models-count.json       { label: models,      message: <n>, color: purple }
    scenarios-count.json    { label: scenarios,   message: <n>, color: green }
    latest-submission.json  { label: latest,      message: <YYYY-MM-DD>, color: orange }

Usage::

    python3 scripts/generate_badges.py [<submissions_dir>] [<badges_dir>]

Defaults: ``./submissions`` and ``./badges``. Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

log = logging.getLogger("generate_badges")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

_DIR_MODE: int = 0o755


def _parse_iso_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        log.warning("ignoring malformed timestamp %r", value)
        return None


def _extract_fields(payload: dict) -> tuple[str | None, str | None, datetime | None]:
    """Return ``(model, scenario, completed_dt)`` for a single submission."""
    rm = payload.get("run_metadata") or payload.get("run") or {}
    model = rm.get("model")
    scenario = rm.get("scenario")
    completed = rm.get("completed_at") or rm.get("finished_at") or rm.get("started_at")
    ts = _parse_iso_date(str(completed)) if completed else None
    return model, scenario, ts


def _write_badge(target: Path, label: str, message: str, color: str) -> None:
    payload = {
        "schemaVersion": 1,
        "label": label,
        "message": message,
        "color": color,
    }
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    tmp.replace(target)


def generate(submissions_dir: Path, badges_dir: Path) -> int:
    badges_dir.mkdir(parents=True, exist_ok=True)
    try:
        badges_dir.chmod(_DIR_MODE)
    except OSError as exc:  # pragma: no cover — Windows or restricted FS
        log.debug("could not chmod badges dir: %s", exc)

    files: list[Path] = []
    if submissions_dir.is_dir():
        files = sorted(p for p in submissions_dir.glob("*.json") if p.is_file())

    models: set[str] = set()
    scenarios: set[str] = set()
    latest: datetime | None = None
    counted = 0

    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            log.warning("skipping unreadable file %s: %s", path.name, exc)
            continue
        model, scenario, ts = _extract_fields(payload)
        if model:
            models.add(model)
        if scenario:
            scenarios.add(scenario)
        if ts is not None and (latest is None or ts > latest):
            latest = ts
        counted += 1

    latest_message = latest.strftime("%Y-%m-%d") if latest is not None else "none"

    _write_badge(badges_dir / "submission-count.json", "submissions", str(counted), "blue")
    _write_badge(badges_dir / "models-count.json", "models", str(len(models)), "purple")
    _write_badge(badges_dir / "scenarios-count.json", "scenarios", str(len(scenarios)), "green")
    _write_badge(badges_dir / "latest-submission.json", "latest", latest_message, "orange")

    log.info(
        "wrote 4 badges to %s (submissions=%d, models=%d, scenarios=%d, latest=%s)",
        badges_dir,
        counted,
        len(models),
        len(scenarios),
        latest_message,
    )
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "submissions_dir",
        nargs="?",
        type=Path,
        default=Path("submissions"),
    )
    parser.add_argument(
        "badges_dir",
        nargs="?",
        type=Path,
        default=Path("badges"),
    )
    args = parser.parse_args(argv)
    try:
        return generate(args.submissions_dir, args.badges_dir)
    except OSError as exc:
        log.error("filesystem error: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
