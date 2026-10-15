// M1.NET3: normal movement, hold/release net and visible critter escapes.
import {createMotion,getMotionView,advanceMotion,TICK_SECONDS} from '../src/movement.js';
export {TICK_SECONDS};
export const DIR={down:[0,1],up:[0,-1],left:[-1,0],right:[1,0]};
export const RULES=Object.freeze({width:640,height:448,tile:32,columns:20,rows:14,readyAfter:.24,tapHit:.34,readyHit:.14,tapDuration:.70,readyDuration:.48});
export const MEADOW=Array.from({length:14},(_,y)=>Array.from({length:20},(_,x)=>x===(y<4?9:y<10?10:9)||y===8&&x>=5&&x<=14||y===3&&x===10||y===9&&x===9?'path':'grass'));
export const GRASS=[[6,9],[12,9],[4,5],[13,11],[11,3],[4,11]].map(([x,y])=>({x,y}));
export const foot=(x,y)=>({x:x*32+16,y:y*32+32});
export const inside=(x,y)=>Number.isInteger(x)&&Number.isInteger(y)&&x>=1&&x<=18&&y>=2&&y<=12;
const same=(a,b)=>a.x===b.x&&a.y===b.y;
function reservation(m){const v=getMotionView(m);return [m.player,...(!v.settled&&v.destination?[v.destination]:[])];}
export function occupiedCell(c){const v=getMotionView(c.motion);return v.destination&&!v.settled&&v.actionTick>=v.actionTicks/2?{...v.destination}:{x:c.cell.x,y:c.cell.y};}
export function blocked(s,x,y,except=null){if(!inside(x,y))return true;const cell={x,y};
 if(except!=='player'&&reservation(s.motion).some(p=>same(p,cell)))return true;
 return s.critters.some(c=>!c.caught&&!c.escaped&&!c.escape&&c.id!==except&&reservation(c.motion).some(p=>same(p,cell)));
}
function syncPlayer(s){const v=getMotionView(s.motion),p=foot(v.tileX,v.tileY);s.player.x=v.x*2+16;s.player.y=v.y*2+32;s.player.facing=v.facing;s.player.moving=v.moving;s.player.cell={x:v.tileX,y:v.tileY};s.player.settled=v.settled;s.player.destination=v.destination;s.player.frame=v.moving?(v.pose==='strideA'?'A':v.pose==='strideB'?'C':'P'):'idle';s.player.stride=Math.abs(s.player.x-p.x)+Math.abs(s.player.y-p.y);}
function syncCritter(c){const v=getMotionView(c.motion);c.x=v.x*2+16;c.y=v.y*2+32;}
export function createNetTest(){const cell={x:7,y:7,facing:'down'},motion=createMotion(cell);const s={time:0,tick:0,player:{},cell,motion,ready:false,netHeld:false,heldAge:0,pendingSwing:null,swing:null,swings:0,caught:[],effect:null,critters:[
 [0,'button-snail','Land snail',7,8,7], [1,'stag-beetle','Stag beetle',11,7,3], [2,'isopod','Isopod',5,5,5],
 [3,'button-snail','Land snail',13,10,7], [4,'stag-beetle','Stag beetle',10,4,3], [5,'isopod','Isopod',4,10,5]
 ].map(([id,kind,name,x,y,pace])=>{const cell={x,y,facing:'down'};return {id,kind,name,cell,motion:createMotion(cell),pace,gate:pace,gateTick:0,alert:0,fear:0,escape:null,escaped:false,caught:false,pauseTicks:120+id*17};})};syncPlayer(s);s.critters.forEach(syncCritter);return s;}
export function catchTile(s){const facing=s.swing?.facing||s.player.facing,[dx,dy]=DIR[facing];return {x:s.cell.x+dx,y:s.cell.y+dy};}
export function catchCenter(s){const c=catchTile(s);return foot(c.x,c.y);}
function beginSwing(s,prepared=false){s.pendingSwing=null;s.swing={age:0,prepared,hit:prepared?RULES.readyHit:RULES.tapHit,duration:prepared?RULES.readyDuration:RULES.tapDuration,facing:s.player.facing,resolved:false,tile:catchTile(s)};s.swings++;s.player.moving=false;s.player.frame='idle';}
export function startSwing(s,prepared=false){if(s.swing||s.pendingSwing)return false;if(!getMotionView(s.motion).settled)s.pendingSwing={prepared};else beginSwing(s,prepared);return true;}
export function pressNet(s){if(s.netHeld||s.swing||s.pendingSwing)return false;s.netHeld=true;s.heldAge=0;s.ready=false;return true;}
export function releaseNet(s){if(!s.netHeld)return false;const prepared=s.ready;s.netHeld=false;s.ready=false;s.heldAge=0;return startSwing(s,prepared);}
export function cancelNet(s){s.netHeld=false;s.ready=false;s.heldAge=0;}
export function netPose(s){if(!s.swing)return s.ready||s.pendingSwing?'ready':'carry';const t=s.swing.age,hit=s.swing.hit;return t<hit-.06?'windup':t<hit?'sweep':t<hit+.10?'strike':t<hit+.22?'follow':'recover';}
export function beginEscape(s,c){if(c.caught||c.escape||c.escaped)return;const style=c.kind==='stag-beetle'?'fly':'crawl';const target=GRASS.map(g=>({...g,...{foot:foot(g.x,g.y)}})).sort((a,b)=>Math.hypot(a.foot.x-c.x,a.foot.y-c.y)-Math.hypot(b.foot.x-c.x,b.foot.y-c.y))[0];const dx=c.x-s.player.x,dy=c.y-s.player.y,len=Math.hypot(dx,dy)||1;c.escape={style,age:0,duration:style==='fly'?1.2:1.05,from:{x:c.x,y:c.y},target:{x:target.foot.x,y:target.foot.y},grass:{x:target.x,y:target.y},away:{x:dx/len,y:dy/len}};c.alert=0;}
export function escapePosition(c){const e=c.escape,p=Math.min(1,Math.max(0,e.age/e.duration));if(e.style==='fly'){const f=Math.max(0,(p-.12)/.88);return{x:e.from.x+e.away.x*70*f,y:e.from.y+e.away.y*24*f-(RULES.height+64)*f*f};}const t=Math.min(1,p/.85);return{x:e.from.x+(e.target.x-e.from.x)*t,y:e.from.y+(e.target.y-e.from.y)*t};}
function scareNear(s,tile,radius){for(const c of s.critters){if(c.caught||c.escape||c.escaped||c.alert>0)continue;const q=occupiedCell(c);if(Math.abs(q.x-tile.x)+Math.abs(q.y-tile.y)<=radius)c.alert=.18;}}
export function stepNetTest(s,input={},dt=TICK_SECONDS){s.time+=dt;s.tick++;const p=s.player;p.moving=false;
 if(s.effect){s.effect.age+=dt;if(s.effect.age>1)s.effect=null;}
 if(s.netHeld){s.heldAge+=dt;s.ready=s.heldAge>=RULES.readyAfter;}
 if(s.pendingSwing&&getMotionView(s.motion).settled)beginSwing(s,s.pendingSwing.prepared);
 if(s.swing){s.swing.age+=dt;if(!s.swing.resolved&&s.swing.age>=s.swing.hit){s.swing.resolved=true;const tile=s.swing.tile,center=foot(tile.x,tile.y);const c=s.critters.find(c=>!c.caught&&!c.escaped&&!c.escape&&same(occupiedCell(c),tile));
  if(c){c.caught=true;s.caught.push({id:c.id,kind:c.kind,name:c.name});s.effect={kind:'catch',...center,critter:c.kind,age:0};}else s.effect={kind:'miss',...center,age:0};scareNear(s,tile,c?1:2);
 }if(s.swing.age>=s.swing.duration)s.swing=null;
 }else{
  // Exactly the unchanged adventure controller, one advance every game tick.
  const held=s.pendingSwing?new Set():new Set(input.directions|| (input.direction?[input.direction]:[]));advanceMotion(s.motion,held,false,(x,y)=>!blocked(s,x,y,'player'));syncPlayer(s);
 }

 for(const c of s.critters){if(c.caught)continue;
  if(c.escape){c.escape.age+=dt;if(c.escape.age>=c.escape.duration)c.escaped=true;continue;}if(c.escaped)continue;
  if(c.alert>0){c.alert=Math.max(0,c.alert-dt);if(!c.alert)beginEscape(s,c);continue;}
  const distance=Math.abs(c.cell.x-s.cell.x)+Math.abs(c.cell.y-s.cell.y),disturbing=p.moving||s.motion.action?.kind==='blocked';
  const tolerance=c.kind==='stag-beetle'?.40:c.kind==='isopod'?.52:.70;
  c.fear=Math.max(0,(c.fear||0)+(disturbing&&!s.ready&&distance<=2?dt:-dt*1.5));if(c.fear>=tolerance){c.alert=.18;continue;}
  const v=getMotionView(c.motion);if(v.settled&&c.gateTick===0){if(c.pauseTicks>0){c.pauseTicks--;continue;}c.gate=c.pace;const choices=Object.keys(DIR).filter(d=>{const [dx,dy]=DIR[d];return !blocked(s,c.cell.x+dx,c.cell.y+dy,c.id);});
   c.direction=choices[(Math.floor(s.tick/180)+c.id)%Math.max(1,choices.length)];c.gateTick=0;
  }
  if(c.gateTick===0){advanceMotion(c.motion,new Set(c.direction?[c.direction]:[]),false,(x,y)=>!blocked(s,x,y,c.id));syncCritter(c);}c.gateTick=(c.gateTick+1)%c.gate;
 }
 return s;
}
