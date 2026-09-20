import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import site from '../data/site.js';

export default function Privacy() {
  return (
    <Section
      eyebrow="Home / Privacy Policy"
      title="Privacy policy"
      lead="How we collect, use, store and disclose your personal information."
    >
      <Reveal className="mx-auto max-w-3xl">
        <div className="rounded-xl border border-amber-500/40 bg-amber-50 p-4 text-amber-900">
          <p className="font-semibold">Draft for legal review — not yet in force.</p>
          <p className="mt-1 text-sm">Date of effect to be inserted on approval.</p>
        </div>

        <div className="mt-10 space-y-10 text-[17px] leading-relaxed text-body">
          <p>
            This policy explains how {site.brand} handles personal information in accordance with
            the Privacy Act 1988 (Cth) and the Australian Privacy Principles.
          </p>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">1. What we collect</h2>
            <ul className="mt-3 list-disc space-y-2 pl-5">
              <li><strong>Identity and contact details</strong> — name, email, phone number, residential or business address.</li>
              <li><strong>Service information</strong> — collection addresses, access instructions, laundry preferences, order history, item counts and weights.</li>
              <li><strong>Payment information</strong> — processed by our third-party payment provider. We do not store full card numbers on our systems.</li>
              <li><strong>Communications</strong> — enquiries, messages and records of our correspondence with you.</li>
              <li><strong>Technical information</strong> — IP address, browser type and pages visited, collected when you use this website.</li>
              <li><strong>Operator applicants</strong> — additionally, ABN, equipment details, availability, and the results of identity and background screening.</li>
            </ul>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">2. Why we collect it</h2>
            <ul className="mt-3 list-disc space-y-2 pl-5">
              <li>To provide the service you have booked and to contact you about it</li>
              <li>To process payments and issue invoices</li>
              <li>To route your job to an operator in your area</li>
              <li>To handle enquiries, complaints and claims</li>
              <li>To meet our legal and tax record-keeping obligations</li>
              <li>To improve our service and plan where we open next</li>
            </ul>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">3. Who we share it with</h2>
            <p className="mt-3">We disclose personal information only where necessary, to:</p>
            <ul className="mt-3 list-disc space-y-2 pl-5">
              <li><strong>The operator assigned to your job</strong> — your name, collection address, access instructions and service preferences. Operators are bound by confidentiality obligations in their agreement with us.</li>
              <li><strong>Specialist partner cleaners</strong> — where your order includes dry cleaning.</li>
              <li><strong>Service providers</strong> — payment processing, SMS and email delivery, cloud hosting and customer support tooling.</li>
              <li><strong>Plan managers or support coordinators</strong> — only where you have engaged us through them, and only invoicing and service information.</li>
              <li><strong>Law enforcement or regulators</strong> — where we are legally required to do so.</li>
            </ul>
            <p className="mt-3">We do not sell personal information. We do not disclose it for third-party marketing.</p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">4. Overseas disclosure</h2>
            <p className="mt-3">
              Some of our technology providers store data outside Australia. Where that is the case
              we take reasonable steps to ensure the recipient handles the information consistently
              with the Australian Privacy Principles. The specific providers and their locations will
              be listed here before this policy takes effect.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">5. Security</h2>
            <p className="mt-3">
              We hold personal information in access-controlled systems and restrict access to
              those who need it to do their job. No system is perfectly secure. If a data breach
              occurs that is likely to result in serious harm, we will notify affected individuals and
              the Office of the Australian Information Commissioner as required under the
              Notifiable Data Breaches scheme.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">6. Retention</h2>
            <p className="mt-3">
              We keep personal information only as long as needed for the purpose it was
              collected, or as required by law — including tax and business record-keeping
              obligations, generally five years. Unsuccessful operator applications are destroyed
              within 12 months unless you ask us to keep them on file.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">7. Accessing and correcting your information</h2>
            <p className="mt-3">
              You may request access to the personal information we hold about you, and ask us to
              correct it. Contact us through the contact page. We will respond within 30 days. If we
              refuse access we will tell you why in writing.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">8. Marketing</h2>
            <p className="mt-3">
              We may send you service updates and offers by email or SMS. Every marketing
              message includes an unsubscribe method. Opting out of marketing does not stop
              operational messages about a booking you have made.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">9. Cookies</h2>
            <p className="mt-3">
              This website uses cookies and similar technologies for essential functionality and
              analytics. You can block cookies in your browser, though some parts of the site may
              not work correctly.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">10. Complaints</h2>
            <p className="mt-3">
              If you believe we have mishandled your personal information, contact us first and we
              will investigate. If you are not satisfied with our response, you may complain to the
              Office of the Australian Information Commissioner at oaic.gov.au.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">11. Changes</h2>
            <p className="mt-3">
              We may update this policy. The current version is always published here with its date
              of effect.
            </p>
          </div>
        </div>
      </Reveal>
    </Section>
  );
}
