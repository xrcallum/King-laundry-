import { Suspense, lazy, useEffect } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import Lenis from 'lenis';
import Navbar from './components/Navbar.jsx';
import Footer from './components/Footer.jsx';
import Home from './pages/Home.jsx';

const P = (n) => lazy(() => import(`./pages/${n}.jsx`));
const PAGES = {
  '/book': P('Book'), '/services': P('Services'), '/pricing': P('Pricing'),
  '/legends-club': P('LegendsClub'), '/coverage': P('Coverage'), '/business': P('Business'),
  '/supported-living': P('SupportedLiving'), '/operators': P('Operators'), '/about': P('About'),
  '/guarantee': P('Guarantee'), '/faq': P('Faq'), '/contact': P('Contact'),
  '/privacy': P('Privacy'), '/terms': P('Terms'), '/account': P('Account'), '/messages': P('Messages'),
};
const NotFound = P('Placeholder');

function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => { window.scrollTo(0, 0); }, [pathname]);
  return null;
}

export default function App() {
  useEffect(() => {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const coarse = window.matchMedia('(pointer: coarse)').matches;
    if (reduced || coarse) return;
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
        <Suspense fallback={<div className="container-x py-24" aria-busy="true" />}>
          <Routes>
            <Route path="/" element={<Home />} />
            {Object.entries(PAGES).map(([path, C]) => <Route key={path} path={path} element={<C />} />)}
            <Route path="*" element={<NotFound title="Page not found" notFound />} />
          </Routes>
        </Suspense>
      </main>
      <Footer />
    </div>
  );
}
