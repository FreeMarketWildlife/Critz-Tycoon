import {createRequire}from'node:module';import{readFile,mkdir,writeFile}from'node:fs/promises';import assert from'node:assert/strict';
const require=createRequire(import.meta.url),{chromium}=require((process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES||'/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules')+'/playwright');
const url=process.env.TEST_URL||'http://localhost:5242',out=process.env.TEST_OUTPUT_DIR||'docs/reviews/M1-WA10/browser';await mkdir(out,{recursive:true});
const before=(await readFile(new URL('../docs/reviews/M1-WA10/before-native.png',import.meta.url))).toString('base64'),browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}),ctx=await browser.newContext({viewport:{width:1440,height:960}}),page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
try{
 await page.goto(url+'/map-editor/?area=rootport');await page.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));
 const result=await page.evaluate(async before=>{
  const {inspect}=await import('/map-editor/editor.js'),{compileCoastalField}=await import('/src/coastal-format.js'),{isWater}=await import('/src/water-map.js'),project=inspect().project,m=project.maps[0],cells=[];
  for(let y=0;y<m.h;y++)for(let x=0;x<m.w;x++)if(isWater(m.terrain[y*m.w+x]))cells.push({x,y});
  const field=compileCoastalField(cells,m.w*32,m.h*32+32),canvas=document.querySelector('#map'),actual=canvas.getContext('2d').getImageData(0,0,canvas.width,canvas.height).data;
  const image=new Image();image.src='data:image/png;base64,'+before;await image.decode();const reference=document.createElement('canvas');reference.width=canvas.width;reference.height=canvas.height;reference.getContext('2d').drawImage(image,0,0);const old=reference.getContext('2d').getImageData(0,0,canvas.width,canvas.height).data;
  let changed=0,changedWater=0;for(let i=0;i<field.wet.length&&i<actual.length/4;i++)if([0,1,2,3].some(c=>actual[i*4+c]!==old[i*4+c])){changed++;if(field.wet[i])changedWater++;}
  return{changed,changedWater,projectName:project.name,mapSize:[m.w,m.h]};
 },before);
 assert.ok(result.changed>100);assert.equal(result.changedWater,0);assert.equal(result.projectName,'Rootport');assert.deepEqual(result.mapSize,[22,16]);await page.screenshot({path:out+'/rootport-desktop.png'});
 await page.setViewportSize({width:390,height:844});await page.locator('#fit').click();assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await page.screenshot({path:out+'/rootport-phone.png'});
 assert.deepEqual(errors,[]);await writeFile(out+'/bank-browser-check.json',JSON.stringify({url,...result,errors,checks:['Actual Rootport canvas differs only outside the previous water mask','Rootport project and dimensions retained','Phone canvas fits','No browser exceptions']},null,2)+'\n');console.log(result);
}finally{await browser.close();}
