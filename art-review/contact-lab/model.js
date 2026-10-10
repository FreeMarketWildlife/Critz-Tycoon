import {createMotion,getMotionView,advanceMotion,TICK_SECONDS} from '../../src/movement.js';
// Separate M1.CT1 proposal. Never imports or mutates adventure/editor saves.
export const CELL=32,STEP_SECONDS=TICK_SECONDS;
export const OPTIONS={A:{cut:8,label:'25% structure / 75% ground'},B:{cut:16,label:'50% structure / 50% ground'},C:{cut:24,label:'75% structure / 25% ground'},D:{cut:28,label:'87.5% structure / 12.5% ground'}};
export const STATIONS={house:{name:'House',height:160,top:3,rear:'Roof projects over two clear rear rows.'},wall:{name:'Indoor wall',height:64,top:5,rear:'A short freestanding wall, viewed from inside.'},cliff:{name:'Cliff',height:96,top:4,rear:'Solid mountain edge; not a jumpable ledge.'}};
export const DELTA={up:[0,-1],down:[0,1],left:[-1,0],right:[1,0]};
export const FOOT={halfWidth:11,height:8};
export const boundary=option=>6*CELL+OPTIONS[option].cut;
export function blockedCell(station,x,y){if(x<1||x>13||y<1||y>10)return true;return x>=5&&x<=9&&y>=STATIONS[station].top&&y<=6;}
export function footBox(px,py){return{x:px-FOOT.halfWidth,y:py-FOOT.height,w:FOOT.halfWidth*2,h:FOOT.height};}
export function fits(station,px,py){const b=footBox(px,py);for(let y=Math.floor(b.y/CELL);y<=Math.floor((b.y+b.h-1)/CELL);y++)for(let x=Math.floor(b.x/CELL);x<=Math.floor((b.x+b.w-1)/CELL);x++)if(blockedCell(station,x,y))return false;return true;}
function syncMotion(s){const v=getMotionView(s.motion);Object.assign(s,{px:v.x*2+16,py:v.y*2+32,facing:v.facing,pose:v.pose,moving:v.moving,ticks:v.tick});return v;}
export function createState({option='B',station='house',surface='grass'}={}){
 const player={x:7,y:8,facing:'up'};
 const s={option:Object.hasOwn(OPTIONS,option)?option:'B',station:Object.hasOwn(STATIONS,station)?station:'house',movement:'grid',surface:['grass','path','paving','wood'].includes(surface)?surface:'grass',player,motion:createMotion(player),bumps:0,contact:false,lastContact:null};syncMotion(s);return s;
}
export function resetPosition(s,side='front'){
 const points={front:[7,8,'up'],left:[3,6,'right'],right:[11,6,'left'],behind:[7,STATIONS[s.station].top-2,'down']};
 const [x,y,facing]=points[side]||points.front;s.player={x,y,facing};s.motion=createMotion(s.player);s.contact=false;s.lastContact=null;syncMotion(s);return s;
}
export function tick(s,direction){
 const held=direction instanceof Set?direction:Object.hasOwn(DELTA,direction)?new Set([direction]):new Set();
 const view=advanceMotion(s.motion,held,false,(x,y)=>!blockedCell(s.station,x,y),{runAllowed:false});syncMotion(s);
 let bump=false;s.contact=view.action==='blocked';
 if(s.contact&&held.size){const key=`${s.facing}/${s.player.x}/${s.player.y}`;if(s.lastContact!==key){s.bumps++;bump=true;}s.lastContact=key;}else{s.lastContact=null;}
 return{bump,view};
}
export function frontGap(s){return s.px>=160&&s.px<320&&s.py>=224?s.py-2-boundary(s.option):null;}
export function choiceText(s,notes=''){return JSON.stringify({format:'critz-contact-review',version:1,task:'M1.CT2',option:s.option,structureRows:OPTIONS[s.option].cut,groundRows:32-OPTIONS[s.option].cut,transitionCollision:'entire 32×32 cell blocked',movement:'tile-based',controller:'src/movement.js — main adventure controller',method:'native assembly translated inside padded frame, same material boundary for house / indoor wall / cliff',station:s.station,surface:s.surface,notes:String(notes).slice(0,3000),status:'User preference for review; not an automatic production change'},null,2);}
export function pulse(api,enabled){if(!enabled||typeof api?.vibrate!=='function')return'unsupported';try{return api.vibrate(18)?'requested':'declined';}catch{return'declined';}}
