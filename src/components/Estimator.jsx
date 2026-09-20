import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getEstimate } from '../lib/api.js';
import { saveEstimate } from '../lib/estimatorStore.js';

const SERVICES = [
  ['wf', 'Wash & Fold', 'loads (approx. 5 kg each)'],
  ['linen', 'Blankets, Rugs & Sheets', 'items'],
  ['dc', 'Dry Cleaning', 'garments'],
  ['bulky', 'Bulky & Household', 'items'],
];
const TURN = { 'next-day': 'Standard turnaround: next day', '48h': 'Indicative turnaround: 48 h', quoted: 'Turnaround confirmed at booking' };
const money = (n) => '$' + (Number.isInteger(n) ? n : n.toFixed(2));

export default function Estimator() {
  const [service, setService] = useState('wf');
  const [qty, setQty] = useState(2);
  const [eco, setEco] = useState(false);
  const [bags, setBags] = useState(0);
  const [est, setEst] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    let live = true;
    const t = setTimeout(async () => {
      const input = { service, qty, eco, bags };
      const r = await getEstimate(input);
      if (!live) return;
      if (r.ok) { setEst(r); setErr(null); saveEstimate(input, r); }
      else { setEst(null); setErr(r.message); }
    }, 180);
    return () => { live = false; clearTimeout(t); };
  }, [service, qty, eco, bags]);

  const unit = SERVICES.find(([k]) => k === service)[2];
  return (
    <div className="card grid gap-8 !p-8 lg:grid-cols-2">
      <div className="space-y-5">
        <div>
          <label className="label" htmlFor="est-svc">Service</label>
          <select id="est-svc" className="input" value={service} onChange={(e) => setService(e.target.value)}>
            {SERVICES.map(([k, l]) => <option key={k} value={k}>{l}</option>)}
          </select>
        </div>
        <div>
          <label className="label" htmlFor="est-qty">{unit.charAt(0).toUpperCase() + unit.slice(1)}</label>
          <div className="flex items-center gap-3">
            <button type="button" aria-label="Decrease" className="btn-navy !h-11 !w-11 !p-0" onClick={() => setQty(Math.max(1, qty - 1))}>−</button>
            <output id="est-qty" className="w-10 text-center font-display text-xl font-bold text-ink">{qty}</output>
            <button type="button" aria-label="Increase" className="btn-navy !h-11 !w-11 !p-0" onClick={() => setQty(Math.min(50, qty + 1))}>+</button>
            {service === 'wf' && <span className="text-sm text-body/70">One load ≈ a full kitchen basket · ≈ 5 kg dry</span>}
          </div>
        </div>
        <label className="flex items-center gap-3 text-sm">
          <input type="checkbox" checked={eco} onChange={(e) => setEco(e.target.checked)} className="h-4 w-4 accent-[#0C265F]" />
          Eco / fragrance-free detergent (+{money(3.5)} per collection)
        </label>
        <div>
          <label className="label" htmlFor="est-bags">Linen Legends bags — optional, yours to keep ($12 each)</label>
          <select id="est-bags" className="input max-w-[120px]" value={bags} onChange={(e) => setBags(Number(e.target.value))}>
            {[0, 1, 2, 3].map((n) => <option key={n} value={n}>{n}</option>)}
          </select>
        </div>
      </div>
      <div className="flex flex-col rounded-2xl bg-navy p-6 text-white" aria-live="polite">
        {err && <p className="text-sm text-white/80">{err}</p>}
        {est && (
          <>
            <dl className="flex-1 space-y-2.5 text-sm">
              {est.lines.map((l, i) => (
                <div key={i} className="flex justify-between gap-4 text-white/85"><dt>{l.label}</dt><dd className="whitespace-nowrap">{money(l.amount)}</dd></div>
              ))}
              <div className="flex justify-between border-t border-white/15 pt-3 font-display text-2xl font-extrabold text-white">
                <dt className="self-end text-sm font-semibold text-white/60">ESTIMATED TOTAL</dt><dd>{money(est.total)}</dd>
              </div>
            </dl>
            <p className="mt-3 text-xs text-white/60">Includes GST · Collection &amp; return included · {TURN[est.turnaround]}</p>
            <Link to="/book" className="btn-primary mt-5 w-full">Request this collection</Link>
            <p className="mt-2 text-center text-[11px] text-white/50">Indicative, not a quote. Your operator confirms the price after weighing, before any work starts.</p>
          </>
        )}
      </div>
    </div>
  );
}
