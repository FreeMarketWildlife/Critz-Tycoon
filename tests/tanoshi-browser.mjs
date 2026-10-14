// Production build, real UI, and isolated synthetic browser storage only.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {createRequire} from 'node:module';
import {createState,startMorning,SAVE_KEY} from '../src/state.js';
import {TANOSHI} from '../src/tanoshi.js';
const require=createRequire(import.meta.url),{chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const base=process.env.TEST_URL||'http://127.0.0.1:5228',out=process.env.TEST_OUTPUT_DIR||'docs/reviews/M1-TN1';
await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE}),context=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce',hasTouch:true}),page=await context.newPage(),checks=[],errors=[];
page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('favicon.ico'))errors.push(r.url());});
const pass=message=>{checks.push(message);console.log('PASS '+message);};
const snapshot=()=>page.evaluate(async()=> (await import('/src/main.js')).getDebugSnapshot());
async function fixture(t,night=false){const s=createState('Ari','boy','River');if(!night)startMorning(s,true);s.scene=t.scene;s.player={x:t.x+1,y:t.y,facing:'left'};if(!night)s.dayClock={day:1,minute:720,remainder:0};await page.goto(base);await page.waitForSelector('[data-action=new]');await page.evaluate(({s,key})=>{localStorage.clear();localStorage.setItem(key,JSON.stringify(s));localStorage.setItem('critz-tycoon.audio.v1',JSON.stringify({enabled:false,volume:0}));localStorage.setItem('critz-tycoon.ui.v1',JSON.stringify({frame:'leaf',calm:true}));},{s,key:SAVE_KEY});await page.reload();await page.locator('[data-action=continue]').click();if(night){await dismiss();await approachBlush();}return s;}
async function approachBlush(){await page.keyboard.down('ArrowLeft');for(let i=0;i<100&&(await snapshot()).player.x>6;i++)await page.waitForTimeout(10);await page.keyboard.up('ArrowLeft');for(let i=0;i<50&&!await page.evaluate(async()=> (await import('/src/main.js')).getDebugMovement().settled);i++)await page.waitForTimeout(10);assert.equal((await snapshot()).player.x,6);}
async function dismiss(){for(let i=0;i<30&&await page.locator('#dialogue').isVisible();i++)await page.locator('#a-button').click();assert.equal(await page.locator('#dialogue').isVisible(),false);}
try{
  for(const [w,h]of [[320,568],[390,844],[844,390],[1280,900]]){
    await page.setViewportSize({width:w,height:h});await fixture(TANOSHI[0],true);
    const before=await page.locator('#world').evaluate(c=>({width:c.width,height:c.height,uri:c.toDataURL()}));
    await page.screenshot({path:`${out}/opening-${w}.png`});
    assert.equal((await snapshot()).player.x,6);
    await page.locator('#a-button').click();assert.equal(await page.locator('#speaker').textContent(),'Found a Tanoshi!');
    assert.equal(await page.locator('#dialogue-accessible').textContent().then(s=>s.includes('Tanoshi')),true);
    const box=await page.locator('#dialogue-next').boundingBox();assert.ok(box.width>=44&&box.height>=44);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
    assert.deepEqual(await page.locator('#world').evaluate(c=>({width:c.width,height:c.height})),{width:before.width,height:before.height});
    await page.locator('#dialogue-next').click();await page.screenshot({path:`${out}/greeting-${w}.png`});await dismiss();
    assert.deepEqual((await snapshot()).tanoshiDiscoveries,['tanoshi-blush']);
    await page.reload();await page.locator('[data-action=continue]').click();assert.deepEqual((await snapshot()).tanoshiDiscoveries,['tanoshi-blush']);await dismiss();await approachBlush();
    await page.locator('#a-button').click();assert.equal(await page.locator('#speaker').textContent(),'Blush Tanoshi');await dismiss();
    await page.keyboard.press('p');await page.locator('[data-action=notebook]').click();assert.ok((await page.locator('#panel').textContent()).includes('Tanoshi greetings · 1/3'));assert.ok((await page.locator('#panel').textContent()).includes('Blush Tanoshi · Shy'));
    if(w===390){await page.locator('#panel h3').filter({hasText:'Tanoshi greetings'}).scrollIntoViewIfNeeded();await page.screenshot({path:`${out}/notebook-phone.png`});}
    pass(`Opening greeting/revisit/Notebook/reload and stable44px dialogue at ${w}×${h}`);
  }
  await page.setViewportSize({width:390,height:844});
  for(const t of TANOSHI.slice(1)){const old=await fixture(t);await page.screenshot({path:`${out}/${t.variant}-phone.png`});await fs.writeFile(`${out}/${t.variant}-world.png`,Buffer.from((await page.locator('#world').evaluate(c=>c.toDataURL())).split(',')[1],'base64'));await page.locator('#a-button').click();assert.equal(await page.locator('#speaker').textContent(),'Found a Tanoshi!');await dismiss();const after=await snapshot();for(const key of ['money','debt','flags','inventory','tankOwned','hero','rival'])assert.deepEqual(after[key],old[key]);assert.deepEqual(after.tanoshiDiscoveries,[t.id]);pass(`${t.name} visible/interactable in ${t.scene}; story/economy preserved`);}
  await fixture(TANOSHI[1]);
  const oldSave=await page.evaluate(key=>localStorage.getItem(key),SAVE_KEY);
  await page.evaluate(key=>{window.tanoshiTestSetItem=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k===key)throw Error('Synthetic quota failure');return window.tanoshiTestSetItem.call(this,k,v);};},SAVE_KEY);
  await page.locator('#a-button').click();const messages=[];
  for(let i=0;i<30&&await page.locator('#dialogue').isVisible();i++){messages.push(await page.locator('#dialogue-accessible').textContent());await page.locator('#a-button').click();}
  assert.ok(messages.some(s=>s.includes('Saving failed')));assert.equal(await page.evaluate(key=>localStorage.getItem(key),SAVE_KEY),oldSave);
  await page.evaluate(()=>{Storage.prototype.setItem=window.tanoshiTestSetItem;delete window.tanoshiTestSetItem;});await page.keyboard.press('p');await page.locator('[data-action=save]').click();assert.deepEqual(await page.evaluate(key=>JSON.parse(localStorage.getItem(key)).tanoshiDiscoveries,SAVE_KEY),['tanoshi-mint']);
  pass('Failed discovery save preserves prior bytes, reports failure, and retries through existing Save');
  // Real new-game sequence, not just a positioned save fixture.
  await page.goto(base);await page.evaluate(()=>localStorage.clear());await page.reload();await page.locator('[data-action=new]').click();await page.locator('#hero-name').fill('Ari');await page.locator('#rival-name').fill('River');await page.locator('[data-action=begin]').click();await dismiss();await page.screenshot({path:`${out}/actual-new-game.png`});assert.ok((await page.evaluate(async()=> (await import('/src/main.js')).getDebugEntities())).some(e=>e.id==='tanoshi-blush'));
  const art=await page.evaluate(async()=>{const data=await (await fetch('/assets/playable/tanoshi/atlas.json')).json();const img=new Image();img.src='/assets/playable/tanoshi/atlas.png';await img.decode();const c=document.createElement('canvas');c.width=96;c.height=32;const ctx=c.getContext('2d');ctx.drawImage(img,0,0);const rgba=ctx.getImageData(0,0,96,32).data;return {size:[img.width,img.height],anchors:data.assets.map(a=>a.anchor),alphas:[...new Set(Array.from(rgba).filter((v,i)=>i%4===3))].sort((a,b)=>a-b)};});assert.deepEqual(art,{size:[96,32],anchors:[[16,32],[16,32],[16,32]],alphas:[0,255]});
  pass('Actual new-game opening contains Tanoshi; native atlas/anchors/binary alpha loaded');
  assert.deepEqual(errors,[]);pass('No runtime exceptions or missing assets');
}finally{await fs.writeFile(`${out}/browser-checks.json`,JSON.stringify({task:'M1.TN1',url:base,checks,errors,physicalSafari:false},null,2)+'\n');await browser.close();}
