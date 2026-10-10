import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {initialState,catchTraits,fishInTub,pay,chooseTub,collect,fishPosition,TUBS,ROOM,blocked,nearTub} from '../art-review/greenhouse-state.js';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES?path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'playwright'):'/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const url=process.env.CRITZ_GREENHOUSE_URL||'http://127.0.0.1:5186/art-review/greenhouse.html';
const output=process.env.CRITZ_QA_OUTPUT||'docs/reviews/M1-LG2';
const executablePath=process.env.CHROMIUM_EXECUTABLE||'/Users/tanoshi/Library/Caches/ms-playwright/chromium_headless_shell-1217/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const report={url,startedAt:new Date().toISOString(),checks:[],screenshots:[],limitations:['Chromium emulation; physical iOS Safari not tested.','Snapshot is read-only. Movement, dialogue, scooping and menus use actual input. Synthetic fixtures only in isolated contexts.']};
await mkdir(output,{recursive:true});const browser=await chromium.launch({executablePath,headless:true});const contexts=[],pages=[];
const KEY='critz.lukes-greenhouse.review.v1';
async function open(fixture=null,options={}){const c=await browser.newContext({viewport:{width:1024,height:800},...options});contexts.push(c);await c.addInitScript(({key,fixture})=>{if(!/^https?:$/.test(location.protocol))return;if(!sessionStorage.getItem('qa-seeded')){localStorage.setItem('critz-tycoon.save.v1','synthetic-adventure-preserve');localStorage.setItem('critz-tycoon.save.v1.backup','synthetic-backup-preserve');if(fixture)localStorage.setItem(key,JSON.stringify(fixture));sessionStorage.setItem('qa-seeded','yes');}window.__saveOps=[];const old=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){window.__saveOps.push(k);return old.call(this,k,v);};},{key:KEY,fixture});const p=await c.newPage();p.qaErrors=[];p.qaFailedAssets=[];p.on('pageerror',e=>p.qaErrors.push(e.message));p.on('response',r=>{if(r.status()>=400)p.qaFailedAssets.push(`${r.status()} ${r.url()}`)});p.on('requestfailed',r=>p.qaFailedAssets.push(r.url()));pages.push(p);await p.goto(url);await p.waitForFunction(()=>!document.querySelector('#begin').disabled);return p;}
async function snapshot(p){return p.evaluate(async()=> (await import('./greenhouse.js')).getReviewSnapshot());}
async function until(p,predicate){const end=Date.now()+8000;while(Date.now()<end){const s=await snapshot(p);if(predicate(s))return s;await p.waitForTimeout(30);}throw Error('Timed out waiting for state: '+JSON.stringify(await snapshot(p)));}
async function check(name,fn){try{const details=await fn();report.checks.push({name,pass:true,details});console.log('PASS '+name);}catch(e){report.checks.push({name,pass:false,error:e.stack});console.error('FAIL '+name+': '+e.message);}}
async function shot(p,name){const file=path.join(output,name);await p.screenshot({path:file,fullPage:true});report.screenshots.push(file);}
async function begin(p,touch=false){await p.locator('#begin')[touch?'tap':'click']();}
async function press(p,key){await p.keyboard.press(key);await p.waitForTimeout(315);}
async function step(p,dir,n=1){for(let i=0;i<n;i++)await press(p,'Arrow'+dir);}
async function enter(p){await step(p,'Up',3);await p.locator('#speech').waitFor({state:'visible'});}
async function answer(p,text){await p.locator('#choices button').filter({hasText:text}).click();}
async function continueSpeech(p){await p.locator('#choices button').first().click();}
async function buy(p){await answer(p,'Yes');await p.locator('#line').filter({hasText:'go ahead'}).waitFor();await continueSpeech(p);await until(p,s=>!s.busy);}
async function goToTub(p,id=6){
 const current=await snapshot(p),queue=[{x:current.player.x,y:current.player.y,path:[]}],seen=new Set([`${current.player.x},${current.player.y}`]);let route;
 for(const a of queue){const facing=['up','down','left','right'].find(d=>nearTub(a.x,a.y,d)?.id===id);if(facing){route={...a,facing};break;}for(const [dir,dx,dy]of [['Up',0,-1],['Down',0,1],['Left',-1,0],['Right',1,0]]){const x=a.x+dx,y=a.y+dy,k=`${x},${y}`;if(!blocked(x,y)&&y!==ROOM.doorY&&!(x===current.luke.x&&y===current.luke.y)&&!seen.has(k)){seen.add(k);queue.push({x,y,path:[...a.path,dir]});}}}
 assert.ok(route,`No walkable approach to tub ${id+1}`);for(const d of route.path)await step(p,d);await step(p,route.facing[0].toUpperCase()+route.facing.slice(1));const at=await snapshot(p);assert.equal(nearTub(at.player.x,at.player.y,at.player.facing)?.id,id);return route.path.length;
}
async function toTub(p){await goToTub(p);await press(p,'z');await p.locator('#line').filter({hasText:'Are you sure'}).waitFor();}
async function inspect(p){await answer(p,'Yes');await p.locator('#line').filter({hasText:'Wait for'}).waitFor();await continueSpeech(p);await until(p,s=>s.mode==='observing');}
async function canvasPoint(p,x,y){return p.locator('#world').evaluate((c,{x,y})=>{const r=c.getBoundingClientRect(),z=Math.min(c.width/480,c.height/340),px=Math.floor((c.width-480*z)/2),py=Math.floor((c.height-340*z)/2);return {x:r.left+(px+x*z)*r.width/c.width,y:r.top+(py+y*z)*r.height/c.height};},{x,y});}
async function tapPool(p,x,y,touch=false){const point=await canvasPoint(p,x,y);await p[touch?'touchscreen':'mouse'][touch?'tap':'click'](point.x,point.y);}
async function catchFish(p,touch=false){const before=await snapshot(p),f=before.fish[0],at=fishPosition(f,before.time+.40);await tapPool(p,at.x,at.y,touch);return until(p,s=>s.mode==='reveal');}
try{
 await check('actual shiny catch uses confirmed hopper tub and survives reload',async()=>{
  let seed=1;while(seed%8!==3||!catchTraits(seed,6,0,true).shiny)seed++;
  const q=await open(pay(initialState(),seed));await begin(q);await continueSpeech(q);await toTub(q);
  await until(q,s=>s.hopper.tub===6&&s.hopper.jump===0);await inspect(q);
  const before=await snapshot(q);assert.equal(before.state.visit.shimmeringTub,6);
  await tapPool(q,45,40);await until(q,s=>s.mode==='observing');assert.equal((await snapshot(q)).state.visit.shimmeringTub,6);
  const caught=await catchFish(q);assert.equal(caught.state.collection[0].shiny,true);await q.waitForTimeout(1200);await shot(q,'browser-shiny-reveal.png');
  const saved=caught.state.collection;await q.reload();await q.waitForFunction(()=>!document.querySelector('#begin').disabled);assert.deepEqual((await snapshot(q)).state.collection,saved);return {seed,fish:saved[0],missFree:true};
 });
 await check('ordinary Dorothy is the actual caught legendary, with no forced shine',async()=>{
  let seed=1;while(fishInTub(seed,6,true)[0].kind!==16)seed++;
  const q=await open(pay(initialState(),seed));await begin(q);await continueSpeech(q);await toTub(q);await inspect(q);const caught=await catchFish(q);assert.equal(caught.state.collection[0].kind,16);assert.equal(caught.state.collection[0].rarity,'legendary');assert.equal(caught.state.collection[0].shiny,false);await q.waitForTimeout(1200);await shot(q,'browser-dorothy-reveal.png');return caught.state.collection[0];
 });
 await check('native shadow layer animates in discrete pixels; off clears; calm is static',async()=>{
  const q=await open();const result=await q.evaluate(async()=>{const {paintShadowMask}=await import('./greenhouse-effects.js');const c=document.createElement('canvas');c.width=416;c.height=544;const x=c.getContext('2d');const render=opts=>{paintShadowMask(x,opts);return [...x.getImageData(0,0,416,544).data];};const a=render({enabled:true,time:0}),b=render({enabled:true,time:6}),c0=render({enabled:true,calm:true,time:0}),c1=render({enabled:true,calm:true,time:6}),off=render({enabled:false,time:6});return {moves:a.some((v,i)=>v!==b[i]),calm:c0.every((v,i)=>v===c1[i]),off:off.every(v=>v===0),binary:a.every((v,i)=>i%4!==3||v===0||v===255)};});assert.deepEqual(result,{moves:true,calm:true,off:true,binary:true});return result;
 });
 for(const p of pages){assert.deepEqual(p.qaErrors,[]);assert.deepEqual(p.qaFailedAssets,[]);}report.pass=report.checks.every(c=>c.pass);
}finally{await browser.close();await writeFile(path.join(output,'rarity-browser-checks.json'),JSON.stringify(report,null,2));}
if(!report.pass)process.exitCode=1;
