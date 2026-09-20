/* Booking form constants — single source shared by the client (BookingForm.jsx,
   native `pattern` attributes) and the server (api/bookings.js, api/_lib/validate.js).
   Client code must never import from api/ directly — the Vite dev proxy shadows
   the /api path and 404s (see api/_lib/coverage.js for the same rule). */
export const WINDOWS = ['9am–12pm', '12pm–3pm', '4pm–7pm'];
export const POSTCODE_PATTERN = '\\d{4}';
export const PHONE_PATTERN = '[0-9+()\\s-]{8,15}';
export const POSTCODE_RE = new RegExp(`^${POSTCODE_PATTERN}$`);
export const PHONE_RE = new RegExp(`^${PHONE_PATTERN}$`);
export const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
