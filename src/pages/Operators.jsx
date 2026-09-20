import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import EnquiryForm from '../components/EnquiryForm.jsx';

const OFFER = [
  'Your own ABN, your own business, your own hours',
  'Your own washing and drying equipment',
  'Jobs routed to you by suburb — no advertising or cold calling',
  'Booking, scheduling, invoicing and payment handled by our platform',
  'Onboarding, training and ongoing support provided',
  'No franchise purchase price and no territory buy-in',
];

const REQUIREMENTS = [
  'An active ABN, or willingness to register one',
  'A reliable washing machine and dryer, and space to work',
  'A vehicle for collections and returns',
  'Willingness to complete identity and background screening',
  'Appropriate insurance — we will tell you exactly which policies before you start',
  'A smartphone for the operator app',
];

export default function Operators() {
  return (
    <>
      <Section eyebrow="Home / Become an Operator" title="Become a Linen Legends operator"
        lead="Run laundry collections in your own suburb, as your own business, with our customers, brand and systems behind you.">
        <Reveal className="max-w-3xl">
          <p className="eyebrow mb-2">What the arrangement is</p>
          <p className="leading-relaxed">You operate as an independent business with your own ABN. You use your own equipment and premises, choose your own hours, and decide how much work you take on. We route customers to you, handle the booking platform, brand and customer support, and pay you on an agreed revenue share.</p>
        </Reveal>

        <div className="mt-10 grid gap-8 lg:grid-cols-2">
          <Reveal>
            <h3 className="font-display text-lg font-bold">What we offer</h3>
            <ul className="mt-3 space-y-2 text-sm leading-relaxed">
              {OFFER.map((o) => <li key={o} className="flex gap-2"><span aria-hidden="true" className="text-ember">•</span><span>{o}</span></li>)}
            </ul>
          </Reveal>
          <Reveal delay={90}>
            <h3 className="font-display text-lg font-bold">What you need</h3>
            <ul className="mt-3 space-y-2 text-sm leading-relaxed">
              {REQUIREMENTS.map((r) => <li key={r} className="flex gap-2"><span aria-hidden="true" className="text-ember">•</span><span>{r}</span></li>)}
            </ul>
          </Reveal>
        </div>
      </Section>

      <Section className="!bg-paper">
        <Reveal className="mx-auto max-w-3xl">
          <div className="card !border-ember/40 !bg-paper">
            <h3 className="font-display text-lg font-bold text-ink">Before you apply, read this.</h3>
            <p className="mt-2 leading-relaxed">This is an independent contracting arrangement, not employment. That has real consequences for your tax, superannuation and entitlements, and whether it is the correct classification depends on how the work is actually performed. We will give you the full written agreement to review before you commit, and we recommend you take independent advice on it. We will not pretend this is a decision to make casually.</p>
          </div>
        </Reveal>
      </Section>

      <Section eyebrow="Before you register" title="What we cannot tell you yet">
        <Reveal className="max-w-3xl">
          <div className="card !border-ember/40 !bg-paper">
            <h3 className="font-display text-lg font-bold text-ink">Earnings figures</h3>
            <p className="mt-2 leading-relaxed">We are not publishing income claims. We have not been operating long enough to have real operator earnings data, and quoting a range we cannot evidence would be misleading. Once we have genuine figures from active operators, they will be published here with the basis they were calculated on.</p>
            <p className="mt-4 leading-relaxed">What we can tell you is the revenue share percentage, the expected job volume in your suburb, and the current booking rate. We will give you all three in writing during the application conversation.</p>
          </div>
        </Reveal>
      </Section>

      <Section dark eyebrow="Apply" title="Register your interest"
        lead="We will be in touch to talk through the arrangement, answer your questions, and send you the agreement to review.">
        <Reveal><EnquiryForm kind="operator" /></Reveal>
        <Reveal delay={80}>
          <p className="mt-6 max-w-2xl text-sm text-white/70">Submitting this form is an expression of interest only. It does not create any contract or obligation on either side.</p>
        </Reveal>
      </Section>
    </>
  );
}
