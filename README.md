# rostiq-site

The public website of RostiQ at **https://rostiq.be**: the landing page (NL/FR/EN, plain HTML, no build step).

The app itself lives in the [rostiq](https://github.com/levicaers1-pixel/rostiq) repo at **https://app.rostiq.be**.
Old app links that arrive on rostiq.be (`/?t=…`, `carpool.html`, `admin.html`, sign-in links…) are forwarded
there by the small pages in this repo and by `404.html`.

## Pages

- `index.html` – the landing page, with links to the demo teams (`app.rostiq.be/?demo=football|padel|hockey|golf`).
- `voetbal/`, `padel/`, `hockey/`, `golf/` – the same page per sport (own headline, search texts, mock-up and demo
  button). **Generated:** after changing `index.html`, run `python tools/make_sport_pages.py` (also rewrites `sitemap.xml`).
