import {createRequire} from 'node:module';
import assert from 'node:assert/strict';
import {mkdir,writeFile} from 'node:fs/promises';
import path from 'node:path';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES?path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'playwright'):'playwright');
const url=process.env.CRITZ_EDITOR_URL||'http://localhost:5191/sprite-editor/';
const output=process.env.CRITZ_QA_OUTPUT||'test-results/sprite-free';await mkdir(output,{recursive:true});
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE,headless:true});
const context=await browser.newContext({viewport:{width:1440,height:1050},acceptDownloads:true});
const p=await context.newPage(),errors=[],results=[];p.on('pageerror',e=>errors.push(e.message));
await p.addInitScript(()=>localStorage.setItem('critz-tycoon.save.v1','synthetic-free-reference-sentinel'));
const snap=()=>p.evaluate(async()=> (await import('./editor.js')).getSnapshot());
const settle=()=>p.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
const test=async(name,fn)=>{try{await fn();results.push({name,pass:true});console.log('PASS '+name);}catch(e){results.push({name,pass:false,error:e.stack});console.error('FAIL '+name+' '+e.message);}};
async function fixture(page,w=256,h=512){return Buffer.from(await page.evaluate(([w,h])=>{const c=document.createElement('canvas');c.width=w;c.height=h;const g=c.getContext('2d');for(let x=0;x<w;x++){g.fillStyle=x%2?'#0000ff':'#ff0000';g.fillRect(x,0,1,h);}return c.toDataURL().split(',')[1];},[w,h]),'base64');}
async function dragHandle(handle,dx,dy){const b=p.locator(`[data-handle=${handle}]`);await b.scrollIntoViewIfNeeded();const r=await b.boundingBox(),z=(await snap()).zoom;await p.mouse.move(r.x+r.width/2,r.y+r.height/2);await p.mouse.down();await p.mouse.move(r.x+r.width/2+dx*z,r.y+r.height/2+dy*z,{steps:4});await p.mouse.up();await settle();}
try{
 await p.goto(url);await p.waitForFunction(()=>document.documentElement.dataset.editorReady==='true');
 await p.locator('#canvas').click({position:{x:5,y:5}});const artwork=(await snap()).project;
 await test('large reference auto-fits entire image; scale offers only 1x, 2x and Free',async()=>{
  await p.locator('#reference-file').setInputFiles({name:'large.png',mimeType:'image/png',buffer:await fixture(p)});
  await p.waitForFunction(async()=> (await import('./editor.js')).getSnapshot().reference?.mode==='free');await settle();
  await p.locator('#position-panel summary').click();await p.locator('#crop-panel summary').click();
  const r=(await snap()).reference;assert.deepEqual(r.crop,{x:0,y:0,w:256,h:512});assert.deepEqual(r.rect,{x:0,y:0,w:32,h:64});assert.equal(await p.locator('#ref-layer').inputValue(),'above');
  assert.deepEqual(await p.locator('#ref-scale option').evaluateAll(a=>a.map(o=>o.value)),['1','2','free']);
 });
 await test('average maps all covered pixels to native cells; nearest is selectable and fixed 1x/2x exact',async()=>{
  await p.locator('#opacity').fill('100');await settle();
  assert.deepEqual(await p.locator('#canvas').evaluate(c=>[...c.getContext('2d').getImageData(10,20,1,1).data]),[128,0,128,255]);
  await p.locator('#ref-sampling').selectOption('nearest');await settle();assert.deepEqual(await p.locator('#canvas').evaluate(c=>[...c.getContext('2d').getImageData(10,20,1,1).data]),[255,0,0,255]);
  await p.locator('#ref-scale').selectOption('1');await settle();assert.equal((await snap()).reference.rect.w,256);
  await p.locator('#ref-scale').selectOption('2');await settle();assert.equal((await snap()).reference.rect.w,512);
  await p.locator('#ref-scale').selectOption('free');await p.locator('#ref-sampling').selectOption('average');await settle();assert.equal((await snap()).reference.rect.w,32);
 });
 await test('direct drag moves reference without painting, handles resize and unlocked edges stretch',async()=>{
  await p.locator('#ref-transform').click();await settle();const c=await p.locator('#canvas').boundingBox(),z=(await snap()).zoom;
  await p.mouse.move(c.x+12*z,c.y+20*z);await p.mouse.down();await p.mouse.move(c.x+16*z,c.y+23*z,{steps:3});await p.mouse.up();await settle();
  assert.deepEqual((await snap()).reference.rect,{x:4,y:3,w:32,h:64});assert.deepEqual((await snap()).project,artwork);
  await p.locator('#ref-fit').click();await settle();await dragHandle('se',-8,-16);assert.deepEqual((await snap()).reference.rect,{x:0,y:0,w:24,h:48});
  await p.locator('#ref-lock').uncheck();await dragHandle('e',4,0);assert.deepEqual((await snap()).reference.rect,{x:0,y:0,w:28,h:48});
  await p.locator('#ref-transform').click();await settle();assert.equal((await snap()).reference.editing,false);assert.deepEqual((await snap()).project,artwork);
 });
 await test('crop selection uses original source coordinates and automatically refits',async()=>{
  await p.locator('#crop-x').fill('16');await p.locator('#crop-x').press('Tab');await p.locator('#crop-y').fill('32');await p.locator('#crop-y').press('Tab');
  await p.locator('#crop-w').fill('128');await p.locator('#crop-w').press('Tab');await p.locator('#crop-h').fill('256');await p.locator('#crop-h').press('Tab');await settle();
  assert.deepEqual((await snap()).reference.crop,{x:16,y:32,w:128,h:256});assert.deepEqual((await snap()).reference.rect,{x:0,y:0,w:32,h:64});
  const source=p.locator('#reference-source');await source.scrollIntoViewIfNeeded();const r=await source.boundingBox();
  await p.mouse.move(r.x+r.width*.25,r.y+r.height*.25);await p.mouse.down();await p.mouse.move(r.x+r.width*.5,r.y+r.height*.5,{steps:3});await p.mouse.up();await settle();
  const state=(await snap()).reference;assert.ok(Math.abs(state.crop.x-64)<=1);assert.ok(Math.abs(state.crop.y-128)<=1);assert.ok(state.rect.w<=32&&state.rect.h<=64);assert.deepEqual((await snap()).project,artwork);
 });
 await test('numeric dimensions lock proportions; keyboard resizing and Escape return to drawing',async()=>{
  await p.locator('#crop-x').fill('0');await p.locator('#crop-x').press('Tab');await p.locator('#crop-y').fill('0');await p.locator('#crop-y').press('Tab');await p.locator('#crop-w').fill('256');await p.locator('#crop-w').press('Tab');await p.locator('#crop-h').fill('512');await p.locator('#crop-h').press('Tab');
  await p.locator('#ref-lock').check();await p.locator('#ref-width').fill('20');await p.locator('#ref-width').press('Tab');await settle();assert.equal((await snap()).reference.rect.h,40);
  await p.locator('#ref-transform').click();await settle();await p.locator('[data-handle=e]').focus();await p.keyboard.press('ArrowRight');await settle();assert.equal((await snap()).reference.rect.w,21);assert.equal((await snap()).reference.rect.h,42);
  await p.keyboard.press('Escape');await settle();assert.equal((await snap()).reference.editing,false);
  await p.locator('#canvas').click({position:{x:15,y:15}});assert.equal((await snap()).project.frames[0].pixels.filter(Boolean).length,2);
 });
 await test('reference remains excluded from clipboard/project/export and game save',async()=>{
  const state=(await snap()).project;assert.equal('reference' in state,false);
  const preview=await p.locator('#preview').evaluate(c=>[...c.getContext('2d').getImageData(10,20,1,1).data]);assert.deepEqual(preview,[0,0,0,0]);
  await p.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>window.__copied=text}}));await p.locator('#copy').click();const copy=JSON.parse(await p.evaluate(()=>window.__copied));assert.equal('reference' in copy,false);assert.ok(!copy.palette.includes('#800080'));
  assert.equal(await p.evaluate(()=>localStorage.getItem('critz-tycoon.save.v1')),'synthetic-free-reference-sentinel');
 });
 await test('desktop and mobile controls have no horizontal page overflow',async()=>{
  await p.locator('#ref-fit').click();await p.locator('#ref-transform').click();
  for(const [width,height]of [[1440,1050],[390,844],[320,568]]){await p.setViewportSize({width,height});await p.locator('#reset-layout').click();await p.locator('#fit').click();await settle();assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await p.screenshot({path:path.join(output,`reference-${width}.png`),fullPage:true});}
 });
 await test('touch transform moves without creating artwork',async()=>{
  const c=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true}),q=await c.newPage();await q.goto(url);await q.waitForFunction(()=>document.documentElement.dataset.editorReady==='true');
  await q.locator('#reference-file').setInputFiles({name:'large.png',mimeType:'image/png',buffer:await fixture(q)});await q.waitForFunction(async()=> (await import('./editor.js')).getSnapshot().hasReference);
  await q.locator('#toggle-inspector').tap();await q.locator('#ref-transform').tap();await q.locator('#canvas').scrollIntoViewIfNeeded();const r=await q.locator('#canvas').boundingBox(),cdp=await c.newCDPSession(q);
  await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:r.x+25,y:r.y+60}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:r.x+40,y:r.y+75}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await q.waitForTimeout(60);
  const s=await q.evaluate(async()=> (await import('./editor.js')).getSnapshot());assert.ok(s.reference.rect.x>0);assert.ok(s.reference.rect.y>0);assert.equal(s.project.frames[0].pixels.filter(Boolean).length,0);await c.close();
 });
 await test('Wildlife slots, transparent drawing and legacy project preservation',async()=>{
  const c=await browser.newContext(),q=await c.newPage();await q.goto(url);await q.waitForFunction(()=>document.documentElement.dataset.editorReady==='true');
  assert.equal(await q.locator('#swatches button').count(),32);assert.ok((await q.locator('#swatches button').first().getAttribute('title')).includes('#00000000'));
  const old=await q.evaluate(async()=>{const data=await(await fetch('./palettes.json')).json(),{makeProject}=await import('./model.js');const p=makeProject(data.banks.find(b=>b.id==='hero').colors);p.bank='hero';p.frames[0].pixels[0]=1;return p;});
  await q.locator('#project-file').setInputFiles({name:'legacy.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(old))});
  await q.waitForFunction(async()=> (await import('./editor.js')).getSnapshot().project.palette[1]==='#292532');
  let state=await q.evaluate(async()=> (await import('./editor.js')).getSnapshot());assert.deepEqual(state.project.frames,old.frames);assert.equal(state.project.bank,'wildlife');
  await q.locator('#swatches button').first().click();await q.locator('#canvas').scrollIntoViewIfNeeded();const r=await q.locator('#canvas').boundingBox();await q.mouse.click(r.x+state.zoom/2,r.y+state.zoom/2);
  state=await q.evaluate(async()=> (await import('./editor.js')).getSnapshot());assert.equal(state.project.frames[0].pixels[0],0);
  await c.close();
 });
 await test('zero runtime errors',async()=>assert.deepEqual(errors,[]));
}finally{await writeFile(path.join(output,'reference-browser-report.json'),JSON.stringify(results,null,2)+'\n');await browser.close();}
if(results.some(r=>!r.pass))process.exitCode=1;
