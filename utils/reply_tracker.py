"""
Reply Tracker
-------------
Lightweight, manual reply-tracking for the AI Outreach Agent.

Automated reply detection would require continuously polling the
sender's inbox via IMAP, which isn't practical inside a Streamlit app
that only runs while a user has it open. Instead, this module lets the
user mark a lead as "Replied" from the Campaign History tab after they
see the reply land in their own inbox — a simple, honest, and fully
functional way to track response rates per campaign.
"""

import json
from pathlib import Path

from logs.log import log_info, log_error
from datetime import datetime

HISTORY_PATH = Path("data/sent_emails.json")


def _load_all() -> list:
    try:
        with open(HISTORY_PATH, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_all(emails: list) -> None:
    with open(HISTORY_PATH, "w") as file:
        json.dump(emails, file, indent=4)


def set_replied(recipient_email: str, replied: bool) -> bool:
    """
    Mark a specific lead's email as replied / not replied.

    Returns True if a matching record was found and updated.
    """
    emails = _load_all()
    found = False

    for record in emails:
        if record.get("recipient_email") == recipient_email:
            record["replied"] = replied
            record["replied_at"] = (
                datetime.now().strftime("%d %B %Y") if replied else None
            )
            found = True
            break

    if found:
        try:
            _save_all(emails)
            log_info(f"Reply status updated for {recipient_email}: {replied}")
        except Exception as e:
            log_error(f"Reply Tracker Save Error: {e}")
            return False
    else:
        log_error(f"Reply Tracker: no record found for {recipient_email}")

    return found


def get_reply_stats(emails: list | None = None) -> dict:
    """
    Compute reply-rate statistics across all (or a given list of) sent
    emails.
    """
    if emails is None:
        emails = _load_all()

    total = len(emails)
    replied = sum(1 for e in emails if e.get("replied", False))
    reply_rate = round((replied / total) * 100, 1) if total else 0.0

    return {
        "total": total,
        "replied": replied,
        "not_replied": total - replied,
        "reply_rate": reply_rate,
    }
