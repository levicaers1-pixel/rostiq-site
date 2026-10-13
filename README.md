# rostiq-site

The public website of RostiQ at **https://rostiq.be**: the landing page (NL/FR/EN, plain HTML, no build step).

The app itself lives in the [rostiq](https://github.com/levicaers1-pixel/rostiq) repo at **https://app.rostiq.be**.
Old app links that arrive on rostiq.be (`/?t=…`, `carpool.html`, `admin.html`, sign-in links…) are forwarded
there by the small pages in this repo and by `404.html`.

## Pages

The site is generated from `src/template.html` (the Dutch landing page with the French and English texts):
run `python tools/build.py` after every change. It writes one address per language, so search engines index
all three:

| | NL | FR | EN |
|---|---|---|---|
| Landing page | `/` | `/fr/` | `/en/` |
| Sport pages | `/voetbal/` `/padel/` `/hockey/` `/golf/` | `/fr/football/` `/fr/padel/` … | `/en/football/` … |

Each page gets its title and description, `hreflang` alternates, Open Graph tags and structured data
(SoftwareApplication, plus FAQPage on the landing pages), and `sitemap.xml` lists every page with its alternates.
The language switch links between the versions; a first-time visitor of a Dutch page whose browser prefers
French or English is sent to that version (search engines are not).
