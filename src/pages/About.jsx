import { Link } from 'react-router-dom';
import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import site from '../data/site.js';

const commitments = [
  {
    title: 'Published pricing',
    body: 'Every rate is on this website. You never have to ring to find out what something costs.',
  },
  {
    title: 'Price confirmed before work starts',
    body: 'Your operator weighs and counts, then confirms the figure. Nothing proceeds until you have it.',
  },
  {
    title: 'Your wash is your wash',
    body: "Processed on its own cycle, never combined with another household's items.",
  },
  {
    title: 'We say what we cannot do',
    body: 'If we are not accredited for something, or not registered for something, we say so on the relevant page rather than letting you find out later.',
  },
];

export default function About() {
  return (
    <>
      <Section
        eyebrow="Home / About"
        title={`About ${site.brand}`}
        lead={`An Australian-owned laundry collection and delivery business built for ${site.region}.`}
      >
        <Reveal className="max-w-3xl">
          <h3 className="font-display text-xl font-bold text-ink">What we are</h3>
          <p className="mt-3 text-[17px] leading-relaxed text-body">
            {site.brand} collects your laundry, washes it properly, and brings it back. That is the
            whole proposition. We are not a laundromat you drive to, and we are not an app that
            disappears when something goes wrong.
          </p>
          <p className="mt-4 text-[17px] leading-relaxed text-body">
            We operate through a network of local operators — independent small businesses
            running collections in their own suburbs — supported by a central booking, routing and
            customer service platform. The person handling your washing lives near you, and the
            systems behind them are run properly.
          </p>
        </Reveal>
      </Section>

      <Section dark className="!bg-navy" eyebrow="Why we built it this way" title="Two things are broken in this category">
        <Reveal className="max-w-3xl">
          <p className="text-lg leading-relaxed text-white/80">
            Traditional laundries keep hours that working people cannot use, and publish no
            pricing at all. App-based services solved the convenience problem but treated the
            people doing the work as disposable — and most of them are gone.
          </p>
          <p className="mt-4 text-lg leading-relaxed text-white/80">
            We built for the middle: published pricing, proper scheduling, and operators treated
            as business partners rather than units of throughput. A round only opens when there is
            someone good enough to run it.
          </p>
        </Reveal>
      </Section>

      <Section eyebrow="How we are different" title="Four commitments" className="!bg-paper">
        <div className="grid gap-6 sm:grid-cols-2">
          {commitments.map((c, i) => (
            <Reveal key={c.title} delay={i * 80}>
              <div className="card h-full">
                <h3 className="font-display text-lg font-bold text-ink">{c.title}</h3>
                <p className="mt-2 text-[15px] leading-relaxed text-body">{c.body}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </Section>

      <Section eyebrow="Coverage" title="Building out suburb by suburb">
        <Reveal className="max-w-3xl">
          <p className="text-[17px] leading-relaxed text-body">
            We are currently building out across {site.region}, suburb by suburb. Our coverage page
            shows where we are live and where we are opening next.
          </p>
          <Link to="/coverage" className="btn-navy mt-6 inline-flex">See coverage &amp; suburbs</Link>
          <p className="mt-10 border-t border-line pt-6 text-sm text-body/80">
            Company name and ABN details are published in the footer of every page.
          </p>
        </Reveal>
      </Section>
    </>
  );
}
