# Laundrylegends — copy of record

Laundry pickup and delivery across Brisbane, Logan and South East Queensland.
This repository is the source of record for the website file and the project dossier.
The live site is published as a Claude artefact; the PDF dossier is for reading, this repo is for editing.

## Layout

| Path | What it is |
|---|---|
| `site/laundrylegends-site.html` | The complete website (marketing, customer app, ops backend) as one file. Renamed from `laundrykings-site.html` and rebranded LaundryKings → Laundrylegends on 19 September 2026; the live artefact needs republishing to match (see note below). |
| `verify/preflight.py` | Pre-publish checks. Run before every publish. |
| `dossier/*.html`, `dossier/build.py` | Source and build script for the Complete Project Dossier. |
| `dossier/LKG-GOV00-01_Complete Dossier_v2.pdf` | The built dossier, revision 2, 19 September 2026. |

## Publish workflow (never skip a step)

1. Edit `site/laundrylegends-site.html`.
2. `python3 verify/preflight.py site/laundrylegends-site.html` (add `--strict-tokens` once Phase A has landed). It must print `RESULT: PASS`.
3. `NODE_PATH=/opt/node22/lib/node_modules node verify/collide.js site/laundrylegends-site.html`. The floating layers (sticky pill, chat button, app tab bar, assistant panel) must not overlap each other or any button beneath them at phone widths. It must print `RESULT: PASS`. Preflight cannot see this class of bug; the collision check exists because it shipped once.
4. Commit with the artefact version in the message, e.g. `site: v4.3 Phase A foundation tokens`.
5. Publish to the existing artefact URL with capabilities `{"db":{},"user":{}}`, favicon crown, contract 0.2.52. Never add `mcp`.
6. Confirm on a phone.

## Linen Legends (Framer) page — auto-ship

`site/linen-legends-framer.html` is the page live at https://claude.ai/artifact/7dAa3qVyaN8NV5pGXkbrQw.
The build agent works on `claude/framer-site-import-linen-2wh926`. A ship agent (session "Linen Legends auto-ship updates") checks hourly and ships from `claude/linen-legends-auto-ship-afzpsw`:

1. Fetch the build branch and read the live artifact's `index.html`.
2. The live artifact wins when it is ahead of git: its page is committed so nothing published is ever lost from the record.
3. `python3 verify/framer_static.py site/linen-legends-framer.html` and `NODE_PATH=/opt/node22/lib/node_modules node verify/framer-smoke.js site/linen-legends-framer.html` must both print `RESULT: PASS`, or nothing ships.
4. PR into the default branch and merge.
5. Republish the artifact only when the build branch has a change the live page doesn't — never overwrite a newer live version.

Build agent: commit and push after each publish so git and the live page stay level.

## Rebuild the dossier

```
python3 dossier/build.py site/laundrylegends-site.html verify/preflight.py \
  "dossier/LKG-GOV00-01_Complete Dossier_v2.html" "dossier/LKG-GOV00-01_Complete Dossier_v2.pdf"
```

Requires Python 3, Node with Playwright and a Chromium build. Appendix C of the PDF is generated from the site file at build time, so the PDF always matches the committed source.

**Not yet done:** the dossier PDF (`LKG-GOV00-01_Complete Dossier_v2.pdf`) still carries the `LKG` filing prefix and "LaundryKings" in its own header/footer template and title, and hasn't been rebuilt since the rename. Renaming a filed governance document's code is a filing decision, not a text substitution — confirm the new prefix (`LLG`? `LL`?) before renaming and rebuilding it, rather than guessing.

## Rules that travel with the code

- Keep every existing element ID; the script depends on them.
- Never strip Australian compliance text (GST-inclusive pricing, NDIS statement, AS/NZS 4146 statement, contractor and WHS statements, ACL not-limited statement).
- Never invent footer entity text. Company name, ABN and address come from Max Jones.
- Pricing lives in the database document `config/pricing`; do not hard-code changes.
