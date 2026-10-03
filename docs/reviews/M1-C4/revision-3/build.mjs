// R3: original drawing on the target grid. No doubled source occupancy is used
// to construct this image. Region envelopes and landmarks stay measured.
import {readFile,writeFile} from 'node:fs/promises';
import {createRequire} from 'node:module';
import assert from 'node:assert/strict';
import {Raster} from '../../../../art/source/raster.mjs';
const require=createRequire(import.meta.url);
const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const dir=new URL('./',import.meta.url);
const low=JSON.parse(await readFile(new URL('../revision-2/hero-16x32.json',dir)));
low.reference='Pinned Brendan frame 0; annotations in ../revision-2/measurements.json';
const before=JSON.parse(await readFile(new URL('../revision-2/hero-32x64.json',dir)));
const palette={...low.palette,V:'#775a66',K:'#b9b69b'};
const rows=Array.from({length:64},()=>Array(32).fill('.'));
const labels=Array.from({length:64},()=>Array(32).fill('.'));
// Explicit one-target-pixel contours. Every right side reflects the left;
// measurements constrain the envelope, not each inherited 2x2 block.
const spans={
 20:[12,19],21:[10,21],22:[8,23],23:[7,24],24:[6,25],25:[5,26],
 26:[4,27],27:[4,27],28:[4,27],29:[4,27],30:[4,27],31:[5,26],
 32:[5,26],33:[6,25],34:[6,25],35:[7,24],
 36:[3,28],37:[2,29],38:[2,29],39:[3,28],40:[4,27],41:[5,26],
 42:[6,25],43:[6,25],44:[7,24],45:[8,23],
 46:[7,24],47:[4,27],48:[3,28],49:[2,29],50:[2,29],51:[3,28],
 52:[4,27],53:[5,26],54:[6,25],55:[7,24],56:[6,25],57:[6,25],
 58:[6,25],59:[6,25],60:[7,24],61:[8,23],
};
const part=(x,y)=>y<36?'hair':y<46?'skull':y<54&&(x<10||x>21)?(y<50?'arms':'hands'):y<56?'torso':y<58?'hips':'legsFeet';
for(const [ys,[l,r]]of Object.entries(spans)){const y=Number(ys);for(let x=l;x<=r;x++){
 if(y>=58&&x>=14&&x<=17)continue;
 labels[y][x]=part(x,y);rows[y][x]='O';
}}
const occupied=(x,y)=>Boolean(rows[y]&&rows[y][x]&&rows[y][x]!=='.');
const edge=(x,y)=>!occupied(x-1,y)||!occupied(x+1,y)||!occupied(x,y-1)||!occupied(x,y+1);
// Hue is independent of anatomy. Colored contour pixels and short material
// ramps turn toward the light; deep ink is reserved for actual separations.
for(let y=20;y<62;y++)for(let x=0;x<32;x++){
 if(!occupied(x,y))continue;const p=labels[y][x],e=edge(x,y);let k;
 if(p==='hair')k=e?(x<12&&y<29?'J':'O'):'H';
 if(p==='skull'){
  k='M';if(x<9||x>24||y>=44)k='S';
  if(y<=40&&x>=8&&x<=18)k='L';
  if(e)k='S';
 }
 if(p==='arms')k=e?'K':'W';
 if(p==='hands')k=e?'S':x<16?'L':'M';
 if(p==='torso'){
  k=x<14?'C':'D';if(x>=11&&x<=19)k='C';
  if(x===10&&y<53)k='A';if(y>=54||e)k='D';
 }
 if(p==='hips')k=y===56?'P':'N';
 if(p==='legsFeet')k=y<60?'W':'K';
 if(p==='legsFeet'&&e)k=y===61?'O':'N';
 rows[y][x]=k;
}
function paint(x,y,k,p=null){assert.ok(occupied(x,y),`outside contour ${x},${y}`);rows[y][x]=k;if(p)labels[y][x]=p;}
function run(x,y,s){[...s].forEach((k,i)=>paint(x+i,y,k));}
function pair(x,y,k,other=k){paint(x,y,k);paint(31-x,y,other);}
// Connected curl groups: a light-facing arc and restrained secondary masses.
for(const [x,y,s]of [
 [12,21,'JJJJHH'],[10,22,'JVVJJHHHHH'],[8,23,'JVVJJJHHHHJJ'],
 [7,24,'JJJJHHHHHJJJHH'],[6,25,'JJJHHHHHJJJHHHH'],
 [6,26,'JJHHHHHHHJHHHHH'],[5,27,'JHHHHJJHHHHHHHH'],
 [5,28,'JHHHJJJJHHHHHHH'],[6,29,'HHHJJJHHHHHHHH'],
 [7,30,'HHHHJHHHHHHHH'],[20,28,'JJH'],[21,29,'JHH'],
 [10,32,'JHHHHHH'],[11,33,'HHHHHH'],[7,34,'HHH'],[21,34,'HHH']])run(x,y,s);
// Short irregular hairline inside the existing envelope, not a thick flat bar.
pair(8,35,'S');pair(9,35,'M');pair(10,35,'H');
pair(11,35,'O');pair(12,35,'H');pair(13,35,'O');
// Soft cheek/ear planes. No long vertical nose highlight or square chin patch.
run(5,38,'MLM');run(24,38,'MMS');
run(6,39,'MLLM');run(22,39,'MMMS');
run(8,40,'LLM');run(21,40,'MMS');run(9,41,'LLM');
run(10,42,'MMMMMMMMMMMM');run(12,43,'MMMMMMMM');
run(12,44,'MMMMMMMM');run(13,45,'MMMMMM');
paint(16,41,'S');pair(15,43,'S');
// Measured eye envelopes; glints are surface color inside those envelopes.
for(let y=38;y<=41;y++)for(const x of [12,13,18,19])paint(x,y,'E','eyes');
paint(12,38,'W');paint(19,38,'W');
// Neck-to-shirt overlap is local. Sleeve contacts have one-pixel seams.
run(12,46,'DSSMMSSD');run(12,47,'DCCCCCCD');
for(const [x,y,k,other]of [[7,47,'W','K'],[6,48,'W','W'],[5,49,'W','K'],[9,49,'D','D'],[9,50,'D','D'],[9,51,'D','D'],[8,52,'S','S'],[10,53,'C','D'],[11,54,'C','D']])pair(x,y,k,other);
// Rounded hands with a tiny near-side highlight; shape stays paired.
for(const[y,x,s]of [[50,2,'SMLLMMSO'],[51,3,'SMMMMSO'],[52,4,'SMMMSO'],[53,5,'SSSSO']]){
 [...s].forEach((k,i)=>pair(x+i,y,k,k==='L'?'M':k));
}
// Lit cloth edges remain warm; dark joins sit below the sleeves, beside hands.
pair(3,49,'K','O');pair(4,48,'K','S');pair(9,49,'D','D');
// A curved hem and a small, connected cloth fold explain volume.
run(11,52,'CCCCCCCCCD');run(12,53,'CCCCCCCC');
run(11,54,'DCCCCCCCCD');run(12,55,'DDCCCCDD');
for(let y=48;y<53;y++)paint(10,y,'C');
paint(11,48,'A');paint(11,49,'A');paint(12,49,'A');paint(12,50,'A');paint(12,51,'C');
paint(20,49,'D');paint(20,50,'D');paint(20,51,'D');
run(10,56,'PNNNNNNNNNNP');
// Toe/sole clusters use target-pixel corners; no 2px rectangular shoe frame.
for(const [x,y,k]of [[7,58,'K'],[8,58,'W'],[9,58,'W'],[10,58,'W'],[11,58,'W'],[12,58,'K'],[7,59,'W'],[8,59,'W'],[9,59,'W'],[10,59,'W'],[11,59,'W'],[12,59,'K'],[8,60,'K'],[9,60,'W'],[10,60,'W'],[11,60,'K']])pair(x,y,k);
const target={...before,id:'review.hero.boy.south.idle.32x64.r3',reference:'Pinned Brendan frame 0; region targets and actuals in independent-validation.json',palette,rows:rows.map(r=>r.join('')),partLabels:labels,status:'awaiting-user-art-review',exceptions:['Original afro inside measured envelope; original costume and palette.','Target-grid contour refinement changes individual occupied rows; exact doubled low-resolution occupancy is not required.'],symmetry:{}};
const report={frames:[],referenceRevision:'5eff78649e7170a877b961ef0b3da13b81a16038',approval:false};
for(const model of [low,target]){
 const [w,h]=model.frame,r=new Raster(w,h),parts={};
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const k=model.rows[y][x],p=model.partLabels[y][x];
  assert.equal(k==='.',model.rows[y][w-1-x]==='.');
  assert.equal(p,model.partLabels[y][w-1-x]);
  if(k==='.')continue;r.dot(x,y,model.palette[k]);parts[p]??={left:0,right:0};parts[p][x<w/2?'left':'right']++;
 }
 for(const v of Object.values(parts))assert.equal(v.left,v.right);
 model.symmetry=parts;await r.save(new URL(`hero-${w}x${h}.png`,dir).pathname);
 await writeFile(new URL(`hero-${w}x${h}.json`,dir),JSON.stringify(model,null,2)+'\n');
 report.frames.push({frame:model.frame,symmetry:parts,mismatchPairs:0});
}
function mixed(m){let n=0;for(let y=0;y<64;y+=2)for(let x=0;x<32;x+=2){const v=new Set();for(let j=0;j<2;j++)for(let i=0;i<2;i++)v.add(m.rows[y+j][x+i]!=='.');if(v.size>1)n++;}return n;}
report.mixedAlphaBlocks={before:mixed(before),after:mixed(target)};assert.ok(report.mixedAlphaBlocks.after>0,'native contours must not remain a locked 2x enlargement');
const models=[{...low,scale:24},{...target,scale:12}];
const text=(x,y,t,n=19,extra='')=>`<text x="${x}" y="${y}" font-size="${n}" ${extra}>${t}</text>`;
function cells(s,x,y,z=s.scale){let a=[];s.rows.forEach((r,j)=>[...r].forEach((k,i)=>{if(k!=='.')a.push(`<rect x="${x+i*z}" y="${y+j*z}" width="${z}" height="${z}" fill="${s.palette[k]}"/>`);}));return a.join('');}
function panel(s,x,y){const[w,h]=s.frame,z=s.scale,W=w*z,H=h*z;let a=[`<rect x="${x}" y="${y}" width="${W}" height="${H}" fill="#edf0ec"/>`,cells(s,x,y)];
 for(let i=0;i<=w;i++)a.push(`<path d="M${x+i*z} ${y}v${H}" stroke="#566666" stroke-opacity=".22"/>`);
 for(let j=0;j<=h;j++){const major=j%10===0||j===h;a.push(`<path d="M${x} ${y+j*z}h${W}" stroke="${major?'#3e697c':'#566666'}" stroke-width="${major?2:1}" stroke-opacity="${major?.85:.22}"/>`);if(major)a.push(text(x-14,y+j*z+6,''+j,17,'text-anchor="end"'));}
 for(const i of[0,w/2,w])a.push(text(x+i*z,y-15,''+i,17,'text-anchor="middle"'));
 a.push(`<path d="M${x+W/2} ${y-6}v${H+12}" stroke="#c23a78" stroke-width="3"/>`);
 a.push(text(x+W/2,y+H+35,`Symmetry axis: x = ${w/2}`,18,'text-anchor="middle" fill="#a32f65"'));return a.join('');}
const svgStart=(w,h)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><rect width="${w}" height="${h}" fill="#faf7ef"/><g font-family="Arial, sans-serif" fill="#233337">`;
const grid=svgStart(1120,1180)+text(64,50,'HERO / FINER CONTOURS, SAME PROPORTIONS',27,'font-weight="700"')+text(64,84,'One square = one native pixel. Pink = centerline. Blue = every 10 rows.')+text(290,135,'16 × 32 / unchanged baseline',24,'text-anchor="middle" font-weight="700"')+text(828,135,'32 × 64 / native redraw',24,'text-anchor="middle" font-weight="700"')+panel(models[0],98,180)+panel(models[1],636,180)+text(290,1010,'14 × 21 painted · displayed at 24×',18,'text-anchor="middle"')+text(828,1010,'28 × 42 painted · displayed at 12×',18,'text-anchor="middle"')+text(64,1055,'Contours use individual target pixels; anatomy stays mirrored.',21)+text(64,1092,'Material-colored edges, rounded corners and grouped light/shadow planes.')+text(64,1130,'Front idle only · revision 3 · awaiting visual review')+'</g></svg>';
let clean=svgStart(1100,730)+text(55,48,'2× DETAIL REVIEW / WITHOUT THE GRID',27,'font-weight="700"');
clean+=text(260,92,'Previous: enlarged block edges',21,'text-anchor="middle"')+text(810,92,'Revision 3: target-pixel contours',21,'text-anchor="middle"');
clean+=cells(before,100,-80,10)+cells(target,650,-80,10);
clean+=text(55,603,'Both drawings: 32×64 frames, 28×42 painted bounds, identical eye locations.',20);
clean+=text(55,639,'Contour smoothing here means deliberate opaque pixel placement—not blur.',19);
clean+=text(55,685,'Native 1×',16)+cells(target,178,633,1)+text(280,685,'Native 2× display',16)+cells(target,444,601,2)+'</g></svg>';
for(const[name,svg]of[['hero-grid',grid],['before-after',clean]]){await writeFile(new URL(name+'.svg',dir),svg);await sharp(Buffer.from(svg)).png().toFile(new URL(name+'.png',dir).pathname);}
await writeFile(new URL('validation.json',dir),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
