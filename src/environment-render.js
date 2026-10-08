import {actorView,drawReaction} from './actors.js';
import {drawCritter,RESCUES} from './living-art.js';
import {applyLighting} from './lighting.js';
import {scenes,getEntities} from './world.js';
import {TICK_SECONDS} from './movement.js';
let sheet,manifest,tiles;
export async function loadEnvironment(){
 const url=new URL('../assets/playable/overworld/master.json',import.meta.url),response=await fetch(url);
 if(!response.ok)throw Error('Overworld manifest failed to load');manifest=await response.json();
 sheet=new Image();sheet.src=new URL(manifest.image,url).href;await sheet.decode();
 if(sheet.width!==manifest.imageWidth||sheet.height!==manifest.imageHeight)throw Error('Overworld sheet dimensions do not match');
 tiles=new Map(manifest.tiles.map(t=>[t.id,t]));
 for(const [sceneId,scene]of Object.entries(scenes)){if(!scene.map)continue;const map=scene.map;
  for(const id of [...map.ground,...map.decals.map(d=>d.id),...map.objects.flatMap(o=>o.tiles?o.tiles.flat():manifest.assemblies[o.id]?.flat()||[o.id])])if(!tiles.has(id))throw Error(`Missing tile ${id} in ${sceneId}`);
 }
}
export function animationFrame(id,time,phase=0){
 const frame=Math.floor(time/(16*TICK_SECONDS)+phase)%4;
 if(id.startsWith('water.')&&/^water\.\d+$/.test(id))return frame?`anim.${id}.${frame}`:id;
 if(id.startsWith('flowers.')){const f=[0,1,0,2][frame];return f?`anim.${id}.${f}`:id;}
 if(id.startsWith('waterfall.0.'))return frame?`anim.waterfall.${id.split('.')[2]}.${frame}`:id;
 return id;
}
export function renderEnvironment(c,state,time,view,character,npcLook){
 const map=scenes[state.scene].map,foot={x:view.x*2+16,y:view.y*2+32};
 const camera={x:Math.max(0,Math.min(map.w*32-480,foot.x-240)),y:Math.max(0,Math.min(map.h*32-320,foot.y-(view.focusY??176)))};
 c.imageSmoothingEnabled=false;c.fillStyle='#487b59';c.fillRect(0,0,480,320);c.save();c.translate(-camera.x,-camera.y);
 const visible=(x,y,w=1,h=1)=>x*32<camera.x+512&&(x+w)*32>camera.x-32&&y*32<camera.y+352&&(y+h)*32>camera.y-64;
 const draw=(id,x,y,phase=0)=>{const a=tiles.get(animationFrame(id,time,phase));if(!a)throw Error('Missing environment tile '+id);c.drawImage(sheet,a.x,a.y,32,32,Math.round(x),Math.round(y),32,32);};
 const assembly=(o)=>{const objectId=o.id==='mill.wheel.0'?`mill.wheel.${Math.floor(time/.18)%4}`:o.id;const rows=o.tiles||manifest.assemblies[objectId];if(rows)rows.forEach((row,j)=>row.forEach((id,i)=>draw(id,(o.x+i)*32,(o.y+j)*32)));else draw(o.id,o.x*32,o.y*32);};
 const drawActor=(x,y,options)=>{c.save();c.translate(x,y);character(c,0,0,options);c.restore();};
 for(let y=Math.max(0,Math.floor(camera.y/32));y<Math.min(map.h,Math.ceil((camera.y+320)/32));y++)for(let x=Math.max(0,Math.floor(camera.x/32));x<Math.min(map.w,Math.ceil((camera.x+480)/32));x++)draw(map.ground[y*map.w+x],x*32,y*32);
 const actorCell={x:Math.floor(foot.x/32),y:Math.floor((foot.y-1)/32)};
 const activeGrass=map.grass.has(`${actorCell.x},${actorCell.y}`),grassFrame=view.moving?[1,3,2,3][Math.floor((view.actionTick||0)/3)%4]:0;
 for(const d of map.decals){if(!visible(d.x,d.y))continue;let id=d.id;if(id==='grass.living.0'&&d.x===actorCell.x&&d.y===actorCell.y)id=`grass.living.${grassFrame}`;draw(id,d.x*32,d.y*32,d.id.startsWith('flowers.')?(d.x+d.y)%4:0);}
 const effects=[],sorted=[];for(const o of map.objects)if(visible(o.x,o.y,o.w,o.h))sorted.push({depth:o.depth*32,draw:()=>{assembly(o);if(o.id==='fountain.jet')draw(`water.spray.${Math.floor(time/.18)%4}`,o.x*32,(o.y+1)*32);}});
 for(const e of getEntities(state)){
  if(e.type==='npc'){const v=actorView(state,e.id),x=(v.x===null?e.x*16:v.x)*2+16,y=(v.y===null?e.y*16:v.y)*2+32;sorted.push({depth:y,draw:()=>drawActor(x,y-v.hop,{look:npcLook(e,state.gender),facing:v.facing,pose:v.pose})});effects.push(()=>drawReaction(c,x,y,v));}
  else if(e.type==='rescue')sorted.push({depth:(e.y+1)*32,draw:()=>{drawCritter(c,RESCUES[e.id],e.x*32,e.y*32,time);const x=e.x*32+16,y=e.y*32+18-Math.floor(time*3)%2;c.fillStyle='#fff3bb';c.fillRect(x-1,y-5,2,10);c.fillRect(x-5,y-1,10,2);}});
 }
 const hero=actorView(state,'hero');sorted.push({depth:foot.y+.1,draw:()=>drawActor(foot.x,foot.y-hero.hop,{gender:state.gender,facing:view.facing,pose:view.pose,mode:view.action==='run'?'run':'walk'})});effects.push(()=>drawReaction(c,foot.x,foot.y,hero));
 sorted.sort((a,b)=>a.depth-b.depth).forEach(o=>o.draw());
 // Only the contacted blades overlap shoes; grass elsewhere stays on the ground.
 if(activeGrass)draw(`grass.front.${grassFrame}`,actorCell.x*32,actorCell.y*32);
 effects.forEach(draw=>draw());
 // Direction plaques sit in the landscape and remain readable at its north/south thresholds.
 c.restore();const lighting=applyLighting(c,state);return {lighting,camera,width:480,height:320,scene:state.scene,atlas:'assets/playable/overworld/master.png',activeGrass,grassFrame,visibleObjects:sorted.length};
}
