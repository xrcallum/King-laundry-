import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';
import EnquiryForm from '../components/EnquiryForm.jsx';

const SEGMENTS = [
  ['Short-stay & holiday properties', 'Bedding, towels and linen turned around between guests. Collections scheduled around your checkout windows across multiple properties.'],
  ['Salons, gyms & studios', 'Towels, robes and gowns on a standing weekly or twice-weekly collection. Consistent volume, consistent return day.'],
  ['Cafés, restaurants & clubs', 'Aprons, tea towels, table linen and uniforms. Bulk rates with monthly account billing.'],
  ['Trades & industrial', 'Heavy-soil workwear and shop rags handled separately from domestic loads. Talk to us about soil level before we quote.'],
];

export default function Business() {
  return (
    <>
      <Section eyebrow="Home / Business & Commercial" title="Business & commercial laundry"
        lead="Scheduled collections, account billing and volume pricing for businesses across South East Queensland.">
        <p className="eyebrow mb-2">Who we work with</p>
        <div className="mt-6 grid gap-5 sm:grid-cols-2">
          {SEGMENTS.map(([h, p], i) => (
            <Reveal key={h} delay={i * 80} className="h-full">
              <div className="card h-full">
                <h3 className="font-display text-lg font-bold">{h}</h3>
                <p className="mt-2 text-sm leading-relaxed">{p}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </Section>

      <Section className="!bg-paper">
        <Reveal className="mx-auto max-w-3xl">
          <div className="card !border-ember/40 !bg-paper">
            <h3 className="font-display text-lg font-bold text-ink">Note on regulated linen.</h3>
            <p className="mt-2 leading-relaxed">We do not currently hold accreditation to process clinical or healthcare linen (AS/NZS 4146). If your business requires accredited healthcare laundry, tell us at enquiry and we will say so plainly rather than quote for work we cannot legally do.</p>
          </div>
        </Reveal>
      </Section>

      <Section dark eyebrow="Get a quote" title="Request a commercial quote"
        lead="Tell us your volume and we will come back with a written quote and a proposed collection schedule.">
        <Reveal><EnquiryForm kind="business" /></Reveal>
      </Section>
    </>
  );
}
