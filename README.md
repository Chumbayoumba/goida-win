# ГОЙДА.WIN

Одностраничник: бесплатный прокси Telegram → канал [@vnespiska](https://t.me/vnespiska) → VPN-бот [@vnespiskabot](https://t.me/vnespiskabot), промокод **VNESPISKA** (239 ₽).

Сайт: **https://goida.win/** (GitHub Pages).

## Воронка

| Шаг | Куда |
|-----|------|
| 1. Прокси | `tg://proxy` из `data/proxy.json` |
| 2. Канал | https://t.me/vnespiska |
| 3. VPN | https://t.me/vnespiskabot · код `VNESPISKA` |

Слот прокси один. Если он мёртвый, `python3 refresh.py` подставляет кандидата из `data/fallbacks.json`.

## Локально

```bash
python3 -m unittest discover -s tests -v
python3 -m http.server 8765 --directory .
```

## DNS

`goida.win` и `www` → CNAME `chumbayoumba.github.io` (Cloudflare flattening).
