// Original native Critz artwork. Reads no reference images or prior sprite pixels.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {Pixels} from '../living-collection-v1/pixels.mjs';
import {describe,readProjectData,gifBytes,validateProject} from '../../../sprite-editor/model.js';
const require=createRequire(import.meta.url),sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'../../..');
const source=path.join(root,'art/source/button-v2'),out=path.join(root,'assets/playable/button-v2');
fs.mkdirSync(out,{recursive:true});
const P={o:'#343e36',s:'#684a35',d:'#a16c43',m:'#c69757',l:'#e6bd78',h:'#f6dfa3',b:'#82977a',a:'#a7b28c',c:'#d7d9ae',e:'#232d30',w:'#fbefce'};
// Hand-authored whorl: no ellipse rasterization, noise, resampling or dilation.
const shell=[
 '......ooooo......',
 '....oohhhlloo....',
 '...ohhhllllmmo...',
 '..ohhllmmmmddmo..',
 '.ohllmmmssdddmmo.',
 '.ollmmsslmmssdmmo',
 'olmmmslhlmdmsdmmo',
 'olmmslhllmmmsdmmo',
 'olmmslmmssmmsdmmo',
 'olmmsssssmmmsdmmo',
 '.ommmmmmmmmsddmo.',
 '.odmmmmmmmssddmo.',
 '..oddddddddssmo..',
 '...ossddddssoo...',
 '.....ooooooo.....',
];
function snail(phase=0,action='glide'){
 const p=new Pixels(32,32),wave=[0,0,1,1,0,0,-1,-1][phase%8];
 const retract=action==='tuck'? [0,1,3,1][phase%4]:0;
 const nibble=action==='nibble'?[0,1,2,1][phase%4]:0;
 const lean=action==='look'?[0,-1,0,1][phase%4]:wave;
 // The foot moves as a low connected wave; shell remains registered throughout.
 p.stamp(3,23,['...oooooooooooooooooo...','..obbaaaaaaacaaaaaaabbo.','.obbaacccccccccccccaaabo','obbaaaacccaaaacccaaaabbo','..oooooooooooooooooooo..'],P);
 p.line(6+wave,27,10+wave,27,P.a);p.line(15-wave,27,19-wave,27,P.c);
 const hx=23-retract,hy=22+nibble;
 p.rect(hx-2,hy,hx+2,hy+3,P.o);p.rect(hx-2,hy+1,hx+1,hy+3,P.a);p.line(hx-1,hy,hx+1,hy,P.c);
 // Two long eyestalks remain attached to the head in every pose.
 const stalks=retract===3?[[hx-1,hy-3],[hx+2,hy-2]]:[[hx-2+lean,hy-7+nibble],[hx+4+lean,hy-6+nibble]];
 stalks.forEach(([x,y],i)=>{p.line(hx+(i?1:-1),hy+1,x,y,P.o);p.line(hx+(i?1:-1),hy,x,y+1,P.a);p.rect(x-1,y-1,x+1,y,P.e);if(!(action==='look'&&phase===2))p.p(x,y-1,P.w);});
 // Short feelers / mouth stay low; nibbling is a head action, never a shell bounce.
 p.line(hx+1,hy+2,hx+4,hy+1,P.b);p.p(hx+3,hy+2,P.o);
 p.stamp(4,10,shell,P);
 // Small aperture separates the shell lip from the living foot.
 p.line(17,23,19,24,P.s);p.p(18,23,P.l);
 return p;
}
const sequences={glide:{frames:Array.from({length:8},(_,i)=>snail(i)),ticks:Array(8).fill(9)},look:{frames:Array.from({length:4},(_,i)=>snail(i,'look')),ticks:[24,12,6,24]},nibble:{frames:Array.from({length:4},(_,i)=>snail(i,'nibble')),ticks:[12,9,12,15]},tuck:{frames:Array.from({length:4},(_,i)=>snail(i,'tuck')),ticks:[9,12,24,12]}};
const frames=Object.values(sequences).flatMap(s=>s.frames),ticks=Object.values(sequences).flatMap(s=>s.ticks);
const palette=[null,...new Set(frames.flatMap(p=>p.a.filter(Boolean)))];
const project={format:'fmw-sprite',version:1,name:'Button · native personality motion v2',preset:'custom',width:32,height:32,palette,bank:'custom',notes:'Original M1.OV1 pixels. Observation scale, not biological scale. Fixed shell/ground registration; gliding foot, attached eyestalks, look/nibble/tuck actions. No cast shadow.',frames:frames.map((p,i)=>({name:i<8?'Glide '+i:i<12?'Look '+(i-8):i<16?'Nibble '+(i-12):'Tuck '+(i-16),ticks:ticks[i],pixels:p.a.map(c=>palette.indexOf(c))}))};
const rle=describe(project),roundtrip=readProjectData(JSON.parse(rle),new Set(palette.slice(1)));
validateProject(project,new Set(palette.slice(1)));
if(JSON.stringify(roundtrip.frames)!==JSON.stringify(project.frames))throw Error('RLE round trip differs');
fs.writeFileSync(path.join(source,'button.sprite.json'),JSON.stringify(project)+'\n');fs.writeFileSync(path.join(source,'button.rle.json'),rle+'\n');
const columns=8,sheet=new Pixels(256,96),assets=[];
let index=0;
for(const [action,s] of Object.entries(sequences)){
 const id=action==='glide'?'button-snail':'button-'+action;
 for(let i=0;i<s.frames.length;i++,index++){
  const p=s.frames[i],x=index%columns*32,y=Math.floor(index/columns)*32;
  sheet.blit(p,x,y);await sharp(p.rgba(),{raw:{width:32,height:32,channels:4}}).png().toFile(path.join(out,`${action}-${i}.png`));
  assets.push({id:`${id}.${i}`,rect:[x,y,32,32],anchor:[16,32],ticks:s.ticks[i],rgbaSHA256:crypto.createHash('sha256').update(p.rgba()).digest('hex')});
 }
 const actionProject={...project,frames:project.frames.slice(index-s.frames.length,index)};
 fs.writeFileSync(path.join(out,`${action}.gif`),gifBytes(actionProject));
}
await sharp(sheet.rgba(),{raw:{width:256,height:96,channels:4}}).png().toFile(path.join(out,'atlas.png'));
fs.writeFileSync(path.join(out,'atlas.json'),JSON.stringify({schemaVersion:1,id:'critz.button.v2',task:'M1.OV1',image:'atlas.png',size:[256,96],source:'art/source/button-v2/button.sprite.json',tickSeconds:280896/16777216,approval:'new appearance awaits morning visual review',provenance:'Original native-cell authoring; no external images or audio',assets},null,2)+'\n');
console.log('Button v2: 20 original native poses; indexed/RLE, transparent PNGs, four native GIFs and runtime atlas.');
