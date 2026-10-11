import {loadContactArt,drawContactArt,contactArtInfo,contactEntry,contactFrontiers} from './contact-art.js';
import {fruitTreeView,APPLE_POSITIONS} from './fruit-trees.js';
import {worldFoot,CAMERA_FOCUS_Y} from './world-space.js';
import {actorView,drawReaction} from './actors.js';
import {drawCritter,RESCUES} from './living-art.js';
import {applyLighting} from './lighting.js';
import {scenes,getEntities} from './world.js';
import {TICK_SECONDS} from './movement.js';
let sheet,manifest,tiles;
export async function loadEnvironment(){
 await loadContactArt();
 const url=new URL('../assets/playable/overworld/master.json',import.meta.url),response=await fetch(url);
 if(!response.ok)throw Error('Overworld manifest failed to load');manifest=await response.json();
 sheet=new Image();sheet.src=new URL(manifest.image,url).href;await sheet.decode();
 if(sheet.width!==manifest.imageWidth||sheet.height!==manifest.imageHeight)throw Error('Overworld sheet dimensions do not match');
 tiles=new Map(manifest.tiles.map(t=>[t.id,t]));
 for(const [sceneId,scene]of Object.entries(scenes)){if(!scene.map)continue;const map=scene.map;
  for(const id of [...map.ground,...map.decals.map(d=>d.id),...map.objects.flatMap(o=>o.tiles?o.tiles.flat():manifest.assemblies[o.id]?.flat()||[o.id])])if(!tiles.has(id))throw Error(`Missing tile ${id} in ${sceneId}`);
 }
}
export function drawEnvironmentTile(c,id,x,y){
 const t=tiles.get(id);if(!t)throw Error(`Missing environment tile ${id}`);
 c.drawImage(sheet,t.x,t.y,32,32,Math.round(x),Math.round(y),32,32);
}
export function animationFrame(id,time,phase=0){
 const frame=Math.floor(time/(16*TICK_SECONDS)+phase)%4;
 if(id.startsWith('water.')&&/^water\.\d+$/.test(id))return frame?`anim.${id}.${frame}`:id;
 if(id.startsWith('flowers.')){const f=[0,1,0,2][frame];return f?`anim.${id}.${f}`:id;}
 if(id.startsWith('waterfall.0.'))return frame?`anim.waterfall.${id.split('.')[2]}.${frame}`:id;
 return id;
}
export function renderEnvironment(c,state,time,view,character,npcLook){
 const map=scenes[state.scene].map,foot=worldFoot(view.x,view.y);
 const {width,height}=c.canvas;
 const axis=(size,field,focus)=>size<field?Math.floor((size-field)/2):Math.max(0,Math.min(size-field,focus));
 const camera={x:axis(map.w*32,width,foot.x-Math.floor(width/2)),y:axis(map.h*32,height,foot.y-Math.round(height*CAMERA_FOCUS_Y/320))};
 c.imageSmoothingEnabled=false;c.fillStyle='#487b59';c.fillRect(0,0,width,height);c.save();c.translate(-camera.x,-camera.y);
 const visible=(x,y,w=1,h=1)=>x*32<camera.x+width+32&&(x+w)*32>camera.x-32&&y*32<camera.y+height+32&&(y+h)*32>camera.y-64;
 const draw=(id,x,y,phase=0)=>{const a=tiles.get(animationFrame(id,time,phase));if(!a)throw Error('Missing environment tile '+id);c.drawImage(sheet,a.x,a.y,32,32,Math.round(x),Math.round(y),32,32);};
 const assembly=(o)=>{if(o.collision){drawContactArt(c,`${state.scene}:${map.objects.indexOf(o)}${o.id==='mill.wheel.0'?':phase'+Math.floor(time/.18)%4:''}`.replace(':phase0',''),o.x*32,o.y*32);return;}const attached=map.objects.find(b=>b.kind==='building'&&o.x>=b.x&&o.x<b.x+b.w&&(o.id==='chimney'&&o.y===b.y-1||o.id.startsWith('shop.sign.')&&o.y===b.y+3)),fountain=map.objects.find(b=>b.id==='fountain.small'&&o.id==='fountain.jet'&&o.x===b.x+1&&o.y===b.y),parent=attached||fountain,offset=parent?contactEntry(`${state.scene}:${map.objects.indexOf(parent)}`).dy:0;const objectId=o.id==='mill.wheel.0'?`mill.wheel.${Math.floor(time/.18)%4}`:o.id;const rows=o.tiles||manifest.assemblies[objectId];if(rows)rows.forEach((row,j)=>row.forEach((id,i)=>draw(id,(o.x+i)*32,(o.y+j)*32+offset)));else draw(o.id,o.x*32,o.y*32+offset);};
 // A wide/tall viewport can look beyond a small map. Existing dense forest
 // art marks that non-playable backdrop instead of exposing a flat clear field.
 if(camera.x<0||camera.y<0||camera.x+width>map.w*32||camera.y+height>map.h*32){
  c.save();c.beginPath();c.rect(camera.x,camera.y,width,height);c.rect(0,0,map.w*32,map.h*32);c.clip('evenodd');
  for(let y=Math.floor(camera.y/32)*32;y<camera.y+height;y+=32)for(let x=Math.floor(camera.x/32)*32;x<camera.x+width;x+=32)draw('meadow.grass.0',x,y);
  const rows=manifest.assemblies['tree.broadleaf'];
  for(let y=Math.floor(camera.y/64)*64-32;y<camera.y+height;y+=48)for(let x=Math.floor(camera.x/64)*64;x<camera.x+width;x+=64)rows.forEach((row,j)=>row.forEach((id,i)=>draw(id,x+i*32,y+j*32)));
  c.restore();
 }
 const drawActor=(x,y,options)=>{c.save();c.translate(x,y);character(c,0,0,options);c.restore();};
 for(let y=Math.max(0,Math.floor(camera.y/32));y<Math.min(map.h,Math.ceil((camera.y+height)/32));y++)for(let x=Math.max(0,Math.floor(camera.x/32));x<Math.min(map.w,Math.ceil((camera.x+width)/32));x++)draw(map.terrain[y*map.w+x]==='water'?'meadow.grass.0':map.ground[y*map.w+x],x*32,y*32);
 for(let y=Math.max(0,Math.floor(camera.y/32)-1);y<Math.min(map.h,Math.ceil((camera.y+height)/32));y++)for(let x=Math.max(0,Math.floor(camera.x/32));x<Math.min(map.w,Math.ceil((camera.x+width)/32));x++)if(map.terrain[y*map.w+x]==='water'){let mask=0;for(const [dx,dy,b]of [[0,-1,1],[1,0,2],[0,1,4],[-1,0,8],[1,-1,16],[1,1,32],[-1,1,64],[-1,-1,128]])if(map.terrain[(y+dy)*map.w+x+dx]==='water')mask|=b;for(const [b,a,d]of [[16,1,2],[32,2,4],[64,4,8],[128,8,1]])if(!(mask&a)||!(mask&d))mask&=~b;const phase=Math.floor(time/(16*TICK_SECONDS))%4;drawContactArt(c,`terrain:water:${mask}${phase?':'+phase:''}`,x*32,y*32);}
 const actorCell={x:Math.floor(foot.x/32),y:Math.floor((foot.y-1)/32)};
 const activeGrass=map.grass.has(`${actorCell.x},${actorCell.y}`),grassFrame=view.moving?[1,3,2,3][Math.floor((view.actionTick||0)/3)%4]:0;
 for(const d of map.decals){if(!visible(d.x,d.y))continue;let id=d.id;if(id==='grass.living.0'&&d.x===actorCell.x&&d.y===actorCell.y)id=`grass.living.${grassFrame}`;draw(id,d.x*32,d.y*32,d.id.startsWith('flowers.')?(d.x+d.y)%4:0);}
 const drawFruitTree=(o)=>{
  const v=fruitTreeView(state,o.fruitId,time),id=`${state.scene}:${map.objects.indexOf(o)}${v.ripe?':ripe':''}`,a=contactEntry(id),x=o.x*32,y=o.y*32,base=y+a.contact.y+a.contact.h;
  c.save();c.beginPath();c.rect(x-2,y-32,a.w+4,base-y+32-12);c.clip();drawContactArt(c,id,x+v.shake,y);c.restore();
  c.save();c.beginPath();c.rect(x,base-12,a.w,12);c.clip();drawContactArt(c,id,x,y);c.restore();
  if(v.falling)effects.push(()=>{for(const [i,[px,py]]of APPLE_POSITIONS.entries()){const fall=Math.max(0,Math.min(1,(v.age-.18)/.48)),bounce=v.age>.66&&v.age<.86?Math.round(Math.sin((v.age-.66)/.2*Math.PI)*4):0;draw('fruit.apple',x+px-16+(fall?Math.round((i-1)*5*fall):v.shake),y+a.dy+py-16+Math.round((62-py)*fall*fall)-bounce);}});
 };

 const effects=[],sorted=[];for(const o of contactFrontiers(state.scene))if(visible(o.x,o.y))sorted.push({depth:(o.y+1)*32,draw:()=>drawContactArt(c,o.id,o.x*32,o.y*32)});for(const o of map.objects)if(visible(o.x,o.y,o.w,o.h))sorted.push({depth:o.depth*32,draw:()=>{if(o.fruitId)drawFruitTree(o);else assembly(o);if(o.id==='fountain.jet'){const parent=map.objects.find(b=>b.id==='fountain.small'&&o.x===b.x+1&&o.y===b.y),dy=parent?contactEntry(`${state.scene}:${map.objects.indexOf(parent)}`).dy:0;draw(`water.spray.${Math.floor(time/.18)%4}`,o.x*32,(o.y+1)*32+dy);}}});
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
 c.restore();const lighting=applyLighting(c,state);return {lighting,camera,playerFoot:foot,width,height,scene:state.scene,atlas:'assets/playable/overworld/master.png',contact:contactArtInfo(),activeGrass,grassFrame,visibleObjects:sorted.length};
}
