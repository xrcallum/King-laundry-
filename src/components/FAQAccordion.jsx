import { useState } from 'react';
import site from '../data/site.js';

export default function FAQAccordion({ limit }) {
  const [open, setOpen] = useState(-1);
  const faqs = limit ? site.faqs.slice(0, limit) : site.faqs;
  return (
    <div className="divide-y divide-line rounded-2xl border border-line bg-white">
      {faqs.map((f, i) => (
        <div key={i}>
          <button
            type="button" aria-expanded={open === i}
            onClick={() => setOpen(open === i ? -1 : i)}
            className="flex w-full items-center justify-between gap-4 px-6 py-5 text-left font-display font-semibold text-ink"
          >
            {f.q}
            <span aria-hidden="true" className={`text-xl text-ember transition-transform duration-300 ${open === i ? 'rotate-45' : ''}`}>+</span>
          </button>
          <div className={`grid transition-[grid-template-rows] duration-300 ${open === i ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'}`}>
            <div className="overflow-hidden"><p className="px-6 pb-5 text-[15px] leading-relaxed">{f.a}</p></div>
          </div>
        </div>
      ))}
    </div>
  );
}
