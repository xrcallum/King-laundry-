# Laundrylegends — copy of record

Laundry pickup and delivery across Brisbane, Logan and South East Queensland.
This repository is the source of record for the website file and the project dossier.
The live site is published as a Claude artefact; the PDF dossier is for reading, this repo is for editing.

## Layout

| Path | What it is |
|---|---|
| `site/laundrylegends-site.html` | The complete website (marketing, customer app, ops backend) as one file. Renamed from `laundrykings-site.html` and rebranded LaundryKings → Laundrylegends on 19 September 2026. Published live at `https://claude.ai/artifact/5QptppvdarNfZyVYBFpyy3` (capabilities `{"db":{},"user":{}}`, contract 0.2.52, icon crown). Two older artefacts still titled "LaundryKings" were not overwritten and should be retired manually once confirmed unused. |
| `verify/preflight.py` | Pre-publish checks. Run before every publish. |
| `dossier/*.html`, `dossier/build.py` | Source and build script for the Complete Project Dossier. |
| `dossier/LLG-GOV00-01_Complete Dossier_v3.pdf` | The built dossier, revision 3, 19 September 2026 — full LaundryKings → Laundrylegends rebrand, filing prefix LKG → LLG. |

## Publish workflow (never skip a step)

1. Edit `site/laundrylegends-site.html`.
2. `python3 verify/preflight.py site/laundrylegends-site.html` (add `--strict-tokens` once Phase A has landed). It must print `RESULT: PASS`.
3. `NODE_PATH=/opt/node22/lib/node_modules node verify/collide.js site/laundrylegends-site.html`. The floating layers (sticky pill, chat button, app tab bar, assistant panel) must not overlap each other or any button beneath them at phone widths. It must print `RESULT: PASS`. Preflight cannot see this class of bug; the collision check exists because it shipped once.
4. Commit with the artefact version in the message, e.g. `site: v4.3 Phase A foundation tokens`.
5. Publish to the existing artefact URL with capabilities `{"db":{},"user":{}}`, favicon crown, contract 0.2.52. Never add `mcp`.
6. Confirm on a phone.

## Rebuild the dossier

```
python3 dossier/build.py site/laundrylegends-site.html verify/preflight.py \
  "dossier/LLG-GOV00-01_Complete Dossier_v3.html" "dossier/LLG-GOV00-01_Complete Dossier_v3.pdf"
```

Requires Python 3, Node with Playwright and a Chromium build (the build script uses `pymupdf`, not `pypdf`, for page-number extraction — `pypdf` panics in this environment via its `cryptography` binding). Appendix C of the PDF is generated from the site file at build time, so the PDF always matches the committed source.

**Filing note:** the dossier now files as `LLG-GOV00-01` (prefix `LLG` for Laundrylegends, replacing `LKG`) — an assumption pending confirmation against the real Maxcal artefact register, flagged as such on the cover page.

**Domain facts not yet re-verified:** the domain-availability/WHOIS findings in Parts 9–18 (D-09) were checked against `laundrykings.*` before the 19 September rebrand and are left under that name — restating them under `laundrylegends.*` without re-running the check would assert an unverified fact. Re-run the same Vercel/WHOIS check against `laundrylegends.com.au`, `.com`, `.au` and `.co` before D-09 is decided.

## Rules that travel with the code

- Keep every existing element ID; the script depends on them.
- Never strip Australian compliance text (GST-inclusive pricing, NDIS statement, AS/NZS 4146 statement, contractor and WHS statements, ACL not-limited statement).
- Never invent footer entity text. Company name, ABN and address come from Max Jones.
- Pricing lives in the database document `config/pricing`; do not hard-code changes.
