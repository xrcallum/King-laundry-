import { save } from './_lib/store.js';
import { bad, noStore, rateLimit, spamGuard } from './_lib/http.js';
export default async function handler(req, res) {
  noStore(res);
  if (req.method !== 'POST') return bad(res, 'method', 'POST only.');
  if (!rateLimit(req, res)) return;
  const b = req.body || {};
  if (!spamGuard(b)) return res.status(200).json({ ok: true, id: 'ok' });
  if (!b.name || !b.email || !b.message) return bad(res, 'missing_field', 'Name, email and message are required.');
  const { id } = await save('contact', { ...b, complaint: !!b.complaint, escalated: !!b.complaint });
  return res.status(200).json({ ok: true, id });
}
