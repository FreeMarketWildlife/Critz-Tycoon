// Original integer-pixel material studies. Deterministic variants, never runtime noise.
import {Raster} from '../raster.mjs';
export const terrainPalette = {
 grass:['#8bc77a','#82bd72','#75ae68','#689d60','#a1d487','#b4df91'],
 sward:['#7eb76d','#75ad65','#689e5d','#619158','#94c77a','#a4d285'],
 path:['#dfc28d','#d9bb85','#c5a474','#e7cc98','#eed7a7','#af9369'],
};
const G=terrainPalette.grass,D=terrainPalette.path;
const mod=(v,n)=>(v%n+n)%n;
function stamp(r,rows,x,y,palette){rows.forEach((row,j)=>[...row].forEach((v,i)=>{if(v!=='.')r.dot(x+i,y+j,palette[Number(v)]);}));}
// Wide connected leaf clusters carry the texture; single pixels only finish tips.
export function meadow(v=0){
 const r=new Raster(32,32);r.rect(0,0,32,32,G[0]);
 for(const [a,b,n] of [[4,6,0],[21,13,1],[10,24,2]]){
  const x=2+mod(a+v*7+n*3,22),y=3+mod(b+v*11+n,23);
  stamp(r,['..11....','111111..','.1111111','..1111..'],x,y,G);
  if((v+n)%3!==0)stamp(r,['..4...','4.24..','.242..','..22..','...1..'],x+1,y-2,G);
  else stamp(r,['.4.4.','42224','.222.','..1..'],x,y-1,G);
 }
 // Occasional low, spreading clover; avoid an identical bright tuft in every cell.
 if(v%4===0)stamp(r,['.44.44.','4422444','.42224.','..222..','...1...'],21,24,G);
 return r;
}
function inside(x,y,m){
 const east=x>=16,south=y>=16,dx=east?31-x:x,dy=south?31-y:y;
 const vx=!!(m&(east?2:8)),vy=!!(m&(south?4:1)),diag=!!(m&(south?(east?32:64):(east?16:128)));
 if(!vx&&!vy)return dx>=6&&dy>=6&&((dx-11)**2+(dy-11)**2<=36||dx>=11||dy>=11);
 if(!vx)return dx>=6;if(!vy)return dy>=6;
 if(!diag&&dx<6&&dy<6)return dx*dx+dy*dy>=36;
 return true;
}
export function trail(mask,v=0){
 const r=meadow(v),dirt=new Raster(32,32);dirt.rect(0,0,32,32,D[0]);
 // Compressed sand and low mineral plates, not a grid of identical speckles.
 for(const [a,b] of [[3,6],[17,20],[27,12]]){
  const x=mod(a+v*9,27),y=mod(b+v*5,28);
  stamp(dirt,['..11....','111111..','.1111111','...111..'],x,y,D);
  stamp(dirt,['..333.','.30003','..000.'],x-1,y-2,D);
 }
 for(const [a,b]of (v===3?[[8,15],[24,28]]:v===1?[[24,28]]:[])){const x=mod(a+v*3,27)+1,y=mod(b+v*7,27)+2;stamp(dirt,['.33.','3223','.55.'],x,y,D);}
 const sample=(x,y)=>inside(Math.max(0,Math.min(31,x)),Math.max(0,Math.min(31,y)),mask);
 for(let y=0;y<32;y++)for(let x=0;x<32;x++)if(inside(x,y,mask)){
  const near=n=>!sample(x-n,y)||!sample(x+n,y)||!sample(x,y-n)||!sample(x,y+n);
  const i=(y*32+x)*4;r.p.set(dirt.p.subarray(i,i+4),i);
  // Thin earth lip and small grass teeth give the verge a worn, living outline.
  if(near(1))r.dot(x,y,D[2]);
  else if(near(2))r.dot(x,y,((x+y)%7<3)?D[1]:D[0]);
  if(near(2)&&((x*3+y*5)%17<3))r.dot(x,y,G[2]);
  else if(near(3)&&((x*3+y*5)%17===2))r.dot(x,y,G[4]);
 }
 return r;
}
// Connected patches of deeper turf: a shared edge bank, not isolated tile stamps.
function turfInside(x,y,m){
 const east=x>=16,south=y>=16,dx=east?31-x:x,dy=south?31-y:y;
 const vx=!!(m&(east?2:8)),vy=!!(m&(south?4:1)),diag=!!(m&(south?(east?32:64):(east?16:128)));
 if(!vx&&!vy)return dx>=3&&dy>=3&&((dx-15)**2+(dy-15)**2<=144||dx>=15||dy>=15);
 if(!vx)return dx>=3;if(!vy)return dy>=3;
 if(!diag&&dx<12&&dy<12)return dx*dx+dy*dy>=144;
 return true;
}
export function sward(mask,v=0){
 const r=meadow(v+5),base=meadow(v*5+2),colors=new Map(G.map((c,i)=>[c,terrainPalette.sward[i]]));
 const sample=(x,y)=>turfInside(Math.max(0,Math.min(31,x)),Math.max(0,Math.min(31,y)),mask);
 for(let y=0;y<32;y++)for(let x=0;x<32;x++)if(turfInside(x,y,mask)){
  const i=(y*32+x)*4,c='#'+base.p.subarray(i,i+3).toString('hex');r.dot(x,y,colors.get(c)||c);
  const edge=!sample(x-1,y)||!sample(x+1,y)||!sample(x,y-1)||!sample(x,y+1);
  if(edge)r.dot(x,y,(x+y)%5<2?G[0]:G[1]);
  else if(!sample(x-2,y)||!sample(x+2,y)||!sample(x,y-2)||!sample(x,y+2))r.dot(x,y,G[1]);
 }
 return r;
}
export function appendTerrain({group,add,ids}){
 group('Meadow revision · sixteen clustered turf variations');
 for(let v=0;v<16;v++)add(`meadow.grass.${v}`,meadow(v),'ground');
 const masks=[...ids.values()].filter(t=>t.id.startsWith('path.')&&t.neighborMask!==undefined).map(t=>t.neighborMask);
 group('Worn golden trails · all 47 edge shapes in four material variations');
 for(let v=0;v<4;v++)for(const mask of masks){const id=add(`meadow.path.${mask}.${v}`,trail(mask,v),'ground');Object.assign(ids.get(id),{terrain:'path',neighborMask:mask,variant:v});}
 group('Connected turf islands · two variations of all 47 shapes');
 for(let v=0;v<2;v++)for(const mask of masks){const id=add(`meadow.sward.${mask}.${v}`,sward(mask,v),'ground');Object.assign(ids.get(id),{terrain:'sward',neighborMask:mask,variant:v});}
}
