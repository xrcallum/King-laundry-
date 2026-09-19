# Laundrylegends — Home Laundry Landing Page
## Complete Handoff Document

**Prepared:** 19 September 2026
**Venture:** Laundrylegends
**Owner:** Callum Page
**Repo:** `github.com/xrcallum/King-laundry-`
**Branch:** `claude/laundry-australia-landing-page-g9nuvw`
**File:** `site/laundry-australia/home-laundry.html` (single file, 871 lines, no build step)
**Latest commit:** `30ea2f6`

---

## 1. PASTE THIS INTO THE NEW CLAUDE FIRST

> I'm continuing work on the Laundrylegends home-laundry landing page. It's a single self-contained HTML file — no build step, no dependencies beyond three Google Fonts. It lives at `site/laundry-australia/home-laundry.html` on branch `claude/laundry-australia-landing-page-g9nuvw` in `github.com/xrcallum/King-laundry-`.
>
> It started as a mobile-first replica of a competitor's page (laundryaustralia.com.au/home-laundry/), built from iPhone screen recordings because the site couldn't be fetched directly. It has since been rebranded to Laundrylegends with recharacterised copy and a different display typeface.
>
> The full spec, copy inventory, outstanding tasks and go-live blockers are in the handoff document I'm attaching. Read section 7 (Blockers) before suggesting we publish anything.

---

## 2. What this is, and how it got here

| Stage | What happened |
|---|---|
| Brief | Replicate `laundryaustralia.com.au/home-laundry/` 1:1 as a single HTML file |
| Obstacle | Environment's egress proxy blocked the domain — no direct fetch, no scrape, no screenshot |
| Workaround | Owner supplied 3 iPhone screen recordings; 56 frames extracted at 2fps via `imageio-ffmpeg`; all content transcribed visually |
| Verification | Rendered at 390px (iPhone 12) in headless Chromium; 7 side-by-side source-vs-build comparisons produced and reviewed |
| Rebrand | Renamed to Laundrylegends, display font swapped, all body copy rewritten, fake contact details inserted as placeholders |

**Design target:** mobile-first, 390px viewport, single column, `max-width: 520px`.

**UNVERIFIED:** The build was never compared against the live site directly — only against the owner's screen recordings. Anything not visible in those 56 frames (hover states, menu contents, form behaviour, any section below the footer) is unconfirmed.

---

## 3. Brand specification

### Colour tokens

| Token | Value | Used for |
|---|---|---|
| `--orange` | `#EE6E1F` | Primary CTA, accents, section rules, headings on white cards |
| `--orange-2` | `#F58A3A` | Reserved (declared, not yet used) |
| `--orange-soft` | `#FCE4D2` | Reserved (declared, not yet used) |
| `--ink` | `#111111` | Body text |
| `--ink-2` | `#333333` | Reserved |
| `--grey-card` | `#2E2E2E` | Dark "Take it off your list" card |
| `--blue` | `#194B9E` | Footer background, clients section headings |
| `--blue-2` | `#0F3F8A` | Reserved |
| Hero/header bg | `#000000` | Hardcoded, not tokenised |

### Typography

| Role | Font | Weight | Notes |
|---|---|---|---|
| Display / headings | **Archivo** | 600 (logo lockup 700) | Corporate restyle 19 Sep 2026 — replaced Anton; calmer scale, leading ≥1.0 |
| Label accent | **Inter** 500, letter-spaced caps (.2–.32em) | 500 | Replaced Yellowtail script — hero subtitle, brand tagline, price-card labels |
| Body | **Inter** | 300–600 + italics | Replaced Poppins |

Google Fonts URL in `<head>`:
```
https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,500;0,600;0,700;1,500&family=Inter:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap
```

> **Note for the next Claude:** the 19 Sep 2026 corporate restyle replaced Anton/Yellowtail/Poppins with Archivo/Inter across both pages, reduced heading sizes and weights (600 max, logo 700), softened card shadows, and converted all script accents to letter-spaced uppercase Inter labels. The type-scale table below reflects the ORIGINAL Anton build and is superseded — read the CSS as source of truth.

### Type scale (fluid)

| Element | Size |
|---|---|
| Hero "HOME" | `clamp(48px, 17vw, 84px)` → `96px` at ≥640px |
| Hero "LAUNDRY" | `clamp(70px, 22vw, 130px)` → `152px` at ≥640px |
| Hero script sub | `clamp(34px, 11vw, 56px)` → `64px` at ≥640px |
| Section h2 (life-busy) | `clamp(28px, 8.5vw, 44px)` → `56px` at ≥640px |
| Card h3 | `34px` |
| Step card h3 | `30px` |

### Other tokens

`--radius-card: 26px` · `--radius-pill: 999px` · `--gutter: 20px` · `--maxw: 520px`

---

## 4. Page structure, in order

1. **Sticky header** — black. Brand lockup `LAUNDRY / LEGENDS` with orange star glyph, script tagline "Always Fresh", hamburger (toggles `aria-expanded` only — no menu exists yet)
2. **Hero** — black. `HOME` / `LAUNDRY` stacked, right-aligned script "Fresh & Effortless", white outline pill CTA, inline iron-with-steam SVG
3. **Life's too short** — centred headline, subline, body, two orange sparkle SVGs absolutely positioned
4. **"Take it off your list"** — dark grey card (`#2E2E2E`)
5. **"Reclaim your free time"** — white card, orange heading
6. **Our Process** — 4 white cards, each with a 120px inline SVG icon: basket, van, twin washers, iron
7. **Pricing** — title + orange rule, 4-bag illustration SVG (labelled WASHED/DRIED, IRONED/FOLDED, "& ready for pickup", branded back bag), personal bag wash card, ironing row, T&Cs list
8. **Request pickup CTA** — orange banner with white outline pill
9. **Clients** — blue headings, horizontal scroll-snap carousel, 5 dashed placeholder tiles
10. **Footer** — blue. Brand lockup, orange Order pickup button, two addresses, phone, 1800 number, copyright, white scalloped cloud SVG strip
11. **Floating mailing list pill** — fixed bottom-left, orange, dismissible

### Interactive behaviour

Two small IIFEs at the bottom of the file:
- **Mailing pill** — click within 44px of the left edge dismisses it (`.hidden`); clicking elsewhere sets `location.hash = '#mailing-list'` (placeholder, no target exists)
- **Hamburger** — opens the full-screen menu overlay (`#site-menu`): About us, Our services (Commercial Laundry, Home Laundry, Dry Cleaning, Sports Laundry), Price list. Built 19 Sep 2026 from three new screen recordings of the source site's menu. "Blankets for Brisbane" (the competitor's charity campaign) was deliberately omitted.
- **Contact page** — `contact.html`, built 19 Sep 2026 from the second source recording (competitor heading "Let's talk dirty" recharacterised to "Let's talk laundry", copy rewritten). Head Office / Service Centre placeholders, Call 1800 PICKUP, and a First name/Last name/Phone/Email/Message form. THE FORM HAS NO BACKEND — submit is intercepted with a notice. If it goes live it collects personal information: Privacy Act obligations and the missing Privacy Policy page (Blockers #6/#7) attach to it too.
- **Price list panel** — `#price-panel` slide-up sheet with Sports / Personal / T&C's pill tabs (scroll-to + scroll-spy), opened from the menu or the "View full price list" button in Pricing. ALL FIGURES TRANSCRIBED FROM THE COMPETITOR'S PANEL — covered by Blocker #5, replace before publish. Express service fee $68.45 included.

---

## 5. Complete copy inventory

Every user-visible string, in document order. Use this to diff against any future edit.

| Location | Copy |
|---|---|
| `<title>` | Home Laundry — Laundrylegends |
| Meta description | Home Laundry pickup and delivery from Laundrylegends. Fresh & effortless. Book a pickup online or call 1800 PICKUP. |
| Header brand | LAUNDRY / LEGENDS · *Always Fresh* |
| Hero | HOME / LAUNDRY · *Fresh & Effortless* · [Order pickup] |
| Section headline | Life's too short to spend it folding washing. |
| Subline | Hand it over — we've got it covered. |
| Body | Our Home Laundry service takes the grunt work off your plate in just a few taps. |
| Dark card h3 | Take it off your list |
| Dark card body | Book a pickup and your laundry day is done. We collect, wash, dry, fold — and if anything needs the full dry cleaning treatment, we handle that too — then bring it straight back to your door. |
| White card h3 | Reclaim your free time |
| White card p1 | More time with your kids, your partner, your mates… less time dealing with household chores that eat up your weekend. |
| White card p2 | We genuinely love doing this stuff. Seriously — it's our thing. |
| Process h2 | Our Process |
| Step 1 | **Order** — Book online or ring 1800 PICKUP and the Laundrylegends crew will be on their way. Consider it handled. |
| Step 2 | **Pick up** — A Laundrylegends van heads your way, one of our team jumps out, collects your washing and we're gone — quick as you like. |
| Step 3 | **Wash & Dry** — Whites sorted from colours, delicates kept separate — then washed, dried and neatly folded. Anything needing the full dry cleaning treatment gets that too, just say the word. |
| Step 4 | **Drop off** — Clean, fresh and ready to go — we bring it straight back to your door. All you have to do is put it away. |
| Pricing h2 | Pricing |
| Bag labels | WASHED / DRIED · IRONED / FOLDED · *& ready for pickup* · LAUNDRY LEGENDS *Fresh & Effortless* |
| Price card | *Personal bag wash* — Once a week pick up* **$59.95** |
| Price bullets | * 1 standard 7kg household washing machine load per week *(all items including underwear)* · * Up to 10 items ironed *(e.g. flat sheets/pillow cases)* · * Excludes business shirts, delicates and dry cleaning items · * Terms & conditions apply |
| Ironing | Ironing per piece — **$3** |
| T&Cs | * Advise us of items valued at over $250. Extra delicate & large items may incur higher charges · * All items identified as Dry Cleaning will be charged accordingly · * For personal bags, if over weight/specified number of pieces, extra charges may apply · * A basic wash is just that – provide us with the usual assortment of clothes your would normally put through a standard wash. No delicates. We have specific services for these items · * All prices include GST |
| CTA banner | Request pickup / online now · [Order pickup] |
| Clients h2 | We wash for / the best around |
| Clients lead | A few of our valued clients — you might recognise a name or two. |
| Client tiles | Italian Street Kitchen · Louis Vuitton · RNA · Australian Rugby · Brisbane Showgrounds |
| Footer brand | LAUNDRY / LEGENDS · *Always Fresh* · [Order pickup] |
| Footer addresses | **Head Office** — 42 Fresh Lane, Brisbane, QLD 4000 · **Service Center** — Unit 5, 168 Distribution Drive, Coorparoo, QLD 4151 |
| Footer phone | T: (07) 3555 1800 · Call 1800 PICKUP |
| Footer legal | © Copyright 2026 Laundrylegends \| All rights reserved \| Privacy Policy |
| Mailing pill | × Mailing list |

### Known copy defects (inherited from the source page, deliberately preserved)

- T&Cs bullet 4: *"clothes **your** would normally"* — should be "you". Carried over from the original transcription. **Fix before go-live.**
- "Service Center" uses US spelling. Should be "Centre" for Australian English. **Fix before go-live.**

---

## 6. Rebrand change log (commit `40112f9` → `30ea2f6`)

| Element | Before | After |
|---|---|---|
| Brand name | LAUNDRY / AUSTRALIA | LAUNDRY / LEGENDS |
| Tagline | Delivering More | Always Fresh |
| Display font | Barlow Condensed 900 | Anton 400 |
| Hero script | Clean & Simple | Fresh & Effortless |
| Headline | Life's too busy to waste precious time doing laundry. | Life's too short to spend it folding washing. |
| Subline | Let us do it for you! | Hand it over — we've got it covered. |
| Dark card | Simplify your life | Take it off your list |
| White card | Get back to doing what you love | Reclaim your free time |
| Sign-off | Loonies hey? | Seriously — it's our thing. |
| Order step | Delegation done. | Consider it handled. |
| Pick up step | super schmick HOME LAUNDRY vans | A Laundrylegends van |
| Clients h2 | It all comes out in the wash | We wash for the best around |
| Clients lead | Not to name drop, but here's just a few of our valued clients. | A few of our valued clients — you might recognise a name or two. |
| Dry cleaning ref | "our Plus Dry Cleaners intensive care treatment" | "the full dry cleaning treatment" |
| Head Office | 20 Propriety Street, Tingalpa QLD 4173 | 42 Fresh Lane, Brisbane QLD 4000 (**fake**) |
| Second address | Plus Dry Cleaners Stores, Yeronga | Service Center, Coorparoo (**fake**) |
| Phone | (07) 3848 3775 | (07) 3555 1800 (**fake**) |

---

## 7. BLOCKERS — do not publish until these are cleared

These are the things that will cause real problems if the page goes live as-is. Ranked by exposure.

| # | Blocker | Why it matters | Owner | Due |
|---|---|---|---|---|
| 1 | **Client logos are third-party trademarks** — Louis Vuitton, RNA, Australian Rugby, Brisbane Showgrounds, Italian Street Kitchen | These were transcribed from a *competitor's* client list. Presenting them as Laundrylegends' clients is a misleading-conduct exposure under Australian Consumer Law, and a trademark issue on top. They are currently dashed placeholder tiles, not logos — keep it that way until each client has confirmed in writing. | Callum Page | Before any publish |
| 2 | **"Order pickup" CTAs point to `drycleaning.com.au`** | That is the competitor's booking system. Four links on the page. Must be repointed to Laundrylegends' own booking flow. | Callum Page | Before any publish |
| 3 | **1800 PICKUP is the competitor's number** | Appears in the meta description, Step 1 copy and the footer. Replace with Laundrylegends' own number. | Callum Page | Before any publish |
| 4 | **Contact details are fabricated** — 42 Fresh Lane; Unit 5, 168 Distribution Drive; (07) 3555 1800 | Inserted as placeholders on request. They are not real addresses. Publishing a fake business address is a compliance problem. | Callum Page | Before any publish |
| 5 | **Pricing is the competitor's pricing** — $59.95/week, $3/piece, $250 declaration threshold, 7kg load, 10 ironed items | Every figure on this page came from the competitor's page via screen recording. None has been set by Laundrylegends. All prices are stated GST-inclusive, which is correct for AU — but the numbers themselves need to be Laundrylegends' own. | Max Jones (pricing model) → Callum Page (implement) | Before any publish |
| 6 | **Privacy Policy link is a dead `/privacy-policy/`** | No such page exists. Required if any mailing-list capture goes live. | Callum Page | Before mailing list activates |
| 7 | **Mailing list pill does nothing** | Sets a URL hash pointing at nothing. Either wire it to a real capture form or remove it. If wired, it collects personal information — Privacy Act obligations attach. | Callum Page | Before any publish |
| 8 | **Copy defects** — "your would normally" typo; "Service Center" US spelling | Small, but visible. | Callum Page | Before any publish |

> **Legal boundary:** The above flags commercial and compliance *risk*. It is not legal advice. Items 1, 4, 6 and 7 should go to the venture's solicitor with a short brief before the page is published.

---

## 8. Outstanding build tasks (non-blocking)

| Task | Detail | Owner | Due |
|---|---|---|---|
| Replace client tiles | Drop real logo files into `site/laundry-australia/assets/`, swap each `<div class="placeholder">` for `<img src="assets/name.svg" alt="Name" />`. Instructions already in `assets/README.md`. Gated on Blocker #1. | Callum Page | On client sign-off |
| ~~Build the nav menu~~ | Done 19 Sep 2026 — menu overlay + price-list panel built from new source recordings. Menu links except Home Laundry are `#` placeholders (no other pages exist yet) | Callum Page | Done |
| Rename the directory | Folder is still `site/laundry-australia/` — misleading post-rebrand. Suggest `site/laundrylegends/`. | Callum Page | Next session |
| Desktop breakpoint | Only one breakpoint exists (`≥640px`, type sizes only). Layout is single-column at every width. | Callum Page | TBC |
| Audit workflow results | An Ultracode audit (`wf_9a84a40c-512`) comparing all 56 source frames against the build across 6 dimensions was launched and never reviewed. Results may still be retrievable in the prior session. | — | Optional |

---

## 9. Technical notes for the next session

- **No build step.** Open the file in a browser. That's it.
- **No dependencies** except the three Google Fonts. Everything else — every icon, every illustration, the cloud strip — is inline SVG written from scratch. No assets were copied from the source site.
- **Rendering/verification:** headless Chromium at `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`. Launch with the proxy configured or webfonts won't load.
- **If fonts don't render in a screenshot**, it's the proxy, not the CSS. Barlow Condensed reported `False` on a font-availability check during the original build while visually rendering correctly.
- **The clouds SVG** uses `preserveAspectRatio="none"` and a series of `A` arc commands of differing radii along a baseline. Editing radii changes bump width; the `Z` close and the `L500 110` baseline must stay.
- **Git:** develop on `claude/laundry-australia-landing-page-g9nuvw`. Push with `git push -u origin claude/laundry-australia-landing-page-g9nuvw`. No PR has been opened.

---

## 10. Full source

The complete file is `site/laundry-australia/home-laundry.html` in the repo at commit `30ea2f6`. It is 871 lines. Rather than reproducing it here, pull it directly:

```bash
git clone https://github.com/xrcallum/King-laundry-
cd King-laundry-
git checkout claude/laundry-australia-landing-page-g9nuvw
open site/laundry-australia/home-laundry.html
```

If the new Claude session has no repo access, the HTML file has been sent alongside this document — hand it over directly and ask it to work from that.

---

*Handoff prepared 19 September 2026. Every figure and claim above is traceable to the repository at commit `30ea2f6` or to the three source screen recordings, except where explicitly labelled **fake**, **ASSUMPTION** or **UNVERIFIED**.*
