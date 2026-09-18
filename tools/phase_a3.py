#!/usr/bin/env python3
"""Phase A, part 3 — colour on navy surfaces (D16, D20).

Two problems the token pass exposed rather than created:

  1. Red text on a navy surface. Measured: red #CC2228 on navy 2.07:1 and on
     navy-d 2.67:1; red-l #E8474C on navy 2.94:1 and on navy-d 3.80:1. Only the
     hero heading is large enough for the 3:1 large-text floor, and even that
     sits below the 4.5:1 the rest of the page holds itself to.
  2. Secondary text set as white at 45-78% opacity over navy. White at 62% over
     navy measures about 3.6:1, so most of the supporting copy on every navy
     band fails the 4.5:1 body floor.

Both are fixed with solid tokens: #FFFFFF and #C9D2F2, which measure 11.37:1
and 7.57:1 on the lightest navy in use. The hero keeps its red, but as a slab
behind white text (5.49:1) rather than as red text on navy — which also gives
the page the single red slab the design direction asks for.

The wordmark keeps red on navy: WCAG exempts text that is part of a logo.
"""
import re
import sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
n = 0

# --- tokens ----------------------------------------------------------------
src = src.replace("  --navy-sel:#2A2F6B; --navy-hov:#23407A; --navy-raised:#22409A;",
                  "  --navy-sel:#2A2F6B; --navy-hov:#23407A; --navy-raised:#22409A;\n"
                  "  --on-navy:#FFFFFF;        /* primary text on any navy surface */\n"
                  "  --on-navy-2:#C9D2F2;      /* secondary text on navy — 7.57:1 at worst */")

# --- 1. every translucent white text colour becomes a solid token ----------
def solid(m):
    global n
    alpha = float(m.group(1))
    n += 1
    return "color:var(--on-navy)" if alpha >= 0.8 else "color:var(--on-navy-2)"


src = re.sub(r"color:rgba\(255,\s*255,\s*255,\s*(\.\d+|1|0?\.\d+)\)", solid, src)

# --- 2. red that sits on navy ---------------------------------------------
FIXES = [
    # The hero: red slab, white text. This is the page's one red slab.
    (".hero-h span{color:var(--red-l)}",
     ".hero-h span{color:var(--white);background:var(--red);"
     "padding:.02em .22em .08em;border-radius:6px;"
     "-webkit-box-decoration-break:clone;box-decoration-break:clone}"),
    # Eyebrows: red-l measures 3.86:1 on white, so the light-surface eyebrow
    # moves to the darker red; the navy-surface eyebrow moves off red entirely.
    (".sec-navy .eyebrow{color:var(--red-l)}", ".sec-navy .eyebrow{color:var(--on-navy-2)}"),
    (".sec-navy .cicon{color:var(--red-l)}", ".sec-navy .cicon{color:var(--on-navy)}"),
    (".svc-c.hl .price{color:var(--red-l);", ".svc-c.hl .price{color:var(--on-navy);"),
    (".kc-save-m b{color:var(--red-l);font-weight:800}",
     ".kc-save-m b{color:var(--on-navy);font-weight:800}"),
    ("#mob a:hover{color:var(--red-l)}", "#mob a:hover{color:var(--on-navy);text-decoration:underline}"),
    # The savings box: translucent white over navy becomes a solid raised surface.
    (".kc-save{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.16)",
     ".kc-save{background:var(--navy-raised);border:1px solid rgba(255,255,255,.28)"),
]
for old, new in FIXES:
    if old in src:
        src = src.replace(old, new)
        n += 1
    else:
        print("  ! not found:", old[:66])

# The base eyebrow is used on light surfaces; red-l fails 4.5:1 there.
src = re.sub(r"(\.eyebrow\{[^}]*?)color:var\(--red-l\)", r"\1color:var(--red)", src, count=1)

# The hero eyebrow sits on navy-d.
src = src.replace(".hero-h span{color:var(--white)",
                  ".hero-v4 .eyebrow,.hero .eyebrow,#p-home .eyebrow{color:var(--on-navy-2)}\n"
                  ".hero-h span{color:var(--white)")

open(path, "w", encoding="utf-8").write(src)
print("phase A3 applied:", n, "colour corrections")
