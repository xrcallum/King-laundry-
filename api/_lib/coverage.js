/* Coverage of record — lifted verbatim from site/laundrylegends-site.html LIVE_PC / SOON_PC.
   D1(a): 4000 stays "opening" until an operator is confirmed. */
export const LIVE_PC = {
  4131: 'Meadowbrook', 4127: 'Springwood', 4128: 'Shailer Park', 4129: 'Loganholme',
  4130: 'Cornubia', 4132: 'Marsden', 4133: 'Waterford', 4207: 'Beenleigh',
  4118: 'Browns Plains', 4119: 'Kuraby', 4109: 'Sunnybank', 4122: 'Mansfield',
  4121: 'Holland Park', 4120: 'Greenslopes', 4151: 'Coorparoo', 4152: 'Camp Hill',
};
export const SOON_PC = {
  4000: 'Brisbane CBD', 4101: 'South Brisbane', 4102: 'Woolloongabba', 4169: 'Kangaroo Point',
  4170: 'Morningside', 4171: 'Balmoral', 4030: 'Windsor', 4031: 'Kedron', 4032: 'Chermside',
  4034: 'Aspley', 4066: 'Toowong', 4068: 'Indooroopilly', 4508: 'North Lakes', 4509: 'Mango Hill',
};

export function check(postcode) {
  const pc = String(postcode || '').trim();
  if (!/^\d{4}$/.test(pc)) return { ok: false, error: 'bad_postcode', message: 'Please enter a valid four-digit Australian postcode.' };
  if (LIVE_PC[pc]) return { ok: true, postcode: pc, status: 'active', suburb: LIVE_PC[pc], message: `We are running collections in ${LIVE_PC[pc]} (${pc}).` };
  if (SOON_PC[pc]) return { ok: true, postcode: pc, status: 'opening', suburb: SOON_PC[pc], message: `${SOON_PC[pc]} (${pc}) is next on our list — we are recruiting an operator for that round now.` };
  return { ok: true, postcode: pc, status: 'waitlist', message: `We are not in ${pc} yet. Register your interest — we open new rounds where registered demand is highest.` };
}
