import fs from 'node:fs';import path from 'node:path';
import {Pixels,repo,loadProject,saveAsset,hash} from './pixels.mjs';
function warp(a,fn){const b=new Pixels(a.w,a.h);for(let y=0;y<a.h;y++)for(let x=0;x<a.w;x++){const c=a.get(x,y);if(c){const [xx,yy]=fn(x,y);b.p(xx,yy,c);}}return b;}
function shiftPart(a,box,dx,dy){const b=a.clone();b.rect(box[0],box[1],box[2]-1,box[3]-1,null);b.blit(a,dx,dy,box);return b;}
function move(a,id,phase){
 if(phase===0||phase===2)return a.clone();
 const s=phase===1?1:-1;
 if(id==='pebble-gecko'){
  // Opposing limb pairs travel in opposite phases; the tail tip bends separately.
  const b=warp(a,(x,y)=>{
   if(y>=24)return [x+s,y];
   if(x>=22&&y>=14&&y<=18)return [x,y+s];
   if(x<=10&&y>=19&&y<=24)return [x,y-s];
   if(x<=10&&y>=12&&y<=18)return [x+s,y];
   if(x>=15&&x<=19&&y>=17&&y<=22)return [x-s,y];
   return [x,y];
  });
  // Explicit joint cells reconnect the moved tail and opposing toes to the trunk.
  if(phase===1){b.p(5,23,'#627247');b.p(19,19,'#25382c');}
  else b.p(7,19,'#25382c');
  return b;
 }
 if(id==='button-snail'){
  const b=warp(a,(x,y)=>y>=25?[x+(y===27?s:0),y]:[x,y]);
  // The shell is unchanged. Only the foot wave and paired eyestalk tips move.
  return shiftPart(b,[23,19,28,23],s,0);
 }
 if(id==='isopod'||id==='stag-beetle'){
 const b=warp(a,(x,y)=>{
  const left=id==='isopod'?10:10,right=id==='isopod'?21:20;
  if(y>18&&(x<left||x>right))return [x,y+((y%4<2?1:-1)*(x<16?s:-s))];
  if(id==='stag-beetle'&&y<16)return [x+(x<16?s:-s),y];
  return [x,y];
 });
 if(id==='stag-beetle'&&phase===1)b.p(9,28,'#263138');
 return b;
 }
 if(id==='springtail')return warp(a,(x,y)=>[x,y-(phase===1?3:1)]);
 if(id==='tree-frog'){
 const b=warp(a,(x,y)=>{
  if(phase===1)return [x,y-(y<21?4:2)];
  return [x,y+(y<20?1:0)];
 });
 if(phase===1){b.rect(10,17,20,17,'#203d30');b.rect(11,17,19,17,'#dae6a0');b.rect(9,18,21,18,'#203d30');b.rect(10,18,20,18,'#50a46e');}
 return b;
 }
 if(id==='cherry-shrimp')return warp(a,(x,y)=>{
  if(x<=8&&y>=22)return [x+s,y];
  if(y>=23&&x>=8&&x<=16)return [x+s,y];
  if(x>=21&&y<=16)return [x,y+s];
  return [x,y];
 });
 if(id==='guppy'||id==='cory-catfish'){
  const b=a.clone(),ink=id==='guppy'?'#283e5b':'#333f43',mid=id==='guppy'?'#518faf':'#8d9c99',lit=id==='guppy'?'#9ed4d3':'#c4ccc0';
  b.rect(0,13,8,25,null);
  // Deliberately drawn narrow/open tail fans stay attached at the peduncle.
  const shape=phase===1?[[9,18],[5,15],[4,16],[4,21],[5,22],[9,20]]:[[9,18],[3,13],[2,14],[2,23],[3,24],[9,20]];
  b.polygon(shape,ink);b.polygon(phase===1?[[8,18],[5,17],[5,20],[8,20]]:[[8,18],[3,15],[3,22],[8,20]],mid);
  b.line(phase===1?5:3,17,phase===1?5:3,20,lit);return b;
 }
 if(id==='mangrove-crab')return warp(a,(x,y)=>{
  if(y>=23&&(x<=10||x>=21))return [x,y+(x<16?s:-s)];
  if(y<19&&(x<=9||x>=22))return [x,y-(x<16?s:-s)];
  return [x,y];
 });
 throw Error(id);
}
export async function makeCritters(){
 const entries=JSON.parse(fs.readFileSync(path.join(repo,'assets/review/idle-collection-v1/manifest.json'))).assets.filter(e=>e.kind==='animal').map(e=>({...e,idle:loadProject(path.join(repo,e.source)).frames[0]}));
 const crab=new Pixels(32,32);crab.stamp(3,11,[
 '..oo................oo....','..omo..............omo....','.ommmo............ommmo...',
 '.omlmo............omlmo...','..olmo..oo..oo....omlo.....','...omo..oe..eo...omo......','....omooommmmoooomo.......',
 '.....omllllllllmo.........','....omllhhhhllllmo........','...omlllhhhhllllmmo.......','....omllllllllllmo........',
 '..ooommmmmmmmmmmmoo.......','.omo.oommmmmmmmoo.omo.....','..omo..oooooooo..omo......','.omo..............omo.....','..oo..............oo......'
 ],{o:'#463340',m:'#b35f49',l:'#e9995e',h:'#f3c783',e:'#171d26'});
 entries.push({slug:'mangrove-crab',label:'Mangrove Crab',idle:crab,role:'New paludarium visual proposal',notes:'Stylized amphibious crab study; not a precise species identification or salinity/housing recommendation.'});
 const cat=new Pixels(32,32);cat.stamp(3,13,[
 '...........ooo............','..........olhmo...........','..oo.....olhmmmo..........','.omlo..oolhllllmoo........',
 'omhlmoomlllhhhhllmoo......','omhlmmmlllhhhhlllemmo.....','omhlmmmddddddddddlmmo.....','omhlmoomllhhhhllllmmo.....',
 '.omlo...omllllllllmoo.....','..oo.....ooommmooo........','...........olmo....o.o....','............oo............'
 ],{o:'#333f43',d:'#657479',m:'#8d9c99',l:'#c4ccc0',h:'#eee3bb',e:'#182227'});
 cat.line(23,21,25,23,'#333f43');cat.line(22,21,23,23,'#333f43');
 entries.push({slug:'cory-catfish',label:'Cory Catfish',idle:cat,role:'New aquarium visual proposal',notes:'Original small bottom-swimmer study. Stylized observation scale; exact species/care requirements remain separate.'});
 const result=[],rasters={};
 for(const e of entries){const frames=Array.from({length:4},(_,i)=>move(e.idle,e.slug,i)),ticks=e.slug==='button-snail'?[18,18,18,18]:e.slug==='springtail'?[12,4,8,6]:e.slug==='tree-frog'?[14,6,10,8]:[8,8,8,8];
  result.push(await saveAsset(e.slug,e.label,'critter',frames,{idleRGBA:hash(e.idle.rgba()),stillSource:e.source||null,role:e.role,movement:e.slug==='guppy'||e.slug==='cory-catfish'?'swim':e.slug==='button-snail'?'glide':e.slug==='tree-frog'||e.slug==='springtail'?'hop':e.slug==='cherry-shrimp'?'swim/paddle':'crawl/scuttle',notes:e.notes||'Original species-specific motion study.'},ticks));rasters[e.slug]=frames;
 }
 return {result,rasters};
}
