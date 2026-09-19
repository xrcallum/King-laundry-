# Laundrylegends — brief: prototype to operating business

**Prepared:** 19 September 2026
**For:** whoever picks up this venture next — paste sections 1–7 verbatim as the
opening prompt to a new agent or session.
**Built from:** `README.md`, `site/laundry-australia/HANDOFF.md`, the dossier, the
commit history, and a live read of all five published artefacts on 19 Sep 2026.
Decisions made in conversation and never written down are not in here.

---

You are taking over the Laundrylegends venture: a laundry pickup-and-delivery
business for Brisbane, Logan and South East Queensland. It currently exists as
two polished, fully-simulated websites. Your job is to close the gap between
that and a business that can legally accept a paying customer's booking,
collect their washing, and get it back to them.

Work in Australian English, AUD, GST-inclusive. Today's date is your reference
for every due date you set.

## 1. Source of truth — read before you propose anything

| Path | What it is |
|---|---|
| `README.md` | Publish workflow and the rules that travel with the code |
| `site/laundry-australia/HANDOFF.md` | Full history, §7 blockers, §11 operator portal |
| `docs/3d-web-architecture-blueprint.md` | Architecture blueprint |
| `dossier/LKG-GOV00-01_Complete Dossier_v2.pdf` | Governance dossier, revision 2 |

Repo: `github.com/xrcallum/King-laundry-`
Branch: `claude/chat-review-confirmation-458hx6` (latest; commit `39ee1d5`)

Treat these documents as claims to verify, not facts. An audit on 19 Sep 2026
found three of them stale: the README says the live artefact needs
republishing (it didn't), says pricing lives in a database document at
`config/pricing` (that document does not exist — prices are hard-coded at
`site/laundrylegends-site.html` line ~4161), and the dossier still carries the
old LaundryKings brand and `LKG` filing prefix throughout.

## 2. What is actually live — verified 19 September 2026

| Surface | URL | Backed by |
|---|---|---|
| Master site | `claude.ai/artifact/5QptppvdarNfZyVYBFpyy3` | `site/laundrylegends-site.html` — one 505KB file, 7,300 lines: 14 marketing routes, customer app, booking wizard, Legends Club portal, operator screens, priced AI assistant |
| Home-laundry | `claude.ai/artifact/11cT6RXSi4G3EprLXGzFqE` | `site/laundry-australia/{index,contact,portal}.html` |
| Booking flow | `claude.ai/artifact/SJihvya38JukdcAUL7JiFx` | **Shared with the owner, not owned by him**, and still titled "LaundryKings" |

Every Book / Legends Club / Privacy / Terms link on the home-laundry pages
points at that booking artefact. The owner cannot edit it. Resolve this before
anything else ships.

Stale, still published under dead brands — decide keep / retire / delete:

- `YKZ5cbiCmG52FpRBByGPPR` and `5tEepYWartpqhgn6XD3M2X` — LaundryKings
- `RMtABY7RdxsRFnak9Ejsyv` and `XUL5bw8tUeT25PTh4CcJ3S` — Linen Legends, a
  third brand name in the wild

**Nothing persists anywhere.** Verified: the artifact database has no
documents; the operator portal keeps job status in browser localStorage only
(per device, gone if site data is cleared); the contact form intercepts submit
with a notice and has no backend; there is no payment processing; operator
"sign-in" is a name typed into a box with no identity check. A booking made on
the live site reaches nobody.

## 3. The price schedule — one schedule, three surfaces, currently consistent

| Line | Price |
|---|---|
| Wash & fold, per load (~5kg) | $32.00 |
| Premium Clean add-on, per load | +$15.00 |
| Eco / fragrance-free add-on | +$3.50 |
| Collection & return, flat | $13.50 |
| One-off minimum, waived for Club | $73.50 |
| Reusable branded bag, optional | $12.00 |
| Linen & bulky, per item | sheet set $24 · blanket $32 · rug $42 · doona $45 · king doona $75 · curtain $38 |
| Dry cleaning (partner), per item | dress $16.50 · jacket $18.50 · suit $32 |
| Legends Club, per week | Solo $63.70 · Pair $89.70 · Family $115.70 |

Code comments record two decisions: the minimum is "Laundry Lady $70 min +5%,
18 Sep 2026" and Club is "+30% on the launch rate, 19 Sep 2026". The page
labels all of it "launch pricing, under review and subject to change". It has
never been signed off. Do not change a figure without Max Jones's written
decision, and when you do, change it in one place and re-verify all three
surfaces still agree.

Coverage claimed live: 16 suburbs — Camp Hill 4152, Coorparoo 4151,
Greenslopes 4120, Holland Park 4121, Mansfield 4122, Sunnybank 4109,
Kuraby 4119, Browns Plains 4118, Springwood 4127, Meadowbrook 4131,
Shailer Park 4128, Loganholme 4129, Cornubia 4130, Marsden 4132,
Waterford 4133, Beenleigh 4207. Confirm the venture can actually service these
before a public launch — this is a promise, not a wish list.

## 4. Workstream A — what must be true before a stranger can pay

Each item: state the decision needed, the options (best first, marked
"Recommended"), the owner, and a due date. Do not give legal or tax advice —
produce options and a drafted brief for the venture's solicitor or accountant.

| # | Item | Owner |
|---|---|---|
| A1 | **Trading entity.** The footer reads "Company name and ABN to be published on registration". Australian Consumer Law expects a trading entity to be identifiable. | Max Jones |
| A2 | **Contactable channels.** The footer promises a phone line and an email and gives neither. Publish them or drop the promise. | Callum Page |
| A3 | **Privacy Policy and Terms of Service.** Both are drafts, both flagged "not yet in force" on the live page, and the booking flow collects personal information. They must be in force before it goes public. | Callum Page → solicitor |
| A4 | **Pricing sign-off.** | Max Jones |
| A5 | **Operator engagement.** The portal deliberately avoids implying an employment relationship, and HANDOFF §11 puts this out of scope. It is now in scope. Apply the contractor-vs-employee test — a labour-only ABN contract triggers Superannuation. Consider Fair Work "employee-like worker" exposure for platform-style engagement, and Queensland payroll tax grouping if the venture is grouped with other entities. | Max Jones → adviser |
| A6 | **Insurance.** Name specific policies, never "get insurance". At minimum scope: public liability; goods in care, custody and control (bailee cover for customers' garments — a standard public liability policy typically excludes them); motor vehicle with business use declared; WorkCover Queensland if anyone is an employee; cyber/privacy cover once personal information is stored. Label each UNVERIFIED until a broker confirms it. | Max Jones |
| A7 | **WHS, including chemicals.** Detergents and stain treatments need SDS on file, storage and handling instructions, and a documented induction — the site already claims every operator is "identity-screened, licence-and-vehicle checked and WHS-inducted". That claim must become true or come off the page. | Callum Page |
| A8 | **Regulated-channel flag — deal with this first.** The site markets to "supported living & aged care" and states Laundrylegends is not a registered NDIS provider but works with self-managed and plan-managed participants. Confirm what that permits, what it does not, and whether the copy is accurate before any spend points at it. | Callum Page |
| A9 | **Substantiation sweep.** Every claim on the page is a representation under the ACL: "next-day return", "never mixed with another household", "fee refunded if late", "same operator every week", "48-hour re-wash". List each, and for each say what operationally makes it true. Anything that cannot be backed comes off the page. | Callum Page |

## 5. Workstream B — what must be built

In priority order. Justify any architecture choice against where this venture
is going, not just today, and state the scale assumption you sized for.

- **B1 — A booking has to reach a human.** Today it reaches nobody. This is the
  single highest-value change.
- **B2 — Durable storage** for bookings, customers and operator rounds,
  replacing localStorage. Turning this on is the moment the Privacy Act
  attaches — decide what is stored and for how long before you write the first
  record.
- **B3 — Real operator authentication.** A name in a box is not identity.
- **B4 — Payments.** The page says "pay after weighing", which is a real
  constraint: the price is confirmed at the door, so the flow needs
  authorisation-then-capture or an equivalent, not upfront charging.
- **B5 — Retire or fix the shared LaundryKings booking artefact** (§2).
- **B6 — Known defects**, all verified, none fixed:
  - `kcRecalc()` and the home estimator read `px.min`; the pricing table
    defines `minimum` (everything else reads `PX.minimum`). Harmless on
    defaults, silently wrong the moment anyone sets an override.
  - `preflight --strict-tokens` fails: 101 font-size and 37 letter-spacing
    literals outside the token set ("Phase A" in the README, never landed).
  - The dossier still says LaundryKings and carries the `LKG` filing prefix.
    Renaming a filed governance document's code is a filing decision — get the
    new prefix confirmed, don't guess.
  - The folder is still `site/laundry-australia/` post-rebrand.

## 6. Guardrails

- Never invent a figure. Cite the file and line, or label it ASSUMPTION with
  its basis and what would change it. Same for non-financial claims: label
  UNVERIFIED and say what would confirm it.
- No legal, tax or structuring advice. Options plus a drafted brief, routed to
  the named adviser.
- Extend what exists. Do not create a new site, a new repo or a fourth brand.
- Every publish: run `verify/preflight.py`, `verify/collide.js`,
  `verify/a11y.js` and `verify/e2e.js` — all must pass (e2e is 20/20 as of
  commit `39ee1d5`). Call the Artifact `read` action on the live URL before
  publishing; two sessions once published over each other and silently
  reintroduced a fixed bug.
- Publishing without the existing artefact URL creates a second artefact
  instead of updating the live one.
- Never strip the compliance text: GST-inclusive pricing, the NDIS statement,
  the AS/NZS 4146 statement, the contractor and WHS statements, the ACL
  not-limited statement.
- Every action you propose ends with a named owner and a date.

## 7. Your first reply

Do not start building. Reply with:

1. Anything in §2–§3 your own reading of the repo contradicts.
2. The shortest credible path to one real paying customer in one suburb — what
   must be true, in what order, and what it costs. Recommendation first, then
   reasoning.
3. The five questions only Callum Page or Max Jones can answer, as a fillable
   "Ask this person: `<name>`" block per person.
