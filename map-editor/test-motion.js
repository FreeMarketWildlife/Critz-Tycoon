import {createMotion,advanceMotion} from '../src/movement.js';
import {move} from './model.js';
export function probeStep(t,dir){return move({...t.project,maps:t.project.maps.map(m=>({...m,objects:m.objects.map(o=>({...o}))}))},t.map,t.player,dir);}
// Jumps never enter the one-cell walking controller, including immediate turns
// out of walking or a blocked action. At rest retain the normal turn first.
export function tickMapTest(t,held,now){
 if(t.pendingArrival){if(now-t.dust.start<300)return;t.player=t.pendingArrival;t.map=t.player.map;t.pendingArrival=null;t.motion=createMotion(t.player);return 'transition';}
 if(t.animation)return;
 if(t.benchWaitRelease){if(!held)t.benchWaitRelease=false;return;}
 if(t.player.sitting){
  const dest=held?probeStep(t,held):null;
  if(dest?.benchJump){t.animation={x:t.player.x,y:t.player.y,tx:dest.x,ty:dest.y,start:now,duration:280,jump:true,bench:'exit',from:{...t.player},dest};return 'bench-exit';}
  return;
 }

 const a=t.motion.action,accept=!a||a.elapsed===a.duration||a.kind==='blocked'&&held!==a.direction;
 const canFace=t.player.facing===held||t.motion.inputState==='moving';
 if(held&&accept&&canFace){const dest=probeStep(t,held);if(dest?.benchJump){t.animation={x:t.player.x,y:t.player.y,tx:dest.x,ty:dest.y,start:now,duration:280,jump:true,bench:'enter',from:{...t.player},dest};return 'bench-enter';}if(dest?.jump){const old={...t.player};move(t.project,t.map,t.player,held);t.player=dest;t.animation={x:old.x,y:old.y,start:now,duration:360,jump:true};t.hops=(t.hops||0)+1;return 'jump';}}
 advanceMotion(t.motion,new Set(held?[held]:[]),false,(x,y)=>{const dx=x-t.player.x,dy=y-t.player.y,dir=dx<0?'left':dx>0?'right':dy<0?'up':'down',dest=probeStep(t,dir);return !!dest&&!dest.jump&&!dest.benchJump;});
 const done=t.motion.action;if(done?.target&&done.elapsed===done.duration){const dest=move(t.project,t.map,{...done.from,facing:done.direction},done.direction);if(dest?.transition){t.player=dest;t.map=dest.map;t.motion=createMotion(t.player);return 'transition';}}
}
export function finishMapJump(t,now){if(!t.animation||now-t.animation.start<t.animation.duration)return false;if(t.animation.bench){t.player={...t.animation.dest};delete t.player.benchJump;t.animation=null;t.benchWaitRelease=true;t.motion=createMotion(t.player);return true;}t.dust={x:t.player.x,y:t.player.y,start:now};if(t.player.arrival)t.pendingArrival=t.player.arrival;t.animation=null;t.motion=createMotion(t.player);t.landings=(t.landings||0)+1;return true;}
