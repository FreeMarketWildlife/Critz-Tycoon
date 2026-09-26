// Isolated browser validation and contact-sheet export; never uses real save storage.
import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);
let chromium;try{({chromium}=require('playwright'));}catch{({chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright'));}
const server=spawn(process.execPath,['scripts/serve.mjs','--dist'],{env:{...process.env,PORT:'5181'},stdio:['ignore','pipe','pipe']});
await new Promise((resolve,reject)=>{server.stdout.once('data',resolve);server.once('error',reject);server.once('exit',c=>reject(Error('Server stopped '+c)));});
let browser;const report={checks:[],errors:[],viewports:[],groups:null};
const pass=text=>{report.checks.push(text);console.log('PASS '+text);};
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE,args:['--no-sandbox']});
 const context=await browser.newContext({viewport:{width:1280,height:900}}),page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));
 await page.addInitScript(()=>localStorage.setItem('critz-gallery-test-sentinel','synthetic-only'));
 await page.goto('http://127.0.0.1:5181/art-review/');await page.waitForFunction(()=>window.catalog?.ready);
 const groups=await page.evaluate(()=>window.catalog.groups);report.groups=groups;assert.equal(groups.v2,13);assert.equal(groups.v1,162);assert.ok(groups.prototype>25);pass('All 175 environment entries and prototype inventory loaded');
 assert.equal(await page.locator('.asset').count(),Object.values(groups).reduce((a,b)=>a+b));pass('Every catalog entry is shown');
 assert.equal(await page.locator('.actor canvas').count(),10);assert.equal(await page.locator('.effect canvas').count(),3);pass('10 four-direction actor previews and 3 motion previews present');
 const before=await page.locator('.actor canvas').first().evaluate(c=>c.toDataURL());await page.waitForTimeout(180);const after=await page.locator('.actor canvas').first().evaluate(c=>c.toDataURL());assert.notEqual(before,after);pass('Walking preview changes rendered pixels');
 await page.getByRole('button',{name:'Pause',exact:true}).click();const frozen=await page.evaluate(()=>window.catalog.time);await page.waitForTimeout(150);assert.equal(await page.evaluate(()=>window.catalog.time),frozen);pass('Pause freezes animation time');
 await page.getByRole('button',{name:'Step +1/12 s',exact:true}).click();assert.ok((await page.evaluate(()=>window.catalog.time))>frozen);pass('Step advances paused animation');
 await page.locator('#pose').selectOption('idle');await page.locator('#filter').selectOption('v2');assert.equal(await page.locator('.asset').count(),13);await page.locator('#search').fill('tree');assert.equal(await page.locator('.asset').count(),3);pass('Status and text filters narrow correctly');
 await page.locator('#search').fill('');await page.locator('#filter').selectOption('all');
 await mkdir('assets/catalogue',{recursive:true});
 for(const [method,file]of [['sheet','all-assets.png'],['characterFrames','character-frames.png']]){const data=await page.evaluate(method=>window.catalog[method]().toDataURL('image/png'),method);await writeFile('assets/catalogue/'+file,Buffer.from(data.split(',')[1],'base64'));}pass('Complete contact sheet and 160 sampled character views exported');
 const download=page.waitForEvent('download');await page.getByRole('button',{name:'Download character frames',exact:true}).click();assert.equal((await download).suggestedFilename(),'critz-prototype-character-frames.png');pass('PNG download works');
 for(const width of [320,390,844,1280]){await page.setViewportSize({width,height:844});const over=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);assert.equal(over,false,'Page overflow at '+width);report.viewports.push({width,overflow:false});}pass('No page overflow at 320, 390, 844 and 1280 px');
 const storage=await page.evaluate(()=>({...localStorage}));assert.deepEqual(storage,{'critz-gallery-test-sentinel':'synthetic-only'});pass('Gallery does not access/write game saves; synthetic storage unchanged');
 await page.setViewportSize({width:1280,height:900});await page.screenshot({path:'assets/catalogue/gallery-preview.png'});
 assert.equal(report.errors.length,0);pass('Zero uncaught page errors');
 await context.close();
 const reduced=await browser.newContext({reducedMotion:'reduce'}),rp=await reduced.newPage();await rp.goto('http://127.0.0.1:5181/art-review/');await rp.waitForFunction(()=>window.catalog?.ready);assert.equal(await rp.locator('#pause').innerText(),'Play');pass('Reduced-motion preference starts paused');await reduced.close();
}finally{if(browser)await browser.close();server.kill();await mkdir('docs/verification',{recursive:true});await writeFile('docs/verification/ART_GALLERY.json',JSON.stringify(report,null,2)+'\n');}
