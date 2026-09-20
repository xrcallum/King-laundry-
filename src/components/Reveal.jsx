import { useEffect, useRef } from 'react';
/* variant: fade | rise | wipe-x | wipe-y
   The observed wrapper stays unclipped (Chromium reports zero intersection for a
   fully clip-pathed target); the variant styles live on the inner box. */
export default function Reveal({ as: Tag = 'div', variant = 'rise', delay = 0, className = '', children, ...rest }) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { el.classList.add('in'); return; }
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) { el.classList.add('in'); io.disconnect(); }
    }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });
    io.observe(el);
    return () => io.disconnect();
  }, []);
  return (
    <Tag ref={ref} className={`rv ${className}`} {...rest}>
      <div className={`rv-box rv-${variant}`} style={delay ? { transitionDelay: `${delay}ms` } : undefined}>
        {children}
      </div>
    </Tag>
  );
}
