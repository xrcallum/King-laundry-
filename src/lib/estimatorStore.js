/* Tiny cross-page store so /book can pre-fill from the home estimator. */
const KEY = 'll-estimate';
export function saveEstimate(input, result) {
  try { sessionStorage.setItem(KEY, JSON.stringify({ input, result })); } catch { /* private mode */ }
}
export function loadEstimate() {
  try { return JSON.parse(sessionStorage.getItem(KEY) || 'null'); } catch { return null; }
}
