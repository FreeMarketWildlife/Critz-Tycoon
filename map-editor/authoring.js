import {STAMPS,MATERIALS,FEATURES,clone,inside,at,objectFootprint,objectBlocks,objectsAt,blocked,placementError,placeObject,relocateDoorLinks,paint,eraseAt,eraseObject,DIRS} from './model.js';

export const EDIT_LAYERS=['ground','features','raw','objects'];
export const rectBetween=(a,b)=>({x:Math.min(a.x,b.x),y:Math.min(a.y,b.y),w:Math.abs(a.x-b.x)+1,h:Math.abs(a.y-b.y)+1});
function checkedRect(m,r){
 if(!r||![r.x,r.y,r.w,r.h].every(Number.isInteger)||r.w<1||r.h<1||!inside(m,r.x,r.y)||!inside(m,r.x+r.w-1,r.y+r.h-1))throw Error('The whole selection needs to fit inside the map.');
 return r;
}
const intersects=(a,b)=>a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y;
const encloses=(a,b)=>b.x>=a.x&&b.y>=a.y&&b.x+b.w<=a.x+a.w&&b.y+b.h<=a.y+a.h;
export function copySelection(project,mapId,rect,layers=EDIT_LAYERS){
 const m=project.maps.find(m=>m.id===mapId);if(!m)throw Error('Select an existing map.');checkedRect(m,rect);
 if(!Array.isArray(layers)||!layers.length||layers.some(a=>!EDIT_LAYERS.includes(a)))throw Error('Choose a supported edit layer.');
 const out={format:'critz-map-selection',version:1,w:rect.w,h:rect.h,layers:[...new Set(layers)]};
 for(const [layer,key]of [['ground','terrain'],['features','features']])if(layers.includes(layer)){
  out[key]=[];for(let y=rect.y;y<rect.y+rect.h;y++)for(let x=rect.x;x<rect.x+rect.w;x++)out[key].push(m[key][at(m,x,y)]);
 }
 if(layers.includes('raw')){
  out.raw={};for(let y=0;y<rect.h;y++)for(let x=0;x<rect.w;x++){const raw=m.raw[at(m,rect.x+x,rect.y+y)];if(raw)out.raw[y*rect.w+x]=clone(raw);}
 }
 if(layers.includes('objects')){
  out.objects=[];
  for(const o of m.objects){const footprint=objectFootprint(o);if(!intersects(rect,footprint))continue;let occupied=false;for(let y=Math.max(rect.y,footprint.y);y<Math.min(rect.y+rect.h,footprint.y+footprint.h);y++)for(let x=Math.max(rect.x,footprint.x);x<Math.min(rect.x+rect.w,footprint.x+footprint.w);x++)if(objectBlocks(o,x,y))occupied=true;if(!occupied)continue;
   if(!encloses(rect,footprint))throw Error(`Selection cuts through ${o.name}'s ground footprint. Include all of its occupied cells, or copy another layer.`);
   out.objects.push({sourceId:o.id,type:o.type,x:o.x-rect.x,y:o.y-rect.y,name:o.name});
  }
 }
 return out;
}
function checkClipboard(clip){
 if(clip?.format!=='critz-map-selection'||clip.version!==1||!Number.isInteger(clip.w)||!Number.isInteger(clip.h)||clip.w<1||clip.h<1||clip.w>128||clip.h>128||!Array.isArray(clip.layers)||!clip.layers.length||clip.layers.some(a=>!EDIT_LAYERS.includes(a)))throw Error('Copy a valid map selection first.');
 for(const [layer,key,values]of [['ground','terrain',MATERIALS],['features','features',FEATURES]])if(clip.layers.includes(layer)&&(!Array.isArray(clip[key])||clip[key].length!==clip.w*clip.h||clip[key].some(v=>!values.includes(v))))throw Error('Invalid copied cells.');
 if(clip.layers.includes('raw'))for(const [k,v]of Object.entries(clip.raw||{}))if(!/^\d+$/.test(k)||+k>=clip.w*clip.h||!v||typeof v.id!=='string'||typeof v.blocked!=='boolean')throw Error('Invalid copied exact tile.');
 if(clip.layers.includes('objects')&&(!Array.isArray(clip.objects)||clip.objects.length>4096||clip.objects.some(o=>!STAMPS[o.type]||!Number.isInteger(o.x)||!Number.isInteger(o.y))))throw Error('Invalid copied props.');
}
function protectLinks(before,after,mapId){
 const oldMap=before.maps.find(m=>m.id===mapId),m=after.maps.find(m=>m.id===mapId);
 for(const source of before.maps)for(const [index,w]of source.warps.entries()){
  const current=after.maps.find(m=>m.id===source.id).warps[index];
  if(source.id===mapId&&!blocked(oldMap,w.x,w.y)&&blocked(m,current.x,current.y))throw Error(`This edit blocks the existing passage at ${w.x},${w.y}.`);
  if(w.target===mapId&&!blocked(oldMap,w.tx,w.ty)&&blocked(m,current.tx,current.ty))throw Error(`This edit blocks an existing arrival at ${w.tx},${w.ty}.`);
 }
 for(const o of oldMap.objects){const s=STAMPS[o.type],current=m.objects.find(a=>a.id===o.id);if(!s.door||!current)continue;const x=o.x+s.door[0],y=o.y+s.door[1]+1,tx=current.x+s.door[0],ty=current.y+s.door[1]+1;if(!blocked(oldMap,x,y)&&blocked(m,tx,ty))throw Error(`This edit blocks ${o.name}'s door approach at ${tx},${ty}.`);}
}
export function pasteSelection(project,mapId,clip,x,y){
 checkClipboard(clip);const result=clone(project),m=result.maps.find(m=>m.id===mapId);if(!m)throw Error('Select an existing map.');
 checkedRect(m,{x,y,w:clip.w,h:clip.h});
 for(let b=0;b<clip.h;b++)for(let a=0;a<clip.w;a++){
  const from=b*clip.w+a,to=at(m,x+a,y+b);
  if(clip.layers.includes('ground'))m.terrain[to]=clip.terrain[from];
  if(clip.layers.includes('features'))m.features[to]=clip.features[from];
  if(clip.layers.includes('raw')){if(clip.raw?.[from])m.raw[to]=clone(clip.raw[from]);else delete m.raw[to];}
 }
 const pasted=[];
 if(clip.layers.includes('objects'))for(const o of clip.objects){
  const placed=placeObject(m,o.type,x+o.x,y+o.y);if(typeof placed==='string')throw Error(placed);placed.name=String(o.name||STAMPS[o.type].name);pasted.push(placed);
 }
 for(const o of m.objects){if(!pasted.includes(o)&&!intersects({x,y,w:clip.w,h:clip.h},objectFootprint(o)))continue;const error=placementError(m,o.type,o.x,o.y,{ignoreObject:o});if(error)throw Error(`${o.name}: ${error}`);}
 protectLinks(project,result,mapId);
 return {project:result,rect:{x,y,w:clip.w,h:clip.h},objects:pasted};
}
export function moveStamp(project,mapId,id,x,y){
 const result=clone(project),m=result.maps.find(m=>m.id===mapId),o=m?.objects.find(o=>o.id===id);if(!o)throw Error('Select a prop to move.');
 const error=placementError(m,o.type,x,y,{ignoreObject:o});if(error)throw Error(error);
 const old={x:o.x,y:o.y};o.x=x;o.y=y;relocateDoorLinks(result,mapId,o,old);protectLinks(project,result,mapId);
 return result;
}
export function sampleCell(m,x,y,layer='auto',options){
 if(!inside(m,x,y))throw Error('Pick a cell inside the map.');const i=at(m,x,y),o=objectsAt(m,x,y,options)[0];
 if((layer==='auto'||layer==='objects')&&o)return {kind:'stamp',value:o.type};
 if((layer==='auto'||layer==='raw')&&m.raw[i])return {kind:'raw',...clone(m.raw[i])};
 if((layer==='auto'||layer==='features')&&m.features[i])return {kind:'brush',value:m.features[i]};
 if(layer==='auto'||layer==='ground')return {kind:'brush',value:m.terrain[i]};
 throw Error('That layer is empty at this cell.');
}
export function paintLayer(project,mapId,x,y,brush,layer='auto',{erase=false,raw=null}={}){
 const m=project.maps.find(m=>m.id===mapId),i=at(m,x,y);if(i<0)return;
 if(layer==='auto'){if(erase)eraseAt(project,mapId,x,y);else if(raw)m.raw[i]=clone(raw);else paint(m,x,y,brush);return;}
 if(layer==='ground'){if(erase)m.terrain[i]='grass';else if(MATERIALS.includes(brush))m.terrain[i]=brush;return;}
 if(layer==='features'){if(erase)m.features[i]='';else if(FEATURES.includes(brush))m.features[i]=brush;return;}
 if(layer==='raw'){if(erase)delete m.raw[i];else if(raw)m.raw[i]=clone(raw);return;}
 if(layer==='objects'&&erase)eraseObject(project,mapId,objectsAt(m,x,y).find(o=>{const r=objectFootprint(o);return x>=r.x&&y>=r.y&&x<r.x+r.w&&y<r.y+r.h;}));
}
export function floodLayer(project,mapId,x,y,brush,layer='auto'){
 const m=project.maps.find(m=>m.id===mapId),start=at(m,x,y);if(start<0||!MATERIALS.includes(brush)||!['auto','ground'].includes(layer))return;
 const old=m.terrain[start],seen=new Set(),queue=[[x,y]];if(old===brush)return;
 for(let n=0;n<queue.length;n++){const [a,b]=queue[n],i=at(m,a,b);if(i<0||seen.has(i)||m.terrain[i]!==old)continue;seen.add(i);paintLayer(project,mapId,a,b,brush,layer);for(const [dx,dy]of Object.values(DIRS))queue.push([a+dx,b+dy]);}
}

export function mapCamera(m,p,width=480,height=320){
 const axis=(size,field,focus)=>size<field?Math.floor((size-field)/2):Math.max(0,Math.min(size-field,focus));
 return {x:axis(m.w*32,width,Math.round((p.px??p.x*32)+16-width/2)),y:axis(m.h*32,height,Math.round((p.py??p.y*32)+32-height*176/320))};
}
