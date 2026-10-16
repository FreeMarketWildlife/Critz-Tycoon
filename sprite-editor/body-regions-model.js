import {mirrorPoints} from './mirror.js';
// Labels only: source rasters and registration are never edited or included in corrections.
export const WIDTH=32, HEIGHT=64, SIZE=WIDTH*HEIGHT;
export const STORAGE='fmw.sprite-editor.body-regions.v1';
export const PART_IDS=['unassigned','head','ears','eyes','torso','pelvis','leftArm','rightArm','leftHand','rightHand','leftLeg','rightLeg','leftShoe','rightShoe'];
// UI categories keep the stable v1 serialized IDs. Paired paint resolves each target independently.
export const PART_OPTIONS=[{id:0,name:'Unassigned'},{id:1,name:'Head'},{id:2,name:'Ears'},{id:3,name:'Eyes'},{id:4,name:'Torso'},{id:5,name:'Pelvis'},{id:6,name:'Arm'},{id:8,name:'Hand'},{id:10,name:'Leg'},{id:12,name:'Foot / shoe'}];
export function anatomicalPartId(id,x,width=WIDTH,facing='front'){
 if(!Number.isInteger(id)||id<0||id>=PART_IDS.length)throw Error('Unknown label.');
 if(!Number.isInteger(x)||x<0||x>=width)return null;
 if(id<6)return id;
 if(facing!=='front')throw Error('Automatic paired labels support the registered front view only.');
 if(x===(width-1)/2)return null; // Exact odd-width center has no unambiguous paired side.
 const leftId=id-id%2;
 return x<(width-1)/2?leftId+1:leftId; // Viewer-left is character-right in the front view.
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
export function validateLabels(labels){
 if(!Array.isArray(labels)||labels.length!==SIZE||Array.from(labels).some(v=>!Number.isInteger(v)||v<0||v>=PART_IDS.length))fail('Expected all 2048 labels, each an integer from 0 to 13.');
 return labels.slice();
}
export function validateSeed(seed){
 keys(seed,['schema','version','seedId','width','height','source','registration','parts','referenceRGBA','dummyRGBA','labels']);
 if(typeof seed.seedId!=='string'||!/^[-a-zA-Z0-9_.]{1,100}$/.test(seed.seedId))fail('Invalid seed identity.');
 if(seed.schema!=='critz.body-regions.seed'||seed.version!==1||seed.width!==WIDTH||seed.height!==HEIGHT)fail('Expected a version 1 registered 32 × 64 body-region seed.');
 safeMetadata(seed.source);safeMetadata(seed.registration);
 keys(seed.source,['reference','dummy','segmentation']);
 keys(seed.source.reference,['id','url','gifSha256','frame'],['id','gifSha256','frame']);
 keys(seed.source.dummy,['id','commit','sha256'],['id','sha256']);
 keys(seed.source.segmentation,['id','sha256']);
 for(const [name,source]of Object.entries(seed.source)){const hash=name==='reference'?source.gifSha256:source.sha256;if(typeof source.id!=='string'||!source.id||typeof hash!=='string'||!/^[a-f0-9]{64}$/i.test(hash))fail('Each source needs an identity and SHA-256.');}
 if(seed.source.reference.frame!==2)fail('Expected the frozen reference frame 2.');
 const r=seed.registration;
 if(canonical(r.crop)!=='[0,0,128,192]'||r.displayDivisor!==4||canonical(r.native)!=='[32,48]'||canonical(r.translation)!=='[0,16]'||r.centerlineX!==15.5||r.contactEdgeY!==62||r.facing!=='front'||typeof r.leftRight!=='string'||!r.leftRight.includes('character-relative'))fail('Seed registration does not match the frozen front reference.');
 if(!Array.isArray(seed.parts)||seed.parts.length!==PART_IDS.length)fail('Expected all 14 named parts.');
 Array.from(seed.parts).forEach((p,i)=>{keys(p,['id','name','color']);if(p.id!==i||typeof p.name!=='string'||!p.name||p.name.length>80||!/^#[a-f0-9]{6}$/i.test(p.color))fail('Invalid body-part definition.');});
 for(const rgba of [seed.referenceRGBA,seed.dummyRGBA])if(!Array.isArray(rgba)||rgba.length!==SIZE*4||Array.from(rgba).some(v=>!Number.isInteger(v)||v<0||v>255))fail('Expected 8192 RGBA bytes per source layer.');
 validateLabels(seed.labels);
 return structuredClone(seed);
}
export function correctionData(seed,labels){return{schema:'critz.body-regions.corrections',version:1,seedId:seed.seedId,width:WIDTH,height:HEIGHT,labelOrder:'row-major-top-left',source:structuredClone(seed.source),registration:structuredClone(seed.registration),parts:structuredClone(seed.parts),labels:validateLabels(labels)};}
export function exportCorrections(seed,labels){return JSON.stringify(correctionData(seed,labels));}
export function importCorrections(text,seed){
 if(typeof text!=='string'||text.length>100000)fail('Correction text must be smaller than 100 KB.');
 let data;try{data=JSON.parse(text);}catch{fail('Corrections must be valid JSON.');}
 keys(data,['schema','version','seedId','width','height','labelOrder','source','registration','parts','labels']);
 if(data.schema!=='critz.body-regions.corrections'||data.version!==1||data.width!==WIDTH||data.height!==HEIGHT||data.labelOrder!=='row-major-top-left')fail('Wrong correction format, version, dimensions or label order.');
 safeMetadata(data.source);safeMetadata(data.registration);safeMetadata(data.parts);
 for(const key of ['seedId','source','registration','parts'])if(canonical(data[key])!==canonical(seed[key]))fail(`Corrections have different ${key}. Load the matching source seed first.`);
 return validateLabels(data.labels);
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
