import { useState } from 'react';
import { Link } from 'react-router-dom';
import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import FAQAccordion from '../components/FAQAccordion.jsx';
import site from '../data/site.js';

export default function Faq() {
  const [filter, setFilter] = useState('');
  const [open, setOpen] = useState(-1);

  const query = filter.trim().toLowerCase();
  const isFiltering = query.length > 0;
  const filtered = isFiltering
    ? site.faqs.filter(
        (f) => f.q.toLowerCase().includes(query) || f.a.toLowerCase().includes(query)
      )
    : [];

  return (
    <Section
      eyebrow="Home / FAQ"
      title="Frequently asked questions"
      lead="If your question is not answered here, contact us and we will answer it — and add it to this page."
    >
      <Reveal className="mx-auto max-w-3xl">
        <input
          type="text"
          className="input max-w-md"
          placeholder="Filter questions…"
          aria-label="Filter questions"
          value={filter}
          onChange={(e) => {
            setFilter(e.target.value);
            setOpen(-1);
          }}
        />

        <div className="mt-6">
          {!isFiltering ? (
            <FAQAccordion />
          ) : filtered.length === 0 ? (
            <p className="text-[15px] text-body">
              No questions match — <Link to="/contact" className="font-semibold text-navy underline underline-offset-4">contact us and we will answer it</Link>.
            </p>
          ) : (
            <div className="divide-y divide-line rounded-2xl border border-line bg-white">
              {filtered.map((f, i) => (
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
          )}
        </div>

        <p className="mt-8 text-[15px] text-body">
          Still have a question? <Link to="/contact" className="font-semibold text-navy underline underline-offset-4">Get in touch</Link>.
        </p>
      </Reveal>
    </Section>
  );
}
