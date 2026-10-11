// Isolated synthetic saves only. Never connects to a user browser profile.
import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE});
const base=process.env.TEST_URL||'http://127.0.0.1:5178';
const results=[], errors=[];
const out=process.env.TEST_OUTPUT_DIR||'test-results/visual'; await mkdir(out,{recursive:true});
try {
 const context=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
 const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base);await page.waitForSelector('[data-action="new"]');
 const fidelity=await page.evaluate(async()=>{
  const {character}=await import('./src/render.js');
  const m=await (await fetch('./assets/playable/atlas.json')).json();const im=new Image();im.src='./assets/playable/atlas.png';await im.decode();
  const source=document.createElement('canvas');source.width=im.width;source.height=im.height;const s=source.getContext('2d');s.drawImage(im,0,0);
  const cv=document.createElement('canvas');cv.width=48;cv.height=48;const c=cv.getContext('2d');let checked=0;const mismatches=[];
  for(const a of m.assets.filter(a=>a.id.startsWith('char.'))){
   c.clearRect(0,0,48,48);character(c,24,40,{look:a.character,facing:a.direction,mode:a.mode,pose:a.pose});
   const expected=s.getImageData(...a.rect).data, actual=c.getImageData(24-a.anchor[0],40-a.anchor[1],a.rect[2],a.rect[3]).data;
   if(actual.some((v,i)=>v!==expected[i]))mismatches.push(a.id);checked++;
  }
  return {checked,mismatches};
 });
 assert.equal(fidelity.checked,288);assert.deepEqual(fidelity.mismatches,[]);results.push('all 288 character entries render pixel-exact at the native foot anchor');
 for(const [scene,pos] of Object.entries({bedroom:[8,7],house:[8,7],yard:[8,7],town:[15,9],critz:[8,8],vet:[8,8],pharmacy:[8,8],bike:[8,8],glass:[8,8],kaidHome:[8,8],rivalHome:[8,10]})) {
  const data=await page.evaluate(async({scene,pos})=>{
   const {createState,startMorning}=await import('./src/state.js');const {isBlocked}=await import('./src/world.js');const {renderWorld,getRenderDebug}=await import('./src/render.js');
   const s=createState('Review','boy','Robin');startMorning(s);s.scene=scene;s.player={x:pos[0],y:pos[1],facing:'down'};if(isBlocked(scene,...pos,s))throw new Error('Blocked visual fixture '+scene);
   // A separate native canvas avoids the main game's animation loop.
   const cv=document.createElement('canvas');cv.width=240;cv.height=160;
   renderWorld(cv,s,0,{x:pos[0]*16,y:pos[1]*16,facing:'down',pose:'idle',action:'idle'});
   return {png:cv.toDataURL().split(',')[1],debug:getRenderDebug()};
  },{scene,pos});
  await writeFile(`${out}/${scene}-native.png`,Buffer.from(data.png,'base64'));
  assert.equal(data.debug.width,240);assert.equal(data.debug.height,160);
  assert.ok(Object.values(data.debug.camera).every(Number.isInteger));
  results.push(`${scene}: native atlas render and integer camera`);
 }
 // Verify canopy opaque pixels cover an actor behind it, then a foreground
 // actor's opaque pixels cover the same tree. Compare actual atlas RGB bytes.
 const layer=await page.evaluate(async()=>{
  const {createState,startMorning}=await import('./src/state.js');const {renderWorld}=await import('./src/render.js');
  const m=await (await fetch('./assets/playable/atlas.json')).json();const im=new Image();im.src='./assets/playable/atlas.png';await im.decode();
  const ac=document.createElement('canvas');ac.width=im.width;ac.height=im.height;const a=ac.getContext('2d');a.drawImage(im,0,0);
  const cv=document.createElement('canvas');cv.width=240;cv.height=160;const c=cv.getContext('2d');const s=createState();startMorning(s);s.scene='town';s.player={x:10,y:5,facing:'down'};
  let count=0,bad=0;const t=m.assets.find(e=>e.id==='tree.canopy');const rgba=a.getImageData(...t.rect).data;
  const view={x:160,y:80,facing:'down',pose:'idle',action:'idle'};renderWorld(cv,s,0,view);
  for(let y=0;y<32;y++)for(let x=0;x<32;x++) {const i=(y*32+x)*4;if(!rgba[i+3])continue;
   const pixel=c.getImageData(144+x-(160-120),64+y-(80-88),1,1).data;count++;if(pixel.some((v,j)=>v!==rgba[i+j]))bad++;
  }
  // No other actor overlaps the tree; foreground Hero is later in depth order.
  const h=m.assets.find(e=>e.id==='char.hero.boy.down.walk.idle');const hero=a.getImageData(...h.rect).data;let frontCount=0,frontBad=0;
  renderWorld(cv,s,0,{...view,y:104});
  for(let y=0;y<h.rect[3];y++)for(let x=0;x<h.rect[2];x++){const i=(y*h.rect[2]+x)*4;if(!hero[i+3])continue;const p=c.getImageData(120-h.anchor[0]+x,88-h.anchor[1]+y,1,1).data;frontCount++;if(p.some((v,j)=>v!==hero[i+j]))frontBad++;}
  return {count,bad,frontCount,frontBad};
 });
 assert.ok(layer.count>100&&layer.frontCount>50);assert.equal(layer.bad,0);assert.equal(layer.frontBad,0);results.push('canopy/actor occlusion: atlas-pixel equality behind and in front');
 await page.addInitScript(()=>localStorage.clear());
 for(const [w,h] of [[320,568],[390,844],[844,390],[1280,900]]) {
  await page.setViewportSize({width:w,height:h});await page.evaluate(()=>localStorage.clear());await page.reload();await page.waitForSelector('[data-action="new"]');
  await page.locator('[data-action="new"]').click();
  const previews=await page.locator('.hero-preview').evaluateAll(canvases=>canvases.map(c=>({w:c.width,h:c.height,display:[c.getBoundingClientRect().width,c.getBoundingClientRect().height]})));
  assert.deepEqual(previews,[{w:24,h:32,display:[48,64]},{w:24,h:32,display:[48,64]}]);
  await page.locator('#hero-name').fill('Review');await page.locator('#rival-name').fill('Robin');await page.locator('[data-action="begin"]').click();
  for(let i=0;i<2;i++)await page.locator('#a-button').click();
  const layout=await page.evaluate(()=>{const b=document.getElementById('world').getBoundingClientRect();return {w:b.width,h:b.height,screen:innerWidth,doc:document.documentElement.scrollWidth,controls:[...document.querySelectorAll('[data-dir],#a-button,#b-button')].map(b=>({w:b.getBoundingClientRect().width,h:b.getBoundingClientRect().height}))};});
  console.log({viewport:[w,h],layout});
  await page.screenshot({path:`${out}/phone-${w}x${h}.png`,fullPage:true});
  assert.equal(layout.w/240,Math.floor(layout.w/240));assert.equal(layout.h/160,layout.w/240);assert.ok(layout.doc<=w);assert.ok(layout.controls.every(c=>c.w>=44&&c.h>=44));
  await page.screenshot({path:`${out}/phone-${w}x${h}.png`,fullPage:true});results.push(`${w}x${h}: integer uniform world scale, no horizontal overflow,44px controls`);
 }
 // Intentionally missing assets must fail visibly without touching storage.
 const bad=await browser.newContext();await bad.route('**/assets/playable/atlas.png',r=>r.abort());const p=await bad.newPage();await p.goto(base);await p.waitForSelector('[data-action="reload"]');
 assert.equal(await p.locator('#panel-title').textContent(),'Artwork could not load');assert.equal(await p.evaluate(()=>localStorage.length),0);await bad.close();results.push('missing PNG produces recoverable error without save writes');
 assert.deepEqual(errors,[]);results.push('zero uncaught browser exceptions');
  await writeFile(`${out}/visual-browser.json`,JSON.stringify({passed:results.length,results,layer,fidelity,errors},null,2)+'\n');console.log(JSON.stringify({passed:results.length,results,layer,fidelity,errors},null,2));await context.close();
} finally {await browser.close();}
