# Laundrylegends — Home Laundry Landing Page
## Complete Handoff Document

**Prepared:** 19 September 2026
**Last revised:** 19 September 2026 — live publish, green `+` pricing
**Venture:** Laundrylegends
**Owner:** Callum Page
**Repo:** `github.com/xrcallum/King-laundry-`
**Branch:** `claude/push-latest-chats-live-xnijoo`
**Files:** `site/laundry-australia/index.html` and `contact.html` (self-contained, no build step)
**Live:** https://claude.ai/artifact/11cT6RXSi4G3EprLXGzFqE — private, visible only to the owner and anyone the owner shares it with
**Booking flow:** a separate artefact, `SJihvya38JukdcAUL7JiFx`, which every Book/Club/legal link targets

> The two files in this folder are byte-identical to what is published at that URL. `index.html` is the home-laundry page; the artefact serves it as the site root. If you change one, republish both.

---

## 1. PASTE THIS INTO THE NEW CLAUDE FIRST

> I'm continuing work on the Laundrylegends home-laundry landing page. It's two self-contained HTML files — no build step, no dependencies beyond three Google Fonts. They live at `site/laundry-australia/index.html` and `contact.html` on branch `claude/push-latest-chats-live-xnijoo` in `github.com/xrcallum/King-laundry-`, and they are byte-identical to what is published at https://claude.ai/artifact/11cT6RXSi4G3EprLXGzFqE. Change the repo files and republish both to that URL together.
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

> **HISTORY — superseded.** This inventory, and the change log in section 6, describe the earlier build that mirrored the competitor's page. The live page carries different copy and its own pricing. Read section 7 for what is actually published. Kept here because it records where the original material came from.

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

## 7. BLOCKERS — all eight cleared, 19 September 2026

The page that is live carries none of the competitor-derived material the original eight blockers described. Every one was checked against the published files before this revision, not assumed.

| # | Original blocker | How it was cleared | Verified |
|---|---|---|---|
| 1 | Client logos were third-party trademarks (Louis Vuitton, RNA, Australian Rugby, Brisbane Showgrounds, Italian Street Kitchen) | The client carousel was removed from the page entirely. No client is named anywhere. | No match for any of the five names in either file |
| 2 | "Order pickup" CTAs pointed at `drycleaning.com.au` | Every Book/Club/legal link now targets the venture's own booking artefact `SJihvya38JukdcAUL7JiFx`. | No match for `drycleaning.com.au` |
| 3 | 1800 PICKUP was the competitor's number | No phone number is published. The footer states "Phone line being connected." | No match for `1800 PICKUP` |
| 4 | Contact details were fabricated (42 Fresh Lane; Unit 5, 168 Distribution Drive; (07) 3555 1800) | All removed. The footer publishes no address and states "Email to be published." | No match for any of the three |
| 5 | Pricing was the competitor's pricing | Replaced with Laundrylegends' own launch pricing, set by the venture: $32.00 a load (~5 kg), $13.50 flat collection and return, Legends Club $63.70/$89.70/$115.70 a week. Labelled "Launch pricing, under review and subject to change". GST-inclusive, AUD. | Every `$` figure on the page is from the new schedule |
| 6 | Privacy Policy link was a dead `/privacy-policy/` | Now points at the booking artefact's `#/privacy`. The footer states the policy and terms are "drafts for legal review and not yet in force". | Link resolves; disclaimer present |
| 7 | Mailing list pill did nothing | Removed. The page captures no personal information, so no Privacy Act obligation attaches to it. | No match for `mail-pill` |
| 8 | Copy defects — "your would normally", "Service Center" | Both strings are gone; the surrounding copy was rewritten. | No match for either |

**Still open before a public launch** — these are not page bugs, they are facts the business does not yet have:

| Item | Detail | Owner | Due |
|---|---|---|---|
| Company name and ABN | The footer says "Company name and ABN to be published on registration". Australian Consumer Law expects a trading entity to be identifiable. | Max Jones | On registration |
| Phone and email | Footer currently promises both without giving either. Publish them or drop the promise. | Callum Page | Before a public launch |
| Privacy policy and Terms | Both are drafts and flagged as not in force. They need to be in force before any personal information is collected — the booking flow collects it. | Callum Page → solicitor | Before the booking flow goes public |
| Pricing sign-off | The schedule is labelled launch pricing under review. Confirm it is the intended commercial position. | Max Jones | Before a public launch |

> **Legal boundary:** the above flags commercial and compliance *risk*. It is not legal advice. The company-name, privacy and terms items should go to the venture's solicitor with a short brief.

---

## 8. Outstanding build tasks (non-blocking)

| Task | Detail | Owner | Due |
|---|---|---|---|
| ~~Replace client tiles~~ | Moot — the client carousel was removed from the page. If clients are ever named, each must confirm in writing first. | — | Done |
| ~~Build the nav menu~~ | Done 19 Sep 2026 — menu overlay and price-list panel. | Callum Page | Done |
| ~~Fix dead nav links~~ | Done 19 Sep 2026, twice — the brand logo and the "Home laundry" menu item on both pages pointed at `home-laundry.html`, which the artefact does not serve. Fixed to `index.html`, then reintroduced when a second session republished from an older copy, then fixed again the same day. If this keeps happening: whoever edits this page next should read the live artefact with the Artifact tool before publishing, not work from a stale local copy. | Callum Page | Done |
| ~~Interactive estimator~~ | Done 19 Sep 2026 — the static price card in Pricing was replaced with a live estimator (load stepper, add-on toggles, running total) and the five process steps became a numbered rail. Built by a different session; merged in without losing the link fix or the price-panel `+` treatment (see below). | — | Done |
| ~~Operator portal — first version~~ | Done 19 Sep 2026 — `portal.html`, published alongside the other two pages but not linked from the public nav. See §11. | Callum Page | Done, not final |
| Rename the directory | Folder is still `site/laundry-australia/` — misleading post-rebrand. Suggest `site/laundrylegends/`. Deferred because it breaks every path reference in this document. | Callum Page | Next session |
| Desktop breakpoint | Only one breakpoint exists (`≥640px`, type sizes and the step grid). Layout is single-column at every width. | Callum Page | TBC |
| Audit workflow results | An Ultracode audit (`wf_9a84a40c-512`) comparing all 56 source frames against the build was launched and never reviewed. Largely superseded: the page no longer mirrors the source. | — | Optional |

---

## 9. Technical notes for the next session

- **No build step.** Open the file in a browser. That's it.
- **No dependencies** except the three Google Fonts. Everything else — every icon, every illustration, the cloud strip — is inline SVG written from scratch. No assets were copied from the source site.
- **Rendering/verification:** headless Chromium at `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`. Launch with the proxy configured or webfonts won't load.
- **If fonts don't render in a screenshot**, it's the proxy, not the CSS. Barlow Condensed reported `False` on a font-availability check during the original build while visually rendering correctly.
- **The clouds SVG** uses `preserveAspectRatio="none"` and a series of `A` arc commands of differing radii along a baseline. Editing radii changes bump width; the `Z` close and the `L500 110` baseline must stay.
- **Git:** develop on `claude/push-latest-chats-live-xnijoo`. Push with `git push -u origin claude/push-latest-chats-live-xnijoo`.
- **Publishing:** the repo files and the live artefact must stay byte-identical. Publish `index.html` as the page and `contact.html` and `portal.html` alongside it, all in the same call, to https://claude.ai/artifact/11cT6RXSi4G3EprLXGzFqE. Publishing without that URL creates a second artefact instead of updating the live one.
- **The artefact serves `index.html` as the site root.** Nothing resolves `home-laundry.html` — any link to that name is dead. Internal links must use `index.html`, `contact.html` and `portal.html`.
- **Two sessions edited this artefact concurrently on 19 Sep 2026.** One added the interactive estimator and process rail; another (this one) was mid-publish of the price-panel `+` treatment when the first session's version went live, which silently reintroduced the dead-link bug and dropped the `+` from the price-panel rows (the on-page estimator and rate chips kept theirs — they were built fresh with it). Both were re-fixed and merged rather than one side overwriting the other. **Before publishing, always call the Artifact tool's `read` action on the live URL first** — a `publish` built on a stale copy is refused with a pointer to the newer version, but by then you've already done the work twice.

---

## 10. Full source

The complete files are `site/laundry-australia/index.html`, `contact.html` and `portal.html`. Rather than reproducing them here, pull them directly:

```bash
git clone https://github.com/xrcallum/King-laundry-
cd King-laundry-
git checkout claude/push-latest-chats-live-xnijoo
open site/laundry-australia/index.html
```

If the new Claude session has no repo access, the HTML files have been sent alongside this document — hand them over directly and ask it to work from those.

---

## 11. Operator portal (`portal.html`) — first version, not final

**Status:** a working prototype, published live alongside the public pages but not linked from any public nav. Reachable only if someone has the direct URL path.

**What it does:** an operator signs in with a name only (no password, no identity check — see limitations), sees an example round of three stops in suburbs drawn from the real coverage list, and for each stop can open a weigh-and-price sheet that calculates the total from the venture's own published rates — the same $32.00/load, +$15.00 Premium Clean, +$3.50 Eco add-on, $13.50 flat collection and return, and $73.50 one-off minimum (waived for Legends Club members) that appear on the public price list. The total shown is verified to match the worked example on the home page ($77.50 for 2 loads, no add-ons, not a Club member). A status ladder tracks each stop through Scheduled → Collected → Washing → Ready → Delivered.

**What it deliberately does not do, and why:**
- **No real bookings feed.** The round shown is example data, clearly labelled as such. There is no backend to receive a real booking yet.
- **No real sign-in.** A name typed into a box is not authentication. Building real operator identity — who they are, whether they're screened, what they're allowed to see — is a security decision, not a styling one.
- **Nothing is stored centrally.** Job status is kept in the browser's local storage only: per device, not shared with anyone, gone if site data is cleared. A shared database is available (the `db` capability) but wasn't added here, because turning it on means deciding what real operator and customer data gets stored and for how long — a Privacy Act question, not a code change, once real personal information is involved.
- **No payment processing.**
- **How operators are engaged is out of scope for this page.** Contractor vs employee status, ABN, Super obligations, WHS, insurance — these are legal and commercial questions for the venture's advisers. The portal's copy is deliberately neutral ("your round", "confirm and continue") rather than anything that implies an employment relationship, but this page does not decide the actual engagement terms and shouldn't be read as having done so.

**Before this becomes the operators' real tool**, in rough order: decide on and build real sign-in, decide on and wire a shared database for round data (this is also when the venture needs a privacy-policy decision, since it stops being a static site once it stores anyone's personal information), connect it to an actual bookings source, and get the AU compliance items above signed off with an adviser.

---

*Handoff prepared 19 September 2026, revised twice the same day — once after the first live publish, again after merging a concurrent session's changes and adding the operator portal. Every figure and claim above is traceable to the repository on `claude/push-latest-chats-live-xnijoo`, except where explicitly labelled **ASSUMPTION** or **UNVERIFIED**. Sections 5 and 6 describe the earlier competitor-derived build and are kept as history; section 7 states what is actually live.*
