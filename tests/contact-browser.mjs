import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {createState,startMorning,SAVE_KEY} from '../src/state.js';
import {scenes,isBlocked} from '../src/world.js';
const require=createRequire(import.meta.url),{chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE}),context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true}),page=await context.newPage();
const checks=[],errors=[],out=process.env.TEST_OUTPUT_DIR||'test-results/contact',url=process.env.TEST_URL||'http://127.0.0.1:5173';await mkdir(out,{recursive:true});
page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(r.url());});
const snap=()=>page.evaluate(async()=>(await import('/src/main.js')).getDebugSnapshot());
const motion=()=>page.evaluate(async()=>(await import('/src/main.js')).getDebugMovement());
const rendered=()=>page.evaluate(async()=>(await import('/src/render.js')).getRenderDebug());
const pass=s=>{checks.push(s);console.log('PASS '+s);};
async function fixture(scene,x,y,facing='up'){
 await page.goto(url);await page.waitForSelector('[data-action=new]');const s=createState('Ari','boy','River');startMorning(s,true);s.scene=scene;s.player={x,y,facing};
 await page.evaluate(({s,key})=>{localStorage.clear();localStorage.setItem(key,JSON.stringify(s));},{s,key:SAVE_KEY});await page.reload();await page.locator('[data-action=continue]').click();await page.waitForTimeout(70);
}
async function stable(camera){const samples=await page.evaluate(async()=>{const {getRenderDebug}=await import('/src/render.js'),rows=[];for(let i=0;i<12;i++){await new Promise(requestAnimationFrame);rows.push(getRenderDebug().camera);}return rows;});for(const c of samples)assert.deepEqual(c,camera);}
try{
 for(const [width,height]of [[320,568],[390,844],[844,390],[1280,900]]){
  await page.setViewportSize({width,height});
  for(const [scene,x,y]of [['house',5,7],['town',22,25]]){
   await fixture(scene,x,y);const camera=(await rendered()).camera,box=await page.locator('#world').boundingBox();
   await page.locator('#a-button').click();assert.ok(await page.locator('#dialogue').isVisible());await stable(camera);
   const d=await page.locator('#dialogue').boundingBox(),button=await page.locator('#dialogue-next').boundingBox();assert.ok(d.x>=0&&d.y>=0&&d.x+d.width<=width+1&&d.y+d.height<=height+1);assert.ok(button.width>=44&&button.height>=44);assert.deepEqual(await page.locator('#world').boundingBox(),box);
   const data=await rendered();const heroY=box.y+(data.playerFoot.y-camera.y)*box.width/480;assert.ok(heroY<d.y,`Hero feet covered at ${width}: ${heroY} >= ${d.y}`);
   await page.screenshot({path:`${out}/dialogue-${scene}-${width}.png`});
   for(let n=0;n<80&&await page.locator('#dialogue').isVisible();n++){await page.locator('#a-button').click();assert.deepEqual((await rendered()).camera,camera);}
   assert.equal(await page.locator('#dialogue').isVisible(),false);await stable(camera);assert.deepEqual(await page.locator('#world').boundingBox(),box);
   pass(`${scene} ${width}×${height}: opening, typing, paging and closing speech keep camera/layout fixed; text, actor and touch target fit`);
  }
 }
 await page.setViewportSize({width:390,height:844});
 const tree=scenes.forest.objects.find(o=>o.kind==='tree'&&!isBlocked('forest',o.x-1,o.y+o.h-1));
 for(const [label,scene,x,y,dir]of [['left-wall','house',1,8,'left'],['right-wall','house',15,8,'right'],['north-wall','house',8,3,'up'],['south-wall','house',10,11,'down'],['table','house',5,8,'right'],['building','town',3,9,'right'],['roots','forest',tree.x-1,tree.y+tree.h-1,'right']]){
  await fixture(scene,x,y,dir);const before=await snap(),camera=(await rendered()).camera;await page.keyboard.down('Arrow'+dir[0].toUpperCase()+dir.slice(1));await page.waitForTimeout(150);assert.equal((await motion()).action,'blocked');assert.deepEqual((await snap()).player,before.player);assert.deepEqual((await rendered()).camera,camera);await page.keyboard.up('Arrow'+dir[0].toUpperCase()+dir.slice(1));await page.waitForTimeout(60);assert.equal((await motion()).action,'idle');
  assert.deepEqual((await rendered()).playerFoot,{x:x*32+16,y:y*32+32});await page.screenshot({path:`${out}/contact-${label}.png`});
  await writeFile(`${out}/contact-${label}-native.png`,Buffer.from(await page.locator("#world").evaluate(c=>c.toDataURL("image/png").split(",")[1]),"base64"));
  pass(`${label}: contact blocks correctly without camera displacement; releasing input immediately rests`);
 }
 // Save state still uses original integer cells; visual anchor changes need no migration.
 await fixture('house',15,8,'right');await page.locator('#start').click();await page.locator('[data-action=save]').click();await page.reload();await page.locator('[data-action=continue]').click();const s=await snap();assert.deepEqual(s.player,{x:15,y:8,facing:'right'});assert.equal(s.money,11200);assert.equal(s.debt,10000);assert.equal(s.tank.gallons,25);pass('Save/reload keeps exact cell, gift, loan and money');
 assert.deepEqual(errors,[]);pass('No missing assets or browser exceptions');
}finally{await writeFile(`${out}/report.json`,JSON.stringify({checks,errors},null,2)+'\n');await browser.close();}
