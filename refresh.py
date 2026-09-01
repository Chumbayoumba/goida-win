#!/usr/bin/env python3
"""Swap the featured goida.win proxy when the current slot is dead.

Runs on GitHub Actions (best-effort schedule). Writes ``data/proxy.json``
and optional HTML hrefs. The site itself stays on GitHub Pages.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from proxy_slot import (
    patch_html_file,
    read_slot,
    refresh_featured,
    tcp_probe,
)

HERE = Path(__file__).resolve().parent


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--slot", type=Path, default=HERE / "data" / "proxy.json")
    p.add_argument("--candidates", type=Path, default=HERE / "data" / "fallbacks.json")
    p.add_argument("--html", type=Path, default=HERE / "index.html")
    p.add_argument("--no-probe", action="store_true")
    p.add_argument("--timeout", type=float, default=4.0)
    args = p.parse_args(argv)

    raw = json.loads(args.candidates.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        candidates = raw.get("proxies") or raw.get("candidates") or []
    else:
        candidates = raw
    if not isinstance(candidates, list):
        print("candidates JSON must be a list or {proxies: [...]}", file=sys.stderr)
        return 2

    probe = None
    if not args.no_probe:
        probe = lambda server, port, secret: tcp_probe(  # noqa: E731
            server, port, secret, timeout=args.timeout
        )

    slot = refresh_featured(args.slot, candidates, probe=probe)
    if args.html.exists() and slot.get("server"):
        patch_html_file(args.html, slot)

    print(json.dumps(slot, ensure_ascii=False, indent=2))
    if args.slot.exists():
        disk = read_slot(args.slot)
        if disk.get("server") != slot.get("server"):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
