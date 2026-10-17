// Render the lla.ma lockup (llama + "lla.ma") exactly like the site header's
// Wordmark (@lla-ma/ui navbar.jsx): mark 35px wide, gap 9px, DM Mono 500 at
// 16px, tracking-tight (-0.025em), text nudged down 4px, accent dot.
// Everything is scaled by S and screenshotted with a transparent background.
import { readFileSync } from "node:fs";
// Uses the Playwright install in llama-apps-cloud (no install needed here).
import { chromium } from "../../llama-supabase-vercel/llama-apps-cloud/node_modules/playwright/index.mjs";

const DIR = new URL(".", import.meta.url).pathname;
const OUT = new URL("../llama/logos", import.meta.url).pathname;
const S = 20;
const trim = readFileSync(`${DIR}llama-mark-trim.png`).toString("base64");

const OLIVE = "#7d9944", WHITE = "#ffffff", INK = "#0a0a0b";
const VARIANTS = [
  { name: "for-dark-bg", mark: OLIVE, text: WHITE, dot: OLIVE },
  { name: "for-light-bg", mark: OLIVE, text: INK, dot: OLIVE },
  { name: "white", mark: WHITE, text: WHITE, dot: WHITE },
  { name: "black", mark: INK, text: INK, dot: INK },
];

const page = await (await chromium.launch()).newPage({ viewport: { width: 2600, height: 1400 } });

for (const v of VARIANTS) {
  // The mark is recolored with a CSS mask so all variants share one shape.
  await page.setContent(`<!doctype html><html><head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@500&display=block">
    <style>
      html,body{margin:0;background:transparent}
      #lockup{display:inline-flex;align-items:center;gap:${9 * S}px;padding:2px}
      .mark{width:${35 * S}px;aspect-ratio:787/939;background:${v.mark};
        -webkit-mask:url(data:image/png;base64,${trim}) center/contain no-repeat}
      .word{font-family:"DM Mono";font-weight:500;font-size:${16 * S}px;letter-spacing:-0.025em;
        margin-top:${4 * S}px;color:${v.text};line-height:1}
      .dot{color:${v.dot}}
    </style></head><body>
    <div id="lockup"><div class="mark"></div><span class="word">lla<span class="dot">.</span>ma</span></div>
  </body></html>`);
  await page.evaluate(() => document.fonts.ready);
  const ok = await page.evaluate(() => document.fonts.check('500 320px "DM Mono"'));
  if (!ok) throw new Error("DM Mono did not load");
  await page.locator("#lockup").screenshot({ path: `${OUT}/raw-lockup-${v.name}.png`, omitBackground: true });
  console.log("rendered", v.name);
}
process.exit(0);
