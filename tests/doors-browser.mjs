import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {createState,startMorning,SAVE_KEY} from '../src/state.js';
import {scenes} from '../src/world.js';
const require=createRequire(import.meta.url),{chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE});
const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
const page=await context.newPage(),touch=await context.newCDPSession(page),errors=[],checks=[],out=process.env.TEST_OUTPUT_DIR||'test-results/doors';
await mkdir(out,{recursive:true});page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(r.url());});
const snapshot=()=>page.evaluate(async()=> (await import('/src/main.js')).getDebugSnapshot());
const delta={up:[0,-1],down:[0,1],left:[-1,0],right:[1,0]};
async function fixture(scene,player){
 await page.goto(process.env.TEST_URL||'http://127.0.0.1:5173');await page.waitForSelector('[data-action=new]');
 const s=createState('Ari','girl','River');startMorning(s,true);s.scene=scene;s.player=player;
 await page.evaluate(({s,key})=>{localStorage.clear();localStorage.setItem(key,JSON.stringify(s));},{s,key:SAVE_KEY});await page.reload();await page.locator('[data-action=continue]').click();
}
try{
 for(const [id,scene]of Object.entries(scenes))for(const e of scene.entities.filter(e=>e.type==='door')){
  const [dx,dy]=delta[e.entryFacing];await fixture(id,{x:e.x-dx,y:e.y-dy,facing:e.entryFacing});
  await page.waitForFunction(()=>document.getElementById('interact-prompt').textContent.startsWith('Walk '));
  assert.equal(await page.locator('#interact-prompt b').count(),0);
  if(id==='yard')await page.screenshot({path:`${out}/yard-${e.id}.png`});
  // Touch D-pad for both previously blocked yard entrances; keyboard elsewhere.
  const key='Arrow'+e.entryFacing[0].toUpperCase()+e.entryFacing.slice(1);
  if(id==='yard'){
   const box=await page.locator(`[data-dir=${e.entryFacing}]`).boundingBox();
   await touch.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:box.x+box.width/2,y:box.y+box.height/2}]});
  }else await page.keyboard.down(key);
  await page.waitForTimeout(90);assert.equal((await snapshot()).scene,id,'finish entrance step before travel');
  if(id==='yard')await touch.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});else await page.keyboard.up(key);
  for(let n=0;n<50&&(await snapshot()).scene!==e.to;n++)await page.waitForTimeout(30);
  assert.equal((await snapshot()).scene,e.to);
  const after=await snapshot();assert.equal(after.money,11200);assert.equal(after.debt,10000);assert.equal(after.tank.gallons,25);
  assert.equal((await page.evaluate(async()=> (await import('/src/main.js')).getDebugUI())).panel,'');
  await page.waitForTimeout(220);assert.equal((await snapshot()).scene,e.to,'no return bounce');
  checks.push(`${id}/${e.id} → ${e.to}: movement only, no A/confirmation, safe arrival`);console.log('PASS '+checks.at(-1));
 }
 await fixture('town',{x:6,y:22,facing:'right'});await page.keyboard.down('ArrowRight');await page.waitForTimeout(90);await page.keyboard.up('ArrowRight');await page.waitForTimeout(350);assert.equal((await snapshot()).scene,'town');assert.deepEqual([(await snapshot()).player.x,(await snapshot()).player.y],[7,22]);checks.push('Crossing a storefront sideways does not enter');
 assert.deepEqual(errors,[]);checks.push('No browser exceptions or missing assets');
}finally{await writeFile(`${out}/report.json`,JSON.stringify({checks,errors},null,2)+'\n');await browser.close();}
