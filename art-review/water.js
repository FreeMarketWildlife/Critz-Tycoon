import {loadCloudArt,cloudsVisible,cloudSun} from '../src/water-clouds.js';
import {surface,footstepRipples,neighborMask,RIPPLE_SECONDS} from '../src/water-surfaces.js';
import {loadWaterTerrain,maskPath,drawRipples,drawReflection,drawSky} from '../src/water-effects.js';
import {createMotion,getMotionView,advanceMotion,createMotionClock,advanceMotionClock,resetMotionClock} from '../src/movement.js';
import {initWorldArt,character} from '../src/render.js';
import {drawEnvironmentTile} from '../src/environment-render.js';
import {createState} from '../src/state.js';
import {ensureDayClock,advanceDayClock,endDay,paintClock,displayedMinute} from '../src/day-clock.js';
import {applyLighting} from '../src/lighting.js';
import {WATER_FRAMES,WATER_FRAME_SECONDS,loadWaterArt,createTurtle,updateTurtle,turtleOffset,fishPose} from '../src/water-wildlife.js';
import {readRenderSettings,saveRenderSettings} from '../src/render-settings.js';
const canvas=document.querySelector('#pond'),c=canvas.getContext('2d'),state=createState('Hero','boy','River');state.stage='morning';ensureDayClock(state);
let player={x:2,y:7,facing:'up'},motion=createMotion(player);const motionClock=createMotionClock();
const hero={x:80,y:256,facing:'up'},turtles=[createTurtle(176,176),createTurtle(336,240)],down=new Set(),renderSettings=readRenderSettings(localStorage);
let cloudArt,weather='sunny';
let terrain,identity='fresh',ground='grass',ripples=[],steps=0,reflectionVisible=false;
let time=0,last=performance.now(),paused=false,speed=1,calm=matchMedia('(prefers-reduced-motion: reduce)').matches,draw,ready=false;
const $=id=>document.getElementById(id),message=s=>$('message').textContent=s;
function waterType(x,y){if(x>=1&&x<=3&&y>=8&&y<=9)return 'shallow-still';if(x>=4&&x<=13&&y>=4&&y<=8&&!((x===4||x===13)&&y===4))return x<7?'shallow-still':x<10?'still':x<12?'shallow-moving':'moving';return null;}
function water(x,y){return !!waterType(x,y);}
function cellSurface(x,y){const t=waterType(x,y);return t?surface(t,identity):null;}
function walkable(x,y){const s=cellSurface(x,y);return x>=0&&x<15&&y>=1&&y<10&&(!s||s.shallow)&&!(x===2&&(y===2||y===3))&&!turtles.some(t=>Math.floor(t.x/32)===x&&Math.floor(t.y/32)===y);}
function cells(){const result=[];for(let y=0;y<10;y++)for(let x=0;x<15;x++)if(water(x,y))result.push({x,y,surface:cellSurface(x,y),mask:neighborMask(x,y,(xx,yy)=>water(xx,yy))});return result;}
function visit(x,y){player={x,y,facing:'down'};motion=createMotion(player);down.clear();resetMotionClock(motionClock);syncHero();}
$('identity').onclick=()=>{identity=identity==='fresh'?'ocean':'fresh';$('identity').textContent=identity==='fresh'?'Freshwater · Reflective':'Ocean · No character reflections';};
$('ground').onchange=e=>ground=e.target.value;
$('weather').onchange=e=>weather=e.target.value;
for(const b of document.querySelectorAll('[data-visit]'))b.onclick=()=>{const [x,y]=b.dataset.visit.split(',').map(Number);visit(x,y);};
function syncHero(){const v=getMotionView(motion);Object.assign(hero,{x:v.x*2+16,y:v.y*2+32,facing:v.facing});return v;}
function sleep(forced=false){if(!forced&&Math.hypot(hero.x-80,hero.y-108)>55){message('Walk beside the bed in the upper-left corner first.');return;}endDay(state);speed=1;$('speed').textContent='Speed · 1×';player={x:2,y:4,facing:'down'};motion=createMotion(player);resetMotionClock(motionClock);down.clear();syncHero();message(forced?'You fell asleep at 2:00am and woke safely in bed at 6:00am. No fee.':'Good morning! You woke in bed at 6:00am.');}
for(const button of document.querySelectorAll('[data-dir]')){button.onpointerdown=e=>{e.preventDefault();button.setPointerCapture(e.pointerId);down.add(button.dataset.dir);};button.onpointerup=button.onpointercancel=()=>down.delete(button.dataset.dir);}
const keys={ArrowUp:'up',ArrowDown:'down',ArrowLeft:'left',ArrowRight:'right'};
addEventListener('keydown',e=>{if(keys[e.key]&&e.target.tagName!=='INPUT'){e.preventDefault();down.add(keys[e.key]);}if(e.key.toLowerCase()==='a')sleep();});addEventListener('keyup',e=>down.delete(keys[e.key]));
function clear(){down.clear();last=performance.now();resetMotionClock(motionClock);}addEventListener('blur',clear);document.addEventListener('visibilitychange',clear);
$('sleep').onclick=()=>sleep();$('pause').onclick=()=>{paused=!paused;$('pause').textContent=paused?'Resume':'Pause';};$('speed').onclick=()=>{speed=speed===1?60:1;$('speed').textContent=`Speed · ${speed}×`;};
function setTime(value){const m=Number(value);state.dayClock.minute=Math.floor(m/10)*10;state.dayClock.remainder=(m%10)*1.4;}
for(const b of document.querySelectorAll('[data-minute]'))b.onclick=()=>setTime(b.dataset.minute);$('time').oninput=e=>setTime(e.target.value);
$('calm').onclick=()=>{calm=!calm;$('calm').textContent=`Calm · ${calm?'On':'Off'}`;};$('calm').textContent=`Calm · ${calm?'On':'Off'}`;
function showShadows(){$('shadows').textContent=`Shadows · ${renderSettings.shadows?'On':'Off'}`;}showShadows();$('shadows').onclick=()=>{renderSettings.shadows=!renderSettings.shadows;try{saveRenderSettings(localStorage,renderSettings);}catch{message('Shadow preference could not be saved.');}showShadows();};
// Cast shadows are a separate, independently clearable native raster.
const shadow=document.createElement('canvas');shadow.width=480;shadow.height=320;const sc=shadow.getContext('2d');
const actor=document.createElement('canvas');actor.width=32;actor.height=64;const ac=actor.getContext('2d');ac.imageSmoothingEnabled=false;
function render(){c.imageSmoothingEnabled=false;
 const all=cells(),wet=maskPath(all),still=maskPath(all,s=>s.reflective&&!s.moving),moving=maskPath(all,s=>s.reflective&&s.moving),f=calm?0:Math.floor(time/WATER_FRAME_SECONDS)%WATER_FRAMES;
 for(let y=0;y<10;y++)for(let x=0;x<15;x++)drawEnvironmentTile(c,'meadow.grass.0',x*32,y*32);
 for(const cell of all){const {x,y,surface:s,mask}=cell,id=`${identity}.${s.type}`;terrain.draw(c,`join.${id}.${ground}.${mask}`,x*32,y*32);c.save();c.clip(maskPath([cell]));const other=[[0,-1],[1,0],[0,1],[-1,0]].map(([dx,dy])=>waterType(x+dx,y+dy)).find(t=>t&&t!==s.type);if(other){const typeMask=neighborMask(x,y,(xx,yy)=>waterType(xx,yy)===s.type);terrain.draw(c,`${identity}.${other}.${f}`,x*32,y*32);c.save();c.clip(maskPath([{...cell,mask:typeMask}]));terrain.draw(c,`${id}.${f}`,x*32,y*32);c.restore();}else terrain.draw(c,`${id}.${f}`,x*32,y*32);c.restore();}
 drawSky(c,time,displayedMinute(state.dayClock),wet,calm,cloudArt,weather);
 ac.clearRect(0,0,32,64);character(ac,16,64,{gender:'boy',facing:hero.facing,pose:calm?'idle':getMotionView(motion).pose});const pixels=ac.getImageData(0,0,32,64);for(let i=0;i<pixels.data.length;i+=4){pixels.data[i]=Math.round(pixels.data[i]*.68+147*.32);pixels.data[i+1]=Math.round(pixels.data[i+1]*.68+200*.32);pixels.data[i+2]=Math.round(pixels.data[i+2]*.68+213*.32);}ac.putImageData(pixels,0,0);
 drawReflection(c,{image:actor,x:hero.x,y:hero.y},still,time,false);drawReflection(c,{image:actor,x:hero.x,y:hero.y},moving,calm?0:time,true);
 reflectionVisible=identity==='fresh'&&all.some(cell=>hero.x>=cell.x*32&&hero.x<(cell.x+1)*32&&hero.y<(cell.y+1)*32&&hero.y+64>cell.y*32);
 for(const {x,y,surface:s,mask} of all)terrain.draw(c,`bank.${identity}.${s.type}.${ground}.${mask}`,x*32,y*32);
 drawRipples(c,ripples,time,wet);
 // Original compact bed, visibly located outside the pond's blocked cells.
 c.fillStyle='#503f38';c.fillRect(62,62,36,46);c.fillStyle='#c89665';c.fillRect(64,64,32,40);c.fillStyle='#ded8b9';c.fillRect(67,66,26,9);c.fillStyle='#629699';c.fillRect(66,77,28,25);c.fillStyle='#84b9b0';c.fillRect(68,78,24,5);
 sc.clearRect(0,0,480,320);if(renderSettings.shadows){sc.fillStyle='#17343a';sc.fillRect(Math.round(hero.x)-8,Math.round(hero.y)-2,16,3);for(const t of turtles)sc.fillRect(t.x-10,t.y+8,24,5);c.save();c.globalAlpha=.25;c.drawImage(shadow,0,0);c.restore();}
 for(const t of turtles){draw(c,'rock',t.x-16,t.y-16);const v=calm?{x:0,y:0,visible:!(['sliding','submerged'].includes(t.phase))}:turtleOffset(t);if(v.visible){c.save();c.translate(t.x+v.x,t.y+v.y);c.rotate(Math.PI/2);draw(c,`turtle.${calm?0:Math.floor(t.age*8)%4}`,-16,-16);c.restore();}if(t.phase==='submerged'&&t.age<.8&&!calm)draw(c,`splash.${Math.min(3,Math.floor(t.age*5))}`,t.x+6,t.y-3);}
 for(let i=0;i<3;i++){const p=fishPose(time,i,displayedMinute(state.dayClock),calm);if(p){const x=197+i*42+p.x,y=210+p.y;draw(c,`fish.${p.frame}`,x,y);if(p.splash)draw(c,'splash.2',x,210);}}
 character(c,Math.round(hero.x),Math.round(hero.y),{gender:'boy',facing:hero.facing,pose:calm?'idle':getMotionView(motion).pose});
 applyLighting(c,state);
 // Local night illumination: hard-pixel concentric rings, separate from cast shadows.
 const h=displayedMinute(state.dayClock)/60;if(h>=20){c.save();for(let r=42;r>=10;r-=8){c.fillStyle='rgba(255,204,116,.045)';for(let yy=-r;yy<=r;yy+=2){const w=Math.floor(Math.sqrt(r*r-yy*yy));c.fillRect(80-w,84+yy,w*2,2);}}c.restore();}
 paintClock($('day-clock'),state,paused);if(document.activeElement!==$('time'))$('time').value=displayedMinute(state.dayClock);
}
function frame(now){const elapsed=Math.max(0,(now-last)/1000),dt=Math.min(.1,elapsed);last=now;if(ready&&!document.hidden){if(!paused&&document.hasFocus()){
 time+=dt;advanceMotionClock(motionClock,elapsed,()=>{const before=`${player.x},${player.y}`;advanceMotion(motion,down,false,walkable,{runAllowed:true});if(before!==`${player.x},${player.y}`){steps++;const s=cellSurface(player.x,player.y);if(footstepRipples(s)&&!calm)ripples.push({x:player.x*32+16,y:player.y*32+29,time});}});syncHero();ripples=ripples.filter(r=>time-r.time<RIPPLE_SECONDS);
 for(const t of turtles)updateTurtle(t,hero,dt,{calm});if(advanceDayClock(state,dt*speed))sleep(true);
 }else resetMotionClock(motionClock);render();}requestAnimationFrame(frame);}
try{await initWorldArt();draw=await loadWaterArt();terrain=await loadWaterTerrain();cloudArt=await loadCloudArt();ready=true;requestAnimationFrame(frame);}catch(e){message(`Artwork could not load: ${e.message}`);}
export function getWaterReview(){return structuredClone({state,hero,player,movement:getMotionView(motion),turtles,time,paused,speed,calm,shadows:renderSettings.shadows,identity,ground,weather,cloudsVisible:cloudsVisible(displayedMinute(state.dayClock),weather),cloudSun:cloudSun(displayedMinute(state.dayClock)),ripples,steps,reflectionVisible,cells:cells(),ready});}
