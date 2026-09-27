// Original native-pixel extensions to the B1/G1 editable source.
// No source-game sprite or rejected environment art is read here.
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { Raster } from '../raster.mjs';
const originals = JSON.parse(await readFile('art/source/characters-v1/native-pixel-data.json','utf8'));
const out = 'assets/playable/characters';
await mkdir(out,{recursive:true});
const clone = rows => rows.map(row => Array.from(row));
const blank = () => Array.from({length:32},()=>Array(16).fill('.'));
const fill = (rows,x,y,w,h,symbol) => { for(let yy=y;yy<y+h;yy++)for(let xx=x;xx<x+w;xx++)if(rows[yy] && xx>=0 && xx<16) rows[yy][xx]=symbol; };
const stamp = (rows,lines,y) => lines.forEach((line,i)=>Array.from(line).forEach((v,x)=>{if(v!=='.')rows[y+i][x]=v;}));
const humanoids = [
  {id:'hero.boy',source:'B1'}, {id:'hero.girl',source:'G1'},
  {id:'mom',source:'G1',adult:true,palette:{D:'#784858',C:'#b87080',A:'#d898a0',N:'#485068',P:'#686878'},hair:'bun'},
  {id:'professor',source:'B1',adult:true,palette:{S:'#886050',M:'#b89070',L:'#e0b888',H:'#889088',J:'#c0c0a0',D:'#98a898',C:'#d8dcc0',A:'#f0ecd0',N:'#586858',P:'#809070'},hat:true,glasses:true},
  {id:'adult',source:'B1',adult:true,palette:{S:'#805048',M:'#b88060',L:'#d8a880',H:'#483838',J:'#705040',D:'#486858',C:'#789078',A:'#a8b090'}},
  {id:'shopkeeper',source:'B1',adult:true,palette:{S:'#705048',M:'#a87858',L:'#d0a078',H:'#584038',J:'#885840',D:'#385858',C:'#58a098',A:'#98c0a0'},apron:true},
  {id:'doctor',source:'G1',adult:true,palette:{S:'#886058',M:'#c09078',L:'#e0b098',H:'#584040',J:'#785858',D:'#a0b0a8',C:'#e0e8d0',A:'#f0f0d8',N:'#607880',P:'#88a0a0'},badge:true,hair:'bob'},
  {id:'glassblower',source:'G1',adult:true,palette:{S:'#705048',M:'#a07858',L:'#d0a078',H:'#483830',J:'#705040',D:'#806040',C:'#c09858',A:'#e0c080',N:'#486878',P:'#709098'},apron:true,glasses:true,hair:'bun'},
];

function front(spec) {
  let rows=clone(originals[spec.source].rows);
  if(!spec.adult) return rows;
  // Adult posture: a slightly longer torso, same16x32 frame and comparable head.
  const head=rows.slice(11,23).map(row=>[...row]);
  rows=blank(); head.forEach((row,i)=>rows[10+i]=row);
  stamp(rows,[
    '....OWSSSSWO....','...OWCCCCCCWO...','..OSWACCCCAWSO..',
    '..OLWCCCCCCWLO..','..OMDCCCCCCDMM..','...ODCCCCCCDO...',
    '....ONPPPNO.....','....OMMOMMO.....','...OWWOOWWO.....',
  ],22);
  if(spec.hair==='bun') {
    fill(rows,0,9,16,6,'.');
    stamp(rows,['......OOOO......','.....OJJHHO.....','....OJJHHHHO....','...OJJHHHHHHO...','..OJJHHHHHHHHO..','..OHHHHHHHHHHO..'],9);
  }
  if(spec.hair==='bob') {
    fill(rows,0,10,16,5,'.');
    stamp(rows,['.....OOOOOO.....','...OOJJJHHHOO...','..OJJHHHHHHHHO..','..OHHHHHHHHHHO..','..OHHHHHHHHHHO..'],10);
    fill(rows,2,15,2,7,'H'); fill(rows,12,15,2,7,'H');
  }
  if(spec.hat) {
    fill(rows,1,9,14,3,'.');
    stamp(rows,['.....OOOOOO.....','....OAAAACCO....','....OCCCCCCO....','..OOCCCCCCCCOO..','..ODDDDDDDDDDO..'],8);
  }
  if(spec.glasses) { fill(rows,4,18,3,2,'A');fill(rows,9,18,3,2,'A');fill(rows,5,19,1,1,'O');fill(rows,10,19,1,1,'O');fill(rows,7,18,2,1,'D'); }
  if(spec.apron) { fill(rows,6,23,4,1,'N');fill(rows,5,24,6,4,'N');fill(rows,6,24,2,1,'P');fill(rows,6,26,4,1,'P'); }
  if(spec.badge) { fill(rows,10,24,2,2,'V'); }
  return rows;
}
function back(spec,base) {
  const rows=base.map(r=>[...r]);
  for(let y=15;y<22;y++)for(let x=2;x<14;x++)if(rows[y][x]!=='.' && rows[y][x]!=='O')rows[y][x]=(y===16 && x<7)?'J':'H';
  fill(rows,5,22,6,1,'S');fill(rows,5,23,6,1,'D');
  if(spec.apron) {fill(rows,5,24,6,4,'C');fill(rows,5,25,6,1,'N');}
  if(spec.badge) fill(rows,10,24,2,2,'C');
  return rows;
}
function side(spec,dir) {
  const rows=blank();
  const y=spec.adult?10:11;
  fill(rows,5,y,6,1,'O');fill(rows,4,y+1,8,2,'O');fill(rows,3,y+3,10,6,'O');fill(rows,4,y+9,8,2,'O');fill(rows,5,y+11,6,1,'O');
  fill(rows,5,y+1,6,2,'J');fill(rows,4,y+3,8,4,'H');fill(rows,5,y+3,3,1,'J');
  fill(rows,3,y+6,7,4,'S');fill(rows,4,y+6,5,4,'M');fill(rows,3,y+6,4,2,'L');
  fill(rows,2,y+7,2,2,'O');fill(rows,2,y+7,2,1,'L');fill(rows,4,y+8,1,2,'O');
  fill(rows,9,y+4,3,6,'H');fill(rows,8,y+8,2,2,'M');fill(rows,5,y+10,4,1,'M');
  if(spec.source==='G1') {fill(rows,10,y,3,2,'O');fill(rows,11,y+1,3,4,'H');fill(rows,10,y+2,2,1,'J');}
  if(spec.hair==='bun') {fill(rows,8,y-1,3,2,'O');fill(rows,9,y,3,2,'H');}
  if(spec.hat) {fill(rows,5,9,7,3,'C');fill(rows,6,9,4,1,'A');fill(rows,2,12,11,1,'D');}
  const top=spec.adult?22:23;
  fill(rows,5,top,7,6,'O');fill(rows,6,top,5,5,'C');fill(rows,6,top,4,1,'A');
  fill(rows,7,top+1,3,3,'W');fill(rows,7,top+3,3,3,'S');fill(rows,7,top+3,2,2,'M');
  if(spec.apron) {fill(rows,5,top+1,2,5,'N');fill(rows,5,top+2,1,2,'P');}
  if(spec.glasses) {fill(rows,3,y+7,4,2,'A');fill(rows,4,y+8,1,1,'O');}
  fill(rows,5,28,6,2,'N');fill(rows,6,28,2,1,'P');fill(rows,4,30,4,1,'O');fill(rows,8,30,3,1,'O');fill(rows,4,29,3,1,'W');
  return dir==='right'?rows.map(row=>[...row].reverse()):rows;
}

function gait(base,dir,pose,mode) {
  if(pose==='idle' && mode==='walk')return base.map(r=>[...r]);
  const rows=base.map(r=>[...r]);
  const phase=pose==='strideB'?1:0;
  fill(rows,0,28,16,4,'.');
  if(dir==='left'||dir==='right') {
    const a=phase?9:3,b=phase?4:9;
    fill(rows,a,28,3,3,'N');fill(rows,a,29,2,1,'P');fill(rows,a-1,31,4,1,'O');fill(rows,a-1,30,3,1,'W');
    fill(rows,b,28,3,2,'N');fill(rows,b-1,30,4,1,'O');fill(rows,b-1,29,3,1,'W');
    // Running has a forward hand and compact bent rear elbow.
    if(mode==='run') {const lead=dir==='left'?3:11;fill(rows,lead,23,2,3,'O');fill(rows,lead,23,2,2,'M');fill(rows,7,26,3,2,'C');}
  } else {
    const a=phase?9:4,b=phase?4:9;
    fill(rows,a,28,3,3,'N');fill(rows,a,29,2,1,'M');fill(rows,a-1,31,4,1,'O');fill(rows,a-1,30,3,1,'W');
    fill(rows,b,28,3,2,'N');fill(rows,b-1,30,4,1,'O');fill(rows,b-1,29,3,1,'W');
    const arm=phase?2:12;fill(rows,arm,24,2,3,'S');fill(rows,arm,24,2,2,'M');
    if(mode==='run') {const other=phase?12:2;fill(rows,other,22,2,3,'O');fill(rows,other,22,2,2,'M');}
  }
  if(pose==='idle') {fill(rows,0,28,16,4,'.');fill(rows,4,28,3,2,'N');fill(rows,9,28,3,2,'N');fill(rows,3,30,4,1,'O');fill(rows,8,30,4,1,'O');fill(rows,3,29,3,1,'W');fill(rows,8,29,3,1,'W');}
  return rows;
}

const kaidPalette={'.':'#000000',O:'#304850',H:'#407878',J:'#68a8a8',S:'#986840',M:'#c09050',L:'#e8c878',D:'#487878',C:'#78b8b0',A:'#b8e0c8',N:'#405870',P:'#688898',W:'#e8e8c8',V:'#d87860'};
function pitcher(dir) {
  const r=blank();
  fill(r,3,11,9,15,'O');fill(r,4,12,7,13,'D');fill(r,4,13,6,10,'C');
  fill(r,5,16,5,7,'M');fill(r,5,17,4,2,'L');fill(r,5,22,5,1,'S');
  fill(r,3,11,9,2,'A');fill(r,4,13,1,10,'A');fill(r,10,14,1,9,'J');
  // Explicit sides preserve the same physical asymmetric vessel: never mirror Kaid.
  if(dir==='down'||dir==='up') {
    fill(r,0,11,3,2,'O');fill(r,1,12,3,2,'A');
    fill(r,12,14,3,1,'O');fill(r,12,15,2,1,'A');fill(r,14,15,2,7,'O');fill(r,14,16,1,5,'C');fill(r,12,22,3,1,'O');fill(r,12,21,2,1,'A');
  } else if(dir==='left') {
    fill(r,0,11,4,2,'O');fill(r,1,12,3,2,'A');fill(r,10,14,3,9,'O');fill(r,11,15,1,7,'J');
  } else {
    fill(r,1,14,3,9,'O');fill(r,1,15,1,7,'A');fill(r,2,16,1,5,'.');fill(r,11,11,3,2,'A');
  }
  if(dir!=='up') {
    if(dir==='down') {fill(r,5,18,1,2,'O');fill(r,9,18,1,2,'O');fill(r,7,21,2,1,'O');}
    else {const x=dir==='left'?5:9;fill(r,x,18,1,2,'O');fill(r,x,21,2,1,'S');}
  } else {fill(r,6,17,2,4,'L');fill(r,7,20,3,1,'M');}
  fill(r,2,23,2,3,'O');fill(r,2,23,2,2,'C');fill(r,11,23,2,3,'O');fill(r,11,23,2,2,'C');
  fill(r,4,25,7,3,'N');fill(r,5,26,5,1,'P');fill(r,4,28,3,2,'N');fill(r,9,28,3,2,'N');fill(r,3,30,4,1,'O');fill(r,8,30,4,1,'O');fill(r,3,29,3,1,'W');fill(r,8,29,3,1,'W');
  return r;
}
const frames=[];const characters={};
for(const spec of [...humanoids,{id:'kaid'}]) {
  const palette=spec.id==='kaid'?kaidPalette:{...originals[spec.source].palette,...spec.palette};
  const base=spec.id==='kaid'?null:front(spec);
  characters[spec.id]={frame:[16,32],anchor:[8,32],directions:{},status:'playable-review'};
  for(const dir of ['down','up','left','right']) {
    const basePose=spec.id==='kaid'?pitcher(dir):dir==='down'?base:dir==='up'?back(spec,base):side(spec,dir);
    characters[spec.id].directions[dir]={};
    for(const mode of ['walk','run']) {
      characters[spec.id].directions[dir][mode]={};
      for(const pose of ['idle','strideA','strideB']) {
        const rows=gait(basePose,dir,pose,mode);
        const frame=new Raster(16,32);
        rows.forEach((row,y)=>row.forEach((symbol,x)=>{if(symbol!=='.')frame.dot(x,y,palette[symbol]);}));
        const id=`char.${spec.id}.${dir}.${mode}.${pose}`;
        frames.push({id,frame,character:spec.id,direction:dir,mode,pose,anchor:[8,32],mirrored:spec.id!=='kaid'&&dir==='right'});
        characters[spec.id].directions[dir][mode][pose]=id;
      }
    }
  }
}
const atlas=new Raster(256,Math.ceil(frames.length/16)*32);
const assets=frames.map((f,i)=>{const x=i%16*16,y=Math.floor(i/16)*32;atlas.blit(f.frame,x,y);return {id:f.id,rect:[x,y,16,32],anchor:f.anchor,character:f.character,direction:f.direction,mode:f.mode,pose:f.pose,mirrored:f.mirrored,status:'playable-review'};});
await atlas.save(out+'/atlas.png');
await writeFile(out+'/atlas.json',JSON.stringify({schemaVersion:1,image:'atlas.png',size:[atlas.w,atlas.h],status:'playable-review',assets,characters},null,2)+'\n');
// A readable4x sheet: rows characters, columns down/up/left/right idle+strides.
const lineup=new Raster(16*12,32*9);
for(let i=0;i<frames.length;i++){const f=frames[i];if(f.mode!=='walk')continue;const row=Object.keys(characters).indexOf(f.character),col=['down','up','left','right'].indexOf(f.direction)*3+['idle','strideA','strideB'].indexOf(f.pose);lineup.blit(f.frame,col*16,row*32);}
await lineup.scale(4).save('docs/reviews/M1-I2/characters-4x.png');
console.log(JSON.stringify({characters:Object.keys(characters),frames:frames.length,size:[atlas.w,atlas.h]}));
