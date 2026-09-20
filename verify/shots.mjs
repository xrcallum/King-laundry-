/* Route screenshot gate: renders routes at 390px and 1280px, fails on console errors. */
import { chromium } from 'playwright-core';
import { mkdirSync } from 'node:fs';

const BASE = process.env.SHOTS_BASE || 'http://localhost:5173';
const ROUTES = (process.env.SHOTS_ROUTES || '/').split(',');
mkdirSync('shots', { recursive: true });

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
let errors = [];
for (const [w, h, tag] of [[390, 844, 'mobile'], [1280, 800, 'desktop']]) {
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  page.on('console', (m) => { if (m.type() === 'error') errors.push(`${tag} ${page.url()} :: ${m.text()}`); });
  page.on('pageerror', (e) => errors.push(`${tag} ${page.url()} :: ${e.message}`));
  for (const r of ROUTES) {
    await page.goto(BASE + r, { waitUntil: 'networkidle' });
    await page.waitForTimeout(600);
    const name = (r === '/' ? 'home' : r.replaceAll('/', '_').slice(1));
    await page.screenshot({ path: `shots/${name}-${tag}.png`, fullPage: true });
  }
  // mobile menu check on home
  if (tag === 'mobile') {
    await page.goto(BASE + '/', { waitUntil: 'networkidle' });
    await page.click('button[aria-controls="site-menu"]');
    await page.waitForTimeout(600);
    const expanded = await page.getAttribute('button[aria-controls="site-menu"]', 'aria-expanded');
    await page.screenshot({ path: 'shots/menu-mobile.png' });
    await page.keyboard.press('Escape');
    await page.waitForTimeout(400);
    const closed = await page.getAttribute('button[aria-controls="site-menu"]', 'aria-expanded');
    if (expanded !== 'true' || closed !== 'false') errors.push(`menu toggle broken: open=${expanded} closed=${closed}`);
  }
  await page.close();
}
await browser.close();
if (errors.length) { console.log('CONSOLE/PAGE ERRORS:\n' + errors.join('\n')); console.log('RESULT: FAIL'); process.exit(1); }
console.log(`RESULT: PASS (${ROUTES.length} routes x2 widths, menu toggle ok)`);
