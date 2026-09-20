import { Link } from 'react-router-dom';
import Kinetic from '../components/Kinetic.jsx';
import Reveal from '../components/Reveal.jsx';
import Marquee from '../components/Marquee.jsx';
import Section from '../components/Section.jsx';
import Estimator from '../components/Estimator.jsx';
import PostcodeChecker from '../components/PostcodeChecker.jsx';
import FAQAccordion from '../components/FAQAccordion.jsx';
import site from '../data/site.js';
import { useMagnetic, useTilt, useParallax } from '../lib/hooks.js';

const TRUST = [
  ['Screened operators', 'Identity and background checks before the first job. Every operator, every time.'],
  ['Your wash, only yours', "Processed on its own cycle. Never mixed with another household's items."],
  ['Written guarantee', 'If we get it wrong, we re-do it or we refund it. In writing, no arguments.'],
  ['GST included, always', 'Every price on this site includes GST. No checkout surprises, no call-out fees.'],
];
const STEPS = [
  ['Book your window', 'Choose a day and a three-hour collection window online. Add care notes — cold wash, hang dry, folded flat. Takes two minutes.'],
  ['Price confirmed first', 'Your operator collects and weighs everything, then confirms the total before touching a thing. No work starts until you have the number.'],
  ['Back at your door', 'Washed, dried, folded or pressed, and delivered back. You pay after your price is confirmed. Pickup and return included.'],
];

function ClubCard({ p, i }) {
  const tilt = useTilt(6);
  return (
    <div ref={tilt} className={`card h-full !border-white/15 !bg-white/[0.05] text-white ${i === 0 ? 'ring-1 ring-ember' : ''}`}>
      <h3 className="font-display font-bold text-white">{p.name}</h3>
      <p className="mt-1 font-display text-4xl font-extrabold text-white">{['$63.70', '$89.70', '$115.70'][i]}<span className="text-sm font-semibold text-white/50">/week</span></p>
      <p className="mt-3 text-sm text-white/75">{p.blurb}</p>
      <p className="mt-4 border-t border-white/15 pt-3 text-xs font-semibold tracking-wide text-white/60">{p.loads.toUpperCase()}</p>
    </div>
  );
}

export default function Home() {
  const mag = useMagnetic(12);
  const parallax = useParallax(0.18);
  return (
    <>
      <section className="relative overflow-hidden bg-navy text-white">
        <div ref={parallax} aria-hidden="true" className="absolute inset-0 bg-[radial-gradient(80%_60%_at_70%_20%,#0e2a6a_0%,transparent_60%)]" />
        <div className="container-x relative grid gap-12 py-20 sm:py-28 lg:grid-cols-2 lg:items-center">
          <div>
            <Kinetic
              className="text-[clamp(2.6rem,7.5vw,4.6rem)] font-extrabold leading-[1.02] tracking-tight text-white"
              lines={['Laundry collected,', 'washed and returned.', 'We wash it well.']}
            />
            <Reveal delay={350}>
              <p className="mt-6 max-w-md text-lg leading-relaxed text-white/80">
                From your door, washed on its own cycle, folded or pressed, and brought back.
                Your price is confirmed after weighing — before we touch a thing.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                <Link ref={mag} to="/book" className="btn-primary">Book a collection</Link>
                <Link to="/pricing" className="btn-outline">See pricing</Link>
              </div>
              <p className="mt-6 text-sm text-white/60">Brisbane-owned · No app to download · Pay after weighing</p>
            </Reveal>
          </div>
          <Reveal variant="wipe-y" delay={200} className="hidden lg:block">
            <div className="card animate-float !border-white/10 !bg-white/[0.06] p-8 backdrop-blur">
              <p className="eyebrow !text-white/60">Typical household estimate</p>
              <dl className="mt-4 space-y-3 text-sm">
                <div className="flex justify-between text-white/80"><dt>2 × wash &amp; fold loads</dt><dd>$64</dd></div>
                <div className="flex justify-between text-white/80"><dt>Collection &amp; return</dt><dd>$13.50</dd></div>
                <div className="flex justify-between border-t border-white/15 pt-3 font-display text-2xl font-extrabold text-white"><dt className="self-end text-sm font-semibold text-white/60">FROM</dt><dd>$77.50</dd></div>
              </dl>
              <Link to="/book" className="btn-primary mt-6 w-full">Get my exact price</Link>
              <p className="mt-3 text-center text-xs text-white/50">Indicative only. Final price set when your operator weighs and counts. GST incl.</p>
            </div>
          </Reveal>
        </div>
        <div className="border-t border-white/10 py-4">
          <Marquee items={['Published GST-inclusive pricing', 'Washed on its own cycle', 'Screened operators', 'Written service guarantee', site.region, 'Pay after weighing']} />
        </div>
      </section>

      {/* Trust bento */}
      <Section>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {TRUST.map(([h, p], i) => (
            <Reveal key={h} delay={i * 80} className="h-full">
              <div className="card h-full transition-colors duration-300 hover:border-navy-light">
                <h3 className="font-display text-lg font-bold">{h}</h3>
                <p className="mt-2 text-sm leading-relaxed">{p}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </Section>

      {/* Steps — sticky stack */}
      <Section dark eyebrow="How it works" title="Three steps. Nothing to drop off.">
        <div className="grid gap-5">
          {STEPS.map(([h, p], i) => (
            <div key={h} className="lg:sticky" style={{ top: `${96 + i * 24}px` }}>
              <Reveal>
                <div className="card grid gap-4 !border-white/10 !bg-[#0e2a6a] p-8 sm:grid-cols-[64px_1fr] sm:items-start">
                  <span aria-hidden="true" className="font-display text-5xl font-extrabold text-ember">{i + 1}</span>
                  <div>
                    <h3 className="font-display text-xl font-bold text-white">{h}</h3>
                    <p className="mt-2 max-w-xl leading-relaxed text-white/75">{p}</p>
                  </div>
                </div>
              </Reveal>
            </div>
          ))}
        </div>
      </Section>

      {/* Bookable services */}
      <Section eyebrow="What you can book" title="Book online right now."
        lead="Published pricing, no phone call needed. Minimum $73.50 includes pickup, washing and return.">
        <div className="grid gap-5 lg:grid-cols-2">
          <Reveal className="h-full">
            <div className="card h-full !border-ember !bg-navy text-white ring-1 ring-ember">
              <p className="eyebrow">Most booked</p>
              <h3 className="mt-2 font-display text-2xl font-bold text-white">Wash &amp; Fold</h3>
              <p className="mt-2 leading-relaxed text-white/75">Everyday washing, collected and washed on its own cycle. Lights and darks separated as standard. Dried and folded.</p>
              <p className="mt-5 border-t border-white/15 pt-4 font-display font-bold">From $32 per load</p>
              <Link to="/book" className="btn-primary mt-4 w-full">Book Wash &amp; Fold</Link>
            </div>
          </Reveal>
          <Reveal delay={100} className="h-full">
            <div className="card h-full">
              <h3 className="font-display text-2xl font-bold">Blankets, Rugs &amp; Sheets</h3>
              <p className="mt-2 leading-relaxed">Large-format items only — not for everyday laundry. Priced per item, not by weight.</p>
              <p className="mt-5 border-t border-line pt-4 font-display font-bold text-ink">From $24 per item</p>
              <Link to="/book" className="btn-navy mt-4 w-full">Book Blankets &amp; Rugs</Link>
            </div>
          </Reveal>
        </div>
        <p className="mt-6 text-center text-sm">Dry cleaning, commercial linen and supported living are quoted per job — <Link to="/services" className="font-semibold text-navy underline">see all services</Link></p>
      </Section>

      {/* Estimator */}
      <Section id="estimate" className="!bg-paper" eyebrow="Before you book" title="Get your exact number."
        lead="An indicative estimate, not a quote. Your real price is set when your operator weighs and counts.">
        <Reveal><Estimator /></Reveal>
      </Section>

      {/* Club teaser */}
      <Section dark eyebrow="Legends Club" title="Put it on a schedule and stop thinking about it."
        lead="A recurring collection on a fixed day, weekly or fortnightly. Same operator, same preferences, flat weekly rate.">
        <div className="grid gap-5 lg:grid-cols-3">
          {site.club.plans.map((p, i) => (
            <Reveal key={p.key} delay={i * 90} className="h-full">
              <ClubCard p={p} i={i} />
            </Reveal>
          ))}
        </div>
        <Reveal delay={200}>
          <p className="mt-8 max-w-2xl text-white/80">Two ad-hoc loads a week ≈ $77.50 · Legends Club Solo = $63.70/week. Save around $14 a week compared with two ad-hoc loads — no lock-in, pause any time.</p>
          <Link to="/legends-club" className="btn-primary mt-5">See Legends Club plans</Link>
        </Reveal>
      </Section>

      {/* Coverage gate */}
      <Section eyebrow="Service area" title="Ready to book? Check your postcode."
        lead="We collect in 16 suburbs today and open more every month. If we are not in your street yet, register and we will contact you.">
        <Reveal><PostcodeChecker /></Reveal>
        <p className="mt-6 text-center text-sm"><Link to="/coverage" className="font-semibold text-navy underline">See every suburb, including opening soon</Link></p>
      </Section>

      {/* Honest new-business block — no fake reviews, ever */}
      <Section className="!bg-paper">
        <Reveal className="mx-auto max-w-3xl text-center">
          <p className="eyebrow">New in Brisbane</p>
          <h2 className="mt-2 text-3xl font-extrabold sm:text-4xl">Be one of our first customers and shape how we grow.</h2>
          <p className="mx-auto mt-4 max-w-2xl text-lg leading-relaxed">We're a new business. Rather than claim thousands of orders we don't have, we're being honest: we're starting with great systems, screened operators, and a written service guarantee. Your feedback makes us better.</p>
          <Link to="/book" className="btn-primary mt-6">Book your first collection</Link>
        </Reveal>
      </Section>

      {/* Not a household */}
      <Section eyebrow="Not booking for a household?" title="Business, care and operators.">
        <div className="grid gap-5 lg:grid-cols-3">
          {[
            ['/business', 'Business & commercial', 'Short-stay properties, salons, gyms, cafés and clubs. Scheduled collections, account billing, volume rates.', 'Request a quote'],
            ['/supported-living', 'Supported living & aged care', 'Regular laundry assistance for people living independently, and for the providers who support them.', 'See how it works'],
            ['/operators', 'Become an operator', 'Run a round in your own suburb, under your own ABN, with our customers and systems behind you.', 'Operator information'],
          ].map(([to, h, p, cta], i) => (
            <Reveal key={to} delay={i * 90} className="h-full">
              <Link to={to} className="card block h-full transition-all duration-300 hover:-translate-y-1 hover:border-navy-light">
                <h3 className="font-display text-xl font-bold">{h}</h3>
                <p className="mt-2 text-sm leading-relaxed">{p}</p>
                <p className="mt-4 font-display text-sm font-bold text-ember">{cta} →</p>
              </Link>
            </Reveal>
          ))}
        </div>
      </Section>

      {/* FAQ teaser */}
      <Section className="!bg-paper" eyebrow="Questions" title="Asked all the time.">
        <div className="mx-auto max-w-3xl">
          <Reveal><FAQAccordion limit={4} /></Reveal>
          <p className="mt-5 text-center"><Link to="/faq" className="font-semibold text-navy underline">All questions, answered plainly</Link></p>
        </div>
      </Section>

      {/* CTA */}
      <section className="bg-ember py-16 text-center text-white sm:py-20">
        <Reveal className="container-x">
          <h2 className="text-3xl font-extrabold text-white sm:text-4xl">Tonight's basket, gone by tomorrow.</h2>
          <p className="mx-auto mt-3 max-w-xl text-white/85">Book a three-hour window now. Price confirmed before a single item is washed.</p>
          <Link to="/book" className="btn mt-6 bg-white font-bold text-ember hover:bg-white/90">Book a collection</Link>
        </Reveal>
      </section>
    </>
  );
}
