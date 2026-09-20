import { save } from './_lib/store.js';
import { bad, noStore, rateLimit, spamGuard } from './_lib/http.js';
const KINDS = ['business', 'supported-living', 'operator'];
export default async function handler(req, res) {
  noStore(res);
  if (req.method !== 'POST') return bad(res, 'method', 'POST only.');
  if (!rateLimit(req, res)) return;
  const b = req.body || {};
  if (!spamGuard(b)) return res.status(200).json({ ok: true, id: 'ok' });
  if (!KINDS.includes(b.kind)) return bad(res, 'bad_kind', `kind must be one of: ${KINDS.join(', ')}.`);
  if (!b.name || !b.email) return bad(res, 'missing_field', 'Name and email are required.');
  const { id } = await save('enquiries', b);
  return res.status(200).json({ ok: true, id });
}
