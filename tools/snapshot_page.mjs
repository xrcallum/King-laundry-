/* Pre-renders a route from the running dev server (:5173) to a self-contained static HTML file — used for the Canva Websites import (static HTML/CSS only, no JS). Usage: node tools/snapshot_page.mjs <out.html> [route] */
import { chromium } from 'playwright-core';
import { writeFileSync } from 'node:fs';
const OUT = process.argv[2];
const ROUTE = process.argv[3] || '/';
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' });
await page.goto('http://localhost:5173' + ROUTE, { waitUntil: 'networkidle' });
await page.evaluate(async () => {
  const step = innerHeight * 0.8;
  for (let y = 0; y < document.documentElement.scrollHeight; y += step) { scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); }
  scrollTo(0, 0);
});
await page.waitForTimeout(700);
const html = await page.evaluate(() => {
  document.querySelectorAll('script, link[rel="modulepreload"], link[rel="icon"]').forEach(n => n.remove());
  // Vite dev injects CSS as <style> tags; drop @font-face blocks pointing at /node_modules and use Google Fonts instead.
  document.querySelectorAll('style').forEach(s => {
    s.textContent = s.textContent.replace(/@font-face\s*\{[^}]*node_modules[^}]*\}/g, '');
    s.removeAttribute('data-vite-dev-id');
  });
  const gf = document.createElement('link');
  gf.rel = 'stylesheet';
  gf.href = 'https://fonts.googleapis.com/css2?family=Archivo:wght@400..900&family=Inter:wght@400..700&display=swap';
  document.head.prepend(gf);
  document.querySelectorAll('[style]').forEach(el => { if (el.style.transform && /translate3d\(0px, 0px/.test(el.style.transform)) el.style.transform = ''; });
  return '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
});
writeFileSync(OUT, html);
await browser.close();
console.log('wrote', OUT, html.length, 'bytes');
