/* Pricing of record — lifted verbatim from site/laundrylegends-site.html DEFAULT_PRICING.
   Launch pricing, under review (Max Jones sign-off pending). GST-inclusive AUD.
   This module is the ONLY place price arithmetic happens. */
export const PRICING = {
  load: 32.0, premium: 15.0, bag: 12.0, delivery: 13.5,
  minimum: 73.5, // Laundry Lady $70 min +5% — decision 18 Sep 2026
  dcJacket: 18.5, dcDress: 16.5, dcSuit: 32.0,
  bulkDoona: 45.0, bulkDoonaKing: 75.0, bulkCurtain: 38.0,
  linenSheetSet: 24.0, linenBlanket: 32.0, linenRug: 42.0,
  ecoAddon: 3.5,
  plan1: 63.7, plan2: 89.7, plan3: 115.7,
};

const round2 = (n) => Math.round(n * 100) / 100;

export const SERVICES = {
  wf:    { label: 'Wash & Fold',              unit: 'load',    rate: PRICING.load,        turnaround: 'next-day' },
  linen: { label: 'Blankets, Rugs & Sheets',  unit: 'item',    rate: PRICING.linenBlanket, turnaround: '48h' }, // D2(a): indicative
  dc:    { label: 'Dry Cleaning',             unit: 'garment', rate: PRICING.dcDress,     turnaround: 'quoted' },
  bulky: { label: 'Bulky & Household',        unit: 'item',    rate: PRICING.bulkDoona,   turnaround: 'quoted' },
};

export function estimate({ service, qty, eco = false, bags = 0 }) {
  const svc = SERVICES[service];
  if (!svc) return { ok: false, error: 'bad_service', message: 'Unknown service. Use wf, linen, dc or bulky.' };
  const q = Number(qty);
  if (!Number.isInteger(q) || q < 1 || q > 50) return { ok: false, error: 'bad_qty', message: 'Quantity must be a whole number from 1 to 50.' };

  const lines = [];
  let subtotal = 0;
  const base = round2(q * svc.rate);
  lines.push({ label: `${q} × ${svc.label.toLowerCase()} ${svc.unit}${q > 1 ? 's' : ''}`, amount: base });
  subtotal += base;
  if (eco) { lines.push({ label: 'Eco / fragrance-free detergent', amount: PRICING.ecoAddon }); subtotal += PRICING.ecoAddon; }
  const nb = Number(bags) || 0;
  if (nb > 0) { const v = round2(nb * PRICING.bag); lines.push({ label: `${nb} × Linen Legends bag${nb > 1 ? 's' : ''} (yours to keep)`, amount: v }); subtotal += v; }
  lines.push({ label: 'Collection & return', amount: PRICING.delivery });
  subtotal = round2(subtotal + PRICING.delivery);

  const total = Math.max(PRICING.minimum, subtotal);
  const minimumApplied = total > subtotal + 0.001;
  if (minimumApplied) lines.push({ label: 'Minimum order adjustment', amount: round2(total - subtotal) });

  return {
    ok: true, lines, subtotal, delivery: PRICING.delivery,
    minimumApplied, total: round2(total),
    turnaround: svc.turnaround, gstIncluded: true, indicative: true,
  };
}
