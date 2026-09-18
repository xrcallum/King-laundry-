#!/usr/bin/env python3
"""Follow-up to content_update.py: the four ironing remnants it left behind —
a dead second field in the home quick-estimator, a comment, and two data
objects that still referenced PX.iron (which no longer exists, so this was
about to throw or write undefined into a saved quote)."""
import sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
log = []


def sub1(old, new, label):
    global src
    n = src.count(old)
    assert n == 1, "expected 1 occurrence of %r, found %d (%s)" % (old[:60], n, label)
    src = src.replace(old, new, 1)
    log.append(label)


# The home quick-estimator's second field only ever showed for the old
# combined wash+iron service. Nothing sets showB true any more, so this is
# dead markup with a stale label — and if left in place, the JS below that
# still reaches for #fldB would throw once the element were removed. Take
# out the field and every reference to it together.
sub1('''<div class="fld" id="fldB"><label class="lbl" id="lblB">Items to iron</label>
            <div class="stepper"><button type="button" data-step="b,-1" aria-label="Decrease"><svg class="ic" aria-hidden="true"><use href="#ic-minus"/></svg></button><span id="numB">0</span><button type="button" data-step="b,1" aria-label="Increase"><svg class="ic" aria-hidden="true"><use href="#ic-plus"/></svg></button></div>
          </div>
''', '', "removed the dead second field from the home quick-estimator")

sub1("  const fB = document.getElementById('fldB'), lA = document.getElementById('lblA'), lB = document.getElementById('lblB');\n  let sub = 0, lines = '', showB = false;",
     "  const lA = document.getElementById('lblA');\n  let sub = 0, lines = '';",
     "removed the now-unused fB/lB/showB from calc()")

sub1("    fB.style.display = 'none'; lA.textContent = 'Not applicable';",
     "    lA.textContent = 'Not applicable';",
     "removed the dead fB reference in the commercial branch")

sub1("  fB.style.display = showB ? '' : 'none';\n", "",
     "removed the dead fB reference at the end of calc()")

sub1("  <!-- optional volume (show for wf/wfi/iron) -->",
     "  <!-- optional volume (show for wf/linen) -->",
     "wizard comment updated")

sub1("    loads: C.a, ironItems: C.b,",
     "    loads: C.a,",
     "quote-request record: dropped the always-zero ironItems field")

sub1("    pricingSnapshot: { load: PX.load, iron: PX.iron, delivery: PX.delivery, minimum: PX.minimum }",
     "    pricingSnapshot: { load: PX.load, linenSheetSet: PX.linenSheetSet, delivery: PX.delivery, minimum: PX.minimum }",
     "quote-request pricing snapshot: PX.iron no longer exists")

open(path, "w", encoding="utf-8").write(src)
print("Follow-up applied:")
for l in log:
    print("  -", l)

import re
left = re.findall(r".{30}[Ii][Rr][Oo][Nn].{30}", src)
print("\nremaining 'iron' anywhere in the file:", len(left))
for l in left:
    print("   ", l)
