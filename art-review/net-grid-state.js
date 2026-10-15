// M1.NET2: isolated grid comparison, using the adventure's unchanged controller.
import {createMotion,getMotionView,advanceMotion,TICK_SECONDS} from '../src/movement.js';
export {TICK_SECONDS};
export const DIR={down:[0,1],up:[0,-1],left:[-1,0],right:[1,0]};
export const RULES=Object.freeze({width:640,height:448,tile:32,columns:20,rows:14,creepGate:3,swingSeconds:.56,hitStart:.18});
export const MEADOW=Array.from({length:14},(_,y)=>Array.from({length:20},(_,x)=>x===(y<4?9:y<10?10:9)||y===8&&x>=5&&x<=14||y===3&&x===10||y===9&&x===9?'path':'grass'));
export const foot=(x,y)=>({x:x*32+16,y:y*32+32});
export const inside=(x,y)=>Number.isInteger(x)&&Number.isInteger(y)&&x>=1&&x<=18&&y>=2&&y<=12;
const same=(a,b)=>a.x===b.x&&a.y===b.y;
function reservation(m){const v=getMotionView(m);return [m.player,...(!v.settled&&v.destination?[v.destination]:[])];}
export function occupiedCell(c){const v=getMotionView(c.motion);return v.destination&&!v.settled&&v.actionTick>=v.actionTicks/2?{...v.destination}:{x:c.cell.x,y:c.cell.y};}
export function blocked(s,x,y,except=null){if(!inside(x,y))return true;const cell={x,y};
 if(except!=='player'&&reservation(s.motion).some(p=>same(p,cell)))return true;
 return s.critters.some(c=>!c.caught&&c.id!==except&&reservation(c.motion).some(p=>same(p,cell)));
}
function syncPlayer(s){const v=getMotionView(s.motion),p=foot(v.tileX,v.tileY);s.player.x=v.x*2+16;s.player.y=v.y*2+32;s.player.facing=v.facing;s.player.moving=v.moving;s.player.cell={x:v.tileX,y:v.tileY};s.player.settled=v.settled;s.player.destination=v.destination;s.player.frame=v.moving?(v.pose==='strideA'?'A':v.pose==='strideB'?'C':'P'):'idle';s.player.stride=Math.abs(s.player.x-p.x)+Math.abs(s.player.y-p.y);}
function syncCritter(c){const v=getMotionView(c.motion);c.x=v.x*2+16;c.y=v.y*2+32;}
export function createNetTest(){const cell={x:7,y:7,facing:'down'},motion=createMotion(cell);const s={time:0,tick:0,player:{},cell,motion,gate:1,gateTick:0,ready:false,pendingSwing:false,swing:null,swings:0,caught:[],effect:null,critters:[
 [0,'button-snail','Land snail',7,8,7], [1,'stag-beetle','Stag beetle',11,7,3], [2,'isopod','Isopod',5,5,5],
 [3,'button-snail','Land snail',13,10,7], [4,'stag-beetle','Stag beetle',10,4,3], [5,'isopod','Isopod',4,10,5]
 ].map(([id,kind,name,x,y,pace])=>{const cell={x,y,facing:'down'};return {id,kind,name,cell,motion:createMotion(cell),pace,gate:pace,gateTick:0,alert:0,caught:false,pauseTicks:120+id*17};})};syncPlayer(s);s.critters.forEach(syncCritter);return s;}
export function catchTile(s){const facing=s.swing?.facing||s.player.facing,[dx,dy]=DIR[facing];return {x:s.cell.x+dx,y:s.cell.y+dy};}
export function catchCenter(s){const c=catchTile(s);return foot(c.x,c.y);}
function beginSwing(s){s.pendingSwing=false;s.swing={age:0,facing:s.player.facing,resolved:false,tile:catchTile(s)};s.swings++;s.player.moving=false;s.player.frame='idle';}
export function startSwing(s){if(s.swing||s.pendingSwing)return false;if(!getMotionView(s.motion).settled)s.pendingSwing=true;else beginSwing(s);return true;}
export function netPose(s){if(!s.swing)return s.ready||s.pendingSwing?'ready':'carry';const t=s.swing.age;return t<.12?'windup':t<.18?'sweep':t<.30?'strike':t<.43?'follow':'recover';}
export function stepNetTest(s,input={},dt=TICK_SECONDS){s.time+=dt;s.tick++;const p=s.player;p.moving=false;
 if(s.effect){s.effect.age+=dt;if(s.effect.age>1)s.effect=null;}
 if(s.pendingSwing&&getMotionView(s.motion).settled)beginSwing(s);
 if(s.swing){s.swing.age+=dt;if(!s.swing.resolved&&s.swing.age>=RULES.hitStart){s.swing.resolved=true;const tile=s.swing.tile,center=foot(tile.x,tile.y);const c=s.critters.find(c=>!c.caught&&same(occupiedCell(c),tile));
  if(c){c.caught=true;s.caught.push({id:c.id,kind:c.kind,name:c.name});s.effect={kind:'catch',...center,critter:c.kind,age:0};}else s.effect={kind:'miss',...center,age:0};
 }if(s.swing.age>=RULES.swingSeconds)s.swing=null;
 }else{
  if(s.gateTick===0){if(getMotionView(s.motion).settled)s.gate=s.ready?RULES.creepGate:1;const held=s.pendingSwing?new Set():new Set(input.directions|| (input.direction?[input.direction]:[]));advanceMotion(s.motion,held,false,(x,y)=>!blocked(s,x,y,'player'));syncPlayer(s);}
  else{p.moving=!!getMotionView(s.motion).destination&&!getMotionView(s.motion).settled;}
  s.gateTick=(s.gateTick+1)%s.gate;
 }
 for(const c of s.critters){if(c.caught)continue;const distance=Math.abs(c.cell.x-s.cell.x)+Math.abs(c.cell.y-s.cell.y);
  if(c.kind==='stag-beetle'&&p.moving&&s.gate===1&&distance<=2)c.alert=1.5;else c.alert=Math.max(0,c.alert-dt);
  const v=getMotionView(c.motion);if(v.settled&&c.gateTick===0){if(c.pauseTicks>0){c.pauseTicks--;continue;}c.gate=c.alert?1:c.pace;const choices=Object.keys(DIR).filter(d=>{const [dx,dy]=DIR[d];return !blocked(s,c.cell.x+dx,c.cell.y+dy,c.id);});
   if(c.alert)choices.sort((a,b)=>{const [ax,ay]=DIR[a],[bx,by]=DIR[b];return Math.hypot(c.cell.x+bx-s.cell.x,c.cell.y+by-s.cell.y)-Math.hypot(c.cell.x+ax-s.cell.x,c.cell.y+ay-s.cell.y);});
   c.direction=c.alert?choices[0]:choices[(Math.floor(s.tick/180)+c.id)%Math.max(1,choices.length)];c.gateTick=0;
  }
  if(c.gateTick===0){advanceMotion(c.motion,new Set(c.direction?[c.direction]:[]),false,(x,y)=>!blocked(s,x,y,c.id));syncCritter(c);}c.gateTick=(c.gateTick+1)%c.gate;
 }
 return s;
}
