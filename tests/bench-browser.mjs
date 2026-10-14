import {createRequire} from 'node:module';import {mkdir,writeFile} from 'node:fs/promises';import assert from 'node:assert/strict';
import {newProject,placeObject,objectFootprint,exportProject,DIRS,SAVE_KEY} from '../map-editor/model.js';import {opposite} from '../src/bench-seat.js';
const require=createRequire(import.meta.url),{chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright'),url=process.env.TEST_URL||'http://127.0.0.1:5236',out=process.env.TEST_OUTPUT_DIR||'docs/reviews/M1-BN1';await mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE}),context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage(),checks=[],errors=[];
page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('favicon.ico'))errors.push(r.url());});
const inspect=()=>page.evaluate(async()=>(await import('/map-editor/editor.js')).inspect()),key=d=>'Arrow'+d[0].toUpperCase()+d.slice(1);
async function hold(dir,ms=600){await page.keyboard.down(key(dir));await page.waitForTimeout(ms);await page.keyboard.up(key(dir));await page.waitForTimeout(100);}
try{
 await page.goto(url+'/map-editor/?review=bench');await page.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));
 await page.evaluate(async()=>{window.__bench=await import('/map-editor/editor.js');});
 for(const facing of ['down','up','left','right']){
  const p=newProject(),m=p.maps[0],o=placeObject(m,facing==='down'?'bench':'bench-'+facing,5,5),r=objectFootprint(o),[dx,dy]=DIRS[facing],target={x:facing==='right'?r.x+r.w-1:r.x,y:facing==='down'?r.y+r.h-1:r.y};m.spawn={x:target.x+dx,y:target.y+dy};
  if(await page.locator('#project-panel').isVisible())await page.locator('#project-panel').click();await page.locator('#import').click();await page.locator('#data-text').fill(exportProject(p));await page.locator('#apply-import').click();await page.locator('#test').click();
  await page.keyboard.down(key(opposite(facing)));await page.waitForFunction(()=>Boolean(window.__bench.inspect().test.animation?.bench));
  await page.screenshot({path:out+'/hop-'+facing+'.png'});
  await page.waitForFunction(()=>Boolean(window.__bench.inspect().test.player.sitting));await page.keyboard.up(key(opposite(facing)));await page.waitForTimeout(100);
  let state=(await inspect()).test;assert.equal(state.player.facing,facing);assert.equal(state.player.x,target.x);assert.equal(state.player.y,target.y);
  await page.screenshot({path:out+'/seated-'+facing+'.png'});
  const visible=await page.locator('#play').evaluate((c,{state})=>{const {player}=state,camera=state.camera||{x:Math.max(0,Math.min(160,player.x*32+16-240)),y:Math.max(0,Math.min(320,player.y*32+32-160))},ctx=c.getContext('2d'),x=Math.round(player.x*32-camera.x),y=Math.round(player.y*32-42-camera.y),data=ctx.getImageData(x,y,32,64).data;let count=0;for(let i=0;i<data.length;i+=4)if(data[i]>80&&data[i]<200&&data[i+1]<110&&data[i+2]<90)count++;return count;},{state});assert.ok(visible>10,'Seated Hero skin remains visible in '+facing);

  for(const direction of Object.keys(DIRS).filter(d=>d!==facing)){await hold(direction,180);state=(await inspect()).test;assert.equal(state.player.sitting,true);assert.equal(state.player.facing,facing);assert.equal(state.player.x,target.x);assert.equal(state.player.y,target.y);}
  await hold(facing,450);state=(await inspect()).test;assert.equal(state.player.sitting,undefined);assert.deepEqual({x:state.player.x,y:state.player.y},m.spawn);
  await page.locator('#exit-test').click();assert.deepEqual((await inspect()).project.maps[0].spawn,m.spawn);checks.push(facing+' actual hop, seated lock, front exit and discarded playtest');
 }
 await page.evaluate(key=>localStorage.setItem(key,'bench-draft-sentinel'),SAVE_KEY);await page.goto(url+'/map-editor/?review=bench');await page.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));assert.equal(await page.evaluate(key=>localStorage.getItem(key),SAVE_KEY),'bench-draft-sentinel');
 await page.locator('.view-options summary').click();await page.locator('#grid').uncheck();await page.locator('.view-options summary').click();await page.screenshot({path:out+'/review-desktop.png'});await writeFile(out+'/review-native.png',Buffer.from((await page.locator('#map').evaluate(c=>c.toDataURL())).split(',')[1],'base64'));
 await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await page.locator('#open-build').click();await page.locator('[data-tab=stamps]').click();await page.locator('#toolbox-search').fill('bench');assert.equal(await page.locator('[data-stamp]:visible').count(),4);await page.screenshot({path:out+'/review-phone.png',fullPage:true});checks.push('390px all four searchable stamps, no horizontal overflow; review retains draft');
 assert.deepEqual(errors,[]);checks.push('No runtime errors or missing art');
}finally{await writeFile(out+'/browser-checks.json',JSON.stringify({checks,errors},null,2)+'\n');await browser.close();}
console.log(checks);
