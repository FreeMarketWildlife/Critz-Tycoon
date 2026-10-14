import test from 'node:test';import assert from 'node:assert/strict';
import {newProject,placeObject,move,blocked,exportProject,importProject,DIRS,objectFootprint,reachableMap} from '../map-editor/model.js';
import {createMotion} from '../src/movement.js';
import {tickMapTest,finishMapJump} from '../map-editor/test-motion.js';
import {opposite} from '../src/bench-seat.js';
for(const facing of ['down','up','left','right']){
 test('Bench '+facing+': only front entry, locked facing and same-lane exit',()=>{
  const p=newProject(),m=p.maps[0],o=placeObject(m,facing==='down'?'bench':'bench-'+facing,5,5),r=objectFootprint(o),[dx,dy]=DIRS[facing];
  const target={x:facing==='right'?r.x+r.w-1:r.x,y:facing==='down'?r.y+r.h-1:r.y};
  const from={x:target.x+dx,y:target.y+dy,facing:opposite(facing)};
  assert.equal(blocked(m,target.x,target.y),true);
  const seat=move(p,m.id,from,opposite(facing));assert.equal(seat.sitting,true);assert.equal(seat.facing,facing);
  for(const [dir,[a,b]]of Object.entries(DIRS)){
   if(dir!==facing)assert.equal(move(p,m.id,seat,dir),null,'Seated side/back moves prohibited');
   if(dir!==opposite(facing))assert.equal(move(p,m.id,{x:target.x-a,y:target.y-b},dir),null,'Side/rear entry prohibited');
  }
  const exit=move(p,m.id,seat,facing);assert.equal(exit.x,from.x);assert.equal(exit.y,from.y);assert.equal(exit.benchJump,'exit');
  m.terrain[from.y*m.w+from.x]='cliff';assert.equal(move(p,m.id,seat,facing),null,'Blocked exit cannot escape collider');
 });
 test('Bench '+facing+': controller hops, cannot turn or walk on seat, releases before exit',()=>{
  const p=newProject(),m=p.maps[0],o=placeObject(m,facing==='down'?'bench':'bench-'+facing,5,5),r=objectFootprint(o),[dx,dy]=DIRS[facing];
  const target={x:facing==='right'?r.x+r.w-1:r.x,y:facing==='down'?r.y+r.h-1:r.y};
  const player={x:target.x+dx,y:target.y+dy,facing:opposite(facing)},t={project:p,map:m.id,player,motion:createMotion(player)};
  assert.equal(tickMapTest(t,opposite(facing),0),'bench-enter');assert.equal(t.animation.bench,'enter');assert.equal(t.player.sitting,undefined);
  assert.equal(finishMapJump(t,279),false);assert.equal(finishMapJump(t,280),true);assert.equal(t.player.sitting,true);
  const seated={...t.player};tickMapTest(t,facing,300);assert.equal(t.animation,null,'Held input cannot instantly leave');tickMapTest(t,null,301);
  for(const dir of Object.keys(DIRS).filter(d=>d!==facing)){tickMapTest(t,dir,320);assert.deepEqual(t.player,seated);assert.equal(t.animation,null);}
  assert.equal(tickMapTest(t,facing,400),'bench-exit');finishMapJump(t,680);assert.equal(t.player.sitting,undefined);assert.equal(t.player.x,player.x);assert.equal(t.player.y,player.y);
 });
}
test('Bench orientation projects retain v1 data and cannot create a rear traversal route',()=>{
 const p=newProject(),m=p.maps[0];for(const [i,type]of ['bench','bench-up','bench-left','bench-right'].entries())placeObject(m,type,2+i*4,4);
 assert.deepEqual(importProject(exportProject(p)).maps[0].objects,m.objects);
 const row=newProject(),a=row.maps[0];a.spawn={x:5,y:6};for(let x=0;x<a.w;x++){a.terrain[5*a.w+x]='cliff';}a.terrain[5*a.w+5]='grass';a.terrain[5*a.w+6]='grass';placeObject(a,'bench',5,5);
 const reachable=reachableMap(row,a);assert.equal(reachable.cells.has(4*a.w+5),false,'Reachability cannot walk through a seat');
});
