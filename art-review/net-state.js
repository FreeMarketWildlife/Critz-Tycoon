// Review-only model. No save access, economy or adventure imports.
export const DIR={down:[0,1],up:[0,-1],left:[-1,0],right:[1,0]};
export const RULES=Object.freeze({width:640,height:448,walk:96,creep:38,reach:34,radius:17,swingSeconds:.56,hitStart:.18,hitEnd:.28});
export function createNetTest(){return {time:0,player:{x:256,y:256,facing:'down',stride:0,moving:false},ready:false,swing:null,swings:0,caught:[],effect:null,critters:[
 {id:0,kind:'button-snail',name:'Land snail',x:256,y:291,speed:3,phase:0},
 {id:1,kind:'stag-beetle',name:'Stag beetle',x:380,y:248,speed:12,phase:1.8},
 {id:2,kind:'isopod',name:'Isopod',x:170,y:190,speed:7,phase:3.1},
 {id:3,kind:'button-snail',name:'Land snail',x:440,y:340,speed:3,phase:4.2},
 {id:4,kind:'stag-beetle',name:'Stag beetle',x:326,y:140,speed:12,phase:5.3},
 {id:5,kind:'isopod',name:'Isopod',x:138,y:344,speed:7,phase:6.5}
 ].map(c=>({...c,caught:false,alert:0}))};}
export function startSwing(s){if(s.swing)return false;s.swing={age:0,facing:s.player.facing,resolved:false};s.swings++;return true;}
export function catchCenter(s){const [dx,dy]=DIR[s.swing?.facing||s.player.facing];return {x:s.player.x+dx*RULES.reach,y:s.player.y+dy*RULES.reach};}
export function netPose(s){if(!s.swing)return s.ready?'ready':'carry';const t=s.swing.age;return t<.12?'windup':t<.18?'sweep':t<.30?'strike':t<.43?'follow':'recover';}
export function stepNetTest(s,input,dt){
 s.time+=dt;const p=s.player;p.moving=false;
 if(s.effect){s.effect.age+=dt;if(s.effect.age>1)s.effect=null;}
 if(!s.swing){
  const dir=input.direction;if(DIR[dir]){p.facing=dir;const [dx,dy]=DIR[dir],speed=s.ready?RULES.creep:RULES.walk;
   const x=Math.max(32,Math.min(RULES.width-32,p.x+dx*speed*dt)),y=Math.max(72,Math.min(RULES.height-32,p.y+dy*speed*dt));
   const distance=Math.hypot(x-p.x,y-p.y);p.moving=distance>0;p.stride+=distance;p.x=x;p.y=y;
  }
 }else{
  s.swing.age+=dt;
  if(!s.swing.resolved&&s.swing.age>=RULES.hitStart){
   if(s.swing.age<=RULES.hitEnd){const center=catchCenter(s);const candidates=s.critters.filter(c=>!c.caught&&Math.hypot(c.x-center.x,c.y-center.y)<=RULES.radius).sort((a,b)=>Math.hypot(a.x-center.x,a.y-center.y)-Math.hypot(b.x-center.x,b.y-center.y));
    if(candidates.length){const c=candidates[0];c.caught=true;s.caught.push({id:c.id,kind:c.kind,name:c.name});s.effect={kind:'catch',x:center.x,y:center.y,critter:c.kind,age:0};}
    else s.effect={kind:'miss',...center,age:0};
   }s.swing.resolved=true;
  }
  if(s.swing.age>=RULES.swingSeconds)s.swing=null;
 }
 for(const c of s.critters){if(c.caught)continue;
  const d=Math.hypot(c.x-p.x,c.y-p.y),skittish=c.kind==='stag-beetle';
  if(skittish&&p.moving&&!s.ready&&d<64)c.alert=1.5;else c.alert=Math.max(0,c.alert-dt);
  let angle=s.time*.38+c.phase;if(c.alert)angle=Math.atan2(c.y-p.y,c.x-p.x);
  const speed=c.alert?52:c.speed;c.x=Math.max(44,Math.min(RULES.width-44,c.x+Math.cos(angle)*speed*dt));c.y=Math.max(84,Math.min(RULES.height-36,c.y+Math.sin(angle)*speed*.65*dt));
 }
 return s;
}
