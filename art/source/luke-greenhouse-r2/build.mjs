// M1.LG2: original32px native service equipment. No source-game art or resampling.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {Raster} from '../raster.mjs';
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'../../..');
const src=path.join(root,'art/source/luke-greenhouse-r2'),out=path.join(root,'assets/review/luke-greenhouse-r2');
const oldOut=path.join(root,'assets/review/luke-greenhouse');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const oldHashes=Object.fromEntries(fs.readdirSync(oldOut).filter(n=>fs.statSync(path.join(oldOut,n)).isFile()).map(n=>[n,hash(fs.readFileSync(path.join(oldOut,n)))]));
const C={ink:'#263940',dark:'#354b51',metal:'#617a7a',metalHi:'#a5b7a7',top:'#869e90',cream:'#d5d6ad',green:'#466a60',greenHi:'#72917a',hose:'#5eaaa6',hoseHi:'#bed4c3',cord:'#343d42',cordHi:'#656c68',cap:'#d0a75d'};
function get(a,x,y){const i=(y*a.w+x)*4;return a.p[i+3]?'#'+a.p.subarray(i,i+3).toString('hex'):null;}
function reflect(a){const b=new Raster(a.w,a.h);for(let y=0;y<a.h;y++)for(let x=0;x<a.w;x++){const c=get(a,x,y);if(c)b.dot(a.w-1-x,y,c);}return b;}
function load(name){const j=JSON.parse(fs.readFileSync(path.join(root,'art/source/luke-greenhouse',name+'.sprite.json'))),a=new Raster(j.width,j.height);j.frames[0].pixels.forEach((n,i)=>{if(j.palette[n])a.dot(i%j.width,Math.floor(i/j.width),j.palette[n]);});return a;}
function riser(){const a=new Raster(32,32);a.rect(2,0,6,32,C.green);a.rect(3,0,2,32,C.greenHi);a.rect(8,0,3,32,C.cord);a.rect(9,0,1,32,C.cordHi);a.rect(2,7,10,3,C.ink);a.rect(3,7,8,1,C.metalHi);a.rect(2,24,10,3,C.ink);a.rect(3,24,8,1,C.metalHi);return a;}
function pump(){const a=new Raster(32,64);a.blit(riser(),0,0);a.blit(riser(),0,32);
 // Ventilated metal pump on a low stand, with a mechanical pressure cap.
 a.rect(11,53,16,3,C.ink);a.rect(12,51,3,4,C.dark);a.rect(23,51,3,4,C.dark);
 a.poly([[10,35],[13,32],[25,32],[28,35],[28,49],[25,52],[12,52],[9,49],[9,38]],C.ink);
 a.poly([[12,35],[14,33],[24,33],[26,35],[25,38],[12,38]],C.top);a.rect(11,38,15,11,C.metal);a.rect(12,39,1,9,C.metalHi);a.rect(13,49,11,2,C.dark);a.line(25,38,25,48,C.dark);
 for(let y=40;y<=46;y+=3){a.rect(15,y,7,1,C.ink);a.rect(15,y+1,7,1,C.top);}a.rect(16,31,5,2,C.ink);a.rect(17,30,3,2,C.cap);a.dot(18,30,C.cream);
 // Fixed power cord loops upward to the protected vertical wall channel.
 a.line(9,25,17,25,C.cord);a.line(17,25,19,27,C.cord);a.line(19,27,19,30,C.cord);a.line(10,24,17,24,C.cordHi);a.dot(18,25,C.cordHi);a.rect(7,22,5,5,C.ink);a.rect(8,23,3,3,C.metal);
 // Air outlet and deliberately curved hose, ending exactly at adjoining tub edge.
 a.rect(26,36,3,5,C.ink);a.rect(27,37,3,3,C.hose);a.line(29,38,30,36,C.hose);a.line(30,36,30,21,C.ink);a.line(29,35,29,21,C.hose);a.line(29,21,31,18,C.hose);a.line(30,21,31,19,C.hoseHi);a.dot(31,17,C.hose);a.dot(31,18,C.hoseHi);
 return a;}
function inlet(){const a=new Raster(16,32);a.rect(0,17,9,2,C.hose);a.rect(0,17,8,1,C.hoseHi);a.line(8,18,11,21,C.hose);a.line(9,18,12,21,C.hoseHi);a.rect(10,21,4,4,C.ink);a.rect(11,21,2,3,C.metalHi);a.rect(11,24,2,2,C.hose);return a;}
function header(){const a=new Raster(416,96),tile=load('tiles');
 // Original selected glass module repeated around an exact x208 symmetry axis.
 for(let x=0;x<416;x+=32)for(let y=0;y<96;y+=32)a.blit(tile.crop(64,0,32,32),x,y);
 // Symmetrical structural posts and a restrained brass/cream ceiling beam.
 for(const x of [0,128,256,412]){a.rect(x,0,4,96,C.green);a.rect(x+1,0,1,96,C.cream);}
 a.rect(0,0,416,7,C.green);a.rect(0,2,416,2,C.greenHi);a.rect(0,7,416,2,C.cream);a.rect(0,28,416,4,C.green);
 // Three overhead lamps aligned with existing three96px aquariums.
 for(const center of [80,208,336]){a.rect(center-2,9,4,4,C.ink);a.rect(center-26,13,52,3,C.green);a.rect(center-23,16,46,3,C.cream);a.rect(center-20,19,40,1,'#edf0cf');}
 // Piping lies behind aquariums, no ground shadow or fake light gradient baked in.
 a.rect(29,31,3,65,C.cord);a.rect(30,31,1,65,C.cordHi);
 // Exact mirrored geometry and RGB; the centered lamp's left half completes it.
 for(let y=0;y<96;y++)for(let x=0;x<208;x++){const c=get(a,x,y);if(c)a.dot(415-x,y,c);}return a;}
function facade(){const old=load('greenhouse'),a=new Raster(320,192);
 for(let y=0;y<192;y++)for(let x=0;x<160;x++){const c=get(old,x,y);if(c){a.dot(x,y,c);a.dot(319-x,y,c);}}
 // Redraw roof rib construction on the same original silhouette. Equal bays
 // radiate from narrower rear eave to wider front eave, with one straight center.
 a.poly([[17,56],[44,16],[276,16],[303,56]],'#94bcb0');
 a.poly([[17,58],[303,58],[290,78],[30,78]],'#5d9b8c');
 for(const [rear,front,lip] of [[44,17,30],[73,52,62],[102,88,94],[131,124,126],[159,159,159]]){
  a.line(rear,17,front,54,'#517d70');a.line(rear+1,17,front+1,54,'#d1dfb9');
  a.line(front,60,lip,75,'#517d70');a.line(front+1,60,lip+1,75,'#afd0ab');
 }
 a.rect(14,55,292,5,'#3c6959');a.rect(16,55,288,2,'#c4d5a9');
 for(let y=15;y<78;y++)for(let x=0;x<160;x++){const c=get(a,x,y);if(c)a.dot(319-x,y,c);}
 a.rect(17,174,286,3,'#c7b58e');a.rect(17,177,286,2,'#5e6857');
 // Keep original decorative fish icon and practical single-sided door latch.
 a.blit(old.crop(112,84,96,22),112,84);a.blit(old.crop(144,111,32,64),144,111);
 // Threshold is deliberately centered, not copied from the old off-by-one step.
 a.rect(142,177,36,5,'#8f8a70');a.line(143,177,176,177,'#e0d3b0');return a;}
const D={ink:'#66443f',body:'#eea04b',light:'#ffd57d',shade:'#c16c43',fin:'#f4bb6a',eye:'#283845',white:'#fff1c1'};
function dorothy(top,phase){const a=new Raster(32,32),p=phase?1:0;
 if(!top){
  a.poly([[22,15],[28,9-p],[30,10],[28,16],[31,21+p],[29,23],[22,18]],D.ink);
  a.poly([[24,15],[28,11-p],[27,16],[29,21+p],[26,19],[23,17]],D.fin);a.line(24,16,28,13,D.light);a.line(24,17,28,20,D.shade);
  a.poly([[11,13],[17,7],[19,8],[21,14]],D.ink);a.poly([[13,12],[17,9],[19,13]],D.fin);a.line(17,10,18,13,D.light);
  a.poly([[4,14],[8,11],[14,10],[20,12],[25,15],[25,18],[19,21],[11,23],[6,21],[3,18]],D.ink);
  a.poly([[5,14],[9,12],[14,11],[19,13],[23,15],[24,17],[19,20],[11,22],[7,20],[4,17]],D.body);
  a.poly([[6,14],[10,12],[14,12],[18,14],[14,15],[8,16],[5,17]],D.light);
  a.poly([[8,20],[13,20],[20,18],[23,17],[20,20],[11,22]],D.shade);
  a.rect(5,15,2,3,D.eye);a.dot(5,15,D.white);a.dot(3,17,D.fin);a.dot(3,18,D.ink);a.dot(7,19,D.fin);
  a.poly([[11,18],[15,19],[13+p,23],[11,22]],D.shade);a.line(12,19,13,21,D.light);
  a.poly([[18,20],[22,22],[19,23],[17,22]],D.ink);a.line(18,21,20,22,D.fin);
 }else{
  a.poly([[14,22],[9-p,28],[8,30],[14,28],[16,25],[18,28],[24,30],[23+p,27],[18,22]],D.ink);
  a.poly([[15,23],[11-p,28],[15,26],[16,24],[18,26],[21+p,28],[18,23]],D.fin);
  a.poly([[14,3],[18,3],[21,7],[22,13],[20,19],[18,24],[14,24],[12,19],[10,13],[11,7]],D.ink);
  a.poly([[14,4],[18,4],[20,8],[21,13],[19,19],[17,23],[15,23],[13,18],[11,13],[12,8]],D.body);
  a.poly([[14,5],[17,4],[18,7],[17,19],[16,22],[13,16],[12,11]],D.light);a.line(18,9,19,18,D.shade);
  a.rect(11,7,2,3,D.eye);a.dot(11,7,D.white);a.rect(20,7,2,3,D.eye);a.dot(20,7,D.white);a.rect(15,3,2,1,D.fin);
  a.poly([[11,12],[6-p,15],[7,17],[12,15]],D.shade);a.line(8,15,10,14,D.light);
  a.poly([[21,12],[26+p,15],[25,17],[20,15]],D.shade);a.line(22,14,24,15,D.light);
  a.line(16,11,16,20,D.shade);a.line(15,12,15,18,D.fin);
 }return a;}
function dorothyFront(phase){const a=new Raster(32,32);a.poly([[13,8],[15,3],[17,3],[19,8]],D.ink);a.line(16,4,16,9,D.fin);
 a.poly([[10,16],[5,13+phase],[3,16],[6,20],[11,20]],D.ink);a.poly([[21,16],[26,13+phase],[28,16],[25,20],[20,20]],D.ink);a.line(5,16,9,19,D.fin);a.line(22,19,26,16,D.fin);
 a.poly([[11,9],[15,7],[19,8],[22,11],[24,17],[22,23],[18,26],[13,26],[9,22],[8,16]],D.ink);a.poly([[12,10],[15,8],[18,9],[21,12],[23,17],[21,22],[18,25],[14,25],[10,22],[9,16]],D.body);a.poly([[12,11],[15,9],[18,10],[19,17],[17,23],[13,23],[10,18]],D.light);a.line(20,15,21,20,D.shade);
 for(const x of [10,19]){a.rect(x,14,3,3,D.eye);a.dot(x,14,D.white);}a.oval(13,19,6,5,D.shade);a.oval(14,20,4,3,D.eye);a.dot(14,20,D.fin);a.poly([[12,26],[9,29],[15,27],[17,27],[22,29],[19,26]],D.fin);return a;}
function tinyDorothy(top,phase,golden=false){const a=new Raster(16,16),q=golden?{...D,ink:'#936130',body:'#f6c74d',light:'#fff1a2',shade:'#d89d32',fin:'#ffe280'}:D,p=phase?1:0;
 if(top){a.poly([[7,11],[4-p,15],[7,13],[8,12],[10,14],[12+p,15],[9,10]],q.ink);a.line(6,13,7,11,q.fin);a.line(9,12,11,14,q.fin);a.poly([[7,1],[9,1],[11,4],[11,8],[9,12],[7,12],[5,8],[5,4]],q.ink);a.poly([[7,2],[9,2],[10,5],[10,8],[8,11],[6,8],[6,5]],q.body);a.line(7,3,7,9,q.light);a.dot(5,4,q.eye);a.dot(10,4,q.eye);a.line(5,6,3,8+p,q.fin);a.line(11,6,13,8+p,q.fin);a.line(8,6,8,10,q.shade);
 }else{a.poly([[11,7],[14,3-p],[15,4],[14,8],[15,12],[12,10],[10,9]],q.ink);a.line(12,8,14,5,q.fin);a.line(12,9,14,11,q.fin);a.poly([[5,6],[8,3],[10,6]],q.shade);a.dot(8,4,q.fin);a.poly([[2,7],[5,5],[8,5],[12,7],[12,9],[8,11],[4,11],[1,9]],q.ink);a.poly([[3,7],[5,6],[8,6],[11,8],[10,9],[7,10],[4,10],[2,9]],q.body);a.line(4,7,8,7,q.light);a.dot(3,8,q.eye);a.dot(3,7,q.white);a.dot(1,9,q.fin);a.line(6,9,7,12-p,q.shade);a.dot(7,11-p,q.fin);}return a;}
const dorothySheet=new Raster(128,32),dorothyFaceSheet=new Raster(64,32),dorothyShadowSheet=new Raster(64,32),dorothyWorldSheet=new Raster(64,16),hopperSheet=new Raster(32,16);
for(let phase=0;phase<2;phase++){dorothySheet.blit(dorothy(false,phase),phase*32,0);const top=dorothy(true,phase);dorothySheet.blit(top,64+phase*32,0);dorothyFaceSheet.blit(dorothyFront(phase),phase*32,0);const mask=new Raster(32,32);for(let y=0;y<32;y++)for(let x=0;x<32;x++)if(get(top,x,y))mask.dot(x,y,'#16373c');dorothyShadowSheet.blit(mask,phase*32,0);dorothyWorldSheet.blit(tinyDorothy(true,phase),phase*16,0);dorothyWorldSheet.blit(tinyDorothy(false,phase),32+phase*16,0);hopperSheet.blit(tinyDorothy(false,phase,true),phase*16,0);}
async function save(id,a){await a.save(path.join(out,id+'.png'));const palette=[null],pixels=[];for(let y=0;y<a.h;y++)for(let x=0;x<a.w;x++){const c=get(a,x,y);let i=palette.indexOf(c);if(i<0){i=palette.length;palette.push(c);}pixels.push(i);}fs.writeFileSync(path.join(src,id+'.sprite.json'),JSON.stringify({format:'fmw-sprite',version:1,name:id,width:a.w,height:a.h,palette,frames:[{name:'native',ticks:1,pixels}]})+'\n');return {path:'assets/review/luke-greenhouse-r2/'+id+'.png',width:a.w,height:a.h,paletteColors:palette.length-1,sha256:hash(fs.readFileSync(path.join(out,id+'.png')))};}
const p=pump(),r=riser(),i=inlet(),h=header(),g=facade();const assets={'equipment-left':p,'equipment-right':reflect(p),'inlet-left':i,'inlet-right':reflect(i),'wall-riser-left':r,'wall-riser-right':reflect(r),'header':h,'greenhouse':g,'dorothy':dorothySheet,'dorothy-front':dorothyFaceSheet,'dorothy-silhouettes':dorothyShadowSheet,'dorothy-world':dorothyWorldSheet,'gold-hopper':hopperSheet};
const manifest={schemaVersion:1,task:'M1.LG2',status:'awaiting-user-review',nativeCell:[32,32],room:{frame:[416,544],symmetryAxisX:208,doorCell:[6,16]},equipment:{frame:[32,64],leftCellX:1,rightCellX:11,tubRows:[4,7,10,13],blockedFootprint:[1,2],sortAnchor:[16,64],drawOrder:'after floor; before over-tub inlet; no castshadow baked'},inlet:{frame:[16,32],leftOrigin:'tub top-left',rightOrigin:'tub top-left+(80,0)',leftNozzle:[12,25],rightNozzle:[3,25],drawOrder:'after tub, before bubbles',collision:'included in existing tub footprint'},riser:{frame:[32,32],collision:'visual wall channel; do not infer extra blocked cells'},header:{frame:[416,96],origin:[0,0],drawOrder:'behind three existing wall tanks; no new collision',symmetricRGBA:true},facade:{frame:[320,192],symmetryAxisX:160,door:[144,111,32,64],threshold:[142,177,36,5],symmetry:'mirrored architectural pixels; original fish sign and door latch remain asymmetric details'},dorothy:{kind:16,name:'Dorothy',variety:'common goldfish',columns:['side0','side1','top0','top1'],frame:[32,32],frontColumns:['front0','front1'],worldColumns:['top0','top1','side0','side1'],worldFrame:[16,16],topDirection:'north',sideDirection:'west',notes:'Original plain streamlined goldfish; no wen; dorsalfin; single forked tail. Existing16 fancy fish remain frozen.'},goldHopper:{frame:[16,16],columns:['side0','side1'],direction:'west',notes:'Original golden common goldfish mascot. Parent owns hopping,sparkles and shadow animation.'},sourceFrozenHashes:oldHashes,assets:{}};
for(const [id,a] of Object.entries(assets))manifest.assets[id]=await save(id,a);
fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
for(const [n,digest]of Object.entries(oldHashes))if(hash(fs.readFileSync(path.join(oldOut,n)))!==digest)throw Error('Existing art changed '+n);
const proof=new Raster(416,288),floor=load('tiles').crop(0,0,32,32),tubs=load('tub-variants');for(let x=0;x<416;x+=32)for(let y=0;y<288;y+=32)proof.blit(floor,x,y);proof.blit(h,0,0);const tank=load('tank-wall');[32,160,288].forEach(x=>proof.blit(tank,x,32));for(let row=0;row<2;row++){const y=128+row*96;proof.blit(tubs.crop(row*96,0,96,64),64,y);proof.blit(tubs.crop(row*96,0,96,64),256,y);proof.blit(p,32,y);proof.blit(reflect(p),352,y);proof.blit(i,64,y);proof.blit(reflect(i),336,y);}await proof.save(path.join(out,'contact-native.png'));await proof.scale(3).save(path.join(root,'docs/reviews/M1-LG2/art-contact-3x.png'));await g.scale(3).save(path.join(root,'docs/reviews/M1-LG2/art-facade-3x.png'));
const fishProof=new Raster(256,80);fishProof.rect(0,0,256,80,'#d9dcc1');fishProof.blit(dorothySheet,0,0);fishProof.blit(dorothyFaceSheet,128,0);fishProof.blit(dorothyShadowSheet,192,0);fishProof.blit(dorothyWorldSheet,24,48);fishProof.blit(hopperSheet,144,48);await fishProof.scale(4).save(path.join(root,'docs/reviews/M1-LG2/art-dorothy-4x.png'));console.log('M1.LG2 exported13 native pieces; prior art hashes unchanged.');
