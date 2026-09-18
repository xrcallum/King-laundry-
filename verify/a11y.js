/**
 * Accessibility sweep over the rendered site.
 *
 * Walks every visible text node on every marketing and app route at phone
 * width, resolves the effective background behind it, and measures contrast.
 * Also checks that every interactive element has an accessible name and meets
 * the WCAG 2.2 target-size minimum.
 *
 * Usage: NODE_PATH=/opt/node22/lib/node_modules node verify/a11y.js <site.html>
 */
const { chromium } = require('playwright');

const file = process.argv[2];
if (!file) { console.error('usage: node verify/a11y.js <site.html>'); process.exit(2); }

const ROUTES = ['#/', '#/services', '#/pricing', '#/club', '#/business', '#/support',
  '#/coverage', '#/operators', '#/about', '#/guarantee', '#/faq', '#/contact',
  '#/privacy', '#/terms', '#/app', '#/book', '#/bookings', '#/account'];

const AUDIT = () => {
  const lum = (r, g, b) => {
    const f = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const parse = s => {
    const m = String(s).match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/);
    return m ? { r: +m[1], g: +m[2], b: +m[3], a: m[4] === undefined ? 1 : +m[4] } : null;
  };
  const over = (fg, bg) => ({
    r: fg.r * fg.a + bg.r * (1 - fg.a),
    g: fg.g * fg.a + bg.g * (1 - fg.a),
    b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1
  });
  const bgOf = el => {
    let node = el, acc = null;
    while (node && node.nodeType === 1) {
      const c = parse(getComputedStyle(node).backgroundColor);
      if (c && c.a > 0) { acc = acc ? over(acc, c) : c; if (acc.a >= 0.999) break; }
      node = node.parentElement;
    }
    return acc && acc.a >= 0.999 ? acc : { r: 255, g: 255, b: 255, a: 1 };
  };
  const ratio = (a, b) => {
    const la = lum(a.r, a.g, a.b), lb = lum(b.r, b.g, b.b);
    return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
  };

  const contrast = [], names = [], targets = [];
  const live = document.querySelector('.page.live');
  const scope = live ? [live, document.getElementById('nav'), document.getElementById('foot')].filter(Boolean) : [document.body];

  for (const root of scope) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let t;
    while ((t = walker.nextNode())) {
      const text = t.textContent.trim();
      if (!text || text.length < 2) continue;
      const el = t.parentElement;
      if (!el || el.closest('.ic-sprite,[hidden],.sr-only')) continue;
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
      const box = el.getBoundingClientRect();
      if (!box.width || !box.height) continue;
      const fg = parse(cs.color); if (!fg) continue;
      const bg = bgOf(el);
      const r = ratio(fg.a < 1 ? over(fg, bg) : fg, bg);
      const px = parseFloat(cs.fontSize), bold = +cs.fontWeight >= 700;
      const large = px >= 24 || (px >= 18.66 && bold);
      const need = large ? 3 : 4.5;
      // A logo is exempt from contrast under WCAG; nothing else is.
      if (r < need && !el.closest('.brand')) {
        contrast.push({ text: text.slice(0, 44), ratio: +r.toFixed(2), need, px: +px.toFixed(1), bold, sel: el.className || el.tagName });
      }
    }
    for (const el of root.querySelectorAll('a[href],button,input,select,textarea,[role="switch"]')) {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden' || el.closest('[hidden]')) continue;
      const box = el.getBoundingClientRect();
      if (!box.width || !box.height) continue;
      const name = (el.getAttribute('aria-label') || el.getAttribute('title') ||
        (el.labels && el.labels[0] && el.labels[0].textContent) || el.textContent || el.value || '').trim();
      if (!name) names.push({ tag: el.tagName, sel: el.className || el.id || '', html: el.outerHTML.slice(0, 80) });
      if (el.tagName !== 'A' && (box.width < 24 || box.height < 24)) {
        targets.push({ tag: el.tagName, sel: el.className || el.id || '', w: Math.round(box.width), h: Math.round(box.height) });
      }
    }
  }
  return { contrast, names, targets };
};

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  let bad = 0;
  const seen = new Set();
  for (const route of ROUTES) {
    await page.goto('file://' + file + route, { waitUntil: 'load' });
    await page.waitForTimeout(320);
    const r = await page.evaluate(AUDIT);
    const lines = [];
    for (const c of r.contrast) {
      const key = c.sel + '|' + c.ratio;
      if (seen.has(key)) continue;
      seen.add(key);
      lines.push(`      contrast ${c.ratio}:1 (needs ${c.need}) ${c.px}px${c.bold ? ' bold' : ''} — "${c.text}" [${c.sel}]`);
    }
    for (const n of r.names) {
      const key = 'n|' + n.html;
      if (seen.has(key)) continue;
      seen.add(key);
      lines.push(`      no accessible name: ${n.html}`);
    }
    for (const t of r.targets) {
      const key = 't|' + t.sel + t.w + t.h;
      if (seen.has(key)) continue;
      seen.add(key);
      lines.push(`      target ${t.w}x${t.h} under 24px — ${t.tag}.${t.sel}`);
    }
    bad += lines.length;
    console.log(`  ${lines.length ? 'FAIL' : 'ok  '}  ${route}${lines.length ? ' (' + lines.length + ')' : ''}`);
    lines.forEach(l => console.log(l));
  }
  await browser.close();
  console.log(bad ? `\n${bad} issue(s)` : '\nno contrast, naming or target-size issues found');
  process.exit(bad ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
