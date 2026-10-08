import test from 'node:test';
import assert from 'node:assert/strict';
import {createState,startMorning} from '../src/state.js';
import {scenes,isBlocked,canStep,nearestEntity,transition} from '../src/world.js';
import {migrateGridState} from '../src/grid-save.js';
import {createMotion,advanceMotion} from '../src/movement.js';
import {approachesDoor} from '../src/lighting.js';

function ready(scene){const s=createState('Ari','girl','River');startMorning(s,true);s.scene=scene;return s;}
for(const scene of ['bedroom','house']){
  const stair=scenes[scene].entities.find(e=>e.stair);
  test(`${scene}: stair rails/back are solid and only the landing reaches the entrance`,()=>{
    const s=ready(scene),[x,y,w,h]=stair.stair.footprint;
    for(let cy=y;cy<y+h;cy++)for(let cx=x;cx<x+w;cx++)
      assert.equal(isBlocked(scene,cx,cy,s),cx!==stair.x||cy!==stair.y,`${cx},${cy}`);
    for(const [dx,dy,face]of [[0,1,'up'],[-1,0,'right'],[1,0,'left'],[0,-1,'down']]){
      s.player={x:stair.x+dx,y:stair.y+dy,facing:face};
      assert.equal(canStep(s,stair.x,stair.y),dy===1);
      assert.equal(nearestEntity(s)?.id==='stairs',dy===1);
      assert.equal(approachesDoor(false,false,stair,face),dy===1);
    }
    s.player={x:stair.stair.approach[0],y:stair.stair.approach[1],facing:'down'};
    assert.notEqual(nearestEntity(s)?.id,'stairs');
  });
  test(`${scene}: a complete upward step enters once and arrives outside the other staircase`,()=>{
    const s=ready(scene);s.player={x:stair.stair.approach[0],y:stair.stair.approach[1],facing:'up'};
    const motion=createMotion(s.player);
    for(let i=0;i<16;i++)advanceMotion(motion,new Set(['up']),false,(x,y)=>canStep(s,x,y));
    assert.deepEqual([s.player.x,s.player.y],[stair.x,stair.y]);
    transition(s,stair);
    const target=scenes[s.scene].entities.find(e=>e.stair);
    assert.deepEqual([s.player.x,s.player.y],target.stair.approach);
    assert.equal(s.player.facing,'down');assert.equal(isBlocked(s.scene,s.player.x,s.player.y,s),false);
  });
  test(`${scene}: every legacy stair position recovers to its landing without losing progress`,()=>{
    const [x,y,w,h]=stair.stair.footprint;
    for(let cy=y;cy<y+h;cy++)for(let cx=x;cx<x+w;cx++){
      const before=ready(scene);before.player={x:cx,y:cy,facing:'left'};
      const snapshot=structuredClone(before),after=migrateGridState(before);
      assert.deepEqual(before,snapshot);
      assert.deepEqual(after.player,{x:stair.stair.approach[0],y:stair.stair.approach[1],facing:'left'});
      for(const key of Object.keys(before).filter(k=>!['player','worldVersion','gridVersion'].includes(k)))assert.deepEqual(after[key],before[key],key);
    }
  });
}
test('opening-night stairs keep the story gate closed',()=>{
  const s=createState();s.player={x:14,y:11,facing:'up'};
  assert.equal(canStep(s,14,10),false);assert.notEqual(nearestEntity(s)?.id,'stairs');
});
