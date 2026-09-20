/* Server-side booking field validation. Regex patterns come from
   src/lib/bookingOptions.js — the shared source also used by the client's
   native `pattern` attributes, so the two can never drift apart. */
import { POSTCODE_RE, PHONE_RE, EMAIL_RE } from '../../src/lib/bookingOptions.js';

export function validateBookingFields(b, windows) {
  if (!POSTCODE_RE.test(String(b.postcode || ''))) return { ok: false, error: 'bad_postcode', message: 'Please enter a valid four-digit Australian postcode.' };
  if (!EMAIL_RE.test(String(b.email || ''))) return { ok: false, error: 'bad_email', message: 'Please enter a valid email address.' };
  if (!PHONE_RE.test(String(b.phone || ''))) return { ok: false, error: 'bad_phone', message: 'Please enter a valid phone number.' };
  if (!windows.includes(b.window)) return { ok: false, error: 'bad_window', message: 'Please choose a valid collection window.' };
  const day = new Date(`${b.date}T00:00:00`);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  if (Number.isNaN(day.getTime()) || day < today) return { ok: false, error: 'bad_date', message: 'Collection day must be today or later.' };
  return { ok: true };
}
