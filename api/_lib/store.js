/* Persistence: Ops Sheet webhook when OPS_SHEET_WEBHOOK is set (the Data Spine),
   git-ignored local JSON otherwise (dev fallback only — D6 still open). */
import { mkdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { REF } from './ref.js';

export async function save(collection, record) {
  const id = record.id || REF();
  const row = { ...record, id, collection, createdAt: new Date().toISOString() };
  const hook = process.env.OPS_SHEET_WEBHOOK;
  if (hook) {
    const r = await fetch(hook, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(row) });
    if (!r.ok) throw new Error(`Ops Sheet webhook returned ${r.status}`);
    return { id, stored: 'ops-sheet' };
  }
  mkdirSync('data', { recursive: true });
  const file = `data/${collection}.json`;
  const rows = existsSync(file) ? JSON.parse(readFileSync(file, 'utf8')) : [];
  rows.push(row);
  writeFileSync(file, JSON.stringify(rows, null, 2));
  return { id, stored: 'dev-json' };
}

export function find(collection, id) {
  const file = `data/${collection}.json`;
  if (!existsSync(file)) return null;
  return JSON.parse(readFileSync(file, 'utf8')).find((r) => r.id === id) || null;
}
