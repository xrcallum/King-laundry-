/* Content is duplicated for the seamless loop; the copy is aria-hidden. */
export default function Marquee({ items = [], className = '' }) {
  const row = (hidden) => (
    <div className="mq-track" aria-hidden={hidden || undefined}>
      {items.map((it, i) => (
        <span key={i} className="font-display text-sm font-semibold uppercase tracking-[0.14em] text-white/70">{it}</span>
      ))}
    </div>
  );
  return <div className={`mq flex ${className}`}>{row(false)}{row(true)}</div>;
}
