// Original character redraws in the existing editable native-pixel workflow.
// Internal PNG row indices run down; review Y labels run UP from the bottom.
import {writeFile,readFile} from 'node:fs/promises';
import {createRequire} from 'node:module';
import assert from 'node:assert/strict';
import {Raster} from '../../../../art/source/raster.mjs';
const require=createRequire(import.meta.url);
const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const dir=new URL('./',import.meta.url);
const specs=[
 {slug:'a-afro',title:'A · Rounded afro',outfit:'Teal / cream / navy',top:27,left:[12,9,7,5,4,4,5,5,6],colors:['#398c99','#245966','#63aab0','#245966']},
 {slug:'b-flat-top',title:'B · Flat-top',outfit:'Gold vest / cream shirt',top:27,left:[7,6,6,6,6,6,6,6,7],colors:['#c09838','#866426','#e2be5b','#c09838']},
 {slug:'c-twists',title:'C · Short twists',outfit:'Red stripes / navy shorts',top:28,left:[11,8,6,5,4,4,5,6],colors:['#d35b49','#943d37','#ed8a6d','#d35b49']},
 {slug:'d-cornrows',title:'D · Cornrows',outfit:'Blue jacket / olive shorts',top:29,left:[11,8,6,5,5,6,7],colors:['#397fb8','#254e79','#75acd0','#73774a']},
];
const models=[];
for(let v=0;v<4;v++){
 const s=specs[v];const palette={O:'#171c24',H:'#2b2826',J:'#46382f',V:'#665040',S:'#70412f',M:'#a76740',L:'#c88a57',C:s.colors[0],D:s.colors[1],A:s.colors[2],W:'#f2e9cb',K:'#b6b69a',N:'#27364c',P:'#405573',Q:s.colors[3]};
 const rows=Array.from({length:64},()=>Array(32).fill('.'));
 const parts=Array.from({length:64},()=>Array(32).fill('.'));
 const skull=Array.from({length:64},()=>Array(32).fill(0));
 const dot=(x,y,k,p)=>{rows[y][x]=k;if(p)parts[y][x]=p;};
 const rect=(x,y,w,h,k,p)=>{for(let j=y;j<y+h;j++)for(let i=x;i<x+w;i++)dot(i,j,k,p);};
 const span=(y,l,r,k,p)=>rect(l,y,r-l+1,1,k,p);
 const pair=(x,y,k,p,other=k)=>{dot(x,y,k,p);dot(31-x,y,other,p);};
 const boxes=(x,y,w,h,k,p)=>{rect(x,y,w,h,k,p);rect(32-x-w,y,w,h,k,p);};
 // Symmetric original skull construction. The crown is NOT measured through a hat.
 const faceLeft={30:12,31:9,32:8,33:7,34:7,35:7,36:7,37:6,38:6,39:5,40:4,41:5,42:6,43:7,44:8,45:10};
 for(const [ys,l]of Object.entries(faceLeft)){
  const y=Number(ys);for(let x=l;x<=31-l;x++){
   skull[y][x]=1;dot(x,y,x===l||x===31-l||y===45?'S':y<40&&x<20?'L':'M','face');
  }
 }
 // Short rounded ears; upper attachment and lower corners mirror precisely.
 for(let y=36;y<=40;y++){
  const l=4;
  for(let x=l;x<=6;x++)pair(x,y,x===l||y===40?'S':x===l+1?'L':'M','ears',x===l||y===40?'S':'M');
 }
 // Two connected cheek planes and a compact rounded jaw, not a long nose stripe.
 span(40,8,23,'M','face');span(41,8,23,'M','face');
 span(42,9,22,'M','face');span(43,10,21,'M','face');span(44,12,19,'M','face');
 rect(8,37,3,3,'L','face');rect(21,37,3,3,'M','face');
 boxes(12,38,2,4,'O','eyes');
 // Neck overlap: dark horizontal contact beneath the jaw; no visible tall neck.
 span(46,10,21,'O','neck');span(45,12,19,'S','neck');
 // Narrower, rounded garment with clear dark arm/torso separation.
 const torsoLeft={47:9,48:9,49:9,50:9,51:9,52:9,53:10,54:10,55:10};
 for(const [ys,l]of Object.entries(torsoLeft)){
  const y=Number(ys);span(y,l,31-l,'O','torso');
  for(let x=l+1;x<31-l;x++)dot(x,y,x===30-l||y>=54?'D':'C','torso');
 }
 span(47,12,19,'C','torso');span(48,12,19,'C','torso');
 // Sleeves sit down beside the body, not a broad horizontal arm bar.
 for(const [y,l,r]of [[46,8,9],[47,6,8],[48,5,8],[49,5,8],[50,4,7]]){
  for(let x=l;x<=r;x++)pair(x,y,x===l?'O':x===r?'K':'W','arms',x===l?'O':'K');
 }
 // Rounded hanging hands, including a one-pixel warm outline.
 for(const [y,l,r]of [[50,4,6],[51,3,7],[52,3,7],[53,4,6]]){
  for(let x=l;x<=r;x++)pair(x,y,x===l||x===r||y===53?'S':y===50?'L':'M','hands',x===l||x===r||y===53?'S':'M');
 }
 // Dark sleeve/torso overlap keeps the hands attached in a compact idle.
 for(const [y,l,r]of [[50,8,8],[51,8,8],[52,8,8],[53,7,9]])for(let x=l;x<=r;x++)pair(x,y,'O','underarm');
 // Ink below/inside hands gives separation without widening the anatomy.
 pair(7,52,'O','hands');pair(4,53,'O','hands');pair(6,53,'S','hands');
 for(const [x,y]of [[10,48],[10,49],[11,50],[11,51]])dot(x,y,'A','torso');
 // Shorts begin below the hem; separate feet, with a small two-pixel central gap.
 span(55,10,21,'O','hips');span(56,9,22,'O','hips');
 boxes(9,56,6,2,'N','legs');boxes(10,56,4,1,'P','legs');
 boxes(9,58,6,1,'O','legs');boxes(10,58,4,1,'M','legs');
 for(const [y,l,r]of [[59,9,14],[60,9,14],[61,10,13]]){
  for(let x=l;x<=r;x++)pair(x,y,y===61||x===l||x===r?'O':'W','feet');
 }
 boxes(10,59,2,1,'Q','feet');boxes(12,59,1,1,'W','feet');
 const anatomyParts=parts.map(r=>r.join(','));
 for(let y=0;y<64;y++)for(let x=0;x<16;x++)assert.equal(parts[y][x],parts[y][31-x],`${s.slug} base anatomy ${x},${y}`);
 // Hair now stops well below the old hat-height y20. No resizing of the old rows.
 for(let i=0;i<s.left.length;i++){
  const y=s.top+i,l=s.left[i];span(y,l,31-l,'O','hair');
  for(let x=l+1;x<31-l;x++)dot(x,y,'H','hair');
 }
 if(v===0){
  for(const [x,y,w]of [[11,28,5],[8,29,4],[6,31,4],[17,29,4],[20,31,3],[9,32,3]])rect(x,y,w,1,'J','hair');
  for(const [y,l,r]of [[29,10,15],[30,8,12],[31,6,9],[31,12,14],[32,5,7],[32,10,12],[33,6,8],[30,19,22],[32,22,24]])span(y,l,r,'J','hair');
  rect(12,28,2,1,'V','hair');rect(8,30,2,1,'V','hair');
  // Low curved hairline; central forehead starts at native row36.
  pair(6,36,'H','hair');pair(7,36,'O','hair');
  pair(5,35,'H','hair');pair(8,35,'S','hair');
 }
 if(v===1){
  for(const [x,y,w]of [[8,28,2],[12,28,2],[17,28,2],[21,28,2],[10,30,2],[16,30,2],[20,30,2]])rect(x,y,w,1,'J','hair');
  rect(8,28,1,1,'V','hair');rect(17,28,1,1,'V','hair');
  pair(7,36,'H','hair');pair(7,37,'O','hair');
 }
 if(v===2){
  for(const [x,y,w]of [[11,29,4],[8,30,3],[17,30,3],[6,32,3],[21,32,3]])rect(x,y,w,1,'J','hair');
  // Small scalp gaps and hanging locks; the face stays compact below them.
  for(const x of[9,13,18,22])rect(x,34,1,2,'M','hair');
  for(const [x,len]of [[6,4],[10,3],[15,4],[20,3],[24,4]]){
   rect(x,33,2,len,'H','hair');rect(x,34,1,len-1,'J','hair');dot(x+1,33+len,'O','hair');
  }
 }
 if(v===3){
  // Curved braided lanes over a smaller crown, with subdued warm scalp channels.
  for(let y=31;y<35;y++)for(let x=s.left[y-s.top]+1;x<31-s.left[y-s.top];x++)dot(x,y,y<33?'M':'S','hair');
  for(const [x,len]of [[7,3],[11,4],[15,5],[19,4],[23,3]])for(let i=0;i<len;i++){
   const xx=x+(x<10?Math.floor(i/2):x>22?-Math.floor(i/2):0),y=30+i;
   rect(xx,y,2,1,i%2===0?'J':'H','hair');
  }
  pair(7,35,'H','hair');pair(7,36,'O','hair');
 }
 // Original reference-concept costumes retain their identifying arrangements.
 if(v===1||v===3){
  rect(14,47,4,6,'W','torso');rect(14,52,4,1,'K','torso');
  boxes(12,47,1,5,'A','torso');boxes(13,48,1,5,'D','torso');
  pair(11,53,'D','torso');pair(12,53,'C','torso');
  if(v===3){
   for(let y=46;y<=50;y++)for(let x=0;x<32;x++)if(parts[y][x]==='arms'&&rows[y][x]!=='O')rows[y][x]=x<16?'C':'D';
   boxes(7,47,1,2,'A','arms');
   for(let y=55;y<=57;y++)for(let x=0;x<32;x++)if(['legs','hips'].includes(parts[y][x])&&rows[y][x]!=='O')rows[y][x]=y===56?'Q':'D';
   boxes(10,56,2,1,'K','legs');boxes(10,59,2,1,'C','feet');
  }
 }
 if(v===2){
  for(const y of[48,51])for(let x=11;x<=20;x++)dot(x,y,'W','torso');
  for(let y=46;y<=50;y++)for(let x=0;x<32;x++)if(parts[y][x]==='arms'&&rows[y][x]!=='O')rows[y][x]=y===48?'W':x<16?'C':'D';
  span(47,13,18,'D','torso');
 }
 // Hair is an explicit overlay; all visible non-hair anatomy below it must mirror.
 for(let y=0;y<64;y++)for(let x=0;x<16;x++){
  assert.equal(skull[y][x],skull[y][31-x]);
  if(y>=38)assert.equal(parts[y][x],parts[y][31-x],`${s.slug} anatomy ${x},${y}`);
 }
 const r=new Raster(32,64);const xs=[],ys=[];
 for(let y=0;y<64;y++)for(let x=0;x<32;x++)if(rows[y][x]!=='.'){r.dot(x,y,palette[rows[y][x]]);xs.push(x);ys.push(y);}
 const bbox=[Math.min(...xs),Math.min(...ys),Math.max(...xs)+1,Math.max(...ys)+1];
 const m={slug:s.slug,title:s.title,outfit:s.outfit,id:`review.hero.boy.south.idle.r6.${s.slug}`,status:'awaiting-user-art-review',frame:[32,64],anchor:[16,64],reviewCoordinates:{origin:'bottom-left',xMidpoint:16,yTop:64,yBottom:0,pngRowToGridCellBottom:'63 - row'},palette,rows:rows.map(r=>r.join('')),parts:parts.map(r=>r.join(',')),anatomyParts,skullMask:skull.map(r=>r.join('')),opaqueBBox:bbox,paintedSize:[bbox[2]-bbox[0],bbox[3]-bbox[1]],pose:'front-idle',animation:false,landmarks:{centralExposedFaceTopRow:36,eyes:[[12,38,14,42],[18,38,20,42]],footLastRow:61,skullConstructionTopRow:30},constructionNote:'The original hidden skull scaffold and hairstyle crowns are design choices, not measured through Brendan headwear. No y20 crown requirement.'};
 await r.save(new URL(s.slug+'.png',dir).pathname);await writeFile(new URL(s.slug+'.json',dir),JSON.stringify(m,null,2)+'\n');models.push(m);
}
const text=(x,y,t,size=18,extra='')=>`<text x="${x}" y="${y}" font-size="${size}" ${extra}>${t}</text>`;
const start=(w,h)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}"><rect width="${w}" height="${h}" fill="#faf7ef"/><g font-family="Arial,sans-serif" fill="#253438">`;
function cells(m,x,y,z){let a=[];m.rows.forEach((r,j)=>[...r].forEach((k,i)=>{if(k!=='.')a.push(`<rect x="${x+i*z}" y="${y+j*z}" width="${z}" height="${z}" fill="${m.palette[k]}"/>`);}));return a.join('');}
function panel(m,x,y,z){
 const w=32*z,h=64*z;let a=[text(x+w/2,y-61,m.title,23,'text-anchor="middle" font-weight="700"'),text(x+w/2,y-36,m.outfit,17,'text-anchor="middle"'),`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#edf0eb"/>`,cells(m,x,y,z)];
 for(let i=0;i<=32;i++)a.push(`<path d="M${x+i*z} ${y}v${h}" stroke="#58676a" stroke-opacity=".26"/>`);
 for(let row=0;row<=64;row++){
  const value=64-row,major=value%10===0||value===64;
  a.push(`<path d="M${x} ${y+row*z}h${w}" stroke="${major?'#476e80':'#58676a'}" stroke-width="${major?1.7:1}" stroke-opacity="${major?.8:.26}"/>`);
  if(major)a.push(text(x-10,y+row*z+5,''+value,16,'text-anchor="end"'));
 }
 for(const i of[0,10,16,20,30,32])a.push(text(x+i*z,y+h+21,''+i,13,'text-anchor="middle"'));
 a.push(`<path d="M${x+w/2} ${y-5}v${h+10}" stroke="#cc3c83" stroke-width="2"/>`);
 a.push(text(x+w/2,y+h+48,`${m.paintedSize.join(' × ')} painted · 32 × 64 canvas`,17,'text-anchor="middle"'));
 return a.join('');
}
const layouts={};
for(const [name,cols]of[['four-heroes-grid',4],['four-heroes-grid-2x2',2]]){
 const pw=450,ph=925,w=cols*pw+30,h=Math.ceil(4/cols)*ph+125;
 let svg=start(w,h)+text(48,42,'FOUR HERO DESIGNS · SHORTER HEAD CONSTRUCTION',27,'font-weight="700"')+text(48,75,'One square = one native pixel. Y increases upward: 0 at bottom, 64 at top.',20);
 layouts[name]=[];
 models.forEach((m,i)=>{const x=50+i%cols*pw,y=175+Math.floor(i/cols)*ph;svg+=panel(m,x,y,12);layouts[name].push({slug:m.slug,x,y,scale:12});});
 svg+='</g></svg>';await writeFile(new URL(name+'.svg',dir),svg);await sharp(Buffer.from(svg)).png().toFile(new URL(name+'.png',dir).pathname);
}
for(const m of models){const svg=start(480,975)+panel(m,50,95,12)+'</g></svg>';await sharp(Buffer.from(svg)).png().toFile(new URL(m.slug+'-grid.png',dir).pathname);}
let clean=start(1220,475)+text(32,38,'CLEAN PIXEL CHECK · SAME FOUR NATIVE DRAWINGS',24,'font-weight="700"');
models.forEach((m,i)=>{clean+=text(160+300*i,75,m.title,21,'text-anchor="middle"')+cells(m,32+300*i,-95,8);});
clean+='</g></svg>';await sharp(Buffer.from(clean)).png().toFile(new URL('clean-check.png',dir).pathname);
await writeFile(new URL('grid-layout.json',dir),JSON.stringify(layouts,null,2)+'\n');
console.log(models.map(m=>({id:m.id,bbox:m.opaqueBBox,painted:m.paintedSize})));
// Optional local-only comparison. Never write reference-colored artwork into the repo.
if(process.argv[2]&&process.argv[3]){
 const {resolve,relative}=await import('node:path');const {mkdir}=await import('node:fs/promises');
 const repo=resolve(new URL('../../../../',dir).pathname),output=resolve(process.argv[3]);
 assert.ok(relative(repo,output).startsWith('..'),'reference output must stay outside the project');
 await mkdir(output,{recursive:true});
 const reference=JSON.parse(await readFile(process.argv[2]));
 reference.title='BRENDAN · REFERENCE';reference.outfit='Supplied pixel reconstruction';reference.paintedSize=[26,42];
 let svg=start(2280,1050)+text(48,42,'REFERENCE + FOUR CORRECTED HERO DESIGNS',27,'font-weight="700"')+text(48,75,'Full 32 × 64 grids. Y counts upward from zero. Hair height is independent of hat height.',20);
 [reference,...models].forEach((m,i)=>svg+=panel(m,50+i*450,175,12));svg+='</g></svg>';
 await writeFile(output+'/brendan-and-four-grid.svg',svg);await sharp(Buffer.from(svg)).png().toFile(output+'/brendan-and-four-grid.png');
}
