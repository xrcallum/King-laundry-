import { Link } from 'react-router-dom';
import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import BookingForm from '../components/BookingForm.jsx';

export default function Book() {
  return (
    <>
      <Section
        eyebrow="Home / Book a collection"
        title="Book a collection."
        lead="Two minutes. Price confirmed after weighing, before any work starts."
      >
        <BookingForm />
      </Section>

      <Section className="!bg-paper">
        <Reveal>
          <div className="card mx-auto max-w-2xl">
            <p className="text-xs font-semibold uppercase tracking-wide text-body/70">Before you book</p>
            <p className="mt-2 text-sm leading-relaxed text-body">
              We are in pre-launch. A booking made now is a registration of interest, not a confirmed contract — our{' '}
              <Link to="/privacy" className="text-navy underline underline-offset-2 hover:text-navy-deep">privacy policy</Link>{' '}
              and{' '}
              <Link to="/terms" className="text-navy underline underline-offset-2 hover:text-navy-deep">terms of service</Link>{' '}
              are still drafts for legal review and are not yet in force.
            </p>
          </div>
        </Reveal>
      </Section>
    </>
  );
}
