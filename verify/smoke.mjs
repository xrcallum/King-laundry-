/* API smoke gate — the §7.1 curl cases. Fails loud on any wrong number. */
const BASE = process.env.SMOKE_BASE || 'http://localhost:8787';
let failures = 0;
const eq = (name, got, want) => {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}  got=${JSON.stringify(got)}${ok ? '' : `  want=${JSON.stringify(want)}`}`);
  if (!ok) failures++;
};
const post = async (p, b) => (await fetch(BASE + p, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(b) })).json();
const get = async (p) => (await fetch(BASE + p)).json();

// 1–3 estimator
let r = await post('/api/estimate', { service: 'wf', qty: 2 });
eq('wf x2 total', [r.total, r.minimumApplied], [77.5, false]);
r = await post('/api/estimate', { service: 'wf', qty: 1 });
eq('wf x1 min order', [r.total, r.minimumApplied], [73.5, true]);
r = await post('/api/estimate', { service: 'linen', qty: 3 });
eq('linen x3 48h', [r.total, r.turnaround], [109.5, '48h']);
// 4–6 coverage
r = await get('/api/coverage/check?postcode=4131');
eq('4131 active', [r.status, r.suburb], ['active', 'Meadowbrook']);
r = await get('/api/coverage/check?postcode=4509');
eq('4509 opening', [r.status, r.suburb], ['opening', 'Mango Hill']);
r = await get('/api/coverage/check?postcode=9000');
eq('9000 waitlist', r.status, 'waitlist');
// 7 waitlist
r = await post('/api/waitlist', { postcode: '9000', email: 'test@example.com' });
eq('waitlist ok', [r.ok, typeof r.id], [true, 'string']);
// 8 booking
r = await post('/api/bookings', {
  service: 'wf', qty: 2, name: 'Test Person', phone: '0400000000', email: 'test@example.com',
  address: '1 Test St', suburb: 'Meadowbrook', postcode: '4131', date: '2026-09-25', window: '9am–12pm', consent: true,
});
eq('booking ok', [r.ok, /^LL-[A-Z0-9]{6}$/.test(r.id || ''), r.estimate?.total, r.status], [true, true, 77.5, 'awaiting-operator']);
const bid = r.id;
r = await get('/api/bookings?id=' + bid);
eq('booking readback', [r.ok, r.booking?.statusHistory?.length >= 1], [true, true]);
// 9 contact + enquiries
r = await post('/api/contact', { name: 'T', email: 't@example.com', message: 'hello', complaint: false });
eq('contact ok', r.ok, true);
for (const kind of ['business', 'supported-living', 'operator']) {
  r = await post('/api/enquiries', { kind, name: 'T', email: 't@example.com', detail: 'x' });
  eq(`enquiry ${kind}`, r.ok, true);
}
// invalid input paths
r = await post('/api/estimate', { service: 'wf', qty: 0 });
eq('rejects qty 0', r.ok, false);
r = await get('/api/coverage/check?postcode=abc');
eq('rejects bad pc', r.ok, false);

console.log(failures ? `RESULT: FAIL (${failures})` : 'RESULT: PASS');
process.exit(failures ? 1 : 0);
