import { Suspense, lazy, useEffect } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import Lenis from 'lenis';
import Navbar from './components/Navbar.jsx';
import Footer from './components/Footer.jsx';
import Home from './pages/Home.jsx';
import NotFound from './pages/NotFound.jsx';
import Seo from './components/Seo.jsx';

const P = (n) => lazy(() => import(`./pages/${n}.jsx`));
const PAGES = {
  '/book': P('Book'), '/services': P('Services'), '/pricing': P('Pricing'),
  '/legends-club': P('LegendsClub'), '/coverage': P('Coverage'), '/business': P('Business'),
  '/supported-living': P('SupportedLiving'), '/operators': P('Operators'), '/about': P('About'),
  '/guarantee': P('Guarantee'), '/faq': P('Faq'), '/contact': P('Contact'),
  '/privacy': P('Privacy'), '/terms': P('Terms'), '/account': P('Account'), '/messages': P('Messages'),
};
const TITLES = {
  '/': null, '/book': 'Book a collection', '/services': 'Our services', '/pricing': 'Pricing',
  '/legends-club': 'Legends Club', '/coverage': 'Coverage & suburbs', '/business': 'Business & commercial laundry',
  '/supported-living': 'Supported living & aged care', '/operators': 'Become an operator', '/about': 'About us',
  '/guarantee': 'Our service guarantee', '/faq': 'Frequently asked questions', '/contact': 'Contact us',
  '/privacy': 'Privacy policy', '/terms': 'Terms of service', '/account': 'My account', '/messages': 'Messages',
};
function RouteSeo() {
  const { pathname } = useLocation();
  return <Seo title={TITLES[pathname] || TITLES['/']} path={pathname === '/' ? '' : pathname} />;
}

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
      <RouteSeo />
      <Navbar />
      <main id="main">
        <Suspense fallback={<div className="container-x py-24" aria-busy="true" />}>
          <Routes>
            <Route path="/" element={<Home />} />
            {Object.entries(PAGES).map(([path, C]) => <Route key={path} path={path} element={<C />} />)}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Suspense>
      </main>
      <Footer />
    </div>
  );
}
