import {createRequire} from 'node:module';import assert from 'node:assert/strict';import {mkdir,writeFile} from 'node:fs/promises';import path from 'node:path';
const require=createRequire(import.meta.url),{chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES?path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'playwright'):'playwright');
const url=process.env.CRITZ_EDITOR_URL||'http://localhost:5193/sprite-editor/',output=process.env.CRITZ_QA_OUTPUT||'test-results/sprite-workspace';await mkdir(output,{recursive:true});
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE,headless:true}),context=await browser.newContext({viewport:{width:1366,height:768}}),p=await context.newPage(),errors=[],report=[];
p.on('pageerror',e=>errors.push(e.message));await p.addInitScript(()=>{localStorage.setItem('critz-tycoon.save.v1','workspace-synthetic-sentinel');});
const snap=()=>p.evaluate(async()=> (await import('./editor.js')).getSnapshot());const settle=()=>p.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
async function test(name,fn){try{await fn();report.push({name,pass:true});console.log('PASS '+name);}catch(e){report.push({name,pass:false,error:e.stack});console.error('FAIL '+name+' '+e.message);}}
async function drag(id,dx,dy){const r=await p.locator('#'+id).boundingBox();await p.mouse.move(r.x+r.width/2,r.y+r.height/2);await p.mouse.down();await p.mouse.move(r.x+r.width/2+dx,r.y+r.height/2+dy,{steps:5});await p.mouse.up();await settle();}
async function fixture(width=31,height=42){return Buffer.from(await p.evaluate(([width,height])=>{const c=document.createElement('canvas');c.width=width;c.height=height;const g=c.getContext('2d');for(let x=0;x<width;x++){g.fillStyle=`rgb(${20+Math.min(x,width-1-x)*12},80,120)`;g.fillRect(x,2,1,height-4);}return c.toDataURL().split(',')[1];},[width,height]),'base64');}
async function upload(w=31,h=42){await p.locator('#reference-file').setInputFiles({name:'odd.png',mimeType:'image/png',buffer:await fixture(w,h)});await p.waitForFunction(async()=> (await import('./editor.js')).getSnapshot().hasReference);await settle();}
async function openSym(){await p.locator('#symmetry-open').click();await p.locator('#symmetry-dialog').waitFor({state:'visible'});}
try{
 await p.goto(url);await p.waitForFunction(()=>document.documentElement.dataset.editorReady==='true');
 await test('normal desktop viewports fit without page scrolling and prioritize the drawing area',async()=>{
  for(const [width,height]of [[1366,768],[1280,720],[1440,900],[1920,1080]]){await p.setViewportSize({width,height});await p.locator('#reset-layout').click();await settle();const layout=await p.evaluate(()=>{const r=document.querySelector('#viewport').getBoundingClientRect();return{w:r.width,h:r.height,pageW:document.documentElement.scrollWidth,pageH:document.documentElement.scrollHeight,width:innerWidth,height:innerHeight,animation:document.querySelector('#animation-content').hidden};});assert.ok(layout.pageW<=width);assert.ok(layout.pageH<=height);assert.ok(layout.w>=width*.66,JSON.stringify(layout));assert.ok(layout.h>=height*.6,JSON.stringify(layout));assert.equal(layout.animation,true);await p.screenshot({path:path.join(output,`workspace-${width}.png`)});}
 });
 await p.setViewportSize({width:1366,height:768});await p.locator('#reset-layout').click();await settle();
 await test('draggable panel borders, keyboard resizing, animation collapse and focus restore space',async()=>{
  const before=await p.locator('#viewport').boundingBox();await drag('inspector-resize',-100,0);assert.ok((await snap()).layout.inspectorWidth>370);assert.ok((await p.locator('#viewport').boundingBox()).width<before.width-80);
  await drag('tools-resize',70,0);assert.ok((await snap()).layout.toolsWidth>=120);await p.locator('#tools-resize').focus();await p.keyboard.press('ArrowLeft');assert.ok((await snap()).layout.toolsWidth<=128);
  await p.locator('#toggle-animation').click();await settle();const short=(await p.locator('#viewport').boundingBox()).height;await drag('animation-resize',0,-55);assert.ok((await p.locator('#viewport').boundingBox()).height<short-35);await p.locator('#collapse-animation').click();await settle();assert.ok((await p.locator('#viewport').boundingBox()).height>short+100);
  const previous=(await snap()).layout;await p.locator('#focus-mode').click();await settle();assert.ok((await p.locator('#viewport').boundingBox()).width>1280);await p.locator('#focus-mode').click();await settle();assert.deepEqual((await snap()).layout,previous);
 });
 await test('layout persists independently of artwork and game save and can reset',async()=>{
  await p.waitForTimeout(180);const before=(await snap()).layout;await p.reload();await p.waitForFunction(()=>document.documentElement.dataset.editorReady==='true');assert.deepEqual((await snap()).layout,before);assert.equal(await p.evaluate(()=>localStorage.getItem('critz-tycoon.save.v1')),'workspace-synthetic-sentinel');await p.locator('#reset-layout').click();assert.equal((await snap()).layout.toolsWidth,58);assert.equal((await snap()).layout.inspectorWidth,290);
 });
 await test('reference controls scroll inside their dock while canvas stays visible',async()=>{
  await upload();await p.locator('#crop-panel summary').click();await p.locator('#position-panel summary').click();const before=await p.locator('#viewport').boundingBox();await p.locator('#remove-reference').scrollIntoViewIfNeeded();const after=await p.locator('#viewport').boundingBox();assert.deepEqual(after,before);assert.ok(await p.locator('.inspector-scroll').evaluate(e=>e.scrollTop>0));assert.equal(await p.evaluate(()=>scrollY),0);await p.locator('#symmetry-open').scrollIntoViewIfNeeded();
 });
 await test('31→32 duplicates left neighbor exactly, centers overlay and leaves artwork/export unchanged',async()=>{
  const before=(await snap()).project;await openSym();assert.match(await p.locator('#symmetry-before-label').textContent(),/31 × 42/);assert.match(await p.locator('#symmetry-after-label').textContent(),/32 × 42/);await p.screenshot({path:path.join(output,'symmetry-31-to-32.png')});
  await p.locator('#symmetry-apply').click();await settle();const state=await snap();assert.equal(state.reference.crop.w,32);assert.equal(state.reference.rect.x+state.reference.rect.w/2,16);assert.equal(state.reference.corrected,true);assert.deepEqual(state.project,before);
  const opacity=p.locator('#opacity');await opacity.fill('100');await settle();const row=await p.locator('#canvas').evaluate(c=>[...c.getContext('2d').getImageData(0,32,32,1).data]);for(let x=0;x<32;x++){const sx=x<15?x:x===15?14:x-1;assert.deepEqual(row.slice(x*4,x*4+4),[20+Math.min(sx,30-sx)*12,80,120,255]);}
  assert.equal(await p.locator('#preview').evaluate(c=>[...c.getContext('2d').getImageData(0,0,c.width,c.height).data].some(v=>v)),false);
  await p.locator('#symmetry-restore').click();await settle();assert.equal((await snap()).reference.crop.w,31);assert.equal((await snap()).reference.corrected,false);assert.deepEqual((await snap()).project,before);
 });
 await test('33→32 removal, cancel, even-width treatment and one-column guard are explicit',async()=>{
  await upload(33,42);await openSym();await p.locator('#symmetry-source-size').click();await p.locator('#symmetry-method').selectOption('remove-right');assert.match(await p.locator('#symmetry-after-label').textContent(),/32 × 42/);await p.locator('#symmetry-apply').click();await settle();assert.equal((await snap()).reference.crop.w,32);
  await openSym();assert.match(await p.locator('#symmetry-explanation').textContent(),/32 → 33/);await p.locator('#symmetry-cancel').click();assert.equal((await snap()).reference.crop.w,32);
  await p.locator('#symmetry-restore').click();await upload(1,8);await openSym();await p.locator('#symmetry-method').selectOption('remove-right');assert.equal(await p.locator('#symmetry-apply').isDisabled(),true);assert.match(await p.locator('#symmetry-explanation').textContent(),/only column/);await p.locator('#symmetry-cancel').click();
 });
 await test('large screenshot can select a native grid and malformed dimensions cannot apply',async()=>{
  await upload(620,840);await openSym();await p.locator('#symmetry-width').fill('31');await p.locator('#symmetry-height').fill('42');await p.waitForTimeout(160);assert.match(await p.locator('#symmetry-after-label').textContent(),/32 × 42/);await p.locator('#symmetry-width').fill('0');await p.waitForTimeout(160);assert.equal(await p.locator('#symmetry-apply').isDisabled(),true);await p.locator('#symmetry-width').fill('31');await p.waitForTimeout(160);await p.locator('#symmetry-apply').click();await settle();assert.equal((await snap()).reference.crop.w,32);
 });
 await test('collapsed animation can reopen and remains fully functional',async()=>{
  await p.locator('#toggle-animation').click();await p.locator('#duplicate').click();await p.locator('#play').click();assert.equal((await snap()).playing,true);await p.locator('#collapse-animation').click();assert.equal((await snap()).playing,false);await p.locator('#toggle-animation').click();assert.equal((await snap()).project.frames.length,2);await p.locator('#collapse-animation').click();
 });
 await test('mobile drawer, reset and symmetry modal fit narrow screens',async()=>{
  for(const [width,height]of [[390,844],[320,568],[844,390]]){await p.setViewportSize({width,height});await p.locator('#reset-layout').click();await settle();assert.equal((await snap()).layout.inspector,false);assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth&&document.documentElement.scrollHeight<=innerHeight));await p.locator('#toggle-inspector').click();await openSym();const r=await p.locator('#symmetry-dialog').boundingBox();assert.ok(r.width<=width&&r.height<=height);await p.screenshot({path:path.join(output,`symmetry-mobile-${width}.png`)});await p.locator('#symmetry-close').click();await p.locator('#close-inspector').click();assert.ok((await p.locator('#viewport').boundingBox()).width>width*.7);}
 });
 await test('no runtime errors',async()=>assert.deepEqual(errors,[]));
}finally{await writeFile(path.join(output,'workspace-browser-report.json'),JSON.stringify(report,null,2)+'\n');await browser.close();}
if(report.some(r=>!r.pass))process.exitCode=1;
