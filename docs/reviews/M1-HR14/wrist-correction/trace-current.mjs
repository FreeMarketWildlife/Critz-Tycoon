// Isolated owned-page QA: actual image-element screenshots, no canvas or user storage.
import fs from 'node:fs/promises';
import http from 'node:http';
import path from 'node:path';
import {createRequire} from 'node:module';
import {performance} from 'node:perf_hooks';
const {chromium}=createRequire(import.meta.url)('/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const source=path.dirname(new URL(import.meta.url).pathname),out=process.argv[2];
await fs.mkdir(path.join(out,'captures'),{recursive:true});
const html='<!doctype html><style>*{margin:0;padding:0}body{background:#bed4d5}#stack{width:80px}img{display:block;width:80px;height:96px;image-rendering:pixelated}</style><div id="stack"><img src="/normal.gif"><img src="/slow.gif"></div>';
const server=http.createServer(async(req,res)=>{if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(html);return;}const f=req.url==='/normal.gif'?'south-dressed-bald-normal-1x.gif':req.url==='/slow.gif'?'south-dressed-bald-slow-1x.gif':null;if(!f){res.writeHead(404).end();return;}res.setHeader('Content-Type','image/gif');res.end(await fs.readFile(path.join(source,f)));});
await new Promise(resolve=>server.listen(8787,'127.0.0.1',resolve));
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const report={method:'Actual native image-element screenshot trace in fresh isolated browser context; no uninterrupted human watch',userStorageUsed:false,canvasUsed:false,samples:[]};
try{
 const context=await browser.newContext({viewport:{width:80,height:192},deviceScaleFactor:1}),page=await context.newPage();
 await page.goto('http://127.0.0.1:8787');await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth===80));
 const start=performance.now();report.startedUTC=new Date().toISOString();
 while(performance.now()-start<14000){const t0=performance.now();const file=path.join(out,'captures',String(report.samples.length).padStart(4,'0')+'.png');await page.locator('#stack').screenshot({path:file,animations:'allow',scale:'css'});const t1=performance.now();report.samples.push({file,startMs:t0-start,endMs:t1-start,midpointMs:(t0+t1)/2-start});await new Promise(r=>setTimeout(r,20));}
 report.elapsedMs=performance.now()-start;report.finishedUTC=new Date().toISOString();await context.close();
}finally{await browser.close();server.close();await fs.writeFile(path.join(out,'captures.json'),JSON.stringify(report,null,2));}
console.log(report.samples.length+' actual native rendered screenshots');
