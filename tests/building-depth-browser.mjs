import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {createState,startMorning,SAVE_KEY} from '../src/state.js';
import {scenes} from '../src/world.js';
const require=createRequire(import.meta.url),{chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE});
const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true}),page=await context.newPage();
const out=process.env.TEST_OUTPUT_DIR||'test-results/building-depth',checks=[],errors=[];await mkdir(out,{recursive:true});
page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(r.url());});
const snap=()=>page.evaluate(async()=> (await import('/src/main.js')).getDebugSnapshot());
const motion=()=>page.evaluate(async()=> (await import('/src/main.js')).getDebugMovement());
async function until(read,predicate){for(let n=0;n<800;n++){const v=await read();if(predicate(v))return;await page.waitForTimeout(10);}throw Error('Movement timeout');}
async function fixture(scene,x,y){
 await page.goto(process.env.TEST_URL||'http://127.0.0.1:5173');await page.waitForSelector('[data-action=new]');
 const s=createState('Ari','boy','River');startMorning(s,true);s.scene=scene;s.player={x,y,facing:'right'};
 await page.evaluate(({s,key})=>{localStorage.clear();localStorage.setItem(key,JSON.stringify(s));},{s,key:SAVE_KEY});await page.reload();await page.locator('[data-action=continue]').click();
}
async function walk(key,x){
 await until(motion,m=>m.settled&&m.action==='idle');await page.keyboard.down(key);
 try{await until(motion,m=>(m.destination?.x??m.tileX)===x);}finally{await page.keyboard.up(key);}
 await until(motion,m=>m.settled&&m.action==='idle');assert.equal((await snap()).player.x,x);
}
try{
 for(const id of ['town','liarsville'])for(const b of scenes[id].map.objects.filter(o=>o.kind==='building')){
  const y=b.y+b.rearDepth-1;await fixture(id,b.x-1,y);await walk('ArrowRight',b.x+Math.floor(b.w/2));
  if(b.name==='HOME'||b.name==='THE OLD WATERWORKS')await page.screenshot({path:`${out}/${id}-behind.png`});
  await walk('ArrowRight',b.x+b.w-1);
  await page.keyboard.down('ArrowDown');await page.waitForTimeout(500);await page.keyboard.up('ArrowDown');await until(motion,m=>m.settled&&m.action==='idle');assert.equal((await snap()).player.y,y,'solid wall below overlap');
  await walk('ArrowLeft',b.x-1);assert.equal((await snap()).scene,id);checks.push(`${id}/${b.name}: walk across ${b.rearDepth}-tile rear band, blocked by wall, return safely`);console.log('PASS '+checks.at(-1));
 }
 const pixels=await page.evaluate(async()=>{
  const {renderEnvironment}=await import('/src/environment-render.js'),{scenes}=await import('/src/world.js'),{createState,startMorning}=await import('/src/state.js');
  const cv=document.createElement('canvas');cv.width=480;cv.height=320;const c=cv.getContext('2d');const s=createState();startMorning(s,true);
  const paint=(c,x,y,opts)=>{if(opts.look)return;c.fillStyle='#ff00ff';c.fillRect(-16,-64,32,64);};
  const count=(x,y)=>{renderEnvironment(c,s,0,{x:x*16,y:y*16,facing:'down',pose:'idle',action:'idle'},paint,()=> 'npc');const bytes=c.getImageData(0,0,480,320).data;let n=0;for(let i=0;i<bytes.length;i+=4)if(bytes[i]===255&&bytes[i+1]===0&&bytes[i+2]===255)n++;return n;};
  return ['town','liarsville'].flatMap(id=>{s.scene=id;return scenes[id].map.objects.filter(o=>o.kind==='building').map(b=>({name:b.name,behind:count(b.x+Math.floor(b.w/2),b.y+b.rearDepth-1),front:count(b.x+Math.floor(b.w/2),b.y+b.h)}));});
 });
 for(const p of pixels){assert.ok(p.behind<p.front,JSON.stringify(p));assert.equal(p.front,2048,p.name);}
 checks.push('Actual renderer pixels: every roof occludes the actor behind it and every actor draws fully in front');
 await fixture('liarsville',8,6);await page.locator('#start').click();await page.locator('[data-action=save]').click();await page.reload();await page.locator('[data-action=continue]').click();
 const saved=await snap();assert.deepEqual([saved.player.x,saved.player.y],[8,6]);assert.equal(saved.money,11200);assert.equal(saved.debt,10000);assert.equal(saved.tank.gallons,25);checks.push('Save/reload behind Waterworks keeps position and gift/loan progress');
 assert.deepEqual(errors,[]);checks.push('No runtime exceptions or missing assets');
 await writeFile(`${out}/occlusion.json`,JSON.stringify(pixels,null,2)+'\n');
}finally{await writeFile(`${out}/report.json`,JSON.stringify({checks,errors},null,2)+'\n');await browser.close();}
