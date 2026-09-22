/**
 * Linen Legends (Framer) page smoke test: no JS errors, no missing local files,
 * no horizontal scroll at 390px and 1280px. Used by the auto-ship check.
 * Usage: NODE_PATH=/opt/node22/lib/node_modules node verify/framer-smoke.js site/linen-legends-framer.html
 */
const path=require('path');const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();let bad=0;
for(const w of [390,1280]){const p=await b.newPage({viewport:{width:w,height:844}});const errs=[];
p.on('pageerror',e=>errs.push(e.message));p.on('requestfailed',r=>{if(r.url().startsWith('file:'))errs.push('404 '+r.url())});
await p.goto('file://'+path.resolve(process.argv[2]),{waitUntil:'load'});await p.waitForTimeout(800);
const ox=await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
console.log(w,'errors',errs.length,errs.slice(0,3),'h-overflow',ox);if(errs.length||ox>1)bad++;}
await b.close();console.log('RESULT:',bad?'FAIL':'PASS');process.exit(bad?1:0)})();
