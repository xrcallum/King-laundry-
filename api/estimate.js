import { estimate } from './_lib/pricing.js';
import { bad, noStore, rateLimit } from './_lib/http.js';
export default function handler(req, res) {
  noStore(res);
  if (req.method !== 'POST') return bad(res, 'method', 'POST only.');
  if (!rateLimit(req, res)) return;
  const out = estimate(req.body || {});
  return out.ok ? res.status(200).json(out) : res.status(400).json(out);
}
