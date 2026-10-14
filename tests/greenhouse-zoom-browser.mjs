import assert from 'node:assert/strict';import fs from 'node:fs/promises';import {createRequire} from 'node:module';
import {createState,startMorning,SAVE_KEY} from '../src/state.js';
import {initialState,pay,nearTub,blocked,ROOM,fishPosition} from '../art-review/greenhouse-state.js';
const {chromium}=createRequire(import.meta.url)(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright'),url=process.env.TEST_URL||'http://127.0.0.1:5228',out=process.env.TEST_OUTPUT_DIR||'docs/reviews/M1-TN2/greenhouse-zoom';await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE}),checks=[],errors=[];const pass=s=>{checks.push(s);console.log('PASS '+s);};
try{
 for(const [worldZoom,width,height]of [[0,390,844],[1,390,844],[2,390,844],[2,844,390]]){
  const context=await browser.newContext({viewport:{width,height},hasTouch:true,reducedMotion:'reduce'}),page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  const s=createState('Ari','boy','River');startMorning(s,true);s.scene='town';s.player={x:21,y:26,facing:'up'};s.lukeGreenhouse=pay(initialState(),2468);
  await context.addInitScript(({s,worldZoom,key})=>{localStorage.setItem(key,JSON.stringify(s));localStorage.setItem('critz-tycoon.ui.v1',JSON.stringify({frame:'leaf',calm:true,worldZoom}));localStorage.setItem('critz-tycoon.audio.v1',JSON.stringify({enabled:false,volume:0}));},{s,worldZoom,key:SAVE_KEY});
  await page.goto(url);await page.locator('[data-action=continue]').click();await page.locator('#start').click();await page.locator('[data-action=greenhouse]').click();await page.locator('iframe.game-room').waitFor();
  // The hosted HTML page redirects to /art-review/greenhouse; local retains
  // .html. Both identify this same room, including slower cold navigation.
  let f;for(let i=0;i<1500;i++){f=page.frames().find(f=>f!==page.mainFrame()&&f.url().includes('/art-review/greenhouse'));if(f)break;await page.waitForTimeout(20);}assert.ok(f);
  const snapshot=()=>f.evaluate(async()=> (await import('/art-review/greenhouse.js')).getReviewSnapshot());
  const until=async fn=>{for(let i=0;i<250;i++){const d=await snapshot();if(fn(d))return d;await page.waitForTimeout(20);}throw Error('Greenhouse state wait failed');};
  await f.locator('#begin').waitFor();await f.waitForFunction(()=>!!document.querySelector('#begin')&&!document.querySelector('#begin').disabled);await f.locator('#begin').click();await f.locator('#choices button').first().click();await until(d=>d.mode==='walk');
  const walking=(await snapshot()).presentation;assert.ok(walking.world);
  const current=await snapshot(),q=[{...current.player,path:[]}],seen=new Set([`${current.player.x},${current.player.y}`]);let route;
  for(const a of q){const facing=['up','down','left','right'].find(d=>nearTub(a.x,a.y,d)?.id===6);if(facing){route={...a,facing};break;}for(const [dir,dx,dy]of [['Up',0,-1],['Down',0,1],['Left',-1,0],['Right',1,0]]){const x=a.x+dx,y=a.y+dy,k=`${x},${y}`;if(!blocked(x,y)&&y!==ROOM.doorY&&!(x===current.luke.x&&y===current.luke.y)&&!seen.has(k)){seen.add(k);q.push({x,y,path:[...a.path,dir]});}}}assert.ok(route);
  for(const d of [...route.path,route.facing[0].toUpperCase()+route.facing.slice(1)]){await page.keyboard.press('Arrow'+d);await page.waitForTimeout(310);}
  await f.locator('#a').click();await f.locator('#choices button').filter({hasText:'Yes'}).click();await f.locator('#line').filter({hasText:'Wait for'}).waitFor();await f.locator('#choices button').first().click();await until(d=>d.mode==='observing'&&!d.presentation.world);
  for(let attempt=0;attempt<3;attempt++){
   const d=await snapshot(),at=fishPosition(d.fish[0],d.time+.4),p=await f.locator('#world').evaluate((c,at)=>{const r=c.getBoundingClientRect(),z=Math.min(c.width/480,c.height/340),x=Math.floor((c.width-480*z)/2),y=Math.floor((c.height-340*z)/2);return {x:r.left+(x+at.x*z)*r.width/c.width,y:r.top+(y+at.y*z)*r.height/c.height};},at);
   // Frame bounding boxes are relative to the top-level viewport.
   const iframe=await page.locator('iframe.game-room').boundingBox();await page.touchscreen.tap(iframe.x+p.x,iframe.y+p.y);await until(d=>d.mode==='reveal'||d.mode==='observing'&&d.net===null&&d.notice);if((await snapshot()).mode==='reveal')break;
  }
  const caught=await until(d=>d.mode==='reveal'&&!d.presentation.world);assert.equal(caught.state.collection.length,1);const h=caught.presentation.height;assert.ok(h>=90,'Subview too short for reveal');const viewport=await f.locator('#viewport').boundingBox();assert.ok(Math.abs(caught.presentation.scale-Math.min(1,viewport.width/480))<.001,'World zoom changed reveal presentation scale');await page.screenshot({path:`${out}/reveal-zoom${worldZoom+1}-${width}.png`});
  await f.locator('#a').click();await f.locator('#choices button').first().click();const restored=await until(d=>d.mode==='walk'&&d.presentation.world);assert.deepEqual(restored.presentation,walking);
  const after=await page.evaluate(async()=> (await import('/src/main.js')).getDebugSnapshot());for(const key of ['hero','gender','rival','money','debt','flags','inventory','tank'])assert.deepEqual(after[key],s[key],key);assert.equal(after.lukeGreenhouse.collection.length,1);
  pass(`Paid adventure scoop,touch catch,full reveal labels and walking zoom restoration atlevel${worldZoom+1}/${width}×${height};protected progress preserved`);await context.close();
 }
 assert.deepEqual(errors,[]);pass('No greenhouse zoom-flow exceptions');
}finally{await fs.writeFile(`${out}/browser-checks.json`,JSON.stringify({task:'M1.TN2',url,checks,errors,physicalSafari:false},null,2)+'\n');await browser.close();}
