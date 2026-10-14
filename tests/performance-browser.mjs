// Same-machine diagnostics, isolated profiles and synthetic maps only.
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
const require=createRequire(import.meta.url);
const {chromium}=require((process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES||'/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules')+'/playwright');
const base=process.env.TEST_URL||'http://127.0.0.1:5221';
const out=process.env.TEST_OUTPUT_DIR||'test-results/performance';
await mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const report={commit:execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim(),scope:'Local production preview, desktop Chrome on this host; 390x844 viewport. Cold network: 80ms latency, 1.6Mbps down, 750kbps up; no CPU throttle. Timings are diagnostics, not physical-phone claims.',startup:{},rendering:null,errors:[]};
try {
 for(const [name,route,ready]of [['game','/','[data-action=new]'],['editor','/map-editor/','#status']]){
  const samples=[];
  for(let i=0;i<3;i++){
   const context=await browser.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true}),page=await context.newPage();
   page.on('pageerror',e=>report.errors.push(e.message));
   const cdp=await context.newCDPSession(page);await cdp.send('Network.enable');await cdp.send('Network.setCacheDisabled',{cacheDisabled:true});
   await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:80,downloadThroughput:200000,uploadThroughput:93750});
   const start=performance.now();await page.goto(base+route);await page.locator(ready).waitFor();
   if(name==='editor')await page.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));
   const readyMs=performance.now()-start;
   const resources=await page.evaluate(()=>performance.getEntriesByType('resource').map(r=>({path:new URL(r.name).pathname,startMs:r.startTime,durationMs:r.duration,bytes:r.decodedBodySize,transferBytes:r.transferSize})));
   samples.push({readyMs,requestCount:resources.length,decodedBytes:resources.reduce((n,a)=>n+a.bytes,0),resources});await context.close();
  }
  report.startup[name]={samples,medianReadyMs:samples.map(a=>a.readyMs).sort((a,b)=>a-b)[1]};
 }
 const context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));
 await page.goto(base+'/map-editor/');await page.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));
 report.rendering=await page.evaluate(async()=>{
  const {MapRenderer}=await import('/map-editor/render.js'),{newMap}=await import('/map-editor/model.js'),{drawWorldWater}=await import('/src/world-water.js');
  const renderer=new MapRenderer();await renderer.load();const maps={};
  for(const material of ['grass','sand']){
   const map=newMap('benchmark-'+material,'Synthetic',64,48);map.terrain.fill(material);
   for(let y=10;y<30;y++)for(let x=10;x<36;x++)map.terrain[y*map.w+x]='water-fresh-shallow-moving';
   maps[material]=map;
  }
  const cv=document.createElement('canvas');cv.width=480;cv.height=320;const c=cv.getContext('2d');
  const bounds={x:300,y:310,w:480,h:320},state={dayClock:{minute:720,remainder:0}};
  const samples={};
  const create=document.createElement.bind(document),canvases=[];document.createElement=function(name,...args){const result=create(name,...args);if(name==='canvas')canvases.push(result);return result;};
  try{
   for(const [material,map]of Object.entries(maps)){
    const offset=canvases.length,start=performance.now();c.save();c.translate(-bounds.x,-bounds.y);const debug=drawWorldWater(c,map,state,0,[],()=>{},{bounds});c.restore();const coldMs=performance.now()-start;
    const warm=[];for(let i=1;i<=32;i++){const start=performance.now();c.clearRect(0,0,480,320);c.save();c.translate(-bounds.x,-bounds.y);drawWorldWater(c,map,state,i*.1,[],()=>{},{bounds});c.restore();warm.push(performance.now()-start);}
    const retained=canvases.slice(offset).filter(a=>a.width>32||a.height>32);
    samples[material]={coldMs,warmMs:warm,medianWarmMs:[...warm].sort((a,b)=>a-b)[16],debug,allocatedCanvasCount:retained.length,allocatedCanvasBytes:retained.reduce((n,a)=>n+a.width*a.height*4,0)};
   }
  }finally{document.createElement=create;}
  // A warm operation count is deterministic even when scheduler timings vary.
  let images=0;const draw=c.drawImage.bind(c);c.drawImage=(...args)=>{images++;return draw(...args);};
  c.save();c.translate(-bounds.x,-bounds.y);drawWorldWater(c,maps.grass,state,4,[],()=>{},{bounds});c.restore();c.drawImage=draw;samples.grass.warmDrawImageCalls=images;
  return samples;
 });await context.close();assert.deepEqual(report.errors,[]);
 console.log(JSON.stringify({startup:Object.fromEntries(Object.entries(report.startup).map(([k,v])=>[k,{medianReadyMs:v.medianReadyMs,requests:v.samples[0].requestCount,bytes:v.samples[0].decodedBytes}])),rendering:report.rendering},null,2));
}finally{await writeFile(out+'/performance.json',JSON.stringify(report,null,2)+'\n');await browser.close();}
