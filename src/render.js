import {loadEnvironment,renderEnvironment} from './environment-render.js';
// Native, appearance-only exploration renderer. Collision and interaction live
// in world.js; sprite bounds and transparency never decide a walkable cell.
import { loadAtlas } from './atlas.js';
import { scenes, buildings, getEntities } from './world.js';
import {loadLivingArt,drawLiving,characterFrame,npcIdentity,drawHabitatProp,drawCritter,RESCUES} from './living-art.js';
import {drawThreshold,applyLighting} from './lighting.js';
let atlas, entries;
export async function initWorldArt() {
  atlas = await loadAtlas(new URL('../assets/playable/atlas.json', import.meta.url));
  entries = new Map(atlas.manifest.assets.map(a => [a.id, a]));
  await Promise.all([loadEnvironment(),loadLivingArt()]);
}
function sprite(c, id, x, y) {
  const a = entries.get(id);
  if (!a) throw new Error(`Missing exploration art: ${id}`);
  atlas.draw(c, id, x - a.anchor[0], y - a.anchor[1]);
}
export function character(c, x, y, {gender='boy',look, facing='down',pose='idle',mode='walk'}={}) {
  if(look?.startsWith('legacy.')) { c.save();c.translate(x,y);c.scale(2,2);sprite(c,`char.${look.slice(7)}.${facing}.${mode}.${pose}`,0,0);c.restore();return; }
  drawLiving(c,look||`hero-${gender}`,characterFrame(facing,pose),x-16,y-64);
}
let debug = {};
export function getRenderDebug() { return structuredClone(debug); }
export function renderWorld(canvas, state, time, view) {
  const c = canvas.getContext('2d');
  c.imageSmoothingEnabled = false;
  if(scenes[state.scene].map) { debug=renderEnvironment(c,state,time,view,character,npcIdentity); return; }
  c.save();
  const scene = scenes[state.scene], outside = ['town','yard'].includes(scene.style);
  // Camera tracks the integer rendered foot position directly, without easing.
  const camera = {x: view.x*2 - 240, y: view.y*2 - 176};
  debug = {camera, width:canvas.width,height:canvas.height, scene:state.scene, atlas:atlas.manifest.image};
  c.fillStyle = outside ? '#446749' : '#223038'; c.fillRect(0,0,480,320);
  c.save(); c.translate(-camera.x,-camera.y);
  const oldSprite=(id,x,y)=>{c.save();c.translate(x,y);c.scale(2,2);sprite(c,id,0,0);c.restore();};
  const tile = (id,x,y) => {c.save();c.scale(2,2);atlas.draw(c,id,x*16,y*16);c.restore();};
  const path = (x,y) => scene.style === 'yard' ? (x===7 || x===8) :
    [8,9,17,18,25].includes(y) || [9,10,19,20].includes(x) ||
    buildings.some(b => x===b.x+3 && y>=b.y+5 && y<=b.y+6);
  for (let y=0;y<scene.h;y++) for(let x=0;x<scene.w;x++) {
    if (outside) tile(path(x,y)?'ground.path':'ground.grass',x,y);
    else tile(y===0?'wall.interior.upper':y<3?'wall.interior':x===0?'wall.interior.side':scene.style==='shop'?'floor.tile':'floor.wood',x,y);
  }
  if (outside) {
    for(let x=0;x<scene.w;x++) { tile('fence.horizontal',x,0); if (x!==7&&x!==8) tile('fence.horizontal',x,scene.h); }
    for(let y=1;y<scene.h-1;y++) { tile('fence.vertical',0,y); tile('fence.vertical',scene.w,y); }
  } else {
    for(let y=0;y<scene.h;y++) tile('wall.interior.side',scene.w,y);
    if(scene.style !== 'shop') oldSprite('rug',8*32,8*32);
  }
  const drawables=[], effects=[];
  const add=(depth, draw) => drawables.push({depth,draw});
  const prop = (o,id=o.sprite) => {const x=(o.x+o.w/2)*32,y=(o.y+o.h)*32;
    if(o.kind==='tank'&&id!=='prop.tank.broken')drawHabitatProp(c,'terrarium',x,y);else oldSprite(id,x,y);};
  for(const o of scene.objects) {
    if(o.kind==='pond') { for(let y=o.y;y<o.y+o.h;y++) for(let x=o.x;x<o.x+o.w;x++) tile('ground.water',x,y); continue; }
    if(o.kind==='tree') {
      prop(o,'tree.trunk');
      add((o.y+o.h)*32,()=>prop(o,'tree.canopy')); continue;
    }
    let id=o.sprite;
    if(o.kind==='tank'&&state.scene==='bedroom'&&state.stage==='night')
      id=['broken','kaid'].includes(state.storyBeat)?'prop.tank.broken':'prop.tank.night';
    if(o.kind==='leaves') prop(o,id);
    else add((o.y+o.h)*32,()=>prop(o,id));
  }
  if(scene.style==='town') for(const b of buildings) add((b.y+b.h)*32,()=>prop(b));
  if(scene.visualHouse) add((scene.visualHouse.y+scene.visualHouse.h)*32,()=>prop(scene.visualHouse));
  for(const e of getEntities(state)) {
    if(e.type==='npc') add(e.y*32,()=>character(c,e.x*32,e.y*32,{look:npcIdentity(e,state.gender)}));
    else if(e.type==='rescue') add(e.y*32,()=>drawCritter(c,RESCUES[e.id],e.x*32-16,e.y*32-32,time));
    else if(e.id==='townSign'||e.type==='route') add(e.y*32,()=>oldSprite(e.type==='route'?'sign.route':'sign.town',e.x*32,e.y*32));
    else if(e.type==='door'&&!outside) {
      // Threshold decoration shares the authored entity anchor, never its bounds.
      if(e.id==='stairs')oldSprite(state.scene==='bedroom'?'stairs.down':'stairs.up',e.x*32,e.y*32);
      else drawThreshold(c,e,state.scene,state);
    }
  }
  if(state.stage==='night'&&state.scene==='bedroom') {
    if(['mom','broken','kaid'].includes(state.storyBeat)) add(6*32,()=>character(c,11*32,6*32,{look:'mom'}));
    if(state.storyBeat==='kaid') add(8*32,()=>character(c,12*32,8*32,{look:'kaid'}));
  }
  add(view.y*2,()=>character(c,view.x*2,view.y*2,{gender:state.gender,facing:view.facing,pose:view.pose,mode:view.action==='run'?'run':'walk'}));
  if(state.scene==='glass')for(const [type,x]of [['aquarium',4],['paludarium',12]])add(5*32,()=>drawHabitatProp(c,type,x*32,5*32));
  if(state.scene==='vet')for(const [id,x]of [['gecko',4],['snail',11]])if(state.flags.rescued.includes(id))add(5*32,()=>drawCritter(c,RESCUES[id],x*32,4*32,time));
  drawables.sort((a,b)=>a.depth-b.depth).forEach(o=>o.draw());
  effects.forEach(draw=>draw());
  c.restore();
  debug.lighting=applyLighting(c,state,true);
  c.restore();
}
