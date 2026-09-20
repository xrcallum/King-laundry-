/* Local dev mount for the Vercel-style api/ handlers, so curl tests run without a deploy. */
import express from 'express';
import estimate from '../api/estimate.js';
import coverageCheck from '../api/coverage/check.js';
import waitlist from '../api/waitlist.js';
import bookings from '../api/bookings.js';
import enquiries from '../api/enquiries.js';
import contact from '../api/contact.js';

const app = express();
app.use(express.json());
const wrap = (h) => (req, res) => Promise.resolve(h(req, res)).catch((e) => {
  console.error(e);
  res.status(500).json({ ok: false, error: 'internal', message: 'Something went wrong on our side.' });
});
app.post('/api/estimate', wrap(estimate));
app.get('/api/coverage/check', wrap(coverageCheck));
app.post('/api/waitlist', wrap(waitlist));
app.post('/api/bookings', wrap(bookings));
app.get('/api/bookings', wrap(bookings));
app.post('/api/enquiries', wrap(enquiries));
app.post('/api/contact', wrap(contact));
const port = process.env.PORT || 8787;
app.listen(port, () => console.log(`api dev server on :${port}`));
