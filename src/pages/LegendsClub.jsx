import { Link } from 'react-router-dom';
import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import site from '../data/site.js';

const PRICES = ['$63.70', '$89.70', '$115.70'];

const HOW = [
  ['Set your day', 'Choose a weekly or fortnightly collection day and time window. Your run is built into the operator’s route for that suburb.'],
  ['Set your preferences once', 'Detergent, temperature, hang-dry items, folding style. Saved to your account and applied to every collection without you repeating yourself.'],
  ['Pause any time', 'Going away? Pause with notice before your collection day. No fee, no penalty, and your slot is held for your return.'],
];

export default function LegendsClub() {
  return (
    <>
      <Section eyebrow="Home / Legends Club" title="Legends Club"
        lead="A recurring laundry collection on a fixed day, at a fixed weekly price, with your preferences saved. No lock-in contract.">
        <p className="eyebrow mb-2">Plans</p>
        <h2 className="text-2xl font-extrabold sm:text-3xl">Pick the size that matches your household.</h2>
        <p className="mt-2 text-body">All plans include collection and return.</p>
        <div className="mt-8 grid gap-5 lg:grid-cols-3">
          {site.club.plans.map((p, i) => (
            <Reveal key={p.key} delay={i * 90} className="h-full">
              <div className={`card h-full ${i === 0 ? 'ring-1 ring-ember' : ''}`}>
                <h3 className="font-display text-lg font-bold">{p.name}</h3>
                <p className="mt-1 font-display text-4xl font-extrabold text-ink">{PRICES[i]}<span className="text-sm font-semibold text-body">/week</span></p>
                <p className="mt-3 text-sm leading-relaxed">{p.blurb}</p>
                <p className="mt-4 border-t border-line pt-3 text-xs font-semibold tracking-wide text-body">{p.loads.toUpperCase()}</p>
              </div>
            </Reveal>
          ))}
        </div>
        <p className="mt-6 max-w-2xl text-sm text-body">Bag sizes are confirmed at your first collection. If you consistently exceed your plan size, we will contact you to move you up rather than silently charging extra.</p>
      </Section>

      <Section dark eyebrow="Membership" title="How membership works">
        <div className="grid gap-5 lg:grid-cols-3">
          {HOW.map(([h, p], i) => (
            <Reveal key={h} delay={i * 90} className="h-full">
              <div className="card h-full !border-white/15 !bg-white/[0.05] text-white">
                <h3 className="font-display text-lg font-bold text-white">{h}</h3>
                <p className="mt-2 text-sm leading-relaxed text-white/75">{p}</p>
              </div>
            </Reveal>
          ))}
        </div>
        <Reveal delay={270}>
          <p className="mt-8 max-w-2xl text-sm leading-relaxed text-white/80">Cancellation. Legends Club has no minimum term and no exit fee. Cancel with notice before your next scheduled collection and billing stops. Fees already paid for a completed period are not refunded. Full terms on the Terms of Service page.</p>
        </Reveal>
      </Section>

      <Section className="!bg-paper" eyebrow="The numbers" title="Compare it to ad-hoc booking.">
        <Reveal className="max-w-2xl">
          <p className="text-lg leading-relaxed">Two ad-hoc loads a week ≈ $77.50. Legends Club Solo is $63.70/week — a saving of around $14 a week, with no lock-in and the option to pause any time.</p>
          <Link to="/book" className="btn-primary mt-6">Book your first collection</Link>
        </Reveal>
      </Section>
    </>
  );
}
