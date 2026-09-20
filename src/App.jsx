import { useEffect } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import Lenis from 'lenis';
import Navbar from './components/Navbar.jsx';
import Footer from './components/Footer.jsx';
import Home from './pages/Home.jsx';
import Placeholder from './pages/Placeholder.jsx';

const ROUTES = [
  ['/book', 'Book a collection'], ['/services', 'Our services'], ['/pricing', 'Pricing'],
  ['/legends-club', 'Legends Club'], ['/coverage', 'Coverage & suburbs'], ['/business', 'Business & commercial'],
  ['/supported-living', 'Supported living & aged care'], ['/operators', 'Become an operator'],
  ['/about', 'About Linen Legends'], ['/guarantee', 'Our service guarantee'], ['/faq', 'Frequently asked questions'],
  ['/contact', 'Contact us'], ['/privacy', 'Privacy policy'], ['/terms', 'Terms of service'],
  ['/account', 'My account'], ['/messages', 'Messages'],
];

function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => { window.scrollTo(0, 0); }, [pathname]);
  return null;
}

export default function App() {
  useEffect(() => {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const coarse = window.matchMedia('(pointer: coarse)').matches;
    if (reduced || coarse) return; // native scroll on touch and for reduced-motion users
    const lenis = new Lenis({ duration: 1.1, smoothWheel: true });
    let raf;
    const loop = (t) => { lenis.raf(t); raf = requestAnimationFrame(loop); };
    raf = requestAnimationFrame(loop);
    return () => { cancelAnimationFrame(raf); lenis.destroy(); };
  }, []);

  return (
    <div className="grain">
      <ScrollToTop />
      <Navbar />
      <main id="main">
        <Routes>
          <Route path="/" element={<Home />} />
          {ROUTES.map(([path, title]) => (
            <Route key={path} path={path} element={<Placeholder title={title} />} />
          ))}
          <Route path="*" element={<Placeholder title="Page not found" notFound />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}
