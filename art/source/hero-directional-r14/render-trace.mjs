// Explicitly requested isolated automated test of owned local review assets.
// Screenshots actual <img> renders; never canvas.drawImage(first-frame shortcut).
import fs from 'node:fs/promises';import path from 'node:path';import {createRequire} from 'node:module';import {performance} from 'node:perf_hooks';
const require=createRequire(import.meta.url),{chromium}=require('/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const ext=path.resolve(process.argv[2]),base='http://127.0.0.1:8771',root=path.join(ext,'render-trace');await fs.mkdir(root,{recursive:true});await fs.copyFile(new URL('render-trace-player.html',import.meta.url),path.join(ext,'trace-player.html'));
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--no-sandbox']});
const report={method:'Isolated Playwright owned-page automated screenshot trace; not uninterrupted human watch',actualImageElementRenders:true,canvasDrawImageUsed:false,userStorageUsed:false,base,traces:{}};
async function trace(direction){
 const out=path.join(root,direction);await fs.mkdir(out,{recursive:true});const context=await browser.newContext({viewport:{width:112,height:192},deviceScaleFactor:1});const page=await context.newPage();
 await page.goto(base+'/trace-player.html?direction='+direction);await page.waitForFunction(()=>[...document.images].length===2&&[...document.images].every(i=>i.complete&&i.naturalWidth===112));
 const startedUTC=new Date().toISOString(),start=performance.now(),targetMs=direction==='south'?11000:7600;let samples=[];
 while(performance.now()-start<targetMs){const t0=performance.now();const png=await page.locator('#stack').screenshot({animations:'allow',scale:'css',timeout:10000});const t1=performance.now();const file=path.join(out,String(samples.length).padStart(4,'0')+'.png');await fs.writeFile(file,png);samples.push({file,startMs:t0-start,endMs:t1-start,midpointMs:(t0+t1)/2-start});await new Promise(resolve=>setTimeout(resolve,20));}
 report.traces[direction]={startedUTC,finishedUTC:new Date().toISOString(),elapsedMs:performance.now()-start,targetMs,samples};await context.close();process.stdout.write(direction+': '+samples.length+' actual rendered samples\n');
}
try{await Promise.all(['south','north'].map(trace));await Promise.all(['west','east'].map(trace));}finally{await browser.close();await fs.writeFile(path.join(ext,'render-trace-captures.json'),JSON.stringify(report,null,2)+'\n');}
