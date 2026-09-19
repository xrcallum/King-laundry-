# LaundryKings — copy of record

Laundry collection and delivery Australia-wide.
This repository is the source of record for the website file and the project dossier.
The live site is published as a Claude artefact; the PDF dossier is for reading, this repo is for editing.

## Layout

| Path | What it is |
|---|---|
| `site/laundrykings-site.html` | The complete website (marketing, customer app, ops backend) as one file. v4.2, byte-identical to the live artefact. |
| `verify/preflight.py` | Pre-publish checks. Run before every publish. |
| `dossier/*.html`, `dossier/build.py` | Source and build script for the Complete Project Dossier. |
| `dossier/LKG-GOV00-01_Complete Dossier_v2.pdf` | The built dossier, revision 2, 19 September 2026. |

## Publish workflow (never skip a step)

1. Edit `site/laundrykings-site.html`.
2. `python3 verify/preflight.py site/laundrykings-site.html` (add `--strict-tokens` once Phase A has landed). It must print `RESULT: PASS`.
3. `NODE_PATH=/opt/node22/lib/node_modules node verify/collide.js site/laundrykings-site.html`. The floating layers (sticky pill, chat button, app tab bar, assistant panel) must not overlap each other or any button beneath them at phone widths. It must print `RESULT: PASS`. Preflight cannot see this class of bug; the collision check exists because it shipped once.
4. Commit with the artefact version in the message, e.g. `site: v4.3 Phase A foundation tokens`.
5. Publish to the live artefact, https://claude.ai/artifact/XUL5bw8tUeT25PTh4CcJ3S (published 19 September 2026; the earlier artefact was permanently deleted the same day), with capabilities `{"db":{},"user":{}}`, favicon crown, contract 0.2.52. Never add `mcp`. Publishing without that URL creates a second artefact instead of updating the live one.
6. Confirm on a phone.

## Rebuild the dossier

```
python3 dossier/build.py site/laundrykings-site.html verify/preflight.py \
  "dossier/LKG-GOV00-01_Complete Dossier_v2.html" "dossier/LKG-GOV00-01_Complete Dossier_v2.pdf"
```

Requires Python 3, Node with Playwright and a Chromium build. Appendix C of the PDF is generated from the site file at build time, so the PDF always matches the committed source.

## Rules that travel with the code

- Keep every existing element ID; the script depends on them.
- Never strip Australian compliance text (GST-inclusive pricing, NDIS statement, AS/NZS 4146 statement, contractor and WHS statements, ACL not-limited statement).
- Never invent footer entity text. Company name, ABN and address come from Max Jones.
- Pricing lives in the database document `config/pricing`; do not hard-code changes.
