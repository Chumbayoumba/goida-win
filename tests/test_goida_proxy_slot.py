"""Drive the shipped goida.proxy_slot reader/replace on representative JSON."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SITE = Path(__file__).resolve().parents[1]
if str(SITE) not in sys.path:
    sys.path.insert(0, str(SITE))

from proxy_slot import (  # noqa: E402
    apply_slot_to_html,
    build_links,
    read_slot,
    refresh_featured,
    replace_slot,
    slot_is_dead,
)


LIVE = {
    "server": "live.example.net",
    "port": 443,
    "secret": "eeaabb",
    "alive": True,
}

DEAD = {
    "server": "dead.example.net",
    "port": 443,
    "secret": "eeddcc",
    "alive": False,
}

REPLACEMENT = {
    "server": "fresh.example.net",
    "port": 9443,
    "secret": "eeff00",
}


def _write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


class ProxySlotTests(unittest.TestCase):
    def test_read_slot_returns_shipped_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "proxy.json"
            _write(path, LIVE)
            slot = read_slot(path)
            self.assertEqual(slot["server"], "live.example.net")
            self.assertEqual(int(slot["port"]), 443)
            self.assertEqual(slot["secret"], "eeaabb")

    def test_build_links_are_telegram_deep_links(self) -> None:
        links = build_links("host.example", 9443, "eeabc")
        self.assertEqual(
            links["tg_link"],
            "tg://proxy?server=host.example&port=9443&secret=eeabc",
        )
        self.assertEqual(
            links["https_link"],
            "https://t.me/proxy?server=host.example&port=9443&secret=eeabc",
        )

    def test_dead_flag_is_dead_without_probe(self) -> None:
        self.assertTrue(slot_is_dead(DEAD))
        self.assertFalse(slot_is_dead(LIVE))
        self.assertTrue(slot_is_dead({}))
        self.assertTrue(slot_is_dead({"server": "x"}))

    def test_replace_keeps_live_slot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "proxy.json"
            _write(path, LIVE)
            out = replace_slot(path, REPLACEMENT)
            self.assertEqual(out["server"], "live.example.net")
            self.assertEqual(read_slot(path)["server"], "live.example.net")

    def test_replace_writes_when_slot_dead(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "proxy.json"
            _write(path, DEAD)
            out = replace_slot(path, REPLACEMENT)
            self.assertEqual(out["server"], "fresh.example.net")
            self.assertEqual(int(out["port"]), 9443)
            self.assertIn("tg://proxy?server=fresh.example.net", out["tg_link"])
            disk = read_slot(path)
            self.assertEqual(disk["server"], "fresh.example.net")
            self.assertIn("t.me/proxy?server=fresh.example.net", disk["https_link"])

    def test_probe_false_replaces_even_if_alive_flag_true(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "proxy.json"
            _write(path, LIVE)

            def probe(server: str, port: int, secret: str) -> bool:
                self.assertEqual(server, "live.example.net")
                self.assertEqual(port, 443)
                self.assertEqual(secret, "eeaabb")
                return False

            out = replace_slot(path, REPLACEMENT, probe=probe)
            self.assertEqual(out["server"], "fresh.example.net")

    def test_refresh_picks_first_live_candidate_when_current_dead(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "proxy.json"
            _write(path, DEAD)
            candidates = [
                {"server": "down.example.net", "port": 1, "secret": "ee01", "alive": False},
                {"server": "up.example.net", "port": 2, "secret": "ee02", "alive": True},
            ]
            out = refresh_featured(path, candidates)
            self.assertEqual(out["server"], "up.example.net")
            self.assertEqual(read_slot(path)["server"], "up.example.net")

    def test_apply_slot_to_html_rewrites_cta_hrefs(self) -> None:
        html = (
            '<a id="cta-proxy" href="tg://proxy?server=old&port=1&secret=eeold">x</a>'
            '<a id="cta-proxy-https" href="https://t.me/proxy?server=old&port=1&secret=eeold">y</a>'
        )
        slot = {
            "server": "new.example.net",
            "port": 9443,
            "secret": "eenew",
            **build_links("new.example.net", 9443, "eenew"),
        }
        out = apply_slot_to_html(html, slot)
        self.assertIn('id="cta-proxy" href="tg://proxy?server=new.example.net&port=9443&secret=eenew"', out)
        self.assertIn(
            'id="cta-proxy-https" href="https://t.me/proxy?server=new.example.net&port=9443&secret=eenew"',
            out,
        )
        self.assertNotIn("server=old", out)


if __name__ == "__main__":
    unittest.main()
