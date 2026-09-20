# Linen Legends — Site rebuild plan (React + API)

**Prepared:** 20 September 2026 · **Revised:** 20 September 2026 (rebrand + scope update, §12) · **Owner:** Callum Page · **Venture:** Linen Legends (renamed from Laundrylegends by Callum Page in this conversation, 20 Sep 2026 — see §12.1)
**Branch:** `claude/laundry-legends-build-qmcafm` · **Repo:** `github.com/xrcallum/King-laundry-`
**Filing:** code pending — README flags the `LKG` vs `LL` prefix as an open filing decision (Max Jones). The rebrand strengthens the case for `LL` (fits both "Legends" and "Linen Legends"), but the decision itself stays with Max Jones. File under SYS09 once decided.
**Status:** v2 — plan only. Nothing has been built yet. §1–§11 are the original plan; §12 records the 20 Sep rebrand and scope changes and supersedes any conflicting text above it (brand name, domain, milestone count).

---

## 0. Recommendation

**Superseded by §12 — read that section first.** Build the site and its API as **one Vite + React app at the repo root with the API as Vercel serverless functions under `api/`**, deployed to Vercel (its MCP connector is already attached to this workspace). §6 now runs this as **six milestones**, not four — the booking/account app Callum brought into scope on 20 Sep 2026 (§12.5) adds two real app surfaces (`/account`, `/messages`), not a copy change. Lift every line of copy, every price and every postcode **programmatically from the existing site file** (`site/laundrylegends-site.html`) rather than retyping it, with a brand find-and-replace pass (Laundrylegends → Linen Legends) baked into that extraction step. Keep the existing artefact live under its current brand until the new site passes the acceptance checklist in §7. §3 plus §12 hold the full decision list; everything else is locked here.

---

## 1. Where we are (verified 20 Sep 2026)

| Fact | Evidence |
|---|---|
| The repo has **no React, Tailwind, Node backend or package.json**. | Root contains `site/`, `dossier/`, `tools/`, `verify/`, `docs/` only. |
| The current site is **one 505 KB HTML file** (`site/laundrylegends-site.html`) published as a Claude artefact with a `db` capability, plus a 3-file mobile landing page in `site/laundry-australia/`. | README §Layout; HANDOFF.md §9. |
| The attached PDF (`LaundryKings-site-preview.pdf`, 49 pages) is a **render of that single-file site under the old brand**. It is byte-identical to the copy in the repo root. | `cmp` of upload vs repo file. |
| The PDF shows **15 public pages**, not 12: the 12 in the build sequence plus **/pricing, /privacy, /terms**, and 8 pages of the customer app (My Account, bookings, messages, settings). | PDF pp. 11–12, 34–41, 42–49. |
| **Pricing of record** already exists as a constant block (`DEFAULT_PRICING`): load $32.00, delivery $13.50, minimum $73.50, eco add-on $3.50, sheet set $24, blanket $32, rug $42, dry-clean dress $16.50 / jacket $18.50 / suit $32, doona $45 / $75, curtain $38, Legends Club $63.70 / $89.70 / $115.70 per week. GST-inclusive AUD. Labelled "launch pricing, under review". | Site file lines 4162–4181; HANDOFF §7 item 5. |
| **Coverage of record** exists as two maps: 16 live postcodes (`LIVE_PC`) and 14 opening-soon postcodes (`SOON_PC`). **4000 is currently "opening soon", not active.** 4509 (Mango Hill) is opening soon. 9000 is in neither. | Site file lines 4191–4200. |
| The **order reference generator** already produces `LL-` + 6 uppercase base-36 characters. | Site file line 5031, `REF()`. |
| **Estimator rule of record**: subtotal + delivery, then `max(minimum, subtotal)` with a visible "Minimum order adjustment" line. | Site file `estimate()` lines 5099–5121. |
| **12 FAQs, the guarantee text, the operator disclosure and the NDIS / AS/NZS 4146 statements** exist verbatim and must travel unchanged. | Site file `FAQS` array; README §Rules; HANDOFF §7. |
| The **BACKEND SPEC** the build sequence refers to is **not in the repo, the PDF or any doc**. | `grep -ri "backend spec"` returns nothing. §4 reconstructs it from the site's own logic. |
| Environment: Node 22.22, npm 10.9, Python 3.11, Chromium 1194 (Playwright), npm registry reachable through the proxy (vite 8.3.0, tailwindcss 3.4.19, lenis 1.3.26, react-router-dom 7.18.4, express 5.2.1 all resolve). | Checked this session. |
| Business go-live blockers (company name + ABN, phone, email, privacy/terms in force, pricing sign-off) are **open and owned by the business**, not the build. | HANDOFF §7 "Still open". |

---

## 2. Target stack and hosting

### 2.1 Stack (locked)

| Layer | Choice | Why |
|---|---|---|
| Build tool | **Vite 8 + React 19** | Fastest install and dev loop; the build sequence names `App.js`, `Reveal.jsx` etc. Vite needs `.jsx` for JSX, so the entry is `src/App.jsx`. |
| Styling | **Tailwind CSS 3.4** (pinned, not v4) | The sequence specifies `tailwind.config.js` with theme keyframes. Tailwind 4 moved config into CSS and would force a rewrite of that step. |
| Smooth scroll | **lenis 1.3** | As specified. One instance in `App.jsx`, destroyed on unmount. |
| Routing | **react-router-dom 7** | 12 routes + 3 static legal/pricing routes + 404. |
| Reveal / kinetic / marquee | **Hand-rolled with IntersectionObserver and CSS keyframes** | No framer-motion or GSAP. Keeps the bundle small and avoids a licence question. |
| API | **Vercel serverless functions in `api/`**, each a plain `(req, res)` handler | Zero servers to run. Same handler files are mounted by a tiny Express dev server (`server/dev.js`) so `curl` tests work locally. |
| Data | Shared modules in `api/_lib/` (`pricing.js`, `coverage.js`, `ref.js`, `store.js`) | One source for prices and postcodes, imported by both the API and, at build time, by `src/data/site.js`. |
| Persistence | See §2.3 | |

### 2.2 Hosting

| Option | Fit | Verdict |
|---|---|---|
| **Vercel: static Vite build + `api/` functions** | Connector already attached. Free Hobby tier covers launch traffic. Custom domain: `linenlegends.com.au` — registered 20 Sep 2026 (§12.2), attaches at cut-over; a Vercel-issued `*.vercel.app` URL serves previews until then. | **(Recommended)** |
| Keep publishing as a Claude artefact | Artefacts serve static HTML only. `/api/*` cannot exist, so every form in the spec fails. | Not viable for this spec. |
| Render / Railway with an always-on Express server | Works, but adds a paid always-on process and a second deploy pipeline. | Only if Vercel is refused. |

### 2.3 Persistence for bookings, enquiries and waitlist

| Option | Fit | Verdict |
|---|---|---|
| **Ops Sheet via its Apps Script web-app endpoint** (`OPS_SHEET_WEBHOOK` env var) | The Ops Sheet is the venture's Data Spine (source of truth #2). Bookings and enquiries land where ops already works. No new system. | **(Recommended)** — needs the endpoint URL (decision D6). |
| Vercel KV / Postgres | Adds a store nobody reads day to day. | No. |
| Local JSON file (`data/*.json`, git-ignored) | Not durable on serverless. | **Dev fallback only.** Handlers write here when the webhook env var is absent, so curl tests pass before the Sheet is wired. |

The existing artefact's `db` already holds bookings from the current site. Once the new site is live, that store is frozen (read-only) so there is one live record. Owner: Callum Page, at cut-over.

---

## 3. Decisions to lock before Milestone 1

> **Ask this person: Callum Page** — D4 and D7 are resolved below (20 Sep 2026); D10–D11 are new. D1, D2, D3, D5, D8, D9 were not addressed in the follow-up and their defaults apply, labelled ASSUMPTION in the code, until Callum says otherwise.

| # | Decision | Options (best first) | Status |
|---|---|---|---|
| D1 | **Postcode 4000.** Your checklist says 4000 → active. The coverage data of record says 4000 → opening soon. | (a) Keep data of record (4000 = opening) and change the test to a live postcode such as 4131 **(Recommended — no unverified coverage claim)** · (b) Move 4000 into `LIVE_PC` because an operator is confirmed for the CBD | Open — default (a) applies |
| D2 | **48-hour turnaround for blankets.** New rule; current copy says turnaround is "confirmed at booking". | (a) Estimator shows "Indicative turnaround: 48 h" for the linen service; FAQ and terms copy unchanged **(Recommended)** · (b) Publish 48 h as a commitment across the site | Open — default (a) applies |
| D3 | **Pricing, Privacy and Terms pages** exist in the PDF but are not in the 12 routes. Footer links point at them. | (a) Add `/pricing`, `/privacy`, `/terms` as static routes rendered from extracted copy — three small files **(Recommended)** · (b) Drop them and remove the footer links | Open — default (a) applies |
| ~~D4~~ | ~~Customer app and operator portal are outside the 12 routes.~~ | — | **Resolved 20 Sep 2026 — reversed.** Callum: bring the actual booking-process app in, "mastered... Uber/service-style". Now Milestone 4 (§6). D10 covers the one open sub-question (tracking depth). |
| D5 | **BACKEND SPEC.** Not in the repo. | (a) Paste it and I diff it against §4 · (b) Accept §4 as the spec **(Recommended if it matches your memory of it)** | Open — default (b) applies |
| D6 | **Ops Sheet webhook URL** for bookings/enquiries. | Provide the Apps Script web-app URL, or confirm the Sheet has no script yet and I add the `doPost` handler to the single Ops Runner script in a later step | Open — dev JSON fallback meanwhile (action in §10) |
| ~~D7~~ | ~~Brand string.~~ | — | **Superseded 20 Sep 2026 by the rebrand (§12.1).** Now "Linen Legends" (two words) and "Legends Club" (ASSUMPTION — "Legends Club" reads fine under the new name and needs no rework; say so if you want it changed, e.g. to "Linen Club"). |
| D10 | **Booking-status tracking depth (new, §6 Milestone 4).** A real timestamped status timeline is in scope now. A live-moving-van map is a second product (needs an operator app streaming GPS). | (a) Status timeline only at launch, live map is a phase-2 project **(Recommended)** · (b) Scope the live map now — this is materially larger than everything else in this plan combined | Open — default (a) applies |
| D11 | **Filing prefix**, now that the venture is confirmed as Linen Legends. | (a) `LL` — fits "Legends" and "Linen Legends" both **(Recommended)** · (b) Something else | Stays Max Jones's call per README; not mine or Callum's to set |

---

## 4. Backend spec (reconstructed from the site of record)

All endpoints JSON, GST-inclusive AUD, `Cache-Control: no-store`. Every handler validates input and returns `{ ok:false, error:"<code>", message:"<plain English>" }` on a 400.

| Endpoint | Method | Input | Output | Rule source |
|---|---|---|---|---|
| `/api/estimate` | POST | `{ service:'wf'|'linen'|'dc'|'bulky', qty:int≥1, eco?:bool, bags?:int, postcode?:string }` | `{ ok, lines:[{label,amount}], subtotal, delivery, minimumApplied:bool, total, turnaround:'next-day'|'48h'|'quoted', gstIncluded:true, indicative:true }` | `estimate()` lines 5099–5121; D2 for turnaround |
| `/api/coverage/check` | GET `?postcode=4131` | `{ ok, postcode, status:'active'|'opening'|'waitlist', suburb?:string, message }` | `LIVE_PC` / `SOON_PC`; D1 |
| `/api/waitlist` | POST | `{ postcode, email, suburb? }` | `{ ok:true, id }` | New (spec: "waitlist + email capture") |
| `/api/bookings` | POST | `{ service, qty, eco?, bags?, name, phone, email, address, suburb, postcode, date, window, notes?, consent:true }` | `{ ok:true, id:'LL-XXXXXX', estimate:{…as /api/estimate…}, status:'awaiting-operator' }` | `REF()` line 5031; booking fields from the current `#/book` form |
| `/api/enquiries` | POST | `{ kind:'business'|'supported-living'|'operator', …form fields }` | `{ ok:true, id }` | PDF pp. 15, 17, 22 form fields |
| `/api/contact` | POST | `{ name, email, phone?, topic, message, complaint:bool }` | `{ ok:true, id }` | PDF pp. 32–33 |

**Pricing engine (`api/_lib/pricing.js`):** the `DEFAULT_PRICING` object copied verbatim, one exported `estimate()` that is the only place arithmetic happens. The client never computes money; `src/lib/api.js` calls `/api/estimate` and renders what comes back (with a local mirror only for instant UI while the request is in flight, sourced from the same generated constants).

**Expected results under pricing of record** (for the curl gate in §7):

| Input | Lines | Total |
|---|---|---|
| `wf`, qty 2 | 2 × wash & fold $64.00 · Collection & return $13.50 | **$77.50**, `minimumApplied:false` |
| `wf`, qty 1 | 1 × wash & fold $32.00 · Collection & return $13.50 · Minimum order adjustment $28.00 | **$73.50**, `minimumApplied:true` |
| `linen`, qty 3 | 3 × blanket $96.00 · Collection & return $13.50 | **$109.50**, `turnaround:'48h'` (D2) |

**Persistence (`api/_lib/store.js`):** `save(collection, record)` posts to `OPS_SHEET_WEBHOOK` when set, otherwise appends to `data/<collection>.json` (git-ignored). Both paths return the same `id`.

**Rate limiting and spam:** honeypot field on every form; 20 requests/min/IP in-memory guard in the dev server; Vercel's edge handles the rest. No CAPTCHA at launch.

**Privacy:** bookings collect personal information. The Privacy Policy is a draft "not in force" (HANDOFF §7). The booking route stays behind a visible "Pre-launch — bookings are registrations of interest" banner until Callum confirms the policy is in force (§10). This is a compliance flag, not legal advice.

---

## 5. Credit-efficiency rules for the build sessions

These are the rules that make the difference. Each is a concrete instruction to the session running the build.

1. **Four turns, not twelve.** The sequence was written for a chat model that needs one step per message. In Claude Code one turn can execute several steps and verify them with a script. Re-reading context is the largest recurring cost, so fewer, larger turns win. The cost is a bigger blast radius per turn, which the commit gate at the end of each milestone contains.
2. **Never retype copy.** `tools/extract_site_data.mjs` parses `site/laundrylegends-site.html` once and emits `src/data/site.js` (FAQs, pricing, postcodes, guarantee, services, club plans, JSON-LD). Generated, not authored. Re-run it if the source file changes.
3. **Write, don't re-read.** After a `Write`, trust the harness. Verification is the script in §7, not a second read of the file.
4. **One screenshot script, run once per milestone.** `verify/shots.mjs` renders every route at 390 px and 1280 px into a single contact sheet and captures console errors. No per-component screenshots.
5. **Pin and install once.** Exact versions in `package.json`, lockfile committed, `npm ci` thereafter.
6. **Model by milestone.** Milestones 1 and 4 (arithmetic, API contracts, final audit) on the current model. Milestones 2 and 3 (component and page assembly from fixed copy) on Sonnet. This follows the organisation's default-Sonnet rule and puts the expensive model only where a wrong number costs money.
7. **No web fetches, no exploratory greps.** Everything the build needs is in this document, the site file and the PDF text already extracted. If something is missing, it is a §3 decision, not a search.
8. **Reference, don't paste.** Kick off each milestone with one line: "Run Milestone N of `docs/laundrylegends-build-plan.md`." The session reads the section it needs.
9. **Fail fast on numbers.** The curl gate runs before any UI work in a milestone. A wrong total stops the turn.
10. **Commit at every gate**, push once per milestone. The container is ephemeral.

---

## 6. Build sequence as six milestones

**Updated 20 Sep 2026:** two milestones added — M4 (booking and account experience) and M5 (motion and premium design polish, the effects triaged in §11 plus the Apple/BMW-style pass Callum asked for in §12). The original Milestone 4 is renumbered Milestone 6 and unchanged otherwise. Each milestone maps to the numbered steps in the original build sequence, plus the additions below. "Gate" is what must be true before the milestone is committed.

### Milestone 1 — Foundations (steps 1–3)

| Item | Detail |
|---|---|
| Scaffold | `package.json` at root; `vite.config.js` with `/api` proxied to `server/dev.js` on port 8787; `.gitignore` adds `node_modules/`, `dist/`, `data/`. |
| Backend | `api/_lib/{pricing,coverage,ref,store}.js`; `api/estimate.js`, `api/coverage/check.js`, `api/waitlist.js`, `api/bookings.js`, `api/enquiries.js`, `api/contact.js`; `server/dev.js` mounts them with Express. |
| Data | `tools/extract_site_data.mjs` → `src/data/site.js`. |
| Design system | `tailwind.config.js`: `navy` and `ember` scales, `display` / `body` / `mono` font families, `marquee` and `float` keyframes. `src/index.css`: tokens, `.btn` `.input` `.card`, grain overlay, clip-frames, duotone, spotlight, marquee, selection, scrollbar. `index.html`: title, description, Open Graph, theme colour, fonts preconnect. |
| Shell | `src/App.jsx` (Lenis + router + 15 routes + scroll-to-top), `Reveal.jsx`, `Kinetic.jsx`, `Marquee.jsx`, `Section.jsx`, `lib/api.js`, `Navbar.jsx`, `Footer.jsx`, `pages/Home.jsx` placeholder. |
| Gate | `verify/smoke.sh` passes the six curl cases in §7.1; `npm run build` exits 0; shots script shows Navbar + Footer at both widths with zero console errors. |
| Commit | `site: M1 foundations — API, design system, shell` |

### Milestone 2 — Home and tools (steps 4–8)

| Item | Detail |
|---|---|
| Home hero | Masked line reveal, parallax hero image, three badges, estimate card (mirrors §4 expected 2-load result live from the API). |
| Home sections | Marquee, manifesto, three steps, services grid, club teaser with the "two ad-hoc loads ≈ $77.50 vs Solo $63.70" comparison, reviews, FAQ teaser, CTA. Copy from `site.js`. |
| Tools | `Estimator.jsx` (service, qty, eco, bags; POSTs `/api/estimate`; stores result in a small context for `/book`), `PostcodeChecker.jsx` (three states; waitlist state reveals the email field and POSTs `/api/waitlist`). |
| Forms | `BookingForm.jsx`, `EnquiryForm.jsx` (kind prop), `FAQAccordion.jsx` (one open at a time, `aria-expanded`). |
| Gate | Estimator UI shows $77.50 / $73.50 / $109.50 for the three cases; checker shows the three states; shots at both widths; zero console errors. |
| Commit | `site: M2 home, estimator, postcode checker, forms` |

### Milestone 3 — Pages (steps 9–11, plus D3 routes)

| Route | Source of copy |
|---|---|
| `/book` | Reads estimator context; falls back to service picker; on success shows `LL-XXXXXX` and the estimate. |
| `/contact` | PDF pp. 32–33; complaint checkbox escalates. |
| `/services` | PDF pp. 8–9 + pricing table pp. 11–12 if D3(b), otherwise link to `/pricing`. |
| `/legends-club` | PDF pp. 13–14; three plans; cancellation and pause terms verbatim. |
| `/coverage` | `LIVE_PC` / `SOON_PC` grouped by region; checker embedded. |
| `/business` | PDF pp. 15–16 incl. the AS/NZS 4146 statement; enquiry form kind `business`. |
| `/supported-living` | PDF pp. 17–18 incl. the NDIS registration statement; form kind `supported-living`. |
| `/operators` | PDF pp. 22–23 incl. the contractor-not-employee disclosure and "no income claims" block; form kind `operator`. |
| `/about` | PDF pp. 25–26. |
| `/guarantee` | PDF pp. 27–28 incl. the ACL not-limited statement. |
| `/faq` | 12 FAQs from `site.js`. |
| `/pricing`, `/privacy`, `/terms` | PDF pp. 11–12, 34–36, 38–40 (D3). Legal pages keep the "draft for legal review, not yet in force" banner. |
| Gate | All 15 routes render; every enquiry form returns `{ok:true}` via UI; shots; zero console errors. |
| Commit | `site: M3 all routes` |

### Milestone 4 — Booking and account experience, Uber/service-style (added 20 Sep 2026)

Callum: *"I want the app features of our actual booking process... mastered and turned from a simple AI build into a quality Uber/service-style booking visual."* Source is already in the repo — the customer-app routes inside `site/laundrylegends-site.html` (`#/app`, `#/bookings`, `#/account`, `#/messages`, `#/profile`, `#/invoices`, `bookingCard()`, the `S.messages` model) and `site/laundry-australia/portal.html`. No resend needed; `tools/extract_site_data.mjs` pulls the same source it already reads for pricing and copy.

**What "mastered" means concretely**, not just restyled:

| Item | Detail |
|---|---|
| Order status timeline | A five-to-seven-step stepper — Booked → Confirmed → Collector on the way → Collected → Washing → Ready → Delivered — each step timestamped once reached, large current-step type, Uber-style single-card layout. Ports the existing `status` field (`awaiting-operator`, `confirmed`, `complete`, `cancelled`) into the richer timeline; extra intermediate states are new. |
| **Not built now: live GPS tracking.** A moving van on a real map needs an operator app streaming real location — a second product, not a visual. **Decision D10** below. | The timeline above is real (driven by whatever status the booking record actually holds) — it is not a fake animation. It simply doesn't show a live-moving pin until there is a real feed. |
| `/account` | Bookings list (`bookingCard()` redesigned as a card list, filterable by status), profile, saved preferences (detergent, hang-dry, folding style — ported from the Legends Club "set your preferences" copy), addresses. |
| `/messages` | Notification list ported from `S.messages`, unread badge, read state. In-app only at launch — no push/SMS infrastructure exists yet. |
| Visual bar | White/near-white cards on the light theme, one accent (ember) for the active step and primary actions, generous spacing, large confident numerals for price and ETA — the reference is Uber's trip-status screen and Apple's order-tracking emails, not a dashboard. |
| API additions | `GET /api/bookings/:id` (poll for status), booking record gains `statusHistory:[{status,at}]`. Both additive to §4, no breaking change to `/api/bookings`. |
| Gate | A seeded booking walks through all timeline states in the UI; `/account`, `/messages` render with the same data the booking POST created; shots; zero console errors. |
| Commit | `site: M4 booking and account experience` |

### Milestone 5 — Motion and premium design polish (added 20 Sep 2026)

Applies §11's In-list (parallax, reveals, sticky stacking, progress bar, glass header, fullscreen nav, magnetic and liquid-fill buttons, tilt, glow borders, checkmark draws, bento grid) across every route built in M1–M4, then a dedicated Apple/BMW-style pass: type scale and spacing audited against an 8 px grid, section rhythm tightened, imagery treated with a consistent duotone/grain placeholder until real photography lands (§12.3), copy cut per §12.3 item 6 (roughly 40% shorter, compliance text untouched).

| Item | Detail |
|---|---|
| Motion pass | §11.2–§11.5 "In" items wired into `Reveal`/`Kinetic`/`Marquee`/`Section` and the new booking-app components from M4. |
| Design pass | Spacing and type scale audit against an 8 px grid; hero and section rhythm tightened; `<picture>` duotone/grain placeholder treatment on the one hero image until real photography (§12.3) replaces it. |
| Copy pass | Marketing page copy cut to roughly 40% of current length; every compliance sentinel (§8) and the guarantee/terms text stay verbatim and full length. |
| Gate | Web-vitals thresholds from §11.1 hold across all routes; shots contact sheet reviewed by Callum (§12.6) before M6. |
| Commit | `site: M5 motion and design polish` |

### Milestone 6 — Final pass and cut-over prep (was Milestone 4, renumbered)

| Item | Detail |
|---|---|
| Form audit | curl + UI for booking, contact and the three enquiry kinds; assert `{ok:true}` and an `id`. |
| Mobile nav | Open, close, route change closes menu, focus trap, `Escape`. |
| Console | Zero errors and zero warnings across all routes (15 marketing + `/account`, `/messages`) at 390 px and 1280 px. |
| Accessibility | Reuse `verify/a11y.js` pattern against the built `dist/`; fix contrast on ember-on-navy if flagged. |
| Compliance sentinels | Port the README rule into `verify/sentinels.mjs`: GST-inclusive statement, NDIS statement, AS/NZS 4146 statement, contractor and WHS statements, ACL not-limited statement, no invented entity text, no phone or email unless supplied, brand string is "Linen Legends" nowhere "Laundrylegends". Build fails if any is missing. |
| Deploy | Vercel preview deployment via the connector; smoke script re-run against the preview URL. |
| Commit | `site: M6 final pass — forms, nav, a11y, sentinels` |

---

## 7. Verification harness

### 7.1 `verify/smoke.sh` (curl gate, runs against `http://localhost:8787` or a preview URL)

| # | Request | Assert |
|---|---|---|
| 1 | `POST /api/estimate {"service":"wf","qty":2}` | `total == 77.50`, `minimumApplied == false` |
| 2 | `POST /api/estimate {"service":"wf","qty":1}` | `total == 73.50`, `minimumApplied == true` |
| 3 | `POST /api/estimate {"service":"linen","qty":3}` | `turnaround == "48h"`, `total == 109.50` |
| 4 | `GET /api/coverage/check?postcode=4131` (or 4000 under D1(b)) | `status == "active"` |
| 5 | `GET /api/coverage/check?postcode=4509` | `status == "opening"`, `suburb == "Mango Hill"` |
| 6 | `GET /api/coverage/check?postcode=9000` | `status == "waitlist"` |
| 7 | `POST /api/waitlist {"postcode":"9000","email":"test@example.com"}` | `ok == true` |
| 8 | `POST /api/bookings {sample}` | `ok == true`, `id` matches `^LL-[A-Z0-9]{6}$`, `estimate.total == 77.50` |
| 9 | `POST /api/contact`, `POST /api/enquiries` × 3 kinds | `ok == true` |

### 7.2 `verify/shots.mjs` (Playwright, Chromium 1194 at `/opt/pw-browsers`)

Renders all 15 routes at 390 × 844 and 1280 × 800, writes `shots/contact-sheet.png` (git-ignored), fails on any console error, toggles the mobile menu on `/` and asserts it opens and closes.

### 7.3 Acceptance checklist (your list, mapped)

| Your check | Where it is proven |
|---|---|
| Hero lines mask-reveal on load; marquee drifts; sections reveal on scroll; Lenis feels smooth | M2 shots + a 3-second video capture from Playwright on `/` (one file, once) |
| Estimator: 2 loads → $77.50; 1 load → $73.50; 3 blankets → 48 h | smoke.sh #1–#3 and M2 UI gate |
| 4000 active, 4509 opening, 9000 waitlist + email capture | smoke.sh #4–#7 (D1 decides 4000 vs 4131) |
| Booking returns `LL-XXXXXX` and shows estimate | smoke.sh #8 and `/book` UI |
| Contact + 3 enquiry forms return `{ok:true}` | smoke.sh #9 and M4 form audit |
| All routes render, mobile menu works, no console errors | shots.mjs |

---

## 8. Rules that travel from the current site (unchanged)

From README §Rules and HANDOFF §7, restated so they bind the new codebase:

- Never strip Australian compliance text: GST-inclusive pricing statement, NDIS registration statement, AS/NZS 4146 statement, contractor and WHS statements, ACL not-limited statement. `verify/sentinels.mjs` enforces this at build.
- Never invent footer entity text. Company name, ABN and address come from Max Jones. Until supplied the footer reads exactly as the current site: "Company name and ABN to be published on registration".
- No phone number or email is published until Callum supplies them. Copy reads "Phone line being connected" and "Email to be published".
- Pricing lives in one module (`api/_lib/pricing.js`) and is labelled launch pricing under review on every page that shows a price.
- No income claims on `/operators`. The "What we cannot tell you yet" block ships verbatim.
- Australian English, AUD, GST-inclusive everywhere.

---

## 9. Go-live blockers owned by the business (not the build)

Carried from HANDOFF §7. The build can finish with these open; the site cannot go public with them open.

| Item | Owner | Due |
|---|---|---|
| Company name and ABN for the footer | Max Jones | On registration |
| Phone and email to publish, or drop the promise | Callum Page | Before public launch |
| Privacy Policy and Terms in force (the booking form collects personal information) | Callum Page → solicitor, with a drafted brief | Before `/book` accepts real bookings |
| Pricing sign-off as the commercial position | Max Jones | Before public launch |
| Domain `laundrylegends.com.au` pointed at Vercel | Callum Page | At cut-over |

Legal boundary: these are compliance and commercial risks flagged for the principals. They are not legal advice.

---

## 10. Action register

| # | Action | Owner | Date |
|---|---|---|---|
| 1 | Answer remaining open decisions D1, D2, D3, D5, D6, D8, D9, D10 (§3, §11.7) — or confirm defaults, one message | Callum Page | Before Milestone 1 |
| 2 | Run Milestone 1 (foundations) and commit | Build session (current model) | Next session |
| 3 | Run Milestone 2 (home + tools) and commit | Build session (Sonnet) | Session after M1 |
| 4 | Run Milestone 3 (all marketing routes) and commit | Build session (Sonnet) | Session after M2 |
| 5 | Run Milestone 4 (booking and account app) and commit | Build session (Sonnet) | Session after M3 |
| 6 | Run Milestone 5 (motion and design polish) and commit | Build session (Sonnet) | Session after M4 |
| 7 | Run Milestone 6 (final pass) and deploy a Vercel preview | Build session (current model) | Session after M5 |
| 8 | Provide Ops Sheet Apps Script web-app URL, or approve adding `doPost` to the Ops Runner script | Callum Page | Before M6 |
| 9 | Confirm filing prefix (D11) so this plan and the dossier can be filed | Max Jones | Open since 19 Sep 2026, strengthened toward `LL` by the rebrand |
| 10 | ~~Register `linenlegends.com.au`~~ **Done 20 Sep 2026.** Remaining: confirm the eligibility basis (ABN? which entity?) so the footer entity text can go real (§12.2), then point DNS at Vercel at cut-over | Max Jones (entity/ABN) · Callum Page (DNS) | Entity text before public launch; DNS at cut-over |
| 11 | Decide whether to rebrand the still-live old artefact/site now or let it retire at cut-over (§12.1) | Callum Page | Whenever convenient — not blocking |
| 12 | Freeze the artefact `db` store once the new site accepts bookings | Callum Page | At cut-over |
| 13 | Clear §9 business blockers | Max Jones / Callum Page | Before public launch |

---

## Appendix A — Proposed repository layout after Milestone 1

```
package.json  vite.config.js  tailwind.config.js  postcss.config.js  index.html  vercel.json
api/
  _lib/pricing.js  _lib/coverage.js  _lib/ref.js  _lib/store.js
  estimate.js  waitlist.js  bookings.js  enquiries.js  contact.js
  coverage/check.js
server/dev.js                      # Express: mounts api/ handlers on :8787 for local curl tests
src/
  main.jsx  App.jsx  index.css
  components/  Navbar Footer Reveal Kinetic Marquee Section Estimator PostcodeChecker
               BookingForm EnquiryForm FAQAccordion
  pages/       Home Book Contact Services LegendsClub Coverage Business SupportedLiving
               Operators About Guarantee Faq Pricing Privacy Terms NotFound
  data/site.js                     # GENERATED by tools/extract_site_data.mjs — do not edit
  lib/api.js
tools/extract_site_data.mjs
verify/smoke.sh  verify/shots.mjs  verify/sentinels.mjs   (existing verify/*.js kept)
site/                              # current single-file site and landing page, untouched until cut-over
data/                              # dev-only JSON store, git-ignored
```

## Appendix B — Sizing note

BUILD FOR SCALE: the API is stateless functions and a single pricing module, so adding suburbs, services or a second region is a data change, not a code change. The Ops Sheet is the record at launch; if booking volume passes roughly 500 rows a month (ASSUMPTION — the point at which a Sheet becomes slow to work in day to day), the `store.js` interface is the one place to swap in a database without touching the site.

---

## 11. Motion and interaction wishlist — triage (added 20 Sep 2026)

Callum supplied a 40-item list of scroll, navigation, layout and micro-interaction effects. Each is triaged below into **In** (built in this rebuild), **Later** (phase 2, mostly the operator portal or customer app) or **Out** (conflicts with brand, compliance, performance or credit cost). Convergence rule: every "In" item is an extension of a component already in §6 (`Reveal`, `Kinetic`, `Marquee`, `Section`, `Navbar`, `Footer`) or one of three new small hooks. No animation library is added. No GSAP, Lottie, Three.js or Framer Motion.

### 11.1 Rules that govern every effect

| Rule | Detail |
|---|---|
| Reduced motion | Every effect checks `prefers-reduced-motion: reduce` and degrades to a plain state. Not optional. |
| Pointer-only effects | Magnetic, tilt, liquid fill and hover reveals run only under `@media (pointer: fine)`. Touch devices get the static state. |
| Compositor only | Animate `transform` and `opacity` only. No animated `top`, `height`, `filter` or `box-shadow` on scroll. |
| Budget | JavaScript ≤ 150 KB gzipped, Largest Contentful Paint ≤ 2.5 s on a mid-range phone, Cumulative Layout Shift ≤ 0.1. `verify/shots.mjs` records these from Playwright and fails the gate if exceeded. (ASSUMPTION: thresholds are Google's Core Web Vitals "good" bands; variable is the test device profile.) |
| No effect touches a number | Prices, totals and postcodes are never scrambled, counted up, or animated. A customer must never see a price appear to change. |
| One accent | The ember accent is the single action colour. No second accent (teal, orange, lavender) is introduced. |

### 11.2 Scroll mechanics

| Item | Verdict | How, and where it lands |
|---|---|---|
| Scroll-driven parallax (multi-layer) | **In** | `useScrollProgress()` hook drives `translate3d` on two hero layers (image and badge cluster) and one background layer per `Section`. Milestone 2. |
| Scrubbable Lottie animations | **Out** | Needs vector animation files that do not exist and a 60 KB+ runtime. Replaced by scroll-scrubbed SVG stroke draws (see checkmark, §11.5). Revisit if brand animation assets are commissioned. |
| Horizontal scroll section | **Later** | Desktop-only horizontal rail for the "three steps" section is possible, but scroll-jacking hurts mobile and accessibility, and it is the most expensive single effect to get right. Vertical steps with sticky stacking ship first. |
| Reveal-on-scroll wipes (clip-path unmask) | **In** | Already the job of `Reveal.jsx`. Add variants `fade`, `rise`, `wipe-x`, `wipe-y`, `mask-lines` (hero). Milestone 1. |
| Sticky section stacking (card deck) | **In** | `position: sticky` with staggered `top` offsets on the three-steps cards and the three Legends Club plans. CSS only. Milestone 2. |
| Progress scroll indicator | **In** | 2 px ember line in `Navbar`, `scaleX` from `useScrollProgress()`. Milestone 1. |
| Smooth inertial scrolling | **In** | Lenis, already specified. Disabled under reduced motion and on touch (native scroll is better there). |

### 11.3 Navigation

| Item | Verdict | How, and where it lands |
|---|---|---|
| Shrinking sticky header with glass blur | **In** | `Navbar` gets a `scrolled` class at 24 px: height 76→60 px, `backdrop-filter: blur(12px)`, 60 % navy. Milestone 1. |
| Hidden drawer navigation (fullscreen overlay, large type) | **In** | The planned mobile menu becomes a fullscreen overlay at all widths: `clip-path: circle()` expand from the burger, links in the display face at `clamp(2rem, 8vw, 4.5rem)`, staggered rise. Focus trap and `Escape` already in Milestone 4. |
| Floating action menu (bottom pill) | **Out** for the marketing site | Collides with hero CTAs and the estimator on phones, and this exact class of overlap bug shipped once already (README, collision check). The customer app already has a tab bar; the pattern belongs there. |
| Dynamic breadcrumbs | **Simplified In** | The site is two levels deep. Static `Home / Page` breadcrumb on every non-home route (matches the PDF). No history logic. |
| Contextual footer morph | **Simplified In** | Footer reveals with a single wipe and the marquee slows as it enters view. No rich graphics. |
| Inline dynamic search with thumbnails | **Out** | Fifteen pages and no catalogue: nothing to search. An FAQ filter input on `/faq` covers the real need. |

### 11.4 Responsive, performance and page transitions

| Item | Verdict | How, and where it lands |
|---|---|---|
| Fluid responsive resizing (`clamp`, `vw`) | **In** | Already the type system in §6 Milestone 1. |
| Accessible focus states | **In** | Two-ring focus: 2 px ember outline, 2 px navy offset, `:focus-visible` only. Verified by `verify/a11y.js` pattern. |
| Hardware-accelerated CSS | **In** | The compositor-only rule in §11.1. |
| Smart @2x asset swapping | **In** | `srcset` 1x/2x plus AVIF/WebP `<picture>` for the hero image, the only raster asset. Milestone 2. |
| Optimised font loading | **In** | Self-hosted woff2, `font-display: swap`, `size-adjust` metric-matched fallbacks to kill layout shift. Milestone 1. |
| WebGL wave/wipe page transitions | **Out** | A WebGL context for a transition costs more than every other effect combined and fails the JS budget. **Replaced** by a CSS clip-path wipe using the View Transitions API where supported, plain fade elsewhere. Reads as a clean "wipe" without the GPU cost. |

### 11.5 Layout, colour and micro-interactions

| Item | Verdict | How, and where it lands |
|---|---|---|
| Bento grid layouts | **In** | The trust strip on Home and the "what you get" block on `/operators` become bento grids. **Copy rule:** cards may only name features that exist today. "SMS alerts" and "route tracking" are not live (current copy says "once our messaging system is live"), so they are labelled "Coming" or omitted. UNVERIFIED until Callum confirms which operator features are live. |
| Aurora / mesh gradients | **Out** as specified, **Later** in palette | Sky blue, seafoam and lavender are off-brand. A slow navy-to-deep-navy mesh with one ember bloom behind the hero is a possible phase-2 refinement once the rest is stable. |
| Dark-mode toggle with circular mask | **Later** | Night-shift operators use the operator portal, which is out of scope (D4). Marketing site ships one theme. |
| Neomorphism accents | **Out** | Inset soft-shadow controls fail contrast guidance and read as a different brand. |
| High-contrast typography hierarchy | **In** | Already the display/body pairing in §6. |
| Content border highlights (glowing active border) | **In** | Active Legends Club plan and the selected service card get a 1 px ember border with a 0→1 opacity glow. Milestone 2. |
| Vibrant accent pops | **In, one accent** | Ember is the pop. No second accent. "Book a Demo" wording does not apply; primary CTA stays "Book a collection". |
| Magnetic buttons | **In** | `useMagnetic()` hook on primary `.btn` only, 12 px max pull, pointer-fine only. Milestone 1. |
| Image reveal on hover over suburb names | **Out** | Requires photographs of real operators, which do not exist and would need written consent. Revisit when there are operators and photos. |
| Liquid button fill | **In** | CSS pseudo-element wave (`translateY` on a sine-edge SVG mask) on `.btn-primary` hover. Milestone 1. |
| Card tilt (3D) | **In** | `useTilt()` hook on the three club cards, ±6°, pointer-fine only, reduced-motion off. Milestone 2. |
| Text scramble on figures | **Out** | Violates the "no effect touches a number" rule. Prices must read as fixed. |
| Icon bounces and checkmark draw | **In** | Stroke-dashoffset draw on the estimator's "GST included" tick and form success states; step icons get a one-time 4 px bounce on reveal. Milestone 2. |
| Sound / haptic feedback | **Out** | Browsers block autoplay audio without a gesture, most users find UI sounds intrusive, and there is no Operator/Customer toggle on the marketing site. |

### 11.6 Effect on the build

| Milestone | Added work | Delta (ASSUMPTION: one turn ≈ one milestone as sized in §6) |
|---|---|---|
| M1 | `Reveal` variants, progress bar, shrinking glass header, fullscreen overlay nav, `useScrollProgress` / `useMagnetic` / `useTilt` hooks, liquid fill and focus styles in `index.css`, font self-hosting | About half a turn |
| M2 | Parallax layers, sticky stacking, bento trust strip, glow borders, tilt on club cards, checkmark draws, hero `<picture>` | About half a turn |
| M4 | Web-vitals thresholds in `verify/shots.mjs`, reduced-motion audit, View Transitions wipe | Small |

Total: roughly one extra turn across the four milestones. Everything marked Later or Out costs nothing now.

### 11.7 Decisions this adds

| # | Decision | Options (best first) | Default |
|---|---|---|---|
| D8 | Which operator-app features are live today, for the bento copy (alerts, route tracking, payouts) | (a) Only features live at launch appear, others say "Coming" **(Recommended)** · (b) List planned features as planned | (a) |
| D9 | Horizontal steps rail on desktop | (a) Phase 2 **(Recommended)** · (b) Include in M2 at roughly one extra turn | (a) |

---

## 12. Premium design brief and scope update — resolved 20 Sep 2026

Callum asked for an Apple/BMW/Samsung-style site — "very modern, no corner cut visuals" — then answered ten follow-up questions and, in a second round, three clarifying questions about two answers that were ambiguous or contradictory against the docs of record. This section is the record of that exchange and is authoritative where it conflicts with §0–§11.

### 12.1 Rebrand: Laundrylegends → Linen Legends

Confirmed by Callum Page, 20 Sep 2026, after I flagged that it contradicted every existing doc (README, HANDOFF, the live artefact, the site's own JSON-LD, the current filing-prefix discussion). **This is a real rebrand, not a typo fix.** What it touches:

| Touches | Handling |
|---|---|
| New build (this plan, §1–§11, the eventual `src/data/site.js`, all new copy) | Uses "Linen Legends" from Milestone 1 onward. `tools/extract_site_data.mjs` runs a brand find-and-replace pass (Laundrylegends → Linen Legends, laundrylegends.com.au → linenlegends.com.au) while pulling copy from the old file. |
| Order reference prefix `LL-` | **No change needed** — "LL" already fits "Linen Legends" as well as it fit "Laundrylegends". |
| The still-live artefact and `site/laundrylegends-site.html` | **Untouched by this rebuild.** They keep the old brand until either cut-over (§2.3) or a separate small request to rebrand them now (action register #11). Not blocking. |
| Filing prefix (`LKG` vs `LL`) | Still Max Jones's call (README), but the rebrand strengthens `LL` (D11). |
| Company name for ABN registration | Unaffected either way — that's a separate legal step owned by Max Jones (§9), and "Linen Legends" vs any registered trading name is worth checking doesn't clash before the ABN application. |

### 12.2 Domain

**`linenlegends.com.au` is REGISTERED** — confirmed by Callum Page, 20 Sep 2026, exact string checked back against the registrar spelling. It becomes the canonical domain in every URL, the JSON-LD `@id`, Open Graph tags and the eventual email addresses from Milestone 1 onward. One correction made during the earlier question stands for the record: `.co.au` is not a real Australian namespace — the options are `.com.au` / `.org.au` / `.net.au` (ABN or trademark required under auDA rules) or a bare `.au`.

**Follow-on fact to confirm:** a `.com.au` registration requires an ABN, ACN or trademark basis. If it was registered against a new ABN, that same ABN also clears the biggest §9 footer blocker — Max Jones should supply the registered entity name and ABN for the footer, and the "Company name and ABN to be published on registration" placeholder can finally be replaced with real text. If it was registered some other way (e.g. under an existing entity of the principals'), say which entity, because the footer must name the actual trading entity. UNVERIFIED until one of them confirms — the footer text still comes from Max Jones only, per the standing rule.

Remaining domain tasks: point `linenlegends.com.au` at the Vercel project at cut-over (DNS at the registrar or delegate to Vercel), and decide the www/apex redirect direction (Recommended: apex canonical, www redirects). Owner: Callum Page, at cut-over.

### 12.3 Visual direction — Apple / BMW / Samsung, "no corner cut visuals"

| Question | Answer | Consequence |
|---|---|---|
| Reference style | Not picked explicitly between the three; the request stands as "modern, no cut corners" generally | §6 Milestone 5 treats this as: BMW-style dark cinematic hero + Apple-style restrained light content sections, per my original recommendation, since Callum didn't override it. Revisit in the M5 gate review if the contact sheet doesn't land right. |
| Photography and film | "We will worry about photography and film last" | Confirmed as deferred. M5 ships with the one existing hero JPG under a consistent duotone/grain placeholder treatment, not stock photography (stock is exactly the "corner cut" the brief is trying to avoid). Real assets swap in later without a redesign. |
| 3D hero object | "No" | Confirmed out. No 3D library enters the bundle. |
| Logo and brand files | "We'll do that last" | Confirmed deferred, same bucket as photography. M1's design tokens (navy/ember, the type ramp) don't depend on a final logo file. |
| Typeface | Not actually answered — the reply was about Max Jones's role in the business, not a font. See 12.4. | Default stands: a self-hosted variable grotesk from Google Fonts, zero licensing risk. No commercial face is licensed. Revisit whenever Callum names one. |
| Copy length | "Ok" (to cutting page copy to roughly 40%) | Confirmed, executed in M5. Compliance text and the guarantee/terms stay full length regardless. |
| Testimonials | "No testimonials as we will have a real input review system not fake" | Confirmed: no fake reviews, ever. The site launches with no reviews section. **New item, not yet scoped:** a real review-capture flow. §12.5 records it as a Later item, seeded by reusing the existing `#/feedback` pattern already in the old site rather than inventing a new one (convergence). |
| Five milestones (the polish pass) | "Okay" | Now folded into six (§6 Milestone 5), because Milestone 4 (booking app) was added in the same round — not because the polish pass itself grew. |
| Sign-off | "Me" | Callum Page alone approves the Milestone 5 contact sheet before Milestone 6 starts (§6 M5 gate). |

### 12.4 Typeface / logo clarification

My second-round question asked whether "Max Jones is our licensed face" meant a commercial font licence. Callum's answer: **"No, Max is our owner, he is the licensed everything and the local face to the business."** This is not a typeface decision — it means Max Jones is a business owner/principal and the business's public-facing representative, consistent with the standing context (Max Jones: structures numbers, long-range planning, prior multi-site operator). No font is licensed. The earlier ABC News link (Condobolin/Charleville shops story) was noise, not an instruction, and is disregarded. **Consequence for the build:** none directly — but Max being "the local face" is a usable, UNVERIFIED-until-confirmed fact for `/about` page copy (e.g. an owner's note or photo) once photography is scoped (§12.3), not before.

### 12.5 Booking-process app brought into scope

See §6 Milestone 4 for the full build detail. Summary: the customer-facing booking management experience — order status, bookings list, messages, account/profile — is now in scope for this rebuild, redesigned to an Uber/service-app visual standard rather than ported as-is. Source is already in the repo (no resend needed). One technical honesty point carried into D10: a live GPS-tracked map is a second product, not a styling choice, and is not built now.

### 12.6 Net effect on the plan

- Milestone count: **4 → 6** (booking app + polish pass, both new since the original plan).
- Route count: 15 marketing routes (unchanged) **+ `/account`, `/messages`** app surfaces.
- Domain and brand: **Linen Legends**, `linenlegends.com.au` (registered 20 Sep 2026) — every reference in §0–§11 to "Laundrylegends" or `laundrylegends.com.au` is superseded by this section.
- No change to: pricing of record, coverage of record, estimator rule, compliance sentinels, hosting choice, persistence choice, or the credit-efficiency rules in §5 — those hold as written.
- Still open before Milestone 1: D1, D2, D3, D5, D6, D8, D9, D10 (defaults apply on silence, per §3); D11 stays with Max Jones; action register items 9–11.
