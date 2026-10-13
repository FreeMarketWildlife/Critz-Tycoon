// Independent exported-art check. Does not import the authoring generator.
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import assert from 'node:assert/strict';import {createRequire} from 'node:module';
import {validateProject,readProjectData} from '../../../sprite-editor/model.js';
const require=createRequire(import.meta.url),sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp'),root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'../../..'),out=path.join(root,'docs/reviews/M1-OV1');
const project=JSON.parse(fs.readFileSync(path.join(root,'art/source/button-v2/button.sprite.json'))),atlas=JSON.parse(fs.readFileSync(path.join(root,'assets/playable/button-v2/atlas.json'))),rle=JSON.parse(fs.readFileSync(path.join(root,'art/source/button-v2/button.rle.json')));
validateProject(project);assert.deepEqual(readProjectData(rle).frames,project.frames);assert.deepEqual([project.width,project.height],[32,32]);assert.equal(project.frames.length,20);
const expected=f=>Buffer.from(f.pixels.flatMap(i=>i?[...Buffer.from(project.palette[i].slice(1),'hex'),255]:[0,0,0,0]));
const sheet=await sharp(path.join(root,'assets/playable/button-v2/atlas.png')).ensureAlpha().raw().toBuffer(),frames=[];
for(let index=0;index<20;index++){
 const f=project.frames[index],bytes=expected(f),a=atlas.assets[index],id=a.id.split('.')[0],action={'button-snail':'glide','button-look':'look','button-nibble':'nibble','button-tuck':'tuck'}[id],n=Number(a.id.split('.')[1]);
 const png=await sharp(path.join(root,`assets/playable/button-v2/${action}-${n}.png`)).ensureAlpha().raw().toBuffer();assert.deepEqual(png,bytes);
 assert.equal(crypto.createHash('sha256').update(png).digest('hex'),a.rgbaSHA256);
 let l=32,t=32,r=0,b=0;const occupied=new Set();
 for(let y=0;y<32;y++)for(let x=0;x<32;x++){const i=(y*32+x)*4,at=((a.rect[1]+y)*256+a.rect[0]+x)*4;assert.deepEqual(sheet.subarray(at,at+4),bytes.subarray(i,i+4));assert.ok([0,255].includes(png[i+3]));if(png[i+3]){occupied.add(y*32+x);l=Math.min(l,x);t=Math.min(t,y);r=Math.max(r,x+1);b=Math.max(b,y+1);}}
 const seen=new Set(),queue=[occupied.values().next().value];seen.add(queue[0]);for(let k=0;k<queue.length;k++){const at=queue[k],x=at%32,y=Math.floor(at/32);for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){const a=(y+dy)*32+x+dx;if(x+dx>=0&&x+dx<32&&y+dy>=0&&y+dy<32&&occupied.has(a)&&!seen.has(a)){seen.add(a);queue.push(a);}}}assert.equal(seen.size,occupied.size,'Detached part in '+a.id);
 // No shell displacement or recoloring between personality actions.
 for(let y=10;y<23;y++)for(let x=4;x<21;x++){const i=y*32+x;if(project.frames[0].pixels[i]&&['#684a35','#a16c43','#c69757','#e6bd78','#f6dfa3'].includes(project.palette[project.frames[0].pixels[i]]))assert.equal(f.pixels[i],project.frames[0].pixels[i]);}
 assert.ok(b<=28);frames.push({id:a.id,bounds:[l,t,r,b],opaquePixels:occupied.size,connected:true,rgbaMatchesSourceAndAtlas:true});
}
let gifChecks=0,offset=0;
for(const [action,count]of [['glide',8],['look',4],['nibble',4],['tuck',4]]){
 const {data,info}=await sharp(path.join(root,`assets/playable/button-v2/${action}.gif`),{animated:true}).ensureAlpha().raw().toBuffer({resolveWithObject:true});assert.equal(info.width,32);assert.equal(info.height,count*32);
 for(let i=0;i<count;i++){assert.deepEqual(data.subarray(i*4096,(i+1)*4096),expected(project.frames[offset+i]));gifChecks++;}offset+=count;
}
assert.equal(atlas.assets.slice(0,8).reduce((s,a)=>s+a.ticks,0),72);
assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'assets/characters/hero-boy-v1/idle-south.png'))).digest('hex'),'0099dd331ae2c2d995663328e52763e8b10b1df0d36854d59676ee0ac52f7883');
const proof=await sharp(path.join(root,'assets/playable/button-v2/atlas.png')).resize(1536,576,{kernel:'nearest'}).png().toBuffer();fs.writeFileSync(path.join(out,'button-poses-6x.png'),proof);
const report={task:'M1.OV1',status:'passed',nativeFrame:[32,32],frames,decodedGIFFrames:gifChecks,glideSourceTicks:72,glideSeconds:72*280896/16777216,paletteColors:project.palette.length-1,heroApprovedHashPreserved:true,provenance:'Original native authoring; no reference raster inputs',limitations:'Visual acceptance and physical Safari require user review.'};fs.writeFileSync(path.join(out,'native-checks.json'),JSON.stringify(report,null,2)+'\n');console.log('PASS 20 native PNG/source/atlas/connected-part checks; 20 exact decoded GIF poses; stable shell, source cadence and approved Hero hash.');
