#!/usr/bin/env python3
"""Pull the public t.me/s/vnespiska preview into data/channel-feed.json."""
from __future__ import annotations

import html as html_lib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHANNEL = "vnespiska"
PREVIEW = f"https://t.me/s/{CHANNEL}"
OUT = HERE / "data" / "channel-feed.json"


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; goida-win-feed/1.0)"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", "replace")


def parse_posts(raw: str) -> list[dict]:
    chunks = re.split(r'<div class="tgme_widget_message[^"]*js-widget_message"', raw)
    items: list[dict] = []
    seen: set[str] = set()
    for chunk in chunks[1:]:
        post = re.search(r'data-post="([^"]+)"', chunk)
        if not post:
            continue
        pid = post.group(1)
        if pid in seen:
            continue
        seen.add(pid)
        dt = re.search(r'datetime="([^"]+)"', chunk)
        text_m = re.search(
            r'class="tgme_widget_message_text js-message_text"[^>]*>(.*?)</div>',
            chunk,
            re.S,
        )
        text = ""
        if text_m:
            text = re.sub(r"<br\s*/?>", " ", text_m.group(1), flags=re.I)
            text = re.sub(r"<[^>]+>", "", text)
            text = html_lib.unescape(re.sub(r"\s+", " ", text)).strip()
        items.append(
            {
                "id": pid,
                "url": "https://t.me/" + pid,
                "datetime": dt.group(1) if dt else "",
                "text": text[:320],
                "has_proxy": "tg://proxy" in chunk or "t.me/proxy" in chunk,
            }
        )
    return items


def main() -> int:
    raw = fetch(PREVIEW)
    posts = parse_posts(raw)
    latest = posts[-3:] if posts else []
    payload = {
        "channel": CHANNEL,
        "url": f"https://t.me/{CHANNEL}",
        "updated": datetime.now(timezone.utc).isoformat(),
        "posts": latest,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(OUT), "n": len(latest), "ids": [p["id"] for p in latest]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
