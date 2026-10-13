// Fresh browser contexts and synthetic drafts only. Baseline source is inspected
// through an isolated route; neither checkout nor real browser storage changes.
import assert from 'node:assert/strict';
import {mkdir,writeFile} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';
import {newProject,newMap,paint,placeObject,connectBuilding,exportProject,SAVE_KEY,clone} from '../map-editor/model.js';
const require=createRequire(import.meta.url);
const {chromium}=require((process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES||'/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules')+'/playwright');
const base=process.env.TEST_URL||'http://127.0.0.1:5198',out=process.env.TEST_OUTPUT_DIR||'docs/reviews/M1-ME6';
await mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage(),checks=[],errors=[];
page.on('pageerror',e=>errors.push(e.message));
page.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('favicon.ico'))errors.push(r.url());});
const pass=text=>{checks.push(text);console.log('PASS '+text);};
const inspect=()=>page.evaluate(async()=>(await import('/map-editor/editor.js')).inspect());
async function ready(){await page.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));}
async function fixture(p){await page.locator('#import').click();await page.locator('#data-text').fill(exportProject(p));await page.locator('#apply-import').click();await page.waitForSelector('#data-dialog',{state:'hidden'});}
async function cell(x,y){const s=await inspect(),b=await page.locator('#viewport').boundingBox();return{x:b.x+s.ox+(x+.5)*32*s.zoom,y:b.y+s.oy+(y+.5)*32*s.zoom};}
const benchmark=async()=>{
 const {newMap,paint}=await import('/map-editor/model.js'),{MapRenderer}=await import('/map-editor/render.js'),{drawWorldWater}=await import('/src/world-water.js');
 const r=new MapRenderer();await r.load();const c=document.createElement('canvas');c.width=480;c.height=320;const ctx=c.getContext('2d'),cold=[],dryEdits=[];let debug;
 for(let n=0;n<3;n++){
  const m=newMap('large','Large',60,40);for(let y=10;y<20;y++)for(let x=10;x<20;x++)paint(m,x,y,'water-fresh-still');
  const bounds={x:320,y:320,w:480,h:320};ctx.save();ctx.translate(-bounds.x,-bounds.y);
  let t=performance.now();r.draw(ctx,m,{markers:false,bounds,time:0});cold.push(performance.now()-t);
  paint(m,0,0,'path');t=performance.now();r.draw(ctx,m,{markers:false,bounds,time:0});dryEdits.push(performance.now()-t);
  debug=drawWorldWater(ctx,m,{dayClock:{minute:0,remainder:0}},0,[],()=>{},{bounds});ctx.restore();
 }
 return {coldMs:cold,distantDryEditMs:dryEdits,debug};
};
let measurements;
try{
 await page.goto(base+'/map-editor/?review=me6');await ready();
 await page.evaluate(key=>{localStorage.setItem(key,'synthetic-map-sentinel');localStorage.setItem('critz-tycoon.save.v1','synthetic-adventure-sentinel');},SAVE_KEY);
 const pixels=await page.evaluate(async()=>{
  const M=await import('/map-editor/model.js'),{MapRenderer}=await import('/map-editor/render.js'),{drawWorldWater}=await import('/src/world-water.js'),r=new MapRenderer();await r.load();
  const canvas=()=>{const c=document.createElement('canvas');c.width=c.height=640;return c;},c=canvas(),ctx=c.getContext('2d');
  const data=()=>ctx.getImageData(0,0,640,640).data;
  const difference=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]||a[i+3]!==b[i+3])n++;return n;};
  const overrides=[];
  for(const blocked of [false,true])for(const f of ['bridge','fence','ledge-down','stairs','cave','flowers']){
   const m=M.newMap();M.paint(m,5,5,f);m.raw[M.at(m,5,5)]={id:'meadow.grass.0',blocked};
   r.draw(ctx,m,{markers:false,collision:true,time:0});const before=data();m.features[M.at(m,5,5)]='';r.draw(ctx,m,{markers:false,collision:true,time:0});
   overrides.push({feature:f,blocked,differences:difference(before,data())});
  }
  const margins=[];
  for(const ground of ['path','soil','paving','sand']){
   const m=M.newMap();m.terrain.fill(ground);for(let y=3;y<7;y++)for(let x=3;x<7;x++)M.paint(m,x,y,'water-fresh-still');
   r.draw(ctx,m,{markers:false,time:0});const actual=[...ctx.getImageData(98,138,1,1).data];
   const expected=canvas(),e=expected.getContext('2d'),id=ground==='sand'?'ME3.blend.sand.grass.255':`blend.${ground}.grass.255`;
   r.drawTile(e,id,0,0);margins.push({ground,actual,expected:[...e.getImageData(2,10,1,1).data]});
  }
  const m=M.newMap();for(let y=3;y<7;y++)for(let x=3;x<7;x++)M.paint(m,x,y,'water-fresh-still');
  const region=()=>ctx.getImageData(80,80,176,192).data;ctx.clearRect(0,0,640,640);drawWorldWater(ctx,m,{dayClock:{minute:0,remainder:0}},0,[],()=>{});const before=region();
  for(let y=12;y<14;y++)for(let x=12;x<14;x++)M.paint(m,x,y,'water-fresh-shallow-still');
  ctx.clearRect(0,0,640,640);const water=drawWorldWater(ctx,m,{dayClock:{minute:0,remainder:0}},0,[],()=>{});
  const independentPoolDifferences=difference(before,region());
  m.raw[M.at(m,3,4)]={id:'meadow.grass.0',blocked:false};r.draw(ctx,m,{markers:false,time:0});const raw=ctx.getImageData(96,128,32,32).data;
  const reference=canvas();r.drawTile(reference.getContext('2d'),'meadow.grass.0',0,0);const exactWaterOverrideDifferences=difference(raw,reference.getContext('2d').getImageData(0,0,32,32).data);
  return {overrides,margins,independentPoolDifferences,exactWaterOverrideDifferences,water};
 });
 assert.ok(pixels.overrides.every(a=>a.differences===0));pass('Twelve exact-override composites match feature-free rendering and collision overlays pixel-for-pixel');
 assert.ok(pixels.margins.every(a=>JSON.stringify(a.actual)===JSON.stringify(a.expected)));pass('Path, quiet soil, paving and sand remain their actual native material in water contact margins');
 assert.equal(pixels.independentPoolDifferences,0);assert.equal(pixels.water.components,2);pass('A separate shallow pond changes zero pixels in the original deep-only pond');
 assert.equal(pixels.exactWaterOverrideDifferences,0);pass('Exact raw grass suppresses automatic water and adjacent registered projection inside its cell');

 let p=newProject(),m=p.maps[0];m.spawn={x:2,y:2};for(const [x,y]of [[2,1],[3,2],[2,3],[1,2]])paint(m,x,y,'cliff');
 await fixture(p);await page.locator('#validate').click();await page.locator('[data-issue=spawn-trapped]').click();
 assert.equal(await page.locator('#check-dialog').isVisible(),false);assert.match(await page.locator('#coordinates').innerText(),/2, 2/);assert.match(await page.locator('#status').innerText(),/no traversable exit/);pass('Actionable validation closes the report, centers the trapped start and exposes its coordinates');
 p=newProject();m=p.maps[0];for(let y=3;y<7;y++)for(let x=3;x<7;x++)paint(m,x,y,'water-fresh-still');paint(m,3,3,'water-fresh-shallow-still');await fixture(p);await page.locator('#validate').click();assert.ok(await page.locator('[data-issue=water-border]').isVisible());await page.locator('#check-dialog [data-close]').click();pass('Actual map check reports the canonical mixed-depth shallow-border violation');

 p=newProject();m=p.maps[0];const o=placeObject(m,'cottage',12,2);connectBuilding(p,m.id,o);const before=clone(p);await fixture(p);
 await page.locator('#map-settings').click();await page.locator('#width').fill('10');await page.locator('#apply-settings').click();let s=await inspect();assert.equal(s.project.maps[0].objects.length,0);assert.equal(s.project.maps[1].warps.length,0);assert.equal(s.project.maps.length,2);
 await page.locator('#undo').click();assert.deepEqual((await inspect()).project,before);pass('UI shrinking removes cropped entrance/return links, retains editable rooms and undoes losslessly');
 await page.locator('[data-mode=warp]').click();const pos=await cell(14,6);await page.mouse.click(pos.x,pos.y);await page.locator('#existing-connections button').click();s=await inspect();assert.equal(s.project.maps[0].warps.length,0);assert.equal(s.project.maps[1].warps.length,0);pass('Removing an auto-paired passage removes its return in the actual connection dialog');

 const current=await page.evaluate(benchmark),baselineContext=await browser.newContext({viewport:{width:1440,height:1000}}),baseline=await baselineContext.newPage();
 const old=execFileSync('git',['show','f0a6b31a39a58b752e365ab921da4f14e2d18a87:src/world-water.js'],{encoding:'utf8'});await baseline.route('**/src/world-water.js',route=>route.fulfill({status:200,contentType:'text/javascript',body:old}));
 await baseline.goto(base+'/map-editor/?review=me6');await baseline.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));
 const prior=await baseline.evaluate(benchmark);await baselineContext.close();
 const median=a=>[...a].sort((a,b)=>a-b)[1];measurements={baseline:prior,current,coldSpeedup:median(prior.coldMs)/median(current.coldMs),dryEditSpeedup:median(prior.distantDryEditMs)/median(current.distantDryEditMs),pixels};
 assert.ok(measurements.coldSpeedup>3,JSON.stringify(measurements));assert.equal(current.debug.compiledComponents,0);assert.ok(current.debug.fieldPixels<60*40*32*32/10);pass('Same-device cold-render benchmark improves over threefold; distant dry edits reuse bounded fields without recompilation');

 await page.goto(base+'/map-editor/?review=me6');await ready();await page.locator('#grid').uncheck();
 await writeFile(out+'/review-native.png',Buffer.from((await page.locator('#map').evaluate(c=>c.toDataURL())).split(',')[1],'base64'));await page.screenshot({path:out+'/review-desktop.png'});
 for(const [width,height]of [[390,844],[320,568]]){await page.setViewportSize({width,height});await page.goto(base+'/map-editor/?review=me6');await ready();await page.locator('#grid').uncheck();assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await page.screenshot({path:out+`/editor-${width}.png`});}
 await page.locator('#test').click();await page.screenshot({path:out+'/phone-walking.png'});await page.locator('#exit-test').click();pass('Release review opens on desktop and 320/390px phones with all four native tree styles and working playtest');
 assert.deepEqual(await page.evaluate(key=>[localStorage.getItem(key),localStorage.getItem('critz-tycoon.save.v1')],SAVE_KEY),['synthetic-map-sentinel','synthetic-adventure-sentinel']);pass('All review imports, checks, resize tests and walking preserve synthetic game/draft sentinels');
 assert.deepEqual(errors,[]);pass('No browser exceptions or missing assets');
}finally{
 await writeFile(out+'/browser-checks.json',JSON.stringify({task:'M1.ME6',checks,errors,measurements,physicalSafariTested:false},null,2)+'\n');await browser.close();
}
