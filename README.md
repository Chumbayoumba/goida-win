# ГОЙДА.WIN

Современный одностраничник: бесплатный прокси Telegram → канал [@vnespiska](https://t.me/vnespiska) → VPN-бот [@vnespiskabot](https://t.me/vnespiskabot) с промокодом **VNESPISKA** (239 ₽).

Хостинг: **GitHub Pages** + домен `goida.win`. Сайт **не** живёт на продуктовом VPS `87.121.82.25`.

## Воронка

| Шаг | Куда |
|-----|------|
| 1. Loss-leader | `tg://proxy` из `data/proxy.json` |
| 2. Канал | https://t.me/vnespiska |
| 3. VPN | https://t.me/vnespiskabot · код `VNESPISKA` |

Слот прокси один. Если он мёртвый, `python3 refresh.py` подставляет кандидата из `data/fallbacks.json` и переписывает href в `index.html`. GitHub Actions гоняет это best-effort каждые 15 минут (это не SLA «раз в 5 минут»). Предпочтительный живой пробинг из РФ — VDS_38904.

## Локально

```bash
python3 -m unittest discover -s tests -v
python3 -m http.server 8765 --directory .
```

## DNS (Cloudflare)

`goida.win` CNAME/ALIAS → `chumbayoumba.github.io` (или A-записи GitHub Pages). Apex: `CNAME flattening`. Не направлять на `87.121.82.25`.
