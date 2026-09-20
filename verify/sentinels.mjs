/* Compliance sentinel gate (README rule, ported): the built site must carry every
   sentinel and must not carry forbidden strings. Run against dist/ after build. */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const files = [], srcFiles = [];
const walk = (d, out, ext) => { for (const f of readdirSync(d, { withFileTypes: true })) {
  const p = join(d, f.name);
  if (f.isDirectory()) walk(p, out, ext);
  else if (ext.test(f.name)) out.push(p);
} };
walk('dist', files, /\.(html|js)$/);
walk('src', srcFiles, /\.(jsx|js|css)$/);
const body = files.map((f) => readFileSync(f, 'utf8')).join('\n');
/* Emoji check runs over OUR source + built HTML only — vendor bundles carry their own
   internal strings (e.g. react-router's dev warning) that are not page content. */
const ours = srcFiles.map((f) => readFileSync(f, 'utf8')).join('\n') + readFileSync('dist/index.html', 'utf8');

const MUST = [
  ['GST statement', 'All prices include GST and are in AUD'],
  ['ABN published', 'ABN 12 482 409 883'],
  ['Entity name pending flag', 'Registered entity name to be published'],
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
  const hay = name === 'Emoji' ? ours : body;
  const hit = typeof s === 'string' ? hay.includes(s) : s.test(hay);
  console.log(`${hit ? 'FAIL' : 'PASS'}  must-not: ${name}`);
  if (hit) fail++;
}
console.log(fail ? `RESULT: FAIL (${fail})` : 'RESULT: PASS');
process.exit(fail ? 1 : 0);
