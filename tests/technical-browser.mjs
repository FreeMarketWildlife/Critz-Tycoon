import assert from 'node:assert/strict';import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';import {execFileSync} from 'node:child_process';
import {createState,startMorning,SAVE_KEY} from '../src/state.js';
const require=createRequire(import.meta.url),{chromium}=require((process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES||'/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules')+'/playwright');
const base=process.env.TEST_URL||'http://127.0.0.1:5221',out=process.env.TEST_OUTPUT_DIR||'test-results/technical',fixed=process.env.EXPECT_FIXES!=='0';
await mkdir(out,{recursive:true});const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const checks=[],errors=[],measurements={};const pass=s=>{checks.push(s);console.log('PASS '+s);};
const watch=p=>p.on('pageerror',e=>errors.push(e.message));
const inspect=p=>p.evaluate(async()=>(await import('/map-editor/editor.js')).inspect());
const motion=p=>p.evaluate(async()=>(await import('/src/main.js')).getDebugMovement());
async function hidden(p,value){await p.evaluate(value=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>value});Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>value?'hidden':'visible'});document.dispatchEvent(new Event('visibilitychange'));},value);}
async function startStep(p,key,read){await p.keyboard.down(key);await p.waitForFunction(async()=>{const m=location.pathname.includes('map-editor')?(await import('/map-editor/editor.js')).inspect().test.motion:(await import('/src/main.js')).getDebugMovement();return m.action==='walk'&&!m.settled;});return read(p);}
try{
 // Reproduce lost keyboard/touch ownership using actual browser touch events.
 const c=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true}),p=await c.newPage();watch(p);
 const state=createState('Technical Hero','boy','River');startMorning(state,true);state.gridVersion=1;state.scene='bedroom';state.player={x:4,y:8,facing:'right'};
 await c.addInitScript(({key,state})=>{if(!sessionStorage.getItem('fixture')){localStorage.setItem(key,JSON.stringify(state));sessionStorage.setItem('fixture','1');}}, {key:SAVE_KEY,state});
 await p.goto(base);await p.locator('[data-action=continue]').click();await startStep(p,'ArrowRight',motion);
 const cd=await c.newCDPSession(p),button=await p.locator('.right').boundingBox();
 await cd.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:button.x+button.width/2,y:button.y+button.height/2}]});
 await cd.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
 await p.waitForTimeout(600);const result=await motion(p);measurements.gameAfterTouchRelease={tileX:result.tileX,heldKeyboardStillMoves:result.tileX>=6};
 assert.equal(measurements.gameAfterTouchRelease.heldKeyboardStillMoves,fixed);await p.keyboard.up('ArrowRight');
 pass(fixed?'Releasing a real touch leaves the independently held keyboard direction active':'Baseline reproduces touch release canceling a held keyboard direction');await c.close();

 const editorContext=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 await editorContext.addInitScript(()=>{window.__frameCallbacks=0;const raf=requestAnimationFrame;window.requestAnimationFrame=fn=>raf(now=>{window.__frameCallbacks++;fn(now);});});
 const editor=await editorContext.newPage();watch(editor);await editor.goto(base+'/map-editor/');await editor.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));
 const first=await editor.evaluate(()=>window.__frameCallbacks);await editor.waitForTimeout(300);const idle=(await editor.evaluate(()=>window.__frameCallbacks))-first;measurements.editorIdleCallbacks300ms=idle;assert.equal(idle===0,fixed);pass(fixed?'Static Map Studio schedules no animation frames while idle':'Baseline reproduces continuously scheduled idle Map Studio frames');
 // Import a clear, bounded synthetic map so no real draft or map layout participates.
 const fixture=await editor.evaluate(async()=>{const {newProject,exportProject}=await import('/map-editor/model.js');const p=newProject();p.maps[0].spawn={x:4,y:8};return exportProject(p);});
 await editor.locator('#import').click();await editor.locator('#data-text').fill(fixture);await editor.locator('#apply-import').click();await editor.waitForSelector('#data-dialog',{state:'hidden'});
 await editor.locator('#test').click();await editor.keyboard.down('ArrowRight');
 // Hide in the same browser callback that observes the committed step; a
 // separate protocol roundtrip can otherwise see a later idle boundary.
 await editor.evaluate(async()=>{
  const {inspect}=await import('/map-editor/editor.js');
  await new Promise(resolve=>{function poll(){
   const m=inspect().test.motion;
   if(m.action!=='walk'||m.settled){requestAnimationFrame(poll);return;}
   Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});
   Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>'hidden'});
   document.dispatchEvent(new Event('visibilitychange'));resolve();
  }poll();});
 });const before=(await inspect(editor)).test;
 await editor.waitForTimeout(250);const during=(await inspect(editor)).test;measurements.editorHidden={beforeTick:before.motion.tick,duringTick:during.motion.tick};assert.equal(during.motion.tick===before.motion.tick,fixed);
 await hidden(editor,false);await editor.keyboard.up('ArrowRight');await editor.waitForTimeout(350);const finished=(await inspect(editor)).test;
 if(fixed){assert.deepEqual(finished.player,{...before.player,x:before.motion.destination.x,y:before.motion.destination.y});assert.equal(finished.motion.settled,true);}
 pass(fixed?'Hidden editor playtest freezes a committed step and resumes without lost time or continued held input':'Baseline reproduces editor movement continuing while hidden');
 if(fixed){
  const start=(await inspect(editor)).test.player.x;await editor.keyboard.down('ArrowRight');
  const direction=await editor.locator('#test-dialog [data-dir=up]').boundingBox(),touch=await editorContext.newCDPSession(editor);
  await touch.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:direction.x+direction.width/2,y:direction.y+direction.height/2}]});
  await touch.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
  await editor.waitForFunction(async x=>(await import('/map-editor/editor.js')).inspect().test.player.x>=x+2,start);await editor.keyboard.up('ArrowRight');
  pass('Releasing an editor touch restores the independently held keyboard direction');
  await editor.locator('#exit-test').click();
  const jump=await editor.evaluate(async()=>{const {newProject,exportProject}=await import('/map-editor/model.js');const p=newProject();p.maps[0].spawn={x:4,y:4};p.maps[0].features[5*20+4]='ledge-down';return exportProject(p);});
  await editor.locator('#import').click();await editor.locator('#data-text').fill(jump);await editor.locator('#apply-import').click();await editor.waitForSelector('#data-dialog',{state:'hidden'});await editor.locator('#test').click();await editor.keyboard.down('ArrowDown');
  await editor.evaluate(async()=>{const {inspect}=await import('/map-editor/editor.js');await new Promise(resolve=>{function poll(){if(!inspect().test.animation){requestAnimationFrame(poll);return;}Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'));resolve();}poll();});});
  const jumpBefore=(await inspect(editor)).test;await editor.waitForTimeout(500);assert.deepEqual((await inspect(editor)).test,jumpBefore);
  await hidden(editor,false);await editor.keyboard.up('ArrowDown');await editor.waitForFunction(async()=>(await import('/map-editor/editor.js')).inspect().test.landings===1);
  const landed=(await inspect(editor)).test;assert.deepEqual([landed.player.x,landed.player.y,landed.player.facing,landed.map],[4,6,'down','map-1']);
  pass('Hidden editor hops freeze their animation clock and land once after resume');
 }
 await editor.screenshot({path:out+'/phone-playtest.png'});await editorContext.close();

 if(fixed){
  // Match the pre-optimization renderer, not another copy of the new algorithm.
  const prior=await browser.newContext(),current=await browser.newContext();
  for(const path of ['src/coastal-format.js','src/coastal-drawing.js','src/world-water.js']){
   const body=execFileSync('git',['show','ee2a3cf67ead72385b64170003addf9c28fd9442:'+path],{encoding:'utf8'});
   await prior.route('**/'+path,r=>r.fulfill({status:200,contentType:'text/javascript',body}));
  }
  const a=await prior.newPage(),b=await current.newPage();watch(a);watch(b);
  async function pixels(page){
   await page.goto(base+'/map-editor/');await page.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));
   return page.evaluate(async()=>{
    const {newMap}=await import('/map-editor/model.js'),{drawWorldWater}=await import('/src/world-water.js'),{coastalWashPixels,compileCoastalField}=await import('/src/coastal-format.js'),{createCoastalDrawing,drawCoastalBoundary}=await import('/src/coastal-drawing.js');
    const cv=document.createElement('canvas');cv.width=160;cv.height=128;const c=cv.getContext('2d',{willReadFrequently:true}),hashes=[],probes={};
    const hash=async()=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',c.getImageData(0,0,160,128).data))].map(n=>n.toString(16).padStart(2,'0')).join('');
    for(const type of ['grass','sand-moving','sand-still','mixed','raw']){
     const m=newMap('pixels','Pixels',12,12);m.terrain.fill(type.startsWith('sand')?'sand':'grass');
     for(let y=2;y<=8;y++)for(let x=2;x<=8;x++)if(!(x===5&&y===5))m.terrain[y*12+x]=type==='mixed'&&x>=4&&x<=6&&y>=4&&y<=6?'water-ocean-moving':'water-fresh-shallow-'+(type==='sand-still'?'still':'moving');
     if(type==='raw')m.raw[4*12+4]={id:'meadow.grass.0',blocked:false};
     for(const minute of [720,1260])for(const bounds of [{x:33,y:49,w:160,h:128},{x:208,y:240,w:160,h:128}])for(let f=0;f<32;f++){
      c.clearRect(0,0,160,128);c.save();c.translate(-bounds.x,-bounds.y);drawWorldWater(c,m,{dayClock:{minute,remainder:0}},f*.1,[{x:128,y:132,options:{}}],(ctx,x,y)=>{ctx.fillStyle='#ae7762';ctx.fillRect(x-12,y-40,24,40);},{bounds});c.restore();if(hashes.length===264||hashes.length===384)probes[hashes.length]=[...c.getImageData(0,0,160,128).data];hashes.push(await hash());
     }
    }
    // Packed shoreline canvases must equal the authoritative full native mask.
    const field=compileCoastalField([{x:1,y:1},{x:2,y:1},{x:1,y:2},{x:2,y:2}],128,160),d=createCoastalDrawing(field,()=>({ground:'sand',moving:true}));
    const full=document.createElement('canvas');full.width=128;full.height=160;const context=full.getContext('2d');
    for(let f=0;f<32;f++){context.clearRect(0,0,128,160);drawCoastalBoundary(context,d,f,{bank:false});const actual=context.getImageData(0,0,128,160).data,expected=coastalWashPixels(field,f);for(let i=0;i<actual.length;i++)if(actual[i]!==expected[i])throw Error('Packed wash mismatch '+f+':'+i);}
    return {hashes,probes,waveFrames:d.waves.size,waveBytes:[...d.waves.values()].reduce((n,a)=>n+a.width*a.height*4,0)};
   });
  }
  const old=await pixels(a),now=await pixels(b);const differences=now.hashes.flatMap((h,i)=>h===old.hashes[i]?[]:[{index:i,type:['grass','sand-moving','sand-still','mixed','raw'][Math.floor(i/128)],minute:Math.floor(i/64)%2?1260:720,bounds:Math.floor(i/32)%2,frame:i%32}]);measurements.waterMismatches=differences;measurements.pixelDifferences=Object.fromEntries(Object.entries(now.probes).map(([index,data])=>[index,data.flatMap((v,i)=>v===old.probes[index][i]?[]:[{x:Math.floor(i/4)%160,y:Math.floor(i/4/160),channel:i%4,before:old.probes[index][i],after:v}]).slice(0,12)]));assert.equal(differences.length,0,JSON.stringify(differences.slice(0,12))); assert.equal(now.waveFrames,32);measurements.nativeWaterPixelComparisons=now.hashes.length;measurements.packedWater=now;delete measurements.packedWater.hashes;delete measurements.packedWater.probes;
  pass('640 pre-optimization water composites match exactly across all32 phases, day/night, moving/still sand, mixed depths, raw overrides, reflected actors and clipped viewports');pass('All32 packed shoreline frames match the full native mask exactly and remain reusable');
  await prior.close();await current.close();
 }
 assert.deepEqual(errors,[]);pass('Isolated phone and native compositor checks have no browser exceptions');
}finally{await writeFile(out+'/technical-checks.json',JSON.stringify({checks,errors,measurements,fixed,physicalSafariTested:false},null,2)+'\n');await browser.close();}
