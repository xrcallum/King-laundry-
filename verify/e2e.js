/**
 * End-to-end check of the customer app against the real file.
 *
 * Runs with no db capability, which is the public/preview path: the app falls
 * back to in-session memory. Drives the flow a customer actually follows —
 * save an address, book a collection, see it in Bookings — and fails loudly on
 * any uncaught page error along the way.
 *
 * Usage: NODE_PATH=/opt/node22/lib/node_modules node verify/e2e.js <path-to-site.html>
 */
const { chromium } = require('playwright');

const file = process.argv[2];
if (!file) { console.error('usage: node verify/e2e.js <site.html>'); process.exit(2); }

const steps = [];
let failed = 0;
function check(name, ok, detail) {
  steps.push({ name, ok, detail });
  if (!ok) failed++;
  console.log(`  ${ok ? 'ok  ' : 'FAIL'}  ${name}${detail && !ok ? ' — ' + detail : ''}`);
}

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  // Network failures are environment noise (fonts are blocked in CI sandboxes),
  // not page defects. Only script errors count.
  page.on('console', m => {
    const t = m.text();
    if (m.type() === 'error' && !/Failed to load resource|ERR_CERT|ERR_INTERNET|net::/.test(t)) {
      errors.push('console: ' + t);
    }
  });

  const go = async (hash) => {
    await page.goto('file://' + file + hash, { waitUntil: 'load' });
    await page.waitForTimeout(400);
  };

  console.log('e2e:', file);

  // ---- boot -------------------------------------------------------------
  await go('#/app');
  check('app boots with no uncaught error', errors.length === 0, errors.slice(0, 3).join(' | '));
  check('app shell rendered', await page.locator('#tabs.live').count() === 1);
  check('wizard functions defined',
    await page.evaluate(() => typeof wireWizard === 'function' && typeof wireSettings === 'function'));

  // ---- save an address (wireSettings) -----------------------------------
  await go('#/address');
  await page.fill('#adLine1', '14 Wembley Road');
  await page.fill('#adSub', 'Meadowbrook');
  await page.fill('#adPc', '4131');
  await page.click('#adGo');
  await page.waitForTimeout(250);
  check('address save reports success',
    (await page.locator('#adMsg').getAttribute('class') || '').includes('ok'),
    await page.locator('#adMsg').textContent());
  check('coverage answered for a live postcode',
    (await page.locator('#adCov').textContent() || '').includes('Meadowbrook'));

  // ---- book a collection (wireWizard) -----------------------------------
  await go('#/book');
  check('wizard step 1 shows the saved address',
    (await page.locator('#bkPrInner').textContent() || '').includes('Meadowbrook'));

  await page.click('[data-svc="wf"]');
  await page.waitForTimeout(120);
  const qtyBefore = await page.locator('#bkNumA').textContent();
  await page.click('[data-bstep="a,1"]');
  await page.waitForTimeout(120);
  check('quantity stepper increments',
    Number(await page.locator('#bkNumA').textContent()) === Number(qtyBefore) + 1);

  await page.click('#bkN1');
  await page.waitForTimeout(250);
  check('step 2 reached', await page.locator('#st2.on').count() === 1);

  await page.click('[data-win="am"]');
  await page.waitForTimeout(150);
  await page.click('#bkN2');
  await page.waitForTimeout(250);
  check('step 3 reached', await page.locator('#st3.on').count() === 1);
  const sum = await page.locator('#bkSum').textContent();
  check('estimate shown on review', /\$\d/.test(sum || ''), sum);
  check('whole dollars drop the .00', !/\$\d+\.00\b/.test(sum || ''), sum);

  check('confirm is disabled until terms are accepted', await page.locator('#bkGo').isDisabled());
  await page.check('#bkTos');
  await page.waitForTimeout(120);
  check('confirm enabled after accepting terms', await page.locator('#bkGo').isEnabled());

  await page.click('#bkGo');
  await page.waitForTimeout(500);
  check('step 4 confirmation reached', await page.locator('#st4.on').count() === 1);
  const doneTx = await page.locator('#bkDoneTx').textContent();
  check('confirmation shows a booking reference', /LK-[A-Z0-9]+/.test(doneTx || ''), doneTx);

  // ---- the booking is visible afterwards --------------------------------
  const state = await page.evaluate(() => ({
    bookings: S.bookings.length,
    ref: S.bookings[0] && S.bookings[0].ref,
    status: S.bookings[0] && S.bookings[0].status,
    suburb: S.bookings[0] && S.bookings[0].suburb,
    messages: S.messages.length
  }));
  check('booking stored', state.bookings === 1 && state.status === 'requested', JSON.stringify(state));
  check('booking carries the collection suburb', state.suburb === 'Meadowbrook', JSON.stringify(state));
  check('customer notified in Messages', state.messages >= 1, JSON.stringify(state));

  await page.evaluate(() => { location.hash = '#/bookings'; });
  await page.waitForTimeout(400);
  const cards = await page.locator('#bkList .bkc, #bkList .ap-card').count();
  check('booking appears in Bookings', cards >= 1, 'cards=' + cards);

  // ---- no errors accumulated -------------------------------------------
  check('no uncaught errors across the flow', errors.length === 0, errors.slice(0, 4).join(' | '));

  await browser.close();
  console.log(`\n${steps.length - failed}/${steps.length} checks passed`);
  process.exit(failed ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
