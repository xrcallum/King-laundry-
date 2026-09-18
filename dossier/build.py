#!/usr/bin/env python3
"""Build the LaundryKings dossier: concatenate parts, generate Appendix C from the
site source of record, render to PDF with Chromium (Playwright).

Usage: python3 dossier/build.py <site.html> <preflight.py> <out.html> <out.pdf>
"""
import html
import os
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
site_path, preflight_path, out_html, out_pdf = sys.argv[1:5]

parts = ["00_head.html", "01_parts0_3.html", "02_parts4_8.html", "03_parts9_13.html",
         "04_parts14_18.html", "05_appendixAB.html"]
body = "".join(open(os.path.join(here, p), encoding="utf-8").read() for p in parts)

# Appendix A: embed the preflight script listing
pf = open(preflight_path, encoding="utf-8").read()
body = body.replace("<!--PREFLIGHT_LISTING-->", "<pre>" + html.escape(pf) + "</pre>")

# Appendix C: verbatim source, wrapped not truncated
src = open(site_path, encoding="utf-8").read()
lines = src.split("\n")
if lines and lines[-1] == "":
    lines = lines[:-1]
import hashlib
sha = hashlib.sha256(open(site_path, "rb").read()).hexdigest()
size = os.path.getsize(site_path)

appc = [f'''
<div class="part">
<p class="part-kicker">Appendix C</p>
<h1>Complete website source code, v4.2</h1>
<p class="lede">The entire LaundryKings site: marketing, customer app and ops backend, one self-contained HTML file. Reproduced verbatim from the live artefact. {len(lines):,} lines, {size:,} bytes. SHA-256 <span class="mono">{sha}</span>.</p>
<div class="box"><h4>Read this before using the listing</h4><p>Long lines wrap to the next line here rather than being cut, so the listing is complete. Line numbers are the source line numbers. For editing, use <code>site/laundrykings-site.html</code> in the Git repository, which is the copy of record; this appendix is for a paper reader and for disaster recovery only. The v1 dossier truncated 351 lines; this one truncates none.</p></div>
<div class="codehead">laundrykings-site.html</div>
<pre class="code">''']
for i, l in enumerate(lines, 1):
    appc.append(f'<span class="ln">{i}</span>{html.escape(l)}\n')
appc.append("</pre></div>")
body += "".join(appc)

body += "\n</body></html>\n"
open(out_html, "w", encoding="utf-8").write(body)
print("html written", out_html, len(body.encode()), "bytes")

# Render with Playwright
render = r"""
const {chromium}=require('playwright');
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage();
  await p.goto('file://'+process.argv[2],{waitUntil:'networkidle'});
  await p.waitForTimeout(800);
  await p.pdf({path:process.argv[3],format:'A4',printBackground:true,preferCSSPageSize:true,
    displayHeaderFooter:true,
    headerTemplate:'<div style="font-family:Arial,sans-serif;font-size:7pt;color:#6B7386;width:100%;padding:0 15mm;display:flex;justify-content:space-between"><span>LaundryKings — Complete Project Dossier v2</span><span>19 September 2026</span></div>',
    footerTemplate:'<div style="font-family:Arial,sans-serif;font-size:7pt;color:#6B7386;width:100%;padding:0 15mm;display:flex;justify-content:space-between"><span>Prepared for Max Jones and Callum Page · MAXCAL | LaundryKings</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>',
    margin:{top:'16mm',bottom:'18mm',left:'15mm',right:'15mm'}});
  await b.close();
  console.log('pdf written');
})().catch(e=>{console.error(e);process.exit(1)});
"""
rp = os.path.join(here, "_render.js")
open(rp, "w").write(render)
env = dict(os.environ, NODE_PATH="/opt/node22/lib/node_modules")
subprocess.run(["node", rp, os.path.abspath(out_html), os.path.abspath(out_pdf)], check=True, env=env)
os.unlink(rp)
