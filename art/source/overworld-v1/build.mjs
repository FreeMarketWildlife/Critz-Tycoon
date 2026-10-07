// Original, editable native-pixel environment kit. No reference-game raster input.
// Run from repository root. All large assemblies are made from reusable map tiles.
import { Raster } from '../raster.mjs';
import { mkdir, writeFile, readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
const OUT='assets/review/overworld-v1';
await mkdir(OUT,{recursive:true});
export const P={
  grass:['#487b59','#6aab64','#8bc77a','#9fd285','#b4df91'],
  leaf:['#254e47','#326d50','#4a9155','#6fb15d','#94cc68','#b5de7b','#d2e99b'],
  earth:['#665341','#88704e','#ad8d5d','#ccb17b','#e1ca94','#efdcad'],
  stone:['#535e65','#77827e','#9ba393','#bdc2a8','#dcddbf','#eeebd0'],
  plaster:['#878a82','#b6b7a4','#d8d4b8','#eae2c4','#f8edce'],
  wood:['#514d42','#776144','#9e7e50','#c49b62','#e2bb7d'],
  clay:['#663f45','#8c4f49','#b96651','#d8825d','#efa174','#ffc18a'],
  teal:['#344d60','#416a79','#508992','#68a4a6','#89c0b8','#b4d7c7'],
  water:['#2c6d87','#388ba2','#49a5b4','#70c0c5','#a1d9d4','#d0eee0'],
  glass:['#375669','#51849a','#80b8c4','#c3e0d6'],
  flower:['#a45463','#d47c86','#f0aba0','#f6d9b5','#d5a857'],
};
const C=Object.values(P).flat();
const hash=(x,y,s=0)=>{let a=(Math.imul(x+781,374761393)^Math.imul(y+391,668265263)^Math.imul(s+71,1274126177))>>>0;a=Math.imul(a^(a>>>13),1274126177)>>>0;return (a^(a>>>16))>>>0;};
const mod=(x,n)=>((x%n)+n)%n;
const blank=()=>new Raster(32,32);
const tiles=[],byId={},sections=[];let cursor=0;
const group=(name)=>{cursor=Math.ceil(cursor/32)*32;sections.push({name,start:cursor});};
function add(id,r,properties={}){if(byId[id])throw Error('Duplicate '+id);if(r.w!==32||r.h!==32)throw Error(id+' dimensions');const tile={id,index:cursor++,x:0,y:0,width:32,height:32,layer:'ground',...properties};tile.x=tile.index%32*32;tile.y=Math.floor(tile.index/32)*32;tiles.push({...tile,r});byId[id]=tile;return id;}
function slice(id,r,properties={}){const rows=[];for(let y=0;y<r.h;y+=32){const row=[];for(let x=0;x<r.w;x+=32)row.push(add(`${id}.${x/32}.${y/32}`,r.crop(x,y,32,32),properties));rows.push(row);}return rows;}
function ink(r,pattern,x,y,colors){pattern.forEach((row,j)=>[...row].forEach((v,i)=>{if(v!=='.')r.dot(x+i,y+j,colors[+v]);}));}
function blade(r,x,y,c=P.grass[1],h=4){r.line(x,y,x-2,y-h,c);r.line(x,y,x+2,y-h+1,c);}
function grass(variant=0){const r=blank();r.rect(0,0,32,32,P.grass[2]);const spots=[[5,8],[21,23],[26,6],[10,27]];for(const [a,b]of spots){const x=mod(a+variant*5,26)+3,y=mod(b+variant*3,24)+4;ink(r,['.0..','1.1.','..1.'],x-2,y-2,[P.grass[1],P.grass[3]]);}return r;}
function sand(){const r=blank();r.rect(0,0,32,32,P.earth[4]);for(const [x,y]of [[5,7],[24,17],[12,26]]){r.rect(x,y,3,1,P.earth[3]);r.dot(x+3,y-1,P.earth[5]);}return r;}
function paving(){const r=blank();r.rect(0,0,32,32,P.stone[2]);for(let y=0;y<32;y+=8)for(let x=-8;x<32;x+=16){const a=x+(y%16?8:0);r.rect(a+1,y+1,14,6,P.stone[3]);r.line(a+2,y+1,a+13,y+1,P.stone[4]);r.line(a+14,y+2,a+14,y+6,P.stone[1]);}return r;}
function soil(){const r=blank();r.rect(0,0,32,32,P.earth[1]);for(let y=3;y<32;y+=8){r.rect(0,y,32,2,P.earth[0]);r.rect(0,y+2,32,2,P.earth[2]);}return r;}
function water(phase=0){const r=blank();r.rect(0,0,32,32,P.water[2]);for(const [x,y,w]of [[3,7,7],[20,22,6]]){const yy=mod(y+phase*2,32);r.line(x,yy,x+w,yy,P.water[3]);r.rect(x-2,mod(yy+1,32),3,1,P.water[3]);r.rect(x+w,mod(yy-1,32),3,1,P.water[3]);r.rect(x+1,mod(yy+3,32),w-2,1,P.water[1]);}return r;}
const base={grass:grass(),path:sand(),paving:paving(),soil:soil(),water:water()};
// Clockwise neighbors: N=1, E=2, S=4, W=8, NE=16, SE=32, SW=64, NW=128.
export function normalize(m){for(const [b,a,c]of [[16,1,2],[32,2,4],[64,4,8],[128,8,1]])if(!(m&a)||!(m&c))m&=~b;return m;}
const masks=[...new Set(Array.from({length:256},(_,i)=>normalize(i)))].sort((a,b)=>a-b);
function inside(x,y,m){const east=x>=16,south=y>=16,dx=east?31-x:x,dy=south?31-y:y;
  const vx=!!(m&(east?2:8)),vy=!!(m&(south?4:1)),diag=!!(m&(south?(east?32:64):(east?16:128)));
  if(!vx&&!vy)return dx>=6&&dy>=6&&((dx-11)**2+(dy-11)**2<=36||dx>=11||dy>=11);
  if(!vx)return dx>=6;if(!vy)return dy>=6;
  if(!diag&&dx<6&&dy<6)return dx*dx+dy*dy>=36;
  return true;
}
function connectedTile(kind,m){const r=grass(),src=base[kind];for(let y=0;y<32;y++)for(let x=0;x<32;x++)if(inside(x,y,m)){
  const at=(y*32+x)*4;r.p.set(src.p.subarray(at,at+4),at);
  const inward=(dx,dy)=>inside(Math.max(0,Math.min(31,x+dx)),Math.max(0,Math.min(31,y+dy)),m);
  const edge=!inward(-1,0)||!inward(1,0)||!inward(0,-1)||!inward(0,1);
  const near=!inward(-2,0)||!inward(2,0)||!inward(0,-2)||!inward(0,2);
  if(kind==='water'){
    const bank=!inward(-3,0)||!inward(3,0)||!inward(0,-3)||!inward(0,3);
    if(edge)r.dot(x,y,P.grass[0]);else if(near)r.dot(x,y,P.earth[2]);else if(bank)r.dot(x,y,P.water[0]);
    else if(!inward(0,-5)||!inward(-5,0))r.dot(x,y,P.water[3]);
  }else if(kind==='path'){if(edge)r.dot(x,y,P.grass[1]);else if(near)r.dot(x,y,P.earth[3]);}
  else if(kind==='soil'){if(edge)r.dot(x,y,P.earth[0]);else if(near)r.dot(x,y,P.earth[2]);}
  else if(kind==='paving'&&edge)r.dot(x,y,P.stone[1]);
}return r;}
group('Ground · quiet grass, sand and paving');
for(let v=0;v<8;v++)add(`ground.grass.${v}`,grass(v));
for(const id of ['path','paving','soil','water'])add(`ground.${id}`,base[id]);
for(const kind of ['path','water','paving','soil']){group(`${kind} · all 47 connected shapes`);for(const m of masks)add(`${kind}.${m}`,connectedTile(kind,m),{terrain:kind,neighborMask:m,blocked:kind==='water'});}

// Roofs share edge coordinates; inserting center columns extends the whole roof.
function roof(color,part,row){const p=P[color],r=blank();const left=part==='left',right=part==='right';
  for(let y=0;y<32;y++)for(let x=0;x<32;x++){
    const gy=row*32+y,inset=gy<16?16-gy:0;
    if((left&&x<inset)||(right&&x>31-inset))continue;
    let c=p[3];if(row===0&&y<7)c=p[y<2?1:y<4?5:3];
    else{const sy=mod(gy-7,14),sx=mod(x+(Math.floor((gy-7)/14)%2)*4,8);
      c=p[sx<2?4:sx<6?3:2];
      if(sy===12)c=p[sx<2?3:2];if(sy===13)c=p[sx>1&&sx<6?1:2];
      if(sy===0&&sx>1&&sx<6)c=p[4];
      if(sy===2&&sx===2&&mod(Math.floor(x/8)+row,3)===0)c=p[5];
      // Narrow hipped side planes; diagonal joints turn at the plane boundary.
      if(left&&x<Math.max(5,22-Math.floor(gy/10))){c=p[mod(x+gy,14)<2?1:mod(x+gy,14)<4?3:2];}
      if(right&&x>Math.min(26,9+Math.floor(gy/10))){c=p[mod(31-x+gy,14)<2?0:mod(31-x+gy,14)<4?3:1];}
    }
    if((left&&x<inset+2)||(right&&x>29-inset))c=p[right?0:4];
    if(row===2&&y>=24)c=p[y===24?4:y<27?2:y<29?1:0];
    r.dot(x,y,c);
  }return r;
}
group('Architecture · terracotta and teal modular roofs');
for(const color of ['clay','teal'])for(let row=0;row<3;row++)for(const part of ['left','center','right'])add(`roof.${color}.${row}.${part}`,roof(color,part,row),{layer:'foreground',material:color});
function wall(style,row,part='center'){const r=blank(),p=P.plaster;r.rect(0,0,32,32,p[3]);
  if(style==='timber'){r.rect(0,0,3,32,P.wood[2]);r.rect(3,0,1,32,P.wood[3]);if(row===0)r.rect(0,0,32,4,P.wood[1]);}
  if(style==='stone'){r.rect(0,0,32,32,P.stone[3]);for(let y=0;y<32;y+=12){r.rect(0,y,32,1,P.stone[2]);r.rect((y%24?8:24),y,1,12,P.stone[2]);}}
  if(row===0){r.rect(0,0,32,5,p[0]);r.rect(0,5,32,3,p[1]);r.rect(0,8,32,1,p[2]);}
  if(part==='left'){r.rect(0,0,5,32,p[0]);r.rect(5,0,2,32,p[2]);}
  if(part==='right'){r.rect(27,0,5,32,p[0]);r.rect(25,0,2,32,p[1]);}
  if(row===1){r.rect(0,23,32,9,P.stone[1]);r.rect(0,23,32,2,P.stone[4]);r.rect(0,26,32,5,P.stone[2]);r.rect(15,26,1,5,P.stone[1]);}
  return r;
}
function window(r,x=4,y=6,w=24,h=23){r.rect(x,y,w,h,P.wood[1]);r.rect(x+1,y+1,w-2,h-2,P.plaster[4]);r.rect(x+3,y+3,w-6,h-5,P.glass[0]);r.rect(x+4,y+4,w-8,h-7,P.glass[1]);r.poly([[x+4,y+4],[x+w-5,y+4],[x+4,y+h-5]],P.glass[2]);r.line(x+5,y+4,x+w-6,y+4,P.glass[3]);r.rect(x+w/2-1,y+2,2,h-3,P.plaster[4]);r.rect(x+2,y+Math.floor(h*.57),w-4,2,P.plaster[4]);r.rect(x-1,y+h,w+2,2,P.stone[1]);r.rect(x-1,y+h-1,w+2,1,P.plaster[4]);}
group('Architecture · plaster, timber, stone and window walls');
for(const style of ['plaster','timber','stone'])for(let row=0;row<2;row++)for(const part of ['left','center','right'])add(`wall.${style}.${row}.${part}`,wall(style,row,part),{layer:'object',blocked:true});
for(const style of ['plaster','timber','stone']){const r=wall(style,0);window(r,4,9,24,20);add(`wall.${style}.window`,r,{layer:'object',blocked:true});const b=wall(style,1);window(b,4,0,24,20);add(`wall.${style}.display`,b,{layer:'object',blocked:true});}
for(const style of ['plaster','timber','stone']){const r=new Raster(32,64);r.blit(wall(style,0),0,0);r.blit(wall(style,1),0,32);window(r,3,13,26,29);r.rect(2,45,28,5,P.wood[1]);r.rect(3,45,26,2,P.wood[3]);for(const x of [6,15,25]){r.rect(x-2,43,5,3,P.leaf[2]);r.dot(x-1,42,P.flower[1]);r.dot(x,42,P.flower[3]);}slice(`windowbox.${style}`,r,{layer:'object',blocked:true});}
function door(color,open=false){const r=new Raster(32,64);r.blit(wall('plaster',0),0,0);r.blit(wall('plaster',1),0,32);r.rect(4,9,24,51,P.wood[0]);r.rect(5,10,22,48,P.plaster[1]);r.rect(7,12,18,46,open?P.wood[0]:P[color][1]);if(!open){r.rect(9,14,14,42,P[color][2]);r.rect(10,15,12,20,P.glass[0]);r.rect(11,16,10,18,P.glass[1]);r.poly([[11,16],[20,16],[11,28]],P.glass[2]);r.rect(10,23,12,2,P[color][4]);r.rect(15,16,2,18,P[color][4]);r.rect(10,38,12,15,P[color][1]);r.rect(11,39,10,12,P[color][3]);r.dot(21,36,P.earth[5]);}r.rect(2,59,28,2,P.stone[4]);r.rect(2,61,28,3,P.stone[1]);return r;}
group('Architecture · door states, awnings and details');
const assemblies={};
for(const color of ['wood','teal'])for(const state of ['closed','open'])assemblies[`door.${color}.${state}`]=slice(`door.${color}.${state}`,door(color,state==='open'),{layer:'object',doorState:state});
for(const part of ['left','center','right']){const r=blank();r.rect(0,4,32,18,P.clay[1]);for(let x=0;x<32;x+=8){r.rect(x,5,8,14,(x/8)%2?P.plaster[4]:P.clay[4]);r.rect(x,19,8,5,(x/8)%2?P.plaster[2]:P.clay[2]);r.rect(x+1,24,6,2,(x/8)%2?P.plaster[1]:P.clay[1]);}if(part!=='center')r.rect(part==='left'?0:30,4,2,19,P.clay[0]);add(`awning.${part}`,r,{layer:'foreground'});}
const chimney=new Raster(32,64);chimney.rect(9,10,16,46,P.stone[1]);chimney.rect(9,12,12,42,P.plaster[2]);for(let y=19;y<50;y+=9){chimney.rect(9,y,12,1,P.stone[2]);chimney.rect(y%18?14:19,y,1,8,P.stone[2]);}chimney.rect(6,6,22,7,P.stone[4]);chimney.rect(8,7,18,4,P.stone[0]);chimney.rect(6,12,22,3,P.stone[2]);assemblies.chimney=slice('chimney',chimney,{layer:'foreground'});

// Rocky embankments: upper turf lip, repeatable strata, foot, returns and stair run.
group('Cliffs · turf cap, face, foot, corners and stairs');
function cliff(part,row){const r=blank();r.rect(0,0,32,32,P.earth[1]);for(let y=0;y<32;y++){const gy=y+row*32;for(let x=0;x<32;x++){const seam=mod(gy+((Math.floor(x/11)%2)*2),15);let c=P.earth[seam<2?0:seam<5?3:2];if(mod(x+(Math.floor(gy/15)%2)*7,17)<2)c=P.earth[1];r.dot(x,y,c);}}
  if(part==='left'){r.rect(0,0,4,32,P.earth[0]);r.rect(4,0,2,32,P.earth[1]);}if(part==='right'){r.rect(26,0,6,32,P.earth[0]);r.rect(25,0,1,32,P.earth[1]);}
  if(row===0){for(let x=0;x<32;x++){const d=8+([0,0,1,2,1,1,0,0][x%8]);r.rect(x,0,1,d,P.grass[2]);r.dot(x,d,P.grass[0]);r.dot(x,d-2,P.grass[3]);}for(let x=4;x<32;x+=11)r.line(x,12,x+3,10,P.earth[4]);}
  if(row===2){r.rect(0,27,32,5,P.grass[2]);for(let x=0;x<32;x++){r.dot(x,27-(x%7===0?1:0),P.grass[0]);}blade(r,8,29,P.grass[1]);}
  return r;}
for(let row=0;row<3;row++)for(const part of ['left','center','right'])add(`cliff.${row}.${part}`,cliff(part,row),{layer:'object',blocked:true});
for(const part of ['left','center','right']){const r=blank();r.rect(0,0,32,32,P.stone[1]);for(let y=0;y<32;y+=8){r.rect(0,y,32,4,P.stone[3]);r.rect(0,y,32,1,P.stone[4]);r.rect(0,y+5,32,1,P.stone[2]);}if(part!=='center'){const x=part==='left'?0:28;r.rect(x,0,4,32,P.stone[0]);r.rect(x+1,0,2,32,P.stone[3]);}add(`stairs.${part}`,r,{layer:'ground',walkableProposal:true});}
for(const dir of ['left','right']){const r=grass();const x=dir==='left'?24:0;r.rect(x,0,8,32,P.earth[1]);r.rect(x+(dir==='left'?0:6),0,2,32,P.grass[0]);r.rect(x+3,0,2,32,P.earth[3]);add(`cliff.return.${dir}`,r,{blocked:true});}
for(const side of ['left','right'])for(let row=0;row<3;row++){const r=grass();const src=cliff('center',row);for(let y=0;y<32;y++)for(let x=0;x<32;x++){const inset=row===0?Math.max(4,16-y):row===2?Math.max(4,y-16):4;const d=side==='left'?x:31-x;if(d<inset)continue;const i=(y*32+x)*4;r.p.set(src.p.subarray(i,i+4),i);if(d===inset)r.dot(x,y,P.earth[0]);else if(d<inset+3&&y>10)r.dot(x,y,P.earth[side==='left'?3:1]);}add(`cliff.corner.${side}.${row}`,r,{layer:'object',blocked:true});}
const fall=new Raster(32,96);for(let y=0;y<96;y++){for(let x=0;x<32;x++){const edge=x<3||x>28;let c=edge?P.water[0]:P.water[2];if(x%9===3||x%9===4)c=P.water[4];if(x%9===5&&y%23<15)c=P.water[5];if(y<6)c=P.water[4];fall.dot(x,y,c);}}slice('waterfall',fall,{layer:'object',blocked:true});
const splash=blank();splash.oval(0,4,32,23,P.water[3]);splash.oval(3,6,26,16,P.water[5]);splash.oval(7,8,18,9,P.water[3]);splash.oval(10,8,12,5,P.water[4]);add('waterfall.splash',splash,{layer:'decal'});

function fence(m){const r=blank();const p=P.wood;
 const post=(x,y)=>{r.rect(x,y+3,7,19,p[0]);r.rect(x+1,y+2,5,18,p[2]);r.rect(x+1,y+3,2,15,p[3]);r.rect(x+1,y,5,3,p[4]);r.dot(x+2,y+7,p[0]);};
 if(m&1){r.rect(14,0,5,14,p[0]);r.rect(14,0,2,13,p[3]);}
 if(m&4){r.rect(14,18,5,14,p[0]);r.rect(14,18,2,14,p[3]);}
 for(const bit of [8,2])if(m&bit){const x=bit===8?0:17;for(const y of [12,21]){r.rect(x,y,15,5,p[0]);r.rect(x,y,15,3,p[2]);r.rect(x,y,15,1,p[4]);}}post(12,7);return r;}
group('Fences · all connections and open / closed gates');
for(let m=0;m<16;m++)add(`fence.${m}`,fence(m),{layer:'object',blocked:true,connections:m});
for(const state of ['open','closed']){const r=new Raster(64,32);r.blit(fence(8),-10,0);r.blit(fence(2),42,0);if(state==='closed'){r.rect(9,12,46,14,P.wood[0]);r.rect(10,13,44,11,P.wood[3]);r.line(10,23,51,13,P.wood[1]);r.line(12,24,53,14,P.wood[1]);r.rect(30,12,2,14,P.wood[0]);r.dot(28,18,P.earth[5]);}assemblies[`gate.${state}`]=slice(`gate.${state}`,r,{layer:'object',blocked:state==='closed'});}

function leafMass(r,cx,cy,rx,ry,seed=0){
 for(let y=Math.max(0,cy-ry);y<=Math.min(r.h-1,cy+ry);y++)for(let x=Math.max(0,cx-rx);x<=Math.min(r.w-1,cx+rx);x++){
  const dx=(x-cx)/rx,dy=(y-cy)/ry,edge=dx*dx+dy*dy;
  const jitter=(hash(Math.floor(x/3),Math.floor(y/3),seed)%5-2)*.035;
  if(edge>1+jitter)continue;
  const lit=-dx*.22-dy*.4;
  let tone=edge>.87?1:lit>.32?4:lit>.02?3:2;
  if(dy>.61)tone=1;
  r.dot(x,y,P.leaf[tone]);
 }
 // Connected irregular leaves, no repeated diamond or highlight-dot stamp.
 for(let y=cy-ry+3;y<cy+ry-2;y+=6)for(let x=cx-rx+3;x<cx+rx-2;x+=7){const xx=x+(hash(x,y,seed)%4),yy=y+(hash(y,x,seed)%3),dx=(xx-cx)/rx,dy=(yy-cy)/ry;if(dx*dx+dy*dy>.67)continue;
  const tone=dy<-.25?5:dx<0?4:3;
  ink(r,hash(x,y,seed)%2?['..00.','.0110','012..','22...']:['.000.','011..','.12..','..2..'],xx-2,yy-2,[P.leaf[tone],P.leaf[Math.min(tone+1,6)],P.leaf[Math.max(tone-1,1)]]);
 }
}
group('Hedges · all connections');
for(let m=0;m<16;m++){const r=blank();r.rect(8,14,16,16,P.leaf[0]);if(m&1)r.rect(8,0,16,18,P.leaf[1]);if(m&2)r.rect(16,10,16,19,P.leaf[1]);if(m&4)r.rect(8,16,16,16,P.leaf[1]);if(m&8)r.rect(0,10,18,19,P.leaf[1]);leafMass(r,16,14,13,12,4);if(m&1)leafMass(r,16,0,12,10,4);if(m&2)leafMass(r,31,14,12,12,4);if(m&4)leafMass(r,16,31,12,12,4);if(m&8)leafMass(r,0,14,12,12,4);add(`hedge.${m}`,r,{layer:'object',blocked:true,connections:m});}
group('Trees · tiled canopy and trunk assemblies');
function tree(type){const r=new Raster(64,type==='cypress'?96:64),h=r.h;
 r.rect(26,h-21,12,18,P.wood[0]);r.rect(28,h-20,8,16,P.wood[2]);r.rect(29,h-17,2,11,P.wood[3]);r.line(28,h-7,22,h-3,P.wood[1]);r.line(36,h-7,41,h-3,P.wood[1]);
 if(type==='cypress'){leafMass(r,32,57,24,25,11);leafMass(r,32,37,20,25,14);leafMass(r,32,20,14,18,16);}
 else{leafMass(r,18,40,15,16,21);leafMass(r,46,39,15,17,22);leafMass(r,33,37,23,20,20);leafMass(r,46,26,14,16,23);leafMass(r,17,26,15,15,24);leafMass(r,31,15,19,13,25);leafMass(r,30,29,19,17,26);}
 return r;}
for(const type of ['broadleaf','cypress'])assemblies[`tree.${type}`]=slice(`tree.${type}`,tree(type),{layer:'foreground',anchorPolicy:'trunk-base; explicit footprint, not alpha'});
const bush=blank();leafMass(bush,10,20,9,9,7);leafMass(bush,22,19,9,10,8);leafMass(bush,15,12,10,9,9);add('bush',bush,{layer:'object',blocked:true});
function bloom(r,x,y,color=0){blade(r,x,y+5,P.leaf[2],5);ink(r,['.00.','0110','0110','.00.'],x-2,y-2,[P.flower[color],P.flower[3]]);r.dot(x,y,P.flower[4]);}
group('Gardens · flowers, cultivated beds, grasses, reeds and rocks');
for(let variant=0;variant<6;variant++){const r=blank();for(const [x,y,c]of [[7,9,0],[23,12,2],[14,23,1]])bloom(r,x+variant%2,y,c===0?variant%3:c);add(`flowers.${variant}`,r,{layer:'decal'});}
for(let v=0;v<4;v++){const r=blank();for(let y=7;y<32;y+=10)for(let x=5;x<32;x+=10){blade(r,x+v%2,y+4,P.leaf[2],6);r.line(x,y+4,x,y-3,P.leaf[3]);r.dot(x-1,y-3,P.leaf[4]);}add(`grass.tall.${v}`,r,{layer:'decal'});}
for(let v=0;v<3;v++){const r=blank();for(let i=0;i<5;i++){const x=7+i*4,h=9+(i*7+v*3)%16;r.line(x,29,x-2,29-h,P.leaf[1]);r.line(x+1,29,x+3,32-h,P.leaf[3]);if(i%2===0){r.rect(x-3,26-h,3,6,P.wood[1]);r.dot(x-3,26-h,P.wood[3]);}}add(`reeds.${v}`,r,{layer:'decal'});}
for(let v=0;v<4;v++){const r=blank();r.poly([[4,24],[5,13],[12,6],[22,8],[28,18],[27,27],[10,29]],P.stone[0]);r.poly([[5,22],[7,13],[13,7],[22,9],[26,18],[23,25],[11,26]],P.stone[2]);r.poly([[7,14],[13,8],[22,10],[18,16]],P.stone[4]);r.poly([[7,15],[17,17],[11,25],[5,22]],P.stone[3]);r.line(18,17,22,23,P.stone[1]);if(v>1){r.rect(8,22,7,2,P.leaf[2]);r.rect(10,21,4,1,P.leaf[4]);}add(`rock.${v}`,r,{layer:'object',blocked:true});}
for(let v=0;v<3;v++){const r=blank();r.oval(2,16,16,9,P.leaf[1]);r.oval(2,15,16,8,P.leaf[3]);r.poly([[11,19],[18,14],[18,21]],'transparent');r.oval(20,5,10,6,P.leaf[3]);if(v===1)bloom(r,9,14,2);add(`lilypad.${v}`,r,{layer:'decal'});}
for(const kind of ['lettuce','carrot','seedling']){const r=blank();for(let y=8;y<32;y+=16)for(let x=8;x<32;x+=16){if(kind==='lettuce')leafMass(r,x,y+2,6,5,3);else {blade(r,x,y+3,P.leaf[2],7);blade(r,x,y+2,P.leaf[4],4);if(kind==='carrot')r.rect(x,y+3,2,3,P.clay[4]);}}add(`garden.${kind}`,r,{layer:'decal'});}

group('Bridge and dock · repeating deck, rails, posts and ends');
for(const dir of ['horizontal','vertical'])for(const edge of ['near','center','far']){const r=blank();r.rect(0,0,32,32,P.wood[0]);for(let v=0;v<32;v+=8){if(dir==='horizontal'){r.rect(v+1,0,6,32,P.wood[3]);r.rect(v+1,0,1,32,P.wood[4]);r.rect(v+6,0,1,32,P.wood[2]);r.dot(v+3,5,P.wood[1]);r.dot(v+3,26,P.wood[1]);}else{r.rect(0,v+1,32,6,P.wood[3]);r.rect(0,v+1,32,1,P.wood[4]);r.rect(0,v+6,32,1,P.wood[2]);r.dot(5,v+3,P.wood[1]);r.dot(26,v+3,P.wood[1]);}}
 if(edge!=='center'){const n=edge==='near'?0:27;if(dir==='horizontal'){r.rect(0,n,32,5,P.wood[1]);r.rect(0,n,32,1,P.wood[4]);}else{r.rect(n,0,5,32,P.wood[1]);r.rect(n,0,1,32,P.wood[4]);}}
 add(`bridge.${dir}.${edge}`,r,{layer:'ground',walkableProposal:true});}
const post=blank();post.rect(12,6,9,25,P.wood[0]);post.rect(13,8,7,21,P.wood[2]);post.rect(13,9,2,19,P.wood[3]);post.oval(11,4,11,6,P.wood[4]);post.oval(13,5,6,3,P.wood[2]);add('bridge.post',post,{layer:'object'});

group('Fountain · repeatable basin, corners and two-tile jet');
for(let y=0;y<3;y++)for(let x=0;x<3;x++){const r=water();if(x===0){r.rect(0,0,8,32,P.stone[1]);r.rect(1,0,5,32,P.stone[3]);r.rect(2,0,2,32,P.stone[4]);r.rect(8,0,3,32,P.water[0]);}if(x===2){r.rect(24,0,8,32,P.stone[1]);r.rect(24,0,6,32,P.stone[3]);r.rect(25,0,4,32,P.stone[4]);r.rect(21,0,3,32,P.water[0]);}if(y===0){r.rect(0,0,32,9,P.stone[1]);r.rect(0,1,32,6,P.stone[3]);r.rect(0,1,32,2,P.stone[4]);r.rect(0,9,32,2,P.water[0]);}if(y===2){r.rect(0,21,32,11,P.stone[1]);r.rect(0,21,32,5,P.stone[4]);r.rect(0,26,32,3,P.stone[2]);r.rect(15,22,1,9,P.stone[1]);}if(x!==1&&y!==1){const xx=x===0?0:24,yy=y===0?0:24;r.rect(xx,yy,8,8,P.stone[2]);r.rect(xx+1,yy+1,6,5,P.stone[4]);}add(`fountain.basin.${x}.${y}`,r,{layer:'object',blocked:true});}
const jet=new Raster(32,64);jet.oval(2,48,28,12,P.water[3]);jet.oval(5,50,22,7,P.water[5]);jet.oval(8,51,16,5,P.water[2]);jet.rect(12,29,8,24,P.stone[1]);jet.rect(13,29,5,24,P.stone[3]);jet.oval(3,24,26,12,P.stone[0]);jet.oval(3,22,26,10,P.stone[4]);jet.oval(6,23,20,6,P.water[1]);jet.rect(14,11,3,17,P.water[4]);jet.line(15,9,8,15,P.water[5]);jet.line(15,9,23,15,P.water[3]);jet.line(8,15,7,28,P.water[4]);jet.line(23,15,24,30,P.water[4]);jet.rect(15,7,2,5,P.water[5]);jet.rect(6,32,2,6,P.water[5]);jet.rect(24,35,2,6,P.water[3]);assemblies['fountain.jet']=slice('fountain.jet',jet,{layer:'object'});

group('Town details · benches, lamps, signs, mailbox, pots and planters');
const bench=new Raster(64,32);for(const x of [9,49]){bench.rect(x,10,5,21,P.stone[0]);bench.rect(x+1,11,2,19,P.stone[2]);}for(const y of [4,11,19]){bench.rect(3,y,58,6,P.wood[1]);bench.rect(4,y,56,3,P.wood[3]);bench.rect(4,y,56,1,P.wood[4]);}assemblies.bench=slice('bench',bench,{layer:'object',blocked:true});
const lamp=new Raster(32,64);lamp.rect(14,19,4,43,P.stone[0]);lamp.rect(15,19,1,42,P.stone[2]);lamp.rect(10,60,12,3,P.stone[1]);lamp.rect(9,7,14,15,P.stone[0]);lamp.rect(11,9,10,10,P.earth[4]);lamp.rect(12,10,3,6,P.plaster[4]);lamp.rect(15,8,2,13,P.stone[1]);lamp.poly([[6,7],[12,3],[20,3],[26,7]],P.stone[1]);lamp.rect(15,1,2,3,P.stone[0]);assemblies.lamp=slice('lamp',lamp,{layer:'object'});
const sign=new Raster(32,64);sign.rect(14,26,5,34,P.wood[1]);sign.rect(14,27,2,32,P.wood[3]);sign.rect(2,20,28,20,P.wood[0]);sign.rect(3,21,26,17,P.wood[3]);sign.rect(4,21,24,1,P.wood[4]);sign.line(8,27,24,27,P.wood[1]);sign.line(8,31,20,31,P.wood[1]);assemblies.sign=slice('sign',sign,{layer:'object'});
const mailbox=blank();mailbox.rect(14,15,4,16,P.wood[1]);mailbox.rect(15,16,1,14,P.wood[3]);mailbox.poly([[5,7],[8,3],[23,3],[26,7],[26,18],[5,18]],P.teal[0]);mailbox.rect(6,7,18,10,P.teal[2]);mailbox.rect(8,4,14,3,P.teal[3]);mailbox.rect(7,9,9,2,P.teal[0]);mailbox.rect(23,5,2,8,P.clay[2]);mailbox.rect(24,5,5,4,P.clay[4]);add('mailbox',mailbox,{layer:'object'});
for(const flower of [false,true]){const r=blank();r.poly([[6,15],[26,15],[24,29],[21,31],[11,31],[8,28]],P.clay[1]);r.poly([[8,16],[24,16],[22,28],[11,28]],P.clay[3]);r.rect(5,14,22,5,P.clay[2]);r.rect(6,14,20,2,P.clay[5]);leafMass(r,16,10,12,8,41);if(flower)for(const [x,y]of [[9,8],[19,7],[23,12]])bloom(r,x,y,2);add(`pot.${flower?'flowers':'fern'}`,r,{layer:'object'});}
for(const part of ['left','center','right']){const r=blank();r.rect(0,17,32,13,P.stone[1]);r.rect(0,18,32,8,P.stone[3]);r.rect(0,17,32,2,P.stone[4]);r.rect(0,22,32,1,P.stone[2]);r.rect(15,18,1,4,P.stone[2]);leafMass(r,8,12,11,8,3);leafMass(r,25,12,11,8,7);bloom(r,8,8,1);bloom(r,23,10,2);if(part==='left')r.rect(0,19,2,9,P.stone[1]);if(part==='right')r.rect(30,19,2,9,P.stone[1]);add(`planter.${part}`,r,{layer:'object',blocked:true});}

// Roof/wall center pieces are genuinely reused, including on a wider building.
function house(name,width,color,style){const rows=[];for(let y=0;y<3;y++)rows.push(Array.from({length:width},(_,x)=>`roof.${color}.${y}.${x===0?'left':x===width-1?'right':'center'}`));for(let y=0;y<2;y++)rows.push(Array.from({length:width},(_,x)=>x===Math.floor(width/2)?`door.wood.closed.0.${y}`:x===0||x===width-1?`wall.${style}.${y}.${x===0?'left':'right'}`:`windowbox.${style}.0.${y}`));assemblies[name]=rows;}
house('house.cottage',5,'clay','plaster');house('house.garden',5,'teal','timber');house('house.shop',7,'teal','stone');
assemblies['fountain.small']=Array.from({length:3},(_,y)=>Array.from({length:3},(_,x)=>`fountain.basin.${x}.${y}`));
assemblies['fountain.wide']=Array.from({length:3},(_,y)=>Array.from({length:5},(_,x)=>`fountain.basin.${x===0?0:x===4?2:1}.${y}`));

if(process.argv.includes('--from-pixels')){const source=JSON.parse(await readFile('art/source/overworld-v1/pixels.json','utf8'));if(source.tiles.length!==tiles.length)throw Error('Source tile count');for(const t of tiles){const edited=source.tiles.find(s=>s.id===t.id);if(!edited||edited.rows.length!==32||edited.rows.some(r=>r.length!==32))throw Error('Invalid pixel source '+t.id);t.r=blank();edited.rows.forEach((row,y)=>row.forEach((n,x)=>{if(n)t.r.dot(x,y,source.colors[n]);}));}}
const atlas=new Raster(1024,Math.max(1024,Math.ceil(cursor/32)*32));for(const t of tiles)atlas.blit(t.r,t.x,t.y);
await atlas.save(`${OUT}/master.png`);
await writeFile(`${OUT}/palette.json`,JSON.stringify(P,null,2)+'\n');
const manifest={schemaVersion:1,assetId:'critz.overworld.review.v1',approval:'awaiting user visual review',image:'master.png',imageWidth:atlas.w,imageHeight:atlas.h,tileWidth:32,tileHeight:32,baseTileWidth:16,baseTileHeight:16,columns:32,spacing:0,margin:0,render:'integer coordinates; nearest-neighbor; binary alpha',palette:'palette.json',referenceRevision:'pret/pokeemerald@5eff78649e7170a877b961ef0b3da13b81a16038',referenceMethod:'Existing pinned source/assembly measurements; no new emulator observation; no reference pixels used',neighborBits:{N:1,E:2,S:4,W:8,NE:16,SE:32,SW:64,NW:128},sections,tiles:tiles.map(({r,...t})=>({...t,subtiles:[{x:t.x,y:t.y},{x:t.x+16,y:t.y},{x:t.x,y:t.y+16},{x:t.x+16,y:t.y+16}]})),assemblies,animation:'Static art only; no animation timing or approval inferred',collision:'Properties are review proposals, not gameplay collision. Map-authoring footprints remain separate.'};
manifest.assemblyMetadata={
 'house.cottage':{canvas:[160,160],anchor:[80,160],roofRows:[0,1,2],footprint:[0,3,5,2],doorCell:[2,4]},
 'house.garden':{canvas:[160,160],anchor:[80,160],roofRows:[0,1,2],footprint:[0,3,5,2],doorCell:[2,4]},
 'house.shop':{canvas:[224,160],anchor:[112,160],roofRows:[0,1,2],footprint:[0,3,7,2],doorCell:[3,4]},
 'tree.broadleaf':{canvas:[64,64],anchor:[32,64],footprint:[0,1,2,1],occlusion:'canopy above trunk; per-tile sort pending runtime integration'},
 'tree.cypress':{canvas:[64,96],anchor:[32,96],footprint:[0,2,2,1],occlusion:'canopy above trunk; per-tile sort pending runtime integration'},
 'fountain.small':{canvas:[96,96],anchor:[48,96],footprint:[0,0,3,3]},
 'fountain.wide':{canvas:[160,96],anchor:[80,96],footprint:[0,0,5,3]}
};
await writeFile(`${OUT}/master.json`,JSON.stringify(manifest,null,2)+'\n');
await writeFile(`${OUT}/master.tsj`,JSON.stringify({type:'tileset',version:'1.10',tiledversion:'1.11.2',name:'Critz overworld · REVIEW v1',tilewidth:32,tileheight:32,tilecount:atlas.w*atlas.h/1024,columns:32,spacing:0,margin:0,image:'master.png',imagewidth:atlas.w,imageheight:atlas.h,tiles:manifest.tiles.map(t=>({id:t.index,properties:[{name:'assetId',type:'string',value:t.id},{name:'layer',type:'string',value:t.layer},{name:'reviewOnly',type:'bool',value:true}]}))},null,2)+'\n');
// Editable source pixels; rebuilding does not depend on the generative study.
const colors=['#00000000',...C];const indexed=tiles.map(t=>({id:t.id,rows:Array.from({length:32},(_,y)=>Array.from({length:32},(_,x)=>{const i=(y*32+x)*4;if(!t.r.p[i+3])return 0;const hex='#'+t.r.p.subarray(i,i+3).toString('hex');const n=colors.indexOf(hex);if(n<0)throw Error(hex);return n;}))}));
await writeFile('art/source/overworld-v1/pixels.json',JSON.stringify({colors,tiles:indexed})+'\n');

const maps=[];
function scene(name,w,h){return {name,width:w,height:h,tilewidth:32,tileheight:32,layers:{ground:Array(w*h).fill('ground.grass.0'),decal:Array(w*h).fill(null),object:Array(w*h).fill(null),foreground:Array(w*h).fill(null)}};}
const at=(map,x,y)=>y*map.width+x;
function put(map,id,x,y,layer){if(x<0||y<0||x>=map.width||y>=map.height)return;map.layers[layer||byId[id].layer][at(map,x,y)]=id;}
function stamp(map,name,x,y,layer='object'){assemblies[name].forEach((row,j)=>row.forEach((id,i)=>put(map,id,x+i,y+j,layer)));}
function area(map,kind,predicate){const inside=(x,y)=>x>=0&&y>=0&&x<map.width&&y<map.height&&predicate(x,y);for(let y=0;y<map.height;y++)for(let x=0;x<map.width;x++)if(inside(x,y)){let m=0;[[0,-1,1],[1,0,2],[0,1,4],[-1,0,8],[1,-1,16],[1,1,32],[-1,1,64],[-1,-1,128]].forEach(([dx,dy,b])=>{if(inside(x+dx,y+dy))m|=b;});put(map,`${kind}.${normalize(m)}`,x,y,'ground');}}
function runFence(map,x,y,n){for(let i=0;i<n;i++)put(map,`fence.${i===0?2:i===n-1?8:10}`,x+i,y);}
const town=scene('Garden town assembly proof',32,24);
for(let y=0;y<24;y++)for(let x=0;x<32;x++)put(town,`ground.grass.${hash(x,y)%8}`,x,y,'ground');
area(town,'water',(x,y)=>(x>=24+(y<6?1:y>15?-1:0)&&x<=27+(y<6?1:y>15?-1:0))||(y>=17&&y<=21&&x>=22&&x<=29));
area(town,'path',(x,y)=>(y>=10&&y<=12&&x>=2&&x<=27)||(x>=9&&x<=11&&y>=5&&y<=22)||(x>=19&&x<=21&&y>=5&&y<=16)||(y>=19&&y<=21&&x<=11));
area(town,'paving',(x,y)=>x>=13&&x<=20&&y>=13&&y<=17);
area(town,'soil',(x,y)=>x>=2&&x<=6&&y>=13&&y<=15);
for(let x=2;x<=6;x++)for(let y=13;y<=15;y++)put(town,`garden.${y===13?'lettuce':y===14?'carrot':'seedling'}`,x,y);
stamp(town,'house.cottage',5,3);stamp(town,'house.garden',16,3);stamp(town,'house.shop',13,18);
stamp(town,'chimney',8,2,'foreground');stamp(town,'chimney',19,2,'foreground');
area(town,'path',(x,y)=>(x===7&&y>=7&&y<=10)||(x===18&&y>=7&&y<=10));
// These approaches connect into the horizontal lane with intentional overlap.
for(const x of [7,18]){put(town,'path.255',x,10);put(town,'path.255',x,11);}
runFence(town,3,9,4);runFence(town,8,9,4);runFence(town,15,9,3);runFence(town,19,9,3);
for(const [x,y]of [[4,7],[10,7],[15,7],[21,7]])put(town,'pot.flowers',x,y);
put(town,'mailbox',8,8);put(town,'mailbox',19,8);
stamp(town,'fountain.small',15,14);stamp(town,'fountain.jet',16,13);
stamp(town,'bench',13,16);stamp(town,'bench',19,16);stamp(town,'lamp',13,12);stamp(town,'lamp',20,12);
for(let x=23;x<29;x++)for(let y=10;y<=12;y++)put(town,`bridge.horizontal.${y===10?'near':y===12?'far':'center'}`,x,y,'ground');
area(town,'path',(x,y)=>x>=28&&y>=10&&y<=12);
for(const x of [23,26,28]){put(town,'bridge.post',x,10);put(town,'bridge.post',x,12);}
for(const [x,y]of [[26,6],[26,15],[24,19],[29,20]])put(town,'lilypad.1',x,y);
for(const [x,y]of [[24,5],[23,15],[22,20],[27,2]])put(town,'reeds.1',x,y);
for(const [x,y]of [[0,0],[2,0],[4,0],[6,0],[8,0],[10,0],[12,0],[14,0],[16,0],[18,0],[20,0],[22,0],[0,3],[1,6],[0,14],[0,17],[1,21],[4,21],[27,22],[29,22],[30,0],[30,3],[29,6],[30,14],[30,17]])stamp(town,'tree.broadleaf',x,y,'foreground');
for(const [x,y]of [[12,3],[22,4],[2,17]])stamp(town,'tree.cypress',x,y,'foreground');
for(const [x,y]of [[3,11],[4,8],[12,9],[14,8],[21,17],[7,16],[9,17],[22,7],[2,8]])put(town,'flowers.2',x,y);
for(const [x,y]of [[2,3],[3,4],[11,7],[13,9],[7,14],[7,15],[22,8],[21,8],[11,15],[12,19],[7,21],[28,8],[29,8]])put(town,'bush',x,y);
for(let x=2;x<=6;x++)put(town,`planter.${x===2?'left':x===6?'right':'center'}`,x,16);
for(let x=28;x<=31;x++)for(let y=16;y<19;y++)put(town,`cliff.${y-16}.${x===28?'left':x===31?'right':'center'}`,x,y,'object');
for(let y=16;y<19;y++)put(town,`waterfall.0.${y-16}`,29,y,'object');put(town,'waterfall.splash',29,19);
area(town,'path',(x,y)=>x===16&&y>=22);
maps.push(town);
// A wider town workshop proves replaceable building width and hardscape modules.
const workshop=scene('Architecture and terrain construction proof',30,18);
stamp(workshop,'house.cottage',1,1);stamp(workshop,'house.garden',9,1);stamp(workshop,'house.shop',17,1);
for(let x=1;x<27;x++)for(let y=7;y<=8;y++)put(workshop,'ground.path',x,y,'ground');
stamp(workshop,'fountain.wide',2,11);stamp(workshop,'fountain.jet',4,10);stamp(workshop,'fountain.small',10,11);stamp(workshop,'fountain.jet',11,10);
for(let x=17;x<=27;x++)for(let y=10;y<13;y++)put(workshop,`cliff.${y-10}.${x===17?'left':x===27?'right':'center'}`,x,y,'object');
for(let y=10;y<13;y++)for(let x=21;x<=22;x++)put(workshop,`stairs.${x===21?'left':'right'}`,x,y,'object');
for(let x=17;x<28;x++)put(workshop,`hedge.${x===17?2:x===27?8:10}`,x,15);
runFence(workshop,1,16,6);stamp(workshop,'gate.closed',7,16);runFence(workshop,9,16,5);
maps.push(workshop);
const topology=scene('Terrain topology proof',32,24);
for(const [kind,ox,oy]of [['path',1,1],['water',17,1],['paving',1,13],['soil',17,13]])area(topology,kind,(x,y)=>{x-=ox;y-=oy;return x>=0&&y>=0&&x<13&&y<9&&(!(x>=3&&x<=5&&y>=3&&y<=5))&&(!(x>=8&&y>=5))&&(!(x<2&&y===0));});
maps.push(topology);
function resolveTerrain(map){const original=[...map.layers.ground];for(let y=0;y<map.height;y++)for(let x=0;x<map.width;x++){const id=original[at(map,x,y)],kind=id.split('.')[0];if(!['water','soil','path','paving'].includes(kind))continue;let m=0;[[0,-1,1],[1,0,2],[0,1,4],[-1,0,8],[1,-1,16],[1,1,32],[-1,1,64],[-1,-1,128]].forEach(([dx,dy,b])=>{const a=x+dx,c=y+dy;if(a<0||c<0||a>=map.width||c>=map.height){m|=b;return;}const n=original[at(map,a,c)];if(n.startsWith(kind+'.')||(kind==='path'&&n.startsWith('bridge.')))m|=b;});put(map,`${kind}.${normalize(m)}`,x,y,'ground');}}
function render(map){const r=new Raster(map.width*32,map.height*32);for(const layer of ['ground','decal','object','foreground'])map.layers[layer].forEach((id,i)=>{if(id){const t=byId[id];r.blit(atlas.crop(t.x,t.y,32,32),i%map.width*32,Math.floor(i/map.width)*32);}});return r;}
maps.forEach(resolveTerrain);
const heroSource=JSON.parse(await readFile('art/source/hero-boy-v1/idle.sprite.json','utf8')),hero=new Raster(32,64);heroSource.frames[0].pixels.forEach((n,i)=>{if(n)hero.dot(i%32,Math.floor(i/32),heroSource.palette[n]);});
for(let i=0;i<maps.length;i++){await writeFile(`${OUT}/map-${i}.json`,JSON.stringify(maps[i],null,2)+'\n');const r=render(maps[i]);await r.save(`${OUT}/proof-${i}.png`);if(i===0){r.blit(hero,224,272);await r.save(`${OUT}/town-with-hero.png`);const v=r.crop(96,64,480,320);await v.save(`${OUT}/viewport.png`);await v.scale(3).save(`${OUT}/viewport-3x.png`);await r.crop(384,352,480,320).save(`${OUT}/water-garden-viewport.png`);}}
// Sheet grouped without labels; separate index carries IDs so pixels stay clean.
await atlas.scale(2).save(`${OUT}/master-2x.png`);
await writeFile(`${OUT}/build-summary.json`,JSON.stringify({tiles:tiles.length,allocatedCells:cursor,atlas:[atlas.w,atlas.h],colors:C.length,terrainMasks:masks.length,assemblies:Object.keys(assemblies).length,sha256:createHash('sha256').update(await readFile(`${OUT}/master.png`)).digest('hex')},null,2)+'\n');
console.log(JSON.stringify({tiles:tiles.length,cells:cursor,masks:masks.length,atlas:[atlas.w,atlas.h]}));
