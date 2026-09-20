import { useEffect, useRef } from 'react';
/* Masked line-by-line headline reveal. Pass lines as an array of strings. */
export default function Kinetic({ lines = [], as: Tag = 'h1', className = '', stagger = 110 }) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add('in')));
  }, []);
  return (
    <Tag ref={ref} className={`kin ${className}`}>
      {lines.map((l, i) => (
        <span className="kin-line" key={i}>
          <span style={{ transitionDelay: `${i * stagger}ms` }}>{l}</span>
        </span>
      ))}
    </Tag>
  );
}
