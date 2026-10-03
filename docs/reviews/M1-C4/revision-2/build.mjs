// Exact native-source revision. Geometry and anatomical labels are authored
// independently of hue, so lighting cannot enlarge an arm or move an eye.
import {readFile,writeFile} from 'node:fs/promises';
import {createRequire} from 'node:module';
import assert from 'node:assert/strict';
import {Raster} from '../../../../art/source/raster.mjs';
const require=createRequire(import.meta.url);
const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const dir=new URL('./',import.meta.url);
const palette=JSON.parse(await readFile(new URL('../hero-16x32.json',dir))).palette;
const painted=[
 '......OOOO......',
 '....OOJJHHOO....',
 '...OJJJHHHHHO...',
 '..OJJJHHHHHHHO..',
 '..OJJHHHHHHHHO..',
 '..OHHHHHHHHHHO..',
 '...OHHHHHHHHO...',
 '...OHHHHHHHHO...',
 '.OMMLLLLLLLMMSO.',
 '.OMMLLELLEMMSMO.',
 '..OMMLEMMEMMSO..',
 '...OMMLMMMMSO...',
 '...OOMMMMMMOO...',
 '..OWWDDDDDDWWO..',
 '.OWWOCCCCCCOWWO.',
 '.OMLOCCCCCCOMSO.',
 '..OSODCCCCDOMO..',
 '...ODCCCCCCDO...',
 '...ONNNNNNNNO...',
 '...OWWWOOWWWO...',
 '....OOO..OOO....',
];
const low=Array(10).fill('.'.repeat(16)).concat(painted,'.'.repeat(16)).map(r=>[...r]);
assert.ok(low.every(r=>r.length===16));
const part=(x,y,k)=>{
 if(k==='.')return '.';
 if(y<18)return 'hair';
 if(y<23)return k==='E'?'eyes':'skull';
 if(y<27&&(x<5||x>=11))return y<25?'arms':'hands';
 if(y<28)return 'torso';
 return x>=7&&x<9?'hips':'legsFeet';
};
const labels=low.map((r,y)=>r.map((k,x)=>part(x,y,k)));
const high=low.flatMap(r=>{const q=r.flatMap(k=>[k,k]);return [[...q],[...q]];});
const highLabels=labels.flatMap(r=>{const q=r.flatMap(k=>[k,k]);return [[...q],[...q]];});
const edits=[];
function set(x,y,k){assert.notEqual(high[y][x],'.');const before=high[y][x];if(before!==k){high[y][x]=k;edits.push({x,y,before,after:k});}}
function run(x,y,s){[...s].forEach((k,i)=>set(x+i,y,k));}
// Grouped original curl highlights. These do not alter the anatomical masks.
for(const [x,y,s]of [[12,21,'JJH'],[9,23,'JJH'],[7,25,'JJH'],[5,28,'JHH'],[8,28,'JJH'],[12,26,'JJH'],[17,24,'JH'],[20,27,'JHH'],[22,30,'JH'],[15,30,'JHH'],[7,32,'JH'],[10,33,'HHJ'],[18,32,'JHH'],[12,34,'JH']])run(x,y,s);
// Face features occupy the measured eye rectangles; skin shading is free to
// differ while the skull, eye positions and eye dimensions stay mirrored.
set(12,38,'W');set(19,38,'W');
run(8,37,'MLLL');run(20,37,'MMSS');
run(10,41,'LM');run(20,41,'MS');
run(13,42,'LMMMMM');run(15,43,'SS');
run(10,44,'MMMMMMMMMMMM');run(12,45,'MMMMMMMM');
// Raglan collar/sleeves are shaped by paired edits. The color ramps can vary.
for(const [x,y,left,right]of [[8,46,'W','W'],[9,47,'A','D'],[8,48,'W','W'],[7,49,'W','W'],[5,50,'L','M'],[6,51,'M','S'],[5,52,'M','S'],[10,52,'A','D'],[11,53,'C','D'],[10,54,'D','D'],[11,55,'D','D'],[10,56,'P','N'],[11,57,'P','N'],[9,58,'W','W'],[10,59,'W','W'],[9,60,'W','W'],[10,60,'P','P']]){set(x,y,left);set(31-x,y,right);}
const models=[{frame:[16,32],rows:low,labels,scale:24},{frame:[32,64],rows:high,labels:highLabels,scale:12}];
const report={status:'pass',referenceRevision:'5eff78649e7170a877b961ef0b3da13b81a16038',referenceSha256:'f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1',frames:[],nativeRefinementOperations:edits.length,artApproval:false};
for(const s of models){
 const [w,h]=s.frame,z=w/16,rad=new Raster(w,h),masks={};let minX=w,minY=h,maxX=0,maxY=0;
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const k=s.rows[y][x],p=s.labels[y][x];
  assert.equal(k==='.',s.rows[y][w-1-x]==='.','opaque silhouette symmetry');
  if(p!=='hair')assert.equal(p,s.labels[y][w-1-x],'anatomical mask symmetry');
  // The structural color families must also match so highlights cannot hide
  // a larger hand or uneven sleeve even when the total alpha mask is equal.
  const material=c=>'SML'.includes(c)?'skin':'DCA'.includes(c)?'shirt':'NP'.includes(c)?'shorts':c;
  if(y>=23*z)assert.equal(material(k),material(s.rows[y][w-1-x]),'material boundary symmetry');
  if(k==='.')continue;assert.ok(palette[k]);rad.dot(x,y,palette[k]);
  minX=Math.min(minX,x);minY=Math.min(minY,y);maxX=Math.max(maxX,x+1);maxY=Math.max(maxY,y+1);
  masks[p]??={left:0,right:0};masks[p][x<w/2?'left':'right']++;
 }
 for(const [part,n]of Object.entries(masks))if(part!=='hair')assert.equal(n.left,n.right,part+' equal side areas');
 const id=`review.hero.boy.south.idle.${w}x${h}.r2`;
 const data={id,status:'awaiting-user-art-review',frame:s.frame,anchor:[w/2,h],symmetryAxisX:w/2,opaqueBBox:[minX,minY,maxX,maxY],palette,rows:s.rows.map(r=>r.join('')),partLabels:s.labels,pose:'front-idle',animation:null,reference:'Brendan walking.png frame 0; source-only annotations in measurements.json',exceptions:['Original afro replaces reference headwear; original palette and clothing.'],symmetry:masks};
 await rad.save(new URL(`hero-${w}x${h}.png`,dir).pathname);
 await writeFile(new URL(`hero-${w}x${h}.json`,dir),JSON.stringify(data,null,2)+'\n');
 report.frames.push({id,frame:s.frame,opaqueBBox:data.opaqueBBox,symmetry:masks,opaqueMismatchPairs:0,anatomicalMismatchPairs:0,bodyMaterialMismatchPairs:0});
}
const text=(x,y,t,n=19,extra='')=>`<text x="${x}" y="${y}" font-size="${n}" ${extra}>${t}</text>`;
const skeletonColors={hair:'#716a81',skull:'#e4bd78',eyes:'#142832',arms:'#64b7ab',hands:'#ed9f82',torso:'#3e9b9d',hips:'#597aa4',legsFeet:'#8aa8dc'};
function panel(s,x,y,skeleton){const [w,h]=s.frame,z=s.scale,W=w*z,H=h*z;let a=[`<rect x="${x}" y="${y}" width="${W}" height="${H}" fill="#edf0ec"/>`];
 s.rows.forEach((r,j)=>r.forEach((k,i)=>{if(k!=='.')a.push(`<rect x="${x+i*z}" y="${y+j*z}" width="${z}" height="${z}" fill="${skeleton?skeletonColors[s.labels[j][i]]:palette[k]}"/>`);}));
 for(let i=0;i<=w;i++)a.push(`<path d="M${x+i*z} ${y}v${H}" stroke="#566666" stroke-opacity=".28"/>`);
 for(let j=0;j<=h;j++){const major=j%10===0||j===h;a.push(`<path d="M${x} ${y+j*z}h${W}" stroke="${major?'#3e697c':'#566666'}" stroke-width="${major?2:1}" stroke-opacity="${major?.85:.28}"/>`);if(major)a.push(text(x-14,y+j*z+6,''+j,17,'text-anchor="end"'));}
 for(const i of [0,w/2,w])a.push(text(x+i*z,y-15,''+i,17,'text-anchor="middle"'));
 a.push(`<path d="M${x+W/2} ${y-6}v${H+12}" stroke="#c23a78" stroke-width="3"/>`);
 a.push(text(x+W/2,y+H+35,`Symmetry axis: x = ${w/2}`,18,'text-anchor="middle" fill="#a32f65"'));
 return a.join('');}
function plate(skeleton){let a=[`<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="1180" viewBox="0 0 1120 1180"><rect width="1120" height="1180" fill="#faf7ef"/><g font-family="Arial, sans-serif" fill="#233337">`];
 a.push(text(64,50,skeleton?'HERO / SYMMETRY PROOF':'HERO / EMERALD 1× AND 2×',29,'font-weight="700"'));
 a.push(text(64,84,'One square = one native pixel. Pink = centerline. Blue = every 10 rows.',19));
 a.push(text(290,135,'16 × 32  /  1× budget',25,'text-anchor="middle" font-weight="700"'),text(828,135,'32 × 64  /  2× budget',25,'text-anchor="middle" font-weight="700"'));
 a.push(panel(models[0],98,180,skeleton),panel(models[1],636,180,skeleton));
 a.push(text(290,1010,'14 × 21 painted · displayed at 24×',18,'text-anchor="middle"'),text(828,1010,'28 × 42 painted · displayed at 12×',18,'text-anchor="middle"'));
 if(skeleton){a.push(text(64,1055,'SKULL + EYES   /   ARMS + HANDS   /   TORSO + LEGS: mirrored geometry',21,'font-weight="700"'),text(64,1092,'Hair is a separate layer. Symmetry is checked by part, not only by outer outline.',19),text(64,1130,'Both sides have equal occupied area and mirrored material boundaries.',19));}
 else {a.push(text(64,1055,'Same apparent size. Equal arm and hand shapes. Measured eye placement.',21),text(64,1092,'Shading may differ; anatomy and clothing boundaries remain mirrored.',19),text(64,1130,'Front idle only · revision 2 · artwork awaiting your review',19));}
 return a.join('')+'</g></svg>';}
for(const [name,flag]of [['hero-grid',false],['hero-symmetry',true]]){const svg=plate(flag);await writeFile(new URL(name+'.svg',dir),svg);await sharp(Buffer.from(svg)).png().toFile(new URL(name+'.png',dir).pathname);}
await writeFile(new URL('validation.json',dir),JSON.stringify(report,null,2)+'\n');
await writeFile(new URL('refinements.json',dir),JSON.stringify(edits,null,2)+'\n');
console.log(JSON.stringify(report));
