// Re-measure whole exported production builds; no baseline module interception.
import {createRequire} from 'node:module';import {mkdir,writeFile,readFile} from 'node:fs/promises';import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url),{chromium}=require((process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES||'/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules')+'/playwright');
const out=process.env.TEST_OUTPUT_DIR||'test-results/repeatability';await mkdir(out,{recursive:true});
const startupSamples=Number(process.env.STARTUP_SAMPLES??3),renderSamples=Number(process.env.RENDER_SAMPLES??3);
const versions={baseline:process.env.BASELINE_URL||'http://127.0.0.1:5222',current:process.env.TEST_URL||'http://127.0.0.1:5221'};
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const report={browser:await browser.version(),baselineCommit:'ee2a3cf67ead72385b64170003addf9c28fd9442',currentBaseCommit:process.env.TEST_COMMIT||'2b4723173d1f7c1ba2efe7b0438e7ef23144e6ab',currentBuildModules:{},sourceNote:'Base commit identifies the starting source; currentBuildModules identify the exact measured production bytes, including uncommitted work.',scope:'Whole production builds, matched local uncompressed servers. 390x844 Chrome touch emulation; 80ms latency/200000 bytes per second down/93750 up, no CPU throttle. Configured cold samples alternate version order; actual counts are recorded. One cache-enabled repeat navigation per route/version after an unmeasured warm-up; no-cache servers may still resend bodies. Heap metrics are forced-GC JS/embedder metrics, not total process/GPU RAM. Rendering: configured new map samples, each cold build and two full32-phase loops.',startupSamples,renderSamples,startup:{baseline:{},current:{}},rendering:{},errors:[]};
async function ready(page,route){await page.goto(route,{waitUntil:'domcontentloaded'});if(new URL(route).pathname.includes('map-editor'))await page.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));else await page.locator('[data-action=new]').waitFor();}
async function navigation(page,url){const start=performance.now();await ready(page,url);const ms=performance.now()-start;return page.evaluate(ms=>{const resources=performance.getEntriesByType('resource');return {ms,requests:resources.length,decodedBytes:resources.reduce((n,r)=>n+r.decodedBodySize,0),transferBytes:resources.reduce((n,r)=>n+r.transferSize,0),zeroTransferResources:resources.filter(r=>r.transferSize===0).length};},ms);}
try{
 for(const file of ['src/main.js','src/world-water.js','src/coastal-drawing.js','src/held-input.js','map-editor/editor.js','src/asset-urls.js'])report.currentBuildModules[file]=createHash('sha256').update(await readFile('dist/'+file)).digest('hex');
 for(let round=0;round<startupSamples;round++)for(const version of round%2?['current','baseline']:['baseline','current'])for(const [name,route]of [['game','/'],['editor','/map-editor/']]){
  const context=await browser.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true}),page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));page.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('favicon.ico'))report.errors.push(r.url()+':'+r.status());});
  const cdp=await context.newCDPSession(page);await cdp.send('Network.enable');await cdp.send('Network.setCacheDisabled',{cacheDisabled:true});await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:80,downloadThroughput:200000,uploadThroughput:93750});
  const sample=await navigation(page,versions[version]+route);const group=report.startup[version][name]??={cold:[],repeat:[]};group.cold.push(sample);console.log(JSON.stringify({version,route,round,cold:sample}));
  if(round===startupSamples-1){await cdp.send('Network.setCacheDisabled',{cacheDisabled:false});await ready(page,versions[version]+route);group.repeat.push(await navigation(page,versions[version]+route));console.log(JSON.stringify({version,route,cacheEnabledRepeat:group.repeat[0]}));}
  await context.close();
 }
 for(const [version,url]of Object.entries(versions)){
  const context=await browser.newContext(),page=await context.newPage();await ready(page,url+'/map-editor/');const cdp=await context.newCDPSession(page);const samples=[];
  for(let sample=0;sample<renderSamples;sample++){
   await cdp.send('HeapProfiler.collectGarbage');const before=await cdp.send('Runtime.getHeapUsage');
   const values=await page.evaluate(async sample=>{
    const {newMap}=await import('/map-editor/model.js'),{drawWorldWater}=await import('/src/world-water.js');
    const map=newMap('measure-'+sample,'Synthetic',64,48);map.terrain.fill('sand');for(let y=10;y<30;y++)for(let x=10;x<36;x++)map.terrain[y*64+x]='water-fresh-shallow-moving';
    const canvas=document.createElement('canvas');canvas.width=480;canvas.height=320;const c=canvas.getContext('2d'),bounds={x:300,y:310,w:480,h:320},state={dayClock:{minute:720,remainder:0}},refs=[];
    const create=document.createElement.bind(document),seen=new WeakSet();let count=0,bytes=0;
    document.createElement=(name,...args)=>{const cv=create(name,...args);if(name==='canvas'){refs.push(new WeakRef(cv));const get=cv.getContext.bind(cv);cv.getContext=(...args)=>{if(!seen.has(cv)){seen.add(cv);count++;bytes+=cv.width*cv.height*4;}return get(...args);};}return cv;};
    const draw=f=>{c.clearRect(0,0,480,320);c.save();c.translate(-bounds.x,-bounds.y);const d=drawWorldWater(c,map,state,f*.1,[],()=>{},{bounds});c.restore();return d;};
    try{
     const start=performance.now(),coldDebug=draw(0),coldMs=performance.now()-start,loops=[];let lastDebug=coldDebug;
     for(let loop=0;loop<2;loop++){const beforeCount=count,beforeBytes=bytes,frames=[];for(let f=1;f<=32;f++){const start=performance.now();lastDebug=draw(f);frames.push(performance.now()-start);}loops.push({frames,medianMs:[...frames].sort((a,b)=>a-b)[16],newCanvasCount:count-beforeCount,newCanvasBytes:bytes-beforeBytes});}
     window.__retainedWaterProbe={map,canvas,refs};return {coldMs,coldDebug,allocatedCanvasCount:count,allocatedCanvasBytes:bytes,loops,afterDebug:lastDebug};
    }finally{document.createElement=create;}
   },sample);
   await cdp.send('HeapProfiler.collectGarbage');await cdp.send('HeapProfiler.collectGarbage');const after=await cdp.send('Runtime.getHeapUsage');
   const retained=await page.evaluate(()=>{const alive=window.__retainedWaterProbe.refs.map(r=>r.deref()).filter(Boolean);return {canvasCount:alive.length,bitmapAreaBytes:alive.reduce((n,c)=>n+c.width*c.height*4,0)};});
   samples.push({...values,forcedGcHeapBefore:before,forcedGcHeapAfter:after,observedRetainedCanvases:retained});await page.evaluate(()=>delete window.__retainedWaterProbe);
  }
  report.rendering[version]=samples;console.log(JSON.stringify({version,rendering:samples.map(s=>({coldMs:s.coldMs,firstLoop:s.loops[0].medianMs,secondLoop:s.loops[1].medianMs,secondLoopAllocation:s.loops[1].newCanvasBytes,retained:s.observedRetainedCanvases}))}));await context.close();
 }
 assert.deepEqual(report.errors,[]);assert.ok(report.rendering.current.every(s=>s.loops[1].newCanvasCount===0));assert.ok(report.rendering.baseline.every(s=>s.loops[1].newCanvasCount===32));
 for(const v of Object.values(report.startup))for(const s of Object.values(v)){const times=s.cold.map(a=>a.ms).sort((a,b)=>a-b),mid=Math.floor(times.length/2);s.medianColdMs=times.length%2?times[mid]:(times[mid-1]+times[mid])/2;}
}finally{await writeFile(out+'/repeatability.json',JSON.stringify(report,null,2)+'\n');await browser.close();}
