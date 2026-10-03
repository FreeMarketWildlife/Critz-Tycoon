import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url),{chromium}=require(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'playwright'));
const output=process.env.CRITZ_QA_OUTPUT||'test-results/symmetry-sides';await mkdir(output,{recursive:true});
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE,headless:true});
const context=await browser.newContext({viewport:{width:1366,height:768}}),p=await context.newPage(),errors=[],report=[];
p.on('pageerror',e=>errors.push(e.message));
const settle=()=>p.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
const snap=()=>p.evaluate(async()=>(await import('./editor.js')).getSnapshot());
const viewportPixels=()=>p.locator('#canvas').evaluate(c=>[...c.getContext('2d').getImageData(0,0,c.width,c.height).data]);
async function upload(width){
 const png=await p.evaluate(width=>{const c=document.createElement('canvas');c.width=width;c.height=4;const g=c.getContext('2d');for(let x=0;x<width;x++){g.fillStyle=`rgb(${30+x*30},80,120)`;g.fillRect(x,0,1,4);}return c.toDataURL().split(',')[1];},width);
 await p.locator('#reference-file').setInputFiles({name:'columns.png',mimeType:'image/png',buffer:Buffer.from(png,'base64')});await settle();
 await p.locator('#opacity').fill('100');await settle();
}
async function open(method){await p.locator('#symmetry-open').click();await p.locator('#symmetry-method').selectOption(method);}
async function checkRow(expected){const state=await snap(),{x,y,w}=state.reference.rect;assert.equal(w,expected.length);const row=await p.locator('#canvas').evaluate((c,{x,y,w})=>[...c.getContext('2d').getImageData(x,y,w,1).data],{x,y,w});assert.deepEqual(row,expected.flatMap(x=>[30+x*30,80,120,255]));}
async function test(name,fn){try{await fn();report.push({name,pass:true});console.log('PASS '+name);}catch(e){report.push({name,pass:false,error:e.stack});console.error('FAIL '+name+' '+e.stack);}}
try{
 await p.goto(process.env.CRITZ_EDITOR_URL||'http://localhost:5193/sprite-editor/');await p.waitForFunction(()=>document.documentElement.dataset.editorReady==='true');
 for(const [width,expected]of [[5,{'remove-left':[0,2,3,4],'remove-right':[0,1,2,4],'add-left':[0,1,1,2,3,4],'add-right':[0,1,2,3,3,4]}],[6,{'remove-left':[0,1,3,4,5],'remove-right':[0,1,2,4,5],'add-left':[0,1,2,2,3,4,5],'add-right':[0,1,2,3,3,4,5]}]]){
  await test(`all four treatments immediately replace actual viewport pixels for ${width}px source and restore exact original`,async()=>{
   for(const [method,row]of Object.entries(expected)){
    await upload(width);const before=await viewportPixels(),project=(await snap()).project;
    await open(method);assert.equal(await p.locator('#symmetry-method option').count(),4);assert.equal(await p.locator('#symmetry-apply').textContent(),'Center this image');
    await p.locator('#symmetry-apply').click();await settle();assert.equal(await p.locator('#symmetry-dialog').isVisible(),false);await checkRow(row);assert.notDeepEqual(await viewportPixels(),before);assert.deepEqual((await snap()).project,project);
    await p.locator('#symmetry-restore').click();await settle();assert.deepEqual(await viewportPixels(),before);
   }
  });
 }
 await test('apply reveals hidden zero-opacity behind-layer reference; restore reinstates visibility settings',async()=>{
  await upload(5);await p.locator('#show-reference').uncheck();await p.locator('#opacity').fill('0');await p.locator('#ref-layer').selectOption('behind');await settle();const before=await viewportPixels();
  await open('add-right');await p.locator('#symmetry-apply').click();await settle();assert.equal(await p.locator('#show-reference').isChecked(),true);assert.equal(await p.locator('#ref-layer').inputValue(),'above');assert.equal(await p.locator('#opacity').inputValue(),'30');assert.notDeepEqual(await viewportPixels(),before);
  await p.screenshot({path:path.join(output,'applied-reference.png')});
  await p.locator('#symmetry-restore').click();await settle();assert.equal(await p.locator('#show-reference').isChecked(),false);assert.equal(await p.locator('#ref-layer').inputValue(),'behind');assert.equal(await p.locator('#opacity').inputValue(),'0');assert.deepEqual(await viewportPixels(),before);
 });
 await test('repeated edits operate on replaced image and restore bypasses stale sampled cache',async()=>{
  await upload(5);const before=await viewportPixels();await open('add-left');await p.locator('#symmetry-apply').click();await settle();await open('remove-right');assert.match(await p.locator('#symmetry-before-label').textContent(),/6 × 4/);await p.locator('#symmetry-apply').click();await settle();await checkRow([0,1,1,3,4]);await p.locator('#symmetry-restore').click();await settle();assert.deepEqual(await viewportPixels(),before);
 });
 await test('mobile apply dismisses drawer and shows updated canvas immediately',async()=>{
  await upload(5);await p.setViewportSize({width:390,height:844});await p.locator('#reset-layout').click();await p.locator('#toggle-inspector').click();await open('remove-left');await p.screenshot({path:path.join(output,'mobile-treatment.png')});await p.locator('#symmetry-apply').click();await settle();assert.equal((await snap()).layout.inspector,false);await checkRow([0,2,3,4]);
 });
 await test('large downscaled reference edits the displayed grid once; every corrected column survives apply',async()=>{
  await p.setViewportSize({width:1366,height:768});await p.locator('#reset-layout').click();
  for(const method of ['add-left','add-right','remove-left','remove-right']){
   const png=await p.evaluate(()=>{const c=document.createElement('canvas');c.width=320;c.height=434;const g=c.getContext('2d');for(let x=0;x<320;x++){g.fillStyle=`rgb(${Math.floor(x/20)*16},80,120)`;g.fillRect(x,0,1,434);}return c.toDataURL().split(',')[1];});
   await p.locator('#reference-file').setInputFiles({name:'large.png',mimeType:'image/png',buffer:Buffer.from(png,'base64')});
   await p.waitForFunction(()=>document.querySelector('#crop-w').value==='320');await p.locator('#opacity').fill('100');await settle();
   const original=await viewportPixels(),state=await snap(),{x,y,w,h}=state.reference.rect;assert.equal(w,32);
   const row=await p.locator('#canvas').evaluate((c,{x,y,w})=>[...c.getContext('2d').getImageData(x,y,w,1).data],{x,y,w});
   await open(method);assert.equal(await p.locator('#symmetry-width').inputValue(),'32');assert.equal(await p.locator('#symmetry-height').inputValue(),String(h));
   const adding=method.startsWith('add'),left=method.endsWith('left'),column=left?15:16,insertion=16,newWidth=w+(adding?1:-1),expected=[];
   for(let xx=0;xx<newWidth;xx++){const sx=adding?(xx<insertion?xx:xx===insertion?column:xx-1):(xx<column?xx:xx+1);expected.push(...row.slice(sx*4,sx*4+4));}
   if(method==='add-left')await p.screenshot({path:path.join(output,'large-grid-preview.png')});
   await p.locator('#symmetry-apply').click();await settle();
   const after=await snap(),r=after.reference.rect;assert.equal(r.w,newWidth);assert.equal(r.h,h);assert.equal(after.reference.crop.w,newWidth);
   const visible=Math.min(32-r.x,newWidth),actual=await p.locator('#canvas').evaluate((c,{x,y,w})=>[...c.getContext('2d').getImageData(x,y,w,1).data],{x:r.x,y:r.y,w:visible});
   assert.deepEqual(actual,expected.slice(0,visible*4));assert.notDeepEqual(await viewportPixels(),original);
   assert.match(await p.locator('#ref-correction-status').textContent(),new RegExp(`${newWidth} × ${h}`));
   await p.locator('#symmetry-restore').click();await settle();assert.deepEqual(await viewportPixels(),original);
  }
 });
 await test('explicit source-size edit stays at 1:1 rather than silently shrinking away the treatment',async()=>{
  await open('add-left');await p.locator('#symmetry-source-size').click();assert.equal(await p.locator('#symmetry-width').inputValue(),'320');assert.match(await p.locator('#symmetry-explanation').textContent(),/clipped/);
  await p.locator('#symmetry-apply').click();await settle();assert.equal((await snap()).reference.rect.w,321);assert.equal((await snap()).reference.rect.h,434);await p.locator('#symmetry-restore').click();await settle();
 });
 await test('reference crop previews exact coordinates without changing artwork or reference until Apply',async()=>{
  const before=await viewportPixels(),project=(await snap()).project,original=(await snap()).reference;
  await p.locator('#ref-crop-open').click();await p.locator('#ref-crop-x').fill('80');await p.locator('#ref-crop-y').fill('90');await p.locator('#ref-crop-w').fill('160');await p.locator('#ref-crop-h').fill('240');
  assert.deepEqual((await snap()).reference,original);assert.deepEqual(await viewportPixels(),before);await p.locator('#cancel-reference-crop').click();assert.deepEqual(await viewportPixels(),before);
  await p.locator('#ref-crop-open').click();for(const [id,value]of Object.entries({x:80,y:90,w:160,h:240}))await p.locator('#ref-crop-'+id).fill(String(value));
  await p.screenshot({path:path.join(output,'reference-crop.png')});await p.locator('#apply-reference-crop').click();await settle();assert.deepEqual((await snap()).reference.crop,{x:80,y:90,w:160,h:240});assert.deepEqual((await snap()).project,project);assert.notDeepEqual(await viewportPixels(),before);
  const row=await p.locator('#canvas').evaluate(c=>[...c.getContext('2d').getImageData(0,20,32,1).data]);for(let x=0;x<32;x++)assert.equal(row[x*4],Math.floor((80+x*5)/20)*16);
 });
 await test('reference crop guards invalid rectangles and restores full original image',async()=>{
  await p.locator('#ref-crop-open').click();await p.locator('#ref-crop-w').fill('900');assert.equal(await p.locator('#apply-reference-crop').isDisabled(),true);await p.locator('#ref-crop-reset').click();assert.equal(await p.locator('#apply-reference-crop').isEnabled(),true);await p.locator('#apply-reference-crop').click();await settle();assert.deepEqual((await snap()).reference.crop,{x:0,y:0,w:320,h:434});
 });
 await test('drag crop selects source pixels; symmetry uses the cropped viewport grid',async()=>{
  await p.locator('#ref-crop-open').click();const b=await p.locator('#crop-preview').boundingBox();await p.mouse.move(b.x+b.width*.25+.01,b.y+b.height*.25+.01);await p.mouse.down();await p.mouse.move(b.x+b.width*.75+.01,b.y+b.height*.75+.01,{steps:4});await p.mouse.up();assert.equal(await p.locator('#ref-crop-x').inputValue(),'80');assert.equal(await p.locator('#ref-crop-y').inputValue(),'108');assert.equal(await p.locator('#ref-crop-w').inputValue(),'161');assert.equal(await p.locator('#ref-crop-h').inputValue(),'218');await p.locator('#apply-reference-crop').click();await settle();
  const r=(await snap()).reference.rect;await open('remove-left');assert.equal(await p.locator('#symmetry-width').inputValue(),String(r.w));await p.locator('#symmetry-apply').click();await settle();assert.equal((await snap()).reference.rect.w,r.w-1);await p.locator('#symmetry-restore').click();await settle();assert.deepEqual((await snap()).reference.crop,{x:80,y:108,w:161,h:218});
 });
 await test('reference crop modal fits mobile and apply reveals canvas',async()=>{
  await p.setViewportSize({width:390,height:844});await p.locator('#reset-layout').click();await p.locator('#toggle-inspector').click();await p.locator('#ref-crop-open').click();const b=await p.locator('#reference-crop-dialog').boundingBox();assert.ok(b.width<=390&&b.height<=844);await p.screenshot({path:path.join(output,'reference-crop-mobile.png')});await p.locator('#ref-crop-reset').click();await p.locator('#apply-reference-crop').click();await settle();assert.equal((await snap()).layout.inspector,false);assert.deepEqual((await snap()).reference.crop,{x:0,y:0,w:320,h:434});
 });
 await test('no runtime errors',async()=>assert.deepEqual(errors,[]));
}finally{await writeFile(path.join(output,'symmetry-sides-report.json'),JSON.stringify(report,null,2)+'\n');await browser.close();}
if(report.some(r=>!r.pass))process.exitCode=1;
