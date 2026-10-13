"""Build the website from src/template.html (the Dutch landing page with all texts).

Output, one address per language so search engines index every language:
  /            /fr/            /en/             the landing page
  /voetbal/    /fr/football/   /en/football/    and /padel/, /hockey/, /golf/ in each language: a sport landing page
plus sitemap.xml with the language alternates. Run after changing the template:  python tools/build.py
"""
import html
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://rostiq.be"
APP = "https://app.rostiq.be"
LANGS = ["nl", "fr", "en"]
LOCALE = {"nl": "nl_BE", "fr": "fr_BE", "en": "en_GB"}
SHOT_ALT = {"nl": "RostiQ: beschikbaarheid, wedstrijden en carpool van een demoploeg",
            "fr": "RostiQ : disponibilités, matchs et covoiturage d'une équipe démo",
            "en": "RostiQ: availability, matches and carpools of a demo team"}

SPORTS = {
    "voetbal": {
        "slug": {"nl": "voetbal", "fr": "football", "en": "football"},
        "demo": "football", "team": "KFC Zuiderpark", "opp": "VV Dorpsveld", "yes": 13, "min": 11, "chat": "Eerste ploeg ⚽",
        "nl": {"doc.title": "Voetbalploeg plannen zonder app – RostiQ",
               "doc.desc": "Weet wie er zaterdag speelt, wie naar de uitmatch rijdt en wie nog moet antwoorden. RostiQ is de gratis ploegplanner voor voetbalploegen – zonder app, via WhatsApp.",
               "hero.eyebrow": "Voor voetbalploegen · Gratis tijdens de pilot", "hero.h1a": "Elf man op zaterdag?", "hero.h1b": "Weet het in één tik.",
               "hero.lead": "RostiQ is de ploegplanner voor voetbalploegen: wie speelt er, wie rijdt naar de uitmatch en wie moet je nog porren – op één link in je WhatsApp-groep. Niemand hoeft een app te installeren.",
               "hero.cta2": "Open de voetbaldemo", "f1a": "11/11 – we spelen!"},
        "fr": {"doc.title": "Organiser son équipe de foot sans app – RostiQ",
               "doc.desc": "Sache qui joue samedi, qui conduit au match à l'extérieur et qui doit encore répondre. RostiQ est le planificateur gratuit des équipes de foot – sans app, via WhatsApp.",
               "hero.eyebrow": "Pour les équipes de foot · Gratuit pendant le pilote", "hero.h1a": "Onze joueurs samedi ?", "hero.h1b": "Sache-le en un clic.",
               "hero.lead": "RostiQ est le planificateur des équipes de foot : qui joue, qui conduit au match à l'extérieur et qui il faut encore relancer – sur un seul lien dans ton groupe WhatsApp. Personne n'a rien à installer.",
               "hero.cta2": "Ouvrir la démo foot", "f1a": "11/11 – on joue !"},
        "en": {"doc.title": "Plan your football team without an app – RostiQ",
               "doc.desc": "Know who's playing on Saturday, who drives to the away game and who still has to answer. RostiQ is the free team planner for football teams – no app, via WhatsApp.",
               "hero.eyebrow": "For football teams · Free during the pilot", "hero.h1a": "Eleven players on Saturday?", "hero.h1b": "Know it in one tap.",
               "hero.lead": "RostiQ is the team planner for football teams: who's playing, who drives to the away game and who still needs a nudge – on one link in your WhatsApp group. Nobody has to install an app.",
               "hero.cta2": "Open the football demo", "f1a": "11/11 – we're playing!"},
    },
    "padel": {
        "slug": {"nl": "padel", "fr": "padel", "en": "padel"},
        "demo": "padel", "team": "Smash & Co", "opp": "Vibora Padel", "yes": 5, "min": 4, "chat": "Padel interclub 🎾",
        "nl": {"doc.title": "Padel interclub plannen – RostiQ",
               "doc.desc": "Plan je padelploeg zonder gedoe: wie speelt welke speeldag, wie rijdt met wie en wie je nog mist. Gratis ploegplanner voor padel interclub, zonder app.",
               "hero.eyebrow": "Voor padelploegen · Gratis tijdens de pilot", "hero.h1a": "Wie speelt er", "hero.h1b": "deze interclub?",
               "hero.lead": "Plan je padelploeg zonder gedoe: beschikbaarheid per speeldag, wie met wie naar de club rijdt en wie je nog mist – op één link in je WhatsApp-groep.",
               "hero.cta2": "Open de padeldemo", "f1a": "4/4 – we spelen!"},
        "fr": {"doc.title": "Organiser son interclub de padel – RostiQ",
               "doc.desc": "Organise ton équipe de padel sans prise de tête : qui joue quelle journée, qui va avec qui et qui manque encore. Planificateur gratuit pour l'interclub de padel, sans app.",
               "hero.eyebrow": "Pour les équipes de padel · Gratuit pendant le pilote", "hero.h1a": "Qui joue", "hero.h1b": "cet interclub ?",
               "hero.lead": "Organise ton équipe de padel sans prise de tête : disponibilités par journée, qui va au club avec qui et qui manque encore – sur un seul lien dans ton groupe WhatsApp.",
               "hero.cta2": "Ouvrir la démo padel", "f1a": "4/4 – on joue !"},
        "en": {"doc.title": "Plan your padel interclub – RostiQ",
               "doc.desc": "Plan your padel team without the hassle: who plays which match day, who rides with whom and who's still missing. Free team planner for padel interclub, no app.",
               "hero.eyebrow": "For padel teams · Free during the pilot", "hero.h1a": "Who's playing", "hero.h1b": "this interclub?",
               "hero.lead": "Plan your padel team without the hassle: availability per match day, who rides with whom and who's still missing – on one link in your WhatsApp group.",
               "hero.cta2": "Open the padel demo", "f1a": "4/4 – we're playing!"},
    },
    "hockey": {
        "slug": {"nl": "hockey", "fr": "hockey", "en": "hockey"},
        "demo": "hockey", "team": "HC Scheldevallei", "opp": "Royal Lindenhof HC", "yes": 12, "min": 11, "chat": "Dames 1 🏑",
        "nl": {"doc.title": "Hockeyploeg plannen zonder app – RostiQ",
               "doc.desc": "Genoeg spelers voor zondag? RostiQ toont het in één oogopslag, regelt de carpool naar de uitmatch en herinnert wie nog moet antwoorden. Gratis voor hockeyploegen.",
               "hero.eyebrow": "Voor hockeyploegen · Gratis tijdens de pilot", "hero.h1a": "Genoeg volk", "hero.h1b": "voor zondag?",
               "hero.lead": "RostiQ toont in één oogopslag of je ploeg compleet is, regelt de carpool naar de uitmatch en herinnert wie nog moet antwoorden – via één link in je WhatsApp-groep.",
               "hero.cta2": "Open de hockeydemo", "f1a": "11/11 – we spelen!"},
        "fr": {"doc.title": "Organiser son équipe de hockey sans app – RostiQ",
               "doc.desc": "Assez de joueurs pour dimanche ? RostiQ le montre en un coup d'œil, organise le covoiturage et rappelle qui doit encore répondre. Gratuit pour les équipes de hockey.",
               "hero.eyebrow": "Pour les équipes de hockey · Gratuit pendant le pilote", "hero.h1a": "Assez de monde", "hero.h1b": "pour dimanche ?",
               "hero.lead": "RostiQ montre en un coup d'œil si ton équipe est complète, organise le covoiturage vers le match à l'extérieur et rappelle qui doit encore répondre – via un seul lien dans ton groupe WhatsApp.",
               "hero.cta2": "Ouvrir la démo hockey", "f1a": "11/11 – on joue !"},
        "en": {"doc.title": "Plan your hockey team without an app – RostiQ",
               "doc.desc": "Enough players for Sunday? RostiQ shows it at a glance, sorts the carpool to the away game and reminds whoever still has to answer. Free for hockey teams.",
               "hero.eyebrow": "For hockey teams · Free during the pilot", "hero.h1a": "Enough players", "hero.h1b": "for Sunday?",
               "hero.lead": "RostiQ shows at a glance whether your team is complete, sorts the carpool to the away game and reminds whoever still has to answer – through one link in your WhatsApp group.",
               "hero.cta2": "Open the hockey demo", "f1a": "11/11 – we're playing!"},
    },
    "golf": {
        "slug": {"nl": "golf", "fr": "golf", "en": "golf"},
        "demo": "golf", "team": "Golfclub De Linde", "opp": "Royal Heideveld", "yes": 6, "min": 4, "chat": "Interclub Heren ⛳",
        "nl": {"doc.title": "Golf interclub plannen – RostiQ",
               "doc.desc": "Wie speelt de interclub, wie rijdt naar de verre club en hoe laat vertrekken jullie? RostiQ plant je golf interclubteam zonder app, via WhatsApp. Gratis tijdens de pilot.",
               "hero.eyebrow": "Voor golf interclub · Gratis tijdens de pilot", "hero.h1a": "Je interclubteam,", "hero.h1b": "zonder gedoe.",
               "hero.lead": "Wie speelt de interclub, wie rijdt naar de verre club en hoe laat vertrekken jullie? RostiQ zet het op één link in je WhatsApp-groep, met rijtijden en vertrekuur erbij.",
               "hero.cta2": "Open de golfdemo", "f1a": "4/4 – we spelen!"},
        "fr": {"doc.title": "Organiser son interclub de golf – RostiQ",
               "doc.desc": "Qui joue l'interclub, qui conduit jusqu'au club lointain et à quelle heure partir ? RostiQ organise ton équipe d'interclub de golf sans app, via WhatsApp. Gratuit pendant le pilote.",
               "hero.eyebrow": "Pour l'interclub de golf · Gratuit pendant le pilote", "hero.h1a": "Ton équipe d'interclub,", "hero.h1b": "sans prise de tête.",
               "hero.lead": "Qui joue l'interclub, qui conduit jusqu'au club lointain et à quelle heure partir ? RostiQ réunit tout sur un seul lien dans ton groupe WhatsApp, avec temps de trajet et heure de départ.",
               "hero.cta2": "Ouvrir la démo golf", "f1a": "4/4 – on joue !"},
        "en": {"doc.title": "Plan your golf interclub – RostiQ",
               "doc.desc": "Who plays the interclub, who drives to the far-away club and when do you leave? RostiQ plans your golf interclub team without an app, via WhatsApp. Free during the pilot.",
               "hero.eyebrow": "For golf interclub · Free during the pilot", "hero.h1a": "Your interclub team,", "hero.h1b": "without the hassle.",
               "hero.lead": "Who plays the interclub, who drives to the far-away club and when do you leave? RostiQ puts it on one link in your WhatsApp group, with driving times and departure time included.",
               "hero.cta2": "Open the golf demo", "f1a": "4/4 – we're playing!"},
    },
}


def path_of(page, lang):
    """URL path of a page in a language, e.g. ('voetbal', 'fr') -> '/fr/football/'."""
    prefix = "" if lang == "nl" else f"/{lang}"
    if page == "home":
        return prefix + "/"
    return f"{prefix}/{SPORTS[page]['slug'][lang]}/"


def find_elements(s, key):
    """(start, end) of the inner HTML of every element with data-t="key" (nesting-aware)."""
    out, pos = [], 0
    needle = f'data-t="{key}"'
    while True:
        i = s.find(needle, pos)
        if i < 0:
            return out
        tag_start = s.rfind("<", 0, i)
        name = re.match(r"<([a-zA-Z0-9]+)", s[tag_start:]).group(1)
        inner_start = s.index(">", i) + 1
        depth, j = 1, inner_start
        pat = re.compile(rf"<(/?){name}\b[^>]*>")
        while depth:
            m = pat.search(s, j)
            depth += -1 if m.group(1) else 1
            j = m.end()
        out.append((inner_start, m.start()))
        pos = j


def set_text(s, key, value):
    for a, b in reversed(find_elements(s, key)):
        s = s[:a] + value + s[b:]
    return s


def get_text(s, key):
    els = find_elements(s, key)
    return s[els[0][0]:els[0][1]] if els else None


def plain(h):
    return html.unescape(re.sub(r"<[^>]+>", "", h)).strip()


def load_txt(template):
    i = template.index('<script id="txt-src">') + len('<script id="txt-src">')
    code = template[i:template.index("</script>", i)]
    res = subprocess.run(["node", "-e", code + "\nprocess.stdout.write(JSON.stringify(TXT));"], capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(res.stdout)


def load_icons():
    """name -> inline SVG, from icons.js (the same line icons the app uses)."""
    code = open(os.path.join(ROOT, "icons.js"), encoding="utf-8").read()
    i = code.index("const ICONS"); j = code.index("// Emoji in the interface")
    res = subprocess.run(["node", "-e", code[i:j] + "\nprocess.stdout.write(JSON.stringify(Object.fromEntries(Object.keys(ICONS).map(k => [k, ic(k)]))));"],
                         capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(res.stdout)


def build_page(template, txt, page, lang, icons):
    s = template
    sp = SPORTS.get(page)

    def rep(a, b, count=1):
        nonlocal s
        assert s.count(a) == count, (page, lang, s.count(a), a[:60])
        s = s.replace(a, b)

    # Texts: the language's translations, then the sport's own texts
    texts = dict(txt.get(lang, {})) if lang != "nl" else {}
    if sp:
        texts.update(sp[lang])
        rep('<a class="btn btn-ghost btn-lg" href="#demo" data-t="hero.cta2">', f'<a class="btn btn-ghost btn-lg" href="{APP}/?demo={sp["demo"]}" data-t="hero.cta2">', 2)
        rep('<div class="m-title">Royal Antwerp HC</div>', f'<div class="m-title">{html.escape(sp["opp"])}</div>')
        rep("<b>9</b> / 11 ", f"<b>{sp['yes']}</b> / {sp['min']} ")
        rep("Heren 3 🏑<small", f"{sp['chat']}<small")
    for key, value in texts.items():
        s = set_text(s, key, value)
    # The real app as the hero picture: this sport's demo team (the landing page: football), in this language
    shot = sp["demo"] if sp else "football"
    rep('<img src="/assets/shots/football-nl.webp" width="1600" height="960" alt="RostiQ: de beschikbaarheid van een voetbalploeg"',
        f'<img src="/assets/shots/{shot}-{lang}.webp" width="1600" height="960" alt="{html.escape(SHOT_ALT[lang])}"')

    nl_desc = re.search(r'<meta name="description" content="([^"]*)"', template).group(1)
    title = texts.get("doc.title") or re.search(r"<title>([^<]*)</title>", template).group(1)
    desc = texts.get("doc.desc") or nl_desc
    og_title = texts.get("og.title") if not sp and lang != "nl" else (title if sp else None)
    og_desc = texts.get("og.desc") if not sp and lang != "nl" else (desc if sp else None)
    url = SITE + path_of(page, lang)

    s = re.sub(r"<html lang=\"[a-z]+\">", f'<html lang="{lang}">', s, count=1)
    s = re.sub(r"<title>[^<]*</title>", f"<title>{html.escape(title, quote=False)}</title>", s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc)}">', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', s, count=1)
    s = re.sub(r'<meta property="og:locale" content="[^"]*">', f'<meta property="og:locale" content="{LOCALE[lang]}">', s, count=1)
    if og_title:
        s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(og_title)}">', s, count=1)
    if og_desc:
        s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{html.escape(og_desc)}">', s, count=1)

    # The same page in the other languages (for search engines and the language switch)
    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{path_of(page, l)}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{path_of(page, "nl")}">'
    rep("<!--ALTERNATES-->", alts)
    for l in LANGS:
        default = "/" if l == "nl" else f"/{l}/"
        rep(f'<a data-lang="{l}" href="{default}" hreflang="{l}">',
            f'<a data-lang="{l}" href="{path_of(page, l)}" hreflang="{l}"' + (' aria-current="true"' if l == lang else "") + ">")
    # Sport pills link to the sport pages in this language
    for page_id, key in [("golf", "sp.golf"), ("padel", "sp.padel"), ("hockey", "sp.hockey"), ("voetbal", "sp.football")]:
        rep(f'<a class="sport" href="/{SPORTS[page_id]["slug"]["nl"]}/"><span>', f'<a class="sport" href="{path_of(page_id, lang)}"><span>', 1)

    # Structured data: the product, and (on the landing pages) the FAQ for rich results
    data = [{
        "@context": "https://schema.org", "@type": "SoftwareApplication", "name": "RostiQ", "url": url,
        "applicationCategory": "SportsApplication", "operatingSystem": "Web, iOS, Android", "inLanguage": lang, "description": desc,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "publisher": {"@type": "Organization", "name": "RostiQ", "url": SITE + "/", "logo": SITE + "/assets/icon-512.png", "email": "levi@caersultancy.com"},
    }]
    if not sp:
        qa = []
        for n in range(0, 8):
            q, a = get_text(s, f"q{n}"), get_text(s, f"a{n}")
            if q and a:
                qa.append({"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}})
        data.append({"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang, "mainEntity": qa})
    ld = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    rep("<!--JSONLD-->", f'<script type="application/ld+json">\n{ld}\n</script>')

    # Icons straight in the HTML: nothing shifts when the page's script runs
    s = re.sub(r'(data-ic="([a-z-]+)"[^>]*>)(</span>|</div>)', lambda m: m.group(1) + icons[m.group(2)] + m.group(3), s)

    # The translations were only needed here
    i = s.index('<script id="txt-src">'); j = s.index("</script>", i) + len("</script>\n")
    s = s[:i] + s[j:]
    return s


def main():
    template = open(os.path.join(ROOT, "src", "template.html"), encoding="utf-8").read()
    txt = load_txt(template)
    icons = load_icons()
    pages = ["home"] + list(SPORTS)
    for page in pages:
        for lang in LANGS:
            out = os.path.join(ROOT, path_of(page, lang).strip("/"), "index.html")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8", newline="\n") as f:
                f.write(build_page(template, txt, page, lang, icons))
            print("wrote", path_of(page, lang))
    # Sitemap with the language alternates of every page
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for page in pages:
        for lang in LANGS:
            lines.append(f"  <url><loc>{SITE}{path_of(page, lang)}</loc><changefreq>weekly</changefreq><priority>{'1.0' if page == 'home' else '0.8'}</priority>")
            for l in LANGS:
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{path_of(page, l)}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{path_of(page, "nl")}"/></url>')
    lines.append(f"  <url><loc>{APP}/privacy.html</loc><changefreq>monthly</changefreq></url>")
    lines.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
