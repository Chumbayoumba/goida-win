"""Featured MTProto proxy slot for goida.win.

The landing reads ``data/proxy.json``. This module is the only writer the
refresh job (GitHub Actions or the RU probe VDS) should use, so a dead
proxy is swapped without rewriting the page by hand.
"""
from __future__ import annotations

import json
import re
import socket
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable


Probe = Callable[[str, int, str], bool]


def build_links(server: str, port: int, secret: str) -> dict[str, str]:
    q = f"server={server}&port={int(port)}&secret={secret}"
    return {
        "tg_link": f"tg://proxy?{q}",
        "https_link": f"https://t.me/proxy?{q}",
    }


def normalize(proxy: dict[str, Any]) -> dict[str, Any]:
    server = str(proxy["server"]).strip()
    port = int(proxy["port"])
    secret = str(proxy["secret"]).strip()
    if not server or not secret:
        raise ValueError("proxy slot needs server, port, secret")
    slot = {
        "server": server,
        "port": port,
        "secret": secret,
        "alive": bool(proxy.get("alive", True)),
        "updated": proxy.get("updated") or datetime.now(timezone.utc).isoformat(),
    }
    slot.update(build_links(server, port, secret))
    return slot


def read_slot(path: Path) -> dict[str, Any]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("proxy slot JSON must be an object")
    return raw


def write_slot(path: Path, proxy: dict[str, Any]) -> dict[str, Any]:
    slot = normalize(proxy)
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_text(json.dumps(slot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(dest)
    return slot


def slot_is_dead(slot: dict[str, Any] | None, probe: Probe | None = None) -> bool:
    if not slot:
        return True
    server = str(slot.get("server") or "").strip()
    secret = str(slot.get("secret") or "").strip()
    port_raw = slot.get("port")
    if port_raw is None:
        return True
    try:
        port = int(port_raw)
    except (TypeError, ValueError):
        return True
    if not server or not secret or port <= 0:
        return True
    if slot.get("alive") is False and probe is None:
        return True
    if probe is not None:
        try:
            return not bool(probe(server, port, secret))
        except Exception:
            return True
    return False


def replace_slot(
    path: Path,
    replacement: dict[str, Any],
    probe: Probe | None = None,
) -> dict[str, Any]:
    dest = Path(path)
    current: dict[str, Any] = {}
    if dest.exists():
        current = read_slot(dest)
    if not slot_is_dead(current, probe=probe):
        return current
    return write_slot(dest, replacement)


def refresh_featured(
    path: Path,
    candidates: Iterable[dict[str, Any]],
    probe: Probe | None = None,
) -> dict[str, Any]:
    dest = Path(path)
    current: dict[str, Any] = {}
    if dest.exists():
        current = read_slot(dest)
    if not slot_is_dead(current, probe=probe):
        return current
    for cand in candidates:
        if slot_is_dead(cand, probe=probe):
            continue
        return write_slot(dest, cand)
    return current


def apply_slot_to_html(html: str, slot: dict[str, Any]) -> str:
    links = build_links(str(slot["server"]), int(slot["port"]), str(slot["secret"]))
    tg = slot.get("tg_link") or links["tg_link"]
    https = slot.get("https_link") or links["https_link"]
    html = re.sub(
        r'(id="cta-proxy"\s+href=")[^"]*"',
        r"\1" + tg + '"',
        html,
        count=1,
    )
    html = re.sub(
        r'(id="cta-proxy-https"\s+href=")[^"]*"',
        r"\1" + https + '"',
        html,
        count=1,
    )
    return html


def tcp_probe(server: str, port: int, secret: str = "", timeout: float = 4.0) -> bool:
    """Cheap liveness: TCP connect. MTProto handshake is optional on the RU VDS."""
    try:
        with socket.create_connection((server, int(port)), timeout=timeout):
            return True
    except OSError:
        return False


def patch_html_file(html_path: Path, slot: dict[str, Any]) -> None:
    path = Path(html_path)
    original = path.read_text(encoding="utf-8")
    updated = apply_slot_to_html(original, slot)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
