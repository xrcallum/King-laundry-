#!/usr/bin/env python3
"""Phase C — App. Dossier v2, Part 14.

D1  tab bar: SVG icons landed in Phase A; this adds the red pill active state
D5  stepper: minus and plus at opposite edges with the value floating
D6  verb first, arrow after, on every primary button
D10 wizard card header wraps badly on a phone
D19 icon-only controls with no accessible name
plus the installable web app, the status timeline and reduced-motion-safe entry.
"""
import re
import sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
log = []


def note(x):
    log.append(x)


# =====================================================================
# D19 — every icon-only control gets a name
# =====================================================================
src, n = re.subn(r'<button class="ap-back" id="bkBack">',
                 '<button class="ap-back" id="bkBack" aria-label="Back a step">', src)
src, n2 = re.subn(r'<button class="ap-back" onclick="location\.hash=\'#/(\w+)\'">',
                  lambda m: '<button class="ap-back" aria-label="Back to %s" onclick="location.hash=\'#/%s\'">'
                            % (("settings" if m.group(1) == "account" else m.group(1)), m.group(1)), src)
src, n3 = re.subn(r'<button type="button" data-bstep="(\w),(-?1)">',
                  lambda m: '<button type="button" data-bstep="%s,%s" aria-label="%s %s">'
                            % (m.group(1), m.group(2),
                               "Decrease" if m.group(2) == "-1" else "Increase",
                               "loads" if m.group(1) == "a" else "ironed items"), src)
note("accessible names on %d icon-only controls" % (n + n2 + n3))

# The plus buttons still carry a bare "+" glyph; make them icons with names.
src, n4 = re.subn(r'<button type="button" data-bstep="(\w),1"([^>]*)>\+</button>',
                  lambda m: '<button type="button" data-bstep="%s,1"%s>'
                            '<svg class="ic" aria-hidden="true"><use href="#ic-plus"/></svg></button>'
                            % (m.group(1), m.group(2)), src)
src, n5 = re.subn(r'<button type="button" data-step="(\w),1">\+</button>',
                  lambda m: '<button type="button" data-step="%s,1" aria-label="Increase">'
                            '<svg class="ic" aria-hidden="true"><use href="#ic-plus"/></svg></button>'
                            % m.group(1), src)
src, n6 = re.subn(r'<button type="button" data-step="(\w),-1" aria-label="Decrease">',
                  r'<button type="button" data-step="\1,-1" aria-label="Decrease">', src)
note("plus controls converted to icons (%d)" % (n4 + n5))

# The sprite itself should be out of the accessibility tree entirely.
src = src.replace('<svg class="ic-sprite" aria-hidden="true" focusable="false"',
                  '<svg class="ic-sprite" aria-hidden="true" focusable="false" role="presentation"')

# =====================================================================
# D6 — verb first on the remaining primary buttons
# =====================================================================
before = src
src = re.sub(r'<svg class="ic ic-inl ic-aft"[^>]*><use href="#ic-arrow-right"/></svg>\s*([A-Za-z][\w\' ]{2,28})(</)',
             lambda m: m.group(1).strip() + '<svg class="ic ic-inl ic-aft" aria-hidden="true">'
                       '<use href="#ic-arrow-right"/></svg>' + m.group(2), src)
if src != before:
    note("arrow moved after the verb")

# =====================================================================
# PWA — the "no app to download" promise, made literal
# =====================================================================
MANIFEST = (
    '{"name":"Laundrylegends","short_name":"Laundrylegends","start_url":"#/app","scope":"./",'
    '"display":"standalone","background_color":"%23FFFFFF","theme_color":"%2312245C",'
    '"description":"Laundry collected, washed and returned across Brisbane, Logan and South East Queensland.",'
    '"icons":[{"src":"ICON192","sizes":"192x192","type":"image/svg%2Bxml","purpose":"any maskable"}]}'
)
CROWN = (
    "data:image/svg%2Bxml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E"
    "%3Crect width='36' height='36' fill='%2312245C'/%3E"
    "%3Cpath d='M7 25h22l-2.8-10.5L22 20l-4-9-4 9-4.2-5.5z' fill='%23CC2228' stroke='%23fff' "
    "stroke-width='1.1' stroke-linejoin='round'/%3E"
    "%3Ccircle cx='7' cy='14.5' r='1.9' fill='%23fff'/%3E%3Ccircle cx='18' cy='11' r='1.9' fill='%23fff'/%3E"
    "%3Ccircle cx='29' cy='14.5' r='1.9' fill='%23fff'/%3E%3C/svg%3E"
)
manifest = MANIFEST.replace("ICON192", CROWN)
src = src.replace('<meta name="theme-color" content="#12245C">',
                  '<meta name="theme-color" content="#12245C">\n'
                  '<link rel="icon" href="' + CROWN + '">\n'
                  '<link rel="apple-touch-icon" href="' + CROWN + '">\n'
                  '<meta name="apple-mobile-web-app-capable" content="yes">\n'
                  '<meta name="apple-mobile-web-app-title" content="Laundrylegends">\n'
                  '<link rel="manifest" href="data:application/manifest+json,' + manifest + '">')
note("web app manifest and icons")

INSTALL = """
/* ---------- INSTALL PROMPT ----------
   Web-first is the promise, so the app is installable without an app store.
   Offered once, after a booking, and never again if dismissed. */
let LK_INSTALL = null;
window.addEventListener('beforeinstallprompt', e => { e.preventDefault(); LK_INSTALL = e; });
function offerInstall(){
  try {
    if (!LK_INSTALL || localStorage.getItem('lk-install') === 'done') return;
  } catch(e){ if (!LK_INSTALL) return; }
  const bar = document.getElementById('lkInstall');
  if (!bar) return;
  bar.classList.add('show');
  bar.querySelector('[data-install]').onclick = async () => {
    bar.classList.remove('show');
    try { localStorage.setItem('lk-install','done'); } catch(e){}
    LK_INSTALL.prompt(); LK_INSTALL = null;
  };
  bar.querySelector('[data-install-no]').onclick = () => {
    bar.classList.remove('show');
    try { localStorage.setItem('lk-install','done'); } catch(e){}
  };
}
"""
src = src.replace("function wireWizard(){", INSTALL.strip("\n") + "\n\nfunction wireWizard(){", 1)
src = src.replace("      renderBookings(); renderMessages(); renderHome(); renderTabs('book');",
                  "      renderBookings(); renderMessages(); renderHome(); renderTabs('book');\n      offerInstall();")
note("install offer after the first booking")

INSTALL_HTML = """<div id="lkInstall" role="dialog" aria-live="polite" aria-label="Add Laundrylegends to your home screen">
  <div><strong>Add Laundrylegends to your home screen</strong><small>One tap to your bookings. No app store, no download.</small></div>
  <div class="lk-inst-acts">
    <button class="btn btn-out" data-install-no>Not now</button>
    <button class="btn btn-nv" data-install>Add</button>
  </div>
</div>
"""
src = src.replace('<div id="sheet">', INSTALL_HTML + '<div id="sheet">', 1)

# =====================================================================
# Status timeline on the customer's booking card
# =====================================================================
TIMELINE_JS = """
/* A booking is a promise with stages. Show where it is, not just a word. */
const BK_STAGES = [
  ['requested','Booked'], ['assigned','Assigned'], ['collected','Collected'],
  ['invoiced','Washed'], ['complete','Returned']
];
function bkTimeline(b){
  if (b.status === 'cancelled') return '';
  const at = BK_STAGES.findIndex(s => s[0] === b.status);
  const done = at < 0 ? 0 : at;
  return '<ol class="bk-tl" aria-label="Progress of this collection">' + BK_STAGES.map(([k,label],i) =>
    '<li class="' + (i < done ? 'done' : i === done ? 'now' : '') + '">'
    + '<span class="bk-tl-d" aria-hidden="true"></span>'
    + '<span class="bk-tl-l">' + label + '</span>'
    + (i === done ? '<span class="sr-only"> — current stage</span>' : '')
    + '</li>').join('') + '</ol>';
}
"""
src = src.replace("function richBookingCard(b){", TIMELINE_JS.strip("\n") + "\n\nfunction richBookingCard(b){", 1)

m = re.search(r'(function richBookingCard\(b\)\{.*?return `<div class="bkc[^`]*?)(<div class="bkc-acts">)', src, re.S)
if m:
    src = src[:m.end(1)] + "${bkTimeline(b)}" + src[m.end(1):]
    note("status timeline on the booking card")
else:
    # fall back: inject before the actions row wherever it is built
    m2 = re.search(r'(<div class="bkc-b">)', src)
    if m2:
        src = src[:m2.end(1)] + "${bkTimeline(b)}" + src[m2.end(1):]
        note("status timeline on the booking card (body)")

# =====================================================================
# CSS: stepper, tab pill, wizard header, timeline, install bar, motion
# =====================================================================
CSS = """
/* ---------- PHASE C ---------- */
/* D5 — the stepper is one control, not three things at opposite edges. */
.stepper{max-width:150px;justify-content:space-between}
.stepper span{min-width:2.4ch;flex:0 1 auto;font-size:var(--fs-body);font-variant-numeric:tabular-nums}
.stepper button{padding:.5rem .7rem;display:flex;align-items:center;justify-content:center}
.stepper button .ic{width:18px;height:18px}

/* D1 — the active tab wears a pill, not just red text. */
.tab{position:relative}
.tab i{filter:none;color:var(--mute);width:26px;height:26px;display:flex;align-items:center;justify-content:center}
.tab i .ic,.tab .ic{width:24px;height:24px}
.tab.on i{color:var(--red)}
.tab.on i::before{content:'';position:absolute;top:.38rem;left:50%;transform:translateX(-50%);
  width:46px;height:28px;border-radius:var(--r-pill);background:var(--red-w);z-index:-1}
.tab.on s{color:var(--red)}

/* D10 — the wizard card header stacks rather than squeezing. */
@media(max-width:480px){
  .ap-card-h{flex-wrap:wrap;row-gap:.2rem}
  .ap-card-h span{flex-basis:100%}
}

/* Status timeline. */
.bk-tl{list-style:none;display:flex;margin:.9rem 0 .2rem;padding:0;counter-reset:none}
.bk-tl li{flex:1;position:relative;text-align:center;font-size:var(--fs-badge);
  font-family:var(--fd);font-weight:700;color:var(--mute);letter-spacing:var(--track-micro)}
.bk-tl li::before{content:'';position:absolute;top:5px;left:-50%;width:100%;height:2px;background:var(--line)}
.bk-tl li:first-child::before{display:none}
.bk-tl li.done::before,.bk-tl li.now::before{background:var(--navy)}
.bk-tl-d{display:block;width:12px;height:12px;margin:0 auto .34rem;border-radius:50%;
  background:var(--white);border:2px solid var(--line);position:relative;z-index:1}
.bk-tl li.done .bk-tl-d{background:var(--navy);border-color:var(--navy)}
.bk-tl li.now .bk-tl-d{background:var(--red);border-color:var(--red);box-shadow:0 0 0 3px var(--red-w)}
.bk-tl li.done,.bk-tl li.now{color:var(--navy)}
.bk-tl-l{display:block}

/* Install offer. */
#lkInstall{position:fixed;left:0;right:0;bottom:0;z-index:180;display:none;gap:1rem;
  align-items:center;justify-content:space-between;flex-wrap:wrap;
  background:var(--white);border-top:1px solid var(--line);box-shadow:var(--sh2);
  padding:1rem 1.15rem calc(1rem + env(safe-area-inset-bottom))}
#lkInstall.show{display:flex}
#lkInstall strong{display:block;font-family:var(--fd);font-size:var(--fs-body);color:var(--ink)}
#lkInstall small{display:block;font-size:var(--fs-micro);color:var(--mute);margin-top:.15rem}
.lk-inst-acts{display:flex;gap:.55rem;flex:none}

/* Screen-reader-only text. */
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0 0 0 0);white-space:nowrap;border:0}

/* A visible focus ring everywhere, not only where someone remembered. */
:focus-visible{outline:2px solid var(--navy);outline-offset:2px;border-radius:2px}
.sec-navy :focus-visible,#foot :focus-visible,#mob :focus-visible,#nav :focus-visible{outline-color:var(--white)}

/* Entry motion, off by default for anyone who asks for less. */
@media (prefers-reduced-motion: no-preference){
  .reveal{opacity:0;transform:translateY(12px)}
  .reveal.in{opacity:1;transform:none;transition:opacity .32s ease-out,transform .32s ease-out}
}
"""
src = src.replace("</style>", CSS + "</style>", 1)
note("phase C styles")

# =====================================================================
# Scroll reveal, reduced-motion safe
# =====================================================================
REVEAL = """
/* ---------- SCROLL REVEAL ----------
   Runs only where the viewer has not asked for reduced motion, and only once
   per element. Everything is visible without it. */
(() => {
  if (!window.matchMedia || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
})();
function wireReveal(){
  if (!window.IntersectionObserver) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const targets = document.querySelectorAll('.page.live .sec > .wrap > *, .page.live .trust-c, .page.live .card');
  if (!targets.length) return;
  const io = new IntersectionObserver(es => {
    es.forEach(e => { if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
  targets.forEach(t => { t.classList.add('reveal'); io.observe(t); });
}
"""
src = src.replace("function route(){", REVEAL.strip("\n") + "\n\nfunction route(){", 1)
src = src.replace("  setTitle(id);\n  if (id === 'dash') loadDash();",
                  "  setTitle(id);\n  try { wireReveal(); } catch(e){}\n  if (id === 'dash') loadDash();")
note("scroll reveal, reduced-motion safe")

open(path, "w", encoding="utf-8").write(src)
print("Phase C applied:")
for l in log:
    print("  -", l)
