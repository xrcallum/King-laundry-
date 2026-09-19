#!/usr/bin/env python3
"""Build the Laundrylegends dossier.

Concatenates the part files, embeds the pre-flight script into Appendix A,
generates Appendix C verbatim from the site source of record, renders to PDF
with Chromium, then makes a second pass that writes real page numbers into the
contents and re-renders.

Usage: python3 dossier/build.py <site.html> <preflight.py> <out.html> <out.pdf>
"""
import hashlib
import html
import os
import re
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
site_path, preflight_path, out_html, out_pdf = sys.argv[1:5]

PARTS = ["00_head.html", "01_parts0_3.html", "02_parts4_8.html", "03_parts9_13.html",
         "04_parts14_18.html", "05_appendixAB.html"]


def assemble():
    body = "".join(open(os.path.join(here, p), encoding="utf-8").read() for p in PARTS)

    # Appendix A: the pre-flight script, verbatim
    pf = open(preflight_path, encoding="utf-8").read()
    body = body.replace("<!--PREFLIGHT_LISTING-->", "<pre>" + html.escape(pf) + "</pre>")

    # Appendix C: the site source, verbatim, wrapped not truncated
    src = open(site_path, encoding="utf-8").read()
    lines = src.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    sha = hashlib.sha256(open(site_path, "rb").read()).hexdigest()
    size = os.path.getsize(site_path)

    appc = [f'''
<div class="part">
<p class="part-kicker">Appendix C</p>
<h1>Complete website source code, v4.4 (repository copy of record)</h1>
<p class="lede">The entire Laundrylegends site: marketing, customer app and ops backend, one self-contained HTML file. Reproduced verbatim from <code>site/laundrylegends-site.html</code> on the working branch; the live artefact still carries v4.2 until a principal publishes. {len(lines):,} lines, {size:,} bytes. SHA-256 <span class="mono">{sha}</span>.</p>
<div class="box"><h4>Read this before using the listing</h4><p>Long lines wrap to the next line here rather than being cut, so the listing is complete. Line numbers are the source line numbers. For editing, use <code>site/laundrylegends-site.html</code> in the Git repository, which is the copy of record; this appendix is for a paper reader and for disaster recovery only. The v1 dossier truncated 351 lines; this one truncates none.</p></div>
<div class="codehead">laundrylegends-site.html</div>
<pre class="code">''']
    for i, l in enumerate(lines, 1):
        appc.append(f'<span class="ln">{i}</span>{html.escape(l)}\n')
    appc.append("</pre></div>")
    body += "".join(appc)

    body += open(os.path.join(here, "06_appendixD.html"), encoding="utf-8").read()
    body += open(os.path.join(here, "07_appendixE.html"), encoding="utf-8").read()
    body += "\n</body></html>\n"
    return body


RENDER_JS = r"""
const {chromium}=require('playwright');
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage();
  await p.goto('file://'+process.argv[2],{waitUntil:'networkidle'});
  await p.waitForTimeout(800);
  await p.pdf({path:process.argv[3],format:'A4',printBackground:true,preferCSSPageSize:true,
    displayHeaderFooter:true,
    headerTemplate:'<div style="font-family:Arial,sans-serif;font-size:7pt;color:#6B7386;width:100%;padding:0 15mm;display:flex;justify-content:space-between"><span>Laundrylegends &#8212; Complete Project Dossier v3</span><span>19 September 2026</span></div>',
    footerTemplate:'<div style="font-family:Arial,sans-serif;font-size:7pt;color:#6B7386;width:100%;padding:0 15mm;display:flex;justify-content:space-between"><span>Prepared for Max Jones and Callum Page &#183; MAXCAL | Laundrylegends</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>',
    margin:{top:'16mm',bottom:'18mm',left:'15mm',right:'15mm'}});
  await b.close();
  console.log('pdf ok');
})().catch(e=>{console.error(e);process.exit(1)});
"""


def render(html_path, pdf_path):
    rp = os.path.join(here, "_render.js")
    open(rp, "w").write(RENDER_JS)
    env = dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules")
    subprocess.run(["node", rp, os.path.abspath(html_path), os.path.abspath(pdf_path)],
                   check=True, env=env)
    os.unlink(rp)


def page_map(pdf_path):
    """First PDF page on which each part or appendix starts.

    The .part-kicker is uppercased by CSS, so it extracts as 'PART 7' while every
    cross-reference in body text reads 'Part 7'. That case difference is what makes
    this safe.
    """
    import pymupdf
    doc = pymupdf.open(pdf_path)
    found = {}
    for i, page in enumerate(doc, 1):
        text = page.get_text() or ""
        for m in re.finditer(r"\bPART (\d+)\b", text):
            found.setdefault(f"Part {m.group(1)}", i)
        for m in re.finditer(r"\bAPPENDIX ([A-E])\b", text):
            found.setdefault(f"Appendix {m.group(1)}", i)
    return found


def fill_toc(body, pages):
    def repl(m):
        n = pages.get(m.group(1))
        if n is None:
            return m.group(0)
        return re.sub(r'<span class="r">[^<]*</span>', f'<span class="r">p. {n}</span>', m.group(0))
    return re.sub(r'<li><span>(Part \d+|Appendix [A-E]) —.*?</li>', repl, body)


body = assemble()
open(out_html, "w", encoding="utf-8").write(body)
print(f"pass 1: html {len(body.encode()):,} bytes")
render(out_html, out_pdf)

pages = page_map(out_pdf)
missing = [k for k in ([f"Part {i}" for i in range(19)] + [f"Appendix {c}" for c in "ABCDE"])
           if k not in pages]
if missing:
    print("WARNING: no page number found for", missing)
body2 = fill_toc(body, pages)
open(out_html, "w", encoding="utf-8").write(body2)
print(f"pass 2: contents filled for {len(pages)} entries")
render(out_html, out_pdf)

import pymupdf  # noqa: E402
print(f"done: {out_pdf} — {pymupdf.open(out_pdf).page_count} pages, {os.path.getsize(out_pdf):,} bytes")
