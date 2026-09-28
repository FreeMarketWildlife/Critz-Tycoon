import assert from 'node:assert/strict';
import {TICK_MS,createReviewClock,poseAt,directionAt} from '../art-review/walking-timing.js';
const results=[];
function test(name,fn){fn();results.push({name,pass:true});}
test('same 600 ticks across 30/60/90/120/144 Hz display schedules',()=>{
  for(const hz of [30,60,90,120,144]){
    const clock=createReviewClock(),end=TICK_MS*600;clock.advance(0);
    for(let frame=1;frame*1000/hz<end;frame++)clock.advance(frame*1000/hz);
    clock.advance(end);assert.equal(clock.tick,600,`${hz}Hz`);
  }
});
test('source-derived 8-tick holds and phase continuity',()=>{
  for(let tick=0;tick<128;tick++)assert.equal(poseAt(tick),['strideA','idle','strideB','idle'][Math.floor(tick/8)%4]);
  assert.equal(poseAt(15),'idle');assert.equal(poseAt(16),'strideB');assert.equal(poseAt(31),'idle');assert.equal(poseAt(32),'strideA');
});
test('three complete gaits per direction, exact loop',()=>{
  assert.equal(directionAt(0),'south');assert.equal(directionAt(95),'south');assert.equal(directionAt(96),'west');assert.equal(directionAt(192),'north');assert.equal(directionAt(288),'east');assert.equal(directionAt(384),'south');
});
test('pause/resume reset drops suspended time without changing phase',()=>{
  const c=createReviewClock();c.advance(0);c.advance(10*TICK_MS);assert.equal(c.tick,10);c.resetBaseline();c.advance(60000);assert.equal(c.tick,10);c.advance(60000+8*TICK_MS);assert.equal(c.tick,18);
});
test('long frames drop elapsed time rather than racing through artwork',()=>{
  const c=createReviewClock();c.advance(0);c.advance(5000);assert.equal(c.tick,0);assert.equal(c.droppedMs,5000);c.advance(5000+TICK_MS);assert.equal(c.tick,1);
});
test('single pose stepping follows boundaries and restarts cleanly',()=>{
  const c=createReviewClock();c.advance(0);c.advance(3*TICK_MS);c.nextPose();assert.equal(c.tick,8);c.nextPose();assert.equal(c.tick,16);c.restart();assert.equal(c.tick,0);
});
console.log(JSON.stringify({passed:results.length,checks:results},null,2));
