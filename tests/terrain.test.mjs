import test from 'node:test';import assert from 'node:assert/strict';import{readFileSync}from'node:fs';
import {overworldMaps,normalizeMask}from'../src/overworld.js';import {scenes,isBlocked}from'../src/world.js';
const manifest=JSON.parse(readFileSync(new URL('../assets/playable/overworld/master.json',import.meta.url))),by=new Map(manifest.tiles.map(t=>[t.id,t]));
test('all streets are free of fence cells and every flower has planted, unobstructed ground',()=>{
 for(const [scene,m]of Object.entries(overworldMaps)){
  for(const o of m.objects.filter(o=>o.id.startsWith('fence.')))assert.ok(!['path','paving','bridge'].includes(m.terrain[o.y*m.w+o.x]),`${scene} fence ${o.x},${o.y}`);
  for(const d of m.decals.filter(d=>d.id.startsWith('flowers.')||d.id==='fern.wild')){assert.ok(['grass','soil'].includes(m.terrain[d.y*m.w+d.x]),`${scene} flower ${d.x},${d.y}`);assert.ok(!m.solid.has(`${d.x},${d.y}`),`${scene} blocked flower ${d.x},${d.y}`);}
 }
});
test('all retained fence ends reflect their actual neighboring rails',()=>{
 for(const m of Object.values(overworldMaps)){const fences=m.objects.filter(o=>o.id.startsWith('fence.')),at=new Set(fences.map(o=>`${o.x},${o.y}`));for(const f of fences)assert.equal(f.id,`fence.${(at.has(`${f.x-1},${f.y}`)?8:0)|(at.has(`${f.x+1},${f.y}`)?2:0)}`);}
});
test('path and turf banks provide every normalized corner for every variation',()=>{
 const masks=new Set(Array.from({length:256},(_,i)=>normalizeMask(i)));for(const mask of masks){for(let v=0;v<4;v++)assert.ok(by.has(`meadow.path.${mask}.${v}`));for(let v=0;v<2;v++)assert.ok(by.has(`meadow.sward.${mask}.${v}`));}
 for(let v=0;v<16;v++)assert.ok(by.has(`meadow.grass.${v}`));
});
test('turf patches never paint over roads, bridges, water or crops',()=>{
 for(const m of Object.values(overworldMaps))for(const key of m.meadow){const [x,y]=key.split(',').map(Number);assert.equal(m.terrain[y*m.w+x],'grass');assert.match(m.ground[y*m.w+x],/^meadow.sward\./);}
});
test('cleared road widths and each original doorway remain traversable',()=>{
 for(const [scene,x,y]of [['town',4,12],['town',16,25],['town',23,34],['liarsville',27,15]])assert.equal(isBlocked(scene,x,y),false);
 for(const [id,s]of Object.entries(scenes).filter(([,s])=>s.map))for(const e of s.entities.filter(e=>e.type==='door')){const delta={up:[0,-1],down:[0,1],left:[-1,0],right:[1,0]}[e.entryFacing];assert.equal(isBlocked(id,e.x-delta[0],e.y-delta[1]),false,`${id}/${e.id}`);}
});
