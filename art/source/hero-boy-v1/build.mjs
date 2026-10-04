import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {createRequire}from'node:module';
import {readProjectData,describe,gifBytes}from'../../../sprite-editor/model.js';
const require=createRequire(import.meta.url),sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const root=path.dirname(new URL(import.meta.url).pathname),repo=path.resolve(root,'../../..'),out=path.join(repo,'assets/review/hero-boy-v1-walk'),official=path.join(repo,'assets/characters/hero-boy-v1');
const original=fs.readFileSync(path.join(root,'user-approved.rle.json')),rle=JSON.parse(original),p=readProjectData(rle,new Set(rle.palette.slice(1)));
if(p.width!==32||p.height!==64||p.frames.length!==1)throw Error('Expected one approved 32x64 still');
if(crypto.createHash('sha256').update(original).digest('hex')!=='bef3289d8d62801ea2f223ae9359beb305856764a54afed8fe9990f42676fb3a')throw Error('Approved V1 source changed; create a new version instead');
const idle=p.frames[0].pixels.slice();
function stride(forwardRight){
 const a=Array(2048).fill(0);
 const pixel=(x,y,c)=>{if(x<0||x>=32||y<0||y>=64)throw Error('Clipping');a[y*32+x]=c;};
 const rect=(l,t,r,b,c)=>{for(let y=t;y<=b;y++)for(let x=l;x<=r;x++)pixel(x,y,c);};
 function copy(l,t,r,b,dx,dy,shadow=false){for(let y=t;y<=b;y++)for(let x=l;x<=r;x++){let c=idle[y*32+x];if(c){if(shadow&&c===17)c=16;pixel(x+dx,y+dy,c);}}}
 const front=forwardRight?'right':'left',rear=forwardRight?'left':'right';
 // Receding leg is foreshortened, moved inward, and occluded by the pelvis.
 if(rear==='left')copy(7,57,14,61,2,-2,true);else copy(17,57,24,61,-2,-2,true);
 // The arm on the forward-foot side recedes and rises behind the head.
 if(front==='right'){copy(23,47,28,54,0,-4,true);copy(21,46,26,48,0,-2,true);}
 else {copy(3,47,8,54,0,-4,true);copy(5,46,10,48,0,-2,true);}
 // Preserve the whole visible head/hair/face with a +2px translation only.
 copy(0,0,31,44,0,2);copy(7,45,24,46,0,2);
 // Original shirt clusters and stripe order bob with the head.
 copy(9,47,22,54,0,2);
 // Compact pelvis bridging the two thighs, with a dark crotch seam.
 for(let y=57;y<=59;y++){const l=y===57?10:y===58?11:12;rect(l,y,31-l,y,14);if(y<59)rect(l+1,y,30-l,y,9);}
 rect(15,58,16,59,14);
 // Forward leg and the exact shoe color pattern move inward and down two pixels.
 if(front==='right'){copy(17,57,24,61,-2,2);rect(17,57,20,58,9);}
 else {copy(7,57,14,61,2,2);rect(11,57,14,58,9);}
 // Opposing front arm: sleeve at the shoulder, hand down alongside the torso.
 if(front==='right'){copy(3,47,8,54,0,2);copy(5,46,10,48,0,2);}
 else {copy(23,47,28,54,0,2);copy(21,46,26,48,0,2);}
 return a;
}
const frames=[{name:'Stride A · right foot forward',ticks:8,pixels:stride(true)},{name:'Hero Boy V1 · passing',ticks:8,pixels:idle},{name:'Stride B · left foot forward',ticks:8,pixels:stride(false)},{name:'Hero Boy V1 · passing',ticks:8,pixels:idle.slice()}];
const walk={...p,name:'Hero Boy V1 · front walk review',notes:'Approved idle preserved exactly. Emerald source cadence 3,0,4,0 at 8 ticks each; original stride artwork. Front only. Walk awaits user visual review.',frames};
const still={...p,name:'Hero Boy V1 · official front idle',notes:'User-approved V1. Pixels and palette unchanged from supplied export.',frames:[{...p.frames[0],name:'Idle south · official V1'}]};
fs.writeFileSync(path.join(root,'idle.sprite.json'),JSON.stringify(still,null,2)+'\n');fs.writeFileSync(path.join(root,'walk.sprite.json'),JSON.stringify(walk,null,2)+'\n');fs.writeFileSync(path.join(root,'walk.rle.json'),describe(walk)+'\n');
function rgba(a){return Buffer.from(a.flatMap(c=>c?[...Buffer.from(p.palette[c].slice(1),'hex'),255]:[0,0,0,0]));}
await sharp(rgba(idle),{raw:{width:32,height:64,channels:4}}).png().toFile(path.join(official,'idle-south.png'));
const raws=[];for(const [i,f]of frames.entries()){const raw=rgba(f.pixels);raws.push(raw);await sharp(raw,{raw:{width:32,height:64,channels:4}}).png().toFile(path.join(out,`frame-${i}.png`));}
const sheet=Buffer.alloc(128*64*4);for(let i=0;i<4;i++)for(let y=0;y<64;y++)raws[i].copy(sheet,(y*128+i*32)*4,y*128,(y+1)*128);
await sharp(sheet,{raw:{width:128,height:64,channels:4}}).png().toFile(path.join(out,'walk-sheet.png'));
fs.writeFileSync(path.join(out,'walk-native.gif'),gifBytes(walk));
// Review enlargement duplicates source cells exactly; never resample or interpolate pixels.
const zoom=6,background=p.palette.length;const large={...walk,palette:[...walk.palette,'#eee9df'],width:32*zoom,height:64*zoom,frames:frames.map(f=>({...f,pixels:Array.from({length:64*zoom},(_,y)=>Array.from({length:32*zoom},(_,x)=>f.pixels[Math.floor(y/zoom)*32+Math.floor(x/zoom)]||background)).flat()}))};
fs.writeFileSync(path.join(out,'walk-preview-6x.gif'),gifBytes(large));
fs.writeFileSync(path.join(official,'manifest.json'),JSON.stringify({schemaVersion:1,id:'hero.boy.v1.idle.south',version:1,status:'user-approved',approval:'User declared their editor-corrected still perfect and requested official V1, then supplied this exact RLE export.',file:'idle-south.png',frame:[32,64],anchor:[16,64],sourceSHA256:crypto.createHash('sha256').update(original).digest('hex'),pixelSHA256:crypto.createHash('sha256').update(rgba(idle)).digest('hex'),runtimeIntegrated:false},null,2)+'\n');
fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify({schemaVersion:1,id:'hero.boy.v1.walk.south.review1',status:'awaiting-user-animation-review',frame:[32,64],anchor:[16,64],sequence:['strideA','idleV1','strideB','idleV1'],ticksPerFrame:[8,8,8,8],tickMilliseconds:280896/16777216*1000,gifDelaysMilliseconds:[130,140,130,140],sourceReference:'pret/pokeemerald@5eff78649e7170a877b961ef0b3da13b81a16038',referenceFrames:[3,0,4,0],headStrideOffset:[0,2],footLastRow:{idle:61,stride:63},scope:'front-facing walk in place; no runtime integration'},null,2)+'\n');
console.log('Official V1 unchanged; front walk poses, native GIF, 6x GIF, source and manifests exported.');
