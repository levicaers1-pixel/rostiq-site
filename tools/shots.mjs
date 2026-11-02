// The app screenshots on the website (assets/shots/): the live demo teams on app.rostiq.be in screenshot mode
// (?demo=<sport>&shot: no demo bar), per sport and language, as a laptop picture (1600x960) and a phone picture (560x1120).
// Run after a visible change to the app:  node tools/shots.mjs   (then python tools/build.py)
// Uses Playwright from the app repo's tests (../rostiq/tests, "npm install" there once) and Edge or Chrome on this computer.
import { createRequire } from "node:module";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, "..", "assets", "shots");
const require = createRequire(path.join(process.env.PLAYWRIGHT_FROM || path.join(HERE, "..", "..", "rostiq", "tests"), "package.json"));
const { chromium } = require("playwright-core");

const SPORTS = ["football", "padel", "hockey", "golf"], LANGS = ["nl", "fr", "en"];
const SIZES = {
  "": { viewport: { width: 1280, height: 768 }, deviceScaleFactor: 1.25 },              // 1600 x 960
  "phone-": { viewport: { width: 375, height: 750 }, deviceScaleFactor: 560 / 375, isMobile: true, hasTouch: true }, // 560 x 1120
};

let browser;
for (const channel of ["msedge", "chrome"]) { try { browser = await chromium.launch({ channel, headless: true }); break; } catch {} }
if (!browser) { console.error("No Edge or Chrome found."); process.exit(2); }
const pngs = [];
for (const [prefix, size] of Object.entries(SIZES)) {
  for (const lang of LANGS) {
    const context = await browser.newContext({ ...size, locale: { nl: "nl-BE", fr: "fr-BE", en: "en-GB" }[lang], serviceWorkers: "block" });
    await context.addInitScript(l => { try { localStorage.setItem("lang", l); localStorage.setItem("theme", "light"); localStorage.setItem("pushLater", String(Date.now())); } catch {} }, lang);
    for (const sport of SPORTS) {
      const page = await context.newPage();
      await page.goto(`https://app.rostiq.be/?demo=${sport}&shot`, { waitUntil: "networkidle" });
      await page.waitForSelector("#hero", { state: "visible", timeout: 15000 });
      await page.waitForTimeout(1200); // fonts, icons, the countdown
      const file = path.join(OUT, `${prefix}${sport}-${lang}.png`);
      await page.screenshot({ path: file });
      pngs.push(file);
      console.log("shot", path.basename(file));
      await page.close();
    }
    await context.close();
  }
}
await browser.close();
// To WebP (smaller), the PNGs go.
const py = `
import sys, os
from PIL import Image
for f in sys.argv[1:]:
    Image.open(f).convert("RGB").save(f[:-4] + ".webp", "WEBP", quality=82, method=6)
    os.remove(f)
`;
const r = spawnSync(process.platform === "win32" ? "python" : "python3", ["-c", py, ...pngs], { stdio: "inherit" });
process.exit(r.status ?? 1);
