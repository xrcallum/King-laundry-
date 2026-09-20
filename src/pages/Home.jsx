import { Link } from 'react-router-dom';
import Kinetic from '../components/Kinetic.jsx';
import Reveal from '../components/Reveal.jsx';
import Marquee from '../components/Marquee.jsx';
import site from '../data/site.js';

export default function Home() {
  return (
    <>
      <section className="relative overflow-hidden bg-navy text-white">
        <div aria-hidden="true" className="absolute inset-0 bg-[radial-gradient(80%_60%_at_70%_20%,#0e2a6a_0%,transparent_60%)]" />
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
                <Link to="/book" className="btn-primary">Book a collection</Link>
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
                <div className="flex justify-between border-t border-white/15 pt-3 font-display text-2xl font-extrabold text-white"><dt className="text-sm font-semibold self-end text-white/60">FROM</dt><dd>$77.50</dd></div>
              </dl>
              <Link to="/book" className="btn-primary mt-6 w-full">Get my exact price</Link>
              <p className="mt-3 text-center text-xs text-white/50">Indicative only. Final price set when your operator weighs and counts. GST incl.</p>
            </div>
          </Reveal>
        </div>
        <div className="border-t border-white/10 py-4">
          <Marquee items={[
            'Published GST-inclusive pricing', 'Washed on its own cycle', 'Screened operators',
            'Written service guarantee', site.region, 'Pay after weighing',
          ]} />
        </div>
      </section>
    </>
  );
}
