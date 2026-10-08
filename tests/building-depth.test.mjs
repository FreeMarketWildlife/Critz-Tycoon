import test from 'node:test';
import assert from 'node:assert/strict';
import {buildingFootprint,buildings} from '../src/overworld.js';
import {scenes,isBlocked} from '../src/world.js';
import {createState,startMorning} from '../src/state.js';
import {migrateGridState} from '../src/grid-save.js';
test('all twelve freestanding buildings have connected rear overlap and solid walls',()=>{
 let count=0;
 for(const id of ['town','liarsville'])for(const b of scenes[id].map.objects.filter(o=>o.kind==='building')){
  assert.equal(b.rearDepth,b.name==='THE OLD WATERWORKS'?2:1);
  assert.deepEqual(b.collision,buildingFootprint(b));
  for(let y=b.y;y<b.y+b.h;y++)for(let x=b.x;x<b.x+b.w;x++)
   assert.equal(isBlocked(id,x,y),y>=b.y+b.rearDepth,`${id}/${b.name} ${x},${y}`);
  const q=[scenes[id].safeSpawn],seen=new Set([q[0].join(',')]);
  for(let i=0;i<q.length;i++)for(const [dx,dy]of [[0,1],[0,-1],[1,0],[-1,0]]){const x=q[i][0]+dx,y=q[i][1]+dy,key=`${x},${y}`;if(!seen.has(key)&&!isBlocked(id,x,y)){seen.add(key);q.push([x,y]);}}
  for(let y=b.y;y<b.y+b.rearDepth;y++)for(let x=b.x;x<b.x+b.w;x++)assert.ok(seen.has(`${x},${y}`));
  count++;
 }
 assert.equal(count,12);for(const b of buildings)assert.deepEqual(b.collision,buildingFootprint(b));
});
test('roof depth leaves wall rows and attached chimneys draw above actors behind their building',()=>{
 assert.throws(()=>buildingFootprint({x:0,y:0,w:5,h:5,rearDepth:4}));
 assert.throws(()=>buildingFootprint({x:0,y:0,w:5,h:5,rearDepth:1.5}));
 for(const id of ['town','liarsville'])for(const b of scenes[id].map.objects.filter(o=>o.kind==='building')){
  const chimney=scenes[id].map.objects.find(o=>o.id==='chimney'&&o.x===b.x+b.w-2&&o.y===b.y-1);
  assert.ok(chimney.depth>b.y+b.rearDepth);assert.ok(chimney.depth<b.depth);
 }
});
test('saves behind every building retain their position and all progress',()=>{
 for(const id of ['town','liarsville'])for(const b of scenes[id].map.objects.filter(o=>o.kind==='building')){
  const s=createState('Ari','girl','River');startMorning(s,true);s.scene=id;s.player={x:b.x+1,y:b.y+b.rearDepth-1,facing:'right'};
  assert.deepEqual(migrateGridState(s),s);
 }
});
