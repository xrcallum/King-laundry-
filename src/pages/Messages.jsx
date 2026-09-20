import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import { getBooking } from '../lib/api.js';

const MSG_TEXT = {
  'awaiting-operator': 'Booked, awaiting an operator',
  confirmed: 'Confirmed by your operator',
  collected: 'Collected',
  washing: 'Washing has started',
  ready: 'Ready for delivery',
  delivered: 'Delivered',
  complete: 'Delivered',
  cancelled: 'Cancelled',
};

function readStoredBookings() {
  try {
    const raw = JSON.parse(localStorage.getItem('ll-bookings') || '[]');
    return Array.isArray(raw) ? raw : [];
  } catch {
    return [];
  }
}

function relTime(iso) {
  const diffMs = Date.now() - new Date(iso).getTime();
  const min = Math.round(diffMs / 60000);
  if (min < 1) return 'Just now';
  if (min < 60) return `${min} minute${min === 1 ? '' : 's'} ago`;
  const hr = Math.round(min / 60);
  if (hr < 24) return `${hr} hour${hr === 1 ? '' : 's'} ago`;
  const day = Math.round(hr / 24);
  if (day === 1) return 'Yesterday';
  if (day < 7) return `${day} days ago`;
  return new Date(iso).toLocaleDateString('en-AU', { day: 'numeric', month: 'short', year: 'numeric' });
}

function EmptyState() {
  return (
    <div className="card mx-auto max-w-lg text-center">
      <p className="text-body">No bookings on this device yet.</p>
      <Link to="/book" className="btn-primary mt-5 inline-flex">Book a collection</Link>
    </div>
  );
}

export default function Messages() {
  const [stored, setStored] = useState([]);
  const [loading, setLoading] = useState(true);
  const [events, setEvents] = useState([]);
  const [erroredCount, setErroredCount] = useState(0);

  useEffect(() => {
    setStored(readStoredBookings());
  }, []);

  useEffect(() => {
    if (!stored.length) { setLoading(false); return; }
    let live = true;
    setLoading(true);
    Promise.all(
      stored.map((s) =>
        getBooking(s.id)
          .then((r) => ({ id: s.id, r }))
          .catch(() => ({ id: s.id, r: { ok: false } }))
      )
    ).then((results) => {
      if (!live) return;
      let errors = 0;
      const items = [];
      results.forEach(({ id, r }) => {
        if (!r.ok) { errors += 1; return; }
        (r.booking.statusHistory || []).forEach((h) => {
          items.push({ id, status: h.status, at: h.at });
        });
      });
      items.sort((a, b) => new Date(b.at) - new Date(a.at));
      setEvents(items);
      setErroredCount(errors);
      setLoading(false);
    });
    return () => { live = false; };
  }, [stored]);

  if (stored.length === 0) {
    return (
      <Section eyebrow="Home / Messages" title="Messages" lead="Updates about your collections.">
        <Reveal><EmptyState /></Reveal>
      </Section>
    );
  }

  return (
    <Section eyebrow="Home / Messages" title="Messages" lead="Updates about your collections.">
      <div className="mx-auto grid max-w-2xl gap-4">
        <Reveal>
          <div className="card !bg-navy text-white">
            <p className="eyebrow !text-white/60">How this works</p>
            <p className="mt-2 text-sm leading-relaxed text-white/85">
              Notifications about your collections will appear here as your operator updates each job. Once our
              messaging system is live you will get a notification when your operator is on the way. SMS and push
              notifications are not switched on yet.
            </p>
            {erroredCount > 0 && (
              <p className="mt-3 text-xs text-white/60">
                {erroredCount} booking{erroredCount === 1 ? '' : 's'} could not be checked for updates — the messaging service may be offline.
              </p>
            )}
          </div>
        </Reveal>

        {loading ? (
          <div className="card"><p className="text-body">Checking for updates…</p></div>
        ) : events.length === 0 ? (
          <div className="card"><p className="text-body">No updates yet.</p></div>
        ) : (
          events.map((e, i) => (
            <Reveal key={`${e.id}-${e.status}-${e.at}-${i}`} delay={Math.min(i * 40, 200)}>
              <div className="card flex items-center justify-between gap-4">
                <p className="text-sm text-ink">
                  <span className="font-mono text-xs text-body/60">{e.id}</span>
                  {' — '}
                  {MSG_TEXT[e.status] || e.status}
                </p>
                <p className="shrink-0 text-xs text-body/60">{relTime(e.at)}</p>
              </div>
            </Reveal>
          ))
        )}
      </div>
    </Section>
  );
}
