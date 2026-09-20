import { Link } from 'react-router-dom';
import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import site from '../data/site.js';

export default function Guarantee() {
  return (
    <Section
      eyebrow="Home / Service Guarantee"
      title="Our service guarantee"
      lead="What we promise, what we will do if we get it wrong, and the limits of both — in plain language."
    >
      <Reveal className="mx-auto max-w-3xl space-y-10 text-[17px] leading-relaxed text-body">
        <div>
          <h2 className="font-display text-xl font-bold text-ink">If the wash is not right</h2>
          <p className="mt-3">
            Tell us within 48 hours of delivery and we will re-wash the affected items at no
            charge, collected and returned at our cost. If a re-wash will not fix it, we will refund
            the charge for those items.
          </p>
        </div>

        <div>
          <h2 className="font-display text-xl font-bold text-ink">If we are late</h2>
          <p className="mt-3">
            If we miss your agreed return date and have not contacted you in advance to
            reschedule, the delivery fee for that order is refunded automatically. You do not need
            to ask.
          </p>
        </div>

        <div>
          <h2 className="font-display text-xl font-bold text-ink">If something is damaged or missing</h2>
          <p className="mt-3">
            Report it within 7 days of delivery. We will investigate using the item count and
            weight recorded at collection, and respond within 5 business days with an outcome.
          </p>
          <p className="mt-3">
            Where we are at fault, we will settle the claim. Settlement is based on the item's
            current value taking reasonable account of age and condition, not its original purchase
            price. This is standard practice across the industry and we would rather state it here
            than argue about it later.
          </p>
        </div>

        <div>
          <h2 className="font-display text-xl font-bold text-ink">What is not covered</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5">
            <li>Items where the manufacturer's care label was absent, illegible, or where following it caused the damage</li>
            <li>Pre-existing damage, wear or weakness not visible at collection</li>
            <li>Colour bleed from items not identified as at-risk at collection</li>
            <li>Items left in pockets — we check, but we cannot guarantee we catch everything</li>
            <li>Loss or damage to items we specifically advised against processing and you asked us to proceed with anyway</li>
          </ul>
        </div>

        <div>
          <h2 className="font-display text-xl font-bold text-ink">High-value items</h2>
          <p className="mt-3">
            Tell us before collection if any item is worth more than $250. We will either handle it
            under a specific arrangement or tell you we are not the right service for it. Items above
            this value that were not declared at collection are covered only to the standard limit.
          </p>
        </div>

        <div>
          <h2 className="font-display text-xl font-bold text-ink">Insurance</h2>
          <p className="mt-3">
            Our operators are required to hold current public liability cover, and the specific
            policy type and minimum sum insured are set out in the operator agreement. We will
            confirm the exact cover in place on request — email us and we will send you the detail
            rather than a vague assurance.
          </p>
        </div>

        <div className="card !bg-paper">
          <h2 className="font-display text-xl font-bold text-ink">Your rights under Australian Consumer Law</h2>
          <p className="mt-3">
            {site.legal.acl} Our services come with guarantees that cannot be excluded under the
            ACL, including that services are provided with due care and skill. If you believe we
            have failed to meet those guarantees, you have remedies available to you regardless of
            what this page says.
          </p>
        </div>

        <div>
          <h2 className="font-display text-xl font-bold text-ink">How to make a claim</h2>
          <p className="mt-3">
            Contact us through the contact page with your order reference, the affected items, and
            photographs where relevant. We will acknowledge within one business day.
          </p>
          <Link to="/contact" className="btn-navy mt-6 inline-flex">Contact &amp; complaints</Link>
        </div>
      </Reveal>
    </Section>
  );
}
