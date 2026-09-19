#!/usr/bin/env python3
"""Phase B — Marketing. Dossier v2, Part 14.

D8  coverage Check button reads as a page CTA
D11 mobile menu: 15 flat items, no groups, no CTA
D12 footer: 26 links, about 1,400px tall on a phone
D14 nav red CTA outweighs the logo
D21 no Open Graph tags, no structured data, one title for 34 pages
plus the Legends Club savings qualifier, the warm paper surface, and the
"what a load looks like" strip the estimator needs.
"""
import json
import re
import sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
log = []


def sub1(old, new, label):
    global src
    assert old in src, "not found: " + label
    src = src.replace(old, new, 1)
    log.append(label)


# =====================================================================
# 1. Nav: six items to four (D-08). Coverage and Operators keep their
#    places in the footer and the mobile menu.
# =====================================================================
src, n = re.subn(r'(<ul class="nav-links">)(.*?)(</ul>)',
    lambda m: m.group(1) + """
    <li><a href="#/services" data-nav="services">Services</a></li>
    <li><a href="#/pricing" data-nav="pricing">Pricing</a></li>
    <li><a href="#/club" data-nav="club">Legends&nbsp;Club</a></li>
    <li><a href="#/business" data-nav="business">For&nbsp;business</a></li>
  """ + m.group(3), src, count=1, flags=re.S)
assert n == 1, "nav-links not found"
log.append("nav reduced to four items")

# =====================================================================
# 2. Mobile menu: one CTA, five primary, the rest behind More (D11)
# =====================================================================
NEW_MOB = """  <a href="#/book" class="mob-cta">Book a collection<svg class="ic ic-inl ic-aft" aria-hidden="true"><use href="#ic-arrow-right"/></svg></a>
  <a href="#/services">Services</a>
  <a href="#/pricing">Pricing</a>
  <a href="#/club">Legends Club</a>
  <a href="#/coverage">Coverage &amp; suburbs</a>
  <a href="#/app">My account &amp; bookings</a>
  <button class="mob-more" id="mobMore" aria-expanded="false" aria-controls="mobRest">More<svg class="ic ic-inl ic-aft" aria-hidden="true"><use href="#ic-chevron-down"/></svg></button>
  <div id="mobRest" hidden>
  <a href="#/business">Business &amp; commercial</a>
  <a href="#/support">Supported living &amp; aged care</a>
  <a href="#/operators">Become an operator</a>
  <a href="#/about">About us</a>
  <a href="#/guarantee">Service guarantee</a>
  <a href="#/faq">FAQ</a>
  <a href="#/contact">Contact</a>
  </div>
"""
src, n = re.subn(r'(</button>\n)(\s*<a href="#/">Home</a>.*?)(\s*<a href="#/ops" id="mobOps")',
                 lambda m: m.group(1) + NEW_MOB + m.group(3), src, count=1, flags=re.S)
assert n == 1, "mobile menu block not found"
log.append("mobile menu grouped behind More, with one CTA")

# =====================================================================
# 3. Footer: 26 links to 11 in two groups (D12)
# =====================================================================
OLD_FOOT = re.search(r'<div><h4>SERVICES</h4>.*?SUPPORT &amp; LEGAL.*?</ul></div>', src, re.S)
assert OLD_FOOT, "footer columns not found"
NEW_FOOT = """<div><h4>SERVICE</h4><ul>
<li><a href="#/services">Services</a></li><li><a href="#/pricing">Pricing</a></li>
<li><a href="#/club">Legends Club</a></li><li><a href="#/coverage">Coverage &amp; suburbs</a></li>
<li><a href="#/business">For business</a></li><li><a href="#/support">Supported living</a></li>
</ul></div>
<div><h4>COMPANY</h4><ul>
<li><a href="#/about">About us</a></li><li><a href="#/operators">Become an operator</a></li>
<li><a href="#/faq">FAQ</a></li><li><a href="#/guarantee">Service guarantee</a></li>
<li><a href="#/contact">Contact &amp; complaints</a></li>
</ul></div>"""
src = src[:OLD_FOOT.start()] + NEW_FOOT + src[OLD_FOOT.end():]
log.append("footer reduced to 11 links in two groups")

src = src.replace(".foot-g{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr 1fr;gap:2rem",
                  ".foot-g{display:grid;grid-template-columns:1.7fr 1fr 1fr;gap:2.2rem")
src = src.replace("#foot{background:#0C1430;", "#foot{background:var(--navy-d);")
log.append("footer background moved onto a brand token")

# Privacy and terms move to the legal row, where they belong.
m = re.search(r'<div class="foot-bot">(.*?)</div>', src, re.S)
if m and "privacy" not in m.group(1):
    src = src.replace(m.group(0), m.group(0).replace(
        "</div>",
        '<span class="foot-legal"><a href="#/privacy">Privacy policy</a> · <a href="#/terms">Terms of service</a></span></div>'), 1)
    log.append("privacy and terms in the legal row")

# =====================================================================
# 4. Coverage: the Check button stops shouting (D8)
# =====================================================================
sub1('<button class="btn btn-nv btn-lg" id="covGo2">Check my postcode</button>',
     '<button class="btn btn-out" id="covGo2">Check</button>',
     "coverage Check button made secondary and inline")

# =====================================================================
# 5. Legends Club savings claim carries its basis (ACL)
# =====================================================================
n = 0
for old, new in [
    ("Individual bookings ≈ $77.50/week", "Two ad-hoc loads a week ≈ $77.50"),
    ("save around $28 every week", "save around $28 a week compared with two ad-hoc loads"),
    ("Save around $28 every week", "Save around $28 a week compared with two ad-hoc loads"),
]:
    if old in src:
        src = src.replace(old, new)
        n += 1
if n:
    log.append("Legends Club saving carries its basis (%d places)" % n)

# =====================================================================
# 6. Page surface: warm paper instead of blue-grey
# =====================================================================
sub1("--bg:#FFFFFF; --bg2:#F7F8FC; --white:#FFF;",
     "--bg:#FFFFFF; --bg2:#F6F3EE; --white:#FFF;   /* bg2 is the warm paper surface */",
     "paper surface replaces the blue-grey fill")
src = src.replace("#EEF0F8", "var(--bg2)")

# =====================================================================
# 7. Head: Open Graph, Twitter, canonical-ready, structured data (D21)
# =====================================================================
js = re.search(r"<script>(.*?)</script>", src, re.S).group(1)
faq_raw = js[js.find("const FAQS = ["):]
faq_raw = faq_raw[:faq_raw.find("\n];") + 3]
pairs = re.findall(r"\[\s*'((?:[^'\\]|\\.)*)'\s*,\s*'((?:[^'\\]|\\.)*)'\s*\]", faq_raw)
faq_items = [{"@type": "Question", "name": q.replace("\\'", "'"),
              "acceptedAnswer": {"@type": "Answer", "text": a.replace("\\'", "'")}}
             for q, a in pairs[:8]]

live = dict(re.findall(r"'(\d{4})':'([^']+)'", js[js.find("const LIVE_PC = {"):js.find("const SOON_PC")]))

ld = [
    {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": "https://laundrylegends.com.au/#business",
        "name": "Laundrylegends",
        "slogan": "We Wash It Well",
        "description": "Laundry pickup and delivery across Brisbane, Logan and South East Queensland. "
                       "Wash and fold, ironing, dry cleaning and commercial linen, collected from your door "
                       "and returned. All prices include GST.",
        "areaServed": [{"@type": "PostalAddress", "addressLocality": nm,
                        "postalCode": pc, "addressRegion": "QLD", "addressCountry": "AU"}
                       for pc, nm in sorted(live.items(), key=lambda kv: kv[1])],
        "priceRange": "$$",
        "currenciesAccepted": "AUD",
        "address": {"@type": "PostalAddress", "addressRegion": "QLD", "addressCountry": "AU"},
    },
    {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "Laundry pickup and delivery",
        "provider": {"@id": "https://laundrylegends.com.au/#business"},
        "areaServed": {"@type": "State", "name": "Queensland"},
        "offers": {"@type": "Offer", "priceCurrency": "AUD",
                   "description": "Wash and fold from $32 per load (about 5 kg). Collection and return $13.50. "
                                  "Minimum $73.50 per collection. All prices include GST."},
    },
    {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_items},
]

HEAD_ADD = """<meta name="theme-color" content="#12245C">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Laundrylegends">
<meta property="og:locale" content="en_AU">
<meta property="og:title" content="Laundry collected, washed and returned — Brisbane, Logan &amp; SEQ">
<meta property="og:description" content="From your door, washed on its own cycle, folded or pressed, and brought back. From $32 a load, $13.50 collection and return. Price confirmed after weighing, before any work begins.">
<meta property="og:image" content="og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Laundrylegends — laundry pickup and delivery in Brisbane, Logan and South East Queensland">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Laundry collected, washed and returned — Brisbane, Logan &amp; SEQ">
<meta name="twitter:description" content="From $32 a load. Collection and return $13.50. Price confirmed after weighing, before any work begins.">
<meta name="twitter:image" content="og-card.png">
<link rel="manifest" href="data:application/manifest+json,PLACEHOLDER_MANIFEST">
<script type="application/ld+json">PLACEHOLDER_LD</script>
"""
sub1('<link rel="preconnect" href="https://fonts.googleapis.com">',
     HEAD_ADD + '<link rel="preconnect" href="https://fonts.googleapis.com">',
     "Open Graph, Twitter and structured data")
src = src.replace("PLACEHOLDER_LD", json.dumps(ld, ensure_ascii=False, separators=(",", ":")))

# =====================================================================
# 8. A title per route (D21)
# =====================================================================
TITLES = """
/* One title per route. Search engines and browser history both read this. */
const TITLES = {
  home:'Laundry Pickup & Delivery, Brisbane, Logan & SEQ',
  services:'Our services — wash, fold, iron, dry clean',
  pricing:'Pricing — every price includes GST',
  club:'Legends Club — weekly laundry on a fixed day',
  business:'Commercial & linen laundry for business',
  support:'Supported living & aged care laundry',
  coverage:'Coverage & suburbs we collect from',
  operators:'Become a Laundrylegends operator',
  about:'About Laundrylegends',
  guarantee:'Our service guarantee',
  faq:'Frequently asked questions',
  contact:'Contact us',
  privacy:'Privacy policy',
  terms:'Terms of service',
  app:'My account', book:'Book a collection', bookings:'My bookings',
  messages:'Messages', account:'Settings'
};
function setTitle(id){
  const t = TITLES[id];
  document.title = (t ? t + ' | Laundrylegends' : 'Laundrylegends — Laundry Pickup & Delivery | Brisbane, Logan & SEQ');
}
"""
sub1("function route(){", TITLES.strip("\n") + "\n\nfunction route(){", "per-route titles")
sub1("  if (id === 'dash') loadDash();\n  try { appRoute(id); } catch(e){}",
     "  setTitle(id);\n  if (id === 'dash') loadDash();\n  try { appRoute(id); } catch(e){}",
     "title set on every route change")

# =====================================================================
# 9. Mobile menu More toggle
# =====================================================================
sub1("document.getElementById('mobX').onclick = () => document.getElementById('mob').classList.remove('open');",
     """document.getElementById('mobX').onclick = () => document.getElementById('mob').classList.remove('open');
(() => {
  const more = document.getElementById('mobMore'), rest = document.getElementById('mobRest');
  if (!more || !rest) return;
  more.onclick = () => {
    const open = rest.hasAttribute('hidden');
    if (open) rest.removeAttribute('hidden'); else rest.setAttribute('hidden','');
    more.setAttribute('aria-expanded', open ? 'true' : 'false');
    more.classList.toggle('on', open);
  };
})();""",
     "More toggle wired")

# =====================================================================
# 10. CSS for the new pieces
# =====================================================================
CSS = """
/* ---------- PHASE B ---------- */
/* Mobile menu: one CTA, five primary, the rest behind More. */
.mob-cta{display:flex!important;align-items:center;justify-content:center;
  background:var(--red);color:var(--white)!important;border-radius:var(--r);
  padding:.9rem 1rem!important;margin-bottom:1.1rem;border-bottom:none!important;
  font-size:var(--fs-5);font-weight:800}
.mob-cta:hover{background:var(--red-d);text-decoration:none!important}
.mob-more{display:flex;align-items:center;width:100%;background:none;border:none;
  border-bottom:1px solid rgba(255,255,255,.14);color:var(--on-navy-2);
  font-family:var(--fd);font-size:var(--fs-5);font-weight:700;padding:.7rem 0;cursor:pointer}
.mob-more.on .ic{transform:rotate(180deg)}
.mob-more .ic{transition:transform var(--tr)}
#mobRest a{color:var(--on-navy-2)}

/* Footer: two link groups and a legal row. */
.foot-legal{display:block;margin-top:.5rem}
.foot-legal a{color:var(--on-navy-2);text-decoration:underline}
.foot-legal a:hover{color:var(--white)}

/* Coverage: the input leads, the button follows. */
.cov-f .btn-out{flex:none;white-space:nowrap}

/* What a load looks like — sets the expectation before the scales do. */
.load-look{display:flex;flex-wrap:wrap;gap:.5rem;margin:.9rem 0 0}
.load-look span{display:inline-flex;align-items:center;gap:.4rem;
  background:var(--bg2);border:1px solid var(--line);border-radius:var(--r-pill);
  padding:.3rem .75rem;font-size:var(--fs-micro);color:var(--body)}
.load-look .ic{width:16px;height:16px;color:var(--navy)}

@media(max-width:900px){
  /* The logo is the heaviest thing in the bar, not the CTA (D14). */
  .nav-cta .btn-red{padding:.5rem .8rem;font-size:var(--fs-micro);font-weight:700}
  .nav-cta .btn-ghost{display:none}
}
"""
src = src.replace("</style>", CSS + "</style>", 1)
log.append("phase B styles")

# =====================================================================
# 11. "What a load looks like" beside the estimator
# =====================================================================
STRIP = """<div class="load-look" aria-label="What one load looks like">
<span><svg class="ic" aria-hidden="true"><use href="#ic-basket"/></svg>One load ≈ a full kitchen basket</span>
<span><svg class="ic" aria-hidden="true"><use href="#ic-shirt"/></svg>≈ 25 t-shirts</span>
<span><svg class="ic" aria-hidden="true"><use href="#ic-scale"/></svg>≈ 5 kg dry</span>
</div>"""
m = re.search(r'(<div class="stepper"><button type="button" data-step="a,-1".*?</div>\s*</div>)', src, re.S)
if m:
    src = src[:m.end()] + "\n" + STRIP + src[m.end():]
    log.append("what a load looks like strip")

open(path, "w", encoding="utf-8").write(src)
print("Phase B applied:")
for l in log:
    print("  -", l)
