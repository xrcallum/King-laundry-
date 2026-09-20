import { useEffect, useState } from 'react';
import { createBooking, getEstimate } from '../lib/api.js';
import { loadEstimate } from '../lib/estimatorStore.js';
import { WINDOWS, POSTCODE_PATTERN, PHONE_PATTERN } from '../lib/bookingOptions.js';
import SuccessCard from './SuccessCard.jsx';

const SVC = { wf: 'Wash & Fold', linen: 'Blankets, Rugs & Sheets', dc: 'Dry Cleaning', bulky: 'Bulky & Household' };
const money = (n) => '$' + (Number.isInteger(n) ? n : n.toFixed(2));
const minDate = () => { const d = new Date(Date.now() + 86400000); return d.toISOString().slice(0, 10); };

export default function BookingForm() {
  const pre = loadEstimate();
  const [b, setB] = useState({
    service: pre?.input?.service || 'wf', qty: pre?.input?.qty || 2, eco: !!pre?.input?.eco, bags: pre?.input?.bags || 0,
    name: '', phone: '', email: '', address: '', suburb: '', postcode: '', date: minDate(), window: WINDOWS[0], notes: '', consent: false, website: '',
  });
  const [est, setEst] = useState(pre?.result || null);
  const [result, setResult] = useState(null);
  const [err, setErr] = useState(null);
  const set = (k) => (e) => setB({ ...b, [k]: e.target.type === 'checkbox' ? e.target.checked : e.target.value });

  useEffect(() => {
    let live = true;
    getEstimate({ service: b.service, qty: Number(b.qty), eco: b.eco, bags: Number(b.bags) }).then((r) => { if (live && r.ok) setEst(r); });
    return () => { live = false; };
  }, [b.service, b.qty, b.eco, b.bags]);

  const submit = async (e) => {
    e.preventDefault();
    setErr(null);
    const r = await createBooking({ ...b, qty: Number(b.qty), bags: Number(b.bags) });
    if (r.ok) {
      setResult(r);
      try {
        const mine = JSON.parse(localStorage.getItem('ll-bookings') || '[]');
        mine.unshift({ id: r.id, date: b.date, service: b.service, at: new Date().toISOString() });
        localStorage.setItem('ll-bookings', JSON.stringify(mine.slice(0, 20)));
      } catch { /* private mode */ }
    } else setErr(r.message);
  };

  if (result) return (
    <SuccessCard className="mx-auto max-w-xl">
      <p className="eyebrow !text-green-700">Booking request received</p>
      <p className="mt-2 font-display text-3xl font-extrabold text-green-900">{result.id}</p>
      <p className="mt-2 text-sm text-green-900/80">Keep this reference. An operator will confirm your window. Estimated total {money(result.estimate.total)}, GST included — your exact price is confirmed after weighing, before any work starts.</p>
    </SuccessCard>
  );

  return (
    <form onSubmit={submit} className="grid gap-8 lg:grid-cols-[1fr_360px]">
      <div className="card grid gap-4 sm:grid-cols-2">
        <input type="text" name="website" value={b.website} onChange={set('website')} className="hidden" tabIndex={-1} autoComplete="off" aria-hidden="true" />
        <div><label className="label" htmlFor="bk-svc">Service</label>
          <select id="bk-svc" className="input" value={b.service} onChange={set('service')}>{Object.entries(SVC).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select></div>
        <div><label className="label" htmlFor="bk-qty">Quantity</label><input id="bk-qty" className="input" type="number" min="1" max="50" required value={b.qty} onChange={set('qty')} /></div>
        <div><label className="label" htmlFor="bk-name">Full name</label><input id="bk-name" className="input" required value={b.name} onChange={set('name')} autoComplete="name" /></div>
        <div><label className="label" htmlFor="bk-phone">Phone</label><input id="bk-phone" className="input" type="tel" required pattern={PHONE_PATTERN} title="Enter a valid phone number." value={b.phone} onChange={set('phone')} autoComplete="tel" /></div>
        <div className="sm:col-span-2"><label className="label" htmlFor="bk-email">Email</label><input id="bk-email" className="input" type="email" required value={b.email} onChange={set('email')} autoComplete="email" /></div>
        <div className="sm:col-span-2"><label className="label" htmlFor="bk-addr">Collection address</label><input id="bk-addr" className="input" required value={b.address} onChange={set('address')} autoComplete="street-address" /></div>
        <div><label className="label" htmlFor="bk-sub">Suburb</label><input id="bk-sub" className="input" required value={b.suburb} onChange={set('suburb')} /></div>
        <div><label className="label" htmlFor="bk-pc">Postcode</label><input id="bk-pc" className="input" required inputMode="numeric" maxLength={4} pattern={POSTCODE_PATTERN} title="Enter a four-digit postcode." value={b.postcode} onChange={(e) => setB({ ...b, postcode: e.target.value.replace(/\D/g, '').slice(0, 4) })} /></div>
        <div><label className="label" htmlFor="bk-date">Collection day</label><input id="bk-date" className="input" type="date" min={minDate()} required value={b.date} onChange={set('date')} /></div>
        <div><label className="label" htmlFor="bk-win">Window</label>
          <select id="bk-win" className="input" value={b.window} onChange={set('window')}>{WINDOWS.map((w) => <option key={w}>{w}</option>)}</select></div>
        <div className="sm:col-span-2"><label className="label" htmlFor="bk-notes">Care notes — cold wash, hang dry, folded flat…</label><textarea id="bk-notes" className="input min-h-20" value={b.notes} onChange={set('notes')} /></div>
        <label className="flex items-start gap-3 text-sm sm:col-span-2">
          <input type="checkbox" required checked={b.consent} onChange={set('consent')} className="mt-0.5 h-4 w-4 accent-[#0C265F]" />
          <span>I agree to be contacted about this booking. Pre-launch: this is a registration of interest — the privacy policy and terms are drafts for legal review and not yet in force.</span>
        </label>
        {err && <p className="text-sm text-ember sm:col-span-2" role="alert">{err}</p>}
        <button type="submit" className="btn-primary sm:col-span-2">Request this collection</button>
      </div>
      <aside className="card h-fit !bg-navy text-white lg:sticky lg:top-24" aria-live="polite">
        <p className="eyebrow !text-white/60">Your estimate</p>
        {est && (
          <dl className="mt-4 space-y-2.5 text-sm">
            {est.lines.map((l, i) => <div key={i} className="flex justify-between gap-4 text-white/85"><dt>{l.label}</dt><dd className="whitespace-nowrap">{money(l.amount)}</dd></div>)}
            <div className="flex justify-between border-t border-white/15 pt-3 font-display text-2xl font-extrabold"><dt className="self-end text-xs font-semibold text-white/60">TOTAL</dt><dd>{money(est.total)}</dd></div>
          </dl>
        )}
        <p className="mt-3 text-xs text-white/55">Includes GST. Minimum order applies. Payment is taken after weighing, before return delivery.</p>
      </aside>
    </form>
  );
}
