#!/usr/bin/env python3
"""Linen Legends (Framer) page static checks, run before every auto-ship.

Usage:  python3 verify/framer_static.py site/linen-legends-framer.html
Checks: inline scripts parse, no duplicate ids, every getElementById target exists,
every referenced local asset exists. Exit 0 = PASS.
"""
import collections, os, re, subprocess, sys, tempfile

path = sys.argv[1]
h = open(path).read()
base = os.path.dirname(path)
fail = 0

for i, s in enumerate(re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', h, re.S)):
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t:
        t.write(s)
    r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
    if r.returncode:
        fail += 1
        print('FAIL script', i, r.stderr[:300])

ids = collections.Counter(re.findall(r'\bid="([^"]+)"', h))
dup = [k for k, v in ids.items() if v > 1]
if dup:
    fail += 1
    print('FAIL duplicate ids', dup)

missing = sorted(x for x in set(re.findall(r"getElementById\(['\"]([^'\"]+)", h)) if x not in ids)
if missing:
    fail += 1
    print('FAIL getElementById targets missing', missing)

assets = sorted(r for r in set(re.findall(r'linen-legends-framer-assets/[\w.-]+', h))
                if not os.path.exists(os.path.join(base, r)))
if assets:
    fail += 1
    print('FAIL missing assets', assets)

print('RESULT:', 'FAIL' if fail else 'PASS')
sys.exit(1 if fail else 0)
