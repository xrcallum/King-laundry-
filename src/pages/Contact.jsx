import { useState } from 'react';
import { Link } from 'react-router-dom';
import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import { sendContact } from '../lib/api.js';

const TOPICS = ['Question', 'Quote', 'Complaint', 'Something else'];

function ContactForm() {
  const [state, setState] = useState({
    name: '', email: '', phone: '', topic: 'Question', message: '', complaint: false, website: '',
  });
  const [result, setResult] = useState(null);
  const [err, setErr] = useState(null);
  const set = (k) => (e) => setState({ ...state, [k]: e.target.type === 'checkbox' ? e.target.checked : e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setErr(null);
    const r = await sendContact(state);
    if (r.ok) setResult(r); else setErr(r.message || 'Something went wrong. Please try again.');
  };

  if (result) {
    return (
      <div className="card border-green-600/30 bg-green-50" role="status">
        <p className="font-display font-bold text-green-900">Message received — reference {result.id}.</p>
        <p className="mt-1 text-sm text-green-900/80">We aim to respond the same business day.</p>
        {state.complaint && (
          <p className="mt-1 text-sm text-green-900/80">
            Complaints are escalated rather than queued — acknowledged within one business day.
          </p>
        )}
      </div>
    );
  }

  return (
    <form onSubmit={submit} className="card grid gap-4 sm:grid-cols-2">
      <input
        type="text" name="website" value={state.website} onChange={set('website')}
        className="hidden" tabIndex={-1} aria-hidden="true" autoComplete="off"
      />
      <div>
        <label className="label" htmlFor="contact-name">Name</label>
        <input id="contact-name" className="input" required value={state.name} onChange={set('name')} />
      </div>
      <div>
        <label className="label" htmlFor="contact-email">Email</label>
        <input id="contact-email" className="input" type="email" required value={state.email} onChange={set('email')} />
      </div>
      <div>
        <label className="label" htmlFor="contact-phone">Phone (optional)</label>
        <input id="contact-phone" className="input" type="tel" value={state.phone} onChange={set('phone')} />
      </div>
      <div>
        <label className="label" htmlFor="contact-topic">What is this about?</label>
        <select id="contact-topic" className="input" value={state.topic} onChange={set('topic')}>
          {TOPICS.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>
      <div className="sm:col-span-2">
        <label className="label" htmlFor="contact-message">Message</label>
        <textarea id="contact-message" className="input min-h-32" required value={state.message} onChange={set('message')} />
      </div>
      <label className="flex items-start gap-3 text-sm text-body sm:col-span-2">
        <input type="checkbox" className="mt-1 h-4 w-4 rounded border-line" checked={state.complaint} onChange={set('complaint')} />
        This is a complaint — escalate it
      </label>
      {err && <p className="text-sm text-ember sm:col-span-2" role="alert">{err}</p>}
      <button type="submit" className="btn-primary sm:col-span-2">Send message</button>
    </form>
  );
}

export default function Contact() {
  return (
    <Section
      eyebrow="Home / Contact"
      title="Contact us"
      lead="Questions, quotes, complaints or anything else. We answer every enquiry."
    >
      <div className="grid gap-12 lg:grid-cols-5">
        <Reveal className="lg:col-span-2 space-y-8">
          <div>
            <h3 className="font-display text-lg font-bold text-ink">Phone</h3>
            <p className="mt-2 text-[15px] leading-relaxed text-body">
              Our customer line is being connected. Until it is live, please use the form below and
              we will respond the same business day.
            </p>
          </div>
          <div>
            <h3 className="font-display text-lg font-bold text-ink">Email</h3>
            <p className="mt-2 text-[15px] leading-relaxed text-body">
              Email address to be confirmed and published here. Until then, the form below is the
              fastest way to reach us.
            </p>
          </div>
          <div>
            <h3 className="font-display text-lg font-bold text-ink">Service area</h3>
            <p className="mt-2 text-[15px] leading-relaxed text-body">
              Brisbane, Logan and South East Queensland.{' '}
              <Link to="/coverage" className="font-semibold text-navy underline underline-offset-4">
                Check your postcode on the coverage page
              </Link>.
            </p>
          </div>
          <div>
            <h3 className="font-display text-lg font-bold text-ink">Business hours</h3>
            <p className="mt-2 text-[15px] leading-relaxed text-body">
              Enquiries answered Monday to Friday. Collection windows — including evenings and
              weekends — are shown when you book.
            </p>
          </div>
          <div>
            <h3 className="font-display text-lg font-bold text-ink">Complaints</h3>
            <p className="mt-2 text-[15px] leading-relaxed text-body">
              If something has gone wrong, say so directly in the form and mark it as a complaint.
              Complaints are escalated rather than queued, and we will acknowledge within one
              business day.
            </p>
          </div>
        </Reveal>
        <Reveal className="lg:col-span-3" delay={80}>
          <ContactForm />
        </Reveal>
      </div>
    </Section>
  );
}
