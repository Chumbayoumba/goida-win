"""Shipped-artifact tests for the goida.win landing (read files, do not reimplement)."""
from __future__ import annotations

import json
import re
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
        self.assertIn("magnit.help/p2f9f6fab", html)
        self.assertIn("Geodema_bot", html)
        self.assertRegex(
            html,
            r'id="cta-proxy"[^>]*href="https://t\.me/vnespiska',
        )
        self.assertNotIn("tg://proxy", html)

    def test_seo_mentions_goida_win(self) -> None:
        html = read("index.html")
        robots = read("robots.txt")
        sitemap = read("sitemap.xml")
        llms = read("llms.txt")
        self.assertIn("goida.win", html)
        self.assertIn("canonical", html.lower())
        self.assertIn("og:", html.lower())
        self.assertIn("schema.org", html)
        self.assertIn("SoftwareApplication", html)
        self.assertIn("yandex-verification", html)
        self.assertIn("112149595", html)
        self.assertIn("G-YVMQ4T6HEQ", html)
        self.assertIn("goida.win", robots)
        self.assertIn("goida.win", sitemap)
        self.assertIn("application/ld+json", html)
        self.assertIn("goida.win", llms)
        self.assertIn("5ac758ea9dd240acbfa4d18e67fd497d", read("5ac758ea9dd240acbfa4d18e67fd497d.txt"))

    def test_origin_is_custom_domain_not_raw_ip(self) -> None:
        html = read("index.html")
        robots = read("robots.txt")
        sitemap = read("sitemap.xml")
        cname = read("CNAME")
        blob = html + robots + sitemap + cname
        self.assertIn("goida.win", blob)
        self.assertIsNone(re.search(r"https?://\d{1,3}(?:\.\d{1,3}){3}", blob))

    def test_visual_motifs_and_modern_cyrillic(self) -> None:
        html = read("index.html")
        css = read("css/style.css") + read("css/fonts.css")
        self.assertTrue(
            "флаг" in html.lower() or "tricolor" in html.lower() or "flag-ru" in html,
            "Russian flag motif missing",
        )
        self.assertIn("Не работает Telegram", html)
        self.assertIn("hero_vpn_click", html)
        self.assertIn("hero_proxy_click", html)
        self.assertIn('id="goida-shout"', html)
        self.assertIn("assets/audio/goida.mp3", html)
        self.assertTrue((SITE / "assets" / "audio" / "goida.mp3").is_file())
        self.assertIn("@font-face", css)
        self.assertNotIn("fonts.googleapis.com", html)
        self.assertNotIn("fonts.googleapis.com", css)
        self.assertNotIn("Не для чужих преступлений", html)
        self.assertNotIn("GitHub Pages", html)

    def test_scripts_are_browser_safe(self) -> None:
        js = read("js/app.js")
        self.assertNotIn("module.exports", js)
        self.assertNotIn("require(", js)
        self.assertNotIn("process.exit", js)
        self.assertIn("reachGoal", js)
        self.assertIn("audio.play", js)

    def test_funnel_payload_matches_copy(self) -> None:
        data = json.loads(read("data/funnel.json"))
        self.assertEqual(data["domain"], "goida.win")
        self.assertIn("vnespiska", data["channel"])
        self.assertIn("magnit.help", data["vpn_web"])
        self.assertIn("Geodema_bot", data["vpn_bot"])


if __name__ == "__main__":
    unittest.main()
