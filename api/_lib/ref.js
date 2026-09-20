/* Order reference — same shape as the site of record: LL- + 6 uppercase base-36 chars. */
export const REF = () =>
  'LL-' + Date.now().toString(36).slice(-4).toUpperCase() + Math.random().toString(36).slice(2, 4).toUpperCase();
