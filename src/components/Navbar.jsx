import { useEffect, useRef, useState } from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import site from '../data/site.js';

const LINKS = [
  ['/services', 'Services'], ['/pricing', 'Pricing'], ['/legends-club', 'Legends Club'],
  ['/coverage', 'Coverage'], ['/business', 'For business'],
];
const MENU = [
  ...LINKS, ['/supported-living', 'Supported living'], ['/operators', 'Become an operator'],
  ['/about', 'About'], ['/guarantee', 'Guarantee'], ['/faq', 'FAQ'], ['/contact', 'Contact'],
];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const barRef = useRef(null);
  const { pathname } = useLocation();

  useEffect(() => {
    const bar = document.getElementById('scroll-progress');
    const onScroll = () => {
      setScrolled(window.scrollY > 24);
      if (bar) {
        const h = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.transform = `scaleX(${h > 0 ? window.scrollY / h : 0})`;
      }
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => { setOpen(false); }, [pathname]);
  useEffect(() => {
    if (!open) return;
    const onKey = (e) => { if (e.key === 'Escape') setOpen(false); };
    document.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    return () => { document.removeEventListener('keydown', onKey); document.body.style.overflow = ''; };
  }, [open]);

  return (
    <>
      <div id="scroll-progress" className="progress" aria-hidden="true" />
      <header
        ref={barRef}
        className={`sticky top-0 z-50 transition-all duration-300 ${scrolled ? 'bg-navy/80 backdrop-blur-xl shadow-lg shadow-navy-deep/20' : 'bg-navy'}`}
      >
        <div className={`container-x flex items-center justify-between transition-all duration-300 ${scrolled ? 'h-[60px]' : 'h-[76px]'}`}>
          <Link to="/" className="font-display text-lg font-extrabold uppercase tracking-tight text-white">
            Linen<span className="text-ember"> Legends</span>
            <span className="ml-2 hidden text-[10px] font-semibold tracking-[0.22em] text-white/60 sm:inline">{site.tagline.toUpperCase()}</span>
          </Link>
          <nav className="hidden items-center gap-6 lg:flex" aria-label="Primary">
            {LINKS.map(([to, label]) => (
              <NavLink key={to} to={to} className={({ isActive }) => `font-display text-sm font-semibold ${isActive ? 'text-white' : 'text-white/70 hover:text-white'}`}>{label}</NavLink>
            ))}
          </nav>
          <div className="flex items-center gap-3">
            <Link to="/account" className="hidden font-display text-sm font-semibold text-white/80 hover:text-white sm:block">My account</Link>
            <Link to="/book" className="btn-primary !py-2.5 !px-5 text-sm">Book a collection</Link>
            <button
              type="button" aria-expanded={open} aria-controls="site-menu"
              onClick={() => setOpen(!open)}
              className="flex h-10 w-10 items-center justify-center rounded-full text-white lg:hidden"
            >
              <span className="sr-only">{open ? 'Close menu' : 'Open menu'}</span>
              <svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                {open ? <path d="M4 4l14 14M18 4L4 18" /> : <path d="M2 6h18M2 11h18M2 16h18" />}
              </svg>
            </button>
          </div>
        </div>
      </header>
      <div
        id="site-menu" role="dialog" aria-modal="true" aria-label="Menu"
        className={`fixed inset-0 z-40 bg-navy-deep transition-[clip-path] duration-500 ease-[cubic-bezier(.22,1,.36,1)] ${open ? '[clip-path:circle(150%_at_100%_0)]' : 'pointer-events-none [clip-path:circle(0%_at_calc(100%-40px)_38px)]'}`}
      >
        <nav className="container-x flex h-full flex-col justify-center gap-1 py-24" aria-label="Menu">
          {MENU.map(([to, label], i) => (
            <NavLink
              key={to} to={to} tabIndex={open ? 0 : -1}
              className="font-display text-[clamp(1.6rem,6vw,3rem)] font-extrabold uppercase leading-tight text-white/85 hover:text-white"
              style={{ transitionDelay: `${i * 30}ms` }}
            >{label}</NavLink>
          ))}
          <Link to="/book" tabIndex={open ? 0 : -1} className="btn-primary mt-6 self-start">Book a collection</Link>
        </nav>
      </div>
    </>
  );
}
