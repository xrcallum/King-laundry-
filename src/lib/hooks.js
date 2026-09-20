import { useEffect, useRef } from 'react';
const fine = () => window.matchMedia('(pointer: fine)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const reduced = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* Scroll parallax — moves an element at a fraction of scroll speed. Hero decoration only. */
export function useParallax(speed = 0.15) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el || reduced()) return;
    let raf = null;
    const apply = () => { el.style.transform = `translate3d(0, ${window.scrollY * speed}px, 0)`; raf = null; };
    const onScroll = () => { if (raf === null) raf = requestAnimationFrame(apply); };
    apply();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => { window.removeEventListener('scroll', onScroll); if (raf) cancelAnimationFrame(raf); };
  }, [speed]);
  return ref;
}

/* Magnetic pull toward the cursor — primary CTAs only, 12px max. */
export function useMagnetic(strength = 12) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el || !fine()) return;
    const move = (e) => {
      const r = el.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width - 0.5) * 2;
      const y = ((e.clientY - r.top) / r.height - 0.5) * 2;
      el.style.transform = `translate(${x * strength}px, ${y * strength}px)`;
    };
    const leave = () => { el.style.transform = ''; };
    el.addEventListener('pointermove', move);
    el.addEventListener('pointerleave', leave);
    return () => { el.removeEventListener('pointermove', move); el.removeEventListener('pointerleave', leave); };
  }, [strength]);
  return ref;
}

/* 3D tilt on hover — club/plan cards, ±6 degrees. */
export function useTilt(max = 6) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el || !fine()) return;
    el.style.transformStyle = 'preserve-3d';
    el.style.transition = 'transform .25s ease-out';
    const move = (e) => {
      const r = el.getBoundingClientRect();
      const rx = ((e.clientY - r.top) / r.height - 0.5) * -2 * max;
      const ry = ((e.clientX - r.left) / r.width - 0.5) * 2 * max;
      el.style.transform = `perspective(1200px) rotateX(${rx}deg) rotateY(${ry}deg)`;
    };
    const leave = () => { el.style.transform = ''; };
    el.addEventListener('pointermove', move);
    el.addEventListener('pointerleave', leave);
    return () => { el.removeEventListener('pointermove', move); el.removeEventListener('pointerleave', leave); };
  }, [max]);
  return ref;
}
