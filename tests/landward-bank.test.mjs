import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync}from'node:fs';import{createHash}from'node:crypto';
import{compileCoastalField,coastalBankPixels}from'../src/coastal-format.js';
const baseline=JSON.parse(readFileSync(new URL('./fixtures/wa9-water-preservation.json',import.meta.url))),hash=a=>createHash('sha256').update(a).digest('hex');
test('Landward bank preserves every WA9 water-mask and water-side bank pixel in all orientations',()=>{
 for(const sample of baseline.samples){const cells=baseline.cells.map(({x,y})=>{for(let t=0;t<sample.turn;t++)[x,y]=[10-y,x];return{x,y};}),f=compileCoastalField(cells,352,384),bank=coastalBankPixels(f);
  assert.equal(hash(f.wet),sample.wet);assert.equal(hash(Buffer.from(bank.filter((v,i)=>f.wet[Math.floor(i/4)]))),sample.waterSideBank);
  const added=Array.from(f.wet,(_,i)=>!f.wet[i]&&bank[i*4+3]?i:-1).filter(i=>i>=0);assert.ok(added.length>1000);
  for(const i of added){const x=i%f.width,y=Math.floor(i/f.width);assert.ok(f.signed[i]>=-4);assert.ok(bank[i*4]>bank[i*4+1]&&bank[i*4+1]>bank[i*4+2],'New shoulder uses brown earth');assert.ok(x>=0&&y>=0);}
 }
});
test('Added shoulder lies toward land on north, south, east and west; clear water stays24px',()=>{
 const cells=[];for(let y=1;y<5;y++)for(let x=1;x<5;x++)cells.push({x,y});const f=compileCoastalField(cells,192,224),b=coastalBankPixels(f),alpha=(x,y)=>b[(y*f.width+x)*4+3];
 for(const [x,y]of [[32,96],[159,96],[96,30],[96,179]]){assert.equal(f.wet[y*f.width+x],0);assert.equal(alpha(x,y),255);}
 assert.equal(alpha(31,96),0);assert.equal(alpha(160,96),0);assert.equal(alpha(96,29),0);assert.equal(alpha(96,180),0);
 assert.equal(alpha(40,96),0);assert.equal(alpha(96,40),0);
});
test('Shallow water and sand receive no new raised dry-side shoulder',()=>{
 const f=compileCoastalField(baseline.cells,352,384);
 for(const style of [{ground:'sand'},{ground:'grass',shallow:true},{ground:'grass',shallow:false,landwardShallow:true}]){const b=coastalBankPixels(f,()=>style);for(let i=0;i<f.wet.length;i++)if(!f.wet[i])assert.equal(b[i*4+3],0);}
});
