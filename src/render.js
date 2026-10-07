import {loadEnvironment,renderEnvironment} from './environment-render.js';
// Native, appearance-only exploration renderer. Collision and interaction live
// in world.js; sprite bounds and transparency never decide a walkable cell.
import { loadAtlas } from './atlas.js';
import { scenes, buildings, getEntities } from './world.js';
let atlas, entries;
export async function initWorldArt() {
  atlas = await loadAtlas(new URL('../assets/playable/atlas.json', import.meta.url));
  entries = new Map(atlas.manifest.assets.map(a => [a.id, a]));
  await loadEnvironment();
}
function sprite(c, id, x, y) {
  const a = entries.get(id);
  if (!a) throw new Error(`Missing exploration art: ${id}`);
  atlas.draw(c, id, x - a.anchor[0], y - a.anchor[1]);
}
export function character(c, x, y, {gender='boy',look, facing='down',pose='idle',mode='walk'}={}) {
  const who = look || `hero.${gender}`;
  sprite(c, `char.${who}.${facing}.${mode}.${pose}`, x, y);
}
let debug = {};
export function getRenderDebug() { return structuredClone(debug); }
export function renderWorld(canvas, state, time, view) {
  const c = canvas.getContext('2d');
  c.imageSmoothingEnabled = false;
  if(scenes[state.scene].map) { debug=renderEnvironment(c,state,time,view,character,(e,g)=>e.look==='rival'?`hero.${g==='boy'?'girl':'boy'}`:e.look); return; }
  c.save(); c.scale(2,2);
  const scene = scenes[state.scene], outside = ['town','yard'].includes(scene.style);
  // Camera tracks the integer rendered foot position directly, without easing.
  const camera = {x: view.x - 120, y: view.y - 88};
  debug = {camera, width:canvas.width,height:canvas.height, scene:state.scene, atlas:atlas.manifest.image};
  c.fillStyle = outside ? '#446749' : '#223038'; c.fillRect(0,0,240,160);
  c.save(); c.translate(-camera.x,-camera.y);
  const tile = (id,x,y) => atlas.draw(c,id,x*16,y*16);
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
    if(scene.style !== 'shop') sprite(c,'rug',8*16,8*16);
  }
  const drawables=[], effects=[];
  const add=(depth, draw) => drawables.push({depth,draw});
  const prop = (o,id=o.sprite) => sprite(c,id,(o.x+o.w/2)*16,(o.y+o.h)*16);
  for(const o of scene.objects) {
    if(o.kind==='pond') { for(let y=o.y;y<o.y+o.h;y++) for(let x=o.x;x<o.x+o.w;x++) tile('ground.water',x,y); continue; }
    if(o.kind==='tree') {
      prop(o,'tree.trunk');
      add((o.y+o.h)*16,()=>prop(o,'tree.canopy')); continue;
    }
    let id=o.sprite;
    if(o.kind==='tank'&&state.scene==='bedroom'&&state.stage==='night')
      id=['broken','kaid'].includes(state.storyBeat)?'prop.tank.broken':'prop.tank.night';
    if(o.kind==='leaves') prop(o,id);
    else add((o.y+o.h)*16,()=>prop(o,id));
  }
  if(scene.style==='town') for(const b of buildings) add((b.y+b.h)*16,()=>prop(b));
  if(scene.visualHouse) add((scene.visualHouse.y+scene.visualHouse.h)*16,()=>prop(scene.visualHouse));
  for(const e of getEntities(state)) {
    if(e.type==='npc') add(e.y*16,()=>character(c,e.x*16,e.y*16,{look:e.look==='rival'?`hero.${state.gender==='boy'?'girl':'boy'}`:e.look}));
    else if(e.type==='rescue') effects.push(()=>sprite(c,'rescue.sparkle',e.x*16,e.y*16-(Math.floor(time*2)%2)));
    else if(e.id==='townSign'||e.type==='route') add(e.y*16,()=>sprite(c,e.type==='route'?'sign.route':'sign.town',e.x*16,e.y*16));
    else if(e.type==='door'&&!outside) {
      // Threshold decoration shares the authored entity anchor, never its bounds.
      const id=e.id==='stairs'?(state.scene==='bedroom'?'stairs.down':'stairs.up'):'door.interior';
      sprite(c,id,e.x*16,e.y*16);
    }
  }
  if(state.stage==='night'&&state.scene==='bedroom') {
    if(['mom','broken','kaid'].includes(state.storyBeat)) add(6*16,()=>character(c,11*16,6*16,{look:'mom'}));
    if(state.storyBeat==='kaid') add(8*16,()=>character(c,12*16,8*16,{look:'kaid'}));
  }
  add(view.y,()=>character(c,view.x,view.y,{gender:state.gender,facing:view.facing,pose:view.pose,mode:view.action==='run'?'run':'walk'}));
  drawables.sort((a,b)=>a.depth-b.depth).forEach(o=>o.draw());
  effects.forEach(draw=>draw());
  c.restore();
  if(state.stage==='night') { c.fillStyle='#1e244b38';c.fillRect(0,0,240,160); }
  c.restore();
}
