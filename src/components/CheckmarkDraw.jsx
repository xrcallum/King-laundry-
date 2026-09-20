/* Animated success indicator — circle then check stroke-draw on mount.
   Respects prefers-reduced-motion via the global rule in src/index.css. */
export default function CheckmarkDraw({ className = '' }) {
  return (
    <svg viewBox="0 0 52 52" className={`checkmark ${className}`} aria-hidden="true">
      <circle className="checkmark-circle" cx="26" cy="26" r="25" fill="none" />
      <path className="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8" />
    </svg>
  );
}
