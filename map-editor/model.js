import {isWater,waterSurface,mapWaterSurface,waterComponents} from '../src/water-map.js';
import {validateWaterLayout} from '../src/water-layout.js';
export {isWater,waterSurface} from '../src/water-map.js';
import {crossesFence} from '../src/fence-crossing.js';
import {sliverCells} from '../src/coastal-format.js';
// Authoring semantics are independent of pixels and adventure saves.
export const FORMAT='critz-map-project';
export const SAVE_KEY='critz.map-editor.v1';
export const MATERIALS=['grass','path','paving','soil','water','cliff','sand',...['fresh','ocean'].flatMap(i=>['still','moving','shallow-still','shallow-moving'].map(t=>`water-${i}-${t}`))];
export const materialBase=k=>isWater(k)?'water':k==='sand'?'grass':k;
export const FEATURES=['','fence','fence-picket','fence-barbed','tallgrass','flowers','bridge','stairs','cave','ledge-down','ledge-up','ledge-left','ledge-right'];
export const isFence=f=>['fence','fence-picket','fence-barbed'].includes(f);
export const fenceStyle=f=>f==='fence-picket'?'picket':f==='fence-barbed'?'barbed':'wood';
export const DIRS={up:[0,-1],right:[1,0],down:[0,1],left:[-1,0]};
export const PRESETS=[['Small town · Littleroot',20,20],['Horizontal route · Route 102',50,20],['Compact city · Petalburg',30,30],['Wide town · Mauville',40,20],['Large city · Rustboro',40,60],['Tall route · Route 104',40,80],['Long route · Route 103',80,22],['Bedroom',9,8],['House interior',11,9]];
export const STAMPS={
 cottage:{name:'Cottage',w:5,h:5,assembly:'house.cottage',kind:'building',footprint:[0,1,5,4],door:[2,4]},
 garden:{name:'Garden house',w:5,h:5,assembly:'house.garden',kind:'building',footprint:[0,1,5,4],door:[2,4]},
 shop:{name:'Critz shop',w:7,h:5,assembly:'house.shop',kind:'building',footprint:[0,1,7,4],door:[3,4]},
 tree:{name:'Old Grove · broadleaf',w:2,h:2,assembly:'tree.broadleaf.rooted',treeArt:'old-grove',kind:'scenery',footprint:[0,1,2,1]},
 willow:{name:'Soft Willow',w:2,h:2,assembly:'tree.broadleaf.rooted',treeArt:'soft-willow',kind:'scenery',footprint:[0,1,2,1]},
 palm:{name:'Coastal Palm',w:2,h:2,assembly:'tree.broadleaf.rooted',treeArt:'coastal-palm',kind:'scenery',footprint:[0,1,2,1]},
 cypress:{name:'Tiered Cedar · cypress',w:2,h:3,assembly:'tree.cypress.rooted',treeArt:'tiered-cedar',kind:'scenery',footprint:[0,2,2,1]},
 fountain:{name:'Fountain',w:3,h:3,assembly:'fountain.small',kind:'scenery',footprint:[0,0,3,3]},
 planter:{name:'Planter',w:1,h:1,tile:'planter.center',kind:'object',footprint:[0,0,1,1]},
 boulder:{name:'Pushable boulder',w:1,h:1,tile:'rock.2',kind:'boulder',footprint:[0,0,1,1]},
 bench:{name:'Bench',w:2,h:1,assembly:'bench',kind:'object',footprint:[0,0,2,1]},
 log:{name:'Hollow log',w:3,h:1,assembly:'log.hollow',kind:'object',footprint:[0,0,3,1]},
};
for(const type of ['cottage','garden','shop'])STAMPS[type+'-open']={...STAMPS[type],name:STAMPS[type].name+' · open entrance',artType:type,entrance:'open'};
export const clone=o=>JSON.parse(JSON.stringify(o));
export const inside=(m,x,y)=>Number.isInteger(x)&&Number.isInteger(y)&&x>=0&&y>=0&&x<m.w&&y<m.h;
export const at=(m,x,y)=>inside(m,x,y)?y*m.w+x:-1;
// An exact override replaces the feature's traversal and artwork together.
export const effectiveFeature=(m,x,y)=>m.raw[at(m,x,y)]?'':m.features[at(m,x,y)]||'';
export function newMap(id='map-1',name='My Rootport',w=20,h=20){if(!Number.isInteger(w)||!Number.isInteger(h)||w<8||h<8||w>128||h>128)throw Error('Map dimensions must be whole numbers from 8 to 128.');return{id,name,w,h,terrain:Array(w*h).fill('grass'),features:Array(w*h).fill(''),raw:{},objects:[],spawn:{x:Math.floor(w/2),y:Math.floor(h/2)},warps:[],connections:[]};}
export function newProject(){return{format:FORMAT,version:1,tileSize:32,name:'My little world',maps:[newMap()],active:'map-1',notes:''};}
export function maskAt(m,x,y,predicate){let mask=0;for(const [dx,dy,b]of [[0,-1,1],[1,0,2],[0,1,4],[-1,0,8],[1,-1,16],[1,1,32],[-1,1,64],[-1,-1,128]])if(predicate(x+dx,y+dy))mask|=b;for(const[b,a,c]of [[16,1,2],[32,2,4],[64,4,8],[128,8,1]])if(!(mask&a)||!(mask&c))mask&=~b;return mask;}
export function cellRecipe(m,x,y){const i=at(m,x,y),kind=materialBase(m.terrain[i]),rank=MATERIALS.indexOf(kind);const neighbor=(a,b)=>at(m,a,b)<0?kind:materialBase(m.terrain[at(m,a,b)]);const mask=maskAt(m,x,y,(a,b)=>MATERIALS.indexOf(neighbor(a,b))>=rank);const quadrants=[[-1,-1],[1,-1],[-1,1],[1,1]].map(([dx,dy])=>{const sides=[neighbor(x+dx,y),neighbor(x,y+dy)].filter(k=>MATERIALS.indexOf(k)<rank);const candidates=sides.length?sides:[neighbor(x+dx,y+dy)].filter(k=>MATERIALS.indexOf(k)<rank);const base=candidates.sort((a,b)=>MATERIALS.indexOf(b)-MATERIALS.indexOf(a))[0]||'grass';return kind==='grass'?'meadow.grass.'+((x*7+y*11)%16):`blend.${kind}.${base}.${mask}`;});
 const feature=effectiveFeature(m,x,y);return{quadrants,ledge:feature.startsWith('ledge-')?ledgeMask(m,x,y,feature):null,feature:isFence(feature)?`fence.${fenceStyle(feature)}.${maskAt(m,x,y,(a,b)=>isFence(effectiveFeature(m,a,b)))&15}`:feature,raw:m.raw[i]||null};}
export function objectFootprint(o){const [x,y,w,h]=STAMPS[o.type].footprint;return {x:o.x+x,y:o.y+y,w,h};}
export function footprintFits(m,o){const r=objectFootprint(o);return inside(m,r.x,r.y)&&inside(m,r.x+r.w-1,r.y+r.h-1);}
export function objectDepth(o){const r=objectFootprint(o);return r.y+r.h;}
export function objectArtBounds(o){
 const s=STAMPS[o.type];
 if(s.treeArt){const wide=['old-grove','soft-willow'].includes(s.treeArt);return {x:o.x+s.footprint[0]-(wide?.5:0),y:o.y+s.footprint[1]-1,w:wide?3:2,h:3};}
 return {x:o.x,y:o.y,w:s.w,h:s.h};
}
const contains=(r,x,y)=>x>=r.x&&x<r.x+r.w&&y>=r.y&&y<r.y+r.h;
export function objectsAt(m,x,y,{boundsFor=objectArtBounds}={}){
 return m.objects.map((o,index)=>({o,index,ground:contains(objectFootprint(o),x,y)}))
  .filter(a=>a.ground||contains(boundsFor(a.o),x,y))
  .sort((a,b)=>Number(b.ground)-Number(a.ground)||objectDepth(b.o)-objectDepth(a.o)||b.index-a.index).map(a=>a.o);
}
export function objectAt(m,x,y,options){return objectsAt(m,x,y,options)[0];}
export function objectBlocks(o,x,y){const s=STAMPS[o.type],[a,b,w,h]=s.footprint;if(s.door&&x===o.x+s.door[0]&&y===o.y+s.door[1])return false;return x>=o.x+a&&y>=o.y+b&&x<o.x+a+w&&y<o.y+b+h;}
export function fenceCrossing(m,from,to){return crossesFence(from,to,(a,b)=>isFence(effectiveFeature(m,a,b))&&!m.raw[at(m,a,b)]?maskAt(m,a,b,(xx,yy)=>isFence(effectiveFeature(m,xx,yy)))&15:null);}
export function blocked(m,x,y,{ignoreObject=null}={}){const i=at(m,x,y);if(i<0)return true;const f=m.features[i];if(m.objects.some(o=>o!==ignoreObject&&objectBlocks(o,x,y)))return true;if(m.raw[i])return m.raw[i].blocked; if(f==='bridge'||['stairs','cave'].includes(f)&&!isWater(m.terrain[i]))return false;return (isWater(m.terrain[i])&&!m.terrain[i].includes('shallow')||m.terrain[i]==='cliff')||f.startsWith('ledge-');}
let objectSequence=0;
function newObjectId(m){let id;do{id=`obj-${Date.now()}-${objectSequence++}`;}while(m.objects.some(o=>o.id===id));return id;}
export function placementError(m,type,x,y,{ignoreObject=null}={}){
 const s=STAMPS[type],candidate={type,x,y};
 if(m.objects.length>=4096&&!ignoreObject)return 'Map limit: 4,096 props.';
 if(!s||!Number.isInteger(x)||!Number.isInteger(y)||!footprintFits(m,candidate))return 'The whole ground footprint needs to fit inside the map.';
 const r=objectFootprint(candidate);
 for(let yy=r.y;yy<r.y+r.h;yy++)for(let xx=r.x;xx<r.x+r.w;xx++){
  if(!objectBlocks(candidate,xx,yy))continue;
  const doorway=m.objects.find(o=>{const meta=STAMPS[o.type];return o!==ignoreObject&&meta.door&&xx===o.x+meta.door[0]&&[o.y+meta.door[1],o.y+meta.door[1]+1].includes(yy);});
  if(doorway)return `Leave ${doorway.name}'s doorway and approach clear.`;
  const other=m.objects.find(o=>o!==ignoreObject&&objectBlocks(o,xx,yy));
  if(other)return `That ground footprint overlaps ${other.name||STAMPS[other.type].name} at ${xx},${yy}.`;
  if(blocked(m,xx,yy,{ignoreObject}))return `Ground is blocked at ${xx},${yy}. Place this stamp on clear ground.`;
 }
 if(s.door&&blocked(m,x+s.door[0],y+s.door[1]+1,{ignoreObject}))return 'Leave a clear approach in front of the door.';
 return null;
}
export function placeObject(m,type,x,y){const error=placementError(m,type,x,y);if(error)return error;const o={id:newObjectId(m),type,x,y,name:STAMPS[type].name};m.objects.push(o);return o;}
export function paint(m,x,y,brush){const i=at(m,x,y);if(i<0)return;if(MATERIALS.includes(brush)){m.terrain[i]=brush;m.features[i]='';delete m.raw[i];}else if(FEATURES.includes(brush)){m.features[i]=brush;delete m.raw[i];}else if(brush==='erase'){m.features[i]='';delete m.raw[i];m.objects=m.objects.filter(o=>o!==objectAt(m,x,y));m.warps=m.warps.filter(w=>w.x!==x||w.y!==y);}}
export function flood(m,x,y,brush){const i=at(m,x,y);if(i<0||!MATERIALS.includes(brush))return;const old=m.terrain[i];if(old===brush)return;const queue=[[x,y]],seen=new Set();for(let n=0;n<queue.length;n++){const[a,b]=queue[n],j=at(m,a,b);if(j<0||seen.has(j)||m.terrain[j]!==old)continue;seen.add(j);paint(m,a,b,brush);for(const[dx,dy]of Object.values(DIRS))queue.push([a+dx,b+dy]);}}
export function removePassage(project,mapId,w){
 const m=project.maps.find(m=>m.id===mapId);if(!m)return;
 m.warps=m.warps.filter(a=>a!==w);
 const target=project.maps.find(m=>m.id===w.target),[dx,dy]=DIRS[w.direction];
 if(target)target.warps=target.warps.filter(r=>{
  const [rx,ry]=DIRS[r.direction];
  return !(r.target===mapId&&r.tx===w.x-dx&&r.ty===w.y-dy&&r.x-rx===w.tx&&r.y-ry===w.ty);
 });
}
function removeDoorLinks(project,mapId,o){
 const m=project.maps.find(t=>t.id===mapId),d=doorCell(o);if(!d)return;
 m.warps=m.warps.filter(w=>w.x!==d.x||w.y!==d.y);
 for(const t of project.maps)t.warps=t.warps.filter(w=>!(w.target===m.id&&w.tx===d.x&&w.ty===d.y+1));
}
export function resizeMap(m,w,h,project=null){
 const n=newMap(m.id,m.name,w,h);
 if(project){
  for(const o of m.objects)if(!footprintFits(n,o))removeDoorLinks(project,m.id,o);
  for(const warp of [...m.warps])if(!inside(n,warp.x,warp.y))removePassage(project,m.id,warp);
  for(const t of project.maps)t.warps=t.warps.filter(a=>a.target!==m.id||inside(n,a.tx,a.ty));
 }
 for(let y=0;y<Math.min(h,m.h);y++)for(let x=0;x<Math.min(w,m.w);x++){
  const a=at(m,x,y),b=at(n,x,y);n.terrain[b]=m.terrain[a];n.features[b]=m.features[a];if(m.raw[a])n.raw[b]=clone(m.raw[a]);
 }
 n.objects=m.objects.filter(o=>footprintFits(n,o));
 n.warps=m.warps.filter(a=>inside(n,a.x,a.y));n.connections=clone(m.connections);
 n.spawn=inside(n,m.spawn.x,m.spawn.y)?clone(m.spawn):n.spawn;Object.assign(m,n);
}
export function move(project,mapId,player,dir,{push=true}={}){const m=project.maps.find(m=>m.id===mapId),[dx,dy]=DIRS[dir];let x=player.x+dx,y=player.y+dy,jump=false;
 if(fenceCrossing(m,player,{x,y}))return null;
 if(!inside(m,x,y)){const c=m.connections.find(c=>c.direction===dir);if(!c)return null;const target=project.maps.find(m=>m.id===c.target);if(!target)return null;let tx=dir==='left'?target.w-1:dir==='right'?0:x-c.offset,ty=dir==='up'?target.h-1:dir==='down'?0:y-c.offset;if(blocked(target,tx,ty))return null;return{map:target.id,x:tx,y:ty,facing:dir,transition:true};}
 const f=effectiveFeature(m,x,y);if(f.startsWith('ledge-')){if(isWater(m.terrain[at(m,x,y)])||m.objects.some(o=>objectBlocks(o,x,y))||m.raw[at(m,x,y)]?.blocked||f!==`ledge-${dir}`)return null;if(fenceCrossing(m,{x,y},{x:x+dx,y:y+dy}))return null;x+=dx;y+=dy;jump=true;}
 const b=m.objects.find(o=>STAMPS[o.type].kind==='boulder'&&o.x===x&&o.y===y);if(b&&push&&!jump){if(blocked(m,x+dx,y+dy)||fenceCrossing(m,{x,y},{x:x+dx,y:y+dy}))return null;b.x+=dx;b.y+=dy;}
 if(blocked(m,x,y))return null;
 const doorway=m.objects.find(o=>{const s=STAMPS[o.type];return s.door&&x===o.x+s.door[0]&&y===o.y+s.door[1];});if(doorway&&dir!=='up')return null;
 const warp=m.warps.find(w=>w.x===x&&w.y===y&&w.direction===dir);if(warp){const target=project.maps.find(t=>t.id===warp.target);if(!target||blocked(target,warp.tx,warp.ty))return null;const arrival={map:target.id,x:warp.tx,y:warp.ty,facing:dir,transition:true};return jump?{map:mapId,x,y,facing:dir,jump:true,arrival}:arrival;}
 return{map:mapId,x,y,facing:dir,jump};}
export function reachableMap(project,m){
 const cells=new Set(),warps=new Set(),connections=new Set(),queue=[];
 if(!blocked(m,m.spawn.x,m.spawn.y)){queue.push({...m.spawn});cells.add(at(m,m.spawn.x,m.spawn.y));}
 for(let n=0;n<queue.length;n++){
  const from=queue[n];
  for(const [dir,[dx,dy]]of Object.entries(DIRS)){
   const step=move(project,m.id,from,dir,{push:false});if(!step)continue;
   let x=from.x+dx,y=from.y+dy;
   if(!inside(m,x,y)){connections.add(dir);continue;}
   if(effectiveFeature(m,x,y).startsWith('ledge-')){x+=dx;y+=dy;}
   const w=m.warps.find(w=>w.x===x&&w.y===y&&w.direction===dir);
   if(w)warps.add(w);
   if(step.map===m.id&&inside(m,step.x,step.y)){
    const i=at(m,step.x,step.y);if(!cells.has(i)){cells.add(i);queue.push({x:step.x,y:step.y});}
   }
  }
 }
 return {cells,warps,connections};
}
export function validationIssues(project){
 const issues=[];
 for(const m of project.maps){
  const add=(code,x,y,text)=>issues.push({mapId:m.id,x,y,code,message:`${m.name}: ${text}`});
  for(let y=0;y<m.h;y++)for(let x=0;x<m.w;x++){
   const i=at(m,x,y),f=effectiveFeature(m,x,y);
   if(isFence(f)&&['path','paving'].includes(m.terrain[i]))add('fence-road',x,y,`fence blocks the road at ${x},${y}. Leave a gate gap.`);
   if(f==='stairs'&&isWater(m.terrain[i]))add('stairs-water',x,y,`stairs at ${x},${y} cannot cross water. Use a bridge.`);
   if(f==='stairs'&&m.terrain[i]!=='cliff'&&![[0,-1],[0,1]].some(([dx,dy])=>m.terrain[at(m,x+dx,y+dy)]==='cliff'))add('stairs-approach',x,y,`stairs at ${x},${y} need a cliff approach.`);
   if(f.startsWith('ledge-')){
    const [dx,dy]=DIRS[f.slice(6)];
    if(isWater(m.terrain[i]))add('ledge-water',x,y,`ledge at ${x},${y} cannot grant a hop through water.`);
    if(blocked(m,x+dx,y+dy))add('ledge-landing',x,y,`ledge at ${x},${y} has a blocked landing.`);
   }
  }
  const water=waterComponents(m).cells,thin=sliverCells(water);
  if(thin.length)add('water-width',thin[0].x,thin[0].y,`${thin.length} water cells need a full 2×2 water block. Widen the pool or channel.`);
  const mixed=validateWaterLayout(m.w,m.h,(x,y)=>mapWaterSurface(m,x,y));
  if(mixed.length){const {x,y}=mixed[0].deep;add('water-border',x,y,`mixed-depth water at ${x},${y} needs a complete shallow border, including diagonal corners (${mixed.length} exposed contacts).`);}
  const reach=reachableMap(project,m);
  if(blocked(m,m.spawn.x,m.spawn.y))add('spawn-blocked',m.spawn.x,m.spawn.y,'Hero start is blocked.');
  else if(reach.cells.size===1&&!reach.warps.size&&!reach.connections.size)add('spawn-trapped',m.spawn.x,m.spawn.y,'Hero start has no traversable exit. Clear a path from this cell.');
  for(const o of m.objects){
   const stamp=STAMPS[o.type];if(!stamp.door)continue;
   const d=doorCell(o);
   if(blocked(m,d.x,d.y+1))add('door-approach',d.x,d.y+1,`${o.name} needs a clear door approach.`);
   const w=m.warps.find(w=>w.x===d.x&&w.y===d.y&&w.direction==='up');
   if(!w)add('door-unlinked',d.x,d.y,`${o.name} has no linked doorway. Use Passage → Create room & return exit.`);
  }
  for(const w of m.warps){
   const t=project.maps.find(m=>m.id===w.target);
   if(t&&!t.warps.some(r=>r.target===m.id)&&!t.connections.some(r=>r.target===m.id))add('passage-return',w.x,w.y,`passage to ${t.name} has no return route. Add an exit if this is not intentionally one-way.`);
   if(!t||blocked(t,w.tx,w.ty))add('passage-destination',w.x,w.y,`passage at ${w.x},${w.y} has no clear destination.`);
   if(blocked(m,w.x,w.y))add('passage-blocked',w.x,w.y,`passage at ${w.x},${w.y} is blocked.`);
   else if(!reach.warps.has(w))add('passage-unreachable',w.x,w.y,`passage at ${w.x},${w.y} is not reachable from this map's Hero start in direction ${w.direction}. Clear its approach or move the start.`);
  }
  for(const c of m.connections){
   if(!project.maps.some(t=>t.id===c.target)){add('connection-missing',m.spawn.x,m.spawn.y,'missing connected map.');continue;}
   const vertical=['up','down'].includes(c.direction),length=vertical?m.w:m.h;
   let clear=null;
   for(let i=0;i<length;i++){
    const x=vertical?i:c.direction==='left'?0:m.w-1,y=vertical?(c.direction==='up'?0:m.h-1):i;
    if(!blocked(m,x,y)&&move(project,m.id,{x,y},c.direction,{push:false})){clear={x,y};break;}
   }
   if(!clear)add('connection-crossing',vertical?Math.floor(m.w/2):c.direction==='left'?0:m.w-1,vertical?(c.direction==='up'?0:m.h-1):Math.floor(m.h/2),`${c.direction} connection has no clear aligned crossing.`);
   else if(!reach.connections.has(c.direction))add('connection-unreachable',clear.x,clear.y,`${c.direction} connection is not reachable from this map's Hero start. Clear a path to the edge.`);
  }
 }
 return issues;
}
export function validate(project){return validationIssues(project).map(i=>i.message);}
export function importProject(text,tileIds){if(typeof text!=='string'||text.length>6000000)throw Error('Map file is too large (6 MB maximum).');let p;try{p=JSON.parse(text);}catch{throw Error('Paste a complete map project JSON.');}if(p?.format!==FORMAT||p.version!==1||p.tileSize!==32||!Array.isArray(p.maps)||!p.maps.length||p.maps.length>16)throw Error('Unsupported map project. Expected Critz map version 1, up to 16 maps.');if(p.encoding==='rle-v1'){for(const m of p.maps){for(const key of ['terrain','features']){const runs=m[key];if(!Array.isArray(runs)||runs.length>16384)throw Error('Invalid terrain runs.');const values=[];for(const run of runs){if(!Array.isArray(run)||run.length!==2||!Number.isInteger(run[1])||run[1]<1||values.length+run[1]>16384)throw Error('Invalid terrain runs.');values.push(...Array(run[1]).fill(run[0]));}m[key]=values;}}}const clean=newProject();clean.name=String(p.name||'My world').slice(0,100);clean.notes=String(p.notes||'').slice(0,10000);clean.maps=[];let total=0;const ids=new Set();for(const old of p.maps){if(typeof old.id!=='string'||!/^[a-zA-Z0-9_-]{1,80}$/.test(old.id)||ids.has(old.id))throw Error('Map IDs must be unique.');ids.add(old.id);const m=newMap(old.id,String(old.name||old.id).slice(0,100),old.w,old.h);total+=m.w*m.h;if(total>65536)throw Error('Project limit: 65,536 cells.');for(const key of ['terrain','features']){if(!Array.isArray(old[key])||old[key].length!==m.w*m.h||old[key].some(v=>!(key==='terrain'?MATERIALS:FEATURES).includes(v)))throw Error(`Invalid ${key} in ${m.name}.`);m[key]=[...old[key]];}if(!old.spawn||!inside(m,old.spawn.x,old.spawn.y))throw Error('Invalid Hero start.');m.spawn={x:old.spawn.x,y:old.spawn.y};if(!Array.isArray(old.objects)||old.objects.length>4096)throw Error('Invalid objects.');for(const o of old.objects){const s=STAMPS[o.type];if(!s||!Number.isInteger(o.x)||!Number.isInteger(o.y)||!footprintFits(m,o)||m.objects.some(a=>a.id===o.id))throw Error('Invalid or overlapping stamp.');const footprint=objectFootprint(o);for(let y=footprint.y;y<footprint.y+footprint.h;y++)for(let x=footprint.x;x<footprint.x+footprint.w;x++)if(objectBlocks(o,x,y)&&m.objects.some(a=>objectBlocks(a,x,y)))throw Error('Overlapping ground footprints.');m.objects.push({id:String(o.id).slice(0,100),type:o.type,x:o.x,y:o.y,name:String(o.name||s.name).slice(0,100)});}for(const [k,v]of Object.entries(old.raw||{})){if(!/^\d+$/.test(k)||+k>=m.w*m.h||!v||typeof v.id!=='string'||tileIds&&!tileIds.has(v.id)||typeof v.blocked!=='boolean')throw Error('Unknown raw tile or collision.');m.raw[k]={id:v.id,blocked:v.blocked};}for(const w of old.warps||[]){if(!inside(m,w.x,w.y)||!Object.hasOwn(DIRS,w.direction)||!Number.isInteger(w.tx)||!Number.isInteger(w.ty))throw Error('Invalid passage.');m.warps.push({x:w.x,y:w.y,target:String(w.target),tx:w.tx,ty:w.ty,direction:w.direction});}for(const c of old.connections||[]){if(!Object.hasOwn(DIRS,c.direction)||!Number.isInteger(c.offset)||Math.abs(c.offset)>128||m.connections.some(a=>a.direction===c.direction))throw Error('Invalid edge connection.');m.connections.push({direction:c.direction,target:String(c.target),offset:c.offset});}clean.maps.push(m);}clean.active=ids.has(p.active)?p.active:clean.maps[0].id;return clean;}
export function exportProject(project){return JSON.stringify({...project,compiler:'critz-metatile-v1',contactRule:{id:'B',structurePixels:16,groundPixels:16,axes:'horizontal and vertical'},semantics:{shore:'Deep water cells are blocked; explicitly shallow water cells are walkable. Shared B shoreline geometry and 3.2-second surface/wash loops.',cliff:'Solid raised terrain; stairs and cave openings override',ledge:'Directed two-cell hop with clear landing',building:'Solid footprint, rear overlap and explicit door; link entrance using passage tool'}},null,2);}
export function exportChat(project){const p=JSON.parse(exportProject(project));p.encoding='rle-v1';for(const m of p.maps)for(const key of ['terrain','features']){const runs=[];for(const v of m[key]){const last=runs.at(-1);if(last&&last[0]===v)last[1]++;else runs.push([v,1]);}m[key]=runs;}return JSON.stringify(p);}
export function demoProject(){const p=newProject(),m=p.maps[0];m.name='Your first clearing';for(let x=2;x<18;x++)for(let y=10;y<13;y++)paint(m,x,y,'path');for(let x=12;x<18;x++)for(let y=3;y<8;y++)paint(m,x,y,'water');for(let x=2;x<8;x++)for(let y=2;y<7;y++)paint(m,x,y,'cliff');for(let x=3;x<7;x++)for(let y=3;y<6;y++)paint(m,x,y,'grass');paint(m,4,6,'stairs');paint(m,4,5,'stairs');for(let x=10;x<18;x++)paint(m,x,15,'fence');for(let x=3;x<8;x++)paint(m,x,16,'ledge-down');placeObject(m,'cottage',2,7);placeObject(m,'tree',8,3);placeObject(m,'planter',8,10);m.spawn={x:9,y:12};connectBuilding(p,m.id,m.objects.find(o=>o.type==='cottage'));return p;}

// Ledge neighbors follow the same direction and tangent axis, never perpendicular faces.
export function ledgeMask(m,x,y,feature){const horizontal=['ledge-down','ledge-up'].includes(feature),[dx,dy]=horizontal?[1,0]:[0,1];return(effectiveFeature(m,x-dx,y-dy)===feature?1:0)|(effectiveFeature(m,x+dx,y+dy)===feature?2:0);}
export function doorCell(o){const s=STAMPS[o.type];return s?.door?{x:o.x+s.door[0],y:o.y+s.door[1]}:null;}
export function connectBuilding(project,mapId,o){
 const m=project.maps.find(m=>m.id===mapId),d=doorCell(o);if(!m||!d||!m.objects.includes(o))throw Error('Select a building doorway.');if(project.maps.length>=16)throw Error('Project limit: 16 maps. Link an existing room instead.');if(blocked(m,d.x,d.y+1)||isFence(m.features[at(m,d.x,d.y+1)]))throw Error('Clear the doorway approach first.');if(m.warps.some(w=>w.x===d.x&&w.y===d.y))throw Error('This doorway is already linked. Remove its passage first.');
 let id='room-'+o.id.replace(/[^a-zA-Z0-9_-]/g,'').slice(0,65),n=1;while(project.maps.some(t=>t.id===id))id='room-'+n+++'-'+o.id.slice(0,55);
 const room=newMap(id,o.name+' · interior',11,9),cx=5;room.terrain.fill('paving');for(let y=0;y<room.h;y++)for(let x=0;x<room.w;x++)if(x===0||y===0||x===room.w-1||y===room.h-1)room.terrain[at(room,x,y)]='cliff';room.terrain[at(room,cx,8)]='paving';room.spawn={x:cx,y:7};room.warps.push({x:cx,y:8,direction:'down',target:m.id,tx:d.x,ty:d.y+1});m.warps.push({...d,direction:'up',target:room.id,tx:cx,ty:7});project.maps.push(room);return room;
}
export function relocateDoorLinks(project,mapId,o,old){const s=STAMPS[o.type];if(!s.door)return;const dx=o.x-old.x,dy=o.y-old.y,ox=old.x+s.door[0],oy=old.y+s.door[1];for(const m of project.maps)for(const w of m.warps){if(m.id===mapId&&w.x===ox&&w.y===oy){w.x+=dx;w.y+=dy;}if(w.target===mapId&&w.tx===ox&&w.ty===oy+1){w.tx+=dx;w.ty+=dy;}}}

export function reviewProject(revision='me3'){const p=newProject(),m=newMap('review','Buildings & ledges · revision 3',24,22);p.name='M1.ME3 visual review';p.maps=[m];p.active=m.id;p.notes='Original Critz building/ledge revision; awaiting your visual feedback. Walk into all three doors and back out. Test the four ledge directions, bridge and stairs. This sandbox does not overwrite your saved draft.';for(let y=7;y<=9;y++)for(let x=1;x<23;x++)paint(m,x,y,'path');for(const [type,x]of [['cottage',2],['garden',9],['shop',16]]){const o=placeObject(m,revision==='me4'&&type==='garden'?'garden-open':type,x,2);connectBuilding(p,m.id,o);}for(let x=3;x<=7;x++)paint(m,x,12,'ledge-down');for(let x=10;x<=14;x++)paint(m,x,19,'ledge-up');for(let y=15;y<=18;y++){paint(m,3,y,'ledge-left');paint(m,7,y,'ledge-right');}for(let y=12;y<=15;y++)for(let x=10;x<=13;x++)paint(m,x,y,'cliff');for(let y=14;y<=16;y++)paint(m,11,y,'stairs');for(let y=11;y<=17;y++)for(let x=16;x<=22;x++)paint(m,x,y,'sand');for(let y=12;y<=16;y++)for(let x=17;x<=21;x++)paint(m,x,y,'water-ocean-shallow-moving');for(let y=10;y<=18;y++)paint(m,19,y,'bridge');for(let x=1;x<=8;x++)if(x!==4)paint(m,x,10,'fence');for(let x=1;x<7;x++)paint(m,x,20,'paving');paint(m,1,19,'soil');paint(m,1,18,'path');m.spawn={x:12,y:8};if(revision==='me4'){m.name='Entrances, fences & landing dust · revision 4';p.name='M1.ME4 playable review';p.notes='Walk into all three buildings. Cottage/shop have indoor exit mats; the open garden has daylight at its indoor exit. Stand on the fence row to walk behind the rail; go around the gate to cross. Every ledge crossing jumps and produces landing dust. Your draft is untouched.';}return p;}

// Sand has its own surface identity, between turf and constructed ground.
export function groundRecipe(m,x,y){const order=['grass','sand','path','paving','soil','water','cliff'],kind=isWater(m.terrain[at(m,x,y)])?'water':m.terrain[at(m,x,y)],rank=order.indexOf(kind),neighbor=(a,b)=>at(m,a,b)<0?kind:isWater(m.terrain[at(m,a,b)])?'water':m.terrain[at(m,a,b)],mask=maskAt(m,x,y,(a,b)=>order.indexOf(neighbor(a,b))>=rank);return[[-1,-1],[1,-1],[-1,1],[1,1]].map(([dx,dy])=>{const sides=[neighbor(x+dx,y),neighbor(x,y+dy)].filter(k=>order.indexOf(k)<rank),candidates=sides.length?sides:[neighbor(x+dx,y+dy)].filter(k=>order.indexOf(k)<rank),base=candidates.sort((a,b)=>order.indexOf(b)-order.indexOf(a))[0]||'grass';if(kind==='grass')return 'meadow.grass.'+((x*7+y*11)%16);if(kind==='sand'||base==='sand'&&['path','paving','soil'].includes(kind))return `ME3.blend.${kind}.${base}.${mask}`;return `blend.${kind}.${base==='sand'?'grass':base}.${mask}`;});}

export function eraseObject(project,mapId,o){
 const m=project.maps.find(t=>t.id===mapId);if(!o||!m.objects.includes(o))return;
 removeDoorLinks(project,mapId,o);m.objects=m.objects.filter(a=>a!==o);
}
export function eraseAt(project,mapId,x,y){
 const m=project.maps.find(t=>t.id===mapId),o=objectAt(m,x,y);
 if(o)removeDoorLinks(project,mapId,o);
 for(const w of [...m.warps])if(w.x===x&&w.y===y)removePassage(project,mapId,w);
 paint(m,x,y,'erase');
}

export function exitPresentation(project,m,w){if(w.direction!=='down')return null;const outside=project.maps.find(t=>t.id===w.target);const o=outside?.objects.find(o=>{const d=doorCell(o);return d&&w.tx===d.x&&w.ty===d.y+1&&outside.warps.some(r=>r.x===d.x&&r.y===d.y&&r.target===m.id);});return o?{open:STAMPS[o.type].entrance==='open'}:null;}

export function fenceReviewProject(){const p=newProject(),m=newMap('fence-review','Fence registration · revision 5',26,24);p.maps=[m];p.active=m.id;p.name='M1.ME5 fence review';p.notes='Wood, white picket and barbed wire share a32×64 frame: paint only rows16–47. Collision is unchanged. Walk on a fence row behind it; below the row you are in front. Go around an end or through a gap to cross. Vertical runs and corner/junction joins are shown. This sandbox never saves over your draft.';for(const [i,f]of ['fence','fence-picket','fence-barbed'].entries()){const x=2+i*8;for(let a=x;a<x+6;a++)paint(m,a,4,f);for(let y=8;y<15;y++)paint(m,x+1,y,f);for(let a=x+1;a<x+6;a++)paint(m,a,14,f);for(let y=17;y<21;y++)paint(m,x+3,y,f);for(let a=x;a<x+7;a++)if(a!==x+3)paint(m,a,19,f);}m.spawn={x:5,y:6};return p;}


// M1.OV1 original garden composition. No game/draft storage is consulted.
export function groveReviewProject(){
 const p=newProject(),m=newMap('grove-review','Rootport · a quiet garden',22,16);
 p.name='Rootport Grove · native tree and canopy review';p.maps=[m];p.active=m.id;
 const fill=(x,y,w,h,k)=>{for(let b=y;b<y+h;b++)for(let a=x;a<x+w;a++)paint(m,a,b,k);};
 fill(4,11,17,2,'path');fill(7,6,2,6,'path');fill(10,9,7,2,'path');
 fill(14,4,4,4,'water-fresh-shallow-still');fill(11,3,2,3,'soil');
 for(const [x,y,type]of [[5,2,'cottage'],[1,3,'cypress'],[3,8,'tree'],[18,5,'willow'],[18,13,'palm'],[10,6,'tree'],[1,13,'cypress']]){
  const placed=placeObject(m,type,x,y);if(typeof placed==='string')throw Error(placed);
 }
 for(const [x,y]of [[4,6],[5,7],[11,3],[12,3],[13,9],[20,9]])paint(m,x,y,'flowers');
 placeObject(m,'bench',11,13);m.spawn={x:8,y:13};
 connectBuilding(p,m.id,m.objects.find(o=>o.type==='cottage'));
 p.notes='Original M1.OV1 composition. Trees share exact transparent TR2 pixels and retain explicit two-cell ground footprints. Walk behind crowns, approach roots from four sides, and use the placement preview to inspect overhang. New appearance awaits morning review.';
 return p;
}

export function editorRepairReviewProject(){
 const p=newProject(),m=newMap('editor-repair','Water bodies & exact tiles · repair 6',32,28);
 p.maps=[m];p.active=m.id;p.name='M1.ME6 editor repair review';
 const cases=[['grass','water-fresh-still'],['path','water-fresh-still'],['sand','water-ocean-shallow-moving'],['soil','water-fresh-shallow-still'],['paving','water-fresh-shallow-moving'],['grass','water-ocean-moving']];
 for(const [n,[ground,water]]of cases.entries()){
  const x=2+n%3*10,y=n<3?2:15;
  for(let b=y;b<y+8;b++)for(let a=x;a<x+8;a++)paint(m,a,b,ground);
  for(let b=y+2;b<y+6;b++)for(let a=x+2;a<x+6;a++)paint(m,a,b,water);
  if(n===4)for(let b=y+3;b<y+5;b++)for(let a=x+3;a<x+5;a++)paint(m,a,b,'water-fresh-moving');
 }
 for(let y=12;y<=13;y++)for(let x=1;x<31;x++)paint(m,x,y,'path');
 for(const [n,type]of ['tree','cypress','willow','palm'].entries())placeObject(m,type,2+n*8,23);
 for(const [n,feature]of ['bridge','fence','ledge-down'].entries()){
  paint(m,14+n,12,feature);m.raw[at(m,14+n,12)]={id:'meadow.grass.0',blocked:false};
 }
 m.spawn={x:16,y:13};
 p.notes='Top row: deep freshwater on grass, deep freshwater on path, shallow moving ocean on sand. Bottom row: shallow freshwater on quiet soil, a shallow-ring/deep-center pond on paving, and a separate deep ocean pool. Exact grass overrides on the central path suppress a bridge, fence and ledge. Four unchanged native tree styles remain below. New appearance awaits morning review. This sandbox never overwrites your draft.';
 return p;
}

export function authoringReviewProject(){
 const p=groveReviewProject(),m=p.maps[0];
 p.name='M1.ME7 authoring tools review';m.name='Selection, layers & canopy overlap';
 placeObject(m,'bench',3,8);
 p.notes='Reuse the existing garden to try Select, Copy selection, Paste and Pick. The bench at3,8 sits behind the Grove canopy while its occupied cells stay separate from the tree roots. Picking prioritizes occupied ground. Copy Props to include an entire footprint; Ground/Features/Exact tiles copy independently. Copied buildings need their own Passage links. Escape cancels previews and incomplete strokes. This sandbox never reads or replaces your saved draft. Existing native art remains for morning feedback.';
 return p;
}
