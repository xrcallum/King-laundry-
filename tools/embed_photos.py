#!/usr/bin/env python3
"""Embed real photographs into the journey steps on the home page.

The site ships as one self-contained HTML file, so a photograph cannot be a
sibling asset — it has to travel inside the document. This resizes each photo
to the size it is actually displayed at, encodes it as WebP and writes it into
the matching .jn-art slot as a data URI.

Usage:  python3 tools/embed_photos.py site/laundrykings-site.html [--dir site/photos]
        python3 tools/embed_photos.py site/laundrykings-site.html --strip

Put the photographs in site/photos as jn-1 … jn-5 (.jpg, .jpeg, .png or .webp)
and give each one an entry in site/photos/photos.json:

    "jn-2": {
      "alt":     "Hands holding a digital scale with a laundry bag hanging from it",
      "source":  "Unsplash",
      "credit":  "Jane Doe",
      "licence": "Unsplash License - commercial use, no attribution required",
      "url":     "https://unsplash.com/photos/abc123"
    }

`alt` and `source` are required; anything not shot by us also needs `licence`
and `url`, which is the licence record a commercial site has to be able to
produce. For your own work, "source": "LaundryKings own photograph" is enough.
The alt text is not generated: it describes a photograph this script has never
seen, so only the person who chose it can write it.

Every run rewrites site/photos/CREDITS.md from these entries. A step with no
photo keeps its drawing. Re-running replaces what an earlier run embedded, so
this is safe to run as often as you like.

Requires Node with Playwright and a Chromium build — the same dependency
dossier/build.py already has. No Python image library is needed.
"""
import base64
import json
import os
import re
import subprocess
import sys
import tempfile

here = os.path.dirname(os.path.abspath(__file__))

SLOTS = ["jn-1", "jn-2", "jn-3", "jn-4", "jn-5"]
EXTS = (".jpg", ".jpeg", ".png", ".webp")

# .jn-art.has-photo is 4:3 and at most one fifth of the 1180px wrap, so ~236px
# wide on the widest layout. 640x480 covers that at better than 2x for a retina
# phone and still lands around 40 KB a photo.
OUT_W, OUT_H = 640, 480
QUALITY = 0.82

# Canvas does the resize and the encode: Chromium is already a build dependency
# and this avoids adding Pillow or OpenCV just to shrink five pictures.
ENCODE_JS = r"""
const {chromium} = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  const p = await b.newPage();
  const out = {};
  for (const j of jobs) {
    const bytes = fs.readFileSync(j.path).toString('base64');
    out[j.slot] = await p.evaluate(async ({bytes, type, w, h, q}) => {
      const img = new Image();
      img.src = 'data:' + type + ';base64,' + bytes;
      await img.decode();
      // Cover-crop to the target ratio before scaling, so the encoded pixels
      // are exactly what object-fit:cover would have shown. Nothing is paying
      // for detail the layout then crops away.
      const scale = Math.max(w / img.width, h / img.height);
      const sw = w / scale, sh = h / scale;
      const c = document.createElement('canvas');
      c.width = w; c.height = h;
      c.getContext('2d').drawImage(img, (img.width - sw) / 2, (img.height - sh) / 2,
                                   sw, sh, 0, 0, w, h);
      return c.toDataURL('image/webp', q);
    }, {bytes, type: j.type, w: j.w, h: j.h, q: j.q});
  }
  await b.close();
  fs.writeFileSync(process.argv[3], JSON.stringify(out));
})().catch(e => { console.error(e); process.exit(1); });
"""

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}


def find_photos(photo_dir):
    """Slot -> source path, for every slot that actually has a file."""
    found = {}
    for slot in SLOTS:
        for ext in EXTS:
            cand = os.path.join(photo_dir, slot + ext)
            if os.path.exists(cand):
                if slot in found:
                    sys.exit(f"two files for {slot}: {found[slot]} and {cand} — keep one")
                found[slot] = cand
    return found


# A photo off a stock library carries terms; a photo one of us took does not.
# Either way, "where did this come from" has to be written down before it ships
# rather than reconstructed a year later.
OWN = "laundrykings own photograph"


def load_meta(photo_dir, slots):
    meta_path = os.path.join(photo_dir, "photos.json")
    if not os.path.exists(meta_path):
        sys.exit(f"{meta_path} is missing — every photo needs alt text and a source")
    meta = json.load(open(meta_path, encoding="utf-8"))
    out, problems = {}, []
    for slot in slots:
        e = meta.get(slot) or {}
        got = {k: str(e.get(k, "")).strip() for k in ("alt", "source", "credit", "licence", "url")}
        for field in ("alt", "source"):
            if not got[field]:
                problems.append(f"{slot}: no {field}")
        if got["source"] and got["source"].lower() != OWN:
            for field in ("licence", "url"):
                if not got[field]:
                    problems.append(f"{slot}: source is {got['source']!r}, so {field} is required")
        out[slot] = got
    if problems:
        sys.exit("photos.json is incomplete:\n  " + "\n  ".join(problems))
    return out


def write_credits(photo_dir, meta, photos):
    """The licence record, regenerated from photos.json on every run."""
    out = ["# Photograph credits and licences", "",
           "Generated by `tools/embed_photos.py` — do not edit, change `photos.json`.", ""]
    for slot in sorted(photos):
        e = meta[slot]
        out += [f"## {slot} — {os.path.basename(photos[slot])}", "",
                f"- **Source:** {e['source']}"]
        for label, key in (("Credit", "credit"), ("Licence", "licence"), ("Where from", "url")):
            if e[key]:
                out.append(f"- **{label}:** {e[key]}")
        out += [f"- **Alt text:** {e['alt']}", ""]
    path = os.path.join(photo_dir, "CREDITS.md")
    open(path, "w", encoding="utf-8").write("\n".join(out))
    return path


def encode(photos):
    jobs = [{"slot": s, "path": os.path.abspath(p), "type": MIME[os.path.splitext(p)[1].lower()],
             "w": OUT_W, "h": OUT_H, "q": QUALITY} for s, p in sorted(photos.items())]
    js = os.path.join(here, "_encode.js")
    open(js, "w").write(ENCODE_JS)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(jobs, f)
        jobs_path = f.name
    out_path = jobs_path + ".out"
    try:
        subprocess.run(["node", js, jobs_path, out_path], check=True,
                       env=dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules"))
        return json.load(open(out_path, encoding="utf-8"))
    finally:
        for f in (js, jobs_path, out_path):
            if os.path.exists(f):
                os.unlink(f)


def strip(src):
    """Remove anything a previous run embedded, so this script is idempotent."""
    src = re.sub(r'\s*<img class="jn-photo"[^>]*>', "", src)
    return src.replace('<div class="jn-art has-photo"', '<div class="jn-art"')


def embed(src, slot, data_uri, alt):
    esc = alt.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
    open_tag = '<div class="jn-art" data-photo="%s">' % slot
    if open_tag not in src:
        sys.exit(f"no .jn-art slot for {slot} in the page")
    img = '\n          <img class="jn-photo" src="%s" alt="%s" loading="lazy" decoding="async" width="%d" height="%d">' % (
        data_uri, esc, OUT_W, OUT_H)
    return src.replace(
        open_tag,
        '<div class="jn-art has-photo" data-photo="%s">%s' % (slot, img), 1)


def main(path, photo_dir, strip_only=False):
    src = open(path, encoding="utf-8").read()
    before = len(src)
    src = strip(src)

    if strip_only:
        open(path, "w", encoding="utf-8").write(src)
        print(f"stripped embedded photos: {before:,} -> {len(src):,} bytes")
        return 0

    photos = find_photos(photo_dir)
    if not photos:
        open(path, "w", encoding="utf-8").write(src)
        print(f"no photos in {photo_dir} — every step keeps its drawing")
        print("  expected: " + ", ".join(s + "{" + "|".join(e[1:] for e in EXTS) + "}" for s in SLOTS[:1]) + " … jn-5")
        return 0

    meta = load_meta(photo_dir, sorted(photos))
    encoded = encode(photos)

    for slot in sorted(photos):
        uri = encoded[slot]
        src = embed(src, slot, uri, meta[slot]["alt"])
        kb = len(uri) * 3 // 4 // 1024
        print(f"  {slot}  {os.path.basename(photos[slot])}  ->  {kb} KB webp"
              f"  ·  {meta[slot]['source']}")

    open(path, "w", encoding="utf-8").write(src)
    print("credits: " + write_credits(photo_dir, meta, photos))
    drawn = [s for s in SLOTS if s not in photos]
    print(f"{len(photos)} photo(s) embedded, {len(drawn)} step(s) still drawn"
          + (": " + ", ".join(drawn) if drawn else ""))
    print(f"{before:,} -> {os.path.getsize(path):,} bytes")
    print("now run: python3 verify/preflight.py " + path)
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    d = "site/photos"
    if "--dir" in sys.argv:
        d = sys.argv[sys.argv.index("--dir") + 1]
    sys.exit(main(args[0], d, strip_only="--strip" in sys.argv))
