import { estimate } from './_lib/pricing.js';
import { save, find } from './_lib/store.js';
import { REF } from './_lib/ref.js';
import { bad, noStore, rateLimit, spamGuard } from './_lib/http.js';

export default async function handler(req, res) {
  noStore(res);
  if (req.method === 'GET') {
    const b = find('bookings', req.query?.id);
    return b ? res.status(200).json({ ok: true, booking: b }) : res.status(404).json({ ok: false, error: 'not_found', message: 'No booking with that reference.' });
  }
  if (req.method !== 'POST') return bad(res, 'method', 'POST or GET only.');
  if (!rateLimit(req, res)) return;
  const b = req.body || {};
  if (!spamGuard(b)) return res.status(200).json({ ok: true, id: REF() });
  for (const f of ['service', 'qty', 'name', 'phone', 'email', 'address', 'suburb', 'postcode', 'date', 'window']) {
    if (!b[f]) return bad(res, 'missing_field', `Missing required field: ${f}.`);
  }
  if (b.consent !== true) return bad(res, 'consent', 'Consent to be contacted about this booking is required.');
  const est = estimate({ service: b.service, qty: b.qty, eco: b.eco, bags: b.bags });
  if (!est.ok) return res.status(400).json(est);
  const id = REF();
  const status = 'awaiting-operator';
  await save('bookings', {
    id, status, statusHistory: [{ status, at: new Date().toISOString() }],
    service: b.service, qty: Number(b.qty), eco: !!b.eco, bags: Number(b.bags) || 0,
    name: b.name, phone: b.phone, email: b.email, address: b.address,
    suburb: b.suburb, postcode: b.postcode, date: b.date, window: b.window,
    notes: b.notes || null, estimate: est,
  });
  return res.status(200).json({ ok: true, id, estimate: est, status });
}
