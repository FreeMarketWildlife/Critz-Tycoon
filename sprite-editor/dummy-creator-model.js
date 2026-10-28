import {WIDTH,HEIGHT,SIZE,PART_DEFINITIONS,CATEGORY_PARTS,validateLabels,canonical,importCorrections} from './body-regions-model.js';
export const DIRECTIONS=['south','west','east','north'];
export const PROJECT_STORAGE='fmw.sprite-editor.dummy-creator.v1';
const clone=x=>structuredClone(x),bad=s=>{throw Error(s);};
const fields=(o,ks)=>{if(!o||typeof o!=='object'||Array.isArray(o)||Object.keys(o).some(k=>!ks.includes(k))||ks.some(k=>!Object.hasOwn(o,k)))bad('Unexpected or missing project fields.');};
const safeId=id=>typeof id==='string'&&/^[-a-zA-Z0-9_.]{1,100}$/.test(id)&&!['__proto__','constructor','prototype'].includes(id);
export function sideFor(direction,x,choice='auto'){
 if(!DIRECTIONS.includes(direction)||!Number.isInteger(x)||x<0||x>=WIDTH)bad('Invalid direction or pixel.');
 if(['left','right','center'].includes(choice))return choice;
 if(choice!=='auto')bad('Choose an anatomical side.');
 if(direction==='west'||direction==='east')bad('Profile painting needs an explicit anatomical side.');
 return direction==='south'?(x<16?'right':'left'):(x<16?'left':'right');
}
export function partFor(id,direction,x,choice='auto'){
 const p=PART_DEFINITIONS[id];if(!p)bad('Unknown part.');return CATEGORY_PARTS[p.category][sideFor(direction,x,choice)];
}
export function createProject(seed,labels){
 const initial=validateLabels(labels);
 return{schema:'critz.dummy-creator.project',version:1,seedId:seed.seedId,width:WIDTH,height:HEIGHT,labelOrder:'row-major-top-left',source:clone(seed.source),registration:clone(seed.registration),parts:clone(PART_DEFINITIONS),activeDirection:'south',activeFrame:0,directions:Object.fromEntries(DIRECTIONS.map(d=>[d,[{id:d+'-1',name:d==='south'?'Supplied dummy':'Unedited starting template',durationMs:100,referenceIndex:2,labels:initial.slice()}]]))};
}
export function labelsForFrame(project,direction,index){
 const frame=project.directions[direction]?.[index];if(!frame)bad('Unknown frame.');
 return (project.version===2?project.cels[frame.celId].labels:frame.labels).slice();
}
export function validateProject(data,seed){
 fields(data,['schema','version','seedId','width','height','labelOrder','source','registration','parts','activeDirection','activeFrame','directions',...(data?.version===2?['cels']:[])]);
 if(data.schema!=='critz.dummy-creator.project'||![1,2].includes(data.version)||data.width!==WIDTH||data.height!==HEIGHT||data.labelOrder!=='row-major-top-left')bad('Wrong Dummy Creator project format.');
 for(const k of ['seedId','source','registration'])if(canonical(data[k])!==canonical(seed[k]))bad('Project has different '+k+'.');
 if(canonical(data.parts)!==canonical(PART_DEFINITIONS))bad('Project has different anatomical part definitions.');
 fields(data.directions,DIRECTIONS);const ids=new Set(),usedCels=new Set();
 if(data.version===2){
  if(!data.cels||typeof data.cels!=='object'||Array.isArray(data.cels)||Object.keys(data.cels).length<1||Object.keys(data.cels).length>128)bad('Expected 1–128 editable poses.');
  for(const [id,cel]of Object.entries(data.cels)){fields(cel,['id','name','direction','labels']);if(!safeId(id)||cel.id!==id||typeof cel.name!=='string'||cel.name.length>80||!DIRECTIONS.includes(cel.direction))bad('Invalid editable pose identity.');validateLabels(cel.labels);}
 }
 for(const d of DIRECTIONS){
  const frames=data.directions[d];if(!Array.isArray(frames)||frames.length<1||frames.length>32)bad('Each direction needs 1–32 frames.');
  for(const f of Array.from(frames)){
   fields(f,['id','name','durationMs','referenceIndex',data.version===2?'celId':'labels']);
   if(!safeId(f.id)||ids.has(f.id))bad('Frame IDs must be unique.');ids.add(f.id);
   if(typeof f.name!=='string'||f.name.length>80)bad('Invalid frame name.');
   if(!Number.isFinite(f.durationMs)||data.version===1&&!Number.isInteger(f.durationMs)||f.durationMs<20||f.durationMs>5000)bad('Frame duration must be 20–5000 ms (whole ms in legacy projects).');
   if(!Number.isInteger(f.referenceIndex)||f.referenceIndex<0||f.referenceIndex>7)bad('Reference frame must be 0–7.');
   if(data.version===1)validateLabels(f.labels);else{
    if(!safeId(f.celId)||!Object.hasOwn(data.cels,f.celId)||data.cels[f.celId].direction!==d)bad('Frame needs a valid pose in its own direction.');usedCels.add(f.celId);
   }
  }
 }
 if(data.version===2&&usedCels.size!==Object.keys(data.cels).length)bad('Project contains an unreferenced pose.');
 if(!DIRECTIONS.includes(data.activeDirection)||!Number.isInteger(data.activeFrame)||!data.directions[data.activeDirection][data.activeFrame])bad('Invalid active frame.');return clone(data);
}
export function parseProject(text,seed){if(typeof text!=='string'||text.length>2000000)bad('Project must be smaller than 2 MB.');let d;try{d=JSON.parse(text);}catch{bad('Project must be valid JSON.');}return validateProject(d,seed);}
export function frameAt(frames,elapsed){const period=frames.reduce((n,f)=>n+f.durationMs,0);let t=((elapsed%period)+period)%period;for(let i=0;i<frames.length;i++){if(t<frames[i].durationMs)return i;t-=frames[i].durationMs;}return 0;}
// Consolidate only complete editable label arrays, within each direction. Reference
// guides and timing belong to sequence slots and are preserved independently.
export function migrateProject(initial,seed){
 const p=validateProject(initial,seed);if(p.version===2)return p;
 p.version=2;p.cels={};
 for(const d of DIRECTIONS){const seen=new Map();for(const f of p.directions[d]){
  const key=canonical(f.labels);let id=seen.get(key);
  if(!id){id=d+'-cel-'+(seen.size+1);seen.set(key,id);p.cels[id]={id,name:f.name,direction:d,labels:f.labels.slice()};}
  delete f.labels;f.celId=id;
 }}return validateProject(p,seed);
}
export function createProjectModel(initial,seed){
 let p=migrateProject(initial,seed),undos=[],redos=[],stroke=null,serial=0;
 const frame=()=>p.directions[p.activeDirection][p.activeFrame];
 const currentLabels=()=>p.version===2?p.cels[frame().celId].labels:frame().labels;
 const hydrate=f=>({...clone(f),labels:(p.version===2?p.cels[f.celId].labels:f.labels).slice()});
 const remember=before=>{if(canonical(before)===canonical(p))return false;undos.push(before);if(undos.length>100)undos.shift();redos=[];return true;};
 const end=()=>{if(!stroke)return false;const old=stroke;stroke=null;return remember(old);};
 const edit=fn=>{end();const old=clone(p);try{fn();validateProject(p,seed);}catch(e){p=old;throw e;}return remember(old);};
 const nextId=kind=>p.activeDirection+'-'+kind+'-'+Date.now()+'-'+(++serial);
 const copyCel=blank=>{const id=nextId('pose'),old=p.cels[frame().celId];p.cels[id]={id,name:(blank?'Blank pose':'Copy of '+old.name).slice(0,80),direction:p.activeDirection,labels:blank?Array(SIZE).fill(0):old.labels.slice()};return id;};
 return{
 get labels(){return currentLabels().slice();},get data(){return clone(p);},get direction(){return p.activeDirection;},get index(){return p.activeFrame;},get frame(){return hydrate(frame());},get frames(){return p.directions[p.activeDirection].map(hydrate);},get undoCount(){return undos.length;},get redoCount(){return redos.length;},
 get sharedSlots(){return p.version===2?p.directions[p.activeDirection].flatMap((f,i)=>f.celId===frame().celId?[i]:[]):[p.activeFrame];},get celName(){return p.version===2?p.cels[frame().celId].name:frame().name;},
 begin(){end();stroke=clone(p);},end,cancel(){if(stroke){p=stroke;stroke=null;}},
 paint(x,y,id,mirror=false,choice='auto'){if(!stroke)bad('Start a stroke first.');if(!Number.isInteger(x)||!Number.isInteger(y)||x<0||y<0||x>=WIDTH||y>=HEIGHT)return;const side=sideFor(p.activeDirection,x,choice),category=PART_DEFINITIONS[id]?.category;if(!category)bad('Unknown part.');const labels=currentLabels();labels[y*WIDTH+x]=CATEGORY_PARTS[category][side];if(mirror){const opposite=side==='left'?'right':side==='right'?'left':'center';labels[y*WIDTH+WIDTH-1-x]=CATEGORY_PARTS[category][opposite];}},
 replace(labels){const v=validateLabels(labels);return edit(()=>{if(p.version===2)p.cels[frame().celId].labels=v;else frame().labels=v;});},
 select(direction,index=0){end();if(!DIRECTIONS.includes(direction)||!Number.isInteger(index)||!p.directions[direction][index])bad('Unknown frame.');p.activeDirection=direction;p.activeFrame=index;},
 selectUnique(delta){
  end();const cels=Object.values(p.cels).filter(c=>c.direction===p.activeDirection);
  if(cels.length<2)return;
  const current=cels.findIndex(c=>c.id===frame().celId),next=cels[(current+delta+cels.length)%cels.length];
  this.select(p.activeDirection,p.directions[p.activeDirection].findIndex(f=>f.celId===next.id));
 },
 add(blank=false,linked=false){if(this.frames.length>=32)bad('Maximum 32 frames per direction.');return edit(()=>{const f=clone(frame());f.id=nextId('frame');f.name=(blank?'Blank frame':'Copy of '+f.name).slice(0,80);if(p.version===2){if(blank||!linked)f.celId=copyCel(blank);}else if(blank)f.labels=Array(SIZE).fill(0);p.directions[p.activeDirection].splice(++p.activeFrame,0,f);});},
 detach(){if(p.version!==2||this.sharedSlots.length<2)return false;return edit(()=>{frame().celId=copyCel(false);});},
 remove(){if(this.frames.length===1)bad('Keep at least one frame per direction.');return edit(()=>{p.directions[p.activeDirection].splice(p.activeFrame,1);p.activeFrame=Math.min(p.activeFrame,this.frames.length-1);if(p.version===2){const used=new Set(DIRECTIONS.flatMap(d=>p.directions[d].map(f=>f.celId)));for(const id of Object.keys(p.cels))if(!used.has(id))delete p.cels[id];}});},
 move(delta){const next=p.activeFrame+delta;if(next<0||next>=this.frames.length)return false;return edit(()=>{const fs=p.directions[p.activeDirection],[f]=fs.splice(p.activeFrame,1);fs.splice(next,0,f);p.activeFrame=next;});},
 update(values){return edit(()=>Object.assign(frame(),values));},
 import(text){let v;try{v=JSON.parse(text);}catch{bad('Import must be valid JSON.');}if(v?.schema==='critz.body-regions.corrections')return this.replace(importCorrections(text,seed));const next=migrateProject(parseProject(text,seed),seed);return edit(()=>p=next);},
 undo(){end();if(!undos.length)return false;redos.push(clone(p));p=undos.pop();return true;},redo(){end();if(!redos.length)return false;undos.push(clone(p));p=redos.pop();return true;},export(){end();return JSON.stringify(p);}
 };
}
