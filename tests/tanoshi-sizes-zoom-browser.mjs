// Real production UI, fresh isolated contexts and synthetic saves only.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {createRequire} from 'node:module';
import {createState,startMorning,SAVE_KEY,BACKUP_KEY} from '../src/state.js';
import {scenes} from '../src/world.js';
import {TANOSHI} from '../src/tanoshi.js';
const require=createRequire(import.meta.url),{chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const url=process.env.TEST_URL||'http://127.0.0.1:5228',out=process.env.TEST_OUTPUT_DIR||'docs/reviews/M1-TN2/browser';
await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE}),context=await browser.newContext({viewport:{width:390,height:844},hasTouch:true,reducedMotion:'reduce'}),page=await context.newPage(),checks=[],errors=[];
page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('favicon.ico'))errors.push(r.url());});
const pass=message=>{checks.push(message);console.log('PASS '+message);};
const snapshot=()=>page.evaluate(async()=> (await import('/src/main.js')).getDebugSnapshot());
const ui=()=>page.evaluate(async()=> (await import('/src/main.js')).getDebugUI());
const render=()=>page.evaluate(async()=> (await import('/src/render.js')).getRenderDebug());
const stateAt=(scene,x,y,access=false)=>{const s=createState('Ari','boy','River');startMorning(s,true);s.scene=scene;s.player={x,y,facing:'up'};s.liarsvilleBearAccess=access;s.dayClock={day:1,minute:720,remainder:0};return s;};
async function fixture(s,zoom=0,legacy=false){
 await page.goto(url);await page.locator('[data-action=new]').waitFor();
 const state=structuredClone(s);if(legacy)delete state.liarsvilleBearAccess;
 const bytes=JSON.stringify(state,null,2);
 await page.evaluate(({bytes,zoom,key})=>{localStorage.clear();localStorage.setItem(key,bytes);localStorage.setItem('critz-tycoon.audio.v1',JSON.stringify({enabled:false,volume:0}));localStorage.setItem('critz-tycoon.ui.v1',JSON.stringify({frame:'ocean',calm:true,worldZoom:zoom}));},{bytes,zoom,key:SAVE_KEY});
 await page.reload();await page.locator('[data-action=continue]').click();await page.waitForFunction(async()=>!!(await import('/src/render.js')).getRenderDebug().camera);return bytes;
}
async function centered(){const r=await render(),s=await snapshot(),offset=s.gender==='girl'?23:21;assert.equal(r.playerFoot.x-r.camera.x,r.width/2);assert.equal(r.playerFoot.y-offset-r.camera.y,r.height/2);assert.ok(await page.locator('#world').evaluate(c=>!c.getContext('2d').imageSmoothingEnabled));const a=await page.locator('#world').boundingBox(),v=await page.locator('#viewport').boundingBox();assert.ok(Math.abs(a.x+a.width/2-v.x-v.width/2)<.02);assert.ok(Math.abs(a.y+a.height/2-v.y-v.height/2)<.02);return r;}
async function dismiss(){for(let i=0;i<30&&await page.locator('#dialogue').isVisible();i++)await page.locator('#a-button').click();assert.equal(await page.locator('#dialogue').isVisible(),false);}
async function hold(key,until){await page.keyboard.down(key);try{for(let i=0;i<120;i++){if(await until())break;await page.waitForTimeout(10);}}finally{await page.keyboard.up(key);}await page.waitForFunction(async()=> (await import('/src/main.js')).getDebugMovement().settled);}
try{
 for(const [width,height]of [[320,568],[390,844],[844,390],[1280,900]]){
  await page.setViewportSize({width,height});await fixture(stateAt('town',21,26));await centered();
  const controls=await page.locator('#controller').boundingBox();await page.locator('#start').click();
  const before=await snapshot(),raw=await page.evaluate(key=>localStorage.getItem(key),SAVE_KEY);
  assert.equal((await ui()).settings.worldZoom,0);assert.ok(await page.locator('[data-action=zoom-out]').isDisabled());
  for(const level of [1,2]){await page.locator('[data-action=zoom-in]').click();assert.equal((await ui()).settings.worldZoom,level);await page.waitForTimeout(40);await centered();assert.deepEqual(await page.locator('#controller').boundingBox(),controls);await page.screenshot({path:`${out}/zoom-${level+1}-${width}.png`});}
  assert.ok(await page.locator('[data-action=zoom-in]').isDisabled());await page.keyboard.press('+');assert.equal((await ui()).settings.worldZoom,2);
  assert.equal(await page.evaluate(key=>localStorage.getItem(key),SAVE_KEY),raw);assert.deepEqual((await snapshot()).player,before.player);await page.waitForTimeout(200);assert.deepEqual((await snapshot()).dayClock,before.dayClock);
  await page.keyboard.press('-');assert.equal((await ui()).settings.worldZoom,1);await page.keyboard.press('-');assert.equal((await ui()).settings.worldZoom,0);await page.keyboard.press('-');assert.equal((await ui()).settings.worldZoom,0);
  const buttons=await page.locator('.world-zoom button').evaluateAll(bs=>bs.map(b=>{const r=b.getBoundingClientRect();return [r.width,r.height];}));assert.ok(buttons.every(([w,h])=>w>=44&&h>=44));
  await page.locator('[data-action=zoom-in]').focus();await page.keyboard.press('Enter');assert.equal((await ui()).settings.worldZoom,1);
  await page.keyboard.press('p');await hold('ArrowDown',async()=> (await snapshot()).player.y>=27);await centered();assert.ok((await snapshot()).player.y>=27);
  await page.reload();await page.locator('[data-action=continue]').click();assert.equal((await ui()).settings.worldZoom,1);assert.equal((await ui()).settings.frame,'ocean');await centered();
  await page.setViewportSize({width:height,height:width});await page.waitForTimeout(60);await centered();assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  pass(`Three bounded minus/plus settings,44px touch targets,keyboard,paused clock/fixed controls,reload and rotation at${width}×${height}`);
 }
 // Saved actual renderer output at every boundary, including rooms smaller
 // than the viewport. Direct rendering uses synthetic states, not live saves.
 await page.setViewportSize({width:390,height:844});await fixture(stateAt('town',21,26));
 const edgeEvidence=await page.evaluate(async()=>{
  const {scenes}=await import('/src/world.js'),{renderWorld,getRenderDebug}=await import('/src/render.js'),{createState,startMorning}=await import('/src/state.js'),{worldViewport}=await import('/src/world-space.js');
  const c=document.createElement('canvas'),rows=[];
  for(const scene of Object.keys(scenes))for(const gender of ['boy','girl'])for(const zoom of [0,1,2]){
   const f=worldViewport(390,620,zoom);c.width=f.width;c.height=f.height;
   const m=scenes[scene],positions=[[1,3],[m.w-1,3],[1,m.h-1],[m.w-1,m.h-1],[Math.floor(m.w/2),3],[Math.floor(m.w/2),m.h-1],[1,Math.floor(m.h/2)],[m.w-1,Math.floor(m.h/2)]];
   for(const [x,y]of positions){const s=createState('Ari',gender,'River');startMorning(s,false);s.scene=scene;s.player={x,y,facing:'down'};s.dayClock={day:1,minute:720,remainder:0};renderWorld(c,s,0,{x:x*16,y:y*16,facing:'down',pose:'idle',action:'walk',moving:false});const d=getRenderDebug();if(d.playerFoot.x-d.camera.x!==d.width/2||d.playerFoot.y-(gender==='girl'?23:21)-d.camera.y!==d.height/2)throw Error(`Off-center ${scene}/${gender}/${zoom}/${x},${y}`);const pixels=c.getContext('2d').getImageData(0,0,c.width,c.height).data;if(pixels.some((v,i)=>i%4===3&&v!==255))throw Error('Unpainted backdrop '+scene);rows.push({scene,gender,zoom,x,y,camera:d.camera,width:d.width,height:d.height});}
  }
  return rows;
 });
 assert.equal(edgeEvidence.length,Object.keys(scenes).length*2*3*8);await fs.writeFile(`${out}/edge-center-checks.json`,JSON.stringify(edgeEvidence,null,2)+'\n');pass(`${edgeEvidence.length} actual renderer edge/corner checks across every scene,both genders and all levels;opaque intentional backdrops`);
 // Native variants are visible and discoverable in their existing areas.
 for(const t of TANOSHI){const s=stateAt(t.scene,t.x+1,t.y);s.player.facing='left';await fixture(s,1);await centered();await page.screenshot({path:`${out}/${t.variant}-phone.png`});await fs.writeFile(`${out}/${t.variant}-world.png`,Buffer.from((await page.locator('#world').evaluate(c=>c.toDataURL())).split(',')[1],'base64'));await page.locator('#a-button').click();await dismiss();assert.deepEqual((await snapshot()).tanoshiDiscoveries,[t.id]);await page.locator('#a-button').click();assert.equal(await page.locator('#speaker').textContent(),t.name);await dismiss();for(const key of ['hero','gender','rival','money','debt','flags','inventory','tankOwned'])assert.deepEqual((await snapshot())[key],s[key]);pass(`${t.name} native-visible,first/repeat personality greeting and protected progress`);}
 for(const zoom of [0,1,2]){
  await fixture(stateAt('forest',9,22),zoom,true);await centered();await hold('ArrowUp',async()=>false);assert.deepEqual([(await snapshot()).player.x,(await snapshot()).player.y],[9,22]);await page.screenshot({path:`${out}/bear-closed-zoom${zoom+1}.png`});await page.locator('#a-button').click();assert.match(await page.locator('#dialogue-accessible').textContent(),/blocked for now/);await centered();await dismiss();
  const s=stateAt('forest',9,20);const bytes=await fixture(s,zoom,true);assert.equal((await snapshot()).liarsvilleBearAccess,true);assert.equal((await snapshot()).player.y,20);assert.deepEqual((await page.evaluate(async()=> (await import('/src/main.js')).getDebugEntities())).find(e=>e.id==='route-bear').collision,[17,22,3,1]);await hold('ArrowDown',async()=> (await snapshot()).player.y>=22);await centered();await page.screenshot({path:`${out}/bear-aside-zoom${zoom+1}.png`});await page.locator('#start').click();await page.locator('[data-action=save]').click();assert.equal(await page.evaluate(key=>localStorage.getItem(key),BACKUP_KEY),bytes);
  await fixture(stateAt('forest',18,23,true),zoom);await centered();await page.screenshot({path:`${out}/bear-aside-zoom${zoom+1}.png`});await page.locator('#a-button').click();assert.match(await page.locator('#dialogue-accessible').textContent(),/room to pass/);await dismiss();
  await fixture(stateAt('liarsville',14,28),zoom,true);await hold('ArrowDown',async()=> (await snapshot()).scene==='forest');assert.equal((await snapshot()).scene,'forest');assert.equal((await snapshot()).liarsvilleBearAccess,true);await page.waitForTimeout(80);await centered();
  await fixture(stateAt('forest',13,3,true),zoom);await hold('ArrowUp',async()=> (await snapshot()).scene==='liarsville');assert.equal((await snapshot()).scene,'liarsville');await page.waitForTimeout(80);await centered();
  pass(`Closed bear collision/dialogue,northern legacy access/backup and both Liarsville transitions atzoom${zoom+1}`);
 }
 // Preference-write failure leaves the active adventure save intact.
 await fixture(stateAt('yard',8,10),0);await page.locator('#start').click();const bytes=await page.evaluate(key=>localStorage.getItem(key),SAVE_KEY);
 await page.evaluate(()=>{const set=Storage.prototype.setItem;window.restorePreferenceWrite=()=>Storage.prototype.setItem=set;Storage.prototype.setItem=function(k,v){if(k==='critz-tycoon.ui.v1')throw Error('Synthetic quota');return set.call(this,k,v);};});await page.locator('[data-action=zoom-in]').click();assert.match(await page.locator('#panel-status').textContent(),/could not be saved/);assert.equal(await page.evaluate(key=>localStorage.getItem(key),SAVE_KEY),bytes);await page.evaluate(()=>window.restorePreferenceWrite());await page.locator('[data-action=zoom-out]').click();assert.match(await page.locator('#panel-status').textContent(),/World zoom saved/);assert.equal(await page.evaluate(key=>localStorage.getItem(key),SAVE_KEY),bytes);pass('Failed zoom persistence reports inline,preserves exact adventure bytes and clears on successful preference retry');
 assert.deepEqual(errors,[]);pass('No runtime errors or missing assets');
}finally{await fs.writeFile(`${out}/browser-checks.json`,JSON.stringify({task:'M1.TN2',url,checks,errors,physicalSafari:false},null,2)+'\n');await browser.close();}
