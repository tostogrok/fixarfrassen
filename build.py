#!/usr/bin/env python3
"""Bygger Fixarfrassen till ./dist. Kör: python3 build.py"""
import json, os, re, shutil, html

SITE_URL = "https://fixarfrassen.se"
SITE_NAME = "Fixarfrassen"
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")

# Klistra in AdSense-koden här när kontot är godkänt.
AD_HEAD = ""

# Affiliatelänkar per partner. Tom länk = rutan och annonsmärkningen visas inte.
AFFILIATE = {
    "Byggstart": "",
}

from guides import GUIDES

CATS = [
    ("avlopp-och-vatten", "Avlopp och vatten", "Stopp i avloppet, droppande kranar och läckor."),
    ("varme-och-element", "Värme och element", "Kalla element, luftning och termostater."),
    ("vitvaror", "Vitvaror", "Diskmaskin, tvättmaskin, kyl och frys."),
]
CAT_NAME = {c[0]: c[1] for c in CATS}

# ---------- Frasse ----------
CAT_HEAD = '''<svg viewBox="0 0 160 160" aria-hidden="true"><path d="M38 58 L46 14 L74 44 Z" fill="#f4c430" stroke="#22262a" stroke-width="5" stroke-linejoin="round"/><path d="M122 58 L114 14 L86 44 Z" fill="#f4c430" stroke="#22262a" stroke-width="5" stroke-linejoin="round"/><path d="M47 50 L50 28 L64 44 Z" fill="#f7a8a0"/><path d="M113 50 L110 28 L96 44 Z" fill="#f7a8a0"/><path d="M30 82 C30 50 52 38 80 38 C108 38 130 50 130 82 C130 116 108 140 80 140 C52 140 30 116 30 82 Z" fill="#f4c430" stroke="#22262a" stroke-width="5"/><path d="M33 66 C55 56 105 56 127 66" fill="none" stroke="#22262a" stroke-width="10" stroke-linecap="round"/><rect x="67" y="46" width="26" height="20" rx="5" fill="#22262a"/><circle cx="80" cy="56" r="7" fill="#fff6c8"/><circle cx="62" cy="88" r="9" fill="#fff" stroke="#22262a" stroke-width="3"/><circle cx="98" cy="88" r="9" fill="#fff" stroke="#22262a" stroke-width="3"/><circle cx="63" cy="89" r="4.5" fill="#22262a"/><circle cx="99" cy="89" r="4.5" fill="#22262a"/><ellipse cx="80" cy="107" rx="10" ry="7" fill="#f08a9a" stroke="#22262a" stroke-width="3"/><path d="M80 114 Q80 122 71 122 M80 114 Q80 122 89 122" fill="none" stroke="#22262a" stroke-width="3" stroke-linecap="round"/><path d="M40 106 L60 108 M40 116 L60 112 M120 106 L100 108 M120 116 L100 112" stroke="#22262a" stroke-width="3" stroke-linecap="round"/></svg>'''
CAT_HERO = CAT_HEAD.replace('<svg viewBox="0 0 160 160"', '<svg class="cat" viewBox="0 0 160 160"').replace('</svg>', '<g transform="translate(150 146) rotate(-40) scale(0.75)"><rect x="-7" y="-6" width="14" height="46" rx="7" fill="#8a97a2" stroke="#22262a" stroke-width="3"/><path d="M-17 -20 a19 19 0 1 0 34 0 l0 -12 h-9 v12 h-16 v-12 h-9 z" fill="#8a97a2" stroke="#22262a" stroke-width="3" stroke-linejoin="round"/></g></svg>').replace('viewBox="0 0 160 160"', 'viewBox="0 0 175 175"')
SEARCH_ICON = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16" y2="16"/></svg>'

def esc(s):
    return html.escape(s, quote=True)

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).replace("&nbsp;", " ").strip()

def layout(title, desc, path, body, schema=None, noindex=False):
    url = SITE_URL + path
    sch = ""
    if schema:
        sch = '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + "</script>"
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="sv_SE">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/style.css">
{sch}
{AD_HEAD}
</head>
<body>
<header class="site"><div class="wrap">
<a class="logo" href="/">{CAT_HEAD}<span class="w">Fixar<b>frassen</b></span></a>
<nav><a href="/#guider">Alla guider</a></nav>
</div></header>
<main><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">
<p><a href="/">Start</a><a href="/om/">Om Fixarfrassen</a><a href="/integritet/">Integritet</a></p>
<p>Guiderna gäller vanliga hemmafix. Är du osäker, eller gäller det el, gas eller fukt i väggar, anlita en behörig hantverkare. I hyresrätt och bostadsrätt: kontakta hyresvärden eller föreningen först.</p>
</div></footer>
{'<script src="/search.js" defer></script>' if path == "/" else ""}
</body>
</html>
"""

def card(g):
    return f'<a href="/{g["slug"]}/" data-q="{esc((g["h1"] + " " + g.get("card", "") + " " + " ".join(g.get("keywords", []))).lower())}"><strong>{esc(g["h1"])}</strong><span>{esc(g["card"])}</span></a>'

def crumbs(items):
    parts = [f'<a href="{u}">{esc(n)}</a>' for n, u in items[:-1]] + [esc(items[-1][0])]
    return '<div class="crumbs">' + " › ".join(parts) + "</div>"

def breadcrumb_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + u} for i, (n, u) in enumerate(items)]}

def faq_html(faqs):
    out = '<h2>Vanliga frågor</h2><div class="faq">'
    for q, a in faqs:
        out += f"<details><summary>{esc(q)}</summary><p>{a}</p></details>"
    return out + "</div>"

def guide_page(g, by_slug):
    path = f"/{g['slug']}/"
    cat = g["cat"]
    trail = [("Start", "/"), (CAT_NAME[cat], f"/{cat}/"), (g["card_title"] if g.get("card_title") else g["h1"], path)]
    partner = g.get("partner")
    partner_on = bool(partner and AFFILIATE.get(partner))
    admark = f'<p class="admark">Sidan innehåller reklam genom annonslänkar för {esc(partner)}</p>' if partner_on else ""
    facts = "".join(f"<li><b>{esc(k)}:</b> {esc(v)}</li>" for k, v in g["facts"])
    need = ""
    if g.get("need"):
        need = '<div class="need"><h2>Det här behöver du</h2><ul>' + "".join(f"<li>{x}</li>" for x in g["need"]) + "</ul></div>"
    steps = '<ol class="steps">' + "".join(
        f'<li><h3>{esc(t)}</h3>{"".join("<p>" + p + "</p>" for p in (txt if isinstance(txt, list) else [txt]))}</li>' for t, txt in g["steps"]) + "</ol>"
    help_box = ""
    if g.get("help"):
        h = g["help"]
        link = ""
        if partner_on and h.get("cta"):
            link = f'<a class="cta" href="{AFFILIATE[partner]}" rel="sponsored nofollow noopener" target="_blank">{esc(h["cta"])}</a>'
        help_box = f'<div class="help"><h2>{esc(h["title"])}</h2><p>{h["text"]}</p>{link}</div>'
    related = ""
    if g.get("related"):
        related = '<h2>Fler guider</h2><div class="cards">' + "".join(card(by_slug[s]) for s in g["related"]) + "</div>"
    body = f"""{crumbs(trail)}
<h1>{esc(g['h1'])}</h1>
{admark}
<p class="lead">{g['lead']}</p>
<ul class="facts">{facts}</ul>
<div class="answer"><strong class="h">Snabbt svar</strong><p>{g['answer']}</p></div>
{need}
<h2>{esc(g.get('steps_title', 'Så gör du'))}</h2>
{steps}
{g.get('after', '')}
{help_box}
{faq_html(g['faqs'])}
{related}
<p class="note updated">Senast uppdaterad {g['updated']}</p>"""
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": g["h1"], "description": strip_tags(g["answer"]),
             "inLanguage": "sv-SE",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": t,
                       "text": strip_tags(" ".join(txt) if isinstance(txt, list) else txt)} for i, (t, txt) in enumerate(g["steps"])]}
    if g.get("need"):
        howto["tool"] = [{"@type": "HowToTool", "name": strip_tags(x)} for x in g["need"]]
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in g["faqs"]]}
    article = {"@context": "https://schema.org", "@type": "Article", "headline": g["h1"], "inLanguage": "sv-SE",
               "dateModified": g["updated"], "mainEntityOfPage": SITE_URL + path,
               "author": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL + "/om/"}}
    return layout(g["title"], g["desc"], path, body, [howto, faq, article, breadcrumb_schema(trail)])

def write(path, text):
    full = os.path.join(DIST, "index.html") if path == "/" else os.path.join(DIST, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)

def check(guides):
    slugs = [g["slug"] for g in guides]
    assert len(slugs) == len(set(slugs)), "Dubblett-slug"
    for g in guides:
        assert g["cat"] in CAT_NAME, g["slug"]
        for s in g.get("related", []):
            assert s in slugs, f"{g['slug']} länkar till okänd guide {s}"
        assert len(g["title"]) <= 70, f"För lång title: {g['slug']} ({len(g['title'])})"
        assert len(g["desc"]) <= 165, f"För lång description: {g['slug']} ({len(g['desc'])})"

def build():
    check(GUIDES)
    by_slug = {g["slug"]: g for g in GUIDES}
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    for fn in ("style.css", "search.js", "favicon.svg"):
        shutil.copy(os.path.join(SRC, fn), DIST)
    shutil.copytree(os.path.join(SRC, "fonts"), os.path.join(DIST, "fonts"))

    for g in GUIDES:
        write(f"/{g['slug']}/", guide_page(g, by_slug))

    # Kategorisidor
    for cid, cname, cdesc in CATS:
        items = [g for g in GUIDES if g["cat"] == cid]
        trail = [("Start", "/"), (cname, f"/{cid}/")]
        body = f"""{crumbs(trail)}
<h1>{esc(cname)}</h1>
<p class="lead">{esc(cdesc)}</p>
<div class="cards">{''.join(card(g) for g in items)}</div>"""
        write(f"/{cid}/", layout(f"{cname} – guider för dig som fixar själv | {SITE_NAME}", f"{cdesc} Enkla guider steg för steg från {SITE_NAME}.", f"/{cid}/", body, breadcrumb_schema(trail)))

    # Startsida
    groups = ""
    for cid, cname, cdesc in CATS:
        items = [g for g in GUIDES if g["cat"] == cid]
        if items:
            groups += f'<section class="grp"><h2><a href="/{cid}/" style="color:inherit;text-decoration:none">{esc(cname)}</a></h2><p>{esc(cdesc)}</p><div class="cards">{"".join(card(g) for g in items)}</div></section>'
    body = f"""<section class="hero">
<div>
<h1>Fixa det själv.</h1>
<p class="lead">Raka guider för det som krånglar hemma: stopp i avloppet, droppande kranar, kalla element och vitvaror som strular.</p>
</div>
{CAT_HERO}
</section>
<label class="search">{SEARCH_ICON}<input type="search" id="q" placeholder="Vad har gått sönder?" aria-label="Sök bland guiderna" autocomplete="off"></label>
<div id="guider">{groups}</div>
<p class="note" id="q-none" hidden>Ingen guide matchar ännu. Fler guider kommer löpande.</p>"""
    write("/", layout(f"{SITE_NAME} – guider för dig som fixar själv hemma",
                      "Enkla guider steg för steg för det som krånglar hemma: stopp i avloppet, droppande kran, kalla element och vitvaror. Skrivna av en fastighetsskötare.",
                      "/", body, {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": SITE_URL + "/"}))

    # Om
    write("/om/", layout(f"Om {SITE_NAME}", f"Vem som skriver guiderna på {SITE_NAME} och hur de tas fram.", "/om/", f"""<h1>Om Fixarfrassen</h1>
<p class="lead">Guider för dig som vill fixa själv, skrivna av någon som gör det varje vecka.</p>
<h2>Vem skriver?</h2>
<p>Guiderna bygger på erfarenhet från jobbet som fastighetsskötare, med elutbildning i botten. Det betyder felanmälningar varje vecka: stopp i avlopp, droppande kranar, kalla element, kylskåp som slutat kyla och persienner som hakat upp sig.</p>
<p>Frasse är sajtens maskot. Han gillar verktyg, pannlampor och att saker fungerar.</p>
<h2>Så skrivs guiderna</h2>
<p>Varje guide börjar med det enklaste och säkraste. Fungerar det inte går den vidare steg för steg. Där det finns risker, som el, kemikalier eller vattenskador, står det tydligt, och vi skriver när det är dags att ringa en fackman.</p>
<p>Guiderna tas fram med hjälp av AI och granskas mot erfarenhet från verkliga jobb.</p>
<h2>Fixarfrassen är ingen hantverkarfirma</h2>
<p>Vi utför inga uppdrag och går inte att boka. Sajten finansieras med annonser och ibland annonslänkar, som alltid märks tydligt.</p>
<h2>Ansvar</h2>
<p>Du gör jobbet på egen risk. Elinstallationer får bara göras av behörig elinstallatör, utöver enkla saker som att byta säkring eller lampa. Bor du i hyresrätt eller bostadsrätt, kontakta hyresvärden eller föreningen innan du gör något med rör, stammar eller värmesystem.</p>"""))

    # Integritet
    write("/integritet/", layout(f"Integritet och cookies | {SITE_NAME}", f"Hur {SITE_NAME} hanterar data och cookies.", "/integritet/", """<h1>Integritet och cookies</h1>
<p>Sajten använder i dag inga egna cookies och samlar inte in personuppgifter.</p>
<h2>Tjänster som används</h2>
<ul><li><strong>Cloudflare</strong> levererar sajten och tar, som alla webbservrar, emot din IP-adress när sidan hämtas.</li>
<li><strong>Typsnittet Inter</strong> hämtas från vår egen server.</li></ul>
<h2>Annonser och annonslänkar</h2>
<p>Om sajten visar annonser, till exempel från Google, eller har annonslänkar, kan tredje parter använda cookies för att mäta och visa annonser. Innan det sker uppdateras den här sidan och vi ber om ditt samtycke där lagen kräver det. Annonslänkar märks alltid tydligt.</p>"""))

    # 404
    with open(os.path.join(DIST, "404.html"), "w", encoding="utf-8") as f:
        f.write(layout(f"Sidan finns inte | {SITE_NAME}", "Sidan kunde inte hittas.", "/404", f"""<h1>Sidan finns inte</h1>
<p class="lead">Frasse letade med pannlampan men hittade inget. Här är alla guider:</p>
<div class="cards">{''.join(card(g) for g in GUIDES)}</div>""", noindex=True))

    # Sitemap och robots
    urls = [("/", max(g["updated"] for g in GUIDES))] + [(f"/{c[0]}/", max(g["updated"] for g in GUIDES if g["cat"] == c[0])) for c in CATS if any(g["cat"] == c[0] for g in GUIDES)] + [(f"/{g['slug']}/", g["updated"]) for g in GUIDES] + [("/om/", "2026-10-15"), ("/integritet/", "2026-10-15")]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u, d in urls:
        sm += f"  <url><loc>{SITE_URL}{u}</loc><lastmod>{d}</lastmod></url>\n"
    sm += "</urlset>\n"
    with open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sm)
    with open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("Klart:", len(urls), "sidor i", DIST)

if __name__ == "__main__":
    build()
