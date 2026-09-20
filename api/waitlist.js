import { save } from './_lib/store.js';
import { bad, noStore, rateLimit, spamGuard } from './_lib/http.js';
export default async function handler(req, res) {
  noStore(res);
  if (req.method !== 'POST') return bad(res, 'method', 'POST only.');
  if (!rateLimit(req, res)) return;
  const { postcode, email, suburb } = req.body || {};
  if (!spamGuard(req.body)) return res.status(200).json({ ok: true, id: 'ok' });
  if (!/^\d{4}$/.test(String(postcode || ''))) return bad(res, 'bad_postcode', 'A four-digit postcode is required.');
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(email || ''))) return bad(res, 'bad_email', 'A valid email address is required.');
  const { id } = await save('waitlist', { postcode, email, suburb: suburb || null });
  return res.status(200).json({ ok: true, id });
}
