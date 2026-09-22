# Laundrylegends — copy of record

Laundry pickup and delivery across Brisbane, Logan and South East Queensland.
This repository is the source of record for the website file and the project dossier.
The live site is published as a Claude artefact; the PDF dossier is for reading, this repo is for editing.

## Layout

| Path | What it is |
|---|---|
| `site/laundrylegends-site.html` | The complete website (marketing, customer app, ops backend) as one file. Renamed from `laundrykings-site.html` and rebranded LaundryKings → Laundrylegends on 19 September 2026; the live artefact needs republishing to match (see note below). |
| `site/linenlegends-site.html` | **Linen Legends**, one file. A structural replica of the FramerGeeks laundry template behind `laundryhub.framer.website`, transcribed from the canvas screenshot of 22 September 2026 because the egress allowlist denies every Framer domain. Template copy is verbatim where the screenshot was legible; everything unreadable is marked TO CONFIRM in amber on the page itself. Stock photos are labelled slots. **Replace this file with the real export** via `tools/import_framer.py`. `verify/preflight.py` does not apply to it. |
| `tools/import_framer.py` | Converts a Framer export or a browser "Save Page As" into one self-contained file in `site/`. Inlines local CSS, JS, fonts and images; strips the Framer badge and the FramerGeeks template promo layer; applies brand renames; reports unresolved assets, remaining remote hosts, duplicate IDs and missing AU compliance sentinels. Needed because this repo's automation cannot reach Framer: the egress allowlist excludes `framer.com`, `framer.app`, `framer.website` and `framerusercontent.com`. |
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

## Importing the Framer site

The Framer project cannot be fetched by automation here. The session egress proxy
runs an allowlist; `github.com` and the package registries are on it, Framer is not,
and a policy denial must be reported rather than routed around. So the export is a
manual step, done once.

1. Get the bytes out of Framer, either way:
   - Framer editor on desktop: project menu, then **Export**, and download the ZIP.
   - Any browser on the published URL: **Save Page As, "Web Page, Complete"**. Keep
     the `.html` and its assets folder together.
2. Convert it:

```
python3 tools/import_framer.py <zip-or-folder-or-html> \
    -o site/linenlegends-site.html \
    --rename "Laundry Hub=Linen Legends"
```

3. Read the report before committing. It exits non-zero if any local asset failed to
   resolve or an AU compliance sentinel is missing. Both mean the file is not ready
   to publish.
4. Check the remaining remote hosts. Anything still loading from
   `framerusercontent.com` is a live dependency on Framer's CDN; vendor those assets
   if the site must stand alone.


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
