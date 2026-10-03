import {createRequire} from 'node:module';import assert from 'node:assert/strict';import {mkdir,writeFile} from 'node:fs/promises';import path from 'node:path';
const require=createRequire(import.meta.url),{chromium}=require(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'playwright'));
const out=process.env.CRITZ_QA_OUTPUT||'test-results/sprite-zoom';await mkdir(out,{recursive:true});
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE,headless:true}),context=await browser.newContext({viewport:{width:1366,height:768}}),p=await context.newPage(),report=[],errors=[];
p.on('pageerror',e=>errors.push(e.message));
const settle=()=>p.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
const snap=()=>p.evaluate(async()=>(await import('./editor.js')).getSnapshot());
async function nativeAt(point){const r=await p.locator('#canvas').boundingBox(),z=(await snap()).zoom;return{x:(point.x-r.x)/z,y:(point.y-r.y)/z};}
async function stationary(point,before){const after=await nativeAt(point),z=(await snap()).zoom;assert.ok(Math.abs(after.x-before.x)*z<=1.1,JSON.stringify({point,before,after,z}));assert.ok(Math.abs(after.y-before.y)*z<=1.1,JSON.stringify({point,before,after,z}));}
async function center(){const r=await p.locator('#viewport').boundingBox();return{x:r.x+r.width/2,y:r.y+r.height/2};}
async function test(name,fn){try{await fn();report.push({name,pass:true});console.log('PASS '+name);}catch(e){report.push({name,pass:false,error:e.stack});console.error('FAIL '+name+' '+e.stack);}}
try{
 await p.goto(process.env.CRITZ_EDITOR_URL||'http://localhost:5199/sprite-editor/');await p.waitForFunction(()=>document.documentElement.dataset.editorReady==='true');const project=(await snap()).project;
 await test('ordinary wheel zoom holds every canvas quadrant under the cursor across fit and overflowing sizes',async()=>{
  for(const [fx,fy]of [[.1,.1],[.9,.1],[.1,.9],[.9,.9],[.5,.5]]){
   await p.locator('#fit').click();await settle();const r=await p.locator('#canvas').boundingBox(),point={x:r.x+r.width*fx,y:r.y+r.height*fy},before=await nativeAt(point);await p.mouse.move(point.x,point.y);
   for(let i=0;i<5;i++){await p.mouse.wheel(0,-100);await settle();await stationary(point,before);}
   for(let i=0;i<5;i++){await p.mouse.wheel(0,100);await settle();await stationary(point,before);}
  }
 });
 await test('zoom buttons and native size preserve center of panned viewport',async()=>{
  await p.locator('#fit').click();await p.locator('#viewport').evaluate(e=>{e.scrollLeft+=71;e.scrollTop+=109;});const point=await center(),before=await nativeAt(point);
  for(const id of ['zoom-in','zoom-in','zoom-out','native']){await p.locator('#'+id).click();await settle();await stationary(point,before);}
 });
 await test('keyboard zoom uses hovered point and control-wheel does not zoom the page',async()=>{
  await p.locator('#fit').click();const r=await p.locator('#canvas').boundingBox(),point={x:r.x+7*(await snap()).zoom,y:r.y+21*(await snap()).zoom};await p.mouse.move(point.x,point.y);const before=await nativeAt(point);await p.keyboard.press('+');await settle();await stationary(point,before);
  const z=(await snap()).zoom;await p.keyboard.down('Control');await p.mouse.wheel(0,-100);await p.keyboard.up('Control');await settle();assert.equal((await snap()).zoom,z+1);await stationary(point,before);assert.equal(await p.evaluate(()=>visualViewport.scale),1);
 });
 await test('Space-drag and pan tool move view without painting; Fit recenters',async()=>{
  await p.locator('#fit').click();const r=await p.locator('#canvas').boundingBox();await p.mouse.move(r.x+r.width/2,r.y+r.height/2);await p.keyboard.down('Space');await p.mouse.down();await p.mouse.move(r.x+r.width/2+60,r.y+r.height/2+40,{steps:4});await p.mouse.up();await p.keyboard.up('Space');await settle();let moved=await p.locator('#canvas').boundingBox();assert.ok(Math.abs(moved.x-r.x-60)<1);assert.ok(Math.abs(moved.y-r.y-40)<1);
  await p.locator('[data-tool=pan]').click();const v=await p.locator('#viewport').boundingBox();await p.mouse.move(v.x+15,v.y+15);await p.mouse.down();await p.mouse.move(v.x+45,v.y+45,{steps:3});await p.mouse.up();await settle();const further=await p.locator('#canvas').boundingBox();assert.ok(Math.abs(further.x-moved.x-30)<1);assert.deepEqual((await snap()).project,project);
  await p.locator('#fit').click();await settle();const at=await nativeAt(await center());assert.ok(Math.abs(at.x-project.width/2)<.2);assert.ok(Math.abs(at.y-project.height/2)<.2);await p.locator('[data-tool=pencil]').click();
 });
 await test('drawing hits exact native pixel after cursor zoom and pan',async()=>{
  await p.locator('#fit').click();const r=await p.locator('#canvas').boundingBox(),z=(await snap()).zoom,point={x:r.x+10.5*z,y:r.y+22.5*z};await p.mouse.move(point.x,point.y);await p.mouse.wheel(0,-100);await settle();await p.mouse.click(point.x,point.y);const pixels=(await snap()).project.frames[0].pixels;assert.equal(pixels[22*32+10],1);assert.equal(pixels.filter(Boolean).length,1);await p.locator('#undo').click();
 });
 await test('small-screen zoom stays anchored and never expands the page',async()=>{
  for(const [width,height]of [[390,844],[320,568],[844,390]]){await p.setViewportSize({width,height});await p.locator('#reset-layout').click();await p.locator('#fit').click();await settle();const r=await p.locator('#canvas').boundingBox(),point={x:r.x+r.width*.75,y:r.y+r.height*.25},before=await nativeAt(point);await p.mouse.move(point.x,point.y);await p.mouse.wheel(0,-100);await settle();await stationary(point,before);assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await p.screenshot({path:path.join(out,`zoom-${width}.png`)});}
 });
 await test('zero runtime errors',async()=>assert.deepEqual(errors,[]));
}finally{await writeFile(path.join(out,'zoom-browser-report.json'),JSON.stringify(report,null,2)+'\n');await browser.close();}
if(report.some(x=>!x.pass))process.exitCode=1;
