import { check } from '../_lib/coverage.js';
import { noStore } from '../_lib/http.js';
export default function handler(req, res) {
  noStore(res);
  const out = check(req.query?.postcode);
  return out.ok ? res.status(200).json(out) : res.status(400).json(out);
}
