import assert from 'node:assert/strict';import {createRequire} from 'node:module';import {mkdir,writeFile} from 'node:fs/promises';
const require=createRequire(import.meta.url),{chromium}=require((process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES||'/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules')+'/playwright');
const base=process.env.TEST_URL||'http://127.0.0.1:5221',out=process.env.TEST_OUTPUT_DIR||'test-results/cache-invalidation';await mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}),context=await browser.newContext({viewport:{width:390,height:844}}),p=await context.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));let report;
try{
 await p.goto(base+'/map-editor/');await p.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));
 report=await p.evaluate(async()=>{
  const {newMap,paint,resizeMap,clone}=await import('/map-editor/model.js'),{MapRenderer}=await import('/map-editor/render.js'),{drawWorldWater}=await import('/src/world-water.js'),{compileCoastalField}=await import('/src/coastal-format.js'),{createCoastalDrawing,drawCoastalBoundary}=await import('/src/coastal-drawing.js');
  const r=new MapRenderer();await r.load();const m=newMap('cache','Cache fixture',20,20);for(const origin of [2,12])for(let y=2;y<=5;y++)for(let x=origin;x<origin+4;x++)paint(m,x,y,'water-fresh-shallow-moving');
  const scratch=document.createElement('canvas');scratch.width=scratch.height=672;const sc=scratch.getContext('2d'),rows=[];
  const checksum=async map=>{const c=document.createElement('canvas');c.width=map.w*32;c.height=(map.h+1)*32;const ctx=c.getContext('2d',{willReadFrequently:true});r.draw(ctx,map,{markers:false,time:200});return [...new Uint8Array(await crypto.subtle.digest('SHA-256',ctx.getImageData(0,0,c.width,c.height).data))].map(n=>n.toString(16).padStart(2,'0')).join('');};
  async function check(label,compiled){const info=drawWorldWater(sc,m,{dayClock:{minute:720,remainder:0}},.2,[],()=>{});if(info.compiledComponents!==compiled)throw Error(label+': expected '+compiled+' compiled bodies, got '+info.compiledComponents);if(info.retainedFieldBytes!==0)throw Error(label+': construction arrays remain retained');const cached=await checksum(m),fresh=await checksum(clone(m));if(cached!==fresh)throw Error(label+': cached pixels differ from a fresh immutable map');rows.push({label,compiledComponents:info.compiledComponents,components:info.components,fieldPixels:info.fieldPixels,retainedFieldBytes:info.retainedFieldBytes,cachedWaveBytes:info.cachedWaveBytes,sha256:cached});}
  await check('cold-two-pools',2);await check('unchanged-warm-frame',0);
  paint(m,18,18,'soil');await check('distant-dry-edit',0);
  paint(m,1,3,'sand');await check('one-shore-material-edit',1);
  m.raw[3*m.w+2]={id:'meadow.grass.0',blocked:false};await check('raw-override-removes-wet-cell',1);
  delete m.raw[3*m.w+2];await check('raw-removal-restores-water',1);
  resizeMap(m,18,20);await check('resize-retains-unchanged-component-bounds',0);
  for(let y=2;y<=5;y++)for(let x=2;x<=5;x++)paint(m,x,y,'water-fresh-shallow-still');await check('moving-to-still-invalidates-shore-phase-cache',1);
  if(rows.at(-1).cachedWaveBytes!==0)throw Error('Still water retained a moving sand wash cache');
  for(let y=2;y<=5;y++)for(let x=2;x<=5;x++)paint(m,x,y,'grass');await check('deleted-pool-leaves-no-ghost-components',0);
  const field=compileCoastalField([{x:1,y:1},{x:2,y:1},{x:1,y:2},{x:2,y:2}],128,160),d=createCoastalDrawing(field,()=>({ground:'sand',moving:true}));
  if(!d.patches.every(p=>p.points instanceof Float32Array&&p.points.length%3===0))throw Error('Shoreline metadata is not packed');
  for(let f=0;f<32;f++)drawCoastalBoundary(sc,d,f);const images=[...d.waves.values()],bytes=images.reduce((n,cv)=>n+cv.width*cv.height*4,0);for(let f=0;f<32;f++)drawCoastalBoundary(sc,d,f);if(images.some((cv,i)=>cv!==[...d.waves.values()][i]))throw Error('A reusable phase canvas was replaced');
  // Simulate a large phase atlas using repeated references to the exact same
  // native patch pixels, exercising the byte cap without a giant map fixture.
  const limit=createCoastalDrawing(field,()=>({ground:'sand',moving:true})),first=limit.patches[0];limit.patches=Array.from({length:640},(_,index)=>({...first,index}));for(let f=0;f<33;f++)drawCoastalBoundary(sc,limit,f);
  const capped=[...limit.waves.values()].reduce((n,cv)=>n+cv.width*cv.height*4,0);if(capped>16*1024*1024||limit.waves.size!==6)throw Error('Phase cache cap violated: '+capped+' / '+limit.waves.size);
  return {checks:['Nine lifecycle mutations match fresh full-map pixels and exact component recompilation counts','Moving-to-still and deleted pools release inappropriate wave caches','All32 packed phases reuse identical canvases on the next loop','Oversized phase atlases respect the16MiB component budget'],rows,reusedPhaseBytes:bytes,cappedPhaseBytes:capped,cappedPhaseCount:limit.waves.size};
 });assert.deepEqual(errors,[]);for(const c of report.checks)console.log('PASS '+c);
}finally{await writeFile(out+'/cache-checks.json',JSON.stringify({report,errors},null,2)+'\n');await browser.close();}
