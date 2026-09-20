export const bad = (res, error, message) => res.status(400).json({ ok: false, error, message });
export const noStore = (res) => res.setHeader('Cache-Control', 'no-store');
export const spamGuard = (body) => body && typeof body === 'object' && !body.website; // honeypot field
const seen = new Map();
export function rateLimit(req, res) {
  const ip = req.headers['x-forwarded-for'] || req.socket?.remoteAddress || 'x';
  const now = Date.now();
  const hits = (seen.get(ip) || []).filter((t) => now - t < 60_000);
  hits.push(now); seen.set(ip, hits);
  if (hits.length > 20) { res.status(429).json({ ok: false, error: 'rate_limited', message: 'Too many requests. Try again in a minute.' }); return false; }
  return true;
}
