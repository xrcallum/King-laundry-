#!/usr/bin/env python3
"""
tools/import_framer.py
Fetches the LaundryHub Framer template demo site, extracts all text content
and image URLs via the Framer search index, downloads assets, and writes a
static HTML file ready for Linen Legends rebrand.

Usage:
  python3 tools/import_framer.py [--out site/linen-legends-framer.html]

Requirements: Python 3.8+, requests (pip install requests)
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

BASE_URL = "https://laundryhub.framer.website"
SEARCH_INDEX_URL = (
    "https://framerusercontent.com/sites/10TfPkk0ozorw81oKGRn3d/"
    "searchIndex-Z3qxB7QxZsHT.json"
)
PAGES = ["/", "/services", "/about-us", "/contact-us", "/location"]
ASSET_DIR = Path("site/linen-legends-framer-assets")


def fetch(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 import_framer/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_json(url: str) -> dict:
    return json.loads(fetch(url))


def fetch_images_from_html(html: str) -> list[str]:
    return list(dict.fromkeys(
        re.findall(
            r"https://framerusercontent\.com/images/[A-Za-z0-9/._-]+\.(?:jpg|png|svg|webp)",
            html,
        )
    ))


def download_assets(urls: list[str], dest: Path) -> dict[str, str]:
    """Download images; return {original_url: local_relative_path}."""
    dest.mkdir(parents=True, exist_ok=True)
    mapping = {}
    for url in urls:
        fname = url.split("/")[-1]
        local = dest / fname
        if not local.exists():
            print(f"  ↓ {fname}", flush=True)
            try:
                data = fetch(url)
                local.write_bytes(data)
            except Exception as e:
                print(f"    ✗ {e}", file=sys.stderr)
                continue
        mapping[url] = str(dest / fname)
    return mapping


def build_site(index: dict, asset_map: dict) -> str:
    """Generate a self-contained HTML page from the extracted data."""
    home = index.get("/", {})

    def h(page_key: str, tag: str) -> list[str]:
        return index.get(page_key, {}).get(tag, [])

    def img(url: str) -> str:
        return asset_map.get(url, url)

    # Key images (by position in list — matches what the homepage renders)
    imgs = list(asset_map.keys())
    logo_url      = "https://framerusercontent.com/images/mBVjqOKkzoCZ5jl6HOGwLIYqG0o.png"
    hero_bg_url   = "https://framerusercontent.com/images/TmNjKNpQI4R3PjY754xJuFX7mE.png"
    map_img_url   = "https://framerusercontent.com/images/HYR4WprvCLbOQUTlPM4FheV80P4.png"
    svc1_url      = "https://framerusercontent.com/images/yK99FKksn0SziSGfKcVUIcCibqU.jpg"
    svc2_url      = "https://framerusercontent.com/images/vvmmP1YFmfvJ9YaUBFIKhNeV2s.jpg"
    svc3_url      = "https://framerusercontent.com/images/FqMhgw7Akbwlshuk7cfETGQI.jpg"
    svc4_url      = "https://framerusercontent.com/images/wgAiMcd2q4u0SyOo60S9q3zZD0.jpg"
    steps_url     = "https://framerusercontent.com/images/u8glprt7QGiaxegYOoVMN1LQxQ.png"
    testimonial_url = "https://framerusercontent.com/images/eibaZcQ3NT0wIZCdLe7ly758Zis.png"

    services_h3 = [s for s in h("/", "h3") if s in [
        "Self-Service Laundry", "Pick & Drop Service",
        "Laundry Express", "Ironing Service", "Dry Cleaning",
    ]]
    services_desc = [
        "Use modern, high-capacity washers and dryers for a quick and smooth laundry process.",
        "Convenient doorstep laundry pickup and delivery for clean, fresh clothes without effort.",
        "Fast and efficient wash-and-dry service for busy schedules and quick needs.",
        "Get crisp, wrinkle-free clothes with professional ironing for a polished appearance.",
        "Specialised cleaning for delicate fabrics, suits, and premium garments with expert care.",
    ]
    svc_imgs = [svc1_url, svc2_url, svc3_url, svc4_url, svc4_url]

    benefits_h3 = [s for s in h("/", "h3") if s in [
        "Time-Saving Solutions", "Fast & Efficient Machines",
        "Entertainment & Free Wi-Fi", "Eco-Friendly Cleaning",
        "Trusted Expertise", "Friendly & Helpful Staff",
    ]]
    benefits_desc = [
        "We streamline the laundry process to make your life easier and hassle-free.",
        "High-capacity washers and dryers for quick, smooth, and hassle-free laundry.",
        "Enjoy seamless connectivity and entertainment while waiting for your laundry.",
        "We use environmentally safe methods that are tough on stains yet gentle on fabrics.",
        "Our experienced team ensures reliable service with consistently great results.",
        "Our team ensures a smooth experience with always clean facilities.",
    ]

    locations = [
        ("Brisbane CBD", "123 Queen St, Brisbane QLD 4000", "Mon – Sun", "6:00 AM – 11:00 PM"),
        ("South Brisbane", "456 Melbourne St, South Brisbane QLD 4101", "Mon – Sun", "7:00 AM – 10:00 PM"),
        ("Logan Central", "789 Kingston Rd, Logan Central QLD 4114", "Mon – Sat", "7:00 AM – 9:00 PM"),
        ("Sunnybank", "101 Mains Rd, Sunnybank QLD 4109", "Mon – Sun", "6:30 AM – 11:00 PM"),
        ("Capalaba", "222 Old Cleveland Rd, Capalaba QLD 4157", "Mon – Sun", "5:00 AM – 12:00 AM"),
        ("Chermside", "333 Gympie Rd, Chermside QLD 4032", "24 Hours", "—"),
    ]

    faqs = [
        ("How does Linen Legends' service work?",
         "Book online or call us, drop off or schedule a pickup, and we'll wash, dry, fold, and return your laundry — fresh every time."),
        ("Do you offer pick-up and delivery?",
         "Yes — we cover Brisbane, Logan, and South East Queensland. Book online and we'll be there."),
        ("What types of laundry can you clean?",
         "Everyday clothes, bedding, towels, delicate fabrics, suits, and more. Ask about commercial laundry too."),
        ("How long does the laundry process take?",
         "Standard service is 24 hours. Express is same-day when booked before 9am. Self-service takes as little as an hour."),
        ("Are your products safe for sensitive skin?",
         "Yes — we use fragrance-free, dermatologist-tested detergents on request. Just mention it when you book."),
        ("What payment methods do you accept?",
         "Visa, Mastercard, EFTPOS, and cash. All prices are GST-inclusive."),
    ]

    loc_cards = "\n".join(f"""
      <div class="loc-card">
        <h3>{name}</h3>
        <p class="loc-addr">{addr}</p>
        <p><span class="loc-label">Open Days:</span> {days}</p>
        <p><span class="loc-label">Hours:</span> {hours}</p>
        <a href="#contact" class="btn btn-sm btn-teal">Get Directions</a>
      </div>""" for name, addr, days, hours in locations)

    svc_cards = ""
    for i, (svc, desc) in enumerate(zip(services_h3, services_desc)):
        svc_cards += f"""
      <div class="svc-card">
        <img src="{img(svc_imgs[i % len(svc_imgs)])}" alt="{svc}" loading="lazy">
        <h3>{svc}</h3>
        <p>{desc}</p>
      </div>"""

    ben_cards = ""
    for ben, desc in zip(benefits_h3, benefits_desc):
        ben_cards += f"""
      <div class="ben-card">
        <div class="ben-icon">✓</div>
        <div>
          <h3>{ben}</h3>
          <p>{desc}</p>
        </div>
      </div>"""

    faq_items = ""
    for q, a in faqs:
        faq_items += f"""
      <details class="faq-item">
        <summary>{q}</summary>
        <p>{a}</p>
      </details>"""

    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Linen Legends — Fresh Laundry, Pickup &amp; Delivery Brisbane</title>
<meta name="description" content="Linen Legends — fast, easy &amp; reliable laundry pickup and delivery across Brisbane, Logan and South East Queensland. Book online today.">
<meta property="og:type" content="website">
<meta property="og:title" content="Linen Legends — Fresh Laundry, Pickup &amp; Delivery Brisbane">
<meta property="og:description" content="Fast, easy &amp; reliable laundry pickup and delivery across Brisbane and SEQ.">
<meta property="og:image" content="{img(hero_bg_url)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
/* ── Tokens ──────────────────────────────────────────── */
:root{{
  --teal:#2A9D8F; --teal-d:#1F7268; --teal-l:#48C4B5; --teal-w:#E6F7F5;
  --navy:#0C265F; --navy-d:#071A45; --navy-l:#2B4BAA; --navy-w:#F0F3FC;
  --ink:#141826; --body:#454C60; --mute:#666D80;
  --line:#D3D9E6; --paper:#F6F3EE; --bg:#FFFFFF; --bg2:#F6F3EE;
  --r:8px; --r-lg:16px;
  --f:\'Inter\',sans-serif;
  --tr:180ms ease;
  --max:1200px;
  --s1:.5rem; --s2:1rem; --s3:1.5rem; --s4:2rem; --s6:3rem; --s8:4rem;
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--f);background:var(--bg);color:var(--ink);line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}}
img{{max-width:100%;height:auto;display:block}}
a{{color:inherit;text-decoration:none}}
h1,h2,h3,h4{{font-weight:800;line-height:1.15}}
p{{color:var(--body);line-height:1.7}}
.container{{max-width:var(--max);margin:0 auto;padding:0 1.25rem}}
.section{{padding:var(--s8) 0}}
.section-label{{font-size:.75rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--teal);margin-bottom:.5rem}}
.section-title{{font-size:clamp(1.6rem,3.5vw,2.4rem);margin-bottom:1rem}}
.section-sub{{color:var(--mute);max-width:560px;margin:0 auto 2.5rem;text-align:center}}

/* ── Buttons ─────────────────────────────────────────── */
.btn{{display:inline-flex;align-items:center;gap:.4rem;font-weight:700;border:none;border-radius:var(--r);cursor:pointer;transition:background var(--tr),transform .15s ease;white-space:nowrap;font-family:var(--f)}}
.btn-teal{{background:var(--teal);color:#fff;padding:.75rem 1.5rem;font-size:.875rem}}
.btn-teal:hover{{background:var(--teal-d);transform:translateY(-1px)}}
.btn-outline{{background:transparent;color:var(--teal);border:1.5px solid var(--teal);padding:.72rem 1.45rem;font-size:.875rem}}
.btn-outline:hover{{background:var(--teal-w)}}
.btn-sm{{padding:.55rem 1.1rem;font-size:.8rem}}
.btn-nav{{background:var(--teal);color:#fff;padding:.6rem 1.2rem;font-size:.8rem;border-radius:var(--r)}}

/* ── Top bar ─────────────────────────────────────────── */
#topbar{{background:var(--navy);color:#fff;font-size:.78rem;padding:.4rem 0;text-align:center}}
#topbar a{{color:#C9D2F2}}

/* ── Nav ─────────────────────────────────────────────── */
#nav{{position:sticky;top:0;z-index:90;background:#fff;border-bottom:1px solid var(--line);padding:.9rem 0}}
.nav-inner{{display:flex;align-items:center;justify-content:space-between;gap:1.5rem}}
.brand{{display:flex;align-items:center;gap:.6rem}}
.brand-logo{{height:36px;width:auto}}
.brand-name{{font-weight:900;font-size:1.1rem;letter-spacing:-.01em;color:var(--ink)}}
.brand-name span{{color:var(--teal)}}
.nav-links{{list-style:none;display:flex;gap:1.5rem;align-items:center}}
.nav-links a{{font-size:.875rem;font-weight:600;color:var(--body);transition:color var(--tr)}}
.nav-links a:hover{{color:var(--teal)}}
.nav-cta{{display:flex;align-items:center;gap:.75rem}}
.nav-ham{{display:none;flex-direction:column;gap:5px;cursor:pointer;background:none;border:none;padding:.25rem}}
.nav-ham span{{display:block;width:22px;height:2px;background:var(--ink);border-radius:2px;transition:var(--tr)}}

/* ── Mobile nav ──────────────────────────────────────── */
#mob{{display:none;position:fixed;inset:0;background:#fff;z-index:200;padding:5rem 1.5rem 2rem;overflow-y:auto}}
#mob.open{{display:block}}
#mob-close{{position:absolute;top:1rem;right:1rem;background:none;border:none;font-size:1.5rem;cursor:pointer}}
#mob a{{display:block;font-size:1.1rem;font-weight:700;color:var(--ink);padding:.75rem 0;border-bottom:1px solid var(--line)}}
#mob a:hover{{color:var(--teal)}}

/* ── Hero ────────────────────────────────────────────── */
#hero{{background:linear-gradient(135deg,#0C265F 0%,#1a3a7a 60%,#2A9D8F 100%);color:#fff;padding:5rem 0 4rem;min-height:80vh;display:flex;align-items:center;position:relative;overflow:hidden}}
#hero::after{{content:\'\';position:absolute;inset:0;background:url(\'{img(hero_bg_url)}\') center/cover no-repeat;opacity:.12;pointer-events:none}}
.hero-inner{{display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:center;position:relative;z-index:1}}
.hero-tag{{font-size:.78rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--teal-l);margin-bottom:.75rem}}
.hero-h1{{font-size:clamp(2rem,5vw,3.5rem);font-weight:900;line-height:1.1;margin-bottom:1rem}}
.hero-h1 span{{color:var(--teal-l)}}
.hero-sub{{color:rgba(255,255,255,.8);font-size:1.05rem;margin-bottom:2rem;max-width:460px}}
.hero-actions{{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:2rem}}
.hero-social{{display:flex;align-items:center;gap:.75rem;font-size:.82rem;color:rgba(255,255,255,.7)}}
.hero-rating{{background:rgba(255,255,255,.12);padding:.5rem 1rem;border-radius:100px;display:inline-flex;align-items:center;gap:.5rem}}
.hero-img{{border-radius:var(--r-lg);overflow:hidden;box-shadow:0 24px 64px rgba(0,0,0,.35)}}
.hero-img img{{width:100%;height:420px;object-fit:cover}}

/* ── Location finder ──────────────────────────────────── */
#find{{background:var(--paper);padding:var(--s6) 0}}
.find-card{{background:#fff;border-radius:var(--r-lg);padding:2.5rem;display:grid;grid-template-columns:1fr 1fr;gap:2rem;align-items:center;box-shadow:0 4px 24px rgba(0,0,0,.08)}}
.find-map{{border-radius:var(--r);overflow:hidden}}
.find-map img{{width:100%;height:280px;object-fit:cover}}

/* ── Services ─────────────────────────────────────────── */
#services{{background:var(--bg)}}
.svc-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1.5rem;margin-top:2rem}}
.svc-card{{border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;transition:box-shadow var(--tr),transform var(--tr)}}
.svc-card:hover{{box-shadow:0 8px 32px rgba(0,0,0,.1);transform:translateY(-2px)}}
.svc-card img{{width:100%;height:180px;object-fit:cover}}
.svc-card h3{{font-size:1rem;font-weight:700;padding:1rem 1rem .25rem}}
.svc-card p{{font-size:.875rem;color:var(--mute);padding:0 1rem 1rem}}

/* ── How it works ─────────────────────────────────────── */
#how{{background:var(--paper)}}
.how-inner{{display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:center}}
.how-img img{{width:100%;border-radius:var(--r-lg);box-shadow:0 12px 40px rgba(0,0,0,.12)}}
.steps{{display:flex;flex-direction:column;gap:1.5rem}}
.step{{display:flex;gap:1rem;align-items:flex-start}}
.step-num{{flex-shrink:0;width:2.2rem;height:2.2rem;border-radius:50%;background:var(--teal);color:#fff;font-weight:800;font-size:.9rem;display:flex;align-items:center;justify-content:center}}
.step-text h3{{font-size:1rem;margin-bottom:.25rem}}
.step-text p{{font-size:.875rem;color:var(--mute)}}

/* ── Benefits ─────────────────────────────────────────── */
#benefits{{background:var(--bg)}}
.ben-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.25rem;margin-top:2rem}}
.ben-card{{display:flex;gap:1rem;align-items:flex-start;padding:1.25rem;border:1px solid var(--line);border-radius:var(--r-lg)}}
.ben-icon{{flex-shrink:0;width:2rem;height:2rem;border-radius:50%;background:var(--teal-w);color:var(--teal);font-weight:800;display:flex;align-items:center;justify-content:center}}
.ben-card h3{{font-size:.95rem;font-weight:700;margin-bottom:.2rem}}
.ben-card p{{font-size:.85rem;color:var(--mute)}}

/* ── Testimonials ─────────────────────────────────────── */
#testimonials{{background:var(--paper)}}
.test-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1.5rem;margin-top:2rem}}
.test-card{{background:#fff;padding:1.5rem;border-radius:var(--r-lg);border:1px solid var(--line)}}
.test-card blockquote{{font-style:italic;color:var(--body);font-size:.9rem;margin-bottom:1rem}}
.test-author{{font-weight:700;font-size:.875rem}}
.test-role{{font-size:.8rem;color:var(--mute)}}
.test-stars{{color:#F4B942;font-size:.9rem;margin-bottom:.75rem}}

/* ── Offer banner ─────────────────────────────────────── */
#offer{{background:linear-gradient(135deg,var(--teal) 0%,var(--teal-d) 100%);color:#fff;padding:3.5rem 0;text-align:center}}
#offer h2{{font-size:clamp(1.5rem,3vw,2.2rem);margin-bottom:.5rem}}
#offer p{{color:rgba(255,255,255,.85);margin-bottom:1.5rem}}
.offer-points{{display:flex;justify-content:center;gap:2rem;flex-wrap:wrap;margin-bottom:2rem;font-size:.875rem;font-weight:600}}
.offer-points span::before{{content:"✓ "}}

/* ── FAQ ──────────────────────────────────────────────── */
#faq{{background:var(--bg)}}
.faq-list{{max-width:720px;margin:0 auto}}
.faq-item{{border-bottom:1px solid var(--line);padding:1rem 0}}
.faq-item summary{{font-weight:700;cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;font-size:.95rem}}
.faq-item summary::-webkit-details-marker{{display:none}}
.faq-item summary::after{{content:"+";font-size:1.2rem;color:var(--teal);transition:transform var(--tr)}}
.faq-item[open] summary::after{{transform:rotate(45deg)}}
.faq-item p{{color:var(--mute);font-size:.9rem;padding:.75rem 0 .25rem}}

/* ── Locations grid ───────────────────────────────────── */
#locations{{background:var(--paper)}}
.loc-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1.5rem;margin-top:2rem}}
.loc-card{{background:#fff;padding:1.5rem;border-radius:var(--r-lg);border:1px solid var(--line)}}
.loc-card h3{{font-size:1rem;font-weight:700;margin-bottom:.5rem;color:var(--ink)}}
.loc-addr{{font-size:.875rem;color:var(--mute);margin-bottom:.75rem}}
.loc-label{{font-weight:600;font-size:.82rem;color:var(--ink)}}
.loc-card p{{font-size:.85rem;color:var(--mute);margin-bottom:.35rem}}

/* ── Contact ──────────────────────────────────────────── */
#contact{{background:var(--bg)}}
.contact-inner{{display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start}}
.contact-info h2{{font-size:1.6rem;margin-bottom:.75rem}}
.contact-info p{{color:var(--mute);margin-bottom:1.5rem}}
.contact-detail{{display:flex;gap:.6rem;align-items:center;margin-bottom:.75rem;font-size:.9rem}}
.contact-detail strong{{min-width:80px}}
.contact-form{{background:var(--paper);padding:2rem;border-radius:var(--r-lg)}}
.contact-form h3{{margin-bottom:1.25rem}}
.form-row{{margin-bottom:1rem}}
.form-row label{{display:block;font-size:.82rem;font-weight:600;margin-bottom:.35rem;color:var(--ink)}}
.form-row input,.form-row textarea,.form-row select{{width:100%;padding:.7rem .9rem;border:1.5px solid var(--line);border-radius:var(--r);font-family:var(--f);font-size:.9rem;transition:border-color var(--tr);background:#fff}}
.form-row input:focus,.form-row textarea:focus{{outline:none;border-color:var(--teal)}}
.form-row textarea{{min-height:110px;resize:vertical}}

/* ── Footer ───────────────────────────────────────────── */
#footer{{background:var(--navy);color:#fff;padding:3rem 0 1.5rem}}
.footer-inner{{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:2rem;margin-bottom:2rem}}
.footer-brand h3{{font-size:1.1rem;font-weight:800;margin-bottom:.5rem}}
.footer-brand p{{font-size:.85rem;color:rgba(255,255,255,.6);max-width:240px}}
.footer-col h4{{font-size:.82rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.4);margin-bottom:1rem}}
.footer-col a{{display:block;font-size:.875rem;color:rgba(255,255,255,.7);margin-bottom:.5rem;transition:color var(--tr)}}
.footer-col a:hover{{color:#fff}}
.footer-bottom{{border-top:1px solid rgba(255,255,255,.1);padding-top:1.25rem;display:flex;justify-content:space-between;align-items:center;font-size:.8rem;color:rgba(255,255,255,.4)}}
.compliance{{font-size:.72rem;color:rgba(255,255,255,.35);margin-top:.5rem;line-height:1.6}}

/* ── Responsive ───────────────────────────────────────── */
@media(max-width:900px){{
  .hero-inner,.how-inner,.find-card,.contact-inner{{grid-template-columns:1fr}}
  .hero-img{{display:none}}
  .footer-inner{{grid-template-columns:1fr 1fr}}
}}
@media(max-width:600px){{
  .nav-links,.nav-cta{{display:none}}
  .nav-ham{{display:flex}}
  .section{{padding:3rem 0}}
  .footer-inner{{grid-template-columns:1fr}}
  .offer-points{{flex-direction:column;align-items:center;gap:.75rem}}
}}
</style>
</head>
<body>

<!-- Top bar -->
<div id="topbar">
  <div class="container">
    📞 <a href="tel:0731234567">07 3123 4567</a> &nbsp;·&nbsp;
    ✉ <a href="mailto:hello@linenlegends.com.au">hello@linenlegends.com.au</a>
    &nbsp;·&nbsp; Brisbane · Logan · SEQ
  </div>
</div>

<!-- Nav -->
<nav id="nav" aria-label="Main navigation">
  <div class="container nav-inner">
    <a href="/" class="brand">
      <img src="{img(logo_url)}" alt="Linen Legends logo" class="brand-logo">
      <span class="brand-name">Linen <span>Legends</span></span>
    </a>
    <ul class="nav-links">
      <li><a href="#services">Services</a></li>
      <li><a href="#locations">Locations</a></li>
      <li><a href="#how">How It Works</a></li>
      <li><a href="#faq">FAQs</a></li>
      <li><a href="#contact">About</a></li>
    </ul>
    <div class="nav-cta">
      <a href="#contact" class="btn btn-nav">Book Pickup</a>
    </div>
    <button class="nav-ham" aria-label="Open menu" onclick="document.getElementById('mob').classList.toggle('open')">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>

<!-- Mobile nav -->
<div id="mob" role="dialog" aria-modal="true" aria-label="Mobile menu">
  <button id="mob-close" aria-label="Close menu" onclick="document.getElementById('mob').classList.remove('open')">✕</button>
  <a href="#services" onclick="document.getElementById('mob').classList.remove('open')">Services</a>
  <a href="#locations" onclick="document.getElementById('mob').classList.remove('open')">Locations</a>
  <a href="#how" onclick="document.getElementById('mob').classList.remove('open')">How It Works</a>
  <a href="#faq" onclick="document.getElementById('mob').classList.remove('open')">FAQs</a>
  <a href="#contact" onclick="document.getElementById('mob').classList.remove('open')">Contact</a>
  <a href="#contact" class="btn btn-teal" style="margin-top:1.5rem" onclick="document.getElementById('mob').classList.remove('open')">Book Pickup</a>
</div>

<!-- Hero -->
<section id="hero">
  <div class="container hero-inner">
    <div class="hero-content">
      <p class="hero-tag">Modern Machines, Faster Wash</p>
      <h1 class="hero-h1">Fast, Easy &amp; Reliable <span>Laundry!</span></h1>
      <p class="hero-sub">Enjoy a hassle-free laundry experience with modern machines, free Wi-Fi, a cosy lounge, and easy payment options. Fresh, clean clothes — made simple!</p>
      <div class="hero-actions">
        <a href="#contact" class="btn btn-teal">Schedule a Pickup</a>
        <a href="#services" class="btn btn-outline" style="color:#fff;border-color:rgba(255,255,255,.4)">Our Services</a>
      </div>
      <div class="hero-social">
        <div class="hero-rating">⭐ 4.9+ Rating · 1,200+ Reviews</div>
      </div>
    </div>
    <div class="hero-img">
      <img src="{img(svc2_url)}" alt="Linen Legends laundry service" loading="eager">
    </div>
  </div>
</section>

<!-- Location finder -->
<section id="find">
  <div class="container">
    <div class="find-card">
      <div>
        <p class="section-label">Affordable cleaning solutions</p>
        <h2 class="section-title" style="text-align:left">Find a Linen Legends Near You</h2>
        <p style="margin-bottom:1.5rem">We make doing laundry easy with modern machines, a comfortable space, and multiple locations across Brisbane and SEQ. Whether you're washing a few items or a big load, we've got you covered.</p>
        <a href="#locations" class="btn btn-teal">📍 Find Your Nearest Location</a>
      </div>
      <div class="find-map">
        <img src="{img(map_img_url)}" alt="Linen Legends locations map" loading="lazy">
      </div>
    </div>
  </div>
</section>

<!-- Services -->
<section id="services" class="section">
  <div class="container">
    <div style="text-align:center">
      <p class="section-label">Services</p>
      <h2 class="section-title">Our Laundry Services</h2>
      <p class="section-sub">While we can customise your cleaning plan to suit your needs, most clients schedule regular cleaning services:</p>
    </div>
    <div class="svc-grid">{svc_cards}
    </div>
  </div>
</section>

<!-- How it works -->
<section id="how" class="section">
  <div class="container">
    <div class="how-inner">
      <div class="how-img">
        <img src="{img(steps_url)}" alt="How our pickup service works" loading="lazy">
      </div>
      <div>
        <p class="section-label">How it works</p>
        <h2 class="section-title" style="text-align:left">How Our Pick &amp; Drop Service Works</h2>
        <div class="steps">
          <div class="step">
            <div class="step-num">1</div>
            <div class="step-text">
              <h3>Schedule a Pickup</h3>
              <p>Book online or call us to set your preferred pickup time.</p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">2</div>
            <div class="step-text">
              <h3>We Pick Up Your Laundry</h3>
              <p>Our team arrives at your location to collect your clothes safely.</p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">3</div>
            <div class="step-text">
              <h3>Expert Cleaning &amp; Care</h3>
              <p>We wash, dry, and fold your laundry with the highest quality standards.</p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">4</div>
            <div class="step-text">
              <h3>Delivery to Your Doorstep</h3>
              <p>Your fresh, clean clothes are delivered back to you — ready to wear!</p>
            </div>
          </div>
        </div>
        <a href="#contact" class="btn btn-teal" style="margin-top:2rem">Book Now</a>
      </div>
    </div>
  </div>
</section>

<!-- Benefits -->
<section id="benefits" class="section">
  <div class="container">
    <div style="text-align:center">
      <p class="section-label">Our Benefits</p>
      <h2 class="section-title">Why Choose Linen Legends?</h2>
      <p class="section-sub">We streamline the laundry process to make your life easier and hassle-free.</p>
    </div>
    <div class="ben-grid">{ben_cards}
    </div>
  </div>
</section>

<!-- Testimonials -->
<section id="testimonials" class="section">
  <div class="container">
    <div style="text-align:center">
      <p class="section-label">Our Testimonials</p>
      <h2 class="section-title">What Our Happy Customers Say</h2>
      <p class="section-sub">At Linen Legends, we prioritise customer satisfaction. Thousands trust us for fresh, clean laundry daily.</p>
    </div>
    <div class="test-grid">
      <div class="test-card">
        <div class="test-stars">⭐⭐⭐⭐⭐</div>
        <blockquote>"Linen Legends provides excellent service! My clothes are always fresh, neatly folded, and delivered on time."</blockquote>
        <div class="test-author">Emily R.</div>
        <div class="test-role">Marketing Manager</div>
      </div>
      <div class="test-card">
        <div class="test-stars">⭐⭐⭐⭐⭐</div>
        <blockquote>"The best laundromat in Brisbane! Modern machines, friendly staff, and a smooth experience every time."</blockquote>
        <div class="test-author">Mark T.</div>
        <div class="test-role">Business Owner</div>
      </div>
      <div class="test-card">
        <div class="test-stars">⭐⭐⭐⭐⭐</div>
        <blockquote>"Linen Legends' pickup and delivery service is a lifesaver! Super convenient and reliable."</blockquote>
        <div class="test-author">David W.</div>
        <div class="test-role">Software Engineer</div>
      </div>
      <div class="test-card">
        <div class="test-stars">⭐⭐⭐⭐⭐</div>
        <blockquote>"Impressed with their stain removal service! Linen Legends saved my favourite dress."</blockquote>
        <div class="test-author">Sophia L.</div>
        <div class="test-role">Fashion Designer</div>
      </div>
    </div>
  </div>
</section>

<!-- Offer -->
<section id="offer">
  <div class="container">
    <p class="section-label" style="color:rgba(255,255,255,.6)">Special Offer</p>
    <h2>Fresh Laundry, Big Savings!</h2>
    <p>Enjoy 20% OFF your first laundry service with Linen Legends! Experience professional cleaning, fast turnaround, and fresh clothes every time.</p>
    <div class="offer-points">
      <span>Fast &amp; Efficient – Quick service without compromising quality</span>
      <span>Eco-Friendly Cleaning – Gentle on fabrics, safe for the planet</span>
      <span>Expert Care – Fresh, clean, and neatly folded clothes every time</span>
    </div>
    <a href="#contact" class="btn" style="background:#fff;color:var(--teal);font-size:.9rem;padding:.8rem 2rem">Claim Your Discount</a>
  </div>
</section>

<!-- FAQ -->
<section id="faq" class="section">
  <div class="container">
    <div style="text-align:center;margin-bottom:2rem">
      <p class="section-label">FAQs</p>
      <h2 class="section-title">Frequently Asked Questions</h2>
    </div>
    <div class="faq-list">{faq_items}
    </div>
  </div>
</section>

<!-- Locations -->
<section id="locations" class="section">
  <div class="container">
    <div style="text-align:center">
      <p class="section-label">Locations</p>
      <h2 class="section-title">Find a Linen Legends Near You</h2>
      <p class="section-sub">Serving Brisbane, Logan, and South East Queensland.</p>
    </div>
    <div class="loc-grid">{loc_cards}
    </div>
  </div>
</section>

<!-- Contact -->
<section id="contact" class="section">
  <div class="container">
    <div class="contact-inner">
      <div class="contact-info">
        <p class="section-label">Get in Touch</p>
        <h2>Get in Touch with Us</h2>
        <p>Reach out for inquiries, support, or partnership opportunities. We're here to help!</p>
        <div class="contact-detail">
          <strong>Phone:</strong>
          <a href="tel:0731234567">07 3123 4567</a>
        </div>
        <div class="contact-detail">
          <strong>Email:</strong>
          <a href="mailto:hello@linenlegends.com.au">hello@linenlegends.com.au</a>
        </div>
        <div class="contact-detail">
          <strong>Hours:</strong>
          Mon – Sun, 6:00 AM – 10:00 PM
        </div>
        <div style="margin-top:1.5rem">
          <a href="https://calendly.com/" class="btn btn-teal" target="_blank" rel="noopener">Schedule a Pickup</a>
        </div>
      </div>
      <div class="contact-form">
        <h3>Send Us a Message</h3>
        <form onsubmit="return false">
          <div class="form-row">
            <label for="cf-name">Full Name</label>
            <input type="text" id="cf-name" placeholder="Your name" autocomplete="name">
          </div>
          <div class="form-row">
            <label for="cf-email">Email</label>
            <input type="email" id="cf-email" placeholder="your@email.com" autocomplete="email">
          </div>
          <div class="form-row">
            <label for="cf-service">Service</label>
            <select id="cf-service">
              <option value="">Select a service…</option>
              <option>Pick &amp; Drop Service</option>
              <option>Self-Service Laundry</option>
              <option>Ironing Service</option>
              <option>Dry Cleaning</option>
              <option>Laundry Express</option>
            </select>
          </div>
          <div class="form-row">
            <label for="cf-msg">Message</label>
            <textarea id="cf-msg" placeholder="How can we help?"></textarea>
          </div>
          <button type="submit" class="btn btn-teal" style="width:100%">Submit</button>
        </form>
      </div>
    </div>
  </div>
</section>

<!-- Footer -->
<footer id="footer">
  <div class="container">
    <div class="footer-inner">
      <div class="footer-brand">
        <h3>Linen Legends</h3>
        <p>Fast, reliable, and hassle-free laundry services tailored for your convenience across Brisbane and SEQ.</p>
        <p class="compliance" style="margin-top:1rem">All prices GST-inclusive (AUD). NDIS plan-managed accepted. Laundry services comply with AS/NZS 4146. Independent contractors engaged under written agreements.</p>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <a href="#services">Services</a>
        <a href="#locations">Locations</a>
        <a href="#how">How It Works</a>
        <a href="#faq">FAQs</a>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <a href="#contact">About Us</a>
        <a href="#contact">Contact</a>
        <a href="#contact">Careers</a>
      </div>
      <div class="footer-col">
        <h4>Get in Touch</h4>
        <a href="tel:0731234567">07 3123 4567</a>
        <a href="mailto:hello@linenlegends.com.au">hello@linenlegends.com.au</a>
        <a href="#locations">Find a Location</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Linen Legends. All rights reserved. ABN: [TO BE CONFIRMED].</span>
      <span>Brisbane, QLD, Australia</span>
    </div>
  </div>
</footer>

<script>
// Close mob nav on outside click
document.addEventListener('click', e => {{
  const mob = document.getElementById('mob');
  if (mob.classList.contains('open') && !mob.contains(e.target) && !e.target.closest('.nav-ham')) {{
    mob.classList.remove('open');
  }}
}});
// Escape key closes mob nav
document.addEventListener('keydown', e => {{
  if (e.key === 'Escape') document.getElementById('mob').classList.remove('open');
}});
</script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Import LaundryHub Framer template as Linen Legends")
    parser.add_argument("--out", default="site/linen-legends-framer.html",
                        help="Output HTML file path")
    args = parser.parse_args()

    print("Fetching search index…")
    index = fetch_json(SEARCH_INDEX_URL)
    print(f"  {len(index)} pages found")

    print("Fetching homepage HTML for image list…")
    home_html = fetch(BASE_URL + "/").decode("utf-8", errors="replace")

    print("Finding images…")
    img_urls = fetch_images_from_html(home_html)
    print(f"  {len(img_urls)} images found")

    print("Downloading assets…")
    asset_map = download_assets(img_urls, ASSET_DIR)

    print("Building site HTML…")
    html = build_site(index, asset_map)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"✓ Written to {out} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
