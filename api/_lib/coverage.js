/* API coverage check. The postcode maps live in src/data/coverageData.js — one
   source shared with the client (importing api/ from the client 404s because
   the Vite proxy shadows the /api path). */
export { LIVE_PC, SOON_PC } from '../../src/data/coverageData.js';
import { LIVE_PC, SOON_PC } from '../../src/data/coverageData.js';

export function check(postcode) {
  const pc = String(postcode || '').trim();
  if (!/^\d{4}$/.test(pc)) return { ok: false, error: 'bad_postcode', message: 'Please enter a valid four-digit Australian postcode.' };
  if (LIVE_PC[pc]) return { ok: true, postcode: pc, status: 'active', suburb: LIVE_PC[pc], message: `We are running collections in ${LIVE_PC[pc]} (${pc}).` };
  if (SOON_PC[pc]) return { ok: true, postcode: pc, status: 'opening', suburb: SOON_PC[pc], message: `${SOON_PC[pc]} (${pc}) is next on our list — we are recruiting an operator for that round now.` };
  return { ok: true, postcode: pc, status: 'waitlist', message: `We are not in ${pc} yet. Register your interest — we open new rounds where registered demand is highest.` };
}
