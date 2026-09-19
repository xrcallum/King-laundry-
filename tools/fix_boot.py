#!/usr/bin/env python3
"""Repair the app boot path.

appBoot() calls wireWizard() and wireSettings(). Neither exists anywhere in the
file, so appBoot throws a ReferenceError on its second statement and every line
after it never runs: wireSettings, the version labels, renderHome, renderAccount,
renderForms, renderWizard, renderBookings, renderMessages, appRoute, the
not-signed-in notice, the live config/booking and config/contact listeners, and
the editor preload of operations. The whole customer app and ops layer therefore
never initialises.

The markup this was meant to drive is all present and all dead: the wizard's
[data-bstep] steppers, bkN1/bkN2/bkP2/bkP3/bkGo, the recurring switch, the terms
checkbox, and the settings save buttons pdGo, pfGo, adGo, udGo, cmGo, plus the
profile sheet controls apSw, apSw2, sheetX, sheetNew.

This writes both functions against the existing state objects and helpers, and
fixes one place where button text is set with textContent but contains markup.
"""
import re
import sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read()

# ---------------------------------------------------------------- bkN1 text
# renderWizard sets this with textContent, so any markup would print literally.
# Verb first, arrow after (D6).
OLD_N1 = """document.getElementById('bkN1').textContent=W.svc==='comm'?'<svg class="ic ic-inl ic-aft" aria-hidden="true"><use href="#ic-arrow-right"/></svg> Commercial enquiry':'<svg class="ic ic-inl ic-aft" aria-hidden="true"><use href="#ic-arrow-right"/></svg> Continue';"""
NEW_N1 = """document.getElementById('bkN1').innerHTML=(W.svc==='comm'?'Commercial enquiry':'Continue')+'<svg class="ic ic-inl ic-aft" aria-hidden="true"><use href="#ic-arrow-right"/></svg>';"""
assert OLD_N1 in src, "bkN1 line not found"
src = src.replace(OLD_N1, NEW_N1)

# ------------------------------------------------------------- the two functions
WIRING = r"""
/* ================================================================
   WIRING — the two functions appBoot has always called
   ================================================================ */

function wireWizard(){
  const $ = id => document.getElementById(id);
  if (!$('bkGo')) return;

  /* approximate quantity */
  document.querySelectorAll('[data-bstep]').forEach(btn => {
    btn.onclick = () => {
      const [k, d] = btn.dataset.bstep.split(',');
      W[k] = Math.max(k === 'a' ? 1 : 0, Math.min(40, W[k] + Number(d)));
      renderWizard();
    };
  });

  const di = $('bkDate');
  if (di) di.onchange = () => { W.date = di.value; W.win = ''; renderWizard(); };

  $('bkBack').onclick = () => { if (W.step > 1 && W.step < 4) wizStep(W.step - 1); else location.hash = '#/app'; };
  $('bkP2').onclick   = () => wizStep(1);
  $('bkP3').onclick   = () => wizStep(2);

  $('bkN1').onclick = () => {
    if (W.svc === 'comm'){ location.hash = '#/business'; return; }
    const p = activeP();
    if (!p || !addrLine(p)){ say('bkMsg', false, 'Add a collection address to this profile before booking.'); return; }
    renderWizard(); wizStep(2);
  };

  $('bkN2').onclick = () => {
    if (!W.date){ say('bkMsg', false, 'Choose a collection date to continue.'); return; }
    if (!W.win){  say('bkMsg', false, 'Choose a collection window to continue.'); return; }
    renderWizard(); wizStep(3);
  };

  /* recurring collection */
  const rec = $('bkRec');
  rec.onclick = () => {
    W.rec = !W.rec;
    rec.classList.toggle('on', W.rec);
    rec.setAttribute('aria-pressed', W.rec ? 'true' : 'false');
    $('bkRecOpts').style.display = W.rec ? '' : 'none';
  };
  const rf = $('bkRecFreq'); if (rf) rf.onchange = () => { W.freq = rf.value; };

  /* terms gate the confirm button */
  const tos = $('bkTos'), go = $('bkGo');
  const syncTos = () => { go.disabled = !tos.checked; go.setAttribute('aria-disabled', tos.checked ? 'false' : 'true'); };
  tos.onchange = syncTos; syncTos();

  go.onclick = async () => {
    const p = activeP();
    if (!tos.checked){ say('bkMsg', false, 'Please accept the terms to confirm this booking.'); return; }
    if (!p || !addrLine(p)){ say('bkMsg', false, 'Add a collection address before confirming.'); return; }
    if (!W.win){ say('bkMsg', false, 'Choose a collection window.'); return; }
    go.disabled = true;
    try {
      const win  = BK.windows.find(w => w.id === W.win) || { label:'' };
      const est  = estimate(W.svc, W.a, W.b);
      const care = ($('bkCare').value || '').trim();
      const del  = ($('bkDel').value  || '').trim();
      const b = {
        id: 'b' + uid4(),
        ref: REF(),
        status: 'requested',
        svc: W.svc,
        service: SVCNAME(W.svc),
        date: W.date,
        window: win.label,
        a: W.a, b: W.b,
        ironItems: W.svc === 'wfi' ? W.b : (W.svc === 'iron' ? W.a : 0),
        estimate: est ? est.total : 0,
        care: care,
        delivery: del,
        recurring: W.rec ? W.freq : '',
        profile: p.name,
        contact: p.contact || p.name,
        email: p.email || S.acct.email || '',
        phone: p.phone || S.acct.phone || '',
        address: addrLine(p),
        suburb: p.suburb || '',
        postcode: p.postcode || '',
        createdAt: new Date().toISOString()
      };

      S.bookings.unshift(b);
      await pushDoc('bookings', b);

      /* hand the job to operations */
      if (DB){
        try { const { id, ...rest } = b; await DB.collection('bookings_inbox').doc(id).set(rest); }
        catch(e){ console.error('[LK] bookings_inbox', e); }
      }

      /* optionally keep the notes on the profile */
      if ($('bkCareSave').checked || $('bkDelSave').checked){
        if ($('bkCareSave').checked) p.care = care;
        if ($('bkDelSave').checked)  p.del  = del;
        await saveProfile(p);
      }

      addMessage(b.ref, b.ref + ' received',
        'We have your collection request for ' + longDate(b.date) + ', ' + b.window + '. '
        + 'Your operator is assigned before the day and will message you ahead of arrival. '
        + 'The final price is confirmed after weighing and counting, before any work begins.');

      const tx = $('bkDoneTx');
      if (tx) tx.textContent = 'Reference ' + b.ref + '. We have your request for ' + longDate(b.date)
        + ', ' + b.window + '. You will get a message here once an operator is assigned.';

      renderBookings(); renderMessages(); renderHome(); renderTabs('book');
      say('bkMsg', true, 'Booking ' + b.ref + ' requested.');
      wizStep(4);
    } catch(e){
      console.error('[LK] booking', e);
      say('bkMsg', false, 'Could not confirm that booking. Please try again.');
    } finally {
      go.disabled = false;
    }
  };
}

function wireSettings(){
  const $  = id => document.getElementById(id);
  const v  = id => { const e = $(id); return e ? String(e.value || '').trim() : ''; };
  const on = (id, fn) => { const e = $(id); if (e) e.onclick = fn; };

  /* profile switcher sheet */
  ['apSw','apSw2'].forEach(id => on(id, openSheet));
  on('sheetX', closeSheet);
  on('sheetUser', closeSheet);
  on('sheetHelp', closeSheet);
  const sh = $('sheet');
  if (sh) sh.onclick = e => { if (e.target === sh) closeSheet(); };
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && sh && sh.classList.contains('open')) closeSheet();
  });
  on('sheetNew', async () => {
    const p = { id: 'p' + uid4(), name: 'New profile', type: 'Household', preferred: false, state: 'QLD' };
    S.profiles.push(p);
    S.acct.activeId = p.id;
    await saveProfile(p); await saveAcct();
    closeSheet();
    renderAccount(); renderForms(); renderHome(); renderWizard();
    location.hash = '#/pdetails';
  });

  /* profile and contact details */
  on('pdGo', async () => {
    const p = activeP(); if (!p){ say('pdMsg', false, 'No profile selected.'); return; }
    if (!v('pdName')){ say('pdMsg', false, 'A profile name is required.'); return; }
    Object.assign(p, { name: v('pdName'), contact: v('pdContact'), email: v('pdEmail'),
                       phone: v('pdPhone'), type: v('pdType'), preferred: $('pdPref').checked });
    let ok = await saveProfile(p);
    if (p.preferred){
      for (const o of S.profiles) if (o.id !== p.id && o.preferred){ o.preferred = false; ok = (await saveProfile(o)) && ok; }
    }
    say('pdMsg', ok, ok ? 'Profile saved.' : 'Saved for this session only — sign in to keep it.');
    renderAccount(); renderHome(); renderWizard();
  });

  /* service preferences */
  on('pfGo', async () => {
    const p = activeP(); if (!p){ say('pfMsg', false, 'No profile selected.'); return; }
    Object.assign(p, { care: v('pfCare'), del: v('pfDel'), svc: v('pfSvc'), eco: $('pfEco').checked });
    const ok = await saveProfile(p);
    say('pfMsg', ok, ok ? 'Service preferences saved.' : 'Saved for this session only — sign in to keep them.');
    renderWizard();
  });

  /* pick up address, with a live coverage answer */
  on('adGo', async () => {
    const p = activeP(); if (!p){ say('adMsg', false, 'No profile selected.'); return; }
    if (!v('adLine1') || !v('adSub') || !v('adPc')){
      say('adMsg', false, 'Street address, suburb and postcode are all required.'); return;
    }
    Object.assign(p, { line1: v('adLine1'), suburb: v('adSub'), postcode: v('adPc'),
                       state: v('adState') || 'QLD', access: v('adAccess') });
    const ok = await saveProfile(p);
    const cov = $('adCov'), pc = v('adPc');
    if (cov){
      cov.style.display = '';
      if (LIVE_PC[pc]){
        cov.className = 'ap-note ok';
        cov.innerHTML = '<i class="ic"><svg class="ic" aria-hidden="true"><use href="#ic-check-circle"/></svg></i><span>We collect in ' + esc(LIVE_PC[pc]) + ' (' + esc(pc) + ').</span>';
      } else if (SOON_PC[pc]){
        cov.className = 'ap-note warn';
        cov.innerHTML = '<i class="ic"><svg class="ic" aria-hidden="true"><use href="#ic-clock"/></svg></i><span>' + esc(SOON_PC[pc]) + ' (' + esc(pc) + ') is opening next. Register interest on the coverage page and we will tell you when it is live.</span>';
      } else {
        cov.className = 'ap-note warn';
        cov.innerHTML = '<i class="ic"><svg class="ic" aria-hidden="true"><use href="#ic-pin"/></svg></i><span>We are not collecting in ' + esc(pc) + ' yet. The address is saved — register interest on the <a href="#/coverage" style="text-decoration:underline">coverage page</a>.</span>';
      }
    }
    say('adMsg', ok, ok ? 'Address saved.' : 'Saved for this session only — sign in to keep it.');
    renderAccount(); renderHome(); renderWizard();
  });

  /* account-level user details */
  on('udGo', async () => {
    if (!v('udFirst')){ say('udMsg', false, 'A first name is required.'); return; }
    Object.assign(S.acct, { first: v('udFirst'), last: v('udLast'), email: v('udEmail'), phone: v('udPhone') });
    const ok = await saveAcct();
    say('udMsg', ok, ok ? 'Your details are saved.' : 'Saved for this session only — sign in to keep them.');
    renderAccount();
  });

  /* communication settings */
  on('cmGo', async () => {
    document.querySelectorAll('[data-cm]').forEach(b => { S.acct.comms[b.dataset.cm] = b.classList.contains('on'); });
    const ok = await saveAcct();
    say('cmMsg', ok, ok ? 'Communication settings saved.' : 'Saved for this session only — sign in to keep them.');
  });
}

"""

anchor = "async function appBoot(){"
assert anchor in src
src = src.replace(anchor, WIRING.strip("\n") + "\n\n" + anchor, 1)

# appBoot should not die on one bad statement ever again.
OLD_BOOT = "  await appLoad();\n  wireWizard(); wireSettings();"
NEW_BOOT = ("  await appLoad();\n"
            "  try { wireWizard(); } catch(e){ console.error('[LK] wireWizard', e); }\n"
            "  try { wireSettings(); } catch(e){ console.error('[LK] wireSettings', e); }")
assert OLD_BOOT in src, "appBoot head not found"
src = src.replace(OLD_BOOT, NEW_BOOT)

# The not-signed-in notice assumes an element that only exists on one route.
src = src.replace("    document.getElementById('udSec').textContent='This view is not signed in",
                  "    const udSecEl=document.getElementById('udSec'); if(udSecEl) udSecEl.textContent='This view is not signed in")

open(path, "w", encoding="utf-8").write(src)
print("boot path repaired:", path)
