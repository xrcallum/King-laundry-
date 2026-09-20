import { Link } from 'react-router-dom';
import Section from '../components/Section.jsx';
export default function Placeholder({ title, notFound = false }) {
  return (
    <Section eyebrow={notFound ? '404' : 'Home / ' + title} title={title}
      lead={notFound ? 'That page does not exist. The menu above has everything that does.' : 'This page is being built as part of the current milestone plan.'}>
      <Link to="/" className="btn-navy">Back to home</Link>
    </Section>
  );
}
