"""Shipped-artifact tests for the goida.win landing (read files, do not reimplement)."""
from __future__ import annotations

import json
import unittest
from pathlib import Path


SITE = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (SITE / rel).read_text(encoding="utf-8")


class GoidaStaticTests(unittest.TestCase):
    def test_cname_is_goida_win(self) -> None:
        self.assertEqual(read("CNAME").strip(), "goida.win")

    def test_funnel_strings_on_landing(self) -> None:
        html = read("index.html")
        self.assertIn("t.me/vnespiska", html)
        self.assertIn("t.me/vnespiskabot", html)
        self.assertIn("VNESPISKA", html)
        self.assertTrue(
            "tg://proxy" in html or "t.me/proxy" in html,
            "landing must expose a one-click Telegram proxy href",
        )
        self.assertIn("239", html)

    def test_seo_mentions_goida_win(self) -> None:
        html = read("index.html")
        robots = read("robots.txt")
        sitemap = read("sitemap.xml")
        self.assertIn("goida.win", html)
        self.assertIn("canonical", html.lower())
        self.assertIn("og:", html.lower())
        self.assertIn("schema.org", html)
        self.assertIn("goida.win", robots)
        self.assertIn("goida.win", sitemap)
        self.assertIn("application/ld+json", html)

    def test_origin_is_not_product_vps(self) -> None:
        html = read("index.html")
        robots = read("robots.txt")
        sitemap = read("sitemap.xml")
        cname = read("CNAME")
        blob = html + robots + sitemap + cname
        self.assertNotIn("87.121.82.25", blob)
        self.assertNotIn("http://87.121.82.25", blob)
        self.assertNotIn("https://87.121.82.25", blob)

    def test_visual_motifs_and_modern_cyrillic(self) -> None:
        html = read("index.html")
        css = read("css/style.css") + read("css/fonts.css")
        self.assertIn("Роскомнадзор", html)
        self.assertTrue(
            "флаг" in html.lower() or "tricolor" in html.lower() or "flag-ru" in html,
            "Russian flag motif missing",
        )
        self.assertIn("@font-face", css)
        self.assertNotIn("fonts.googleapis.com", html)
        self.assertNotIn("fonts.googleapis.com", css)

    def test_scripts_are_browser_safe(self) -> None:
        js = read("js/app.js")
        self.assertNotIn("module.exports", js)
        self.assertNotIn("require(", js)
        self.assertNotIn("process.exit", js)

    def test_funnel_payload_matches_copy(self) -> None:
        data = json.loads(read("data/funnel.json"))
        self.assertEqual(data["domain"], "goida.win")
        self.assertEqual(data["promo"], "VNESPISKA")
        self.assertEqual(data["price_promo"], 239)
        self.assertIn("vnespiska", data["channel"])
        self.assertIn("vnespiskabot", data["bot"])


if __name__ == "__main__":
    unittest.main()
