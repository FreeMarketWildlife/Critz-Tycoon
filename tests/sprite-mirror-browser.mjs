import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium,webkit}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');
const fs=require('fs'),assert=require('assert/strict');
const base=process.env.EDITOR_BASE||'http://127.0.0.1:8842';const out=process.env.MIRROR_QA_OUTPUT||'test-results/mirror-editor';fs.mkdirSync(out,{recursive:true});
(async()=>{const report=[];for(const [engine,mobile,width]of [['chrome',false,1400],['chrome',true,390],['webkit',true,320]]){
const b=await(engine==='chrome'?chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE,headless:true}):webkit.launch({headless:true}));const ctx=await b.newContext({viewport:{width,height:mobile?844:1050},isMobile:mobile,hasTouch:mobile});const p=await ctx.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
await ctx.addInitScript(()=>localStorage.setItem('critz-tycoon.save.v1','MIRROR_SYNTHETIC_SENTINEL'));
for(const mode of ['body','normal']){await p.goto(base+'/sprite-editor/'+(mode==='body'?'?mode=body-regions':''));await p.waitForFunction(()=>document.documentElement.dataset.editorReady==='true');const get=()=>p.evaluate(async m=>m==='body'?(await import('./body-regions.js')).getBodyRegionSnapshot():(await import('./editor.js')).getSnapshot(),mode);const cells=async()=>{const s=await get();return mode==='body'?s.labels:s.project.frames[0].pixels};
const draw=async(x,y,x2=x,y2=y)=>{const s=await get(),r=await p.locator('#canvas').boundingBox(),z=s.zoom;const pt=(a,b)=>({x:r.x+(a+.5)*z,y:r.y+(b+.5)*z});const a=pt(x,y),d=pt(x2,y2);if(mobile&&x===x2&&y===y2)await p.touchscreen.tap(a.x,a.y);else{await p.mouse.move(a.x,a.y);await p.mouse.down();await p.mouse.move(d.x,d.y,{steps:3});await p.mouse.up();}await p.waitForTimeout(40);};
const state=await p.locator('#mirror').getAttribute('aria-pressed');assert.equal(state,'false');const before=await cells();await p.locator('#mirror').click();assert.deepEqual(await cells(),before);assert.equal(await p.locator('#mirror').getAttribute('aria-pressed'),'true');
if(mode==='body'){await p.selectOption('#br-part','4');if(mobile&&await p.locator('#inspector').isVisible())await p.locator('#toggle-inspector').click();}
const init=await cells();await draw(0,1);let now=await cells();assert.equal(now[32],now[63]);assert.notEqual(now[32],init[32]);await p.locator('#undo').click();assert.deepEqual(await cells(),init);await p.locator('#redo').click();assert.deepEqual(await cells(),now);
await p.locator(mode==='body'?'#br-erase':'[data-tool=eraser]').click();await draw(31,1);assert.equal((await cells())[32],0);assert.equal((await cells())[63],0);await p.locator('#undo').click();assert.deepEqual(await cells(),now);
await p.locator(mode==='body'?'#br-brush':'[data-tool=pencil]').click();await p.locator('#mirror').click();const off=await cells();await draw(2,3);assert.equal((await cells())[3*32+29],off[3*32+29]);
await p.locator('#mirror').click();const strokeBefore=await cells();await draw(4,5,7,5);const strokeAfter=await cells();for(let x=4;x<=7;x++)assert.equal(strokeAfter[5*32+x],strokeAfter[5*32+31-x]);await p.locator('#undo').click();assert.deepEqual(await cells(),strokeBefore);await p.locator('#redo').click();assert.deepEqual(await cells(),strokeAfter);
if(mode==='body'){
 const keyboardBefore=await cells(),ks=await get(),kr=await p.locator('#canvas').boundingBox();await p.mouse.move(kr.x+16.5*ks.zoom,kr.y+40.5*ks.zoom);await p.locator('#canvas').focus();await p.keyboard.press('Enter');const keyboardAfter=await cells();assert.equal(keyboardAfter[40*32+16],4);assert.equal(keyboardAfter[40*32+15],4);await p.locator('#undo').click();assert.deepEqual(await cells(),keyboardBefore);await p.locator('#redo').click();assert.deepEqual(await cells(),keyboardAfter);
 if(!mobile){const s=await get(),r=await p.locator('#canvas').boundingBox();await p.mouse.click(r.x+16.5*s.zoom,r.y+40.5*s.zoom,{button:'right'});assert.equal((await cells())[40*32+16],0);assert.equal((await cells())[40*32+15],0);await p.locator('#undo').click();assert.deepEqual(await cells(),keyboardAfter);}
}
if(mode==='normal'&&!mobile){
 await p.locator('[data-tool=line]').click();await draw(3,10,7,13);let a=await cells();for(let y=10;y<=13;y++)for(let x=3;x<=7;x++)assert.equal(a[y*32+x],a[y*32+31-x]);
 await p.locator('[data-tool=rectangle]').click();await draw(3,17,7,20);a=await cells();assert.ok(a[17*32+3]);assert.equal(a[17*32+3],a[17*32+28]);
 await p.locator('[data-tool=fill]').click();await draw(4,18);a=await cells();assert.ok(a[18*32+4]);assert.equal(a[18*32+4],a[18*32+27]);
 // An odd-width synthetic project proves center shade changes only once and mirror never edits existing pixels on enable.
 const synthetic=await get();synthetic.project.width=5;synthetic.project.height=5;synthetic.project.palette=[null,'#3878b8'];synthetic.project.frames=[{name:'Odd',ticks:8,pixels:Array(25).fill(1)}];await p.evaluate(v=>localStorage.setItem('fmw.sprite-editor.v1',JSON.stringify(v)),synthetic.project);await p.reload();await p.waitForFunction(()=>document.documentElement.dataset.editorReady==='true');await p.locator('#mirror').click();await p.locator('[data-tool=shade]').click();await draw(2,2);const odd=await cells();assert.equal(odd.filter(v=>v!==1).length,1);assert.notEqual(odd[12],1);
}
assert.equal(await p.evaluate(()=>localStorage.getItem('critz-tycoon.save.v1')),'MIRROR_SYNTHETIC_SENTINEL');
const r=await p.locator('#mirror').boundingBox();assert.ok(r.width>=40&&r.height>=44);assert.ok(r.x>=0&&r.x+r.width<=width);assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await p.screenshot({path:out+'/'+engine+'-'+width+'-'+mode+'.png'});report.push({engine,width,mode,pass:true,errors:[...errors],toggleBounds:r});
}await b.close();}fs.writeFileSync(out+'/browser-report.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));})().catch(e=>{console.error(e);process.exit(1)});
