#!/usr/bin/env python3
"""LaundryKings pre-publish checks.

Usage:  python3 verify/preflight.py site/laundrykings-site.html [--strict-tokens]

Exit code 0 = safe to publish. Every failing check is printed with a count so the
fix is measurable. Run it before EVERY publish of the live artefact.

Checks (Dossier v2, Appendix A):
  1. exactly one <script> block and it parses (node --check)
  2. no duplicate id="" attributes
  3. exactly 34 <section class="page"> elements
  4. every getElementById('x') target exists as an id
  5. zero emoji / pictographic glyphs anywhere in the file
  6. (--strict-tokens) no font-size or letter-spacing literal outside the design tokens
  7. every function called in the script is defined
  8. AU compliance sentinels present
  9. every var(--token) without a fallback resolves to a declared custom property
"""
import re
import subprocess
import sys
import tempfile
import collections
import os

EXPECTED_SECTIONS = 34

# Pictographs, dingbats, arrows, misc symbols, variation selectors.
EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF☀-➿⬀-⯿←-⇿⌀-⏿✀-➿️‍]"
)

# Tokens allowed once Phase A has landed. Adjust here, nowhere else.
ALLOWED_TRACKING = {"-0.04em", "-.04em", "-0.03em", "-.03em", "-0.02em", "-.02em", "-0.01em", "-.01em",
                    "0", "0em", "0.01em", ".01em", "0.08em", ".08em"}
ALLOWED_FONT_SIZE = {"13px", "16px", "20px", "25px", "31px", "39px", "49px", "61px",
                     "var(--fs-micro)", "var(--fs-body)", "var(--fs-5)", "var(--fs-4)", "var(--fs-3)",
                     "var(--fs-2)", "var(--fs-1)", "var(--fs-display)"}

# Anything the browser or the artefact runtime supplies.
JS_GLOBALS = set("""
if for while switch catch function return typeof new delete void do else try finally await async
parseInt parseFloat isNaN isFinite encodeURIComponent decodeURIComponent encodeURI decodeURI
setTimeout setInterval clearTimeout clearInterval requestAnimationFrame queueMicrotask
alert confirm prompt fetch atob btoa structuredClone eval
""".split())

COMPLIANCE_SENTINELS = [
    "NDIS",                 # support page statement
    "AS/NZS 4146",          # no clinical linen
    "ABN",                  # operators page + footer
    "GST",                  # inclusive pricing
    "Australian Consumer Law",
]



def strip_js(js):
    """Blank out comments, string/template literals and regex literals, so a name
    that appears inside prose, CSS text or a character class is never mistaken
    for a function call.

    Template literals are handled with a depth counter so that nested templates
    (backtick inside ${...} inside backtick) are correctly consumed.
    """
    out, i, n, prev = [], 0, len(js), ""
    while i < n:
        c = js[i]
        two = js[i:i + 2]
        if two == "/*":
            j = js.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        if two == "//":
            j = js.find("\n", i)
            i = n if j < 0 else j
            continue
        if c == "`":
            # Template literal — scan with brace depth tracking so nested
            # ${`...`} structures are consumed rather than breaking the scan.
            j, depth = i + 1, 0
            while j < n:
                ch = js[j]
                if ch == "\\":
                    j += 2
                    continue
                if ch == "$" and j + 1 < n and js[j + 1] == "{":
                    depth += 1
                    j += 2
                    continue
                if ch == "}" and depth > 0:
                    depth -= 1
                    j += 1
                    continue
                if ch == "`" and depth == 0:
                    break
                j += 1
            out.append(' "" ')
            i = j + 1
            prev = ")"
            continue
        if c in "'\"":
            q, j = c, i + 1
            while j < n:
                if js[j] == "\\":
                    j += 2
                    continue
                if js[j] == q:
                    break
                j += 1
            out.append(' "" ')
            i = j + 1
            prev = ")"
            continue
        if c == "/" and prev in "(,=:[!&|?{};+*%~^<>" :
            j, klass = i + 1, False
            while j < n:
                ch = js[j]
                if ch == "\\":
                    j += 2
                    continue
                if ch == "[":
                    klass = True
                elif ch == "]":
                    klass = False
                elif ch == "/" and not klass:
                    break
                elif ch == "\n":
                    break
                j += 1
            out.append(" RX ")
            i = j + 1
            prev = ")"
            continue
        out.append(c)
        if not c.isspace():
            prev = c
        i += 1
    return "".join(out)


def main(path, strict_tokens=False):
    src = open(path, encoding="utf-8").read()
    fails = []
    notes = []

    # 1. script parses
    # Only executable blocks count; application/ld+json is data, not code.
    scripts = [m.group(2) for m in re.finditer(r"<script\b([^>]*)>(.*?)</script>", src, re.S)
               if not re.search(r'type\s*=\s*["\']application/ld\+json["\']', m.group(1))]
    if len(scripts) != 1:
        fails.append(f"expected 1 <script> block, found {len(scripts)}")
    for i, s in enumerate(scripts):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(s)
            tmp = f.name
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        os.unlink(tmp)
        if r.returncode != 0:
            fails.append(f"script block {i} does not parse:\n{r.stderr.strip()[:800]}")
        else:
            notes.append(f"script block {i}: {len(s):,} chars, parses")

    # 2. duplicate ids
    ids = re.findall(r'\bid="([^"]+)"', src)
    dups = [k for k, v in collections.Counter(ids).items() if v > 1]
    if dups:
        fails.append(f"duplicate ids: {dups}")
    notes.append(f"{len(ids)} ids, {len(set(ids))} unique")

    # 3. sections
    n_sec = len(re.findall(r'<section class="page', src))
    if n_sec != EXPECTED_SECTIONS:
        fails.append(f"expected {EXPECTED_SECTIONS} page sections, found {n_sec}")
    else:
        notes.append(f"{n_sec} page sections")

    # 4. getElementById targets
    targets = set(re.findall(r"getElementById\(\s*['\"]([^'\"]+)['\"]\s*\)", src))
    missing = sorted(t for t in targets if t not in set(ids))
    if missing:
        fails.append(f"getElementById targets with no element: {missing}")
    notes.append(f"{len(targets)} getElementById targets, {len(missing)} missing")

    # 5. zero emoji
    found = EMOJI.findall(src)
    if found:
        c = collections.Counter(found).most_common(12)
        fails.append(f"{len(found)} emoji/pictographic glyphs remain ({len(set(found))} distinct). Top: {c}")
    else:
        notes.append("0 emoji glyphs")

    # 6. tokens
    if strict_tokens:
        # Stop at a quote too: inline style="" attributes are not brace-delimited.
        fs = [v for v in re.findall(r"font-size:\s*([^;}\"']+)", src)
              if v.strip() not in ALLOWED_FONT_SIZE and v.strip() != "inherit"
              and not v.strip().startswith("clamp(") and not v.strip().startswith("var(--fs-")]
        ls = [v for v in re.findall(r"letter-spacing:\s*([^;}\"']+)", src)
              if v.strip() not in ALLOWED_TRACKING and not v.strip().startswith("var(--track-")
              and not v.strip().startswith("var(")]
        if fs:
            fails.append(f"{len(fs)} font-size literals outside tokens: {sorted(set(v.strip() for v in fs))[:20]}")
        if ls:
            fails.append(f"{len(ls)} letter-spacing literals outside tokens: {sorted(set(v.strip() for v in ls))}")
        if not fs and not ls:
            notes.append("all font-size and letter-spacing values are tokens")

    # 7. every function called is defined
    raw = scripts[0] if scripts else ""
    js = strip_js(raw)
    defined = set(re.findall(r"\bfunction\s+([A-Za-z_$][\w$]*)", raw))
    defined |= set(re.findall(r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>", raw))
    defined |= set(re.findall(r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s+)?function", raw))
    called = set(re.findall(r"(?<![\w$.'\"])([a-z][A-Za-z_$0-9]*)\s*\(", js))
    unknown = sorted(c for c in called - defined - JS_GLOBALS)
    if unknown:
        fails.append("called but never defined: %s" % unknown)
    else:
        notes.append("every function called is defined")

    # 9. every var(--token) resolves
    # An undefined custom property is silently dropped by the browser: a missing
    # radius token squares every card off and nothing errors. JS may set a
    # property at runtime, so a var() carrying its own fallback is exempt.
    declared = set(re.findall(r"(--[A-Za-z0-9_-]+)\s*:", src))
    declared |= set(re.findall(r"setProperty\(\s*['\"](--[A-Za-z0-9_-]+)['\"]", src))
    used = collections.Counter(
        m.group(1) for m in re.finditer(r"var\(\s*(--[A-Za-z0-9_-]+)\s*\)", src))
    undefined = {k: v for k, v in used.items() if k not in declared}
    if undefined:
        detail = ", ".join(f"{k} x{v}" for k, v in sorted(undefined.items(), key=lambda kv: -kv[1]))
        fails.append(f"{sum(undefined.values())} var() references to undeclared tokens: {detail}")
    else:
        notes.append(f"{len(used)} distinct var() tokens, all declared")

    # 8. compliance sentinels
    for s in COMPLIANCE_SENTINELS:
        if s not in src:
            fails.append(f"AU compliance sentinel missing from file: {s!r}")

    size = os.path.getsize(path)
    lines = src.count("\n") + (0 if src.endswith("\n") else 1)
    print(f"preflight: {path}  {lines:,} lines  {size:,} bytes")
    for n in notes:
        print("  ok   ", n)
    for f in fails:
        print("  FAIL ", f)
    print("RESULT:", "PASS - safe to publish" if not fails else f"FAIL - {len(fails)} check(s) failed")
    return 0 if not fails else 1


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(args[0], strict_tokens="--strict-tokens" in sys.argv))
