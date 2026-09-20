import { useState } from 'react';
import { Link } from 'react-router-dom';
import { checkCoverage, joinWaitlist } from '../lib/api.js';

export default function PostcodeChecker() {
  const [pc, setPc] = useState('');
  const [res, setRes] = useState(null);
  const [email, setEmail] = useState('');
  const [joined, setJoined] = useState(null);

  const check = async (e) => {
    e?.preventDefault();
    setJoined(null);
    setRes(await checkCoverage(pc));
  };
  const join = async (e) => {
    e.preventDefault();
    const r = await joinWaitlist({ postcode: pc, email });
    setJoined(r.ok ? 'Registered. We open new rounds where demand is highest — we will email you before we launch near you.' : r.message);
  };

  const tone = res?.status === 'active' ? 'border-green-600/40 bg-green-50 text-green-900'
    : res?.status === 'opening' ? 'border-amber-500/40 bg-amber-50 text-amber-900'
    : 'border-line bg-paper text-ink';

  return (
    <div className="mx-auto max-w-xl">
      <form onSubmit={check} className="flex gap-3">
        <input
          className="input text-center font-display text-lg font-bold tracking-[0.2em]"
          value={pc} onChange={(e) => setPc(e.target.value.replace(/\D/g, '').slice(0, 4))}
          inputMode="numeric" maxLength={4} placeholder="4131" aria-label="Postcode"
        />
        <button type="submit" className="btn-primary shrink-0">Check</button>
      </form>
      {res && (
        <div className={`mt-4 rounded-xl border p-4 text-sm leading-relaxed ${tone}`} role="status">
          <p>{res.message}{res.status === 'active' && <> <Link className="font-semibold underline" to="/book">Get a quote and book a collection.</Link></>}</p>
          {(res.status === 'waitlist' || res.status === 'opening') && !joined && (
            <form onSubmit={join} className="mt-3 flex gap-2">
              <input className="input !py-2.5" type="email" required placeholder="you@email.com" aria-label="Email for waitlist"
                value={email} onChange={(e) => setEmail(e.target.value)} />
              <button type="submit" className="btn-navy shrink-0 !py-2.5">Register</button>
            </form>
          )}
          {joined && <p className="mt-2 font-medium">{joined}</p>}
        </div>
      )}
    </div>
  );
}
