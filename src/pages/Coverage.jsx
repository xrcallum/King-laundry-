import { Link } from 'react-router-dom';
import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import PostcodeChecker from '../components/PostcodeChecker.jsx';
import { LIVE_PC, SOON_PC } from '../../api/_lib/coverage.js';

function bySuburb(map) {
  return Object.entries(map)
    .map(([postcode, suburb]) => ({ postcode, suburb }))
    .sort((a, b) => a.suburb.localeCompare(b.suburb));
}

function SuburbGrid({ items, tone }) {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
      {items.map((s) => (
        <div
          key={s.postcode}
          className={`rounded-xl border p-4 text-sm ${tone === 'active' ? 'border-line bg-white' : 'border-line bg-paper'}`}
        >
          <p className="font-display font-bold text-ink">{s.suburb}</p>
          <p className="mt-0.5 text-body">{s.postcode}</p>
        </div>
      ))}
    </div>
  );
}

export default function Coverage() {
  const live = bySuburb(LIVE_PC);
  const soon = bySuburb(SOON_PC);

  return (
    <>
      <Section
        eyebrow="Home / Coverage"
        title="Coverage & suburbs"
        lead="We open suburb by suburb, not city by city. A suburb goes live once we have an operator with capacity to serve it properly."
      >
        <Reveal><PostcodeChecker /></Reveal>
      </Section>

      <Section className="!bg-paper" eyebrow={`Collecting now (${live.length} suburbs)`} title="Live today">
        <Reveal><SuburbGrid items={live} tone="active" /></Reveal>
      </Section>

      <Section eyebrow={`Opening next (${soon.length} suburbs)`} title="Recruiting an operator now">
        <Reveal><SuburbGrid items={soon} tone="opening" /></Reveal>
        <Reveal delay={100}>
          <p className="mx-auto mt-8 max-w-2xl text-center text-sm text-body">
            Not on the list? Enter your postcode in the checker above and we will register it. We build new rounds
            where demand is highest, and registered interest is exactly how we decide where to go next. If you would
            like to run the round yourself, see{' '}
            <Link to="/operators" className="font-semibold text-navy underline">Become an Operator</Link>.
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
