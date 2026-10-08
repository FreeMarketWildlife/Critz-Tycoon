import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import path from 'node:path';
const require=createRequire(import.meta.url);
const {chromium}=require(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'playwright'));
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE,headless:true});
const context=await browser.newContext({viewport:{width:1366,height:1000},acceptDownloads:true});
await context.addInitScript(()=>localStorage.setItem('critz-tycoon.save.v1','synthetic-music-sentinel'));
const p=await context.newPage(),errors=[],report=[];
p.on('pageerror',e=>errors.push(e.message));
const url=process.env.CRITZ_MUSIC_URL||'http://localhost:5186/music/';
const output=process.env.CRITZ_QA_OUTPUT||'test-results/music';
await mkdir(output,{recursive:true});
async function test(name,fn){try{await fn();report.push({name,pass:true});console.log('PASS '+name);}catch(e){report.push({name,pass:false,error:e.stack});console.error('FAIL '+name+' '+e.message);}}
try {
await p.goto(url);await p.waitForSelector('.track');
await test('all 30 unique tracks, stories and 60 download links load without autoplay',async()=>{
 assert.equal(await p.locator('.track').count(),30);assert.equal(await p.locator('.track-links a').count(),60);
 assert.equal(new Set(await p.locator('.track-title').allTextContents()).size,30);
 assert.equal(await p.locator('.track-spec').count(),30);assert.equal(await p.locator('.track-personality').count(),30);
 assert.match(await p.title(),/Thirty Different Days/);
 assert.ok(await p.locator('audio').evaluate(a=>a.paused));
});
await test('search and all mood filters return exactly their matching collection',async()=>{
 await p.locator('#search').fill('Kaid');assert.equal(await p.locator('.track').count(),1);assert.match(await p.locator('.track-title').innerText(),/Kaid/);
 await p.locator('#search').fill('zxzxzx');assert.ok(await p.locator('#empty').isVisible());
 await p.locator('#search').fill('');
 for(const name of ['Home & heart','Small delights','Out into the world','Strange & shadow','Slow evenings']){
  await p.getByRole('button',{name,exact:true}).click();const n=await p.locator('.track').count();assert.ok(n>=3&&n<30);assert.equal(await p.getByRole('button',{name,exact:true}).getAttribute('aria-pressed'),'true');
 }
 await p.getByRole('button',{name:'All',exact:true}).click();assert.equal(await p.locator('.track').count(),30);
});
await test('every rendered MP3 loads, decodes metadata, starts and seeks to a later section',async()=>{
 const tracks=await p.evaluate(async()=> (await (await fetch('album.json')).json()).tracks);
 for(const t of tracks){
  await p.locator(`.track[data-track="${t.id}"] .track-play`).click();
  await p.waitForFunction(()=>{const a=document.querySelector('audio');return a.readyState>=2&&!a.paused&&a.currentTime>0;});
  const status=await p.locator('audio').evaluate(a=>({duration:a.duration,error:a.error?.message}));
  assert.ok(Math.abs(status.duration-t.duration)<.3,t.title);assert.equal(status.error,undefined);
  const b=t.sections[Math.floor(t.sections.length/2)];
  await p.locator('#chapters button').filter({hasText:b.label}).first().click();
  await p.waitForFunction(expected=>Math.abs(document.querySelector('audio').currentTime-expected)<1.5,b.seconds);
  await p.locator('#toggle').click();assert.ok(await p.locator('audio').evaluate(a=>a.paused));
 }
});
await test('previous, next, play-all and actual end-of-track queue behavior',async()=>{
 await p.locator('#play-all').click();await p.waitForFunction(()=>!document.querySelector('audio').paused);
 assert.match(await p.locator('#now-number').innerText(),/^01/);
 await p.locator('#next').click();assert.match(await p.locator('#now-number').innerText(),/^02/);
 await p.locator('#previous').click();assert.match(await p.locator('#now-number').innerText(),/^01/);
 await p.waitForFunction(()=>document.querySelector('audio').readyState>=2);
 await p.locator('audio').evaluate(a=>{a.currentTime=a.duration-.15;});
 await p.waitForFunction(()=>document.querySelector('#now-number').textContent.startsWith('02'));
});
await test('native repeat, final-track stop and one-player exclusivity',async()=>{
 await p.locator('#repeat').check();assert.ok(await p.locator('audio').evaluate(a=>a.loop));
 await p.locator('#repeat').uncheck();
 await p.locator('.track[data-track="30"] .track-play').click();await p.waitForFunction(()=>document.querySelector('audio').readyState>=2);
 await p.locator('audio').evaluate(a=>{a.currentTime=a.duration-.15;});
 await p.waitForFunction(()=>document.querySelector('audio').paused);
 assert.match(await p.locator('#now-number').innerText(),/^30/);assert.equal(await p.locator('audio').count(),1);
});
await test('MIDI ZIP and individual MIDI download preserve their formats',async()=>{
 let download=p.waitForEvent('download');await p.locator('.download').click();let d=await download;await d.saveAs(path.join(output,'album.zip'));assert.match(d.suggestedFilename(),/30-midi.zip$/);
 download=p.waitForEvent('download');await p.locator('.track[data-track="1"] .track-links a').first().click();d=await download;assert.match(d.suggestedFilename(),/\.mid$/);
 const first=await p.evaluate(async()=> (await (await fetch('album.json')).json()).tracks[0]);
 const response=await context.request.get(new URL(first.midi,url).href);assert.equal((await response.body()).subarray(0,4).toString(),'MThd');
});
await test('audio failure is visible and a later selection recovers',async()=>{
 await p.route('**/audio/03-*.mp3',route=>route.abort());
 await p.locator('.track[data-track="3"] .track-play').click();await p.waitForFunction(()=>!document.querySelector('#player-error').hidden);
 await p.unroute('**/audio/03-*.mp3');await p.locator('.track[data-track="4"] .track-play').click();
 await p.waitForFunction(()=>!document.querySelector('audio').paused&&document.querySelector('audio').readyState>=2);assert.ok(await p.locator('#player-error').isHidden());await p.locator('#toggle').click();
});
await test('desktop, small phone and landscape have no horizontal overflow',async()=>{
 for(const [width,height] of [[1366,1000],[390,844],[320,568],[844,390]]){
  await p.setViewportSize({width,height});await p.evaluate(()=>scrollTo(0,0));
  assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),String(width));
  await p.screenshot({path:path.join(output,`listening-room-${width}.png`),fullPage:width===1366});
 }
});
await test('synthetic game save stays byte-identical and no runtime errors',async()=>{
 assert.equal(await p.evaluate(()=>localStorage.getItem('critz-tycoon.save.v1')),'synthetic-music-sentinel');assert.deepEqual(errors,[]);
});
}finally{await writeFile(path.join(output,'browser-report.json'),JSON.stringify(report,null,2)+'\n');await browser.close();}
if(report.some(r=>!r.pass))process.exitCode=1;
