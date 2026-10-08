import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {inflateSync} from 'node:zlib';
import {worldFoot,cellFoot} from '../src/world-space.js';
import {createMotion,advanceMotion} from '../src/movement.js';
import {scenes,isBlocked} from '../src/world.js';
const manifest=JSON.parse(readFileSync('assets/playable/overworld/master.json'));
const entries=new Map(manifest.tiles.map(t=>[t.id,t]));
function pixels(){const png=readFileSync('assets/playable/overworld/master.png'),chunks=[];for(let p=8;p<png.length;){const n=png.readUInt32BE(p);if(png.toString('ascii',p+4,p+8)==='IDAT')chunks.push(png.subarray(p+8,p+8+n));p+=n+12;}const raw=inflateSync(Buffer.concat(chunks)),stride=manifest.imageWidth*4+1;for(let y=0;y<manifest.imageHeight;y++)assert.equal(raw[y*stride],0);return (id,x,y)=>{const t=entries.get(id),p=(t.y+y)*stride+1+(t.x+x)*4;return [...raw.subarray(p,p+4)];};}
test('indoor and outdoor feet occupy the same bottom-center cell, including interpolation',()=>{
 for(const [x,y] of [[1,3],[15,8],[22,25]]){assert.deepEqual(cellFoot(x,y),{x:x*32+16,y:(y+1)*32});assert.deepEqual(worldFoot(x*16+1,y*16),{x:x*32+18,y:(y+1)*32});}
 // Equal distances to both interior side walls for the same 32px sprite frame.
 assert.equal(cellFoot(1,8).x-16,32);assert.equal(cellFoot(15,8).x+16,16*32);
});
test('releasing blocked input stops immediately; held obstacles never displace the actor',()=>{
 const m=createMotion({x:3,y:4,facing:'right'}),held=new Set(['right']);for(let n=0;n<35;n++){const v=advanceMotion(m,held,false,()=>false);assert.equal(v.moving,false);assert.deepEqual([v.x,v.y],[48,64]);}
 const v=advanceMotion(m,new Set(),false,()=>false);assert.equal(v.action,'idle');assert.equal(v.pose,'idle');assert.equal(v.settled,true);
});
test('foundation metatiles carry a real ground strip and preserve every original source pixel',()=>{
 const pixel=pixels(),source=JSON.parse(readFileSync('art/source/overworld-v1/pixels.json'));
 for(const tile of source.tiles)tile.rows.forEach((row,y)=>row.forEach((v,x)=>assert.deepEqual(pixel(tile.id,x,y),v?[...Buffer.from(source.colors[v].slice(1),'hex'),255]:[0,0,0,0],tile.id)));
 const contact=manifest.tiles.filter(t=>t.contact);assert.equal(contact.length,42);
 for(const t of contact){assert.equal(t.blocked,true);const ground=t.contact.surface==='grass'?'ground.grass.0':`${t.contact.surface}.255`;for(let x=0;x<32;x++)assert.deepEqual(pixel(t.id,x,31),pixel(ground,x,31));}
 for(const t of manifest.tiles)for(let y=0;y<32;y++)for(let x=0;x<32;x++)assert.ok([0,255].includes(pixel(t.id,x,y)[3]));
});
test('every live foundation remains solid and every tree uses roots at its authored footprint',()=>{
 for(const [id,scene]of Object.entries(scenes)){if(!scene.map)continue;for(const o of scene.objects){
  if(o.kind==='building')for(let x=0;x<o.w;x++){assert.ok(entries.get(o.tiles[4][x]).contact);assert.equal(isBlocked(id,o.x+x,o.y+4),true);}
  if(o.kind==='tree'){assert.ok(o.id.endsWith('.rooted'));const rows=manifest.assemblies[o.id];assert.equal(rows.length,o.h);assert.ok(rows.at(-1).every(t=>t.startsWith('contact.tree.')));assert.deepEqual(o.collision,[o.x,o.y+o.h-1,2,1]);}
 }}
});
