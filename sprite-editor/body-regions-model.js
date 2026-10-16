import {mirrorPoints} from './mirror.js';
// Labels only: source rasters and registration are never edited or included in corrections.
export const WIDTH=32, HEIGHT=64, SIZE=WIDTH*HEIGHT;
export const STORAGE='fmw.sprite-editor.body-regions.v1';
// IDs 0..13 retain their original meanings. 14..27 add explicit anatomical eyes,
// head/ear/torso/pelvis halves and true-center limb identities. Color is never identity.
export const PART_IDS=['unassigned','head','ears','eyes','torso','pelvis','leftArm','rightArm','leftHand','rightHand','leftLeg','rightLeg','leftShoe','rightShoe','leftEye','rightEye','leftHead','rightHead','leftEar','rightEar','leftTorso','rightTorso','leftPelvis','rightPelvis','centerArm','centerHand','centerLeg','centerShoe'];
export const CATEGORY_PARTS={unassigned:{left:0,right:0,center:0},head:{left:16,right:17,center:1},ear:{left:18,right:19,center:2},eye:{left:14,right:15,center:3},torso:{left:20,right:21,center:4},pelvis:{left:22,right:23,center:5},arm:{left:6,right:7,center:24},hand:{left:8,right:9,center:25},leg:{left:10,right:11,center:26},shoe:{left:12,right:13,center:27}};
const categoryNames={unassigned:'Unassigned',head:'Head',ear:'Ear',eye:'Eye',torso:'Torso',pelvis:'Pelvis',arm:'Arm',hand:'Hand',leg:'Leg',shoe:'Foot / shoe'};
const categoryColors={unassigned:['#273440','#273440','#273440'],head:['#d5a000','#865b00','#ad7e00'],ear:['#ff8b45','#b64b10','#d56b25'],eye:['#f00020','#900018','#c0001c'],torso:['#288ac5','#134d7a','#206c9e'],pelvis:['#00b09d','#006b60','#008e7d'],arm:['#66ccee','#197b9d','#3aa4c5'],hand:['#ee7733','#a43f0b','#ce5920'],leg:['#50b83e','#216b19','#378f2b'],shoe:['#0047ff','#17247e','#1736b4']};
const oldNames=['Unassigned','Head','Ears','Eyes','Torso','Pelvis','Left arm','Right arm','Left hand','Right hand','Left leg','Right leg','Left shoe','Right shoe'];
export const PART_DEFINITIONS=PART_IDS.map((key,id)=>{
 const category=Object.keys(CATEGORY_PARTS).find(c=>Object.values(CATEGORY_PARTS[c]).includes(id));
 const side=id===0?'none':Object.entries(CATEGORY_PARTS[category]).find(([,v])=>v===id)[0];
 const name=oldNames[id]||`${side[0].toUpperCase()+side.slice(1)} ${category}`;
 return{id,key,name,category,side,color:categoryColors[category][side==='left'?0:side==='right'?1:2]};
});
export const PART_OPTIONS=Object.entries(CATEGORY_PARTS).map(([category,ids])=>({id:ids.left,name:categoryNames[category]}));
export function anatomicalSide(x,width=WIDTH,facing='front'){
 if(facing!=='front')throw Error('Automatic anatomical labels support the registered front view only.');
 if(!Number.isInteger(width)||width<1||!Number.isInteger(x)||x<0||x>=width)return null;
 return x===(width-1)/2?'center':x<(width-1)/2?'right':'left';
}
export function anatomicalPartId(id,x,width=WIDTH,facing='front'){
 if(!Number.isInteger(id)||!PART_DEFINITIONS[id])throw Error('Unknown label.');
 const side=anatomicalSide(x,width,facing);return side===null?null:CATEGORY_PARTS[PART_DEFINITIONS[id].category][side];
}
// Only old generic categories need position-based splitting. Already explicit
// anatomical identities remain stable even when a pose crosses the centerline.
export function migrateLegacyLabels(labels,facing='front'){
 return labels.map((id,i)=>id>=1&&id<=5?anatomicalPartId(id,i%WIDTH,WIDTH,facing):id);
}
function currentParts(parts,version){
 if(version!==1)return parts;
 return PART_DEFINITIONS.map((p,i)=>i<14?{...p,name:parts[i].name}:{...p});
}
const fail=message=>{throw Error(message);};
const isObject=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
function keys(v,allowed,required=allowed){
 if(!isObject(v)||Object.keys(v).some(k=>!allowed.includes(k))||required.some(k=>!Object.hasOwn(v,k)))fail('Unexpected or missing fields.');
}
// Metadata is inert JSON, bounded, and compared canonically. Never merge imported objects.
function safeMetadata(value,depth=0){
 if(depth>8)fail('Metadata is too deeply nested.');
 if(value===null||typeof value==='boolean')return;
 if(typeof value==='number'&&Number.isFinite(value))return;
 if(typeof value==='string'&&value.length<=2048)return;
 if(Array.isArray(value)&&value.length<=32){value.forEach(v=>safeMetadata(v,depth+1));return;}
 if(isObject(value)&&Object.keys(value).length<=32){for(const [k,v]of Object.entries(value)){if(['__proto__','prototype','constructor'].includes(k)||k.length>80)fail('Unsafe metadata field.');safeMetadata(v,depth+1);}return;}
 fail('Invalid metadata.');
}
export function canonical(value){return JSON.stringify(value,(_,v)=>isObject(v)?Object.fromEntries(Object.keys(v).sort().map(k=>[k,v[k]])):v);}
export function validateLabels(labels,partCount=PART_IDS.length){
 if(!Array.isArray(labels)||labels.length!==SIZE||Array.from(labels).some(v=>!Number.isInteger(v)||v<0||v>=partCount))fail(`Expected all 2048 labels, each an integer from 0 to ${partCount-1}.`);
 return labels.slice();
}
export function validateSeed(seed){
 keys(seed,['schema','version','seedId','width','height','source','registration','parts','referenceRGBA','dummyRGBA','labels']);
 if(typeof seed.seedId!=='string'||!/^[-a-zA-Z0-9_.]{1,100}$/.test(seed.seedId))fail('Invalid seed identity.');
 if(seed.schema!=='critz.body-regions.seed'||![1,2].includes(seed.version)||seed.width!==WIDTH||seed.height!==HEIGHT)fail('Expected a version 1 or 2 registered 32 × 64 body-region seed.');
 safeMetadata(seed.source);safeMetadata(seed.registration);
 keys(seed.source,['reference','dummy','segmentation']);
 keys(seed.source.reference,['id','url','gifSha256','frame'],['id','gifSha256','frame']);
 keys(seed.source.dummy,['id','commit','sha256'],['id','sha256']);
 keys(seed.source.segmentation,['id','sha256']);
 for(const [name,source]of Object.entries(seed.source)){const hash=name==='reference'?source.gifSha256:source.sha256;if(typeof source.id!=='string'||!source.id||typeof hash!=='string'||!/^[a-f0-9]{64}$/i.test(hash))fail('Each source needs an identity and SHA-256.');}
 if(seed.source.reference.frame!==2)fail('Expected the frozen reference frame 2.');
 const r=seed.registration;
 if(canonical(r.crop)!=='[0,0,128,192]'||r.displayDivisor!==4||canonical(r.native)!=='[32,48]'||canonical(r.translation)!=='[0,16]'||r.centerlineX!==15.5||r.contactEdgeY!==62||r.facing!=='front'||typeof r.leftRight!=='string'||!r.leftRight.includes('character-relative'))fail('Seed registration does not match the frozen front reference.');
 const partCount=seed.version===1?14:PART_IDS.length;
 if(!Array.isArray(seed.parts)||seed.parts.length!==partCount)fail(`Expected all ${partCount} named parts.`);
 Array.from(seed.parts).forEach((p,i)=>{keys(p,seed.version===1?['id','name','color']:['id','key','name','color','category','side']);if(p.id!==i||seed.version===2&&(p.key!==PART_IDS[i]||p.category!==PART_DEFINITIONS[i].category||p.side!==PART_DEFINITIONS[i].side)||typeof p.name!=='string'||!p.name||p.name.length>80||!/^#[a-f0-9]{6}$/i.test(p.color))fail('Invalid body-part definition.');});
 for(const rgba of [seed.referenceRGBA,seed.dummyRGBA])if(!Array.isArray(rgba)||rgba.length!==SIZE*4||Array.from(rgba).some(v=>!Number.isInteger(v)||v<0||v>255))fail('Expected 8192 RGBA bytes per source layer.');
 validateLabels(seed.labels,partCount);
 const current=structuredClone(seed);current.parts=currentParts(current.parts,seed.version).map((p,i)=>({...p,color:PART_DEFINITIONS[i].color}));current.labels=seed.version===1?migrateLegacyLabels(current.labels,current.registration.facing):current.labels;current.version=2;return current;
}
export function correctionData(seed,labels){return{schema:'critz.body-regions.corrections',version:2,seedId:seed.seedId,width:WIDTH,height:HEIGHT,labelOrder:'row-major-top-left',source:structuredClone(seed.source),registration:structuredClone(seed.registration),parts:structuredClone(currentParts(seed.parts,seed.version)),labels:seed.version===1?migrateLegacyLabels(validateLabels(labels),seed.registration.facing):validateLabels(labels)};}
export function exportCorrections(seed,labels){return JSON.stringify(correctionData(seed,labels));}
export function importCorrections(text,seed){
 if(typeof text!=='string'||text.length>100000)fail('Correction text must be smaller than 100 KB.');
 let data;try{data=JSON.parse(text);}catch{fail('Corrections must be valid JSON.');}
 keys(data,['schema','version','seedId','width','height','labelOrder','source','registration','parts','labels']);
 if(data.schema!=='critz.body-regions.corrections'||![1,2].includes(data.version)||data.width!==WIDTH||data.height!==HEIGHT||data.labelOrder!=='row-major-top-left')fail('Wrong correction format, version, dimensions or label order.');
 safeMetadata(data.source);safeMetadata(data.registration);safeMetadata(data.parts);
 if(Array.isArray(data.parts))for(const [i,part]of data.parts.entries()){keys(part,data.version===1?['id','name','color']:['id','key','name','color','category','side']);if(part.id!==i||typeof part.name!=='string'||!/^#[a-f0-9]{6}$/i.test(part.color))fail('Invalid body-part definition.');}
 for(const key of ['seedId','source','registration'])if(canonical(data[key])!==canonical(seed[key]))fail(`Corrections have different ${key}. Load the matching source seed first.`);
 if(!Array.isArray(data.parts)||data.parts.length!==(data.version===1?14:PART_IDS.length)||canonical(currentParts(data.parts,data.version))!==canonical(currentParts(seed.parts,seed.version)))fail('Corrections have different parts. Load the matching source seed first.');
 const labels=validateLabels(data.labels,data.version===1?14:PART_IDS.length);return data.version===1?migrateLegacyLabels(labels,seed.registration.facing):labels;
}
export function pixelAt(clientX,clientY,rect){
 const x=Math.floor((clientX-rect.left)*WIDTH/rect.width),y=Math.floor((clientY-rect.top)*HEIGHT/rect.height);
 return x>=0&&y>=0&&x<WIDTH&&y<HEIGHT?[x,y]:null;
}
export function createLabelModel(initial){
 let labels=validateLabels(initial),undo=[],redo=[],stroke=null;
 const end=()=>{if(!stroke)return false;const delta=[...stroke].filter(([i,v])=>labels[i]!==v);stroke=null;if(!delta.length)return false;undo.push(delta);if(undo.length>200)undo.shift();redo=[];return true;};
 return{
  get labels(){return labels.slice();},get undoCount(){return undo.length;},get redoCount(){return redo.length;},
  begin(){end();stroke=new Map();},
  paint(x,y,id,mirror=false){if(!stroke)fail('Start a stroke before painting.');if(!Number.isInteger(id)||id<0||id>=PART_IDS.length)fail('Unknown label.');if(!Number.isInteger(x)||!Number.isInteger(y)||x<0||y<0||x>=WIDTH||y>=HEIGHT)return;for(const [px,py]of mirrorPoints(WIDTH,x,y,mirror)){const i=py*WIDTH+px;if(!stroke.has(i))stroke.set(i,labels[i]);labels[i]=id;}},
  paintAnatomical(x,y,id,mirror=false,facing='front'){
   // Resolve before any write, so an unsupported facing cannot partially mutate a stroke.
   const targets=mirrorPoints(WIDTH,x,y,mirror).map(([px,py])=>[px,py,anatomicalPartId(id,px,WIDTH,facing)]);
   for(const [px,py,part]of targets)if(part!==null)this.paint(px,py,part);
  },
  end,
  cancel(){if(!stroke)return false;for(const [i,v]of stroke)labels[i]=v;stroke=null;return true;},
  undo(){end();if(!undo.length)return false;const delta=undo.pop();redo.push(delta.map(([i,v])=>{const next=[i,labels[i]];labels[i]=v;return next;}));return true;},
  redo(){end();if(!redo.length)return false;const delta=redo.pop();undo.push(delta.map(([i,v])=>{const next=[i,labels[i]];labels[i]=v;return next;}));return true;},
  replace(next){end();next=validateLabels(next);const delta=[];next.forEach((v,i)=>{if(v!==labels[i])delta.push([i,labels[i]]);});if(!delta.length)return false;undo.push(delta);labels=next;redo=[];return true;},
 };
}
