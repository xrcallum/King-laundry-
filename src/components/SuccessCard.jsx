import CheckmarkDraw from './CheckmarkDraw.jsx';

/* Shared success-state layout for booking/enquiry/contact confirmations. */
export default function SuccessCard({ children, className = '' }) {
  return (
    <div className={`card flex gap-4 border-green-600/30 bg-green-50 ${className}`} role="status">
      <CheckmarkDraw className="mt-0.5 h-10 w-10 shrink-0 text-green-600" />
      <div className="min-w-0">{children}</div>
    </div>
  );
}
