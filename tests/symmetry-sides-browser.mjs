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
 await test('no runtime errors',async()=>assert.deepEqual(errors,[]));
}finally{await writeFile(path.join(output,'symmetry-sides-report.json'),JSON.stringify(report,null,2)+'\n');await browser.close();}
if(report.some(r=>!r.pass))process.exitCode=1;
