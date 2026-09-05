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
        self.assertIn("G-KCKYM27XVJ", html)
        self.assertNotIn("G-YVMQ4T6HEQ", html)
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
        css = read("css/style.css")
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
        self.assertIn("preventDefault", js)
        self.assertNotIn("scrollIntoView", js)
        self.assertNotIn('"#choice"', js)

    def test_funnel_payload_matches_copy(self) -> None:
        data = json.loads(read("data/funnel.json"))
        self.assertEqual(data["domain"], "goida.win")
        self.assertIn("vnespiska", data["channel"])
        self.assertIn("magnit.help", data["vpn_web"])
        self.assertIn("Geodema_bot", data["vpn_bot"])
        self.assertEqual(data.get("promo"), "VNESPISKA")
        self.assertEqual(int(data.get("price_promo")), 239)

    def test_v2_hub_copy_and_actions(self) -> None:
        html = read("index.html")
        self.assertRegex(html, r"<title>Не работает Telegram или сайты\? Прокси и VPN \| GOIDA\.WIN</title>")
        self.assertRegex(html, r"<h1[^>]*>Не работает Telegram или сайты\?</h1>")
        self.assertIn(
            'content="Не работает Telegram? Получи бесплатный прокси в @vnespiska. Не открываются YouTube и сайты? Подключи VPN в браузере или Telegram."',
            html,
        )
        self.assertIn("ПОЛУЧИТЬ ПРОКСИ", html)
        self.assertIn("ПОДКЛЮЧИТЬ VPN", html)
        self.assertIn("239", html)
        self.assertIn("VNESPISKA", html)
        self.assertNotIn("Хочу открыть всё", html)
        self.assertRegex(html, r"<h2[^>]*>Частые вопросы</h2>")
        self.assertGreaterEqual(html.count("<details"), 6)
        self.assertLessEqual(html.count("<details"), 8)
        sit = html.split('class="sit"', 1)[1].split("</ul>", 1)[0]
        self.assertLessEqual(sit.count("<li"), 3)
        self.assertEqual(sit.lower().count("telegram"), 1)
        self.assertNotIn("Telegram не подключается", sit)
        self.assertNotIn("Telegram не грузится", sit)
        self.assertNotIn("Нужен только Telegram", sit)

    def test_goida_is_choice_cta(self) -> None:
        html = read("index.html")
        css = read("css/style.css")
        js = read("js/app.js")
        self.assertIn("ГОЙДА", html)
        self.assertRegex(html, r'<button[^>]+id="goida-shout"')
        self.assertIn('type="button"', html)
        self.assertNotRegex(html, r'<a[^>]+id="goida-shout"')
        self.assertNotRegex(html, r'id="goida-shout"[^>]*href=')
        self.assertIn("goida_click", html + js)
        self.assertIn("goida_shout", html + js)
        self.assertNotRegex(html, r'<img[^>]+(goida|shout)[^>]+\.(jpg|png|webp)', re.I)
        self.assertIn("goida-btn", css)
        self.assertIn("60px", css)
        self.assertIn("70px", css)

    def test_p1_cluster_pages(self) -> None:
        pages = {
            "telegram-ne-rabotaet/index.html": (
                "Не работает Telegram",
                "прокси",
            ),
            "proxy-telegram/index.html": (
                "Прокси для Telegram",
                "подключ",
            ),
            "vpn-telegram/index.html": (
                "VPN для Telegram",
                "VPN",
            ),
            "vpn-youtube/index.html": (
                "YouTube",
                "VPN",
            ),
            "vpn-whatsapp/index.html": (
                "WhatsApp",
                "VPN",
            ),
            "vpn-instagram/index.html": (
                "Instagram",
                "VPN",
            ),
            "vpn-dlya-iphone/index.html": (
                "iPhone",
                "VPN",
            ),
            "vpn-dlya-android/index.html": (
                "Android",
                "VPN",
            ),
            "vpn-dlya-kompyutera/index.html": (
                "компьютера",
                "VPN",
            ),
        }
        hub = read("index.html")
        for rel, (h1_bit, body_bit) in pages.items():
            html = read(rel)
            self.assertIn("<html lang=\"ru\">", html)
            self.assertIn("canonical", html.lower())
            self.assertIn("https://goida.win/" + rel.split("/")[0] + "/", html)
            self.assertIn(h1_bit, html)
            self.assertIn(body_bit.lower(), html.lower())
            self.assertGreater(len(html.encode("utf-8")), 4000)
            self.assertGreaterEqual(html.count("<h2"), 3)
            self.assertIn("t.me/vnespiska", html)
            self.assertTrue("magnit.help" in html or "Geodema_bot" in html)
            outbound = re.findall(
                r'href="(https://(?:t\.me|magnit\.help)[^"]+)"',
                html,
            )
            self.assertGreaterEqual(len(outbound), 2, rel)
            for href in outbound:
                self.assertIn("utm_source=goida", href, href)
                self.assertIn("utm_medium=site", href, href)
                self.assertIn("utm_campaign=", href, href)
                self.assertIn("utm_content=", href, href)
            slug = rel.split("/")[0]
            self.assertIn("/" + slug + "/", hub)

    def test_sitemap_is_hub_plus_p1_only(self) -> None:
        xml = read("sitemap.xml")
        locs = re.findall(r"<loc>([^<]+)</loc>", xml)
        expected = {
            "https://goida.win/",
            "https://goida.win/telegram-ne-rabotaet/",
            "https://goida.win/proxy-telegram/",
            "https://goida.win/vpn-telegram/",
            "https://goida.win/vpn-youtube/",
            "https://goida.win/vpn-whatsapp/",
            "https://goida.win/vpn-instagram/",
            "https://goida.win/vpn-dlya-iphone/",
            "https://goida.win/vpn-dlya-android/",
            "https://goida.win/vpn-dlya-kompyutera/",
        }
        self.assertEqual(set(locs), expected)
        self.assertTrue(all("utm" not in loc for loc in locs))
        robots = read("robots.txt")
        self.assertIn("Sitemap: https://goida.win/sitemap.xml", robots)
        self.assertNotIn("Disallow: /", robots)


if __name__ == "__main__":
    unittest.main()
