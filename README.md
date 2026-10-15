# Fixarfrassen

Statisk guidesajt: guider för dig som fixar själv hemma.

- `guides.py` – alla guider som data (titel, steg, FAQ, relaterade guider)
- `build.py` – bygger sajten till `dist/` (kategorier, startsida, sitemap)
- `src/` – CSS, sök, favicon och typsnitt
- `dist/` – färdig sajt som Cloudflare publicerar

Bygg om efter ändringar: `python3 build.py`

Affiliatelänkar läggs i `AFFILIATE` i `build.py`. Annonsmärkningen visas automatiskt på sidor med partnerlänk.
