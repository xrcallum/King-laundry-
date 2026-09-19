# LaundryKings — copy of record

Laundry pickup and delivery across Brisbane, Logan and South East Queensland.
This repository is the source of record for the website file and the project dossier.
The live site is published as a Claude artefact; the PDF dossier is for reading, this repo is for editing.

## Layout

| Path | What it is |
|---|---|
| `site/laundrykings-site.html` | The complete website (marketing, customer app, ops backend) as one file. v4.2, byte-identical to the live artefact. |
| `verify/preflight.py` | Pre-publish checks. Run before every publish. |
| `site/photos/` | Journey photographs, the sourcing brief, the alt text and `CREDITS.md` — the licence record. Empty until the photos land. |
| `tools/embed_photos.py` | Puts those photographs into the journey steps on the home page, as resized WebP data URIs. `--strip` takes them back out. |
| `dossier/*.html`, `dossier/build.py` | Source and build script for the Complete Project Dossier. |
| `dossier/LKG-GOV00-01_Complete Dossier_v2.pdf` | The built dossier, revision 2, 19 September 2026. |

## Publish workflow (never skip a step)

1. Edit `site/laundrykings-site.html`.
2. `python3 verify/preflight.py site/laundrykings-site.html` (add `--strict-tokens` once Phase A has landed). It must print `RESULT: PASS`.
3. Commit with the artefact version in the message, e.g. `site: v4.3 Phase A foundation tokens`.
4. Publish to the existing artefact URL with capabilities `{"db":{},"user":{}}`, favicon crown, contract 0.2.52. Never add `mcp`.
5. Confirm on a phone.

## Add or change the journey photographs

The five steps in "How a collection actually goes" ship as drawings and are
replaced one at a time by real photographs. `site/photos/README.md` has the shot
list and the rules. Once the files and their alt text are in `site/photos`:

```
python3 tools/embed_photos.py site/laundrykings-site.html
python3 verify/preflight.py site/laundrykings-site.html
```

Then follow the publish workflow above. Steps without a photo keep their drawing.

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
- Every image needs alt text describing what is in the frame. Preflight enforces it.
- Every photograph needs a recorded source, and a licence and URL unless we shot it.
  `tools/embed_photos.py` refuses to embed one without, and writes `site/photos/CREDITS.md`.
- No photograph of an identifiable person, house number or number plate without a
  signed release on file.
- No other company's branding, signage or livery in any photograph.
