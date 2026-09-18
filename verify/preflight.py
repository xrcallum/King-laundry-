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
  7. AU compliance sentinels present
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

COMPLIANCE_SENTINELS = [
    "NDIS",                 # support page statement
    "AS/NZS 4146",          # no clinical linen
    "ABN",                  # operators page + footer
    "GST",                  # inclusive pricing
    "Australian Consumer Law",
]


def main(path, strict_tokens=False):
    src = open(path, encoding="utf-8").read()
    fails = []
    notes = []

    # 1. script parses
    scripts = re.findall(r"<script\b[^>]*>(.*?)</script>", src, re.S)
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
        fs = [v for v in re.findall(r"font-size:\s*([^;}]+)", src) if v.strip() not in ALLOWED_FONT_SIZE
              and not v.strip().startswith("clamp(")]
        ls = [v for v in re.findall(r"letter-spacing:\s*([^;}]+)", src) if v.strip() not in ALLOWED_TRACKING
              and not v.strip().startswith("var(")]
        if fs:
            fails.append(f"{len(fs)} font-size literals outside tokens: {sorted(set(v.strip() for v in fs))[:20]}")
        if ls:
            fails.append(f"{len(ls)} letter-spacing literals outside tokens: {sorted(set(v.strip() for v in ls))}")
        if not fs and not ls:
            notes.append("all font-size and letter-spacing values are tokens")

    # 7. compliance sentinels
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
