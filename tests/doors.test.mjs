import test from 'node:test';
import assert from 'node:assert/strict';
import {createState,startMorning} from '../src/state.js';
import {scenes,isBlocked,canStep,getEntities,transition} from '../src/world.js';
import {createMotion,advanceMotion} from '../src/movement.js';
import {approachesDoor} from '../src/lighting.js';
const delta={up:[0,-1],down:[0,1],left:[-1,0],right:[1,0]};
test('every live doorway, stair and route endpoint is reachable by walking into its declared entrance',()=>{
 let count=0;
 for(const [id,scene]of Object.entries(scenes))for(const e of scene.entities.filter(e=>e.type==='door')){
  const s=createState();startMorning(s,false);s.scene=id;
  const [dx,dy]=delta[e.entryFacing];s.player={x:e.x-dx,y:e.y-dy,facing:e.entryFacing};
  assert.equal(isBlocked(id,s.player.x,s.player.y,s),false,`${id}/${e.id} approach`);
  assert.equal(canStep(s,e.x,e.y),true,`${id}/${e.id} threshold`);
  const motion=createMotion(s.player);
  for(let n=0;n<16;n++)advanceMotion(motion,new Set([e.entryFacing]),false,(x,y)=>canStep(s,x,y));
  const gate=getEntities(s).find(g=>g.type==='door'&&g.x===s.player.x&&g.y===s.player.y&&approachesDoor(!!scene.map,!!scenes[g.to].map,g,s.player.facing));
  assert.equal(gate?.id,e.id,`${id}/${e.id} automatic travel`);transition(s,gate);
  assert.equal(s.scene,e.to);assert.equal(isBlocked(s.scene,s.player.x,s.player.y,s),false);
  assert.equal(scenes[s.scene].entities.some(g=>g.type==='door'&&g.x===s.player.x&&g.y===s.player.y),false,'arrival outside warp');count++;
 }
 assert.equal(count,28);
});
test('yard opens only the home threshold and gate, keeping neighboring walls and fences solid',()=>{
 assert.equal(isBlocked('yard',8,3),false);assert.equal(isBlocked('yard',8,11),false);
 for(const [x,y]of [[7,3],[9,3],[8,2],[7,11],[9,11],[8,12]])assert.equal(isBlocked('yard',x,y),true,`${x},${y}`);
});
test('sideways movement never activates a doorway, stair or route endpoint',()=>{
 for(const scene of Object.values(scenes))for(const e of scene.entities.filter(e=>e.type==='door'))
  for(const facing of Object.keys(delta))assert.equal(approachesDoor(!!scene.map,!!scenes[e.to].map,e,facing),facing===e.entryFacing);
});
