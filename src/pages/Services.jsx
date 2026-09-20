import { Link } from 'react-router-dom';
import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';

const SERVICES = [
  {
    name: 'Wash & Fold',
    blurb: 'Your everyday washing, collected and returned clean and folded.',
    price: 'From $32 per load',
    cta: 'Book Wash & Fold',
    bullets: [
      "Washed on its own cycle — never mixed with another household's items",
      'Lights and darks separated as standard (charged as separate loads)',
      'Pockets checked before every wash',
      'Standard, sensitive-skin or fragrance-free detergent',
      'Folded and returned in your bag',
    ],
  },
  {
    name: 'Blankets, Rugs & Sheets',
    blurb: 'Large-format items only. Not for everyday laundry, and not charged by weight.',
    price: 'From $24 per item',
    cta: 'Book Blankets & Rugs',
    bullets: [
      'Blankets, quilt covers, rugs and sheet sets',
      'Priced per item, machine capacity confirmed before collection',
      'Longer turnaround — confirmed at booking',
    ],
  },
];

const DRY_CLEANING = {
  name: 'Dry Cleaning',
  blurb: 'Handled through vetted specialist partner cleaners.',
  price: 'From $16.50 per item',
  bullets: [
    'Suits, jackets, formal wear, delicates',
    'Priced by item and size, not by weight',
    'No perchloroethylene (PERC) used',
    'Faults and stains flagged to you before cleaning',
    'Returned covered and on hangers',
  ],
};

const BULKY = {
  name: 'Bulky Items',
  blurb: 'Doonas, quilts, mattress protectors, pet bedding and curtains.',
  price: 'From $45 per item',
  bullets: [
    'Priced per item — full rates on the pricing page',
    'Machine capacity confirmed before collection',
    'Longer turnaround — confirmed at booking',
  ],
};

const COMMERCIAL = {
  name: 'Commercial & Linen',
  blurb: 'Scheduled service for businesses with recurring linen volume.',
  price: 'Quoted per site — enquire',
  bullets: [
    'Short-stay and holiday properties',
    'Salons, gyms, clinics and studios',
    'Cafés, restaurants and clubs',
    'Account billing, scheduled runs, volume pricing',
  ],
};

function ServiceCard({ s, dark = false, delay = 0, to = '/book' }) {
  return (
    <Reveal delay={delay} className="h-full">
      <div
        className={`card h-full transition-all duration-300 hover:-translate-y-1 ${
          dark
            ? '!border-ember !bg-navy text-white ring-1 ring-ember hover:shadow-xl hover:shadow-ember/20'
            : 'hover:border-navy-light hover:shadow-lg'
        }`}
      >
        <h3 className={`font-display text-xl font-bold ${dark ? 'text-white' : ''}`}>{s.name}</h3>
        <p className={`mt-2 leading-relaxed ${dark ? 'text-white/75' : ''}`}>{s.blurb}</p>
        <ul className={`mt-4 space-y-1.5 text-sm ${dark ? 'text-white/80' : ''}`}>
          {s.bullets.map((b) => (
            <li key={b} className="flex gap-2">
              <span aria-hidden="true" className="mt-2 h-1 w-1 shrink-0 rounded-full bg-ember" />
              <span>{b}</span>
            </li>
          ))}
        </ul>
        <p className={`mt-5 border-t pt-4 font-display font-bold ${dark ? 'border-white/15' : 'border-line text-ink'}`}>{s.price}</p>
        {s.cta && (
          <Link to={to} className={`mt-4 w-full ${dark ? 'btn-primary' : 'btn-navy'}`}>{s.cta}</Link>
        )}
      </div>
    </Reveal>
  );
}

export default function Services() {
  return (
    <>
      <Section
        eyebrow="Home / Services"
        title="Our services"
        lead="Every service below is available across our active service area. Pricing is published in full — nothing is hidden behind a phone call."
      >
        <div className="grid gap-5 lg:grid-cols-2">
          <ServiceCard s={SERVICES[0]} dark delay={0} />
          <ServiceCard s={SERVICES[1]} delay={100} />
        </div>
      </Section>

      <Section className="!bg-paper">
        <div className="grid gap-5 lg:grid-cols-2">
          <ServiceCard s={DRY_CLEANING} delay={0} to="/book" />
          <ServiceCard s={BULKY} delay={100} to="/book" />
        </div>
      </Section>

      <Section>
        <Reveal>
          <div className="card transition-all duration-300 hover:-translate-y-1 hover:border-navy-light hover:shadow-lg">
            <h3 className="font-display text-xl font-bold">{COMMERCIAL.name}</h3>
            <p className="mt-2 leading-relaxed">{COMMERCIAL.blurb}</p>
            <ul className="mt-4 grid gap-1.5 text-sm sm:grid-cols-2">
              {COMMERCIAL.bullets.map((b) => (
                <li key={b} className="flex gap-2">
                  <span aria-hidden="true" className="mt-2 h-1 w-1 shrink-0 rounded-full bg-ember" />
                  <span>{b}</span>
                </li>
              ))}
            </ul>
            <p className="mt-5 border-t border-line pt-4 font-display font-bold text-ink">{COMMERCIAL.price}</p>
            <Link to="/business" className="btn-navy mt-4">Request a commercial quote</Link>
          </div>
        </Reveal>

        <Reveal delay={100}>
          <p className="mx-auto mt-8 max-w-3xl text-center text-sm text-body">
            What affects your final price: weight, number of separated loads, large linen items, bulky items, and your
            distance from the nearest active operator. Your operator confirms the final figure after weighing and
            before any work begins.
          </p>
        </Reveal>
      </Section>

      <section className="bg-ember py-16 text-center text-white sm:py-20">
        <Reveal className="container-x">
          <h2 className="text-3xl font-extrabold text-white sm:text-4xl">Ready to book?</h2>
          <p className="mx-auto mt-3 max-w-xl text-white/85">
            Published pricing, price confirmed after weighing, collection and return included.
          </p>
          <Link to="/book" className="btn mt-6 bg-white font-bold text-ember hover:bg-white/90">Book a collection</Link>
        </Reveal>
      </section>
    </>
  );
}
