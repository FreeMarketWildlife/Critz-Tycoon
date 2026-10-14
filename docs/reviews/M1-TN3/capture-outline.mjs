// Inspect the actual playable renderer at every existing world zoom.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {createRequire} from 'node:module';
import {createState,startMorning,SAVE_KEY} from '../../../src/state.js';
import {TANOSHI} from '../../../src/tanoshi.js';
const {chromium}=createRequire(import.meta.url)(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const out=process.env.TEST_OUTPUT_DIR,url=process.env.TEST_URL;
await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE});
const context=await browser.newContext({viewport:{width:390,height:844},hasTouch:true,reducedMotion:'reduce'});
const page=await context.newPage(),checks=[],errors=[];
page.on('pageerror',e=>errors.push(e.message));
page.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('favicon.ico'))errors.push(r.url());});
try{
 for(const zoom of [0,1,2])for(const t of TANOSHI){
  const s=createState('Ari','boy','River');startMorning(s,true);s.scene=t.scene;s.player={x:t.x+1,y:t.y,facing:'left'};s.dayClock={day:1,minute:720,remainder:0};
  await page.goto(url);await page.locator('[data-action=new]').waitFor();
  await page.evaluate(({s,key,zoom})=>{localStorage.clear();localStorage.setItem(key,JSON.stringify(s));localStorage.setItem('critz-tycoon.ui.v1',JSON.stringify({frame:'ocean',calm:true,worldZoom:zoom}));localStorage.setItem('critz-tycoon.audio.v1',JSON.stringify({enabled:false,volume:0}));},{s,key:SAVE_KEY,zoom});
  await page.reload();await page.locator('[data-action=continue]').click();
  await page.waitForFunction(async()=>!!(await import('/src/render.js')).getRenderDebug().camera);
  const d=await page.evaluate(async()=>{const c=document.querySelector('#world'),r=(await import('/src/render.js')).getRenderDebug(),ui=(await import('/src/main.js')).getDebugUI();return {...r,zoom:ui.settings.worldZoom,smoothing:c.getContext('2d').imageSmoothingEnabled};});
  assert.equal(d.zoom,zoom);assert.equal(d.smoothing,false);
  await page.screenshot({path:`${out}/${t.id}-zoom${zoom+1}-phone.png`});
  const png=await page.locator('#world').evaluate(c=>c.toDataURL());
  await fs.writeFile(`${out}/${t.id}-zoom${zoom+1}-world.png`,Buffer.from(png.split(',')[1],'base64'));
  checks.push({id:t.id,size:t.size,zoom:zoom+1,scene:t.scene,width:d.width,height:d.height,camera:d.camera,smoothing:d.smoothing});
 }
 assert.deepEqual(errors,[]);
}finally{await fs.writeFile(`${out}/checks.json`,JSON.stringify({task:'M1.TN3',checks,errors,syntheticOnly:true,physicalSafari:false},null,2)+'\n');await browser.close();}
console.log(`PASS ${checks.length} actual in-game outline views across all four Tanoshi sizes and three zooms`);
