# Laundrylegends — Site rebuild plan (React + API)

**Prepared:** 20 September 2026 · **Owner:** Callum Page · **Venture:** Laundrylegends
**Branch:** `claude/laundry-legends-build-qmcafm` · **Repo:** `github.com/xrcallum/King-laundry-`
**Filing:** code pending — README flags the `LKG` vs `LL` prefix as an open filing decision (Max Jones). File under SYS09 once decided.
**Status:** v1 — plan only. Nothing in this document has been built yet.

---

## 0. Recommendation

Build the 12-route React site and its API as **one Vite + React app at the repo root with the API as Vercel serverless functions under `api/`**, deployed to Vercel (its MCP connector is already attached to this workspace). Run the 12-step build sequence as **four milestones, not twelve messages**, each ending in a commit, one scripted verification run and one screenshot contact sheet. Lift every line of copy, every price and every postcode **programmatically from the existing site file** (`site/laundrylegends-site.html`) rather than retyping it. Keep the existing artefact live until the new site passes the acceptance checklist in §7. Seven decisions in §3 need an answer from Callum before Milestone 1 starts; everything else is locked here.

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
| **Vercel: static Vite build + `api/` functions** | Connector already attached. Free Hobby tier covers launch traffic. `laundrylegends.com.au` (already referenced in the site's JSON-LD) attaches as a custom domain. | **(Recommended)** |
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

> **Ask this person: Callum Page** — answer D1–D7 in one message. Each has a default; silence means the default applies and is labelled ASSUMPTION in the code.

| # | Decision | Options (best first) | Default if unanswered |
|---|---|---|---|
| D1 | **Postcode 4000.** Your checklist says 4000 → active. The coverage data of record says 4000 → opening soon. | (a) Keep data of record (4000 = opening) and change the test to a live postcode such as 4131 **(Recommended — no unverified coverage claim)** · (b) Move 4000 into `LIVE_PC` because an operator is confirmed for the CBD | (a) |
| D2 | **48-hour turnaround for blankets.** New rule; current copy says turnaround is "confirmed at booking". | (a) Estimator shows "Indicative turnaround: 48 h" for the linen service; FAQ and terms copy unchanged **(Recommended)** · (b) Publish 48 h as a commitment across the site | (a) |
| D3 | **Pricing, Privacy and Terms pages** exist in the PDF but are not in the 12 routes. Footer links point at them. | (a) Add `/pricing`, `/privacy`, `/terms` as static routes rendered from extracted copy — three small files **(Recommended)** · (b) Drop them and remove the footer links | (a) |
| D4 | **Customer app and operator portal** (PDF pp. 42–49; `portal.html`) are outside the 12 routes. | (a) Out of scope for this rebuild; the "My Account" button links to the existing artefact until phase 2 **(Recommended)** · (b) Include now (roughly doubles the build) | (a) |
| D5 | **BACKEND SPEC.** Not in the repo. | (a) Paste it and I diff it against §4 · (b) Accept §4 as the spec **(Recommended if it matches your memory of it)** | (b) |
| D6 | **Ops Sheet webhook URL** for bookings/enquiries. | Provide the Apps Script web-app URL, or confirm the Sheet has no script yet and I add the `doPost` handler to the single Ops Runner script in a later step | Dev JSON fallback; Sheet wiring becomes an action in §10 |
| D7 | **Brand string.** PDF says "LaundryKings / Kings Club". Repo is "Laundrylegends". Your sequence says `/legends-club`. | (a) "Laundrylegends" (one word, as the repo) and "Legends Club" **(Recommended — matches the copy of record)** · (b) "Laundry Legends" two words | (a) |

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

## 6. Build sequence as four milestones

Each milestone maps to the numbered steps in the original sequence. "Gate" is what must be true before the milestone is committed.

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

### Milestone 4 — Final pass and cut-over prep (step 12)

| Item | Detail |
|---|---|
| Form audit | curl + UI for booking, contact and the three enquiry kinds; assert `{ok:true}` and an `id`. |
| Mobile nav | Open, close, route change closes menu, focus trap, `Escape`. |
| Console | Zero errors and zero warnings across 15 routes at 390 px and 1280 px. |
| Accessibility | Reuse `verify/a11y.js` pattern against the built `dist/`; fix contrast on ember-on-navy if flagged. |
| Compliance sentinels | Port the README rule into `verify/sentinels.mjs`: GST-inclusive statement, NDIS statement, AS/NZS 4146 statement, contractor and WHS statements, ACL not-limited statement, no invented entity text, no phone or email unless supplied. Build fails if any is missing. |
| Deploy | Vercel preview deployment via the connector; smoke script re-run against the preview URL. |
| Commit | `site: M4 final pass — forms, nav, a11y, sentinels` |

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
| 1 | Answer decisions D1–D7 in §3 in one message | Callum Page | Before Milestone 1 |
| 2 | Run Milestone 1 (foundations) and commit | Build session (current model) | Next session |
| 3 | Run Milestone 2 (home + tools) and commit | Build session (Sonnet) | Session after M1 |
| 4 | Run Milestone 3 (all routes) and commit | Build session (Sonnet) | Session after M2 |
| 5 | Run Milestone 4 (final pass) and deploy a Vercel preview | Build session (current model) | Session after M3 |
| 6 | Provide Ops Sheet Apps Script web-app URL, or approve adding `doPost` to the Ops Runner script | Callum Page | Before M4 |
| 7 | Confirm filing prefix (`LKG` or `LL`) so this plan and the dossier can be filed | Max Jones | Open since 19 Sep 2026 |
| 8 | Freeze the artefact `db` store once the new site accepts bookings | Callum Page | At cut-over |
| 9 | Clear §9 business blockers | Max Jones / Callum Page | Before public launch |

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
