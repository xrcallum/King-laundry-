/**
 * Fixed-layer collision check against the real file.
 *
 * Two agents built this site in parallel and each added a floating layer at
 * the bottom of the phone screen: a "Book a collection" pill on the home
 * route, a chat button on every route, and the app tab bar on app routes.
 * Nothing checked them against each other or against the buttons beneath
 * them, and the owner photographed the pill sitting on the closing band's
 * own "Book a collection" button. This is the check that would have caught
 * it: it fails loudly if any fixed layer touches another fixed layer or
 * occludes a button or link, at phone widths, at the scroll positions where
 * the layers appear and disappear.
 *
 * Usage: NODE_PATH=/opt/node22/lib/node_modules node verify/collide.js <path-to-site.html>
 */
const path = require('path');
const { chromium } = require('playwright');

const file = process.argv[2];
if (!file) { console.error('usage: node verify/collide.js <site.html>'); process.exit(2); }
const F = 'file://' + path.resolve(file);

let failed = 0;
function check(name, ok, detail) {
  if (!ok) failed++;
  console.log(`  ${ok ? 'ok  ' : 'FAIL'}  ${name}${detail ? ' — ' + detail : ''}`);
}
const hit = (a, b) => a && b && a.width > 0 && b.width > 0
  && a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;

async function launch() {
  try { return await chromium.launch(); }
  catch (e) { return chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); }
}

(async () => {
  const browser = await launch();
  const errors = [];

  // Home route: the pill must yield to the hero, the closing band, the footer
  // and the assistant, and never touch the chat button or any control.
  for (const w of [320, 390, 430]) {
    const page = await browser.newPage({ viewport: { width: w, height: 844 } });
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(F + '#/home'); await page.waitForTimeout(1000);

    const pill = () => page.evaluate(() => {
      const el = document.querySelector('.stickyCta'); if (!el) return null;
      const cs = getComputedStyle(el), r = el.getBoundingClientRect();
      return { opacity: +cs.opacity, hidden: el.classList.contains('is-hidden'),
               rect: { left: r.left, right: r.right, top: r.top, bottom: r.bottom, width: r.width } };
    });
    const rect = sel => page.evaluate(s => {
      const e = document.querySelector(s); if (!e) return null;
      const cs = getComputedStyle(e); if (cs.display === 'none') return null;
      const r = e.getBoundingClientRect();
      return { left: r.left, right: r.right, top: r.top, bottom: r.bottom, width: r.width, height: r.height };
    }, sel);
    const scrollTo = frac => page.evaluate(f => {
      const max = document.documentElement.scrollHeight - innerHeight;
      window.scrollTo(0, f >= 1 ? document.documentElement.scrollHeight : max * f);
    }, frac);
    const settled = () => page.waitForTimeout(700); // past the 220ms fade with margin
    const gone = s => s && (s.hidden || s.opacity === 0);

    console.log(`\nhome @ ${w}px`);
    await scrollTo(0); await settled();
    let s = await pill();
    check('pill hidden while hero is on screen', gone(s), s && `opacity ${s.opacity}`);

    await scrollTo(0.5); await settled();
    s = await pill();
    check('pill visible mid-page', s && !s.hidden && s.opacity > 0.9, s && `opacity ${s.opacity}`);
    if (s) {
      check('pill keeps the 16px gutter', s.rect.left >= 15.5 && s.rect.right <= w - 0.5,
        `left ${Math.round(s.rect.left)} right ${Math.round(s.rect.right)}`);
      const fab = await rect('#aiFab');
      check('pill does not touch the chat button', !hit(s.rect, fab),
        `pill right ${Math.round(s.rect.right)} vs button left ${fab && Math.round(fab.left)}`);
      const under = await page.evaluate(pr => {
        const out = [];
        document.querySelectorAll('button, a[href]').forEach(el => {
          if (el.closest('.stickyCta') || el.closest('#aiFab')) return;
          if (getComputedStyle(el).position === 'fixed') return;
          const r = el.getBoundingClientRect(); if (!r.width) return;
          if (r.left < pr.right && pr.left < r.right && r.top < pr.bottom && pr.top < r.bottom)
            out.push((el.textContent || '').trim().slice(0, 30) || el.tagName);
        });
        return out;
      }, s.rect);
      check('pill occludes no button or link', under.length === 0, under.join(' | '));
    }

    await scrollTo(1); await settled();
    s = await pill();
    check('pill hidden over the closing band and footer', gone(s), s && `opacity ${s.opacity}`);

    await page.evaluate(() => { const el = document.querySelector('#finalcta .btn'); el && el.scrollIntoView({ block: 'center' }); });
    await settled();
    s = await pill();
    check('pill hidden while "Ready when you are" button is on screen', gone(s), s && `opacity ${s.opacity}`);

    await scrollTo(0.5); await settled();
    await page.click('#aiFab'); await page.waitForTimeout(500);
    s = await pill();
    check('pill hidden while assistant is open', gone(s));
    const panel = await rect('#aiPanel');
    check('assistant panel fits the viewport', panel && panel.left >= 0 && panel.right <= w && panel.bottom <= 844,
      panel && `right ${Math.round(panel.right)} bottom ${Math.round(panel.bottom)}`);
    await page.click('#aiX'); await page.waitForTimeout(600);
    s = await pill();
    check('pill returns when assistant closes', s && !s.hidden && s.opacity > 0.9);
    await page.close();
  }

  // App routes: the chat button must clear the tab bar, and the home pill
  // must not leak onto app screens.
  for (const w of [320, 390]) {
    const page = await browser.newPage({ viewport: { width: w, height: 844 } });
    page.on('pageerror', e => errors.push(e.message));
    console.log(`\napp routes @ ${w}px`);
    for (const r of ['app', 'book', 'bookings', 'account', 'rewards']) {
      await page.goto(F + '#/' + r); await page.waitForTimeout(900);
      const x = await page.evaluate(() => {
        const R = s => { const e = document.querySelector(s); if (!e) return null;
          if (getComputedStyle(e).display === 'none') return null;
          const b = e.getBoundingClientRect();
          return { left: b.left, right: b.right, top: b.top, bottom: b.bottom, width: b.width, height: b.height }; };
        return { tabs: R('#tabs'), fab: R('#aiFab'), pill: R('.stickyCta') };
      });
      check(`#/${r}: tab bar is live`, x.tabs && x.tabs.height > 0, x.tabs && `height ${Math.round(x.tabs.height)}`);
      check(`#/${r}: chat button clears the tab bar`, !hit(x.fab, x.tabs),
        `button bottom ${x.fab && Math.round(x.fab.bottom)} vs bar top ${x.tabs && Math.round(x.tabs.top)}`);
      check(`#/${r}: home pill not shown`, !x.pill);
    }
    await page.close();
  }

  await browser.close();
  const real = errors.filter(e => !/CERT_AUTHORITY/.test(e));
  if (real.length) { console.log(`\n${real.length} page error(s):`); real.slice(0, 5).forEach(e => console.log('   ', e)); }
  const bad = failed + real.length;
  console.log(bad ? `\nRESULT: FAIL - ${failed} check(s), ${real.length} page error(s)` : '\nRESULT: PASS');
  process.exit(bad ? 1 : 0);
})();
