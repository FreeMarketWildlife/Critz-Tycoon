// All reflection/effect masks are hard native pixels; no reference artwork.
import {waterPixel,ripplePose} from './water-surfaces.js';
export async function loadWaterTerrain(){const url=new URL('../assets/review/water-terrain/atlas.json',import.meta.url),manifest=await(await fetch(url)).json(),img=new Image();img.src=new URL(manifest.image,url).href;await img.decode();const tiles=new Map(manifest.assets.map(t=>[t.id,t]));return {manifest,draw(c,id,x,y){const a=tiles.get(id);if(!a)throw Error('Missing water tile '+id);c.drawImage(img,a.x,a.y,32,32,x,y,32,32);}};}
const pathCache=new Map();
export function maskPath(cells,predicate=()=>true){const selected=cells.filter(cell=>predicate(cell.surface)),key=selected.map(({x,y,mask})=>`${x},${y},${mask}`).join(';');if(pathCache.has(key))return pathCache.get(key);const p=new Path2D();for(const {x,y,mask} of selected){for(let yy=0;yy<32;yy++){let start=-1;for(let xx=0;xx<=32;xx++){const inside=xx<32&&waterPixel(xx,yy,mask);if(inside&&start<0)start=xx;if(!inside&&start>=0){p.rect(x*32+start,y*32+yy,xx-start,1);start=-1;}}}}pathCache.set(key,p);return p;}
const ellipse=(c,cx,cy,rx,ry,color,outline=false)=>{c.fillStyle=color;for(let yy=-ry;yy<=ry;yy++){const w=Math.round(rx*Math.sqrt(Math.max(0,1-yy*yy/(ry*ry))));if(outline){c.fillRect(cx-w,cy+yy,2,1);c.fillRect(cx+w-1,cy+yy,2,1);}else c.fillRect(cx-w,cy+yy,w*2+1,1);}};
export function drawRipples(c,ripples,time,clip){c.save();c.clip(clip);for(const r of ripples){const p=ripplePose(time-r.time);if(!p)continue;c.globalAlpha=p.alpha;ellipse(c,r.x,r.y,p.rx,p.ry,'#c8e5d9',true);if(time-r.time<.134){c.fillRect(r.x-5,r.y-2,3,1);c.fillRect(r.x+3,r.y-3,2,2);}}c.restore();}
export function drawReflection(c,actor,clip,time,moving=false){c.save();c.clip(clip);c.globalAlpha=.52;
 // Copy the same pose, invert about the foot anchor. Integer scanlines keep pixels crisp.
 for(let y=0;y<64;y++){const drift=moving?Math.round(Math.sin(time*2+y/7)):0;c.drawImage(actor.image,0,63-y,32,1,Math.round(actor.x)-16+drift,Math.round(actor.y)-4+y,32,1);}
 c.restore();}
export function drawSky(c,time,minute,clip,calm){const night=minute>=1260,phase=calm?0:time;c.save();c.clip(clip);
 if(night){for(let i=0;i<28;i++){const x=(i*73+21)%480,y=(i*47+136)%320;c.fillStyle=i%3?'#b4d5db':'#deead7';c.globalAlpha=.35+(calm?.1:Math.sin(phase*1.8+i)*.15);c.fillRect(x,y,2,2);if(i%5===0){c.fillRect(x-2,y+1,6,1);c.fillRect(x+1,y-2,1,6);}}}
 else{c.globalAlpha=.22;for(let i=0;i<3;i++){const x=Math.round(((410+i*181-phase*9)%660+660)%660)-100,y=140+i*55;ellipse(c,x,y,36,9,'#e0e9d3');ellipse(c,x-16,y-6,18,9,'#e0e9d3');ellipse(c,x+11,y-9,22,11,'#e0e9d3');}}
 c.restore();}
