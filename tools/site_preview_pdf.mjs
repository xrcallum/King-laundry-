/* Builds a single PDF preview of the whole site from the running dev server (:5173).
   Desktop pages for every route, then mobile pages for the key ones.
   Needs `npm run dev` + `npm run api` running, and pdf-lib installed outside the repo
   (kept out of package.json — it is only needed for this one-off deliverable):
     npm install --prefix /tmp/pdfbuild pdf-lib
     PDFLIB=/tmp/pdfbuild/node_modules/pdf-lib/cjs/index.js \
       node tools/site_preview_pdf.mjs LinenLegends-site-preview.pdf */
import { chromium } from 'playwright-core';
import { writeFileSync } from 'node:fs';
import { execSync } from 'node:child_process';
/* pdf-lib lives outside the repo (scratch install) so it stays out of package.json. */
const pdfLib = (await import(process.env.PDFLIB)).default;

const { PDFDocument, StandardFonts, rgb } = pdfLib;
const BASE = process.env.PREVIEW_BASE || 'http://localhost:5173';
const OUT = process.argv[2] || 'site-preview.pdf';

const ROUTES = [
  ['/', 'Home'],
  ['/book', 'Book a collection'],
  ['/services', 'Services'],
  ['/pricing', 'Pricing'],
  ['/legends-club', 'Legends Club'],
  ['/coverage', 'Coverage & suburbs'],
  ['/business', 'Business & commercial'],
  ['/supported-living', 'Supported living & aged care'],
  ['/operators', 'Become an operator'],
  ['/about', 'About us'],
  ['/guarantee', 'Service guarantee'],
  ['/faq', 'FAQ'],
  ['/contact', 'Contact'],
  ['/privacy', 'Privacy policy'],
  ['/terms', 'Terms of service'],
  ['/account', 'My account'],
  ['/messages', 'Messages'],
];
const MOBILE_ROUTES = ['/', '/book', '/pricing', '/legends-club', '/coverage'];

/* Fixed-position chrome repeats on every printed page in Chromium; the grain overlay
   would also wash the whole document. Neutralise for print only. */
const PRINT_CSS = `
  .grain::before { display: none !important; }
  .progress { display: none !important; }
  #site-menu { display: none !important; }
  .card { break-inside: avoid; }
`;

async function routePdf(browser, route, width, height) {
  const page = await browser.newPage({ viewport: { width, height }, reducedMotion: 'reduce' });
  await page.emulateMedia({ media: 'screen' });
  await page.goto(BASE + route, { waitUntil: 'networkidle' });
  await page.addStyleTag({ content: PRINT_CSS });
  // Scroll the whole page so IntersectionObserver reveals fire before printing.
  await page.evaluate(async () => {
    const step = innerHeight * 0.8;
    for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
      scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 80));
    }
    scrollTo(0, 0);
  });
  await page.waitForTimeout(600);
  const buf = await page.pdf({ width: `${width}px`, height: `${height}px`, printBackground: true, scale: 1 });
  await page.close();
  return buf;
}

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const out = await PDFDocument.create();
const bold = await out.embedFont(StandardFonts.HelveticaBold);
const reg = await out.embedFont(StandardFonts.Helvetica);
const NAVY = rgb(0.047, 0.149, 0.373);
const EMBER = rgb(0.769, 0.22, 0.157);

let sha = 'unknown';
try { sha = execSync('git rev-parse --short HEAD').toString().trim(); } catch { /* not a repo */ }

// Cover
{
  const p = out.addPage([1280, 800]);
  p.drawRectangle({ x: 0, y: 0, width: 1280, height: 800, color: NAVY });
  p.drawText('LINEN', { x: 90, y: 560, size: 68, font: bold, color: rgb(1, 1, 1) });
  p.drawText('LEGENDS', { x: 305, y: 560, size: 68, font: bold, color: EMBER });
  p.drawText('Website preview', { x: 92, y: 500, size: 26, font: reg, color: rgb(1, 1, 1) });
  const lines = [
    `Generated 21 September 2026 from commit ${sha}`,
    `${ROUTES.length} routes at 1280px, plus ${MOBILE_ROUTES.length} routes at 390px (mobile).`,
    'Rendered from the built site. Not the live production site — pre-launch.',
    'All prices shown include GST and are in AUD.',
  ];
  lines.forEach((t, i) => p.drawText(t, { x: 92, y: 430 - i * 30, size: 15, font: reg, color: rgb(0.85, 0.88, 0.94) }));
  p.drawText('Contents', { x: 92, y: 320, size: 15, font: bold, color: rgb(1, 1, 1) });
  ROUTES.forEach(([r, label], i) => {
    const col = Math.floor(i / 9);
    const row = i % 9;
    p.drawText(`${label}  ${r}`, { x: 92 + col * 380, y: 288 - row * 24, size: 12, font: reg, color: rgb(0.78, 0.82, 0.9) });
  });
}

async function append(route, label, width, height, tag) {
  process.stdout.write(`  ${tag} ${route} ... `);
  const buf = await routePdf(browser, route, width, height);
  const src = await PDFDocument.load(buf);
  const pages = await out.copyPages(src, src.getPageIndices());
  pages.forEach((pg) => out.addPage(pg));
  console.log(`${pages.length}p`);
}

console.log('desktop 1280x800');
for (const [route, label] of ROUTES) await append(route, label, 1280, 800, 'desktop');
console.log('mobile 390x844');
for (const route of MOBILE_ROUTES) {
  const label = ROUTES.find(([r]) => r === route)?.[1] || route;
  await append(route, label, 390, 844, 'mobile');
}

await browser.close();
writeFileSync(OUT, await out.save());
console.log('wrote', OUT, out.getPageCount(), 'pages');
