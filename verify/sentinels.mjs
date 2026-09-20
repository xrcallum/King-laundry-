/* Compliance sentinel gate (README rule, ported): the built site must carry every
   sentinel and must not carry forbidden strings. Run against dist/ after build. */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const files = [];
const walk = (d) => { for (const f of readdirSync(d, { withFileTypes: true })) {
  const p = join(d, f.name);
  if (f.isDirectory()) walk(p);
  else if (/\.(html|js)$/.test(f.name)) files.push(p);
} };
walk('dist');
const body = files.map((f) => readFileSync(f, 'utf8')).join('\n');

const MUST = [
  ['GST statement', 'All prices include GST and are in AUD'],
  ['Entity placeholder', 'Company name and ABN to be published on registration'],
  ['Australian owned', 'Australian owned and operated'],
  ['NDIS statement', 'not currently a registered NDIS provider'],
  ['AS/NZS 4146 statement', 'AS/NZS 4146'],
  ['ACL not-limited statement', 'Nothing on this page limits or replaces those rights'],
  ['Contractor statement', 'independent contracting arrangement, not employment'],
  ['Draft policies flag', 'not yet in force'],
  ['Brand', 'Linen Legends'],
];
const NEVER = [
  ['Old brand', 'Laundrylegends'], ['Old brand spaced', 'LaundryKings'], ['Old club', 'Kings Club'],
  ['Old domain', 'laundrylegends.com.au'], ['Competitor', 'drycleaning.com.au'], ['Competitor phone', '1800 PICKUP'],
  ['Invented phone', /\(07\) *3\d{3} *\d{4}/], ['Emoji', /[\u{1F300}-\u{1FAFF}]/u],
];

let fail = 0;
for (const [name, s] of MUST) {
  const ok = body.includes(s);
  console.log(`${ok ? 'PASS' : 'FAIL'}  must-have: ${name}`);
  if (!ok) fail++;
}
for (const [name, s] of NEVER) {
  const hit = typeof s === 'string' ? body.includes(s) : s.test(body);
  console.log(`${hit ? 'FAIL' : 'PASS'}  must-not: ${name}`);
  if (hit) fail++;
}
console.log(fail ? `RESULT: FAIL (${fail})` : 'RESULT: PASS');
process.exit(fail ? 1 : 0);
