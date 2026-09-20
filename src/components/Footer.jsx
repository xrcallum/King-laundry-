import { Link } from 'react-router-dom';
import site from '../data/site.js';

const COLS = [
  ['Service', [['/services', 'Services'], ['/pricing', 'Pricing'], ['/legends-club', 'Legends Club'], ['/coverage', 'Coverage & suburbs'], ['/business', 'For business'], ['/supported-living', 'Supported living']]],
  ['Company', [['/about', 'About us'], ['/operators', 'Become an operator'], ['/faq', 'FAQ'], ['/guarantee', 'Service guarantee'], ['/contact', 'Contact & complaints']]],
];

export default function Footer() {
  return (
    <footer className="bg-navy-deep text-white" role="contentinfo">
      <div className="container-x grid gap-10 py-16 sm:grid-cols-2 lg:grid-cols-4">
        <div className="lg:col-span-2">
          <p className="font-display text-lg font-extrabold uppercase">Linen<span className="text-ember"> Legends</span></p>
          <p className="mt-1 text-[11px] font-semibold tracking-[0.22em] text-white/50">{site.tagline.toUpperCase()}</p>
          <p className="mt-4 max-w-xs text-sm leading-relaxed text-white/70">Laundry collection and delivery across {site.region.replace(' & ', ', ')}.</p>
          <p className="mt-4 text-sm text-white/60">{site.legal.phone}. {site.legal.email}.</p>
        </div>
        {COLS.map(([head, links]) => (
          <nav key={head} aria-label={head}>
            <p className="font-display text-sm font-bold uppercase tracking-wider text-white/50">{head}</p>
            <ul className="mt-4 space-y-2.5">
              {links.map(([to, label]) => (
                <li key={to}><Link to={to} className="text-sm text-white/75 hover:text-white">{label}</Link></li>
              ))}
            </ul>
          </nav>
        ))}
      </div>
      <div className="border-t border-white/10">
        <div className="container-x flex flex-col gap-3 py-6 text-xs text-white/55 sm:flex-row sm:items-center sm:justify-between">
          <p>© 2026 {site.brand} · {site.legal.footerEntity} · {site.legal.gst} · {site.legal.owned}</p>
          <p className="flex gap-4">
            <Link to="/privacy" className="hover:text-white">Privacy policy</Link>
            <Link to="/terms" className="hover:text-white">Terms of service</Link>
            <Link to="/guarantee" className="hover:text-white">Service guarantee</Link>
          </p>
        </div>
      </div>
    </footer>
  );
}
