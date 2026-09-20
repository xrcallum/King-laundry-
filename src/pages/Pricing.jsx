import { Link } from 'react-router-dom';
import Section from '../components/Section.jsx';
import Reveal from '../components/Reveal.jsx';

const GROUPS = [
  {
    name: 'Washing',
    unit: 'Per load',
    rows: [
      ['Wash & fold — per load', 'Approximately 5 kg', '$32'],
      ['Lights & darks separated', 'Washed separately — charged as two loads', '$64'],
      ['Collection & return', 'One flat fee, both directions', '$13.50'],
      ['Eco / fragrance-free detergent', 'Optional add-on per load', '$3.50'],
      ['Minimum order', 'One-off bookings only', '$73.50'],
    ],
  },
  {
    name: 'Blankets, Rugs & Sheets',
    unit: 'Per item — large-format items only, not charged by weight',
    rows: [
      ['Sheet set', 'Per set, any bed size', '$24'],
      ['Blanket or quilt cover', 'Single or double', '$32'],
      ['Rug or floor mat', 'Subject to size', '$42'],
    ],
  },
  {
    name: 'Dry Cleaning',
    unit: 'Per item',
    rows: [
      ['Dress or skirt', 'From — final price depends on fabric', '$16.50'],
      ['Suit jacket or blazer', '', '$18.50'],
      ['Two-piece suit', '', '$32'],
    ],
  },
  {
    name: 'Bulky & Household',
    unit: 'Per item',
    rows: [
      ['Doona — single or double', '', '$45'],
      ['Doona — queen or king', '', '$75'],
      ['Curtains', 'Per panel, subject to size', '$38'],
      ['Mattress protector', '', '$45'],
      ['Pet bedding', 'Processed separately from household loads', 'Quoted on inspection'],
      ['Specialist items', 'Leather, bridal, heavily beaded', 'Quoted individually'],
    ],
  },
];

const STEPS = [
  'Loads. One load is approximately 5 kg. Lights and darks are washed separately and count as two loads.',
  'Large linen. Blankets, rugs and sheet sets only — charged per item, not by weight.',
  'Delivery. One flat fee covering both collection and return.',
  'Minimum order. Applies to one-off bookings. Legends Club members are not subject to it.',
  'Confirmation. Your operator weighs and counts at collection and confirms the final price before starting.',
];

function PriceTable({ group }) {
  return (
    <Reveal className="h-full">
      <div className="card h-full !p-0 overflow-hidden">
        <div className="border-b border-line p-6 pb-4">
          <h3 className="font-display text-lg font-bold">{group.name}</h3>
          <p className="text-sm text-body">{group.unit}</p>
        </div>
        <table className="w-full text-sm">
          <tbody>
            {group.rows.map(([item, note, price]) => (
              <tr key={item} className="border-b border-line last:border-0">
                <td className="px-6 py-3 align-top">
                  <p className="font-medium text-ink">{item}</p>
                  {note && <p className="mt-0.5 text-xs text-body">{note}</p>}
                </td>
                <td className="whitespace-nowrap px-6 py-3 text-right align-top font-display font-bold text-ink">{price}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Reveal>
  );
}

export default function Pricing() {
  return (
    <>
      <Section
        eyebrow="Home / Pricing"
        title="Pricing"
        lead="All prices include GST and are shown in Australian dollars. Collection and return are included in the delivery fee. No call-out charge, no fuel levy."
      >
        <div className="grid gap-5 lg:grid-cols-2">
          {GROUPS.map((g) => (
            <PriceTable key={g.name} group={g} />
          ))}
        </div>
      </Section>

      <Section className="!bg-paper">
        <Reveal>
          <div className="card">
            <h3 className="font-display text-lg font-bold">Pricing under review</h3>
            <p className="mt-2 leading-relaxed">
              The figures above are our launch pricing and are subject to change as our operator network and delivery
              costs settle. Any price change is published here before it takes effect, and Legends Club members are
              notified in writing before their next billing date.
            </p>
          </div>
        </Reveal>

        <Reveal delay={100}>
          <div className="mt-5 card">
            <h3 className="font-display text-lg font-bold">How your price is calculated</h3>
            <ol className="mt-3 space-y-2 text-sm leading-relaxed">
              {STEPS.map((s, i) => (
                <li key={s} className="flex gap-3">
                  <span aria-hidden="true" className="font-display font-bold text-ember">{i + 1}.</span>
                  <span>{s}</span>
                </li>
              ))}
            </ol>
          </div>
        </Reveal>

        <Reveal delay={200}>
          <p className="mx-auto mt-8 max-w-3xl text-center text-sm text-body">
            What affects your final price: weight, number of separated loads, large linen items, bulky items, and your
            distance from the nearest active operator. Your operator confirms the final figure after weighing and
            before any work begins.
          </p>
        </Reveal>
      </Section>

      <section className="bg-ember py-16 text-center text-white sm:py-20">
        <Reveal className="container-x">
          <h2 className="text-3xl font-extrabold text-white sm:text-4xl">Ready to book?</h2>
          <p className="mx-auto mt-3 max-w-xl text-white/85">
            Published pricing, price confirmed after weighing, collection and return included.
          </p>
          <Link to="/book" className="btn mt-6 bg-white font-bold text-ember hover:bg-white/90">Book a collection</Link>
        </Reveal>
      </section>
    </>
  );
}
