"""Build the sport landing pages (rostiq.be/voetbal/, /padel/, /hockey/, /golf/) from index.html.

Each page is the main landing page with its own headline, search texts, phone mock-up and a button straight
to that sport's demo. Run after changing index.html:  python tools/make_sport_pages.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = "https://app.rostiq.be"

SPORTS = {
    "voetbal": {
        "demo": "football", "emoji": "⚽", "team": "KFC Zuiderpark", "opp": "VV Dorpsveld", "yes": 13, "min": 11, "chat": "Eerste ploeg ⚽",
        "nl": {"title": "Voetbalploeg plannen zonder app – RostiQ",
               "desc": "Weet wie er zaterdag speelt, wie naar de uitmatch rijdt en wie nog moet antwoorden. RostiQ is de gratis ploegplanner voor voetbalploegen – zonder app, via WhatsApp.",
               "eyebrow": "Voor voetbalploegen · Gratis tijdens de pilot", "h1a": "Elf man op zaterdag?", "h1b": "Weet het in één tik.",
               "lead": "RostiQ is de ploegplanner voor voetbalploegen: wie speelt er, wie rijdt naar de uitmatch en wie moet je nog porren – op één link in je WhatsApp-groep. Niemand hoeft een app te installeren.",
               "cta2": "Open de voetbaldemo", "f1a": "11/11 – we spelen!"},
        "fr": {"title": "Organiser son équipe de foot sans app – RostiQ", "eyebrow": "Pour les équipes de foot · Gratuit pendant le pilote",
               "h1a": "Onze joueurs samedi ?", "h1b": "Sache-le en un clic.",
               "lead": "RostiQ est le planificateur des équipes de foot : qui joue, qui conduit au match à l'extérieur et qui il faut encore relancer – sur un seul lien dans ton groupe WhatsApp. Personne n'a rien à installer.",
               "cta2": "Ouvrir la démo foot", "f1a": "11/11 – on joue !"},
        "en": {"title": "Plan your football team without an app – RostiQ", "eyebrow": "For football teams · Free during the pilot",
               "h1a": "Eleven players on Saturday?", "h1b": "Know it in one tap.",
               "lead": "RostiQ is the team planner for football teams: who's playing, who drives to the away game and who still needs a nudge – on one link in your WhatsApp group. Nobody has to install an app.",
               "cta2": "Open the football demo", "f1a": "11/11 – we're playing!"},
    },
    "padel": {
        "demo": "padel", "emoji": "🎾", "team": "Smash & Co", "opp": "Vibora Padel", "yes": 5, "min": 4, "chat": "Padel interclub 🎾",
        "nl": {"title": "Padel interclub plannen – RostiQ",
               "desc": "Plan je padelploeg zonder gedoe: wie speelt welke speeldag, wie rijdt met wie en wie je nog mist. Gratis ploegplanner voor padel interclub, zonder app.",
               "eyebrow": "Voor padelploegen · Gratis tijdens de pilot", "h1a": "Wie speelt er", "h1b": "deze interclub?",
               "lead": "Plan je padelploeg zonder gedoe: beschikbaarheid per speeldag, wie met wie naar de club rijdt en wie je nog mist – op één link in je WhatsApp-groep.",
               "cta2": "Open de padeldemo", "f1a": "4/4 – we spelen!"},
        "fr": {"title": "Organiser son interclub de padel – RostiQ", "eyebrow": "Pour les équipes de padel · Gratuit pendant le pilote",
               "h1a": "Qui joue", "h1b": "cet interclub ?",
               "lead": "Organise ton équipe de padel sans prise de tête : disponibilités par journée, qui va au club avec qui et qui manque encore – sur un seul lien dans ton groupe WhatsApp.",
               "cta2": "Ouvrir la démo padel", "f1a": "4/4 – on joue !"},
        "en": {"title": "Plan your padel interclub – RostiQ", "eyebrow": "For padel teams · Free during the pilot",
               "h1a": "Who's playing", "h1b": "this interclub?",
               "lead": "Plan your padel team without the hassle: availability per match day, who rides with whom and who's still missing – on one link in your WhatsApp group.",
               "cta2": "Open the padel demo", "f1a": "4/4 – we're playing!"},
    },
    "hockey": {
        "demo": "hockey", "emoji": "🏑", "team": "HC Scheldevallei", "opp": "Royal Lindenhof HC", "yes": 12, "min": 11, "chat": "Dames 1 🏑",
        "nl": {"title": "Hockeyploeg plannen zonder app – RostiQ",
               "desc": "Genoeg spelers voor zondag? RostiQ toont het in één oogopslag, regelt de carpool naar de uitmatch en herinnert wie nog moet antwoorden. Gratis voor hockeyploegen.",
               "eyebrow": "Voor hockeyploegen · Gratis tijdens de pilot", "h1a": "Genoeg volk", "h1b": "voor zondag?",
               "lead": "RostiQ toont in één oogopslag of je ploeg compleet is, regelt de carpool naar de uitmatch en herinnert wie nog moet antwoorden – via één link in je WhatsApp-groep.",
               "cta2": "Open de hockeydemo", "f1a": "11/11 – we spelen!"},
        "fr": {"title": "Organiser son équipe de hockey sans app – RostiQ", "eyebrow": "Pour les équipes de hockey · Gratuit pendant le pilote",
               "h1a": "Assez de monde", "h1b": "pour dimanche ?",
               "lead": "RostiQ montre en un coup d'œil si ton équipe est complète, organise le covoiturage vers le match à l'extérieur et rappelle qui doit encore répondre – via un seul lien dans ton groupe WhatsApp.",
               "cta2": "Ouvrir la démo hockey", "f1a": "11/11 – on joue !"},
        "en": {"title": "Plan your hockey team without an app – RostiQ", "eyebrow": "For hockey teams · Free during the pilot",
               "h1a": "Enough players", "h1b": "for Sunday?",
               "lead": "RostiQ shows at a glance whether your team is complete, sorts the carpool to the away game and reminds whoever still has to answer – through one link in your WhatsApp group.",
               "cta2": "Open the hockey demo", "f1a": "11/11 – we're playing!"},
    },
    "golf": {
        "demo": "golf", "emoji": "⛳", "team": "Golfclub De Linde", "opp": "Royal Heideveld", "yes": 6, "min": 4, "chat": "Interclub Heren ⛳",
        "nl": {"title": "Golf interclub plannen – RostiQ",
               "desc": "Wie speelt de interclub, wie rijdt naar de verre club en hoe laat vertrekken jullie? RostiQ plant je golf interclubteam zonder app, via WhatsApp. Gratis tijdens de pilot.",
               "eyebrow": "Voor golf interclub · Gratis tijdens de pilot", "h1a": "Je interclubteam,", "h1b": "zonder gedoe.",
               "lead": "Wie speelt de interclub, wie rijdt naar de verre club en hoe laat vertrekken jullie? RostiQ zet het op één link in je WhatsApp-groep, met rijtijden en vertrekuur erbij.",
               "cta2": "Open de golfdemo", "f1a": "4/4 – we spelen!"},
        "fr": {"title": "Organiser son interclub de golf – RostiQ", "eyebrow": "Pour l'interclub de golf · Gratuit pendant le pilote",
               "h1a": "Ton équipe d'interclub,", "h1b": "sans prise de tête.",
               "lead": "Qui joue l'interclub, qui conduit jusqu'au club lointain et à quelle heure partir ? RostiQ réunit tout sur un seul lien dans ton groupe WhatsApp, avec temps de trajet et heure de départ.",
               "cta2": "Ouvrir la démo golf", "f1a": "4/4 – on joue !"},
        "en": {"title": "Plan your golf interclub – RostiQ", "eyebrow": "For golf interclub · Free during the pilot",
               "h1a": "Your interclub team,", "h1b": "without the hassle.",
               "lead": "Who plays the interclub, who drives to the far-away club and when do you leave? RostiQ puts it on one link in your WhatsApp group, with driving times and departure time included.",
               "cta2": "Open the golf demo", "f1a": "4/4 – we're playing!"},
    },
}


def esc(t):
    return t.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def build(slug, sp, template):
    s, nl = template, sp["nl"]
    url = f"https://rostiq.be/{slug}/"

    def rep(a, b, count=1):
        nonlocal s
        assert s.count(a) == count, (slug, s.count(a), a[:60])
        s = s.replace(a, b)

    rep("<title>RostiQ – Je ploeg geregeld, zonder app</title>", f"<title>{esc(nl['title'])}</title>")
    start = s.index('<meta name="description" content="'); end = s.index('">', start)
    s = s[:start] + f'<meta name="description" content="{esc(nl["desc"])}' + s[end:]
    rep('<link rel="canonical" href="https://rostiq.be/">', f'<link rel="canonical" href="{url}">')
    rep('<meta property="og:url" content="https://rostiq.be/">', f'<meta property="og:url" content="{url}">')
    rep('<meta property="og:title" content="RostiQ – Stop met tellen in de WhatsApp-groep">', f'<meta property="og:title" content="{esc(nl["title"])}">')
    # Dutch texts straight in the HTML (also what search engines read)
    for key, field in [("hero.eyebrow", "eyebrow"), ("hero.h1a", "h1a"), ("hero.h1b", "h1b"), ("hero.lead", "lead")]:
        i = s.index(f'data-t="{key}">') + len(f'data-t="{key}">'); j = s.index("</", i)
        s = s[:i] + nl[field] + s[j:]
    # the second hero button opens this sport's demo
    rep('<a class="btn btn-ghost btn-lg" href="#demo" data-t="hero.cta2">Probeer de demo</a>',
        f'<a class="btn btn-ghost btn-lg" href="{APP}/?demo={sp["demo"]}" data-t="hero.cta2">{nl["cta2"]}</a>', 2)
    # phone mock-up and chat in this sport
    rep("<b>KHC Dragons H3</b>", f"<b>{esc(sp['team'])}</b>")
    rep('<div class="m-title">Royal Antwerp HC</div>', f'<div class="m-title">{esc(sp["opp"])}</div>', 2)
    rep("<b>9</b> / 11 ", f"<b>{sp['yes']}</b> / {sp['min']} ", 2)
    rep("Heren 3 🏑<small", f"{sp['chat']}<small")
    # texts per language for the script (also NL, for the language switch back to Dutch)
    over = {lang: {"doc.title": sp[lang]["title"], "hero.eyebrow": sp[lang]["eyebrow"], "hero.h1a": sp[lang]["h1a"], "hero.h1b": sp[lang]["h1b"],
                   "hero.lead": sp[lang]["lead"], "hero.cta2": sp[lang]["cta2"], "f1a": sp[lang]["f1a"]} for lang in ("nl", "fr", "en")}
    rep('<script src="/icons.js"></script>', f'<script>window.SPORT_TXT = {json.dumps(over, ensure_ascii=False)};</script>\n<script src="/icons.js"></script>')
    out = os.path.join(ROOT, slug)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def main():
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
        template = f.read()
    for slug, sp in SPORTS.items():
        build(slug, sp, template)
        print("wrote", slug + "/index.html")
    urls = ["https://rostiq.be/"] + [f"https://rostiq.be/{slug}/" for slug in SPORTS]
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f"  <url><loc>{u}</loc><changefreq>weekly</changefreq><priority>{'1.0' if u.endswith('.be/') else '0.8'}</priority></url>\n")
        f.write(f"  <url><loc>{APP}/privacy.html</loc><changefreq>monthly</changefreq></url>\n</urlset>\n")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
