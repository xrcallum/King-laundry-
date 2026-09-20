import { useState } from 'react';
import { sendEnquiry } from '../lib/api.js';
import SuccessCard from './SuccessCard.jsx';

const FIELDS = {
  business: { org: 'Business name', detail: 'Estimated volume & frequency — e.g. 4 properties, approx. 6 changeovers per week' },
  'supported-living': { org: 'Organisation (if applicable)', detail: 'Frequency, volume, and anything we should know about handling requirements' },
  operator: { org: 'Suburb you would operate from', detail: 'Hours per week you would like, and anything about your setup' },
};

export default function EnquiryForm({ kind }) {
  const f = FIELDS[kind];
  const [state, setState] = useState({ name: '', email: '', phone: '', org: '', detail: '', website: '' });
  const [done, setDone] = useState(null);
  const [err, setErr] = useState(null);
  const set = (k) => (e) => setState({ ...state, [k]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    const r = await sendEnquiry({ kind, ...state });
    if (r.ok) setDone(r.id); else setErr(r.message);
  };

  if (done) return (
    <SuccessCard>
      <p className="font-display font-bold text-green-900">Enquiry received — reference {done}.</p>
      <p className="mt-1 text-sm text-green-900/80">We answer every enquiry, same business day where we can.{kind === 'operator' && ' Submitting this form is an expression of interest only — it does not create any contract or obligation on either side.'}</p>
    </SuccessCard>
  );
  return (
    <form onSubmit={submit} className="card grid gap-4 sm:grid-cols-2">
      <input type="text" name="website" value={state.website} onChange={set('website')} className="hidden" tabIndex={-1} autoComplete="off" aria-hidden="true" />
      <div><label className="label" htmlFor={`${kind}-name`}>Your name</label><input id={`${kind}-name`} className="input" required value={state.name} onChange={set('name')} /></div>
      <div><label className="label" htmlFor={`${kind}-email`}>Email</label><input id={`${kind}-email`} className="input" type="email" required value={state.email} onChange={set('email')} /></div>
      <div><label className="label" htmlFor={`${kind}-phone`}>Phone</label><input id={`${kind}-phone`} className="input" type="tel" value={state.phone} onChange={set('phone')} /></div>
      <div><label className="label" htmlFor={`${kind}-org`}>{f.org}</label><input id={`${kind}-org`} className="input" value={state.org} onChange={set('org')} /></div>
      <div className="sm:col-span-2"><label className="label" htmlFor={`${kind}-detail`}>{f.detail}</label><textarea id={`${kind}-detail`} className="input min-h-28" value={state.detail} onChange={set('detail')} /></div>
      {err && <p className="text-sm text-ember sm:col-span-2" role="alert">{err}</p>}
      <button type="submit" className="btn-primary sm:col-span-2">{kind === 'operator' ? 'Register my interest' : 'Request a quote'}</button>
    </form>
  );
}
