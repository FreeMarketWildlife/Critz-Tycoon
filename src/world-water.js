import {isWater,waterSurface} from '../map-editor/model.js';
import {compileCoastalField} from './coastal-format.js';
import {createCoastalDrawing,coastalFieldPath,drawCoastalBoundary} from './coastal-drawing.js';
import {surface,footstepRipples,ripplePose,RIPPLE_SECONDS} from './water-surfaces.js';
import {loadCloudArt,cloudsVisible} from './water-clouds.js';
import {displayedMinute} from './day-clock.js';
const cache=new WeakMap();let water,cloud,sand,actorCanvas;
export async function loadWorldWater(){
 const url=new URL('../assets/review/coastal-format/water.json',import.meta.url),m=await(await fetch(url)).json(),im=new Image();im.src=new URL(m.image,url);await im.decode();
 const entries=new Map(m.assets.map(a=>[a.id,a]));water={draw(c,id,x,y){const a=entries.get(id);if(!a)throw Error('Missing water '+id);c.drawImage(im,a.x,a.y,a.w,a.h,x,y,a.w,a.h);}};cloud=await loadCloudArt();const propsUrl=new URL('../assets/review/coastal-format/props.json',import.meta.url),props=await(await fetch(propsUrl)).json(),propsImage=new Image();propsImage.src=new URL(props.image,propsUrl);await propsImage.decode();sand={manifest:props,image:propsImage};
}
export function drawSand(c,x,y,variant=0){const a=sand.manifest.assets.find(a=>a.id===`sand.${variant%4}`);c.drawImage(sand.image,a.x,a.y,a.w,a.h,x,y,32,32);}
function drawing(map){
 const signature=map.terrain.join(',');
 if(cache.get(map)?.signature===signature)return cache.get(map);
 const cells=[];for(let y=0;y<map.h;y++)for(let x=0;x<map.w;x++)if(isWater(map.terrain[y*map.w+x])){const tile=waterSurface(map.terrain[y*map.w+x]);cells.push({x,y,surface:surface(tile.type,tile.identity)});}
 const byCell=new Map(cells.map(a=>[`${a.x},${a.y}`,a]));
 const d=createCoastalDrawing(compileCoastalField(cells,map.w*32,map.h*32+32),(x,y)=>{const xx=Math.floor(x/32),yy=Math.floor((y-16)/32),cell=byCell.get(`${xx},${yy}`),beach=[[-1,0],[1,0],[0,-1],[0,1]].some(([dx,dy])=>map.terrain[(yy+dy)*map.w+xx+dx]==='sand');return {ground:beach?'sand':'grass',shallow:!!cell?.surface.shallow,moving:!!cell?.surface.moving};});
 d.freshPath=cells.every(a=>a.surface.identity==='fresh')?d.path:coastalFieldPath(compileCoastalField(cells.filter(a=>a.surface.identity==='fresh'),map.w*32,map.h*32+32));
 d.deepPath=cells.some(a=>a.surface.shallow)?coastalFieldPath(compileCoastalField(cells.filter(a=>!a.surface.shallow),map.w*32,map.h*32+32,{sideInset:5,verticalInset:5})):null;
 d.cells=cells;d.byCell=byCell;d.ripples=[];d.lastPositions=[];d.signature=signature;cache.set(map,d);return d;
}
export function drawWorldWater(c,map,state,time,actors,character){
 if(!map.terrain.some(isWater))return {cells:0};
 const d=drawing(map),f=Math.floor(time/.1)%32,minute=displayedMinute(state.dayClock),identity=map.waterIdentity||'fresh';
 c.save();c.clip(d.path);
 for(const a of d.cells)water.draw(c,`${a.surface.identity}.${(d.deepPath&&!a.surface.shallow?'shallow-'+a.surface.type:a.surface.type)}.${f}`,a.x*32,a.y*32+16);
 if(d.deepPath){c.save();c.clip(d.deepPath);for(const a of d.cells.filter(a=>!a.surface.shallow))water.draw(c,`${a.surface.identity}.${a.surface.type}.${f}`,a.x*32,a.y*32+16);c.restore();}
 if(minute>=1260){for(let i=0;i<70;i++){c.fillStyle=i%3?'#acd5da':'#e5eacb';c.fillRect((i*83+31)%(map.w*32),(i*57+126)%(map.h*32),2,2);}}
 else if(cloudsVisible(minute,'sunny')){c.save();c.globalAlpha=.52;for(let i=0;i<6;i++)cloud.draw(c,i%3,minute,Math.round(((map.w*32+i*181-time*9)%(map.w*32+200)))-96,140+i*66);c.restore();}
 for(const [i,a] of actors.entries()){const x=Math.floor(a.x/32),y=Math.floor((a.y-1)/32),key=`${x},${y}`;if(d.lastPositions[i]&&key!==d.lastPositions[i]&&footstepRipples(d.byCell.get(key)?.surface))d.ripples.push({x:a.x,y:a.y,time});d.lastPositions[i]=key;}d.ripples=d.ripples.filter(r=>time>=r.time&&time-r.time<RIPPLE_SECONDS);for(const r of d.ripples){const pose=ripplePose(time-r.time);if(pose){c.save();c.globalAlpha=pose.alpha;c.fillStyle='#d0e7d9';for(let y=-pose.ry;y<=pose.ry;y++){const w=Math.round(pose.rx*Math.sqrt(Math.max(0,1-y*y/pose.ry**2)));c.fillRect(r.x-w,r.y+y,1,1);c.fillRect(r.x+w,r.y+y,1,1);}c.restore();}}
 c.save();c.clip(d.freshPath);for(const a of actors){if(!actorCanvas){actorCanvas=document.createElement('canvas');actorCanvas.width=actorCanvas.height=64;}const cv=actorCanvas,ac=cv.getContext('2d');ac.clearRect(0,0,64,64);character(ac,32,64,a.options);c.save();c.globalAlpha=.5;c.translate(Math.round(a.x)-32,Math.round(a.y)-4);c.scale(1,-1);c.drawImage(cv,0,-64);c.restore();}
 c.restore();c.restore();drawCoastalBoundary(c,d,f,{wash:map.terrain.includes('sand')});while(d.waves.size>8)d.waves.delete(d.waves.keys().next().value);
 return {cells:d.cells.length,identity,frame:f};
}
