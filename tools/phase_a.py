#!/usr/bin/env python3
"""Phase A — Foundation. Dossier v2, Part 14.

Fixes D2, D3, D4, D7, D15, D16, D17, D18, D20:
  1. tracking tokens by size, replacing 13 ad-hoc letter-spacing values
  2. an eight-step type scale replacing 57 font sizes
  3. three radius tokens plus a pill, replacing 17 values
  4. solid state colours; no rgba over a coloured surface (kills the purple bug)
  5. money() strips .00 on whole dollars; tabular numerals on every price
  6. an SVG symbol sprite replacing every emoji
  7. card borders that can be seen; card shadows removed
  8. muted text darkened to pass 4.5:1; red never sits on navy

Run:  python3 tools/phase_a.py site/laundrylegends-site.html
It rewrites the file in place and prints a change report.
"""
import re
import sys
import collections

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from icons import sprite_html, use  # noqa: E402

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
before = src
log = collections.Counter()


def contrast(a, b):
    def lum(h):
        h = h.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        r, g, bl = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        return .2126 * f(r) + .7152 * f(g) + .0722 * f(bl)
    la, lb = lum(a), lum(b)
    return round((max(la, lb) + .05) / (min(la, lb) + .05), 2)


# =====================================================================
# 1. Design tokens
# =====================================================================
OLD_ROOT_TAIL = """  --maxw:1180px; --px:clamp(1.1rem,4.5vw,2.75rem); --spy:clamp(3.5rem,7vw,5.5rem);
  --r:6px; --r2:12px; --r3:18px;
  --sh:0 1px 3px rgba(20,24,38,.07),0 6px 24px rgba(20,24,38,.06);
  --sh2:0 18px 50px rgba(20,24,38,.16);
  --tr:.18s ease;"""

NEW_ROOT_TAIL = """  --maxw:1180px; --px:clamp(1.1rem,4.5vw,2.75rem); --spy:clamp(3.5rem,7vw,5.5rem);

  /* Type scale — 1.25 major third, eight steps. Nothing outside this list. */
  --fs-badge:11px;   /* numeric badges and fixed-height chrome only */
  --fs-micro:13px; --fs-body:16px; --fs-5:20px; --fs-4:25px;
  --fs-3:31px; --fs-2:39px; --fs-1:49px; --fs-display:61px;
  --fs-hero:clamp(2.8rem,6.5vw,5.4rem);
  --fs-h1:clamp(1.9375rem,4vw,3.0625rem);
  --fs-h2:clamp(1.5625rem,3.2vw,2.4375rem);
  --fs-h3:clamp(1.25rem,2.6vw,1.5625rem);

  /* Tracking loosens as size drops. */
  --track-display:-.04em; --track-h1:-.03em; --track-h2:-.02em; --track-h3:-.01em;
  --track-body:0; --track-micro:.01em; --track-caps:.08em;

  /* Radius: three steps, a pill and a circle. */
  --r:6px; --r2:12px; --r3:18px; --r-pill:999px;

  /* Elevation: 0 surface step, 1 sticky chrome, 2 sheets and menus. */
  --sh1:0 1px 0 rgba(20,24,38,.09);
  --sh2:0 18px 50px rgba(20,24,38,.16);
  --sh:none;
  --tr:.18s ease;"""

assert OLD_ROOT_TAIL in src, "root tail not found"
src = src.replace(OLD_ROOT_TAIL, NEW_ROOT_TAIL)
log["root tokens"] += 1

# Muted text to 4.75:1; border colour to a step you can see; solid state colours.
src = src.replace("--ink:#141826; --body:#4A5266; --mute:#7C8598; --line:#E1E5EE;",
                  "--ink:#141826; --body:#454C60; --mute:#6B7386; --line:#D3D9E6; --line2:#BFC7D8;")
src = src.replace("--navy:#1A3480; --navy-d:#12245C; --navy-l:#2B4BAA; --navy-w:#F0F3FC;",
                  "--navy:#1A3480; --navy-d:#12245C; --navy-l:#2B4BAA; --navy-w:#F0F3FC;\n"
                  "  --navy-sel:#2A2F6B; --navy-hov:#23407A; --navy-raised:#22409A;\n"
                  "  --paper:#F6F3EE;")
log["colour tokens"] += 1

# =====================================================================
# 2. Type scale
# =====================================================================
LADDER = [(11, "var(--fs-badge)"), (13, "var(--fs-micro)"), (16, "var(--fs-body)"),
          (20, "var(--fs-5)"), (25, "var(--fs-4)"), (31, "var(--fs-3)"),
          (39, "var(--fs-2)"), (49, "var(--fs-1)"), (61, "var(--fs-display)")]


def nearest(px):
    return min(LADDER, key=lambda t: (abs(t[0] - px), -t[0]))[1]


# Selectors whose role decides the step, not arithmetic.
FORCE = {
    ".inp,.sel,.ta": "var(--fs-body)",          # 14px inputs make iOS zoom on focus
    ".prose p": "var(--fs-body)", ".prose li": "var(--fs-body)",
    ".faq button": "var(--fs-body)", ".faq .ans": "var(--fs-body)",
    ".card p": "var(--fs-body)", ".step p": "var(--fs-body)",
    ".bub": "var(--fs-body)", ".chk li": "var(--fs-body)", ".chk2 li": "var(--fs-body)",
    ".svc-c p": "var(--fs-body)", ".door p": "var(--fs-body)",
    ".hero-p": "var(--fs-5)", ".hero-v4 .hero-p": "var(--fs-5)", ".lede": "var(--fs-5)",
    ".lbl": "var(--fs-micro)", ".foot-bot": "var(--fs-micro)", ".fine": "var(--fs-micro)",
    ".plan p": "var(--fs-micro)", ".trust-p": "var(--fs-micro)", ".ap-fine": "var(--fs-micro)",
    ".plan h4": "var(--fs-body)", ".hero-ph": "var(--fs-body)",
}
for sel, tok in FORCE.items():
    pat = re.compile(r"(" + re.escape(sel) + r"\s*\{[^}]*?font-size:\s*)([^;}]+)")
    src, n = pat.subn(lambda m: m.group(1) + tok, src, count=1)
    if n:
        log["font-size role override"] += n
    else:
        print("  ! override selector not matched:", sel)

# Fluid headings.
for old, new in [
    ("clamp(2.15rem,4.6vw,3.55rem)", "var(--fs-hero)"),
    ("clamp(1.8rem,3.6vw,2.7rem)", "var(--fs-h1)"),
    ("clamp(1.5rem,2.9vw,2.2rem)", "var(--fs-h2)"),
    ("clamp(1.5rem,3vw,2.1rem)", "var(--fs-h2)"),
    ("clamp(1.35rem,3vw,1.75rem)", "var(--fs-h3)"),
]:
    src, n = re.subn(re.escape("font-size:" + old), "font-size:" + new, src)
    log["fluid heading"] += n

# Everything else by nearest step.
def repl_fs(m):
    val = m.group(1).strip()
    if val.startswith("var(") or val == "inherit":
        return m.group(0)
    mm = re.match(r"^([\d.]+)rem$", val)
    if not mm:
        print("  ! unmapped font-size:", val)
        return m.group(0)
    tok = nearest(float(mm.group(1)) * 16)
    log["font-size mapped"] += 1
    return "font-size:" + tok


src = re.sub(r"font-size:\s*([^;}\"']+)", repl_fs, src)

# =====================================================================
# 3. Tracking
# =====================================================================
TRACK = {
    "-.035em": "var(--track-h1)", "-.03em": "var(--track-display)",
    "-.025em": "var(--track-h2)", "-.02em": "var(--track-h2)", "-.01em": "var(--track-h3)",
    "0": "var(--track-body)", ".01em": "var(--track-micro)",
    ".02em": "var(--track-caps)", ".03em": "var(--track-caps)", ".06em": "var(--track-caps)",
    ".07em": "var(--track-caps)", ".09em": "var(--track-caps)", ".1em": "var(--track-caps)",
    ".14em": "var(--track-caps)",
}
def repl_ls(m):
    v = m.group(1).strip()
    if v.startswith("var("):
        return m.group(0)
    if v in TRACK:
        log["tracking mapped"] += 1
        return "letter-spacing:" + TRACK[v]
    print("  ! unmapped letter-spacing:", v)
    return m.group(0)


src = re.sub(r"letter-spacing:\s*([^;}\"']+)", repl_ls, src)
# The hero is the one display-tracked element; page H1s take h1 tracking.
src = src.replace(".hero-h{font-size:var(--fs-hero);letter-spacing:var(--track-display)",
                  ".hero-h{font-size:var(--fs-hero);letter-spacing:var(--track-display)")
src = re.sub(r"(\.phead h1\{[^}]*?letter-spacing:)var\(--track-h2\)", r"\1var(--track-h1)", src)

# =====================================================================
# 4. Radius
# =====================================================================
RAD = {"2px": "var(--r-pill)", "3px": "var(--r)", "5px": "var(--r)", "6px": "var(--r)",
       "9px": "var(--r)", "10px": "var(--r2)", "14px": "var(--r2)", "16px": "var(--r3)",
       "99px": "var(--r-pill)", "999px": "var(--r-pill)"}
def repl_r(m):
    v = m.group(1).strip()
    if v in RAD:
        log["radius mapped"] += 1
        return "border-radius:" + RAD[v]
    return m.group(0)


src = re.sub(r"border-radius:\s*([^;}\"']+)", repl_r, src)

# =====================================================================
# 5. Solid state colours — the purple bug and everything like it
# =====================================================================
REPL = [
    # D3/D16: 13% red over navy rendered indigo. Solid selected surface instead.
    (".plan:hover,.plan.on{border-color:var(--red);background:rgba(204,34,40,.13)}",
     ".plan:hover{border-color:rgba(255,255,255,.4);background:var(--navy-hov)}\n"
     ".plan.on{border-color:var(--white);background:var(--navy-sel)}"),
    (".plan{background:rgba(255,255,255,.06);border:2px solid rgba(255,255,255,.13)",
     ".plan{background:var(--navy);border:2px solid rgba(255,255,255,.22)"),
    # Red price figures on a navy surface measure 3.4:1. White on navy is 12.2:1.
    (".plan .amt{font-family:var(--fd);font-size:var(--fs-3);font-weight:900;color:var(--red-l)",
     ".plan .amt{font-family:var(--fd);font-size:var(--fs-3);font-weight:900;color:var(--white)"),
    (".sec-navy .card{background:rgba(255,255,255,.055)",
     ".sec-navy .card{background:var(--navy)"),
    (".sec-navy .card:hover{background:rgba(255,255,255,.08)",
     ".sec-navy .card:hover{background:var(--navy-hov)"),
    (".ap-sw{background:rgba(255,255,255,.1)", ".ap-sw{background:var(--navy-raised)"),
    (".ap-sw:hover{background:rgba(255,255,255,.18)", ".ap-sw:hover{background:var(--navy-hov)"),
    (".btn-ghost:hover{background:rgba(255,255,255,.08)",
     ".btn-ghost:hover{background:var(--navy-hov)"),
]
for old, new in REPL:
    if old in src:
        src = src.replace(old, new)
        log["solid state colour"] += 1
    else:
        print("  ! solid-colour target not found:", old[:60])

# =====================================================================
# 6. Money and numerals
# =====================================================================
OLD_MONEY = "const money = n => '$' + Number(n).toFixed(2);"
NEW_MONEY = ("const money = n => { const v = Number(n) || 0; "
             "return '$' + (Math.abs(v - Math.round(v)) < 0.005 ? String(Math.round(v)) : v.toFixed(2)); };")
assert OLD_MONEY in src
src = src.replace(OLD_MONEY, NEW_MONEY)
log["money()"] += 1

NUMERALS = (
    "\n/* Prices and figures align on the decimal. */\n"
    ".amt,.price,.qtot-v,.qtot-n,.hero-pc-tot-v,.hero-pc-row,.sumr,.bd,.prow,.kpi-c h4,"
    ".ptab,.inv-preview,.card .price,.svc-c .price,.opt-p,.pchip strong,.plan .amt,"
    ".cov-chip,.chip,.bkc-r,.num{font-variant-numeric:tabular-nums;font-feature-settings:'tnum' 1}\n"
)

# =====================================================================
# 7. Borders and shadows
# =====================================================================
n = src.count("box-shadow:var(--sh)")
src = src.replace("box-shadow:var(--sh)", "box-shadow:none")
log["card shadow removed"] += n
# Sticky chrome keeps a hairline instead.
src = src.replace("#nav{", "#nav{box-shadow:var(--sh1);")
log["sticky chrome shadow"] += 1

# =====================================================================
# 8. Icons
# =====================================================================
EMOJI_ICON = {
    "🧾": "receipt", "🧺": "basket", "🚚": "truck", "👕": "shirt", "👤": "user",
    "💬": "chat", "📍": "pin", "🔒": "lock", "🗓": "calendar", "📅": "calendar",
    "❓": "help", "👷": "worker", "⚖️": "scale", "⚖": "scale", "📄": "doc",
    "💳": "card", "✅": "check-circle", "✓": "check", "✉️": "mail", "✉": "mail",
    "⚠️": "alert", "⚠": "alert", "⚙️": "settings", "⚙": "settings",
    "🎧": "headset", "★": "star", "📦": "box", "✏️": "pencil", "✏": "pencil",
    "📣": "megaphone", "🛡️": "shield", "🛡": "shield", "📊": "chart", "🏦": "bank",
    "🔗": "link", "✕": "x", "➕": "plus-circle", "👑": "crown", "🆕": "sparkle",
    "📋": "clipboard", "📞": "phone", "↺": "refresh", "🔄": "refresh", "→": "arrow-right",
}

# 8a. <i>EMOJI</i> — the icon slots. Keep the <i> so existing flex rules hold.
def repl_i(m):
    glyph = m.group(1)
    name = EMOJI_ICON.get(glyph)
    if not name:
        print("  ! no icon for <i> glyph:", repr(glyph))
        return m.group(0)
    log["icon in <i>"] += 1
    return '<i class="ic">%s</i>' % use(name)


src = re.sub(r"<i>([^<]{1,4})</i>", repl_i, src)

# 8b. Loose glyphs in prose and JS template strings.
def repl_loose(m):
    glyph = m.group(0)
    name = EMOJI_ICON.get(glyph)
    if not name:
        print("  ! no icon for loose glyph:", repr(glyph))
        return glyph
    log["icon inline"] += 1
    cls = "ic ic-inl ic-aft" if name == "arrow-right" else "ic ic-inl"
    return use(name, cls)


src = re.sub("[\U0001F000-\U0001FAFF☀-➿⬀-⯿←-⇿⌀-⏿]️?",
             repl_loose, src)

# 8c. The tick in a CSS ::before becomes a masked SVG, so no glyph survives.
TICK = ("data:image/svg+xml;utf8,"
        "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' "
        "stroke='%23fff' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'"
        "%3E%3Cpath d='M4.6 12.4 9.6 17.4 19.4 6.8'/%3E%3C/svg%3E")
src = re.sub(r"content:'(?:&#10003;|\\2713)?'", "content:''", src)
src = src.replace("content:'✓';", "content:'';")
n = src.count("background-size:11px")
src = re.sub(r"(\.chk2 li::before\{content:'';)",
             r"\1background-image:url(\"%s\");background-repeat:no-repeat;"
             r"background-position:center;background-size:11px 11px;" % TICK, src)
log["css tick"] += 1

# 8d. Sprite into the document, right after <body>.
m = re.search(r"<body[^>]*>", src)
src = src[:m.end()] + "\n" + sprite_html() + src[m.end():]
log["sprite"] += 1

# 8e. Icon CSS, appended to the stylesheet.
ICON_CSS = """
/* ---------- ICONS ----------
   One set, 24px grid, 1.75 stroke, currentColor. No emoji anywhere. */
.ic{display:inline-flex;align-items:center;justify-content:center;flex:none;
    width:24px;height:24px;font-style:normal;color:inherit}
svg.ic{width:24px;height:24px}
.ic>svg{width:100%;height:100%;display:block}
.ic-inl{width:1.05em;height:1.05em;vertical-align:-.16em;margin-right:.34em}
.ic-aft{margin:0 0 0 .4em}
.ic-sm{width:18px;height:18px}
.ic-lg{width:32px;height:32px}
"""

src = src.replace("</style>", NUMERALS + ICON_CSS + "</style>", 1)
log["icon css"] += 1

open(path, "w", encoding="utf-8").write(src)

print("\nPhase A applied to", path)
for k, v in sorted(log.items()):
    print("  %-28s %d" % (k, v))
print("  size %d -> %d bytes" % (len(before.encode()), len(src.encode())))
print("\ncontrast checks")
for label, a, b in [("body #454C60 on white", "#454C60", "#FFFFFF"),
                    ("mute #6B7386 on white", "#6B7386", "#FFFFFF"),
                    ("line #D3D9E6 on white", "#D3D9E6", "#FFFFFF"),
                    ("line #D3D9E6 on bg2", "#D3D9E6", "#F7F8FC"),
                    ("white on navy-sel", "#FFFFFF", "#2A2F6B"),
                    ("white on navy", "#FFFFFF", "#1A3480")]:
    print("  %-26s %.2f:1" % (label, contrast(a, b)))
