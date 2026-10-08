import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {createState,startMorning,SAVE_KEY} from '../src/state.js';
const require=createRequire(import.meta.url),{chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE});
const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true}),page=await context.newPage();
const url=process.env.TEST_URL||'http://127.0.0.1:5173',out=process.env.TEST_OUTPUT_DIR||'test-results/screen',checks=[],errors=[];
await mkdir(out,{recursive:true});page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(r.url());});
const pass=s=>{checks.push(s);console.log('PASS '+s);};
async function fixture(scene='town',x=22,y=25){
 await page.goto(url);await page.waitForSelector('[data-action=new]');const s=createState('Ari','boy','River');startMorning(s,true);s.scene=scene;s.player={x,y,facing:'up'};
 await page.evaluate(({s,key})=>{localStorage.clear();localStorage.setItem(key,JSON.stringify(s));},{s,key:SAVE_KEY});await page.reload();await page.locator('[data-action=continue]').click();
}
try {
 await fixture();
 for(const [width,height] of [[320,568],[390,844],[430,932],[844,390],[1280,900]]) {
  await page.setViewportSize({width,height});await page.waitForTimeout(100);
  const world=await page.locator('#viewport').boundingBox(),canvas=await page.locator('#world').boundingBox(),controls=await page.locator('#controller').boundingBox();
  assert.equal(world.x,0);assert.equal(world.y,0);assert.equal(canvas.x,0);assert.equal(canvas.y,0);
  if(width>height&&height<600){assert.equal(world.height,height);assert.equal(world.width,controls.x);}
  else {assert.equal(world.width,width);assert.equal(world.height,controls.y);assert.equal(controls.y+controls.height,height);}
  const native=await page.locator('#world').evaluate(c=>({width:c.width,height:c.height}));
  assert.ok(Math.abs(canvas.width/native.width-canvas.height/native.height)<.001,'square pixel scale');
  assert.ok(canvas.width>=world.width&&canvas.width-world.width<2);assert.ok(canvas.height>=world.height&&canvas.height-world.height<2);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth===innerWidth&&document.documentElement.scrollHeight===innerHeight));
  for(const selector of ['#a-button','#b-button','#start','#run','.up','.down','.left','.right']){const b=await page.locator(selector).boundingBox();assert.ok(b.width>=44&&b.height>=44);assert.ok(b.x>=0&&b.y>=0&&b.x+b.width<=width&&b.y+b.height<=height);}
  assert.equal(await page.locator('.brand,#hud,#quest-strip,#interact-prompt,#scene-label,#toast,footer').count(),0);
  await page.screenshot({path:`${out}/world-${width}.png`});pass(`${width}×${height}: world fills available top edge, pixels remain square, controls fit, no page overflow or tip chrome`);
 }
 await page.setViewportSize({width:390,height:844});await page.locator('#start').click();
 assert.match(await page.locator('.menu-status').textContent(),/Rootport.*Day 1/);assert.match(await page.locator('.eyebrow').textContent(),/Ari.*\$/);
 await page.locator('[data-action=save]').click();assert.match(await page.locator('#panel-status').textContent(),/Progress saved/);
 const original=await page.evaluate(k=>localStorage.getItem(k),SAVE_KEY);
 await page.evaluate(()=>{const set=Storage.prototype.setItem;window.restoreTestStorage=()=>Storage.prototype.setItem=set;Storage.prototype.setItem=function(){throw new DOMException('Synthetic quota','QuotaExceededError');};});
 await page.locator('[data-action=save]').click();assert.match(await page.locator('#panel-status').textContent(),/Could not save/);assert.ok(await page.locator('#panel-status').isVisible());assert.equal(await page.evaluate(k=>localStorage.getItem(k),SAVE_KEY),original);
 await page.screenshot({path:`${out}/inline-save-error.png`});await page.evaluate(()=>window.restoreTestStorage());await page.locator('[data-action=save]').click();assert.match(await page.locator('#panel-status').textContent(),/Progress saved/);
 await page.locator('[data-action=notebook]').click();assert.ok((await page.locator('.notice').first().textContent()).length>10);pass('Start retains money, place/time, Notebook objectives and inline save success/error; failed save preserves original bytes');
 await fixture('yard',13,5);await page.locator('#a-button').tap();assert.equal(await page.locator('#toast,#interact-prompt').count(),0);assert.match(await page.locator('#game-status').textContent(),/apples/);assert.equal(await page.locator('#game-status').evaluate(e=>e.getBoundingClientRect().width),1);await page.screenshot({path:`${out}/quiet-harvest.png`});pass('Harvest has animation and accessible feedback without a visible popup');
 const lighting=await page.evaluate(async()=>{const {applyLighting}=await import('/src/lighting.js'),{createState,startMorning}=await import('/src/state.js');const c=document.createElement('canvas');c.width=700;c.height=900;const x=c.getContext('2d'),s=createState();startMorning(s,true);s.time=23;x.fillStyle='#fff';x.fillRect(0,0,700,900);applyLighting(x,s);return {near:[...x.getImageData(100,100,1,1).data],far:[...x.getImageData(699,899,1,1).data]};});assert.deepEqual(lighting.near,lighting.far);assert.ok(lighting.far[0]<255);pass('Night lighting covers the entire expanded framebuffer');
 assert.deepEqual(errors,[]);pass('No missing assets or uncaught exceptions');
} finally {await writeFile(`${out}/report.json`,JSON.stringify({checks,errors},null,2)+'\n');await browser.close();}
