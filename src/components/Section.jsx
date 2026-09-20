import Reveal from './Reveal.jsx';
export default function Section({ id, eyebrow, title, lead, dark = false, children, className = '' }) {
  return (
    <section id={id} className={`${dark ? 'bg-navy text-white' : 'bg-white'} py-16 sm:py-24 ${className}`}>
      <div className="container-x">
        {(eyebrow || title) && (
          <Reveal className="mb-10 max-w-2xl">
            {eyebrow && <p className="eyebrow mb-2">{eyebrow}</p>}
            {title && <h2 className={`text-3xl font-extrabold sm:text-4xl ${dark ? 'text-white' : ''}`}>{title}</h2>}
            {lead && <p className={`mt-3 text-lg leading-relaxed ${dark ? 'text-white/80' : ''}`}>{lead}</p>}
          </Reveal>
        )}
        {children}
      </div>
    </section>
  );
}
