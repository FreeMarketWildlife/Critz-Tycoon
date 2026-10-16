import {migrateLegacyLabels} from '../sprite-editor/body-regions-model.js';
import {createRequire} from 'node:module';import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';import assert from 'node:assert/strict';
const require=createRequire(import.meta.url),{chromium,webkit}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const seed=JSON.parse(readFileSync(new URL('../sprite-editor/assets/body-regions-seed.json',import.meta.url))),legacy=Array.from({length:2048},(_,i)=>i%14),backup={schema:'critz.body-regions.corrections',version:1,seedId:seed.seedId,width:32,height:64,labelOrder:'row-major-top-left',source:seed.source,registration:seed.registration,parts:seed.parts.slice(0,14).map(({id,name,color})=>({id,name,color})),labels:legacy};
const expectedLegacy=migrateLegacyLabels(legacy);
const base=process.env.EDITOR_BASE||'http://127.0.0.1:8843',out=process.env.PAIRS_QA_OUTPUT||'test-results/paired-labels';mkdirSync(out,{recursive:true});const reports=[];
for(const [name,width]of [['chrome',1400],['chrome',390],['webkit',320]]){
 const browser=await(name==='chrome'?chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE,headless:true}):webkit.launch({headless:true})),context=await browser.newContext({viewport:{width,height:width>1000?1050:844},isMobile:width<1000,hasTouch:width<1000});
 await context.addInitScript(({key,data})=>{if(!localStorage.getItem(key))localStorage.setItem(key,JSON.stringify(data));localStorage.setItem('critz-tycoon.save.v1','PAIRS_SYNTHETIC_SAVE');},{key:'fmw.sprite-editor.body-regions.v1:'+seed.seedId,data:backup});
 // Only initialize once: subsequent reloads must use the editor's actual autosave.
 const p=await context.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));await p.goto(base+'/sprite-editor/?mode=body-regions');await p.waitForFunction(()=>document.documentElement.dataset.bodyRegionsReady==='true');
 await p.locator('#br-import').click();await p.locator('#br-text').fill(JSON.stringify(backup));await p.locator('#br-apply').click();
 const snap=()=>p.evaluate(async()=>(await import('./body-regions.js')).getBodyRegionSnapshot()),labels=async()=>(await snap()).labels;
 assert.deepEqual(await labels(),expectedLegacy);assert.equal(await p.locator('#br-part option').count(),10);assert.equal(await p.locator('#br-parts button').count(),10);assert.deepEqual(await p.locator('#br-parts button').allTextContents(),['Unassigned','Head','Ear','Eye','Torso','Pelvis','Arm','Hand','Leg','Foot / shoe']);
 const point=async(x,y)=>{await p.waitForTimeout(80);const r=await p.locator('#canvas').boundingBox(),z=r.width/32;return{x:r.x+(x+.5)*z,y:r.y+(y+.5)*z};};
 const paint=async(x,y)=>{const a=await point(x,y);if(width<1000)await p.touchscreen.tap(a.x,a.y);else await p.mouse.click(a.x,a.y);};
 const rgbaAt=(x,y)=>p.evaluate(([x,y])=>Array.from(document.querySelector('#canvas').getContext('2d').getImageData(x,y,1,1).data),[x,y]);
 const expected=id=>[...Buffer.from(seed.parts[id].color.slice(1),'hex'),255];
 // Remove only display overlays so the actual label color can be inspected directly.
 if(!await p.locator('#inspector').isVisible())await p.locator('#toggle-inspector').click();await p.locator('#br-reference-visible').uncheck();assert.equal(await p.locator('#br-dummy-visible').count(),0);await p.locator('#br-labels-opacity').evaluate(el=>{el.value='100';el.dispatchEvent(new Event('input',{bubbles:true}));});
 if(width<1000&&await p.locator('#inspector').isVisible())await p.locator('#toggle-inspector').click();
 const beforeEnable=await labels();await p.locator('#mirror').click();assert.deepEqual(await labels(),beforeEnable);
 for(const [i,id]of [6,8,10,12].entries()){
  const y=6+i*3;await p.selectOption('#br-part',String(id));
  for(const x of [2,29]){
   const before=await labels();await paint(x,y);const after=await labels();assert.equal(after[y*32+2],id+1);assert.equal(after[y*32+29],id);assert.deepEqual(await rgbaAt(2,y),expected(id+1));assert.deepEqual(await rgbaAt(29,y),expected(id));
   await p.locator('#undo').click();assert.deepEqual(await labels(),before);await p.locator('#redo').click();assert.deepEqual(await labels(),after);
   await p.locator('#br-erase').click();await paint(x,y);assert.equal((await labels())[y*32+2],0);assert.equal((await labels())[y*32+29],0);await p.locator('#undo').click();assert.deepEqual(await labels(),after);await p.locator('#undo').click();assert.deepEqual(await labels(),before);await p.locator('#br-brush').click();
  }
  await p.locator('#mirror').click();
  for(const x of [2,29]){const before=await labels();await paint(x,y);const after=await labels();assert.equal(after[y*32+x],x<16?id+1:id);assert.equal(after[y*32+31-x],before[y*32+31-x]);await p.locator('#undo').click();assert.deepEqual(await labels(),before);}
  await p.locator('#mirror').click();
 }
 await p.selectOption('#br-part','20');await paint(15,20);let final=await labels();assert.equal(final[20*32+15],21);assert.equal(final[20*32+16],20);
 await p.selectOption('#br-part','6');const a=await point(2,25);await p.mouse.move(a.x,a.y);await p.locator('#canvas').focus();await p.keyboard.press('Enter');final=await labels();assert.equal(final[25*32+2],7);assert.equal(final[25*32+29],6);
 await p.locator('#br-copy').click();const exported=JSON.parse(await p.locator('#br-text').inputValue());assert.deepEqual(exported.directions.south[0].labels,final);assert.deepEqual(exported.parts,seed.parts);assert.deepEqual(exported.registration,seed.registration);assert.equal(exported.version,1);await p.locator('#br-close-transfer').click();
 await p.locator('#br-import').click();await p.locator('#br-text').fill(JSON.stringify(backup));await p.locator('#br-apply').click();assert.deepEqual(await labels(),expectedLegacy);await p.locator('#undo').click();assert.deepEqual(await labels(),final);await p.locator('#redo').click();assert.deepEqual(await labels(),expectedLegacy);await p.locator('#undo').click();assert.deepEqual(await labels(),final);
 // The guarded fixture initializer leaves the real autosave intact on reload.
 await p.evaluate(()=>sessionStorage.setItem('paired-reload-check','ready'));
 const saved=await p.evaluate(key=>JSON.parse(localStorage.getItem(key)),(await snap()).draftKey);assert.deepEqual(saved.directions.south[0].labels,final);assert.equal(await p.evaluate(key=>localStorage.getItem(key),'fmw.sprite-editor.body-regions.v1:'+seed.seedId),JSON.stringify(backup));
 // Runtime source still rejects non-front seed registration, rather than guessing side/back limbs.
 const rejection=await p.evaluate(async()=>{const {validateSeed}=await import('./body-regions-model.js');const s=await(await fetch('./assets/body-regions-seed.json')).json();return ['back','west','east'].every(facing=>{try{validateSeed({...s,registration:{...s.registration,facing}});return false;}catch{return true;}});});assert.equal(rejection,true);
 assert.equal(await p.evaluate(()=>localStorage.getItem('critz-tycoon.save.v1')),'PAIRS_SYNTHETIC_SAVE');assert.deepEqual(errors,[]);assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
 await p.reload();await p.waitForFunction(()=>document.documentElement.dataset.bodyRegionsReady==='true');assert.deepEqual(await labels(),final);assert.equal(await p.locator('#mirror').getAttribute('aria-pressed'),'false');await p.selectOption('#br-part','6');
 await p.screenshot({path:out+'/'+name+'-'+width+'.png'});reports.push({engine:name,width,pass:true,options:10,stableExportParts:28,pairedIdsAndActualColorsVerified:true,legacyImportAutosaveUnchanged:true,legacySeedFrontRegistration:true,errors});await browser.close();
}
writeFileSync(out+'/report.json',JSON.stringify({passed:reports.length,cases:reports,physicalPhoneTested:false},null,2));console.log(JSON.stringify(reports));
