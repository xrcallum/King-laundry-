import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import site from '../data/site.js';

export default function Terms() {
  return (
    <Section
      eyebrow="Home / Terms of Service"
      title="Terms of service"
      lead="The terms on which we provide laundry collection, cleaning and delivery services."
    >
      <Reveal className="mx-auto max-w-3xl">
        <div className="rounded-xl border border-amber-500/40 bg-amber-50 p-4 text-amber-900">
          <p className="font-semibold">Draft for legal review — not yet in force.</p>
          <p className="mt-1 text-sm">Date of effect to be inserted on approval.</p>
        </div>

        <div className="mt-10 space-y-10 text-[17px] leading-relaxed text-body">
          <div>
            <h2 className="font-display text-xl font-bold text-ink">1. These terms</h2>
            <p className="mt-3">
              These terms apply when you book any service from {site.brand}. By placing a booking
              you agree to them. If you do not agree, do not book.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">2. Bookings and quotes</h2>
            <p className="mt-3">
              Prices shown on this website and in the online estimator are indicative. Your final
              price is determined after your items are weighed and counted at collection, and is
              confirmed to you before any cleaning begins. If you do not accept the confirmed
              price, your items are returned to you at no charge.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">3. Collection and delivery</h2>
            <p className="mt-3">
              Collection and delivery occur within the window agreed at booking. Where you have
              authorised unattended collection or delivery, items left at an agreed location are at
              your risk from the point they are left until they are collected by us, and from the
              point they are delivered until you retrieve them.
            </p>
            <p className="mt-3">
              If we cannot access your items at the agreed time through no fault of ours, a failed
              collection fee may apply. It will be disclosed to you before it is charged.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">4. Your items</h2>
            <p className="mt-3">You confirm that items you submit:</p>
            <ul className="mt-3 list-disc space-y-2 pl-5">
              <li>Are yours, or you are authorised to submit them</li>
              <li>Are suitable for the service selected</li>
              <li>Do not contain hazardous materials, biohazards, sharps, or contaminated waste</li>
              <li>Have been emptied of valuables, cash, keys and electronics</li>
            </ul>
            <p className="mt-3">
              We are not liable for items left in pockets. We may refuse to process any item at our
              discretion, and will tell you why.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">5. Care labels and risk</h2>
            <p className="mt-3">
              We process items in accordance with their manufacturer care labels. Where a label is
              missing, illegible or incorrect, we process according to reasonable professional
              judgement and are not liable for resulting damage. Where we assess an item as
              high-risk we will contact you and proceed only with your instruction, at your risk.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">6. Payment</h2>
            <p className="mt-3">
              Payment is due once your final price is confirmed and before return delivery, unless
              you hold an approved account. {site.club.name} memberships are billed in advance on
              your nominated cycle. We may suspend service on overdue accounts after written
              notice.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">7. {site.club.name}</h2>
            <p className="mt-3">
              {site.club.name} has no minimum term. You may pause or cancel with notice before
              your next scheduled collection; billing stops from that point. Fees already paid for a
              completed billing period are not refunded. We may change plan pricing with written
              notice before your next billing date, and you may cancel rather than accept the
              change.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">8. Liability and claims</h2>
            <p className="mt-3">
              Claims must be made within the timeframes set out in our Service Guarantee. Our
              liability for loss or damage is limited as described there, and is based on an item's
              current value taking reasonable account of age and condition.
            </p>
            <p className="mt-3">
              Nothing in these terms excludes, restricts or modifies any guarantee, right or remedy
              you have under the Australian Consumer Law that cannot lawfully be excluded. Where
              our liability can be limited under the ACL, it is limited to resupplying the service or
              paying the cost of resupply.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">9. Unclaimed items</h2>
            <p className="mt-3">
              Where we cannot deliver items and cannot contact you, we will hold them for 90 days
              and make reasonable attempts to reach you. After 90 days we may dispose of or
              donate them, and recover reasonable storage costs.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">10. Our operators</h2>
            <p className="mt-3">
              Services are performed by independent operators engaged by us. We remain
              responsible to you for the service under these terms and under the Australian
              Consumer Law.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">11. Suspension and termination</h2>
            <p className="mt-3">
              We may decline or discontinue service where items are unsuitable, where an account
              is overdue, or where an operator's safety is at risk. We will tell you why.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">12. Governing law</h2>
            <p className="mt-3">
              These terms are governed by the laws of Queensland, Australia, and the courts of
              Queensland have jurisdiction.
            </p>
          </div>

          <div>
            <h2 className="font-display text-xl font-bold text-ink">13. Changes</h2>
            <p className="mt-3">
              We may update these terms. The version published here at the time you place a
              booking is the version that applies to it.
            </p>
          </div>
        </div>
      </Reveal>
    </Section>
  );
}
