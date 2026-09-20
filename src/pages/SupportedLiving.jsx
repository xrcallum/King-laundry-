import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import EnquiryForm from '../components/EnquiryForm.jsx';

const PROMISES = [
  'A consistent operator wherever possible, so the same familiar person attends',
  'Agreed collection day and time window, communicated in advance',
  'Clear written quotes before service starts — no variable surprise charges',
  'Itemised invoices suitable for plan managers and support coordinators',
  'Operators screened before their first job, including identity and background checks',
  'Notes on handling requirements recorded and applied every visit',
];

export default function SupportedLiving() {
  return (
    <>
      <Section eyebrow="Home / Supported Living & Aged Care" title="Supported living & aged care"
        lead="Regular, reliable laundry assistance for people living independently, and for the providers and coordinators who support them.">
        <Reveal>
          <div className="card !border-ember/40 !bg-paper">
            <h3 className="font-display text-lg font-bold text-ink">Our registration status.</h3>
            <p className="mt-2 leading-relaxed">Linen Legends is not currently a registered NDIS provider. We can be engaged directly by self-managed and plan-managed participants, and by support coordinators and providers purchasing on a participant's behalf. We cannot invoice the NDIA directly for agency-managed plans. If our registration status changes, this page is updated first. Ask us before you commit and we will tell you plainly what we can and cannot do.</p>
          </div>
        </Reveal>
      </Section>

      <Section className="!bg-paper" eyebrow="What you can expect" title="How we work with participants and providers">
        <div className="grid gap-4 sm:grid-cols-2">
          {PROMISES.map((p, i) => (
            <Reveal key={p} delay={i * 60} className="h-full">
              <div className="card h-full">
                <p className="text-sm leading-relaxed">{p}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </Section>

      <Section eyebrow="Providers" title="Aged care and community providers">
        <Reveal className="max-w-2xl">
          <p className="leading-relaxed">We work with community aged care and disability support organisations that need personal laundry handled for clients in their own homes. Volume is arranged per client or per site, and billing runs through a single monthly account.</p>
        </Reveal>
      </Section>

      <Section dark eyebrow="Get in touch" title="Enquire about supported living service"
        lead="For participants, families, coordinators and providers. We will come back to you with what we can offer and what we cannot.">
        <Reveal><EnquiryForm kind="supported-living" /></Reveal>
      </Section>
    </>
  );
}
