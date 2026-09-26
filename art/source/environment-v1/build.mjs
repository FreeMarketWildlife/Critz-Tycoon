// Original Critz pixel art. Every shape is authored on the native integer grid.
// Run from repo root: node art/source/environment-v1/build.mjs
import { mkdir, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { Raster } from './raster.mjs';
const OUT='assets/review/environment-v1', REVIEW='docs/reviews/M1-E1';
await mkdir(OUT,{recursive:true});await mkdir(REVIEW,{recursive:true});
const palettes={
  landscape:['transparent','#233f39','#38634d','#4f8053','#72a05c','#9abd72','#c4d78a','#655343','#92724e','#b99565','#d9b57b','#efd29a','#245c67','#368793','#65b3b0','#b3d9bf'],
  woodwork:['transparent','#293e40','#57463e','#7e5841','#a6764f','#cca173','#e8c99b','#f7e6be','#497f87','#79afb1','#b8d6c7','#d48b57','#a35f46','#769d62','#acbc7f','#334f54'],
  terracotta:['transparent','#513f45','#804e49','#a85e4d','#c77c59','#e1a16e','#f0be87'],
  plum:['transparent','#3b3d51','#574c64','#75617b','#958091','#b49dad','#d4c1c4'],
  teal:['transparent','#264650','#396775','#558e98','#80b6b6','#b7d8c4','#e4e4bc'],
  interior:['transparent','#293e40','#624b48','#896654','#b08762','#d5b286','#edcfa0','#f7e6be','#3b7479','#5a9b9b','#99c6b6','#527b58','#84a168','#ad695f','#d08f7a','#efbba0']
};
const assets=new Map();
function asset(id,w,h,bank,draw,meta={}){const r=new Raster(w,h);draw(r,palettes[bank]);assets.set(id,{id,r,bank,...meta});return r;}
const get=id=>{if(!assets.has(id))throw Error('Missing '+id);return assets.get(id).r;};
const tile=(id,bank,draw,meta={})=>asset(id,16,16,bank,draw,{kind:'metatile',...meta});
// Ground variants use matching edge pixels; interiors are intentionally quiet.
for(let v=0;v<4;v++)tile('ground.grass.'+v,'landscape',(r,p)=>{r.rect(0,0,16,16,p[4]);for(const [x,y] of [[3+v,3],[10,10-v]]){r.rect(x,y,2,1,p[3]);r.dot(x+1,y-1,p[5]);}});
for(const material of ['path','water','cobble'])for(let mask=0;mask<16;mask++){
  tile(`ground.${material}.${mask}`,'landscape',(r,p)=>{
    r.blit(get('ground.grass.0'),0,0);
    const left=mask&8?0:3,right=mask&2?16:13,top=mask&1?0:3,bottom=mask&4?16:13;
    const base=material==='water'?13:material==='cobble'?9:10;
    r.rect(left,top,right-left,bottom-top,p[base]);
    if(!(mask&1)){r.line(left,top-1,right-1,top-1,p[material==='water'?2:9]);r.line(left,top,right-1,top,p[material==='water'?12:11]);}
    if(!(mask&4)){r.line(left,bottom,right-1,bottom,p[material==='water'?2:9]);r.line(left,bottom-1,right-1,bottom-1,p[material==='water'?14:11]);}
    if(!(mask&8)){r.line(left-1,top,left-1,bottom-1,p[material==='water'?2:9]);r.line(left,top,left,bottom-1,p[material==='water'?12:11]);}
    if(!(mask&2)){r.line(right,top,right,bottom-1,p[material==='water'?2:9]);r.line(right-1,top,right-1,bottom-1,p[material==='water'?14:11]);}
    if(material==='path'){r.rect(6,7,2,1,p[11]);r.dot(10,11,p[9]);}
    if(material==='water'){r.line(6,6,9,6,p[14]);r.dot(5,7,p[14]);r.line(9,12,11,12,p[12]);}
    if(material==='cobble')for(let y=top+1;y<bottom-2;y+=5)for(let x=left+1;x<right-2;x+=6){r.rect(x,y,4,3,p[10]);r.line(x,y+3,x+3,y+3,p[8]);r.dot(x,y,p[11]);}
  });
  // Concave corners are separate appearance overlays, never collision rules.
}
for(const material of ['path','water','cobble'])for(let c=0;c<4;c++)tile(`corner.${material}.${c}`,'landscape',(r,p)=>{const x=c%2?13:0,y=c>1?13:0;r.rect(x,y,3,3,p[4]);r.dot(c%2?12:3,c>1?13:2,p[material==='water'?2:9]);r.dot(c%2?13:2,c>1?12:3,p[material==='water'?2:9]);});
for(let v=0;v<2;v++)tile('floor.wood.'+v,'interior',(r,p)=>{r.rect(0,0,16,16,p[5]);r.line(0,0,15,0,p[4]);r.line(v?8:0,0,v?8:0,15,p[4]);r.line(4,5,9,5,p[5]);r.dot(12,12,p[4]);});
tile('floor.tile','interior',(r,p)=>{r.rect(0,0,16,16,p[7]);r.line(0,0,15,0,p[5]);r.line(0,0,0,15,p[5]);r.rect(2,2,5,5,p[6]);r.rect(10,10,5,5,p[6]);});
// A 3x3 roof grammar: ridge/end, repeating slope, eave/end.
for(const bank of ['terracotta','plum','teal'])for(let row=0;row<3;row++)for(let col=0;col<3;col++)tile(`roof.${bank}.${col}.${row}`,bank,(r,p)=>{
  r.rect(0,0,16,16,p[3]);
  for(let y=0;y<16;y+=4){r.line(0,y,15,y,p[2]);r.line(0,y+1,15,y+1,p[4]);for(let x=(y%8?4:0);x<16;x+=8){r.line(x,y,x,y+3,p[2]);r.dot(x+1,y+2,p[5]);}}
  if(row===0){r.rect(0,0,16,3,p[1]);r.line(0,3,15,3,p[5]);r.line(0,4,15,4,p[4]);}
  if(row===2){r.rect(0,13,16,3,p[1]);r.line(0,12,15,12,p[5]);r.line(0,14,15,14,p[2]);}
  if(col===0){r.rect(0,0,2,16,p[1]);r.line(2,0,2,12,p[5]);}
  if(col===2){r.rect(14,0,2,16,p[1]);r.line(13,0,13,12,p[2]);}
});
for(let col=0;col<3;col++)for(let row=0;row<2;row++)tile(`wall.exterior.${col}.${row}`,'woodwork',(r,p)=>{
  r.rect(0,0,16,16,p[6]);r.rect(0,0,16,2,p[row===0?3:5]);r.line(0,2,15,2,p[row===0?4:7]);
  if(row===1){r.rect(0,12,16,4,p[3]);r.line(0,12,15,12,p[5]);r.line(0,15,15,15,p[2]);r.line(7,13,7,14,p[4]);}
  if(col===0){r.rect(0,0,4,16,p[2]);r.rect(2,0,2,12,p[4]);}
  if(col===2){r.rect(12,0,4,16,p[2]);r.rect(12,0,2,12,p[3]);}
});
asset('fixture.window',16,24,'woodwork',(r,p)=>{r.rect(1,1,14,20,p[2]);r.rect(2,2,12,17,p[5]);r.rect(4,4,8,12,p[8]);r.poly([[4,4],[9,4],[4,10]],p[10]);r.rect(7,3,2,14,p[6]);r.rect(3,9,10,2,p[6]);r.rect(0,18,16,3,p[3]);r.line(0,18,15,18,p[7]);r.rect(3,21,10,2,p[2]);},{kind:'facade-detail'});
asset('fixture.door',16,32,'woodwork',(r,p)=>{r.rect(1,0,14,31,p[2]);r.rect(3,1,10,27,p[4]);r.rect(4,2,8,11,p[8]);r.poly([[4,2],[10,2],[4,8]],p[10]);r.rect(7,2,1,11,p[6]);r.rect(4,7,8,1,p[6]);r.rect(4,16,8,9,p[3]);r.line(4,16,4,24,p[5]);r.rect(11,16,1,2,p[7]);r.rect(0,28,16,4,p[5]);r.line(0,28,15,28,p[7]);r.line(0,31,15,31,p[2]);},{kind:'facade-detail',sortAnchor:[8,32],groundFootprint:[0,16,16,16]});
asset('fixture.chimney',16,24,'woodwork',(r,p)=>{r.rect(4,0,10,22,p[2]);r.rect(5,2,8,18,p[5]);for(let y=5;y<20;y+=5){r.line(5,y,12,y,p[3]);r.dot(y%2?8:10,y+2,p[3]);}r.rect(3,0,12,4,p[6]);r.rect(5,0,8,2,p[2]);r.line(3,4,14,4,p[3]);},{kind:'roof-detail'});
asset('fixture.gable',32,24,'woodwork',(r,p)=>{r.poly([[0,15],[16,0],[32,15],[31,23],[1,23]],p[2]);r.poly([[3,15],[16,3],[29,15],[29,22],[3,22]],p[6]);r.line(16,3,16,21,p[3]);r.line(3,15,29,15,p[3]);r.line(7,15,16,6,p[4]);r.line(25,15,16,6,p[4]);},{kind:'roof-detail'});
asset('fixture.display',32,24,'woodwork',(r,p)=>{r.rect(0,0,32,22,p[2]);r.rect(1,1,30,19,p[6]);r.rect(3,3,26,15,p[8]);r.poly([[3,3],[15,3],[3,15]],p[9]);r.rect(15,2,2,18,p[5]);r.rect(5,12,6,5,p[11]);r.rect(20,10,5,7,p[13]);r.line(3,18,28,18,p[3]);r.rect(0,21,32,3,p[3]);r.line(0,21,31,21,p[5]);},{kind:'facade-detail'});
for(const color of ['cream','teal'])asset('fixture.awning.'+color,32,16,'woodwork',(r,p)=>{r.poly([[3,1],[29,1],[32,10],[32,14],[0,14],[0,10]],p[2]);for(let x=1;x<31;x+=5){r.rect(x,5,5,7,p[x%2?7:color==='teal'?8:11]);r.rect(x,12,4,2,p[x%2?6:color==='teal'?8:12]);}r.line(3,1,28,1,p[3]);r.line(2,3,29,3,p[6]);},{kind:'facade-detail'});
asset('fixture.flowerbox',24,16,'woodwork',(r,p)=>{r.rect(1,8,22,7,p[2]);r.rect(2,9,20,4,p[4]);r.line(2,9,21,9,p[6]);for(let x=3;x<22;x+=5){r.rect(x,4,3,4,p[13]);r.rect(x-1,3,4,2,p[11]);r.dot(x,2,p[7]);}},{kind:'facade-detail'});
for(let type=0;type<5;type++)asset('fixture.sign.'+type,16,16,'woodwork',(r,p)=>{
  r.rect(0,0,16,15,p[2]);r.rect(1,1,14,12,p[7]);r.line(1,13,14,13,p[4]);
  if(type===0){r.oval(5,7,6,4,p[3]);for(const [x,y] of [[3,4],[6,2],[9,2],[12,4]])r.oval(x,y,2,3,p[3]);}
  if(type===1){r.poly([[4,10],[4,6],[11,3],[12,7],[8,11]],p[13]);r.line(5,10,10,5,p[1]);}
  if(type===2){r.rect(6,2,4,2,p[13]);r.rect(5,4,6,8,p[8]);r.rect(6,5,4,5,p[10]);r.dot(6,5,p[7]);}
  if(type===3){r.oval(3,2,10,10,p[1]);r.oval(5,4,6,6,p[7]);r.line(4,7,11,7,p[3]);r.line(8,3,8,11,p[3]);}
  if(type===4){r.poly([[6,2],[10,2],[10,5],[13,10],[11,12],[5,12],[3,10],[6,5]],p[8]);r.line(6,7,9,7,p[10]);r.rect(5,9,6,2,p[11]);}
},{kind:'facade-detail'});
for(const type of ['horizontal','vertical','left','right'])tile('fence.'+type,'woodwork',(r,p)=>{const xs=type==='left'?[3]:type==='right'?[11]:[3,11];if(type!=='vertical'){r.rect(0,5,16,3,p[3]);r.line(0,5,15,5,p[6]);r.rect(0,10,16,2,p[4]);}for(const x of xs){r.rect(x,3,3,12,p[2]);r.rect(x,2,2,12,p[4]);r.dot(x,1,p[6]);r.line(x,3,x,12,p[5]);}});
tile('bridge.planks','woodwork',(r,p)=>{r.rect(0,0,16,16,p[2]);for(let y=0;y<16;y+=4){r.rect(0,y,16,3,p[4]);r.line(0,y,15,y,p[5]);r.dot(2,y+1,p[2]);r.dot(13,y+1,p[2]);}});
// Tree silhouettes are hand-placed leaf clusters; canopy and trunk remain separate.
for(const [name,size] of [['broadleaf',48],['compact',32],['sunleaf',48]]){
  const h=size,offset=h-48;
  asset('tree.'+name+'.trunk',32,h,'landscape',(r,p)=>{const y=h-16;r.oval(7,h-7,20,6,p[2]);r.poly([[14,y-6],[20,y-6],[20,h-7],[24,h-4],[18,h-5],[15,h-3],[14,h-6],[10,h-5],[14,h-9]],p[7]);r.rect(15,y-4,3,13,p[8]);r.line(15,y-2,15,h-8,p[9]);r.line(18,y+2,18,h-7,p[7]);},{kind:'trunk',sortAnchor:[16,h],groundFootprint:[8,h-16,16,16]});
  asset('tree.'+name+'.canopy',32,h,'landscape',(r,p)=>{
    const oy=name==='compact'?-9:0,ys=name==='compact'?.60:1;
    const poly=(pts,c)=>r.poly(pts.map(([x,y])=>[x,Math.round(y*ys+oy+(name==='compact'?9:0))]),c);
    const ramp=name==='sunleaf'?[2,3,4,5]:[1,2,3,4];
    poly([[13,1],[21,2],[24,5],[28,7],[29,13],[32,17],[31,24],[28,27],[29,32],[24,36],[18,37],[14,35],[7,37],[3,32],[4,27],[0,23],[1,17],[4,14],[3,9],[8,6]],p[ramp[0]]);
    for(const [x,y,w,hh] of [[5,6,15,14],[13,6,14,16],[2,16,17,16],[14,17,15,17],[8,23,16,13]]){
      poly([[x+4,y],[x+w-4,y],[x+w,y+4],[x+w-1,y+hh-3],[x+w-6,y+hh],[x+3,y+hh-1],[x,y+hh-5],[x,y+5]],p[ramp[1]]);
      poly([[x+4,y+1],[x+w-5,y+1],[x+w-3,y+4],[x+w-5,y+7],[x+5,y+8],[x+2,y+5]],p[ramp[2]]);
      poly([[x+5,y+2],[x+9,y+2],[x+8,y+4],[x+4,y+4]],p[ramp[3]]);
    }
    for(const [x,y] of [[9,8],[20,10],[6,20],[17,22],[12,29]]){const yy=Math.round(y*ys+oy+(name==='compact'?9:0));r.rect(x,yy,3,1,p[5]);r.dot(x+1,yy-1,p[4]);}
  },{kind:'canopy',sortAnchor:[16,h],foreground:true,groundFootprint:null});
  const r=new Raster(32,h);r.blit(get('tree.'+name+'.trunk'),0,0);r.blit(get('tree.'+name+'.canopy'),0,0);assets.set('tree.'+name,{id:'tree.'+name,r,bank:'landscape',kind:'assembly',parts:[{id:'tree.'+name+'.trunk',x:0,y:0},{id:'tree.'+name+'.canopy',x:0,y:0}],sortAnchor:[16,h],groundFootprint:[8,h-16,16,16]});
}
asset('plant.fern',16,16,'landscape',(r,p)=>{for(const [x,y] of [[2,5],[5,2],[10,3],[14,6],[3,9],[12,10]]){r.line(8,14,x,y,p[2]);r.line(x,y,x+1,y+3,p[5]);r.dot(x-1,y+1,p[3]);}r.rect(7,11,2,4,p[3]);},{kind:'ground-detail'});
asset('plant.flowers',16,16,'landscape',(r,p)=>{for(const [x,y] of [[3,4],[11,8],[6,12]]){r.rect(x,y,1,3,p[2]);r.rect(x-1,y-1,3,2,p[11]);r.dot(x,y-2,p[11]);r.dot(x,y,p[10]);}},{kind:'ground-detail'});
asset('plant.shrub',32,16,'landscape',(r,p)=>{r.oval(0,3,31,12,p[2]);for(const x of [1,10,20]){r.oval(x,1,11,12,p[3]);r.oval(x+1,1,8,6,p[4]);r.rect(x+3,2,3,1,p[5]);}},{kind:'prop',sortAnchor:[16,16],groundFootprint:[0,0,32,16]});
asset('prop.stump',16,16,'landscape',(r,p)=>{r.rect(3,6,10,7,p[7]);r.oval(1,10,14,4,p[7]);r.oval(2,3,12,7,p[9]);r.oval(4,4,8,4,p[10]);r.line(5,5,9,5,p[8]);r.line(3,9,3,12,p[8]);r.dot(7,7,p[8]);},{kind:'prop',sortAnchor:[8,16],groundFootprint:[0,0,16,16]});
asset('prop.log',32,16,'landscape',(r,p)=>{r.rect(4,4,22,10,p[7]);r.rect(4,5,22,5,p[8]);r.line(6,5,26,5,p[9]);r.line(9,10,24,10,p[7]);r.oval(1,3,9,12,p[9]);r.oval(2,5,6,8,p[10]);r.oval(4,7,3,4,p[8]);r.rect(23,4,2,10,p[7]);},{kind:'prop',sortAnchor:[16,16],groundFootprint:[0,0,32,16]});
asset('prop.bench',32,16,'woodwork',(r,p)=>{r.rect(3,9,3,7,p[2]);r.rect(25,9,3,7,p[2]);r.rect(1,0,30,5,p[3]);r.line(1,0,30,0,p[6]);r.rect(1,7,30,6,p[4]);r.line(1,7,30,7,p[6]);r.line(1,10,30,10,p[3]);},{kind:'prop',sortAnchor:[16,16],groundFootprint:[0,0,32,16]});
asset('prop.notice',32,32,'woodwork',(r,p)=>{r.rect(4,4,3,28,p[2]);r.rect(25,4,3,28,p[2]);r.rect(1,3,30,19,p[3]);r.rect(3,5,26,14,p[4]);r.rect(5,7,9,10,p[7]);r.rect(17,7,9,8,p[6]);r.line(7,10,11,10,p[4]);r.line(7,13,10,13,p[4]);r.line(19,10,23,10,p[4]);r.rect(0,1,32,3,p[2]);r.line(1,0,30,0,p[5]);},{kind:'prop',sortAnchor:[16,32],groundFootprint:[0,16,32,16]});
// Interior components at the existing art bible's proposed scale.
for(let col=0;col<3;col++)tile('wall.interior.'+col,'interior',(r,p)=>{r.rect(0,0,16,16,p[6]);r.rect(0,0,16,2,p[2]);r.rect(0,13,16,3,p[3]);r.line(0,12,15,12,p[7]);r.line(5,3,5,10,p[5]);if(col!==1)r.rect(col===0?0:14,0,2,16,p[2]);});
for(let y=0;y<3;y++)for(let x=0;x<3;x++)tile(`rug.${x}.${y}`,'interior',(r,p)=>{r.rect(0,0,16,16,p[8]);if(x!==1){r.rect(x===0?0:13,0,3,16,p[10]);r.line(x===0?4:11,0,x===0?4:11,15,p[9]);}if(y!==1){r.rect(0,y===0?0:13,16,3,p[10]);r.line(0,y===0?4:11,15,y===0?4:11,p[9]);}if(x===1&&y===1){r.poly([[8,3],[13,8],[8,13],[3,8]],p[9]);r.dot(8,8,p[10]);}});
asset('inside.bed',32,32,'interior',(r,p)=>{r.rect(2,0,28,31,p[2]);r.rect(3,1,26,29,p[4]);r.line(4,1,27,1,p[6]);r.rect(5,4,22,22,p[7]);r.rect(7,5,18,7,p[6]);r.rect(8,5,16,5,p[7]);r.rect(5,13,22,15,p[8]);r.rect(5,13,22,3,p[10]);r.line(6,17,6,25,p[9]);r.rect(20,16,4,11,p[9]);r.rect(3,28,26,3,p[3]);r.line(4,28,27,28,p[5]);},{kind:'furniture',sortAnchor:[16,32],groundFootprint:[0,0,32,32]});
asset('inside.desk',32,32,'interior',(r,p)=>{r.rect(2,16,3,16,p[2]);r.rect(26,16,3,16,p[2]);r.rect(0,3,32,19,p[2]);r.rect(1,4,30,12,p[5]);r.line(1,4,30,4,p[7]);r.rect(1,17,30,4,p[3]);r.rect(20,17,9,3,p[4]);r.dot(24,18,p[7]);r.rect(5,7,11,6,p[7]);r.line(7,9,12,9,p[4]);r.rect(23,6,4,6,p[8]);r.dot(24,5,p[10]);},{kind:'furniture',sortAnchor:[16,32],groundFootprint:[0,16,32,16]});
asset('inside.shelf',32,32,'interior',(r,p)=>{r.rect(0,0,32,32,p[2]);r.rect(2,2,28,27,p[3]);for(let y=3;y<28;y+=12){for(let i=0;i<7;i++){r.rect(3+i*4,y,3,8,p[[8,13,5,9,6,14,11][i]]);r.dot(4+i*4,y+2,p[7]);}r.rect(1,y+9,30,3,p[5]);r.line(1,y+9,30,y+9,p[6]);}r.rect(1,0,30,2,p[5]);},{kind:'furniture',sortAnchor:[16,32],groundFootprint:[0,16,32,16]});
asset('inside.tank25',32,32,'interior',(r,p)=>{r.rect(0,0,32,21,p[1]);r.rect(2,2,28,17,p[8]);r.rect(3,3,26,9,p[9]);r.rect(3,13,26,5,p[3]);r.line(3,12,28,12,p[5]);r.poly([[3,11],[11,8],[15,11],[22,9],[29,12],[29,16],[3,16]],p[11]);r.line(8,12,8,6,p[12]);r.line(8,9,5,7,p[12]);r.line(22,13,22,5,p[12]);r.line(22,9,25,7,p[12]);r.line(4,3,4,10,p[10]);r.line(5,3,12,3,p[10]);r.rect(0,0,32,2,p[1]);for(let x=3;x<30;x+=3)r.dot(x,0,p[6]);r.rect(0,20,32,12,p[2]);r.rect(2,22,13,8,p[4]);r.rect(17,22,13,8,p[4]);r.dot(12,25,p[6]);r.dot(19,25,p[6]);},{kind:'furniture',sortAnchor:[16,32],groundFootprint:[0,16,32,16],label:'25-gallon ventilated starter tank; volume specified in UI'});
asset('inside.chair',16,24,'interior',(r,p)=>{r.rect(2,0,12,12,p[2]);r.rect(3,1,10,9,p[4]);r.line(3,1,12,1,p[6]);r.rect(1,12,14,7,p[2]);r.rect(2,12,12,5,p[5]);r.line(2,12,13,12,p[6]);r.rect(2,19,2,5,p[2]);r.rect(12,19,2,5,p[2]);},{kind:'furniture',sortAnchor:[8,24],groundFootprint:[0,8,16,16]});
asset('inside.plant',16,24,'interior',(r,p)=>{r.poly([[3,14],[13,14],[11,23],[5,23]],p[2]);r.rect(4,14,8,2,p[15]);r.poly([[4,16],[12,16],[10,22],[6,22]],p[13]);r.line(8,15,8,3,p[11]);for(const [x,y] of [[2,3],[9,1],[1,9],[10,7]]){r.oval(x,y,6,5,p[11]);r.line(x+1,y+1,x+4,y+1,p[12]);}},{kind:'furniture',sortAnchor:[8,24],groundFootprint:[0,8,16,16]});
asset('inside.stairs',32,32,'interior',(r,p)=>{r.rect(0,0,32,32,p[2]);for(let y=4;y<32;y+=5){r.rect(3,y,26,3,p[5]);r.line(3,y,28,y,p[7]);}r.rect(0,0,2,32,p[3]);r.rect(30,0,2,32,p[3]);},{kind:'furniture',sortAnchor:[16,32],groundFootprint:[0,0,32,32]});
// Building assemblies really reuse the exported modules, including wider shops.
const buildings=[];
for(const [name,roof,sign] of [['home','terracotta',null],['kaid-home','terracotta',null],['rival-home','terracotta',null],['critz','teal',0],['vet','teal',1],['drug-store','teal',2],['bike-shop','terracotta',3],['glow-n-blow','teal',4],['liarsville-cottage','plum',null]]){
  const parts=[];const r=new Raster(96,80);const put=(id,x,y)=>{r.blit(get(id),x,y);parts.push({id,x,y});};
  for(let y=0;y<3;y++)for(let x=0;x<6;x++)put(`roof.${roof}.${x===0?0:x===5?2:1}.${y}`,x*16,y*16);
  for(let y=0;y<2;y++)for(let x=0;x<6;x++)put(`wall.exterior.${x===0?0:x===5?2:1}.${y}`,x*16,48+y*16);
  if(sign!==null){put('fixture.display',5,52);put('fixture.display',59,52);put('fixture.awning.'+(name==='critz'||name==='bike-shop'?'cream':'teal'),5,42);put('fixture.awning.'+(name==='critz'||name==='bike-shop'?'cream':'teal'),59,42);}else{put('fixture.window',14,51);put('fixture.window',66,51);}
  put('fixture.door',40,48);
  if(sign!==null)put('fixture.sign.'+sign,40,29);else put('fixture.gable',32,31);
  if(name==='kaid-home')put('fixture.flowerbox',10,63);
  if(name==='rival-home')put('fixture.chimney',70,1);
  if(name==='home'||name==='liarsville-cottage')put('fixture.chimney',9,1);
  const id='building.'+name;assets.set(id,{id,r,bank:null,kind:'assembly',parts,sortAnchor:[48,80],groundFootprint:[0,48,96,32]});buildings.push(id);
}
// Atlas: stable IDs in JSON; no map persists atlas indices.
let ax=0,ay=0,rowh=0;const width=512;const metadata=[];
for(const a of assets.values()){if(ax+a.r.w>width){ax=0;ay+=rowh;rowh=0;}a.rect=[ax,ay,a.r.w,a.r.h];ax+=a.r.w;rowh=Math.max(rowh,a.r.h);}
const atlas=new Raster(width,Math.ceil((ay+rowh)/16)*16);
for(const a of assets.values()){
  atlas.blit(a.r,a.rect[0],a.rect[1]);const {r,...m}=a;metadata.push({...m,paletteId:a.bank?'env.'+a.bank:null,origin:[0,0],approval:'rejected-review-history',sha256:createHash('sha256').update(r.p).digest('hex')});
  if(a.bank){const allowed=new Set(palettes[a.bank].slice(1).map(c=>c.toLowerCase()));for(let i=0;i<r.p.length;i+=4){if(r.p[i+3]!==0&&r.p[i+3]!==255)throw Error('Non-binary alpha');if(r.p[i+3]===255&&!allowed.has('#'+r.p.subarray(i,i+3).toString('hex')))throw Error('Unexpected palette '+a.id);}}
}
await atlas.save(OUT+'/atlas.png');await atlas.scale(4).save(REVIEW+'/atlas-4x.png');
for(const id of buildings)await get(id).save(OUT+'/'+id+'.png');
for(const id of ['tree.broadleaf','tree.compact','tree.sunleaf','inside.tank25'])await get(id).save(OUT+'/'+id+'.png');
await writeFile(OUT+'/palette.json',JSON.stringify({schemaVersion:1,status:'proposed',palettes:Object.fromEntries(Object.entries(palettes).map(([k,v])=>['env.'+k,v]))},null,2)+'\n');
await writeFile(OUT+'/atlas.json',JSON.stringify({schemaVersion:1,assetId:'tiles.environment.review.v1',status:'rejected-review-history',nativeTileSize:8,metatileSize:16,image:'atlas.png',width:atlas.w,height:atlas.h,assets:metadata},null,2)+'\n');
// Editable 8x8 vocabulary and assembly references, deduplicated per palette bank.
const baseTiles=[],baseLookup=new Map(),baseAssemblies=[];
for(const a of assets.values())if(a.bank){const refs=[];for(let y=0;y<a.r.h;y+=8)for(let x=0;x<a.r.w;x+=8){const pixels=a.r.crop(x,y,8,8),key=a.bank+createHash('sha256').update(pixels.p).digest('hex');if(!baseLookup.has(key)){baseLookup.set(key,baseTiles.length);baseTiles.push({r:pixels,bank:a.bank});}refs.push({tile:baseLookup.get(key),x,y});}baseAssemblies.push({id:a.id,width:a.r.w,height:a.r.h,tiles:refs});}
const baseSheet=new Raster(128,Math.ceil(baseTiles.length/16)*8);for(let i=0;i<baseTiles.length;i++)baseSheet.blit(baseTiles[i].r,(i%16)*8,Math.floor(i/16)*8);await baseSheet.save(OUT+'/base-tiles.png');
await writeFile(OUT+'/base-tiles.json',JSON.stringify({schemaVersion:1,image:'base-tiles.png',tileSize:8,columns:16,tiles:baseTiles.map((t,i)=>({id:i,paletteId:'env.'+t.bank})),assemblies:baseAssemblies},null,2)+'\n');
// Map previews: appearance and future gameplay geometry are separate documents.
const maps=[];
function map(id,w,h){const terrain=Array.from({length:h},()=>Array(w).fill('grass')),detail=[],objects=[],pois=[];return {id,w,h,terrain,detail,objects,pois};}
function area(m,x,y,w,h,t){for(let j=y;j<y+h;j++)for(let i=x;i<x+w;i++)if(m.terrain[j]?.[i]!==undefined)m.terrain[j][i]=t;}
function object(m,id,x,y,label){m.objects.push({id,x,y});if(label)m.pois.push({label,x,y});}
function tree(m,x,y,type='broadleaf'){object(m,'tree.'+type,x*16,y*16);}
function border(m){for(let x=0;x<m.w;x+=2){tree(m,x,0);tree(m,x,m.h-3);}for(let y=3;y<m.h-4;y+=3){tree(m,0,y);tree(m,m.w-2,y);}}
const root=map('rootport',40,36);border(root);
area(root,3,9,34,3,'path');area(root,3,20,34,3,'path');area(root,3,30,34,3,'path');area(root,14,9,3,24,'path');area(root,26,9,3,24,'path');area(root,36,20,4,3,'path');
for(const [id,x,y,label] of [['home',5,3,'Hero + Mom'],['kaid-home',17,3,'Kaid'],['rival-home',29,3,'Rival + family'],['critz',5,14,'Critz'],['vet',17,14,'Vet / Nugget'],['drug-store',29,14,'Drug Store'],['bike-shop',5,25,'Bike Shop'],['glow-n-blow',29,25,'Glow n’ Blow']]){object(root,'building.'+id,x*16,y*16,label);area(root,x+2,y+5,2,2,'path');}
for(const [x,y] of [[12,3],[24,3],[3,12],[13,12],[25,12],[36,12],[3,23],[35,25],[17,25],[23,25]])tree(root,x,y);
for(let x=13;x<18;x++)root.detail.push({id:'plant.flowers',x:x*16,y:12*16});
object(root,'prop.bench',23*16,12*16);object(root,'prop.notice',23*16,22*16);maps.push(root);
const route=map('forest-route',40,24);border(route);
// Land bridges are explicit pieces laid over the stream appearance.
area(route,18,0,3,24,'water');area(route,0,16,11,3,'path');area(route,8,11,3,7,'path');area(route,8,11,18,3,'path');area(route,23,6,3,7,'path');area(route,23,6,17,3,'path');area(route,18,0,3,24,'water');
for(let y=11;y<14;y++)for(let x=17;x<22;x++)route.detail.push({id:'bridge.planks',x:x*16,y:y*16});
area(route,9,5,6,4,'path');area(route,11,7,2,5,'path');object(route,'prop.bench',10*16,6*16);object(route,'prop.notice',13*16,6*16);
for(const [x,y] of [[3,3],[5,6],[12,1],[14,14],[4,19],[12,17],[15,18],[23,1],[28,1],[32,2],[25,13],[30,11],[34,13],[23,18],[30,18],[35,19],[4,10]])tree(route,x,y);
for(const [x,y] of [[6,12],[13,9],[16,7],[24,16],[29,15],[33,10],[22,4]])object(route,'plant.fern',x*16,y*16);
object(route,'prop.log',13*16,16*16);object(route,'prop.stump',30*16,15*16);route.pois.push({label:'Rootport ←',x:0,y:17*16},{label:'→ Liarsville',x:35*16,y:7*16},{label:'Observation hollow',x:10*16,y:8*16});maps.push(route);
const liars=map('liarsville',32,28);border(liars);
area(liars,0,14,30,3,'path');area(liars,14,7,3,18,'cobble');area(liars,10,11,12,9,'cobble');area(liars,20,20,7,4,'water');
for(const [x,y] of [[4,4],[21,4],[5,20]]){object(liars,'building.liarsville-cottage',x*16,y*16,'Cottage');area(liars,x+2,y+5,2,y<10?6:2,'path');}
area(liars,7,25,9,2,'path');
object(liars,'prop.notice',15*16,11*16,'Notice pavilion study');object(liars,'prop.bench',18*16,18*16);object(liars,'prop.bench',11*16,18*16);
for(const [x,y] of [[11,3],[17,3],[2,10],[27,10],[2,19],[13,21],[27,21],[19,23]])tree(liars,x,y,'sunleaf');
for(const [x,y] of [[10,9],[20,9],[5,12],[25,12],[18,23]])object(liars,'plant.flowers',x*16,y*16);maps.push(liars);
const room=map('bedroom',15,10);area(room,0,0,15,10,'floor');
for(let x=0;x<15;x++)room.detail.push({id:'wall.interior.'+(x===0?0:x===14?2:1),x:x*16,y:0});
for(let y=0;y<3;y++)for(let x=0;x<3;x++)room.detail.push({id:`rug.${x}.${y}`,x:(6+x)*16,y:(4+y)*16});
for(const [id,x,y] of [['inside.bed',1,2],['inside.desk',5,1],['inside.chair',5,3],['inside.shelf',10,1],['inside.tank25',10,5],['inside.plant',8,1],['inside.stairs',1,7]])object(room,id,x*16,y*16);
room.detail.push({id:'fixture.window',x:3*16,y:0});
room.pois.push({label:'25-gallon gift',x:10*16,y:5*16});maps.push(room);
function render(m){const r=new Raster(m.w*16,m.h*16),placements=[];const put=(id,x,y)=>{r.blit(get(id),x,y);placements.push({id,x,y});};
  for(let y=0;y<m.h;y++)for(let x=0;x<m.w;x++){
    const t=m.terrain[y][x];if(t==='grass'){put('ground.grass.'+((x*7+y*3)%4),x*16,y*16);continue;}if(t==='floor'){put('floor.wood.'+(y%2),x*16,y*16);continue;}
    let mask=0;for(const [dx,dy,bit]of [[0,-1,1],[1,0,2],[0,1,4],[-1,0,8]])if(m.terrain[y+dy]?.[x+dx]===t)mask|=bit;
    put(`ground.${t}.${mask}`,x*16,y*16);
    for(const [dx,dy,b1,b2,c]of [[-1,-1,8,1,0],[1,-1,2,1,1],[-1,1,8,4,2],[1,1,2,4,3]])if((mask&b1)&&(mask&b2)&&m.terrain[y+dy]?.[x+dx]!==t)put(`corner.${t}.${c}`,x*16,y*16);
  }
  for(const p of m.detail)put(p.id,p.x,p.y);
  for(const p of [...m.objects].sort((a,b)=>(a.y+get(a.id).h)-(b.y+get(b.id).h)))put(p.id,p.x,p.y);
  return {r,placements};
}
const proofs=[];
for(const m of maps){
  // Leave explicit map connections, water and door approaches open at borders.
  m.objects=m.objects.filter(o=>{if(!o.id.startsWith('tree.'))return true;const x=o.x/16,y=o.y/16;if(x!==0&&x!==m.w-2&&y!==0&&y!==m.h-3)return true;for(let j=y;j<y+3;j++)for(let i=x;i<x+2;i++)if(m.terrain[j]?.[i]&&m.terrain[j][i]!=='grass')return false;return true;});
  const {r,placements}=render(m);await r.save(OUT+'/'+m.id+'.png');await r.scale(m.id==='bedroom'?4:2).save(REVIEW+'/'+m.id+(m.id==='bedroom'?'-4x':'-2x')+'.png');
  const camera=m.id==='rootport'?[208,32]:m.id==='forest-route'?[160,112]:m.id==='liarsville'?[240,64]:[0,0];
  const viewport=r.crop(...camera,240,160);await viewport.save(OUT+'/'+m.id+'-viewport.png');await viewport.scale(4).save(REVIEW+'/'+m.id+'-viewport-4x.png');
  const visual={schemaVersion:1,id:'review.'+m.id,status:'rejected-review-history',tileSize:16,width:m.w,height:m.h,camera:{x:camera[0],y:camera[1],width:240,height:160},placements,objects:m.objects,pointsOfInterest:m.pois};
  await writeFile(OUT+'/'+m.id+'.json',JSON.stringify(visual,null,2)+'\n');
  proofs.push({id:m.id,width:r.w,height:r.h,placements:placements.length,viewport:[240,160],nativeRgbaSha256:createHash('sha256').update(r.p).digest('hex')});
}
// Separate proposal data: never consumed by production collision, saves or warps.
await writeFile(OUT+'/geometry-proposals.json',JSON.stringify({schemaVersion:1,status:'proposed-not-playable',units:'native-pixels',rules:[{id:'tree.broadleaf',groundFootprint:[8,32,16,16],canopy:'tree.broadleaf.canopy',note:'Trunk occupancy only; canopy cover requires depth validation with approved actor.'},{id:'building.home',groundFootprint:[0,48,96,32],threshold:[40,64,16,16],approach:[40,80,16,16],note:'Illustrative contact footprint, not complete inaccessible roof/rear building volume. Future collision map must explicitly block full building and leave reachable threshold.'}],warps:[],interactions:[],spawns:[]},null,2)+'\n');
// Three rows need 272 native pixels; keep a dedicated architectural comparison.
const houses=new Raster(320,280);houses.rect(0,0,320,280,'#e8c99b');for(let i=0;i<9;i++)houses.blit(get(buildings[i]),8+(i%3)*104,8+Math.floor(i/3)*92);
await houses.save(OUT+'/buildings.png');await houses.scale(4).save(REVIEW+'/buildings-4x.png');
const scenery=new Raster(240,80);scenery.rect(0,0,240,80,'#72a05c');for(const [id,x,y]of [['tree.broadleaf',8,16],['tree.compact',48,32],['tree.sunleaf',88,16],['plant.shrub',128,48],['prop.log',168,48],['plant.fern',208,48],['prop.stump',208,24]])scenery.blit(get(id),x,y);await scenery.save(OUT+'/scenery.png');await scenery.scale(4).save(REVIEW+'/scenery-4x.png');
await writeFile(REVIEW+'/asset-build-report.json',JSON.stringify({status:'rejected-review-history',source:'art/source/environment-v1/build.mjs',assetCount:assets.size,baseTileCount:baseTiles.length,atlas:[atlas.w,atlas.h],palettes:Object.fromEntries(Object.entries(palettes).map(([k,v])=>[k,{entries:v.length,opaque:v.length-1}])),verified:['integer authored pixels','binary alpha','per-asset declared bank membership','all assembly references resolved','map previews use exported asset pixels','exact integer enlargement by pixel replication'],maps:proofs},null,2)+'\n');
console.log(JSON.stringify({assets:assets.size,atlas:[atlas.w,atlas.h],maps:proofs.map(m=>m.id)}));
