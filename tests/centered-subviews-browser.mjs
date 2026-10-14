import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {createRequire} from 'node:module';
import {createState,startMorning,SAVE_KEY} from '../src/state.js';
import {newProject,placeObject,exportProject,SAVE_KEY as MAP_KEY} from '../map-editor/model.js';
const {chromium}=createRequire(import.meta.url)(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const url=process.env.TEST_URL||'http://127.0.0.1:5228',out=process.env.TEST_OUTPUT_DIR||'docs/reviews/M1-TN2/subviews';await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE}),checks=[],errors=[],measurements=[];
const pass=s=>{checks.push(s);console.log('PASS '+s);};
try{
 for(const worldZoom of [0,1,2]){
  const context=await browser.newContext({viewport:{width:390,height:844},hasTouch:true,reducedMotion:'reduce'}),page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('favicon.ico'))errors.push(r.url());});
  const state=createState('Ari','girl','River');startMorning(state,true);state.scene='town';state.player={x:21,y:26,facing:'down'};
  const project=newProject();project.maps[0].spawn={x:9,y:9};placeObject(project.maps[0],'bear',8,8);
  await context.addInitScript(({state,project,worldZoom,saveKey,mapKey})=>{if(sessionStorage.getItem('fixture'))return;sessionStorage.setItem('fixture','1');localStorage.setItem(saveKey,JSON.stringify(state));localStorage.setItem(mapKey,project);localStorage.setItem('critz-tycoon.ui.v1',JSON.stringify({frame:'leaf',calm:true,worldZoom}));localStorage.setItem('critz-tycoon.audio.v1',JSON.stringify({enabled:false,volume:0}));},{state,project:exportProject(project),worldZoom,saveKey:SAVE_KEY,mapKey:MAP_KEY});
  await page.goto(url);await page.locator('[data-action=continue]').click();
  for(const action of ['greenhouse','coast','map-player']){
   await page.locator('#start').click();await page.locator(`[data-action=${action}]`).click();await page.locator('iframe.game-room').waitFor();
   // Sites canonicalizes HTML URLs without the suffix; wait for navigation
   // by page path rather than requiring the local server's exact URL spelling.
   let frame;for(let i=0;i<1500;i++){frame=page.frames().find(f=>f!==page.mainFrame()&&f.url().includes(action==='map-player'?'/map-editor/':`/art-review/${action}`));if(frame)break;await page.waitForTimeout(20);}assert.ok(frame);
   if(action==='greenhouse'){
    await frame.locator('#begin').waitFor();await frame.waitForFunction(()=>!document.querySelector('#begin').disabled);
    const check=async()=>{const d=await frame.evaluate(async()=>{const s=(await import('/art-review/greenhouse.js')).getReviewSnapshot(),c=document.querySelector('#world');return {...s,width:c.width,height:c.height};});assert.equal(Math.round(d.player.x*32+16)-d.camera.x,d.width/2);assert.equal(Math.round(d.player.y*32+32)-23-d.camera.y,d.height/2);return d;};
    await frame.waitForTimeout(60);await check();await frame.locator('#begin').click();await frame.waitForTimeout(120);assert.equal((await check()).scene,'inside');
   }else if(action==='coast'){
    await frame.locator('#coast').waitFor();
    let result;
    for(let i=0;i<150;i++){
     result=await frame.evaluate(async()=>{const {getCoastReview}=await import('/art-review/coast.js'),{worldViewport}=await import('/src/world-space.js');const d=getCoastReview(),c=document.querySelector('#coast'),r=c.parentElement.getBoundingClientRect(),f=worldViewport(r.width,r.height,JSON.parse(localStorage.getItem('critz-tycoon.ui.v1')).worldZoom);return {ready:d.ready,width:c.width,height:c.height,expected:[f.width,f.height],hero:d.hero,camera:d.camera,gender:d.state.gender};});
     if(result.ready&&result.hero.y-(result.gender==='girl'?23:21)-result.camera.y===result.height/2)break;
     await page.waitForTimeout(20);
    }
    assert.deepEqual([result.width,result.height],result.expected);assert.equal(result.gender,'girl');assert.equal(result.hero.y-23-result.camera.y,result.height/2,JSON.stringify(result));
   }else{
    await frame.locator('#test-dialog[open]').waitFor();
    const d=await frame.evaluate(async()=>{const {inspect}=await import('/map-editor/editor.js'),{mapCamera}=await import('/map-editor/authoring.js'),{worldViewport}=await import('/src/world-space.js');const s=inspect(),c=document.querySelector('#play'),r=document.querySelector('#play-view').getBoundingClientRect(),f=worldViewport(r.width,r.height,JSON.parse(localStorage.getItem('critz-tycoon.ui.v1')).worldZoom),p=s.test.player,m=s.project.maps.find(m=>m.id===s.test.map);return {width:c.width,height:c.height,expected:[f.width,f.height],player:p,camera:s.test.camera,bear:m.objects.find(o=>o.type==='bear')};});assert.deepEqual([d.width,d.height],d.expected);assert.equal(d.player.x*32+16-d.camera.x,d.width/2);assert.equal(d.player.y*32+32-21-d.camera.y,d.height/2);assert.ok(d.bear);
    // Independent editor/runtime draw calls must produce exactly the same bear.
    const parity=await frame.evaluate(async()=>{const {MapRenderer}=await import('/map-editor/render.js'),{drawBear}=await import('/src/bear-art.js');const r=new MapRenderer();await r.load();const a=document.createElement('canvas'),b=document.createElement('canvas');a.width=b.width=a.height=b.height=96;r.drawObject(a.getContext('2d'),{type:'bear',x:0,y:1});drawBear(b.getContext('2d'),0,1);const pa=a.getContext('2d').getImageData(0,0,96,96).data,pb=b.getContext('2d').getImageData(0,0,96,96).data;return {equal:pa.every((v,i)=>v===pb[i]),uri:a.toDataURL()};});assert.ok(parity.equal);await fs.writeFile(`${out}/bear-editor-native-zoom${worldZoom+1}.png`,Buffer.from(parity.uri.split(',')[1],'base64'));
   }
   await page.screenshot({path:`${out}/${action}-zoom${worldZoom+1}.png`});await page.locator('#b-button').click();
  }
  pass(`Adventure greenhouse outside/inside,coast and Map Studio centered atzoom${worldZoom+1};editor/native bear pixels exact`);
  const timings=await page.evaluate(async()=>{const {renderWorld}=await import('/src/render.js'),{getDebugSnapshot,getDebugMovement}=await import('/src/main.js');const s=getDebugSnapshot(),v=getDebugMovement(),c=document.querySelector('#world'),samples=[];for(let i=0;i<120;i++){const start=performance.now();renderWorld(c,s,i/60,v);samples.push(performance.now()-start);}samples.sort((a,b)=>a-b);return {median:samples[60],p95:samples[114],width:c.width,height:c.height,scope:'120 synchronous warm renderer calls on host Chrome; not physical phone FPS'};});measurements.push({worldZoom,...timings});assert.ok(timings.p95<1000,'Renderer hangs');
  await context.close();
 }
 assert.deepEqual(errors,[]);pass('No subview runtime errors or missing assets');
}finally{await fs.writeFile(`${out}/browser-checks.json`,JSON.stringify({task:'M1.TN2',url,checks,errors,measurements,physicalSafari:false},null,2)+'\n');await browser.close();}
