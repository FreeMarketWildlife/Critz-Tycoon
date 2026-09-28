import {createRequire} from 'node:module';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import path from 'node:path';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES ? path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'playwright') : 'playwright');
const base=process.env.CRITZ_REVIEW_URL||'http://localhost:5181/art-review/characters.html';
const output=process.env.CRITZ_QA_OUTPUT||'test-results/characters';
const count=Number(process.env.CRITZ_EXPECTED_COUNT||12);
const report={url:base,expectedCount:count,startedAt:new Date().toISOString(),checks:[],screenshots:[]};
await mkdir(output,{recursive:true});
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE,headless:true});
const contexts=[];const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const hash=b=>createHash('sha256').update(b).digest('hex');
async function check(name,fn){try{const details=await fn();report.checks.push({name,status:'pass',details});console.log('PASS '+name)}catch(e){report.checks.push({name,status:'fail',error:e.stack});console.error('FAIL '+name+': '+e.message)}}
async function context(options={}){
 const c=await browser.newContext({viewport:{width:1280,height:900},acceptDownloads:true,...options});contexts.push(c);
 await c.addInitScript(()=>{
  const local=window.localStorage,session=window.sessionStorage;
  const key='critz-tycoon.save.v1',sentinel=JSON.stringify({syntheticQA:true,marker:'M1.C2 fake progress, never actual user data'});
  const originals=Object.fromEntries(['getItem','setItem','removeItem','clear','key'].map(k=>[k,Storage.prototype[k]]));
  originals.setItem.call(local,key,sentinel);originals.setItem.call(local,key+'.backup',sentinel);originals.setItem.call(session,'qa-sentinel',sentinel);
  window.__qaStorageOperations=[];window.__qaAnimationFrames=0;
  for(const method of Object.keys(originals))Storage.prototype[method]=function(...args){window.__qaStorageOperations.push({method,args});return originals[method].apply(this,args)};
  for(const [name,obj] of [['localStorage',local],['sessionStorage',session]])Object.defineProperty(window,name,{configurable:true,get(){window.__qaStorageOperations.push({property:name});return obj}});
  window.__qaCheckSyntheticStorage=()=>({operations:window.__qaStorageOperations.slice(),untouched:originals.getItem.call(local,key)===sentinel&&originals.getItem.call(local,key+'.backup')===sentinel&&originals.getItem.call(session,'qa-sentinel')===sentinel});
  const raf=window.requestAnimationFrame;window.requestAnimationFrame=function(...args){window.__qaAnimationFrames++;return raf.apply(this,args)};
 });return c;
}
async function snapshot(p){return p.evaluate(async()=> (await import('./characters.js')).getCharacterReviewSnapshot())}
async function ready(p){const end=Date.now()+6000;let s;while(Date.now()<end){s=await snapshot(p);if(s.ready)return s;await sleep(30)}throw Error('Artwork not ready: '+JSON.stringify(s))}
async function shot(p,name,locator){const f=path.join(output,name);if(locator)await p.locator(locator).screenshot({path:f});else await p.screenshot({path:f,fullPage:true});report.screenshots.push(f);return f}
async function storage(p){const s=await p.evaluate(()=>window.__qaCheckSyntheticStorage());assert.deepEqual(s.operations,[]);assert.equal(s.untouched,true);return{reads:0,writes:0,syntheticKeys:3}}
let pageErrors=[],requests=[];
try{
 const ctx=await context();const p=await ctx.newPage();p.on('pageerror',e=>pageErrors.push(e.message));p.on('request',r=>requests.push({method:r.method(),url:r.url()}));
 await p.goto(base,{waitUntil:'networkidle'});await ready(p);
 const assets=await p.evaluate(async()=> (await fetch('../assets/review/characters-v2/atlas.json')).json());
 await check('all expected still designs load and every card selects correct details',async()=>{
  assert.equal(assets.assets.length,count);assert.equal(await p.locator('[data-character]').count(),count);
  const details=[];
  for(const a of assets.assets){await p.locator('[data-character]').filter({has:p.locator('strong',{hasText:a.label})}).first().click();const s=await snapshot(p);assert.equal(s.selected,a.character);assert.equal(s.animation,false);assert.equal(await p.locator('#character-name').textContent(),a.label);const actual=await p.locator('#character-design').textContent();assert.ok(actual.trim().length>10,'Missing signature/design for '+a.label);assert.ok((await p.locator('#character-kind').textContent()).trim());const selected=await p.locator('[data-character][aria-pressed="true"]').count();assert.equal(selected,1);details.push({character:a.character,label:a.label,signature:actual,bodyType:await p.locator('#character-kind').textContent()})}
  return details;
 });
 await check('portrait backgrounds switch and preserve still asset selection',async()=>{
  const selected=(await snapshot(p)).selected;const pixels=[];
  for(const bg of ['dark','paper','green']){await p.locator(`[data-bg="${bg}"]`).click();const s=await snapshot(p);assert.equal(s.background,bg);assert.equal(s.selected,selected);assert.equal(await p.locator(`[data-bg="${bg}"]`).getAttribute('aria-pressed'),'true');pixels.push(await p.locator('#portrait').evaluate(c=>c.toDataURL()))}
  assert.equal(new Set(pixels).size,3);await p.locator('[data-bg="dark"]').click();return{backgrounds:3};
 });
 await check('pixel guides alter only inspection portrait and toggle reversibly',async()=>{
  await p.locator('#guides').uncheck();const a=await p.locator('canvas').evaluateAll(cs=>cs.map(c=>c.toDataURL()));await p.locator('#guides').check();assert.equal((await snapshot(p)).guides,true);const b=await p.locator('canvas').evaluateAll(cs=>cs.map(c=>c.toDataURL()));assert.notEqual(a[0],b[0]);assert.deepEqual(a.slice(1),b.slice(1));await shot(p,'guides-desktop.png','.studio');await p.locator('#guides').uncheck();assert.deepEqual(await p.locator('canvas').evaluateAll(cs=>cs.map(c=>c.toDataURL())),a);
 });
 await check('native PNG downloads match checked-in bytes for every design',async()=>{
  const downloads=[];
  for(const a of assets.assets){const dc=await context();const dp=await dc.newPage();await dp.goto(base,{waitUntil:'networkidle'});await ready(dp);await dp.locator(`[data-character="${a.character}"]`).click();const promise=dp.waitForEvent('download');await dp.locator('#download-character').click();const d=await promise;assert.equal(await d.failure(),null);const filename=path.join(output,'download-'+a.character.replaceAll(/[^a-z0-9.-]/gi,'_')+'.png');await d.saveAs(filename);const bytes=await readFile(filename);const source=await readFile(path.join(process.cwd(),'assets/review/characters-v2',a.png));assert.deepEqual(bytes,source);assert.equal(bytes.readUInt32BE(16),24);assert.equal(bytes.readUInt32BE(20),32);downloads.push({character:a.character,bytes:bytes.length,sha256:hash(bytes),suggestedFilename:d.suggestedFilename()});await storage(dp);await dc.close()}return downloads;
 });
 await check('keyboard activation, focus indication and sequential tab reachability',async()=>{
  await p.locator('[data-bg="paper"]').focus();await p.keyboard.press('Enter');assert.equal((await snapshot(p)).background,'paper');await p.locator('#guides').focus();await p.keyboard.press('Space');assert.equal((await snapshot(p)).guides,true);await p.keyboard.press('Space');assert.equal((await snapshot(p)).guides,false);
  const last=assets.assets.at(-1);await p.locator(`[data-character="${last.character}"]`).focus();await p.keyboard.press('Enter');assert.equal((await snapshot(p)).selected,last.character);
  const outline=await p.locator(`[data-character="${last.character}"]`).evaluate(e=>({style:getComputedStyle(e).outlineStyle,width:getComputedStyle(e).outlineWidth}));assert.notEqual(outline.style,'none');assert.ok(parseFloat(outline.width)>=2);
  await p.locator('.brand').focus();const reached=[];for(let i=0;i<count+15;i++){const a=await p.evaluate(()=>{const e=document.activeElement;return{tag:e.tagName,id:e.id,character:e.dataset.character,bg:e.dataset.bg,text:e.textContent?.trim().slice(0,55)}});reached.push(a);await p.keyboard.press('Tab')};assert.equal(new Set(reached.filter(x=>x.character).map(x=>x.character)).size,count);assert.ok(reached.some(x=>x.id==='guides'));assert.ok(reached.some(x=>x.bg==='dark'));assert.ok(reached.some(x=>x.bg==='paper'));assert.ok(reached.some(x=>x.bg==='green'));await p.locator('[data-bg="dark"]').click();return{outline,reached};
 });
 await check('selected card and hover text retain accessible contrast',async()=>{
  const selected=p.locator('[data-character][aria-pressed="true"]');await selected.hover();const data=await selected.evaluate(e=>{const rgb=x=>x.match(/[\d.]+/g).slice(0,3).map(Number);const lum=c=>c.map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4}).reduce((n,v,i)=>n+v*[.2126,.7152,.0722][i],0);const bg=rgb(getComputedStyle(e).backgroundColor);return [...e.querySelectorAll('strong,small')].map(t=>{const s=getComputedStyle(t),color=rgb(s.color),opacity=Number(s.opacity),blended=color.map((v,i)=>v*opacity+bg[i]*(1-opacity));const a=lum(bg),b=lum(blended);return{tag:t.tagName,color:s.color,background:getComputedStyle(e).backgroundColor,opacity,contrast:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)}})});for(const x of data)assert.ok(x.contrast>=4.5,JSON.stringify(x));return data;
 });
 for(const viewport of [{width:320,height:568},{width:390,height:844},{width:844,height:390},{width:1280,height:900}])await check(`responsive layout, labels and integer pixels ${viewport.width}x${viewport.height}`,async()=>{
  await p.setViewportSize(viewport);
  const selectedDesigns=[];
  for(const a of assets.assets){
   await p.locator(`[data-character="${a.character}"]`).click();
   const details=await p.evaluate(()=>({name:document.querySelector('#character-name').textContent,pageWidth:document.documentElement.scrollWidth,viewport:innerWidth,labels:[...document.querySelectorAll('#character-name,#character-design,#character-kind,.measurements dd')].map(e=>{const a=e.getBoundingClientRect(),b=e.parentElement.getBoundingClientRect();return{text:e.textContent,scroll:e.scrollWidth,client:e.clientWidth,left:a.left,right:a.right,parentLeft:b.left,parentRight:b.right}})}));
   assert.ok(details.pageWidth<=details.viewport,'Overflow for '+details.name);
   for(const label of details.labels)assert.ok(label.scroll<=label.client+1&&label.left>=label.parentLeft-1&&label.right<=label.parentRight+1,`Detail clipped for ${details.name}: ${JSON.stringify(label)}`);
   selectedDesigns.push({character:a.character,label:a.label});
  }
  await p.locator('[data-character]').first().click();await p.evaluate(()=>scrollTo(0,0));await sleep(80);
  const layout=await p.evaluate(()=>({pageWidth:document.documentElement.scrollWidth,viewport:innerWidth,canvases:[...document.querySelectorAll('canvas')].map(c=>{const b=c.getBoundingClientRect(),s=getComputedStyle(c);return{id:c.id,native:[c.width,c.height],display:[b.width,b.height],rendering:s.imageRendering,smoothing:c.getContext('2d').imageSmoothingEnabled}}),controls:[...document.querySelectorAll('button,a,input')].map(e=>{const b=e.getBoundingClientRect();return{label:e.getAttribute('aria-label')||e.textContent?.trim(),left:b.left,right:b.right,width:b.width,height:b.height,tag:e.tagName}}),labels:[...document.querySelectorAll('.cast-card strong,.cast-card small,.character-detail h2,#character-design,#character-kind,.measurements dd')].map(e=>{const a=e.getBoundingClientRect(),b=e.parentElement.getBoundingClientRect();return{text:e.textContent,scroll:e.scrollWidth,client:e.clientWidth,left:a.left,right:a.right,parentLeft:b.left,parentRight:b.right}})}));
  assert.ok(layout.pageWidth<=layout.viewport,JSON.stringify(layout));
  for(const c of layout.canvases){const sx=c.display[0]/c.native[0],sy=c.display[1]/c.native[1];assert.equal(sx,sy);assert.ok(Number.isInteger(sx)&&sx>=1);assert.ok(['crisp-edges','pixelated'].includes(c.rendering));assert.equal(c.smoothing,false);if(c.id==='portrait')assert.equal(sx,8);else if(c.id!=='room')assert.equal(sx,4)}
  for(const c of layout.controls)assert.ok(c.left>=-1&&c.right<=viewport.width+1,`Clipped control${JSON.stringify(c)}`);
  for(const l of layout.labels)assert.ok(l.scroll<=l.client+1&&l.left>=l.parentLeft-1&&l.right<=l.parentRight+1,`Clipped label${JSON.stringify(l)}`);
  await shot(p,`characters-${viewport.width}x${viewport.height}.png`);await shot(p,`studio-${viewport.width}x${viewport.height}.png`,'.studio');await shot(p,`cast-${viewport.width}x${viewport.height}.png`,'.cast-section');return{...layout,selectedDesigns};
 });
 await check('still canvases stay fixed without animation frames or CSS animation',async()=>{
  const a=await snapshot(p);const images=await p.locator('canvas').evaluateAll(cs=>cs.map(c=>c.toDataURL()));await sleep(450);assert.deepEqual(await snapshot(p),a);assert.deepEqual(await p.locator('canvas').evaluateAll(cs=>cs.map(c=>c.toDataURL())),images);const actual=await p.evaluate(()=>({raf:window.__qaAnimationFrames,animations:document.getAnimations().length}));assert.equal(actual.raf,0);assert.equal(actual.animations,0);return actual;
 });
 await check('zero storage reads/writes, no gameplay imports and no runtime errors',async()=>{const data=await storage(p);assert.deepEqual(pageErrors,[]);assert.ok(requests.every(r=>['GET','HEAD'].includes(r.method)));assert.ok(!requests.some(r=>/\/src\/(main|state|grid-save)\.js/.test(r.url)));return{...data,pageErrors,requestCount:requests.length};});
 await check('touch review controls on isolated phone context',async()=>{
  const c=await context({viewport:{width:390,height:844},hasTouch:true,isMobile:true});const q=await c.newPage();await q.goto(base,{waitUntil:'networkidle'});await ready(q);
  await q.locator('[data-bg="paper"]').tap();assert.equal((await snapshot(q)).background,'paper');await q.locator('#guides').tap();assert.equal((await snapshot(q)).guides,true);await q.locator('#guides').tap();assert.equal((await snapshot(q)).guides,false);
  await q.locator('[data-character]').last().tap();assert.equal((await snapshot(q)).selected,assets.assets.at(-1).character);await q.locator('[data-bg="green"]').tap();assert.equal((await snapshot(q)).background,'green');await storage(q);await shot(q,'touch-phone-studio.png','.studio');return{touchControls:true,viewport:[390,844]};
 });
 for(const resource of ['atlas.json','atlas.png'])await check(`missing ${resource} reports failure and keeps controls disabled`,async()=>{
  const c=await context();const q=await c.newPage();await q.route(`**/assets/review/characters-v2/${resource}`,r=>r.abort());await q.goto(base,{waitUntil:'networkidle'});await q.locator('#error').waitFor({state:'visible'});assert.match(await q.locator('#error').textContent(),/could not load/);assert.equal(await q.locator('#character-name').textContent(),'Artwork unavailable');assert.equal(await q.locator('button:enabled,input:enabled').count(),0);assert.equal((await snapshot(q)).ready,false);await storage(q);await shot(q,`failure-${resource}.png`);return{message:await q.locator('#error').textContent()};
 });
}catch(error){report.fatal=error.stack;console.error(error)}finally{for(const c of contexts)await c.close();await browser.close();report.finishedAt=new Date().toISOString();report.passed=report.checks.filter(c=>c.status==='pass').length;report.failed=report.checks.filter(c=>c.status==='fail').length;await writeFile(path.join(output,'browser-report.json'),JSON.stringify(report,null,2)+'\n')}
if(report.fatal||report.failed)process.exitCode=1;
