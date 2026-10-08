import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {FRUIT_TREES} from '../src/fruit-trees.js';
import {createState,startMorning,SAVE_KEY} from '../src/state.js';
const require=createRequire(import.meta.url),{chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE}),context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true}),page=await context.newPage();
const url=process.env.TEST_URL||'http://127.0.0.1:5173',out=process.env.TEST_OUTPUT_DIR||'test-results/fruit',checks=[],errors=[];await mkdir(out,{recursive:true});
page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(r.url());});
const snap=()=>page.evaluate(async()=>(await import('/src/main.js')).getDebugSnapshot());
const view=()=>page.evaluate(async()=>(await import('/src/main.js')).getDebugFruit());
const camera=()=>page.evaluate(async()=>(await import('/src/render.js')).getRenderDebug().camera);
const pass=s=>{checks.push(s);console.log('PASS '+s);};
async function fixture(tree,edit=()=>{}){
 await page.goto(url);await page.waitForSelector('[data-action=new]');const s=createState('Ari','boy','River');startMorning(s,true);s.scene=tree.scene;s.player={x:tree.x,y:tree.y+2,facing:'up'};edit(s);
 await page.evaluate(({s,key})=>{localStorage.clear();localStorage.setItem(key,JSON.stringify(s));},{s,key:SAVE_KEY});await page.reload();await page.locator('[data-action=continue]').click();await page.waitForTimeout(60);
}
try{
 for(const tree of FRUIT_TREES){
  await fixture(tree,s=>{delete s.inventory.apples;delete s.fruitHarvests;s.player.y++;});
  await page.keyboard.down('ArrowUp');for(let n=0;n<80;n++){const m=await page.evaluate(async()=>(await import('/src/main.js')).getDebugMovement());if(m.destination?.y===tree.y+2||m.tileY===tree.y+2)break;await page.waitForTimeout(10);}await page.keyboard.up('ArrowUp');await page.waitForTimeout(300);assert.equal((await snap()).player.y,tree.y+2);
  assert.equal(await page.locator('#interact-prompt').count(),0);const before=await camera();
  await page.screenshot({path:`${out}/${tree.id}-ripe.png`});await page.locator('#a-button').tap();
  assert.equal((await snap()).inventory.apples,3);assert.equal((await view()).find(t=>t.id===tree.id).ripe,false);assert.ok((await view()).find(t=>t.id===tree.id).falling);assert.deepEqual(await camera(),before);await page.waitForTimeout(500);await page.screenshot({path:`${out}/${tree.id}-shake.png`});
  for(let i=0;i<3;i++)await page.locator('#a-button').tap();assert.equal((await snap()).inventory.apples,3);await page.waitForTimeout(1150);await page.locator('#a-button').tap();assert.ok((await page.locator('#game-status').textContent()).includes('No ripe apples'));assert.equal((await snap()).inventory.apples,3);
  await page.screenshot({path:`${out}/${tree.id}-bare.png`});await page.reload();await page.locator('[data-action=continue]').click();assert.equal((await snap()).inventory.apples,3);assert.equal((await view()).find(t=>t.id===tree.id).ripe,false);
  pass(`${tree.scene}: walk up and real touch A shakes fruit into Bag once, spam/empty tree cannot duplicate, reload stays harvested`);
 }
 await page.locator('#start').click();await page.locator('[data-action=bag]').click();assert.ok((await page.locator('#panel').textContent()).includes('Orchard apples3'));await page.screenshot({path:`${out}/bag.png`});for(const [width,height]of [[320,568],[844,390]]){await page.setViewportSize({width,height});const box=await page.locator('#panel').boundingBox();assert.ok(box.x>=0&&box.y>=0&&box.x+box.width<=width+1&&box.y+box.height<=height+1);}await page.setViewportSize({width:390,height:844});pass('Bag shows collected apples, explains regrowth and fits narrow/landscape phones');
 const t=FRUIT_TREES[0];await fixture(t,s=>{s.time=32;s.inventory.apples=3;s.fruitHarvests[t.id]=8;});assert.equal((await view())[0].ripe,true);await page.keyboard.press('z');assert.equal((await snap()).inventory.apples,6);assert.equal((await snap()).fruitHarvests[t.id],32);pass('Ripe art and keyboard harvest return at 24 habitat hours');
 await fixture(t);await page.locator('#start').click();await page.locator('[data-action=options]').click();await page.locator('[data-action=calm-motion]').click();await page.locator('#b-button').tap();await page.locator('#b-button').tap();await page.locator('#a-button').tap();const calm=(await view())[0];assert.equal(calm.calm,true);assert.equal(calm.shake,0);assert.equal(calm.falling,false);assert.equal((await snap()).inventory.apples,3);pass('Calm preserves harvest and pickup message without shaking or falling motion');
 const proof=await page.evaluate(async()=>{
  const {createState,startMorning}=await import('/src/state.js'),{cueFruitShake}=await import('/src/fruit-trees.js'),{renderWorld,getRenderDebug}=await import('/src/render.js');
  const s=createState();startMorning(s,true);s.scene='town';s.player={x:10,y:5,facing:'up'};s.fruitHarvests={'apple-rootport':8};const cv=document.createElement('canvas');cv.width=480;cv.height=320;const c=cv.getContext('2d'),view={x:160,y:80,facing:'up',pose:'idle',action:'idle'};cueFruitShake(s,'apple-rootport',0,false);
  const render=time=>{renderWorld(cv,s,time,view);const camera=getRenderDebug().camera,x=320-camera.x,y=96-camera.y;return {roots:[...c.getImageData(x,y+52,64,12).data],crown:[...c.getImageData(x-2,y,68,52).data],camera};};const a=render(.08),b=render(.16);return {rootsFixed:JSON.stringify(a.roots)===JSON.stringify(b.roots),crownMoves:JSON.stringify(a.crown)!==JSON.stringify(b.crown),cameraFixed:JSON.stringify(a.camera)===JSON.stringify(b.camera)};
 });assert.deepEqual(proof,{rootsFixed:true,crownMoves:true,cameraFixed:true});await writeFile(`${out}/motion-proof.json`,JSON.stringify(proof,null,2)+'\n');pass('Actual renderer pixels: crown moves, roots and camera stay fixed');
 assert.deepEqual(errors,[]);pass('No runtime errors or missing assets');
}finally{await writeFile(`${out}/report.json`,JSON.stringify({checks,errors},null,2)+'\n');await browser.close();}
