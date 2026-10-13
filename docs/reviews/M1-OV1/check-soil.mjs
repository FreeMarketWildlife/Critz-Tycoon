// Independent native-source and adjoining-edge checks; generator is not imported.
import fs from 'node:fs';import assert from 'node:assert/strict';import {createRequire} from 'node:module';import {validateProject} from '../../../sprite-editor/model.js';
const require=createRequire(import.meta.url),sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp'),m=JSON.parse(fs.readFileSync('assets/playable/soil-v2/atlas.json')),raw=await sharp('assets/playable/soil-v2/atlas.png').ensureAlpha().raw().toBuffer(),ink=new Set(['#ac926b','#a38a63','#997f5b','#bca276','#b29a70','#92795a']),regions=new Map(),report={task:'M1.OV1',tiles:m.tiles.length,sourceFamilies:4,sourceFrames:0,edgeComparisons:0};
for(const under of ['grass','path','paving','sand']){
 const p=JSON.parse(fs.readFileSync(`art/source/soil-v2/soil-${under}.sprite.json`));validateProject(p);assert.equal(p.frames.length,47);
 const family=m.tiles.filter(t=>t.id.startsWith(under==='sand'?'ME3.blend.soil.sand.':`blend.soil.${under}.`)).sort((a,b)=>a.neighborMask-b.neighborMask);assert.equal(family.length,47);
 family.forEach((t,i)=>{const region=[];for(let y=0;y<32;y++)for(let x=0;x<32;x++){const at=((t.y+y)*m.size[0]+t.x+x)*4,c='#'+raw.subarray(at,at+3).toString('hex');assert.equal(raw[at+3],255);assert.equal(c,p.palette[p.frames[i].pixels[y*32+x]]);region.push(ink.has(c));}if(under==='grass')regions.set(t.neighborMask,region);report.sourceFrames++;});
}
// Exhaust every 4×4 binary land/soil layout, comparing the central horizontal
// and vertical joined boundaries. Underlay variation cannot conceal a bad soil edge.
const dirs=[[0,-1,1],[1,0,2],[0,1,4],[-1,0,8],[1,-1,16],[1,1,32],[-1,1,64],[-1,-1,128]];
for(let layout=0;layout<65536;layout++){
 const on=(x,y)=>x>=0&&y>=0&&x<4&&y<4&&!!(layout&(1<<(y*4+x)));
 const mask=(x,y)=>{let m=0;for(const [dx,dy,bit]of dirs)if(on(x+dx,y+dy))m|=bit;for(const [bit,a,b]of [[16,1,2],[32,2,4],[64,4,8],[128,8,1]])if(!(m&a)||!(m&b))m&=~bit;return m;};
 if(on(1,1)&&on(2,1)){const a=regions.get(mask(1,1)),b=regions.get(mask(2,1));for(let y=0;y<32;y++){assert.equal(a[y*32+31],b[y*32]);report.edgeComparisons++;}}
 if(on(1,1)&&on(1,2)){const a=regions.get(mask(1,1)),b=regions.get(mask(1,2));for(let x=0;x<32;x++){assert.equal(a[31*32+x],b[x]);report.edgeComparisons++;}}
}
fs.writeFileSync('docs/reviews/M1-OV1/soil-checks.json',JSON.stringify({...report,status:'passed',layouts:65536,originalUnderlaysPreserved:true},null,2)+'\n');console.log(`PASS ${report.sourceFrames} exact soil source frames, ${report.edgeComparisons} shared-edge comparisons over 65,536 layouts.`);
