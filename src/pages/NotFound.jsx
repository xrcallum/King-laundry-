import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <section className="flex min-h-[60vh] flex-col items-center justify-center bg-navy px-6 text-center text-white">
      <p className="font-display text-[clamp(5rem,15vw,10rem)] font-bold leading-none">404</p>
      <p className="mt-4 max-w-md text-[15px] text-white/80">
        That page does not exist. Everything that does is in the menu.
      </p>
      <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
        <Link to="/" className="btn bg-white text-navy font-bold">
          Back home
        </Link>
        <Link to="/book" className="btn-primary">
          Book now
        </Link>
      </div>
    </section>
  );
}
