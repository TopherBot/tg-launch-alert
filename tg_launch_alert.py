#!/usr/bin/env python3
"""tg-launch-alert
A minimal Python script that polls a Telegram bot/channel for recent messages and prints those
containing a specific keyword (default: 'launch').
"""

import os
import sys
import json
import requests
from typing import List, Dict

# ---------------------------------------------------------------------------
# Configuration (can be overridden by environment variables)
# ---------------------------------------------------------------------------
TOKEN = os.getenv("TG_BOT_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")
KEYWORD = os.getenv("TG_KEYWORD", "launch")  # keyword to filter messages
MESSAGE_LIMIT = int(os.getenv("TG_MESSAGE_LIMIT", "20"))

API_URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

# ---------------------------------------------------------------------------
def fetch_updates(offset: int = None) -> List[Dict]:
    """Fetch updates from the Telegram Bot API.
    Parameters
    ----------
    offset: int | None
        Update ID to start from (used for pagination). None fetches the latest.
    Returns
    -------
    List[Dict]
        List of update objects.
    """
    params = {
        "timeout": 0,
        "limit": MESSAGE_LIMIT,
    }
    if offset:
        params["offset"] = offset
    try:
        resp = requests.get(API_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            raise RuntimeError(data.get("description", "Unknown error"))
        return data.get("result", [])
    except Exception as e:
        print(f"[Error] Failed to fetch updates: {e}", file=sys.stderr)
        sys.exit(1)

# ---------------------------------------------------------------------------
def filter_messages(updates: List[Dict], keyword: str) -> List[str]:
    """Extract text messages that contain the keyword.
    Returns a list of formatted strings.
    """
    matches = []
    keyword_lower = keyword.lower()
    for upd in updates:
        msg = upd.get("message") or upd.get("edited_message")
        if not msg:
            continue
        # Ensure the message belongs to the target chat (if provided)
        if CHAT_ID and str(msg.get("chat", {}).get("id")) != CHAT_ID:
            continue
        text = msg.get("text", "")
        if keyword_lower in text.lower():
            user = msg.get("from", {}).get("username", "unknown")
            timestamp = msg.get("date")
            matches.append(f"[{timestamp}] @{user}: {text}")
    return matches

# ---------------------------------------------------------------------------
def main():
    if not TOKEN or not CHAT_ID:
        print("[Error] TG_BOT_TOKEN and TG_CHAT_ID environment variables must be set.", file=sys.stderr)
        sys.exit(1)

    updates = fetch_updates()
    alerts = filter_messages(updates, KEYWORD)

    if alerts:
        print("=== Launch Alerts ===")
        for a in alerts:
            print(a)
    else:
        print(f"No messages containing '{KEYWORD}' were found in the last {MESSAGE_LIMIT} updates.")

if __name__ == "__main__":
    main()
