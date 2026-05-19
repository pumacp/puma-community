#!/usr/bin/env python3
"""Send a notification about a PUMA Community submission to Discord or Telegram.

Usage::

    python3 scripts/notify.py --channel discord  --submission-file <path>
    python3 scripts/notify.py --channel telegram --submission-file <path>

Environment variables read (per channel):
    discord:  ``DISCORD_WEBHOOK_URL``
    telegram: ``TELEGRAM_BOT_TOKEN``, ``TELEGRAM_CHAT_ID``

The script never prints, logs, or returns any token / webhook URL value.
Diagnostics use the :func:`mask` helper, which exposes only the first four
and last four characters.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

log = logging.getLogger("notify")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

REPO_URL_PREFIX = "https://github.com/pumacp/puma-community/blob/main/submissions/"
TELEGRAM_API_HOST = "https://api.telegram.org"


class NotificationError(Exception):
    """Non-2xx response or transport failure from the target service."""


def mask(value: str) -> str:
    if not value:
        return "***"
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}...{value[-4:]}"


def _http_post(url: str, payload: dict) -> None:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.getcode()
            if status < 200 or status >= 300:
                raise NotificationError(f"unexpected status {status}")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise NotificationError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise NotificationError(f"transport error: {exc.reason}") from exc


def _format_fields(submission: dict) -> tuple[list[dict], list[str]]:
    """Return Discord-style fields and Telegram-style bullet lines."""
    metrics = submission.get("metrics") or {}
    sustainability = submission.get("sustainability") or {}
    fields: list[dict] = []
    bullets: list[str] = []

    f1 = metrics.get("f1_macro")
    if f1 is not None:
        fields.append({"name": "F1 macro", "value": f"{f1:.4f}", "inline": True})
        bullets.append(f"- F1 macro: {f1:.4f}")

    mae = metrics.get("mae")
    if mae is not None:
        fields.append({"name": "MAE", "value": f"{mae:.2f} SP", "inline": True})
        bullets.append(f"- MAE: {mae:.2f} SP")

    co2 = sustainability.get("co2_grams_total")
    if co2 is not None:
        fields.append({"name": "CO2", "value": f"{co2:.2f} g", "inline": True})
        bullets.append(f"- CO2: {co2:.2f} g")

    return fields, bullets


def _build_discord_payload(submission: dict) -> dict:
    submission_id = str(submission["submission_id"])
    short = submission_id[:12]
    rm = submission.get("run_metadata") or {}
    scenario = rm.get("scenario", "?")
    model = rm.get("model", "?")
    strategy = rm.get("strategy", "?")
    alias = (submission.get("submitter") or {}).get("name_or_alias", "?")
    url = f"{REPO_URL_PREFIX}{submission_id}.json"
    fields, _ = _format_fields(submission)
    return {
        "content": f"New PUMA Community submission: `{short}`",
        "embeds": [
            {
                "title": f"Submission {short}",
                "url": url,
                "description": f"{scenario} / {model} / {strategy} — submitted by {alias}",
                "fields": fields,
            }
        ],
    }


def _build_telegram_payload(submission: dict, chat_id: str) -> dict:
    submission_id = str(submission["submission_id"])
    short = submission_id[:12]
    rm = submission.get("run_metadata") or {}
    scenario = rm.get("scenario", "?")
    model = rm.get("model", "?")
    strategy = rm.get("strategy", "?")
    alias = (submission.get("submitter") or {}).get("name_or_alias", "?")
    url = f"{REPO_URL_PREFIX}{submission_id}.json"
    _, bullets = _format_fields(submission)
    metrics_block = "\n".join(bullets) if bullets else "- (no scalar metrics)"
    text = (
        "*New PUMA Community submission*\n\n"
        f"ID: `{short}`\n"
        f"Scenario: `{scenario}`\n"
        f"Model: `{model}`\n"
        f"Strategy: `{strategy}`\n"
        f"Submitter: `{alias}`\n\n"
        f"{metrics_block}\n\n"
        f"[View on GitHub]({url})"
    )
    return {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}


def _send_discord(submission: dict) -> None:
    webhook = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook:
        raise NotificationError("DISCORD_WEBHOOK_URL is not set")
    log.info("posting to Discord webhook %s", mask(webhook))
    _http_post(webhook, _build_discord_payload(submission))


def _send_telegram(submission: dict) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise NotificationError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required")
    log.info("posting to Telegram (bot %s)", mask(token))
    url = f"{TELEGRAM_API_HOST}/bot{token}/sendMessage"
    _http_post(url, _build_telegram_payload(submission, chat_id))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--channel", required=True, choices=["discord", "telegram"])
    parser.add_argument("--submission-file", required=True, type=Path)
    args = parser.parse_args()

    try:
        payload = json.loads(args.submission_file.read_text(encoding="utf-8"))
    except FileNotFoundError:
        log.error("submission file not found: %s", args.submission_file)
        return 1
    except json.JSONDecodeError as exc:
        log.error("invalid JSON in %s: %s", args.submission_file, exc.msg)
        return 1

    try:
        if args.channel == "discord":
            _send_discord(payload)
        else:
            _send_telegram(payload)
    except NotificationError as exc:
        log.error("notification failed: %s", exc)
        return 1
    log.info("notification sent (%s)", args.channel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
