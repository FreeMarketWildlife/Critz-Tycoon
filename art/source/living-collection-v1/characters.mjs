import fs from 'node:fs';import path from 'node:path';
import {Pixels,repo,loadProject,saveAsset,hash} from './pixels.mjs';
const INK='#201008',CREAM='#f7edcc';
const list=JSON.parse(fs.readFileSync(path.join(repo,'assets/review/idle-collection-v1/manifest.json'))).assets.filter(e=>e.kind==='character');
list.unshift({slug:'hero-boy',label:'Boy Hero V1',source:'art/source/hero-boy-v1/idle.sprite.json',notes:'Child'});
function dominant(a,box,exclude=[]){const counts=new Map();for(let y=box[1];y<box[3];y++)for(let x=box[0];x<box[2];x++){const c=a.get(x,y);if(c&&!exclude.includes(c))counts.set(c,(counts.get(c)||0)+1);}return [...counts].sort((a,b)=>b[1]-a[1])[0]?.[0]||INK;}
function traits(a,e){const adult=/Adult/.test(e.notes||''),coats={mom:'#ba7082','professor-nugget':CREAM,'aunt-ember':'#506b82','dr-fern':CREAM,juniper:'#69895d',mina:CREAM,ollie:'#358b95','rival-boy':'#d7a541','rival-girl':'#786eaf'};return {adult,cut:adult?43:45,eyes:adult?36:38,skin:dominant(a,[11,40,22,43],[INK,CREAM]),hair:dominant(a,[5,26,27,34],[INK,CREAM]),shirt:coats[e.slug]||dominant(a,[10,48,22,53],[INK]),coat:!!coats[e.slug],pants:dominant(a,[9,55,22,58],[INK]),shoe:dominant(a,[9,59,14,61],[INK]),light:CREAM};}
function frontStride(idle,t,right){
 const a=new Pixels(),rear=right?[7,57,15,62]:[17,57,25,62],front=right?[17,57,25,62]:[7,57,15,62];
 a.blit(idle,right?2:-2,-2,rear);
 const armRear=right?[23,t.cut,29,55]:[3,t.cut,9,55];a.blit(idle,0,-2,armRear);
 a.blit(idle,0,2,[0,0,32,t.cut]);a.blit(idle,0,2,[9,t.cut,23,55]);
 // Shoulder attachment follows torso, while the hand on that side recedes.
 a.blit(idle,0,2,[7,t.cut,25,t.cut+2]);
 for(let y=57;y<=59;y++){const l=y===57?10:y===58?11:12;a.rect(l,y,31-l,y,INK);if(y<59)a.rect(l+1,y,30-l,y,t.pants);}a.rect(15,58,16,59,INK);
 a.blit(idle,right?-2:2,2,front);a.rect(right?17:11,57,right?20:14,58,t.pants);
 a.blit(idle,0,2,right?[3,t.cut,9,55]:[23,t.cut,29,55]);
 a.blit(idle,0,2,right?[5,t.cut,11,t.cut+3]:[21,t.cut,27,t.cut+3]);
 return a;
}
function back(idle,t,e){
 const a=idle.clone(),slug=e.slug;
 // All face pixels become the rear cranium/hair. Clothing retains the native body.
 const hairPalette=['#28252b','#3b3030','#594333'];
 if(slug==='professor-nugget')hairPalette.splice(0,3,'#798987','#a8b4af','#d2d7c8');
 for(let y=t.eyes-5;y<t.cut;y++)for(let x=3;x<=28;x++)if(a.get(x,y)){
  if(slug==='kaid')a.p(x,y,y>t.eyes?'#dca444':'#69a9ae');
  else if(y>=t.cut-2&&x>=11&&x<=20)a.p(x,y,t.skin);
  else a.p(x,y,(x<7||x>24||y===t.cut-1)?INK:hairPalette[x<12?2:x>23?0:1]);
 }
 // Back contours retain the outer one-cell boundary, no floating eyes or glasses.
 for(let y=t.eyes-5;y<t.cut;y++)for(let x=3;x<=28;x++)if(a.get(x,y)&&(!idle.get(x-1,y)||!idle.get(x+1,y)||!idle.get(x,y+1)))a.p(x,y,slug==='kaid'?'#366d75':INK);
 if(slug!=='kaid')for(const x of [8,12,17,22])for(let y=t.eyes-5+x%3;y<t.cut-3;y++)if(a.get(x,y)&&a.get(x,y)!==INK)a.p(x,y,hairPalette[x<16?1:0]);
 // Original back garments: no front lapels, badges or aprons copied through the body.
 for(let y=t.cut;y<=54;y++)for(let x=9;x<=22;x++)if(a.get(x,y)&&a.get(x,y)!==INK){
  if(['hero-boy','hero-girl'].includes(slug))continue;
  a.p(x,y,t.shirt);
 }
 if(slug==='aunt-ember'){a.line(11,45,20,51,'#7998a3');a.line(20,45,11,51,'#7998a3');}
 if(slug==='kaid'){
  // A 180° turn swaps the screen positions of the physical handle and spout.
  const b=a.clone();for(let y=24;y<t.cut;y++)for(let x=0;x<32;x++)a.p(x,y,b.get(31-x,y));
 }
 return a;
}
function profile(idle,t,e,east){
 const a=new Pixels(),dir=east?1:-1,eyeX=east?21:10,cy=t.eyes;
 // Authored side body and limb overlap. Back arm lies behind torso.
 a.rect(13,t.cut-1,20,t.cut+1,INK);a.rect(14,t.cut-1,19,t.cut,t.skin);
 for(let y=t.cut+1;y<=55;y++){
  const l=y===t.cut+1?11:y===t.cut+2?10:y>=54?10:9,r=y===t.cut+1?21:y>=54?22:23;
  a.rect(l,y,r,y,INK);
  const sample=idle.get(15,Math.min(y,53));a.rect(l+1,y,r-1,y,!t.coat&&sample&&sample!==INK?sample:t.shirt);
 }
 a.rect(10,55,23,58,INK);a.rect(11,55,22,57,t.pants);
 a.rect(11,58,22,60,INK);a.rect(12,58,21,59,t.pants);a.rect(10,60,23,61,INK);a.rect(11,60,22,60,t.shoe);
 a.rect(east?12:16,t.cut+3,east?17:21,53,INK);a.rect(east?13:17,t.cut+3,east?16:20,t.cut+5,t.shirt);a.rect(east?13:17,t.cut+6,east?16:20,53,t.skin);
 const headTop=Math.min(...idle.a.flatMap((c,i)=>c?[Math.floor(i/32)]:[]));
 // The side crown follows the original height and hair palette; this is a new view,
 // not a resized front face. Row widths are authored independently.
 for(let y=Math.max(headTop,t.cut-21);y<t.cut;y++){
  const k=y-(t.cut-21),l=k<2?12:k<4?9:k<7?7:k<16?6:k<19?8:11,r=31-l;
  for(let x=l;x<=r;x++)a.p(x,y,(x===l||x===r||y===t.cut-1)?INK:t.hair);
 }
 // Skin plane projects forward to the small nose; one eye is visible in profile.
 const face=[[15,cy-4],[22,cy-3],[24,cy],[24,cy+1],[26,cy+2],[25,cy+4],[22,t.cut-1],[14,t.cut-1],[12,cy+2]];
 const transform=pts=>pts.map(([x,y])=>[east?x:31-x,y]);
 a.polygon(transform(face),INK);
 a.polygon(transform([[16,cy-3],[21,cy-2],[23,cy],[23,cy+2],[25,cy+2],[24,cy+3],[21,t.cut-2],[15,t.cut-2],[13,cy+2]]),t.skin);
 a.rect(eyeX,cy,eyeX+1,cy+3,INK);a.p(eyeX,cy,CREAM);
 a.rect(east?14:16,cy+1,east?15:17,cy+3,INK);a.p(east?15:16,cy+2,t.skin);
 // Crown material detail is projected from the correct side without reversing RGB.
 for(let y=Math.max(headTop,t.cut-21);y<cy-2;y++)for(let x=8;x<24;x++)if(a.get(x,y)&&a.get(x,y)!==INK){const c=idle.get(east?x:31-x,y);if(c)a.p(x,y,c);}
 if(['hero-girl','mom','aunt-ember','mina'].includes(e.slug)){
  // Side views show the nearer puff/bun, with its actual native color clusters.
  const paired=e.slug==='hero-girl'||e.slug==='mom';
  a.blit(idle,paired?(east?5:-5):(east?-2:2),0,[paired?(east?3:19):11,headTop,paired?(east?13:29):21,Math.min(31,cy-4)]);
 }
 if(e.slug==='professor-nugget'){a.blit(idle,0,0,[3,headTop,29,33]);a.rect(east?20:8,cy-1,east?24:12,cy-1,'#293445');a.rect(east?24:8,cy,east?24:8,cy+3,'#293445');a.rect(east?20:8,cy+4,east?24:12,cy+4,'#293445');}
 if(e.slug==='kaid'){
  a.rect(0,0,31,44,null);a.polygon([[9,28],[23,28],[23,40],[20,44],[12,44],[8,40],[8,29]],'#163a43');a.rect(9,29,22,39,'#69a9ae');a.rect(10,35,21,40,'#df9f3a');a.rect(12,41,19,42,'#69a9ae');a.rect(10,30,11,33,'#e6f1d8');a.rect(9,28,22,28,'#a5d7d0');a.rect(13,43,20,44,'#163a43');
  // Handle is near in west profile, spout near in east. Never use a blind flip.
  if(east){a.stamp(21,27,['oooo.','mhhmo','mmmo.','ooo..'],{o:'#163a43',m:'#69a9ae',h:'#e6f1d8'});a.rect(21,36,22,39,INK);a.p(21,36,CREAM);}
  else {a.stamp(7,31,['.oooo.','omhhmo','om..mo','om..mo','om..mo','omhhmo','.oooo.'],{o:'#163a43',m:'#69a9ae',h:'#e6f1d8'});a.rect(10,36,11,39,INK);a.p(10,36,CREAM);}
 }
 return a;
}
function sideStride(idle,t,east,phase){
 const a=new Pixels(),s=(phase?1:-1)*(east?1:-1);
 // Rear leg, body bob, opposing near arm, forward leg/foot with actual separation.
 a.rect(13-s*3,55,16-s*3,60,INK);a.rect(14-s*3,56,15-s*3,59,t.pants);a.rect(12-s*3,60,17-s*3,61,t.shoe);
 a.blit(idle,0,2,[0,0,32,55]);
 a.rect(14+s*3,57,18+s*3,62,INK);a.rect(15+s*3,57,17+s*3,61,t.pants);a.rect(13+s*3,62,19+s*3,63,INK);a.rect(14+s*3,62,18+s*3,62,t.shoe);
 a.rect(15-s*2,t.cut+5,18-s*2,55,INK);a.rect(16-s*2,t.cut+5,17-s*2,54,t.skin);
 return a;
}
export async function makeCharacters(){const result=[];
 for(const e of list){const idle=loadProject(path.join(repo,e.source)).frames[0],t=traits(idle,e),poses=[];
  const north=back(idle,t,e),west=profile(idle,t,e,false),east=profile(idle,t,e,true);
  let south=[frontStride(idle,t,true),idle,frontStride(idle,t,false),idle.clone()];
  if(e.slug==='hero-boy')south=loadProject(path.join(repo,'art/source/hero-boy-v1/walk.sprite.json')).frames;
  poses.push(...south,frontStride(north,t,false),north,frontStride(north,t,true),north.clone(),sideStride(west,t,false,true),west,sideStride(west,t,false,false),west.clone(),sideStride(east,t,true,true),east,sideStride(east,t,true,false),east.clone());
  result.push(await saveAsset(e.slug,e.label,'character',poses,{directions:['south','north','west','east'],directionRanges:{south:[0,4],north:[4,8],west:[8,12],east:[12,16]},sequence:['strideA','passing','strideB','passing'],frontIdleRGBA:hash(idle.rgba()),headBobPixels:2,stillSource:e.source,scope:'Four original directional walk cycles; original front idle retained exactly. Back/profile drawings are new review proposals, not approved likenesses.'}));
 }
 return result;
}
