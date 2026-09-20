async function req(path, opts) {
  const r = await fetch(path, opts);
  const data = await r.json().catch(() => ({ ok: false, error: 'bad_response', message: 'Unexpected server response.' }));
  return data;
}
const post = (path, body) => req(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });

export const getEstimate = (input) => post('/api/estimate', input);
export const checkCoverage = (postcode) => req(`/api/coverage/check?postcode=${encodeURIComponent(postcode)}`);
export const joinWaitlist = (input) => post('/api/waitlist', input);
export const createBooking = (input) => post('/api/bookings', input);
export const getBooking = (id) => req(`/api/bookings?id=${encodeURIComponent(id)}`);
export const sendEnquiry = (input) => post('/api/enquiries', input);
export const sendContact = (input) => post('/api/contact', input);
