import test from 'node:test';import assert from 'node:assert/strict';
import {HeldDirections} from '../src/held-input.js';
import {createMotion,advanceMotion,getMotionView} from '../src/movement.js';
test('Keys, aliases and separate fingers retain independent direction ownership',()=>{
 const down=new HeldDirections();down.press('key:ArrowRight','right');down.press('key:d','right');down.press('pointer:1','right');down.press('pointer:2','right');
 down.release('pointer:1');down.release('key:d');down.release('pointer:2');assert.deepEqual([...down],['right']);down.release('pointer:1');assert.equal(down.has('right'),true);
 down.release('key:ArrowRight');assert.equal(down.size,0);
});
test('Releasing the final source exits every blocked phase on the next tick',()=>{
 for(let phase=1;phase<=32;phase++){
  const down=new HeldDirections(),motion=createMotion({x:2,y:2,facing:'right'});down.press('key:ArrowRight','right');
  for(let i=0;i<phase;i++)advanceMotion(motion,down,false,()=>false);
  assert.equal(getMotionView(motion).action,'blocked');down.release('key:ArrowRight');advanceMotion(motion,down,false,()=>false);
  assert.equal(getMotionView(motion).action,'idle');assert.deepEqual(motion.player,{x:2,y:2,facing:'right'});
 }
});
test('Editor input restores an older held direction and ignores repeat priority changes',()=>{
 const down=new HeldDirections();down.press('pointer:1','right');down.press('key:ArrowUp','up');down.press('pointer:1','right');assert.equal(down.latest(),'up');
 down.release('key:ArrowUp');assert.equal(down.latest(),'right');down.clear();assert.equal(down.latest(),null);down.release('pointer:1');assert.equal(down.size,0);
 down.press('pointer:1','left');assert.equal(down.latest(),'left');
});
