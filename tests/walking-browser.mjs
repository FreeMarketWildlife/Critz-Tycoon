import {createRequire} from 'node:module';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES ? path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'playwright') : 'playwright');
const url=process.env.CRITZ_REVIEW_URL||'http://localhost:5182/art-review/walking.html';
const output=process.env.CRITZ_QA_OUTPUT||'test-results/walking';
await mkdir(output,{recursive:true});
const report={url,startedAt:new Date().toISOString(),checks:[],screenshots:[]};
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE,headless:true});
const contexts=[];
async function context(options={}){
  const c=await browser.newContext({viewport:{width:1280,height:900},acceptDownloads:true,...options});contexts.push(c);
  await c.addInitScript(()=>{
    const realLocal=window.localStorage,realSession=window.sessionStorage,original=Object.fromEntries(['getItem','setItem','removeItem','clear','key'].map(k=>[k,Storage.prototype[k]]));
    const sentinel=JSON.stringify({synthetic:true,task:'M1.C3',progress:37});original.setItem.call(realLocal,'critz-tycoon.save.v1',sentinel);original.setItem.call(realLocal,'critz-tycoon.save.v1.backup',sentinel);window.__storage=[];
    for(const key of Object.keys(original))Storage.prototype[key]=function(...args){window.__storage.push(key);return original[key].apply(this,args)};
    for(const [key,value]of [['localStorage',realLocal],['sessionStorage',realSession]])Object.defineProperty(window,key,{get(){window.__storage.push(key);return value}});
    window.__checkStorage=()=>({operations:window.__storage,unchanged:original.getItem.call(realLocal,'critz-tycoon.save.v1')===sentinel&&original.getItem.call(realLocal,'critz-tycoon.save.v1.backup')===sentinel});
  });return c;
}
async function snapshot(p){return p.evaluate(async()=> (await import('./walking.js')).getWalkReviewSnapshot());}
async function ready(p){await p.waitForFunction(()=>document.documentElement.dataset.reviewReady==='true');}
async function check(name,fn){try{report.checks.push({name,pass:true,details:await fn()});console.log('PASS '+name)}catch(e){report.checks.push({name,pass:false,error:e.stack});console.error('FAIL '+name+': '+e.message)}}
async function shot(p,name){const file=path.join(output,name);await p.screenshot({path:file,fullPage:true});report.screenshots.push(file);}
async function storage(p){const s=await p.evaluate(()=>window.__checkStorage());assert.deepEqual(s.operations,[]);assert.equal(s.unchanged,true);return s;}
try{
 const c=await context(),p=await c.newPage(),errors=[],requests=[];p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>requests.push(r.url()));await p.goto(url);await ready(p);await p.locator('#play').click();
 const manifest=await p.evaluate(async()=> (await fetch('../assets/review/characters-walk-v3/atlas.json')).json());
 await check('twelve characters and 144 poses load with faithful labels',async()=>{assert.equal((await snapshot(p)).characters,12);assert.equal((await snapshot(p)).frames,144);for(const person of manifest.characters){await p.locator(`[data-character="${person.id}"]`).click();assert.equal((await snapshot(p)).selected,person.id);assert.equal(await p.locator('#character-name').textContent(),person.label)}return {characters:12,frames:144};});
 await check('every character, direction and pose renders unique pixels; stepping stays paused',async()=>{
   for(const person of manifest.characters){await p.locator(`[data-character="${person.id}"]`).click();for(const direction of manifest.directions){await p.locator(`[data-direction="${direction}"]`).click();const images=[];for(let i=0;i<4;i++){assert.equal((await snapshot(p)).direction,direction);images.push(await p.locator('#portrait').evaluate(c=>c.toDataURL()));await p.locator('#step').click();}assert.equal(new Set(images).size,3);assert.equal(images[1],images[3]);assert.equal((await snapshot(p)).playing,false);}}return {sequences:48,renderedHolds:192};
 });
 await check('pause, play, all-direction cycle and background controls',async()=>{
   await p.locator('#cycle').check();const before=await snapshot(p);await p.waitForTimeout(150);assert.equal((await snapshot(p)).tick,before.tick);await p.locator('#play').click();{const end=Date.now()+5000;while((await snapshot(p)).tick<100&&Date.now()<end)await p.waitForTimeout(30);assert.ok((await snapshot(p)).tick>=100,'Playback failed to advance');}assert.equal((await snapshot(p)).direction,'west');await p.locator('#play').click();
   const images=[];for(const name of ['dark','paper','green']){await p.locator(`[data-bg="${name}"]`).click();assert.equal((await snapshot(p)).background,name);images.push(await p.locator('#portrait').evaluate(c=>c.toDataURL()));}assert.equal(new Set(images).size,3);await p.locator('[data-bg="dark"]').click();return {autoDirection:true,backgrounds:3};
 });
 for(const size of [{width:320,height:568},{width:390,height:844},{width:844,height:390},{width:1280,height:900}])await check(`integer pixels, readable labels and controls at ${size.width}x${size.height}`,async()=>{
   await p.setViewportSize(size);for(const person of manifest.characters){await p.locator(`[data-character="${person.id}"]`).click();assert.equal(await p.locator('#character-name').textContent(),person.label);}
   const layout=await p.evaluate(()=>({width:document.documentElement.scrollWidth,viewport:innerWidth,canvases:[...document.querySelectorAll('canvas')].map(c=>{const r=c.getBoundingClientRect();return {native:[c.width,c.height],display:[r.width,r.height],smoothing:c.getContext('2d').imageSmoothingEnabled}}),controls:[...document.querySelectorAll('button,a,.cycle-label')].filter(e=>e.getBoundingClientRect().height).map(e=>{const r=e.getBoundingClientRect();return {text:e.textContent,height:r.height,left:r.left,right:r.right}}),labels:[...document.querySelectorAll('.cast-card strong,.cast-card small,#character-name')].map(e=>({text:e.textContent,scroll:e.scrollWidth,client:e.clientWidth}))}));
   assert.ok(layout.width<=layout.viewport);for(const canvas of layout.canvases){assert.ok(Number.isInteger(canvas.display[0]/canvas.native[0]));assert.equal(canvas.display[0]/canvas.native[0],canvas.display[1]/canvas.native[1]);assert.equal(canvas.smoothing,false);}for(const control of layout.controls){assert.ok(control.height>=44,JSON.stringify(control));assert.ok(control.left>=0&&control.right<=size.width+1,JSON.stringify(control));}for(const label of layout.labels)assert.ok(label.scroll<=label.client+1,JSON.stringify(label));
   await p.locator('[data-character="hero.boy"]').click();await p.locator('[data-direction="south"]').click();await p.evaluate(()=>scrollTo(0,0));await shot(p,`walking-${size.width}x${size.height}.png`);return layout;
 });
 await check('keyboard operation, focus and touch selection',async()=>{
   await p.locator('[data-direction="east"]').focus();await p.keyboard.press('Enter');assert.equal((await snapshot(p)).direction,'east');const focus=await p.locator('[data-direction="east"]').evaluate(e=>getComputedStyle(e).outlineWidth);assert.ok(parseFloat(focus)>=2);
   const mobile=await context({viewport:{width:390,height:844},isMobile:true,hasTouch:true}),q=await mobile.newPage();await q.goto(url);await ready(q);await q.locator('#play').tap();await q.locator('[data-character="kaid"]').tap();await q.locator('[data-direction="east"]').tap();await q.locator('#step').tap();assert.equal((await snapshot(q)).selected,'kaid');assert.equal((await snapshot(q)).direction,'east');assert.equal((await snapshot(q)).playing,false);await storage(q);await shot(q,'walking-touch.png');return {keyboard:true,touch:true};
 });
 await check('all twelve GIF and PNG downloads plus full-cast GIF match checked-in files',async()=>{
   const results=[];
   for(const person of manifest.characters){const dc=await context(),q=await dc.newPage();await q.goto(url);await ready(q);await q.locator(`[data-character="${person.id}"]`).click();for(const [selector,relative]of [['#download-character',person.gif],['#download-sheet',person.sheet]]){const wait=q.waitForEvent('download');await q.locator(selector).click();const download=await wait;assert.equal(await download.failure(),null);const destination=path.join(output,path.basename(relative));await download.saveAs(destination);assert.deepEqual(await readFile(destination),await readFile(path.join('assets/review/characters-walk-v3',relative)));results.push(relative);}await storage(q);await dc.close();}
   const wait=p.waitForEvent('download');await p.locator('.primary-link').click();const download=await wait;const destination=path.join(output,'all-characters.gif');await download.saveAs(destination);assert.deepEqual(await readFile(destination),await readFile('assets/review/characters-walk-v3/all-characters.gif'));return {downloads:results.length+1};
 });
 await check('reduced motion starts paused and explicit play remains available',async()=>{const rc=await context({reducedMotion:'reduce'}),q=await rc.newPage();await q.goto(url);await ready(q);const a=await snapshot(q);assert.equal(a.playing,false);await q.waitForTimeout(200);assert.equal((await snapshot(q)).tick,a.tick);await q.locator('#play').click();await q.waitForTimeout(150);assert.ok((await snapshot(q)).tick>a.tick);await storage(q);return {reducedMotion:true};});
 await check('background and focus suspension preserve phase without catch-up',async()=>{
   await p.bringToFront();if(!(await snapshot(p)).playing)await p.locator('#play').click();await p.waitForTimeout(100);await p.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'));});const a=await snapshot(p);await p.waitForTimeout(300);assert.equal((await snapshot(p)).tick,a.tick);await p.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});document.dispatchEvent(new Event('visibilitychange'));});await p.waitForTimeout(100);assert.ok((await snapshot(p)).tick-a.tick<10);await p.evaluate(()=>window.dispatchEvent(new Event('blur')));const b=await snapshot(p);await p.waitForTimeout(100);assert.equal((await snapshot(p)).tick,b.tick);await p.evaluate(()=>window.dispatchEvent(new Event('focus')));await p.locator('#play').click();return {visibility:true,focus:true};
 });
 await check('zero save/storage access, no gameplay imports or runtime errors',async()=>{await storage(p);assert.deepEqual(errors,[]);assert.ok(!requests.some(r=>/\/src\/(main|state|grid-save|world|movement)\.js/.test(r)));return {errors,storageOperations:0};});
 for(const resource of ['atlas.json','atlas.png'])await check(`missing ${resource} gives readable error and disabled controls`,async()=>{const ec=await context(),q=await ec.newPage();await q.route(`**/assets/review/characters-walk-v3/${resource}`,r=>r.abort());await q.goto(url);await q.locator('#error').waitFor({state:'visible'});assert.equal(await q.locator('button:enabled,input:enabled').count(),0);assert.equal((await snapshot(q)).ready,false);await storage(q);return {failureUI:true};});
}catch(e){report.fatal=e.stack;console.error(e)}finally{for(const c of contexts)await c.close();await browser.close();report.finishedAt=new Date().toISOString();report.passed=report.checks.filter(c=>c.pass).length;report.failed=report.checks.filter(c=>!c.pass).length;await writeFile(path.join(output,'browser-report.json'),JSON.stringify(report,null,2)+'\n');}
if(report.failed||report.fatal)process.exitCode=1;
