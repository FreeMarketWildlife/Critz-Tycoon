// Isolate viewport work from renderer changes by comparing the opening editor
// with the same current renderer, manifests, browser and synthetic map.
import assert from 'node:assert/strict';import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';import {execFileSync} from 'node:child_process';
const require=createRequire(import.meta.url),{chromium}=require((process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES||'/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules')+'/playwright');
const base=process.env.TEST_URL||'http://127.0.0.1:5221',out=process.env.TEST_OUTPUT_DIR||'test-results/editor-view';
await mkdir(out,{recursive:true});const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}),report={baseline:null,current:null,checks:[],errors:[]};
try{
 for(const version of ['baseline','current']){
  const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true}),p=await context.newPage();p.on('pageerror',e=>report.errors.push(e.message));
  if(version==='baseline'){const body=execFileSync('git',['show','ee2a3cf67ead72385b64170003addf9c28fd9442:map-editor/editor.js'],{encoding:'utf8'});await p.route('**/map-editor/editor.js',r=>r.fulfill({status:200,contentType:'text/javascript',body}));}
  await p.goto(base+'/map-editor/');await p.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));
  const source=await p.evaluate(async()=>{const {newProject,newMap,exportChat}=await import('/map-editor/model.js');const p=newProject();p.maps=[newMap('map-1','Synthetic large map',128,128)];return exportChat(p);});
  await p.locator('#import').click();await p.locator('#data-text').fill(source);await p.locator('#apply-import').click();await p.waitForSelector('#data-dialog',{state:'hidden'});
  const result=await p.evaluate(async()=>{
   const {inspect}=await import('/map-editor/editor.js'),canvas=document.querySelector('#map'),ctx=canvas.getContext('2d'),before=JSON.stringify(inspect().project);
   const bytes=()=>ctx.getImageData(0,0,canvas.width,canvas.height).data;
   const hash=async()=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes()))].map(n=>n.toString(16).padStart(2,'0')).join('');
   const first=await hash(),draw=CanvasRenderingContext2D.prototype.drawImage,samples=[];
   let calls=0;CanvasRenderingContext2D.prototype.drawImage=function(...args){if(this.canvas===canvas)calls++;return draw.call(this,...args);};
   try{
    for(let n=0;n<3;n++){const beforeCalls=calls,start=performance.now();for(let i=0;i<12;i++)document.querySelector('#viewport').dispatchEvent(new WheelEvent('wheel',{deltaX:2,deltaY:2,cancelable:true}));samples.push({ms:performance.now()-start,drawImageCalls:calls-beforeCalls});}
    const beforeZoom=calls,start=performance.now();for(let i=0;i<6;i++)document.querySelector(i%2?'#zoom-out':'#zoom-in').click();
    return {pan:samples,zoom:{ms:performance.now()-start,drawImageCalls:calls-beforeZoom},pixelsRetained:first===await hash(),projectRetained:before===JSON.stringify(inspect().project),nativeSize:[canvas.width,canvas.height]};
   }finally{CanvasRenderingContext2D.prototype.drawImage=draw;}
  });report[version]=result;assert.equal(result.pixelsRetained,true);assert.equal(result.projectRetained,true);
  if(version==='current'){
   assert.ok(result.pan.every(a=>a.drawImageCalls===0));assert.equal(result.zoom.drawImageCalls,0);
   await p.locator('#fit').click();await p.locator('[data-brush=soil]').click();
   const click=await p.evaluate(async()=>{const s=(await import('/map-editor/editor.js')).inspect(),r=document.querySelector('#viewport').getBoundingClientRect();return {x:r.x+s.ox+64.5*32*s.zoom,y:r.y+s.oy+64.5*32*s.zoom};});await p.mouse.click(click.x,click.y);
   assert.equal(await p.evaluate(async()=>(await import('/map-editor/editor.js')).inspect().project.maps[0].terrain[64*128+64]),'soil');await p.locator('#undo').click();
   assert.equal(await p.evaluate(async()=>(await import('/map-editor/editor.js')).inspect().project.maps[0].terrain[64*128+64]),'grass');await p.locator('#grid').uncheck();await p.locator('#collision').check();await p.screenshot({path:out+'/large-map-phone.png'});
  }await context.close();
 }
 assert.ok(report.baseline.pan.every(a=>a.drawImageCalls>=128*128*12));assert.deepEqual(report.errors,[]);
 report.checks=['Pan and zoom preserve all native map pixels and authored data','Thirty-six pan events and six zoom events issue zero map redraws','Large-map coordinate picking, painting, undo and overlay changes remain correct on phone'];console.log(JSON.stringify(report,null,2));
}finally{await writeFile(out+'/editor-view.json',JSON.stringify(report,null,2)+'\n');await browser.close();}
