// R2: a deliberately small visual proof after the user's rejection of R1.
// Original hand-authored pixel clusters. Reference PNGs are never read here.
import { mkdir, writeFile } from 'node:fs/promises';
import { Raster } from '../environment-v1/raster.mjs';
const out='assets/review/environment-v2', review='docs/reviews/M1-E1/revision-2';
await mkdir(out,{recursive:true});await mkdir(review,{recursive:true});
const P={ink:'#50546b',shade:'#737183',woodDark:'#8c7363',wood:'#ba9864',woodLight:'#e0c184',cream:'#e6e5cb',plaster:'#cecfb3',white:'#f6efda',glass:'#69b4c3',glassLight:'#a5d9d2',roofDark:'#996e65',roof:'#c18a6b',roofLight:'#e0ad78',roofTop:'#f0cb8b',roofEdge:'#bd9c78'};
const leaf=['transparent','#315b36','#397635','#519838','#75b642','#9ed35d','#c4e984','#5e6570','#a49a69'];
const art=[];
function add(id,w,h,paint,palette='architecture'){const r=new Raster(w,h);paint(r);art.push({id,r,palette});return r;}
const grass=add('ground.grass',16,16,r=>{r.rect(0,0,16,16,'#78c6a4');r.rect(3,5,1,2,'#59b88f');r.dot(4,5,'#a1dcb8');r.rect(11,12,2,1,'#a1dcb8');},'landscape');
const roof=add('roof.pantile',16,16,r=>{r.rect(0,0,16,16,P.roofDark);for(let x=0;x<16;x+=8)for(let y=0;y<16;y+=8){r.rect(x+1,y,6,7,P.roof);r.line(x+1,y+1,x+6,y+1,P.roofLight);r.line(x+1,y,x+1,y+5,P.roofTop);r.line(x+2,y+6,x+6,y+6,P.roofDark);r.line(x+7,y,x+7,y+7,P.woodDark);r.dot(x+1,y+6,P.roofLight);}});
const ridge=add('roof.ridge',16,8,r=>{r.rect(0,0,16,8,P.ink);r.rect(0,1,16,5,P.wood);for(let x=0;x<16;x+=8){r.rect(x+1,1,6,2,P.roofTop);r.rect(x+1,3,6,2,P.roofLight);r.line(x+1,5,x+6,5,P.roofDark);}r.line(0,7,15,7,P.shade);});
const eave=add('roof.eave',16,8,r=>{r.rect(0,0,16,8,P.ink);r.rect(1,1,15,2,P.shade);r.rect(1,3,15,2,'#93928e');r.line(1,5,15,5,P.ink);r.line(0,7,15,7,P.woodDark);},'structure');
const wall=add('wall.plaster',16,16,r=>{r.rect(0,0,16,16,P.plaster);r.rect(1,1,14,14,P.cream);for(const [x,y]of [[2,3],[11,5],[4,11],[12,13]]){r.rect(x,y,2,2,P.white);}r.line(0,15,15,15,P.wood);});
const column=add('wall.timber',8,16,r=>{r.rect(0,0,8,16,P.ink);r.rect(1,0,6,16,P.woodDark);r.rect(2,0,3,16,P.wood);r.line(2,0,2,15,P.woodLight);r.line(6,0,6,15,P.shade);});
const window=add('window.double',24,16,r=>{r.rect(0,0,24,16,P.plaster);r.rect(1,1,22,13,P.shade);r.rect(2,2,20,10,P.ink);r.rect(3,3,8,8,P.glass);r.rect(13,3,8,8,P.glass);r.rect(3,3,8,2,P.glassLight);r.rect(13,3,8,2,P.glassLight);r.line(3,10,10,10,'#548ea7');r.line(13,10,20,10,'#548ea7');r.rect(1,13,22,2,P.woodDark);r.line(2,13,21,13,P.woodLight);},'window');
const door=add('door.home',16,24,r=>{r.rect(0,0,16,24,P.ink);r.rect(1,1,14,22,P.shade);r.rect(3,2,10,21,P.woodDark);r.rect(4,3,8,18,P.wood);for(const x of [5,9]){r.rect(x,4,2,15,P.woodLight);r.line(x+2,4,x+2,19,P.woodDark);}r.dot(11,14,P.white);r.line(1,23,14,23,P.plaster);});
const houseParts=[];
const house=add('building.rootport.proof',96,80,r=>{
  const put=(id,img,x,y)=>{r.blit(img,x,y);houseParts.push({id,x,y});};
  // Main wall has a short front and a recessed threshold, not a tall front elevation.
  r.rect(7,53,82,27,P.ink);
  for(let x=8;x<88;x+=16)put('wall.plaster',wall,x,56);
  r.rect(9,72,78,6,P.plaster);r.line(9,76,86,76,P.woodLight);r.line(9,78,86,78,P.woodDark);
  for(const x of [8,32,80]){put('wall.timber',column,x,56);put('wall.timber',column,x,64);}
  put('window.double',window,48,58);put('door.home',door,16,56);
  // Low roof plane and its side returns; three native 16px modules plus end trim.
  r.rect(3,21,90,35,P.ink);for(let y=24;y<56;y+=16)for(let x=8;x<88;x+=16)put('roof.pantile',roof,x,y);
  r.rect(4,24,3,29,P.woodDark);r.line(4,24,4,51,P.woodLight);r.rect(89,24,3,29,P.woodDark);
  for(let x=8;x<88;x+=16)put('roof.eave',eave,x,51);
  // Raised offset upper plane makes depth readable without a front-facing triangle.
  r.rect(12,0,73,45,P.ink);
  for(let y=8;y<40;y+=16)for(let x=16;x<80;x+=16)put('roof.pantile',roof,x,y);
  for(let x=16;x<80;x+=16)put('roof.ridge',ridge,x,0);
  r.rect(13,1,3,39,P.woodDark);r.line(14,2,14,37,P.woodLight);
  r.rect(80,1,4,39,P.woodDark);r.line(80,1,80,38,P.roofLight);r.line(83,0,83,41,P.ink);
  for(let x=16;x<80;x+=16)put('roof.eave',eave,x,39);
  r.rect(14,43,2,6,P.ink);r.rect(80,43,3,6,P.ink);
  // Original rooftop accent: shallow sky-blue vent offset from the door.
  r.rect(63,9,12,9,P.ink);r.rect(64,10,10,6,P.shade);r.rect(66,11,6,3,P.glass);r.line(66,11,71,11,P.glassLight);
},'assembly');
// Four distinct cluster stamps, authored at native size, with linked jagged edges.
const clusters=[
 ['...2332.....','..2455432...','.245655432..','24556554332.','23455443222.','.2344432232.','..23332222..','...232222...'],
 ['....232.....','..2345432...','.245655432..','23455544332.','24554433222.','2344322332..','.23322322...','..22222.....'],
 ['...23432....','..2456542...','.245565432..','23455544332.','23444322322.','.233322332..','..2222332...','....2222....'],
 ['...2232.....','..2345432...','.234554432..','23445544332.','23444332222.','.233223232..','..2222232...','....2222....']
];
const trunk=add('tree.clustered.trunk',32,32,r=>{r.poly([[8,25],[24,25],[27,28],[24,31],[8,31],[5,28]],leaf[1]);r.rect(14,24,5,6,leaf[7]);r.rect(15,25,2,5,leaf[8]);r.dot(13,29,leaf[7]);r.dot(19,29,leaf[7]);},'foliage');
const canopy=add('tree.clustered.canopy',32,32,r=>{
  r.poly([[12,0],[21,1],[24,4],[24,6],[28,8],[29,13],[31,16],[30,22],[27,25],[26,28],[21,30],[13,28],[9,29],[5,26],[4,22],[1,20],[2,13],[4,11],[4,7],[8,5],[9,2]],leaf[1]);
  const stamps=[[8,0,0,0],[16,3,2,0],[2,6,1,0],[10,7,3,0],[20,9,0,1],[0,14,3,1],[8,15,2,1],[16,17,1,1],[4,21,0,2],[13,23,3,2],[22,21,2,2]];
  for(const [x,y,k,dark]of stamps)for(let yy=0;yy<clusters[k].length;yy++)for(let xx=0;xx<clusters[k][yy].length;xx++){const c=clusters[k][yy][xx];if(c!=='.')r.dot(x+xx,y+yy,leaf[Math.max(1,Number(c)-dark)]);}
  // Leaf tips interrupt the outer contour; no elliptical highlights or detached shadow.
  for(const [x,y,c]of [[11,1,6],[10,2,5],[5,8,5],[2,15,4],[28,13,4],[26,6,3],[7,25,3]])r.dot(x,y,leaf[c]);
},'foliage');
const tree=add('tree.clustered',32,32,r=>{r.blit(trunk,0,0);r.blit(canopy,0,0);r.rect(14,28,4,3,leaf[7]);r.dot(15,29,leaf[8]);},'foliage');
const flowers=add('plant.flowers',16,16,r=>{r.poly([[4,5],[10,3],[14,7],[13,13],[7,15],[2,11]],leaf[1]);r.rect(4,7,8,6,leaf[3]);for(const [x,y]of [[3,5],[9,4],[7,9]]){r.rect(x,y,4,3,'#d8785e');r.rect(x,y,3,1,'#f3c879');r.dot(x+1,y+1,'#f8e8a7');}r.line(3,12,5,13,leaf[5]);r.line(10,13,12,11,leaf[5]);},'flowers');
const scene=new Raster(240,160);for(let y=0;y<160;y+=16)for(let x=0;x<240;x+=16)scene.blit(grass,x,y);
scene.rect(89,111,14,49,'#c8ce94');scene.rect(91,112,10,48,'#dedba1');for(let y=117;y<160;y+=9){scene.dot(90,y,'#a9c390');scene.dot(101,y+3,'#eddca2');}
scene.blit(house,72,32);scene.blit(tree,24,77);scene.blit(tree,184,77);scene.blit(flowers,42,124);scene.blit(flowers,168,125);
await scene.save(out+'/house-tree-native.png');await scene.scale(4).save(review+'/house-tree-4x.png');await house.save(out+'/house-native.png');await house.scale(4).save(review+'/house-4x.png');await tree.save(out+'/tree-native.png');await tree.scale(8).save(review+'/tree-8x.png');
const atlas=new Raster(256,128);let x=0,y=0,rh=0;const metadata=[];for(const a of art){if(x+a.r.w>256){x=0;y+=rh;rh=0;}atlas.blit(a.r,x,y);metadata.push({id:a.id,rect:[x,y,a.r.w,a.r.h],paletteFamily:a.palette,status:'awaiting-review'});x+=a.r.w;rh=Math.max(rh,a.r.h);}await atlas.save(out+'/atlas.png');await atlas.scale(4).save(review+'/atlas-4x.png');
await writeFile(out+'/atlas.json',JSON.stringify({schemaVersion:1,status:'awaiting-review',image:'atlas.png',baseTile:8,metatile:16,assets:metadata,houseParts,limitations:['Focused visual proof only; no town regeneration or gameplay integration.','Assembly contains hand-authored trim pixels as well as reusable module references.','No palette/character/movement approval is implied.']},null,2)+'\n');
await writeFile(out+'/geometry-proposals.json',JSON.stringify({status:'proposed-only',tree:{size:[32,32],canopy:'tree.clustered.canopy',trunk:'tree.clustered.trunk',groundFootprint:[8,16,16,16],sortAnchor:[16,32]},house:{size:[96,80],sortAnchor:[48,80],doorThreshold:[16,64,16,16],doorApproach:[16,80,16,16]},collision:[],warps:[],interactions:[]},null,2)+'\n');
console.log(JSON.stringify({revision:2,native:[240,160],enlarged:[960,640],assets:art.length,status:'awaiting-review'}));
