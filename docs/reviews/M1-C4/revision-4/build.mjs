// Original native pixel sources, extending the project's editable raster workflow.
// No concept bitmap is resized or sampled into these assets.
import {writeFile} from 'node:fs/promises';
import {createRequire} from 'node:module';
import assert from 'node:assert/strict';
import {Raster} from '../../../../art/source/raster.mjs';
const require=createRequire(import.meta.url);
const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const dir=new URL('./',import.meta.url);
const variants=[
 {slug:'a-afro',title:'A · Rounded afro',outfit:'Teal shirt / cream sleeves',colors:['#338d97','#24616c','#60adb4','#28757c']},
 {slug:'b-flat-top',title:'B · Flat-top',outfit:'Gold vest / cream shirt',colors:['#c89b38','#8d662a','#ead06c','#c89b38']},
 {slug:'c-twists',title:'C · Short twists',outfit:'Red stripes / navy shorts',colors:['#df5545','#963d37','#f47b60','#d84b3c']},
 {slug:'d-cornrows',title:'D · Cornrows',outfit:'Blue jacket / olive shorts',colors:['#387cbd','#285185','#72a9d0','#727648']},
];
const models=[];
for(let v=0;v<4;v++){
 const spec=variants[v],palette={O:'#211f24',H:'#302a29',J:'#493a32',V:'#625047',S:'#70412f',M:'#a76640',L:'#c68653',C:spec.colors[0],D:spec.colors[1],A:spec.colors[2],W:'#f1ebcf',K:'#c4bc94',N:'#293746',P:'#47596b',Q:spec.colors[3]};
 const rows=Array.from({length:64},()=>Array(32).fill('.'));
 const parts=Array.from({length:64},()=>Array(32).fill('.'));
 const masks={};
 function dot(x,y,k,p){rows[y][x]=k;if(p)parts[y][x]=p;}
 function rect(x,y,w,h,k,p){for(let j=y;j<y+h;j++)for(let i=x;i<x+w;i++)dot(i,j,k,p);}
 function span(y,l,r,k,p){rect(l,y,r-l+1,1,k,p);}
 function pair(x,y,k,p,right=k){dot(x,y,k,p);dot(31-x,y,right,p);}
 function boxpair(x,y,w,h,k,p){rect(x,y,w,h,k,p);rect(32-x-w,y,w,h,k,p);}
 // Symmetric hidden skull scaffold, recorded independently of overlaid hair.
 for(let y=27;y<=45;y++){
  let l=y===27?11:y===28?8:y===29?7:y<42?6:y===42?7:y===43?8:y===44?9:11;
  for(let x=l;x<=31-l;x++){
   masks.skull??=Array.from({length:64},()=>Array(32).fill(0));masks.skull[y][x]=1;
   dot(x,y,x===l||x===31-l||y===45?'S':x<=17&&y<41?'L':'M','skull');
  }
 }
 // Small blunt ear tabs, three target pixels of projection, never tapered wings.
 for(let y=37;y<=40;y++){
  const l=y===37||y===40?5:4;
  for(let x=l;x<7;x++)pair(x,y,x===l?'S':y===38?'L':'M','ears',x===l?'S':'M');
 }
 // A restrained cheek plane; no pointed chin or long nose stripe.
 rect(7,39,3,3,'M');rect(22,38,3,4,'M');span(43,9,22,'M');span(44,11,20,'M');
 rect(15,41,2,1,'M');
 // Eyes: exact doubled reference rectangles, no white glints added to shape.
 boxpair(12,38,2,4,'O','eyes');
 // Neck and compact body beneath the large child head.
 rect(12,45,8,2,'S','neck');rect(14,45,4,1,'M','neck');
 for(let y=46;y<=54;y++)span(y,y===46?10:8,y===46?21:23,'C','torso');
 // Mirror sleeve and hand masks. Light direction changes color only.
 for(let y=47;y<=50;y++){
  const l=y===47?6:y===48?5:4;
  for(let x=l;x<=8;x++)pair(x,y,x===l?'K':'W','arms',x===l?'O':'K');
 }
 for(let y=50;y<=53;y++){
  const l=y===50?4:y===53?5:3,r=7;
  for(let x=l;x<=r;x++)pair(x,y,x===l||y===53?'S':y===50?'L':'M','hands',x===l||y===53?'S':'M');
 }
 // One-pixel dark separation at armpits and alongside the hem.
 for(let y=48;y<=54;y++){pair(8,y,'D','torso');pair(23,y,'D','torso');}
 for(let y=47;y<=51;y++)dot(10,y,'A');
 for(let y=48;y<=53;y++)dot(22,y,'D');
 span(54,9,22,'D','torso');span(55,8,23,'N','hips');
 boxpair(8,56,6,2,'N','legs');boxpair(8,56,5,1,'P','legs');
 // No long shins: ankle then two individually shaped sneakers.
 boxpair(9,58,5,1,'S','legs');
 for(let y=59;y<=61;y++){
  const l=y===59?8:7,r=y===61?13:14;
  for(let x=l;x<=r;x++)pair(x,y,y===61?'O':x===l||x===r?'O':'W','feet');
 }
 boxpair(9,59,2,2,'Q','feet');boxpair(11,59,2,1,'W','feet');
 // Hair silhouettes are separately authored in target pixels for each reference.
 const hairLeft=v===0?[12,9,7,5,4,3,3,2,2,3,3,4,4,5,6]:
 v===1?[7,5,5,5,5,5,5,5,5,5,6,6,6,7,7]:
 v===2?[10,7,5,4,3,2,2,3,3,3,4,4,5,5,6]:
 [11,8,6,5,4,3,3,3,4,4,5,5,6,6,7];
 for(let i=0;i<hairLeft.length;i++){
  const y=20+i,l=hairLeft[i];
  for(let x=l;x<=31-l;x++)dot(x,y,x===l||x===31-l||i===0?'O':'H','hair');
 }
 // Controlled hairline: round afro, crisp flat-top, hanging twists, braided scalp.
 if(v===0){
  for(const [y,l,r] of [[30,11,20],[31,9,22],[32,8,23],[33,7,24],[34,7,24]]){
   for(let x=l;x<=r;x++)dot(x,y,y===30?'S':x<18?'L':'M','skull');
  }
  for(const [x,y,w,h]of [[10,22,5,2],[7,24,4,2],[5,27,3,2],[16,23,4,2],[21,26,3,2],[8,28,3,2]])rect(x,y,w,h,'J');
  rect(11,22,3,1,'V');rect(7,25,2,1,'V');rect(18,24,2,1,'V');
  pair(5,35,'H','hair');pair(6,35,'O','hair');
 }
 if(v===1){
  for(let y=30;y<=34;y++)for(let x=8;x<=23;x++)dot(x,y,y===30?'S':x<18?'L':'M','skull');
  for(const [x,y,w,h]of [[7,21,3,2],[12,21,3,2],[18,21,3,2],[23,22,2,2],[9,24,3,2],[16,23,3,2],[21,25,3,2]])rect(x,y,w,h,'J');
  rect(8,21,2,1,'V');rect(13,21,2,1,'V');rect(19,21,2,1,'V');
  pair(7,31,'H','hair');pair(7,32,'H','hair');
 }
 if(v===2){
  for(let y=29;y<=35;y++)for(let x=7;x<=24;x++)dot(x,y,x<18?'L':'M','skull');
  // Five downward locks with one-pixel ends. Hair may overlap the symmetric skull.
  for(const [x,top,len]of [[5,26,10],[9,25,10],[14,24,11],[19,25,10],[24,27,9]]){
   rect(x,top,3,len-1,'H','hair');rect(x+1,top+1,1,len-3,'J','hair');
   dot(x+1,top+len-1,'O','hair');dot(x,top+len-2,'O','hair');
  }
  for(const [x,y,w]of [[10,21,4],[7,23,4],[17,22,4],[4,26,3],[21,24,3]])rect(x,y,w,2,'J');
  rect(8,23,2,1,'V');rect(18,22,2,1,'V');
 }
 if(v===3){
  // Warm scalp channels are surface detail, not cuts in the cranium.
  for(let y=23;y<=33;y++)for(let x=Math.max(hairLeft[y-20]+1,5);x<=Math.min(30-hairLeft[y-20],26);x++)dot(x,y,'M','hair');
  for(const [x0,len]of [[7,7],[11,9],[15,10],[19,9],[23,7]]){
   for(let i=0;i<len;i++){
    const y=21+i,x=x0+(x0<11?Math.floor(i/3):x0>21?-Math.floor(i/3):0);
    rect(x,y,2,1,i%3===0?'J':'H','hair');
   }
  }
  for(let y=31;y<=34;y++)for(let x=8;x<=23;x++)dot(x,y,x<18?'L':'M','skull');
  pair(6,34,'H','hair');pair(7,33,'H','hair');
 }
 // Reference-specific outfits, independent of the shared anatomical masks.
 if(v===1||v===3){
  rect(13,47,6,7,'W','torso');rect(14,46,4,1,'W','torso');
  rect(13,52,6,2,'K','torso');rect(14,52,4,2,'W','torso');
  boxpair(11,47,1,6,'A','torso');boxpair(12,49,1,5,'D','torso');
  if(v===3){
   for(let y=47;y<=50;y++)for(let x=0;x<32;x++)if(parts[y][x]==='arms')rows[y][x]=x<16?'C':'D';
   boxpair(6,47,2,2,'A','arms');
   for(let y=55;y<=58;y++)for(let x=0;x<32;x++)if(parts[y][x]==='hips'||parts[y][x]==='legs')rows[y][x]=y===57?'D':'Q';
   boxpair(9,55,3,1,'K','hips');boxpair(9,59,2,2,'C','feet');
  }
 }
 if(v===2){
  for(const y of[47,50,53])for(let x=9;x<=22;x++)dot(x,y,'W','torso');
  for(let y=47;y<=50;y++)for(let x=0;x<32;x++)if(parts[y][x]==='arms')rows[y][x]=y===48?'W':x<16?'C':'D';
  rect(13,46,6,1,'D','torso');
 }
 // Visible anatomy checks exclude hair. Separate skull mask proves hidden symmetry.
 for(let y=0;y<64;y++)for(let x=0;x<16;x++){
  assert.equal(masks.skull[y][x],masks.skull[y][31-x]);
  if(y>=37)assert.equal(parts[y][x],parts[y][31-x],`${spec.slug} part ${x},${y}`);
 }
 const r=new Raster(32,64);
 for(let y=0;y<64;y++)for(let x=0;x<32;x++)if(rows[y][x]!=='.')r.dot(x,y,palette[rows[y][x]]);
 await r.save(new URL(spec.slug+'.png',dir).pathname);
 const m={...spec,id:`review.hero.boy.south.idle.r4.${spec.slug}`,status:'awaiting-user-art-review',frame:[32,64],anchor:[16,64],symmetryAxisX:16,palette,rows:rows.map(r=>r.join('')),parts:parts.map(r=>r.join(',')),skullMask:masks.skull.map(r=>r.join('')),exceptions:['Original hairstyles and outfits follow the four user concepts.','Face/ear width 24 instead of 28; compact human ear tabs. Hair and face bands overlap, unlike a hat-first interpretation.','Hair may be asymmetric; underlying anatomy remains mirrored.'],pose:'front-idle',animation:false};
 await writeFile(new URL(spec.slug+'.json',dir),JSON.stringify(m,null,2)+'\n');models.push(m);
}
const text=(x,y,t,size=18,extra='')=>`<text x="${x}" y="${y}" font-size="${size}" ${extra}>${t}</text>`;
const start=(w,h)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}"><rect width="${w}" height="${h}" fill="#faf7ef"/><g font-family="Arial,sans-serif" fill="#253438">`;
function panel(m,x,y,z){
 let a=[text(x+16*z,y-64,m.title,23,'text-anchor="middle" font-weight="700"'),text(x+16*z,y-38,m.outfit,17,'text-anchor="middle"'),`<rect x="${x}" y="${y}" width="${32*z}" height="${64*z}" fill="#edf0eb"/>`];
 m.rows.forEach((r,j)=>[...r].forEach((k,i)=>{if(k!=='.')a.push(`<rect x="${x+i*z}" y="${y+j*z}" width="${z}" height="${z}" fill="${m.palette[k]}"/>`);}));
 for(let i=0;i<=32;i++)a.push(`<path d="M${x+i*z} ${y}v${64*z}" stroke="#58676a" stroke-opacity=".26"/>`);
 for(let j=0;j<=64;j++){
  const major=j%10===0||j===64;
  a.push(`<path d="M${x} ${y+j*z}h${32*z}" stroke="${major?'#476e80':'#58676a'}" stroke-width="${major?1.7:1}" stroke-opacity="${major?.8:.26}"/>`);
  if(major)a.push(text(x-10,y+j*z+5,''+j,16,'text-anchor="end"'));
 }
 for(const i of[0,10,16,20,30,32])a.push(text(x+i*z,y-12,''+i,13,'text-anchor="middle"'));
 a.push(`<path d="M${x+16*z} ${y-5}v${64*z+10}" stroke="#cc3c83" stroke-width="2"/>`);
 a.push(text(x+16*z,y+64*z+27,'32 × 64 · symmetry x = 16',16,'text-anchor="middle"'));
 return a.join('');
}
const grids={};
for(const [name,cols,z]of[['four-heroes-grid',4,12],['four-heroes-grid-2x2',2,12]]){
 const pw=450,ph=920,w=cols*pw+30,h=Math.ceil(4/cols)*ph+100;
 let svg=start(w,h)+text(48,42,'BOY HERO · FOUR 2× FRONT-IDLE OPTIONS',28,'font-weight="700"')+text(48,74,'One square = one native pixel. Pink: symmetry. Blue: every 10 pixels.',20);
 grids[name]=[];
 models.forEach((m,i)=>{const x=50+(i%cols)*pw,y=175+Math.floor(i/cols)*ph;svg+=panel(m,x,y,z);grids[name].push({slug:m.slug,x,y,scale:z});});
 svg+='</g></svg>';
 await writeFile(new URL(name+'.svg',dir),svg);await sharp(Buffer.from(svg)).png().toFile(new URL(name+'.png',dir).pathname);
}
for(const m of models){const svg=start(480,970)+panel(m,50,100,12)+'</g></svg>';await sharp(Buffer.from(svg)).png().toFile(new URL(m.slug+'-grid.png',dir).pathname);}
await writeFile(new URL('grid-layout.json',dir),JSON.stringify(grids,null,2)+'\n');
console.log('Built four original 32×64 idle sources and exact native-cell grids.');
