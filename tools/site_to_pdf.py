#!/usr/bin/env python3
"""Render the live site to a single downloadable PDF: one route per page (or
more, where a route runs long), in reading order. Marketing pages first, then
the customer app after a real booking has been made so the screens are
populated rather than empty.

Usage: python3 tools/site_to_pdf.py <site.html> <out.pdf>
"""
import os
import subprocess
import sys

site = os.path.abspath(sys.argv[1])
out_pdf = os.path.abspath(sys.argv[2])
here = os.path.dirname(os.path.abspath(__file__))

MARKETING = [
    "/", "services", "pricing", "club", "business", "support",
    "coverage", "operators", "about", "guarantee", "faq", "contact",
    "privacy", "terms",
]

RENDER_JS = r"""
const { chromium } = require('playwright');
const fs = require('fs');

const site = process.argv[2];
const outDir = process.argv[3];
const routes = JSON.parse(process.argv[4]);

(async () => {
  const browser = await chromium.launch();
  const files = [];

  // ---- marketing pages, one PDF per route -------------------------------
  const mp = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await mp.emulateMedia({ reducedMotion: 'reduce' });
  for (const r of routes) {
    const hash = r === '/' ? '#/' : '#/' + r;
    await mp.goto('file://' + site + hash, { waitUntil: 'load' });
    await mp.waitForTimeout(450);
    await mp.evaluate(async () => {
      for (let y = 0; y < document.body.scrollHeight; y += 600) {
        window.scrollTo(0, y);
        await new Promise(res => setTimeout(res, 30));
      }
      window.scrollTo(0, 0);
    });
    await mp.waitForTimeout(250);
    const label = r === '/' ? 'home' : r;
    const f = `${outDir}/m_${label}.pdf`;
    await mp.pdf({
      path: f, printBackground: true, width: '1280px',
      margin: { top: '0', bottom: '0', left: '0', right: '0' },
      preferCSSPageSize: false
    });
    files.push(f);
    console.log('rendered', label);
  }

  // ---- app: seed a profile and a real booking so the screens are live ---
  const ap = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await ap.emulateMedia({ reducedMotion: 'reduce' });
  await ap.goto('file://' + site + '#/address', { waitUntil: 'load' });
  await ap.waitForTimeout(400);
  await ap.fill('#adLine1', '14 Wembley Road');
  await ap.fill('#adSub', 'Meadowbrook');
  await ap.fill('#adPc', '4131');
  await ap.click('#adGo');
  await ap.waitForTimeout(300);

  await ap.goto('file://' + site + '#/book', { waitUntil: 'load' });
  await ap.waitForTimeout(400);
  await ap.click('[data-svc="wf"]');
  await ap.waitForTimeout(150);
  await ap.click('#bkN1');
  await ap.waitForTimeout(250);
  await ap.click('[data-win="am"]');
  await ap.waitForTimeout(150);
  await ap.click('#bkN2');
  await ap.waitForTimeout(250);
  await ap.check('#bkTos');
  await ap.waitForTimeout(150);
  await ap.click('#bkGo');
  await ap.waitForTimeout(500);

  const appRoutes = [
    ['app', 'app-home'], ['bookings', 'app-bookings'], ['messages', 'app-messages'],
    ['account', 'app-settings'],
  ];
  for (const [route, label] of appRoutes) {
    await ap.evaluate(h => { location.hash = h; }, '#/' + route);
    await ap.waitForTimeout(400);
    const f = `${outDir}/a_${label}.pdf`;
    await ap.pdf({ path: f, printBackground: true, width: '390px', margin: { top: '0', bottom: '0', left: '0', right: '0' } });
    files.push(f);
    console.log('rendered', label);
  }

  await browser.close();
  fs.writeFileSync(`${outDir}/_manifest.json`, JSON.stringify(files));
})().catch(e => { console.error(e); process.exit(1); });
"""

import tempfile
tmpdir = tempfile.mkdtemp(prefix="lk-pdf-")
render_js_path = os.path.join(tmpdir, "render.js")
open(render_js_path, "w").write(RENDER_JS)

import json
env = dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules")
subprocess.run(["node", render_js_path, site, tmpdir, json.dumps(MARKETING)], check=True, env=env)

manifest = json.load(open(os.path.join(tmpdir, "_manifest.json")))
print("pages rendered:", len(manifest))

# Merge with pypdf (via the cryptography shim already set up in this session).
sys.path.insert(0, os.environ.get("PDF_SHIM", ""))
from pypdf import PdfReader, PdfWriter  # noqa: E402

writer = PdfWriter()
for f in manifest:
    r = PdfReader(f)
    for p in r.pages:
        writer.add_page(p)
with open(out_pdf, "wb") as fh:
    writer.write(fh)

print("done:", out_pdf, "-", len(PdfReader(out_pdf).pages), "pages,", os.path.getsize(out_pdf), "bytes")
