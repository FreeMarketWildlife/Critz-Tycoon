import {createRequire} from 'node:module';
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url),{chromium,webkit}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const base=process.env.EDITOR_BASE||'http://127.0.0.1:5173',out=process.env.DUI_QA_OUTPUT||'local-review/dui2';mkdirSync(out,{recursive:true});
const expected=JSON.parse(readFileSync(new URL('../sprite-editor/assets/phil-rough-walk-20261017.json',import.meta.url))),reports=[];
for(const [engine,width,height]of [['chrome',390,844],['webkit',320,740],['chrome',768,1024],['webkit',1024,768],['chrome',1180,820],['chrome',844,390],['chrome',1440,1000]]){
 const compact=width<1400,browser=await(engine==='chrome'?chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE}):webkit.launch({headless:true}));
 const context=await browser.newContext({viewport:{width,height},isMobile:compact,hasTouch:compact,permissions:engine==='chrome'?['clipboard-read','clipboard-write']:[]});const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));page.setDefaultTimeout(12000);
 await page.addInitScript(()=>{localStorage.setItem('critz-tycoon.save.v1','DUI2_SYNTHETIC_GAME');localStorage.setItem('fmw.sprite-editor.dummy-creator.v1.layout',JSON.stringify({tools:true,inspector:true,animation:true}));});
 await page.goto(base+'/sprite-editor/?mode=dummy-creator&labels=phil-walk-draft-20261017');await page.waitForFunction(()=>document.documentElement.dataset.dummyCreatorReady==='true');
 const state=()=>page.evaluate(async()=>(await import('./dummy-creator.js')).getBodyRegionSnapshot());assert.deepEqual((await state()).project,expected);
 const tab=async name=>{await page.getByRole('tab',{name,exact:true}).click();await page.waitForTimeout(80);};
 if(compact){
  assert.equal(await page.locator('body').evaluate(e=>e.classList.contains('compact-dummy')),true);assert.equal(await page.locator('#dm-sheet').isVisible(),false);
  for(const id of ['br-part','dc-frames','br-layers','br-import'])assert.equal(await page.locator('#'+id).isVisible(),false,id+' starts hidden');
  const v=await page.locator('#viewport').boundingBox();assert.ok(v.height>=height*(height<500?.60:.65),JSON.stringify({v,height}));assert.ok(v.width>=width-58);assert.equal(await page.locator('#undo').isVisible(),true);
  await page.screenshot({path:out+'/'+engine+'-'+width+'-canvas.png'});
  await tab('Draw');assert.equal(await page.locator('#br-part').isVisible(),true);assert.equal(await page.locator('#dc-facing + .dm-drawing-tools').count(),1);
  await page.locator('[data-dc-facing="west"]').click();assert.equal((await state()).direction,'west');assert.equal(await page.locator('#dm-sheet').isVisible(),false);
  await tab('Draw');await page.locator('#br-part').selectOption('14');await page.locator('#dm-close').click();
  await page.locator('#fit').click();const c=await page.locator('#canvas').boundingBox();const before=await state();await page.mouse.click(c.x+c.width*16.5/32,c.y+c.height*30.5/64);assert.ok((await state()).undo>before.undo);await page.locator('#undo').click();assert.deepEqual((await state()).labels,before.labels);
  await tab('Frames');await page.locator('#dc-frames button').nth(2).click();assert.equal((await state()).frame,2);const prior=(await state()).project;await page.locator('#dc-duplicate').click();assert.equal((await state()).sharedSlots.length,1);await page.locator('#undo').click();assert.deepEqual((await state()).project,prior);
  await page.locator('#dc-play').click();await page.waitForTimeout(250);assert.equal((await state()).playing,true);await page.locator('#dc-play').click();assert.equal((await state()).playing,false);
  await tab('View');await page.locator('#br-reference-visible').uncheck();assert.equal((await state()).layers.reference.visible,false);await page.locator('#br-reference-visible').check();await page.locator('#dc-reference-panel summary').click();assert.equal(await page.locator('#dc-reference').isVisible(),true);
  await page.locator('#dm-tab-view').focus();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('#dm-tab-file').getAttribute('aria-selected'),'true');assert.equal(await page.locator('#br-import').isVisible(),true);
  const backup=(await state()).project;await page.locator('#br-import').click();await page.locator('#br-text').fill(JSON.stringify(backup));await page.locator('#br-apply').click();assert.deepEqual((await state()).project,backup);
  const downloadEvent=page.waitForEvent('download');await page.locator('#br-download').click();const download=await downloadEvent;assert.deepEqual(JSON.parse(readFileSync(await download.path(),'utf8')),backup);
  await page.locator('#br-copy').click();await page.waitForFunction(()=>!document.querySelector('#br-copy').disabled);
  if(await page.locator('#br-transfer').isVisible()){assert.deepEqual(JSON.parse(await page.locator('#br-text').inputValue()),backup);await page.locator('#br-close-transfer').click();}else{assert.match(await page.locator('#status').textContent(),/^Copied complete/);if(engine==='chrome')assert.deepEqual(JSON.parse(await page.evaluate(()=>navigator.clipboard.readText())),backup);}
  await page.evaluate(()=>Object.defineProperty(navigator.clipboard,'writeText',{configurable:true,value:()=>Promise.reject(new DOMException('Synthetic denied clipboard','NotAllowedError'))}));await page.locator('#br-copy').click();await page.waitForFunction(()=>!document.querySelector('#br-copy').disabled);assert.equal(await page.locator('#br-transfer').isVisible(),true);assert.deepEqual(JSON.parse(await page.locator('#br-text').inputValue()),backup);await page.locator('#br-close-transfer').click();await page.evaluate(()=>delete navigator.clipboard.writeText);
  await page.screenshot({path:out+'/'+engine+'-'+width+'-file.png'});await page.keyboard.press('Escape');assert.equal(await page.locator('#dm-sheet').isVisible(),false);
  await tab('Draw');await page.screenshot({path:out+'/'+engine+'-'+width+'-draw.png'});
  if(width>=700&&height>=500){const vr=await page.locator('#viewport').boundingBox(),cr=await page.locator('#canvas').boundingBox();assert.ok(cr.x>=vr.x&&cr.x+cr.width<=vr.x+vr.width+1,'tablet canvas remains beside panel');}
  // No hidden horizontal page or sheet overflow at any breakpoint.
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.ok(await page.locator('.dm-sheet-scroll').evaluate(e=>e.scrollWidth<=e.clientWidth+1));
  await page.locator('#dm-close').click();
  // Crossing tablet/desktop breakpoints returns every single existing control.
  await page.setViewportSize({width:1600,height:1000});await page.waitForFunction(()=>!document.body.classList.contains('compact-dummy'));assert.equal(await page.locator('#inspector #dc-facing + #br-parts-panel').count(),1);assert.equal(await page.locator('.canvas-panel .dc-timeline').count(),1);assert.equal(await page.locator('#tools-panel #undo').count(),1);
  await page.setViewportSize({width,height});await page.waitForFunction(()=>document.body.classList.contains('compact-dummy'));assert.equal(await page.locator('#dm-sheet').isVisible(),false);assert.equal(await page.locator('#dm-tab-canvas').getAttribute('aria-selected'),'true');assert.deepEqual((await state()).project,backup);
  await page.reload();await page.waitForFunction(()=>document.documentElement.dataset.dummyCreatorReady==='true');assert.equal(await page.locator('#dm-sheet').isVisible(),false);assert.deepEqual((await state()).project,backup);
 }else{assert.equal(await page.locator('.dm-tabs').isVisible(),false);assert.equal(await page.locator('#inspector #dc-facing + #br-parts-panel').count(),1);await page.screenshot({path:out+'/desktop.png'});}
 assert.equal(await page.evaluate(()=>localStorage.getItem('critz-tycoon.save.v1')),'DUI2_SYNTHETIC_GAME');assert.deepEqual(errors,[]);reports.push({engine,width,height,compact,pass:true,initialCanvasHeight:(await page.locator('#viewport').boundingBox()).height,projectAndSavePreserved:true,tabFlows:true,resizeAndReload:true,errors});await browser.close();
}
writeFileSync(out+'/report.json',JSON.stringify({passed:reports.length,cases:reports,physicalPhoneTested:false},null,2));console.log(JSON.stringify(reports));
