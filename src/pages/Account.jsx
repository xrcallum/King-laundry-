import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import { getBooking } from '../lib/api.js';

const SVC = { wf: 'Wash & Fold', linen: 'Blankets, Rugs & Sheets', dc: 'Dry Cleaning', bulky: 'Bulky & Household' };
const STEPS = ['awaiting-operator', 'confirmed', 'collected', 'washing', 'ready', 'delivered'];
const STEP_LABELS = {
  'awaiting-operator': 'Booked — awaiting operator',
  confirmed: 'Confirmed',
  collected: 'Collected',
  washing: 'Washing',
  ready: 'Ready',
  delivered: 'Delivered',
};
const STEP_EXPLAIN = {
  'awaiting-operator': "We've received your request. An operator will confirm your collection window shortly.",
  confirmed: 'Your operator has confirmed this booking. Collection is locked in.',
  collected: 'Your items have been collected and are on their way to be processed.',
  washing: 'Your items are being washed and cared for right now.',
  ready: 'Your order is ready and will be returned to you soon.',
  delivered: 'Your order has been delivered. Thanks for using Linen Legends.',
};
const PILL_LABEL = { ...STEP_LABELS, complete: 'Delivered', cancelled: 'Cancelled' };
const PILL_STYLE = {
  'awaiting-operator': 'bg-amber-100 text-amber-900',
  confirmed: 'bg-navy text-white',
  collected: 'bg-navy text-white',
  washing: 'bg-navy text-white',
  ready: 'bg-navy text-white',
  delivered: 'bg-green-100 text-green-900',
  complete: 'bg-green-100 text-green-900',
  cancelled: 'bg-ember/10 text-ember',
};

const money = (n) => '$' + (Number.isInteger(n) ? n : n.toFixed(2));
const fmtDate = (iso) => new Date(iso).toLocaleDateString('en-AU', { day: 'numeric', month: 'short', year: 'numeric' });
const fmtDateTime = (iso) => new Date(iso).toLocaleString('en-AU', { day: 'numeric', month: 'short', year: 'numeric', hour: 'numeric', minute: '2-digit' });

function readStoredBookings() {
  try {
    const raw = JSON.parse(localStorage.getItem('ll-bookings') || '[]');
    return Array.isArray(raw) ? raw : [];
  } catch {
    return [];
  }
}

function StatusPill({ status }) {
  const label = PILL_LABEL[status] || status;
  const cls = PILL_STYLE[status] || 'bg-line/40 text-body';
  return <span className={`rounded-full px-2.5 py-0.5 text-[11px] font-bold uppercase tracking-wide ${cls}`}>{label}</span>;
}

function EmptyState() {
  return (
    <div className="card mx-auto max-w-lg text-center">
      <p className="text-body">No bookings on this device yet.</p>
      <Link to="/book" className="btn-primary mt-5 inline-flex">Book a collection</Link>
    </div>
  );
}

function BookingCard({ id, meta, record }) {
  if (record?.state === 'loading' || !record) {
    return (
      <div className="card animate-pulse">
        <p className="font-mono text-xs text-body/50">{id}</p>
        <p className="mt-2 text-sm text-body/50">Loading…</p>
      </div>
    );
  }
  if (record.state === 'error') {
    return (
      <div className="card">
        <p className="font-mono text-xs text-body">{id}</p>
        <p className="mt-2 text-sm text-ember">Could not load — the booking service may be offline.</p>
      </div>
    );
  }
  const b = record.booking;
  return (
    <Link to={`/account?id=${encodeURIComponent(id)}`} className="card flex flex-col gap-4 transition-colors hover:border-navy-light sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="font-display font-bold text-ink">{SVC[b.service] || b.service}</p>
        <p className="mt-1 text-sm text-body">{fmtDate(b.date)} · {b.window} · {b.suburb}</p>
        <p className="mt-1 font-mono text-xs text-body/60">{id}</p>
      </div>
      <div className="flex items-center gap-3 sm:flex-col sm:items-end sm:gap-2">
        <p className="font-display text-xl font-extrabold text-ink">{money(b.estimate.total)}</p>
        <StatusPill status={b.status} />
      </div>
    </Link>
  );
}

function StatusTimeline({ id, booking }) {
  const history = booking.statusHistory || [];
  const cancelled = booking.status === 'cancelled';
  const normalized = booking.status === 'complete' ? 'delivered' : booking.status;
  const currentIdx = STEPS.indexOf(normalized);
  const findAt = (step) => history.find((h) => h.status === step || (step === 'delivered' && h.status === 'complete'))?.at;
  const cancelledAt = history.find((h) => h.status === 'cancelled')?.at;
  const reachedBeforeCancel = STEPS.filter((s) => history.some((h) => h.status === s));

  return (
    <div className="card">
      <div className="flex flex-col gap-1 border-b border-line pb-5">
        <p className="font-display text-lg font-bold text-ink">{SVC[booking.service] || booking.service}</p>
        <p className="text-sm text-body">{fmtDate(booking.date)} · {booking.window} · {booking.suburb}</p>
        <p className="font-mono text-xs text-body/60">{id}</p>
      </div>

      <div className="mt-6">
        {cancelled ? (
          <>
            {reachedBeforeCancel.map((step, i) => (
              <div key={step} className="flex gap-4">
                <div className="flex flex-col items-center">
                  <span className="mt-1.5 h-2.5 w-2.5 shrink-0 rounded-full bg-ember" />
                  {i < reachedBeforeCancel.length - 1 && <span className="w-px flex-1 bg-line" />}
                </div>
                <div className="pb-6">
                  <p className="text-sm font-medium text-ink">{STEP_LABELS[step]}</p>
                  {findAt(step) && <p className="mt-0.5 text-xs text-body/60">{fmtDateTime(findAt(step))}</p>}
                </div>
              </div>
            ))}
            <div className="flex gap-4">
              <span className="mt-1.5 h-3 w-3 shrink-0 rounded-full bg-ember ring-4 ring-ember/15" />
              <div>
                <p className="font-display text-2xl font-extrabold text-ember">Cancelled</p>
                <p className="mt-1 text-sm text-body">
                  This booking was cancelled.{cancelledAt ? ` ${fmtDateTime(cancelledAt)}` : ''}
                </p>
              </div>
            </div>
          </>
        ) : (
          STEPS.map((step, i) => {
            const isPast = i < currentIdx;
            const isCurrent = i === currentIdx;
            const isFuture = i > currentIdx;
            const at = isFuture ? undefined : findAt(step);
            return (
              <div key={step} className="flex gap-4">
                <div className="flex flex-col items-center">
                  <span className={`mt-1.5 shrink-0 rounded-full ${isCurrent ? 'h-3 w-3 bg-ember ring-4 ring-ember/15' : isPast ? 'h-2.5 w-2.5 bg-ember' : 'h-2.5 w-2.5 bg-line'}`} />
                  {i < STEPS.length - 1 && <span className="w-px flex-1 bg-line" />}
                </div>
                <div className={isCurrent ? 'pb-8' : 'pb-6'}>
                  {isCurrent ? (
                    <>
                      <p className="font-display text-2xl font-extrabold text-ink">{STEP_LABELS[step]}</p>
                      <p className="mt-1 text-sm text-body">{STEP_EXPLAIN[step]}</p>
                      {at && <p className="mt-1 text-xs text-body/60">{fmtDateTime(at)}</p>}
                    </>
                  ) : (
                    <>
                      <p className={`text-sm font-medium ${isPast ? 'text-ink' : 'text-body/50'}`}>{STEP_LABELS[step]}</p>
                      {isPast && at && <p className="mt-0.5 text-xs text-body/60">{fmtDateTime(at)}</p>}
                    </>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>

      <div className="mt-2 card !bg-navy text-white">
        <p className="eyebrow !text-white/60">Your estimate</p>
        <dl className="mt-4 space-y-2.5 text-sm">
          {booking.estimate.lines.map((l, i) => (
            <div key={i} className="flex justify-between gap-4 text-white/85"><dt>{l.label}</dt><dd className="whitespace-nowrap">{money(l.amount)}</dd></div>
          ))}
          <div className="flex justify-between border-t border-white/15 pt-3 font-display text-2xl font-extrabold">
            <dt className="self-end text-xs font-semibold text-white/60">TOTAL</dt><dd>{money(booking.estimate.total)}</dd>
          </div>
        </dl>
      </div>

      <p className="mt-5 text-sm text-body">
        This timeline updates when your operator updates your job. It is not live GPS tracking.
      </p>

      <Link to="/account" className="btn-navy mt-6 inline-flex">Back to your bookings</Link>
    </div>
  );
}

export default function Account() {
  const [searchParams] = useSearchParams();
  const [stored, setStored] = useState([]);
  const [records, setRecords] = useState({});

  useEffect(() => {
    setStored(readStoredBookings());
  }, []);

  useEffect(() => {
    if (!stored.length) return;
    let live = true;
    setRecords((prev) => {
      const next = { ...prev };
      stored.forEach((s) => { if (!next[s.id]) next[s.id] = { state: 'loading' }; });
      return next;
    });
    Promise.all(
      stored.map((s) =>
        getBooking(s.id)
          .then((r) => ({ id: s.id, r }))
          .catch(() => ({ id: s.id, r: { ok: false } }))
      )
    ).then((results) => {
      if (!live) return;
      setRecords((prev) => {
        const next = { ...prev };
        results.forEach(({ id, r }) => {
          next[id] = r.ok ? { state: 'ok', booking: r.booking } : { state: 'error' };
        });
        return next;
      });
    });
    return () => { live = false; };
  }, [stored]);

  const selectedId = searchParams.get('id');

  if (stored.length === 0) {
    return (
      <Section eyebrow="Home / My account" title="My bookings" lead="Every collection you've requested from this device.">
        <Reveal><EmptyState /></Reveal>
      </Section>
    );
  }

  if (selectedId) {
    const record = records[selectedId];
    return (
      <Section eyebrow="Home / My account" title="Booking status">
        <Reveal className="mx-auto max-w-2xl">
          {!record || record.state === 'loading' ? (
            <div className="card">
              <p className="text-body">Loading your booking…</p>
            </div>
          ) : record.state === 'error' ? (
            <div className="card">
              <p className="text-ember">Could not load — the booking service may be offline.</p>
              <Link to="/account" className="btn-navy mt-5 inline-flex">Back to your bookings</Link>
            </div>
          ) : (
            <StatusTimeline id={selectedId} booking={record.booking} />
          )}
        </Reveal>
      </Section>
    );
  }

  return (
    <Section eyebrow="Home / My account" title="My bookings" lead="Every collection you've requested from this device.">
      <div className="grid gap-4">
        {stored.map((s) => (
          <Reveal key={s.id}><BookingCard id={s.id} meta={s} record={records[s.id]} /></Reveal>
        ))}
      </div>
    </Section>
  );
}
