# Linen Legends — one-shot continuation prompt

Paste this as the FIRST message in a new chat. It is self-contained; do not summarize it, do not paraphrase it, act on it directly.

---

I'm continuing the Linen Legends laundry site (Brisbane/Logan/SEQ pickup & delivery). Everything you need is already in the repo — read before acting, don't rediscover.

**Repo:** `github.com/xrcallum/King-laundry-` · **Branch:** `claude/laundry-legends-build-qmcafm` (already built and pushed through commit `f81a5ed` — check out this branch, don't start from default)

**Read first, in order, before any other action:**
1. `docs/LL-HANDOFF.md` — full state of record, environment IDs, open items list (§5)
2. `docs/laundrylegends-build-plan.md` §12 only — decisions, rebrand record, build status (§12.7)

**Do not re-read** the 49-page PDF, the old `site/laundrylegends-site.html`, or re-derive pricing/coverage from scratch — they're already extracted into `api/_lib/pricing.js` and `src/data/coverageData.js`, which are the sources of truth now. Only fall back to the PDF/old site if a handoff doc explicitly says a fact is missing.

**Immediate verification (run this before any other tool call, confirms the build still works):**
```
cd /home/user/King-laundry- && npm ci
npm run api &
npm run dev &
sleep 3
node verify/smoke.mjs
```
All three must print `RESULT: PASS` (smoke, and after `npm run build`, also `node verify/sentinels.mjs`). If any fails, that's the first thing to fix — nothing else proceeds until gates are green.

**Non-negotiable rules — violating any of these is a defect, not a style choice:**
- Prices ONLY from `api/_lib/pricing.js`. Coverage ONLY from `src/data/coverageData.js`. Never hardcode a number anywhere else.
- Never invent a fact, figure, phone number, email, address, person, testimonial, or feature. If it's not in the copy of record, it doesn't ship.
- Brand is "Linen Legends" (two words) / "Legends Club". Never "Laundrylegends" or "Kings Club" — `verify/sentinels.mjs` fails the build if either leaks in.
- ABN `12 482 409 883` is published in the footer. The registered entity NAME is not — never invent one; it's owed by Max Jones.
- No phone or email exists yet — copy says "being connected" / "to be published". Don't add real-looking contact details.
- Keep every compliance sentinel `verify/sentinels.mjs` checks for (GST-inclusive, NDIS non-registration, AS/NZS 4146, ACL rights-not-limited, contractor-not-employment, "not yet in force" on privacy/terms).
- Australian English, GST-inclusive AUD throughout, no emoji.

**Workflow for this session:**
1. Confirm gates pass (above).
2. Do the requested work in batches — group related changes, don't commit one line at a time.
3. Run the relevant gate(s) after each batch (`smoke.mjs` for API changes, `sentinels.mjs` + `npm run build` for copy/compliance changes, `shots.mjs` for UI changes) before every commit.
4. Commit with a message in the style already in `git log` (one-line summary, blank line, detail, blank line, attribution footer). Push — the Vercel project `linenlegends-site` auto-deploys every push to this branch.
5. Update `docs/LL-HANDOFF.md` §5 (open items) if you close or add anything — that section is the live to-do list across sessions.

**Open items right now** (full detail in LL-HANDOFF.md §5): Ops Sheet webhook URL for real persistence (currently ephemeral on Vercel), registered entity name from Max Jones, Vercel production-branch repoint + DNS for `linenlegends.com.au`, business go-live blockers (phone/email, privacy & terms in force, pricing sign-off), and an unfinished audit-and-polish pass (hero parallax, checkmark-draw success states, booking validation hardening) that was interrupted mid-run last session — re-run only if asked, it's a nice-to-have, not a blocker.

Tell me what to work on, or if nothing's specified, start with the open items in priority order.
