#!/usr/bin/env python3
"""Content update, 19 Sep 2026: drop the duplicate location line, remove every
ironing service, add a blankets/rugs/sheets-only service in its place, and
raise the three Kings Club subscription prices by 30%.

Run:  python3 tools/content_update.py site/laundrylegends-site.html
"""
import re
import sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
log = []


def sub1(old, new, label, count=1):
    global src
    n = src.count(old)
    assert n == count, "expected %d occurrence(s) of %r, found %d (%s)" % (count, old[:60], n, label)
    src = src.replace(old, new, count)
    log.append(label)


# =====================================================================
# 1. Top of page said the service area twice in the first screen: the
#    site-wide top strip, then the home hero eyebrow directly below it.
#    The top strip is on every route; the hero eyebrow only duplicated it
#    on home. Drop the hero eyebrow and let the H1 lead.
# =====================================================================
sub1('        <span class="eyebrow">BRISBANE · LOGAN · SOUTH EAST QLD</span>\n',
     '',
     "removed the duplicate BRISBANE · LOGAN · SOUTH EAST QLD line under the hero (top strip already states it)")

# =====================================================================
# 2. Pricing: three new per-item prices for the replacement service,
#    ironing prices removed, Kings Club raised 30%.
# =====================================================================
sub1("""const DEFAULT_PRICING = {
  load: 32.00,          // per ~5kg load, wash & fold
  iron: 3.50,           // per item, press only
  ironTrouser: 4.50,
  delivery: 13.50,      // collection + return, one flat fee
  minimum: 73.50,   // Laundry Lady $70 min +5% — decision 18 Sep 2026
  dcJacket: 18.50,
  dcDress: 16.50,
  dcSuit: 32.00,
  bulkDoona: 45.00,
  bulkDoonaKing: 75.00,
  bulkCurtain: 38.00,
  ecoAddon: 3.50,
  plan1: 49.00, plan2: 69.00, plan3: 89.00
};""",
     """const DEFAULT_PRICING = {
  load: 32.00,          // per ~5kg load, wash & fold
  delivery: 13.50,      // collection + return, one flat fee
  minimum: 73.50,   // Laundry Lady $70 min +5% — decision 18 Sep 2026
  dcJacket: 18.50,
  dcDress: 16.50,
  dcSuit: 32.00,
  bulkDoona: 45.00,
  bulkDoonaKing: 75.00,
  bulkCurtain: 38.00,
  linenSheetSet: 24.00,   // sheet set, per set — large-linen service, not by weight
  linenBlanket: 32.00,    // single/double blanket or quilt cover, per item
  linenRug: 42.00,        // rug or floor mat, per item, subject to size
  ecoAddon: 3.50,
  // Kings Club, +30% on the launch rate, effective 19 Sep 2026
  plan1: 63.70, plan2: 89.70, plan3: 115.70
};""",
     "no more ironing prices; three new large-linen prices; Kings Club +30%")

# =====================================================================
# 3. Service catalogue: drop wfi and iron, add linen
# =====================================================================
sub1("""const SVCS = [
  { id:'wf',   name:'Wash & Fold',          desc:'Washed on its own cycle, dried and folded.',          px:()=>'From '+money(PX.load)+' per load' },
  { id:'wfi',  name:'Wash, Fold & Iron',    desc:'Everything in Wash & Fold, plus pressing.',            px:()=>money(PX.load)+' + '+money(PX.iron)+'/item' },
  { id:'iron', name:'Ironing only',         desc:'Already washed — returned pressed and on hangers.',    px:()=>'From '+money(PX.iron)+' per item' },
  { id:'dc',   name:'Dry cleaning',         desc:'Suits, formal wear and delicates. PERC-free.',         px:()=>'From '+money(PX.dcDress)+' per item' },
  { id:'comm', name:'Commercial / linen',   desc:'Quoted per site — sends an enquiry, not a booking.',   px:()=>'By quote' }
];""",
     """const SVCS = [
  { id:'wf',    name:'Wash & Fold',                 desc:'Washed on its own cycle, dried and folded.',                          px:()=>'From '+money(PX.load)+' per load' },
  { id:'linen', name:'Blankets, Rugs & Sheets',      desc:'Large-format items only — not for everyday laundry.',                px:()=>'From '+money(PX.linenSheetSet)+' per item' },
  { id:'dc',    name:'Dry cleaning',                 desc:'Suits, formal wear and delicates. PERC-free.',                       px:()=>'From '+money(PX.dcDress)+' per item' },
  { id:'comm',  name:'Commercial / linen',           desc:'Quoted per site — sends an enquiry, not a booking.',                 px:()=>'By quote' }
];""",
     "service catalogue: no ironing, linen (blankets/rugs/sheets) added")

# =====================================================================
# 4. Wizard tile grid — same swap
# =====================================================================
sub1("""const SVC_GRID = [
  { id:'wfi',  name:'Washing', sub:'& Ironing',
    svg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2h12l2 6H4L6 2z"/><rect x="3" y="8" width="18" height="14" rx="3"/><path d="M9 8V6M15 8V6"/><line x1="9" y1="15" x2="15" y2="15"/></svg>' },
  { id:'wf',   name:'Wash, Dry', sub:'& Fold',
    svg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="3"/><circle cx="12" cy="13" r="5"/><line x1="5" y1="6" x2="8" y2="6"/><circle cx="11" cy="6" r="1" fill="currentColor"/></svg>' },
  { id:'iron', name:'Ironing', sub:'only',
    svg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18h18l-3-9H3l2 9z"/><path d="M18 9V5h4"/><line x1="7" y1="14" x2="13" y2="14"/></svg>' }
];""",
     """const SVC_GRID = [
  { id:'wf',    name:'Wash, Dry', sub:'& Fold',
    svg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="3"/><circle cx="12" cy="13" r="5"/><line x1="5" y1="6" x2="8" y2="6"/><circle cx="11" cy="6" r="1" fill="currentColor"/></svg>' },
  { id:'linen', name:'Blankets, Rugs', sub:'& Sheets',
    svg:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M3 16q1.5 2 3 0t3 0 3 0 3 0 3 0 3 0"/><path d="M8 4v12M14 4v12"/></svg>' }
];""",
     "wizard tiles: Wash & Fold, Blankets/Rugs & Sheets")

# =====================================================================
# 5. Home page: 3-card grid to 2 cards. Wash & Fold takes the "most
#    booked" highlight; the old ironing-only slot becomes the new service.
# =====================================================================
sub1('''    <div class="svc3">
      <div class="svc-c">
        <h3>Wash &amp; Fold</h3>
        <p>Everyday washing, collected and washed on its own cycle. Lights and darks separated as standard. Dried and folded.</p>
        <span class="price" data-px="wf"></span>
        <a href="#/book" class="btn btn-out svc-cta">Book Wash &amp; Fold <svg class="ic ic-inl ic-aft" aria-hidden="true"><use href="#ic-arrow-right"/></svg></a>
      </div>
      <div class="svc-c hl">
        <span class="svc-c-tag">MOST BOOKED</span>
        <h3>Wash, Fold &amp; Iron</h3>
        <p>Everything in Wash &amp; Fold, plus pressing. Work shirts, school uniforms, anything that needs to look sharp.</p>
        <span class="price" data-px="wfi"></span>
        <a href="#/book" class="btn svc-cta">Book Wash, Fold &amp; Iron <svg class="ic ic-inl ic-aft" aria-hidden="true"><use href="#ic-arrow-right"/></svg></a>
      </div>
      <div class="svc-c">
        <h3>Ironing Only</h3>
        <p>Already washed and just needs pressing. Collected and returned on hangers, ready to wear.</p>
        <span class="price" data-px="iron"></span>
        <a href="#/book" class="btn btn-out svc-cta">Book Ironing <svg class="ic ic-inl ic-aft" aria-hidden="true"><use href="#ic-arrow-right"/></svg></a>
      </div>
    </div>''',
     '''    <div class="svc3" style="grid-template-columns:1fr 1fr">
      <div class="svc-c hl">
        <span class="svc-c-tag">MOST BOOKED</span>
        <h3>Wash &amp; Fold</h3>
        <p>Everyday washing, collected and washed on its own cycle. Lights and darks separated as standard. Dried and folded.</p>
        <span class="price" data-px="wf"></span>
        <a href="#/book" class="btn svc-cta">Book Wash &amp; Fold <svg class="ic ic-inl ic-aft" aria-hidden="true"><use href="#ic-arrow-right"/></svg></a>
      </div>
      <div class="svc-c">
        <h3>Blankets, Rugs &amp; Sheets</h3>
        <p>Large-format items only — not for everyday laundry. Priced per item, not by weight.</p>
        <span class="price" data-px="linen"></span>
        <a href="#/book" class="btn btn-out svc-cta">Book Blankets &amp; Rugs <svg class="ic ic-inl ic-aft" aria-hidden="true"><use href="#ic-arrow-right"/></svg></a>
      </div>
    </div>''',
     "home page: two service cards, Wash & Fold now most-booked")

# =====================================================================
# 6. Kings Club teaser (home) — savings claim recomputed for the new
#    Solo price, ironing dropped from Full House
# =====================================================================
sub1('<div class="kc-save-m">Two ad-hoc loads a week ≈ $77.50 · Kings Club Solo = $49/week.<br><b>Save around $28 a week compared with two ad-hoc loads</b> — no lock-in, pause any time.</div>',
     '<div class="kc-save-m">Two ad-hoc loads a week ≈ $77.50 · Kings Club Solo = $63.70/week.<br><b>Save around $14 a week compared with two ad-hoc loads</b> — no lock-in, pause any time.</div>',
     "Kings Club saving recomputed for the new Solo price ($13.80, stated as ~$14)")

sub1('      <div class="plan"><h4>Full House</h4><div class="amt" data-px="p3"></div><p>Larger households. Three bags plus an ironing allowance.</p><div class="plan-cap">≈ 4–6 loads per week + ironing</div></div>',
     '      <div class="plan"><h4>Full House</h4><div class="amt" data-px="p3"></div><p>Larger households. Three bags each week.</p><div class="plan-cap">≈ 4–6 loads per week</div></div>',
     "home Full House card: no ironing allowance")

# =====================================================================
# 7. Club page (/club): lede and plan descriptions
# =====================================================================
sub1('<p class="lede">All plans include collection and return. Ironing can be added to any plan at the standard per-item rate.</p>',
     '<p class="lede">All plans include collection and return.</p>',
     "club page lede: no ironing rate")

sub1("""    plan('Solo', PX.plan1, 'One to two people. One standard bag each week, collected and returned. Ironing can be added per item.') +
    plan('Household', PX.plan2, 'Families of three to four. Two standard bags each week, collected and returned.') +
    plan('Full House', PX.plan3, 'Larger households. Three bags each week plus an allowance of ironed items included.');""",
     """    plan('Solo', PX.plan1, 'One to two people. One standard bag each week, collected and returned.') +
    plan('Household', PX.plan2, 'Families of three to four. Two standard bags each week, collected and returned.') +
    plan('Full House', PX.plan3, 'Larger households. Three bags each week, collected and returned.');""",
     "club page plan descriptions: no ironing")

# =====================================================================
# 8. Services page cards: drop Wash Fold & Iron, replace Ironing Only
# =====================================================================
sub1('''      <div class="card"><h3>Wash, Fold &amp; Iron</h3>
        <p>Washing plus pressing, priced per item ironed.</p>
        <ul class="chk2" style="margin-top:.9rem">
          <li>Everything included in Wash &amp; Fold</li>
          <li>Shirts, blouses, trousers and uniforms pressed</li>
          <li>Returned on hangers where you ask for it</li>
          <li>You choose which items are ironed — not the whole load</li>
        </ul>
        <span class="price" data-px="wfi"></span>
        <a href="#/book" class="btn btn-red btn-full" style="margin-top:1rem">Book Wash, Fold &amp; Iron <svg class="ic ic-inl ic-aft" aria-hidden="true"><use href="#ic-arrow-right"/></svg></a>
      </div>
      <div class="card"><h3>Ironing Only</h3>
        <p>For washing you have already done yourself.</p>
        <ul class="chk2" style="margin-top:.9rem">
          <li>Priced per item, no load charge</li>
          <li>Collected and returned on hangers</li>
          <li>Suitable for work shirts and uniform runs</li>
        </ul>
        <span class="price" data-px="iron"></span>
        <a href="#/book" class="btn btn-nv btn-full" style="margin-top:1rem">Book Ironing <svg class="ic ic-inl ic-aft" aria-hidden="true"><use href="#ic-arrow-right"/></svg></a>
      </div>''',
     '''      <div class="card"><h3>Blankets, Rugs &amp; Sheets</h3>
        <p>Large-format items only. Not for everyday laundry, and not charged by weight.</p>
        <ul class="chk2" style="margin-top:.9rem">
          <li>Blankets, quilt covers, rugs and sheet sets</li>
          <li>Priced per item, machine capacity confirmed before collection</li>
          <li>Longer turnaround — confirmed at booking</li>
        </ul>
        <span class="price" data-px="linen"></span>
        <a href="#/book" class="btn btn-nv btn-full" style="margin-top:1rem">Book Blankets &amp; Rugs <svg class="ic ic-inl ic-aft" aria-hidden="true"><use href="#ic-arrow-right"/></svg></a>
      </div>''',
     "services page: Wash Fold & Iron card removed, Ironing Only replaced")

sub1('<div class="pnote" style="margin-top:2rem"><strong>What affects your final price:</strong> weight, number of separated loads, items selected for ironing, bulky items, and your distance from the nearest active operator. Your operator confirms the final figure after weighing and before any work begins.</div>',
     '<div class="pnote" style="margin-top:2rem"><strong>What affects your final price:</strong> weight, number of separated loads, large linen items, bulky items, and your distance from the nearest active operator. Your operator confirms the final figure after weighing and before any work begins.</div>',
     "services page price-factors note: large linen replaces ironing")

# =====================================================================
# 9. Pricing page: price table, bullet list, lede
# =====================================================================
sub1('<div class="ptab-h"><h3>Ironing &amp; Pressing</h3><span>Per item</span></div>\n        <div id="pxIron"></div>',
     '<div class="ptab-h"><h3>Blankets, Rugs &amp; Sheets</h3><span>Per item</span></div>\n        <div id="pxLinen"></div>',
     "pricing page: Ironing & Pressing table header becomes Blankets, Rugs & Sheets")

sub1('<li style="font-size:var(--fs-micro);color:var(--body);margin-bottom:.5rem"><strong>Ironing.</strong> Charged per item you select, not per load.</li>',
     '<li style="font-size:var(--fs-micro);color:var(--body);margin-bottom:.5rem"><strong>Large linen.</strong> Blankets, rugs and sheet sets only — charged per item, not by weight.</li>',
     "pricing page bullet: large linen replaces ironing")

# =====================================================================
# 10. paintPrices(): price map and price-table rows
# =====================================================================
sub1("""  const map = {
    wf: 'From ' + money(PX.load) + ' per load',
    wfi: money(PX.load) + ' per load + ' + money(PX.iron) + ' per item',
    iron: 'From ' + money(PX.iron) + ' per item',
    dc: 'From ' + money(PX.dcDress) + ' per item',
    bulk: 'From ' + money(PX.bulkDoona) + ' per item',
    p1: money(PX.plan1) + '<small>/week</small>',
    p2: money(PX.plan2) + '<small>/week</small>',
    p3: money(PX.plan3) + '<small>/week</small>'
  };""",
     """  const map = {
    wf: 'From ' + money(PX.load) + ' per load',
    linen: 'From ' + money(PX.linenSheetSet) + ' per item',
    dc: 'From ' + money(PX.dcDress) + ' per item',
    bulk: 'From ' + money(PX.bulkDoona) + ' per item',
    p1: money(PX.plan1) + '<small>/week</small>',
    p2: money(PX.plan2) + '<small>/week</small>',
    p3: money(PX.plan3) + '<small>/week</small>'
  };""",
     "price map: linen replaces wfi/iron")

sub1("""  document.getElementById('pxIron').innerHTML =
    R('Shirt or blouse', 'Pressed and returned on a hanger', money(PX.iron)) +
    R('Trousers or jeans', '', money(PX.ironTrouser)) +
    R('School or work uniform item', '', money(PX.iron)) +
    R('Ironing-only service', 'No load charge applies', 'Per item');""",
     """  document.getElementById('pxLinen').innerHTML =
    R('Sheet set', 'Per set, any bed size', money(PX.linenSheetSet)) +
    R('Blanket or quilt cover', 'Single or double', money(PX.linenBlanket)) +
    R('Rug or floor mat', 'Subject to size', money(PX.linenRug)) +
    R('Large-format items only', 'Not charged by weight', 'Per item');""",
     "price table: sheet set / blanket / rug replace the ironing rows")

# =====================================================================
# 11. Settings — usual-service dropdown, and the ops/dashboard dropdown
# =====================================================================
sub1('<option value="wf">Wash &amp; Fold</option><option value="wfi">Wash, Fold &amp; Iron</option><option value="iron">Ironing only</option><option value="dc">Dry cleaning</option>',
     '<option value="wf">Wash &amp; Fold</option><option value="linen">Blankets, Rugs &amp; Sheets</option><option value="dc">Dry cleaning</option>',
     "settings 'usual service' dropdown (#pfSvc): no ironing")

# =====================================================================
# 12. Booking wizard: remove the dead second stepper field and its
#     handlers (it existed only to count ironed items)
# =====================================================================
sub1('''            <div class="fld" id="bkFldB"><label class="lbl" id="bkLblB">Items to iron</label>
              <div class="stepper"><button type="button" data-bstep="b,-1" aria-label="Decrease ironed items"><svg class="ic" aria-hidden="true"><use href="#ic-minus"/></svg></button><span id="bkNumB">0</span><button type="button" data-bstep="b,1" aria-label="Increase ironed items"><svg class="ic" aria-hidden="true"><use href="#ic-plus"/></svg></button></div>
            </div>
''',
     '',
     "removed the dead 'items to iron' second stepper from the wizard")

sub1('<div class="ap-g2">\n            <div class="fld"><label class="lbl" id="bkLblA">Loads (approx. 5&nbsp;kg each)</label>',
     '<div class="ap-g2" style="grid-template-columns:1fr">\n            <div class="fld"><label class="lbl" id="bkLblA">Loads (approx. 5&nbsp;kg each)</label>',
     "single remaining stepper takes the full row")

sub1("  if(document.getElementById('bkFldB')) document.getElementById('bkFldB').style.display=W.svc==='wfi'?'':'none';\n",
     "",
     "removed the dead bkFldB show/hide (the field no longer exists)")

sub1("  if(document.getElementById('bkNumB')) document.getElementById('bkNumB').textContent=W.b;\n",
     "",
     "removed the dead bkNumB text sync (the field no longer exists)")

sub1("if(document.getElementById('bkLblA')) document.getElementById('bkLblA').textContent=W.svc==='iron'?'Items to iron':W.svc==='dc'?'Garments':'Loads (approx. 5 kg each)';",
     "if(document.getElementById('bkLblA')) document.getElementById('bkLblA').textContent=W.svc==='linen'?'Blankets, rugs or sheet sets':W.svc==='dc'?'Garments':'Loads (approx. 5 kg each)';",
     "wizard quantity label: linen replaces iron")

sub1("  /* volume card: show for wf/wfi/iron, hide for dc/comm */",
     "  /* volume card: show for wf/linen, hide for dc/comm */",
     "comment updated")

sub1("        ironItems: W.svc === 'wfi' ? W.b : (W.svc === 'iron' ? W.a : 0),",
     "        linenItems: W.svc === 'linen' ? W.a : 0,",
     "booking record: linenItems replaces ironItems")

# =====================================================================
# 13. Home quick-estimator calc(): remove wfi/iron branches, add linen
# =====================================================================
sub1("""  } else if (svc === 'wfi'){
    lA.textContent = 'Loads (approx. 5 kg each)'; lB.textContent = 'Items to iron'; showB = true;
    const w = C.a * PX.load, i = C.b * PX.iron;
    sub = w + i;
    lines = row(C.a + ' × wash & fold load' + (C.a>1?'s':''), w);
    if (C.b) lines += row(C.b + ' × item' + (C.b>1?'s':'') + ' ironed', i);
  } else if (svc === 'iron'){
    lA.textContent = 'Items to iron';
    sub = C.a * PX.iron;
    lines = row(C.a + ' × item' + (C.a>1?'s':'') + ' ironed', sub);
  } else if (svc === 'dc'){""",
     """  } else if (svc === 'linen'){
    lA.textContent = 'Blankets, rugs or sheet sets';
    sub = C.a * PX.linenSheetSet;
    lines = row(C.a + ' × blanket, rug or sheet set' + (C.a>1?'s':''), sub);
  } else if (svc === 'dc'){""",
     "home estimator: linen branch replaces wfi/iron branches")

sub1('''            <option value="wf">Wash &amp; Fold</option>
            <option value="wfi">Wash, Fold &amp; Iron</option>
            <option value="iron">Ironing only</option>
            <option value="dc">Dry Cleaning</option>
            <option value="comm">Commercial / Linen (quoted separately)</option>''',
     '''            <option value="wf">Wash &amp; Fold</option>
            <option value="linen">Blankets, Rugs &amp; Sheets</option>
            <option value="dc">Dry Cleaning</option>
            <option value="comm">Commercial / Linen (quoted separately)</option>''',
     "home quick-estimator dropdown (#qSvc): no ironing")

# =====================================================================
# 14. Real wizard estimate(): remove wfi/iron branches, add linen
# =====================================================================
sub1("""  if (svc === 'wfi'  ){ const w=a*PX.load, i=b*PX.iron; subtot+=w+i;
                        lines.push([a+' × wash & fold load'+(a>1?'s':''), w]);
                        if (b) lines.push([b+' × item'+(b>1?'s':'')+' ironed', i]); }
  if (svc === 'iron' ){ const v=a*PX.iron; subtot+=v; lines.push([a+' × item'+(a>1?'s':'')+' ironed', v]); }""",
     "  if (svc === 'linen'){ const v=a*PX.linenSheetSet; subtot+=v; lines.push([a+' × blanket, rug or sheet set'+(a>1?'s':''), v]); }",
     "wizard estimator: linen branch replaces wfi/iron branches")

# =====================================================================
# 15. Ops invoice: the "items ironed" field becomes "large linen items"
# =====================================================================
sub1('<div class="fld"><label class="lbl" for="invIron">Items ironed</label><input class="inp" type="number" min="0" id="invIron" placeholder="0"></div>',
     '<div class="fld"><label class="lbl" for="invLinen">Blankets, rugs or sheet sets</label><input class="inp" type="number" min="0" id="invLinen" placeholder="0"></div>',
     "ops invoice field: large linen replaces ironed items")

sub1("document.getElementById('invIron').value=job.ironItems||0;",
     "document.getElementById('invLinen').value=job.linenItems||0;",
     "ops invoice hydration: linenItems replaces ironItems")

sub1("""  const iron=parseInt(document.getElementById('invIron').value)||0;
  const adj=parseFloat(document.getElementById('invAdj').value)||0;
  const svc=job.svc||'wf';
  if(!kg&&svc!=='iron'){ say('invMsg',false,'Enter the actual weight to calculate.'); return; }
  let lines=[],sub=0;
  if(['wf','wfi'].includes(svc)){""",
     """  const linenCount=parseInt(document.getElementById('invLinen').value)||0;
  const adj=parseFloat(document.getElementById('invAdj').value)||0;
  const svc=job.svc||'wf';
  if(!kg&&svc!=='linen'){ say('invMsg',false,'Enter the actual weight to calculate.'); return; }
  let lines=[],sub=0;
  if(svc==='wf'){""",
     "ops invoice calc: linen replaces the wfi/iron weight-required logic")

sub1("""  if((svc==='wfi'||svc==='iron')&&iron){ const v=iron*PX.iron; sub+=v; lines.push([`${iron} × item${iron>1?'s':''} ironed`,v]); }""",
     """  if(svc==='linen'&&linenCount){ const v=linenCount*PX.linenSheetSet; sub+=v; lines.push([`${linenCount} × blanket, rug or sheet set${linenCount>1?'s':''}`,v]); }""",
     "ops invoice calc: linen line item replaces the ironing line item")

# =====================================================================
# 16. wizStep volume-card display condition (was ['dc','comm'] hide-list —
#     already correct since linen isn't in it; comment only, done above)
# =====================================================================

# =====================================================================
# 17. Meta description, title, JSON-LD, per-route titles
# =====================================================================
sub1('<title>LaundryKings — Laundry Pickup &amp; Delivery | Brisbane, Logan &amp; SEQ</title>',
     '<title>LaundryKings — Laundry Pickup &amp; Delivery | Brisbane, Logan &amp; SEQ</title>',
     "title unchanged (no ironing mentioned in it)", count=1)

sub1('<meta name="description" content="LaundryKings — laundry pickup and delivery across Brisbane, Logan and South East Queensland. Wash &amp; fold, ironing, dry cleaning, commercial linen. We Wash It Well.">',
     '<meta name="description" content="LaundryKings — laundry pickup and delivery across Brisbane, Logan and South East Queensland. Wash &amp; fold, dry cleaning, large linen, commercial laundry. We Wash It Well.">',
     "meta description: no ironing")

sub1('"description":"Laundry pickup and delivery across Brisbane, Logan and South East Queensland. Wash and fold, ironing, dry cleaning and commercial linen, collected from your door and returned. All prices include GST."',
     '"description":"Laundry pickup and delivery across Brisbane, Logan and South East Queensland. Wash and fold, dry cleaning, large linen and commercial laundry, collected from your door and returned. All prices include GST."',
     "JSON-LD LocalBusiness description: no ironing")

sub1("services:'Our services — wash, fold, iron, dry clean',",
     "services:'Our services — wash, fold, dry clean, large linen',",
     "per-route title: no ironing")

open(path, "w", encoding="utf-8").write(src)
print("Content update applied:")
for l in log:
    print("  -", l)
print("\nRemaining 'iron' mentions (should be none, or only in unrelated words):")
import subprocess
r = subprocess.run(["grep", "-ni", "iron", path], capture_output=True, text=True)
print(r.stdout or "  (none)")
