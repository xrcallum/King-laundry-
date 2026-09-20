import { Link } from 'react-router-dom';
import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import FAQAccordion from '../components/FAQAccordion.jsx';

export default function Faq() {
  return (
    <Section
      eyebrow="Home / FAQ"
      title="Frequently asked questions"
      lead="If your question is not answered here, contact us and we will answer it — and add it to this page."
    >
      <Reveal className="mx-auto max-w-3xl">
        <FAQAccordion />
        <p className="mt-8 text-[15px] text-body">
          Still have a question? <Link to="/contact" className="font-semibold text-navy underline underline-offset-4">Get in touch</Link>.
        </p>
      </Reveal>
    </Section>
  );
}
