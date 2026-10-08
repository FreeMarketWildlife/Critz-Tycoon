import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {createState,startMorning,SAVE_KEY} from '../src/state.js';
const require=createRequire(import.meta.url),{chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE});
const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
const page=await context.newPage(),errors=[],checks=[],out=process.env.TEST_OUTPUT_DIR||'test-results/stairs';
await mkdir(out,{recursive:true});
page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(r.url());});
const snapshot=()=>page.evaluate(async()=> (await import('/src/main.js')).getDebugSnapshot());
const pass=s=>{checks.push(s);console.log('PASS '+s);};
async function fixture(scene,x,y,facing='up'){
 await page.goto(process.env.TEST_URL||'http://127.0.0.1:5173');await page.waitForSelector('[data-action=new]');
 const s=createState('Ari','boy','River');startMorning(s,true);s.scene=scene;s.player={x,y,facing};
 await page.evaluate(({s,key})=>{localStorage.clear();localStorage.setItem(key,JSON.stringify(s));},{s,key:SAVE_KEY});
 await page.reload();await page.locator('[data-action=continue]').click();return s;
}
async function hold(key,ms=650){await page.keyboard.down(key);await page.waitForTimeout(ms);await page.keyboard.up(key);await page.waitForTimeout(100);}
try{
 for(const [scene,y]of [['bedroom',10],['house',3]]){
  await fixture(scene,12,y,'right');await hold('ArrowRight');assert.deepEqual((await snapshot()).player,{x:12,y,facing:'right'});
  await page.locator('#a-button').click();assert.equal((await snapshot()).scene,scene);
  await fixture(scene,14,y+1,'up');await page.screenshot({path:`${out}/${scene}-landing.png`});
  await page.keyboard.down('ArrowUp');await page.waitForTimeout(90);assert.equal((await snapshot()).scene,scene);
  await page.keyboard.up('ArrowUp');await page.waitForTimeout(600);
  const s=await snapshot(),to=scene==='bedroom'?'house':'bedroom';assert.equal(s.scene,to);
  assert.deepEqual(s.player,{x:14,y:to==='house'?4:11,facing:'down'});
  await page.waitForTimeout(500);assert.equal((await snapshot()).scene,to);
  pass(`${scene}: side collision/A cannot cross rails; committed entrance step travels once to a clear landing`);
 }
 await fixture('bedroom',14,8,'down');await hold('ArrowDown');assert.deepEqual((await snapshot()).player,{x:14,y:8,facing:'down'});pass('Bedroom stair back blocks entry from the north');
 await fixture('bedroom',13,10);assert.deepEqual((await snapshot()).player,{x:14,y:11,facing:'up'});
 await page.locator('#start').click();await page.locator('[data-action=save]').click();
 await page.reload();await page.locator('[data-action=continue]').click();const recovered=await snapshot();
 assert.equal(recovered.money,11200);assert.equal(recovered.debt,10000);assert.equal(recovered.tankOwned,true);assert.equal(recovered.tank.gallons,25);
 assert.deepEqual([recovered.player.x,recovered.player.y],[14,11]);pass('Old save on the stair side recovers, saves and reloads on the landing with gift/loan progress intact');
 await page.locator('#a-button').click();await page.waitForTimeout(400);assert.equal((await snapshot()).scene,'house');pass('A at the correct landing remains an accessible stair shortcut');
 assert.deepEqual(errors,[]);pass('No runtime exceptions or missing assets');
}finally{await writeFile(`${out}/report.json`,JSON.stringify({checks,errors},null,2)+'\n');await browser.close();}
