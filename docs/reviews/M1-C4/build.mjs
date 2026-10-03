// Original indexed-pixel Hero study. This edits the project's native pixel
// drawing format; no concept image is downsampled or used as a texture.
import {readFile, writeFile} from 'node:fs/promises';
import {createRequire} from 'node:module';
import assert from 'node:assert/strict';
import {Raster} from '../../../art/source/raster.mjs';
const require=createRequire(import.meta.url);
const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const dir=new URL('./',import.meta.url);
const old=JSON.parse(await readFile(new URL('../../../art/source/characters-v2/hero.boy.json',import.meta.url)));
const palette={...old.palette};
const body=[
 '.....OOOOOO.....',
 '...OOJJHHHHOO...',
 '..OJJJHHHHHHHO..',
 '.OJJJHHJHHHHHHO.',
 '.OJHHHHHHHHHHHO.',
 '.OHHHHHHHHHHHHO.',
 '..OHHHMMHHHHHO..',
 '..OMMLLLLMMMHO..',
 '.OMLLELLLLEMMSO.',
 '.OMLLELLLLEMMSO.',
 '..OMLLLLMMMMSO..',
 '...OMMMMMMMSO...',
 '...OSMMMMMMSO...',
 '..OWWDDDDDDWWO..',
 '.OWWWACCCCAWWWO.',
 '.OMMWCCCCCCWMMO.',
 '..OSODCCCCDOSO..',
 '...ODCCCCCCDO...',
 '...ONNNNNNNNO...',
 '...OWWWOOWWWO...',
 '....OOO..OOO....',
];
const low=Array(10).fill('.'.repeat(16)).concat(body,'.'.repeat(16));
const hi=low.flatMap(r=>{const t=[...r].map(k=>k+k);return [t.join('').split(''),t.join('').split('')];});
// Native 32×64 refinement: retain the skeleton while adding half-step
// contours, hair clusters, face detail, sleeve seams and sneaker toes.
const edits=[];
function put(x,y,k){assert.ok(x>=0&&x<32&&y>=0&&y<64);const was=hi[y][x];if(was!==k){hi[y][x]=k;edits.push({x,y,from:was,to:k});}}
function run(x,y,s){[...s].forEach((k,i)=>put(x+i,y,k));}
// Explicit scanline contour, traced as anatomy (not the reference's hat/hair).
// Round the afro and cheeks without disconnected outline fragments.
const headSpans=[[11,20],[9,22],[7,24],[6,25],[5,26],[4,27],[3,28],[2,29],[2,29],[2,29],[2,29],[3,28],[4,27],[4,27],[4,27],[3,28],[2,29],[2,29],[2,29],[3,28],[4,27],[5,26],[6,25],[6,25],[6,25],[7,24]];
for(const [i,[l,r]] of headSpans.entries()){const y=20+i;for(let x=0;x<32;x++){if(x<l||x>r)put(x,y,'.');else if(x===l||x===r)put(x,y,'O');else if(hi[y][x]==='.'||hi[y][x]==='O')put(x,y,y<34?'H':x<16?'M':'S');}}
// Grouped curls, not random texture.
for(const [x,y,s] of [[9,23,'JJJ'],[8,24,'JJHH'],[5,27,'JJH'],[6,28,'JHH'],[12,26,'JJ'],[11,27,'JHH'],[20,25,'JH'],[21,26,'JH'],[24,29,'JH'],[18,29,'JJH'],[16,30,'JHH'],[7,30,'JH'],[8,31,'HH']])run(x,y,s);
// Natural hairline follows the broad reference face, without hat/spike copying.
run(10,32,'HHHMMHHHHHHH');run(9,33,'HHMMMLMHHHHHH');
run(8,34,'MMMLLLLLMMMHHH');run(7,35,'MMMLLLLLLLMMMHH');
// Compact eyes: same placement, a tiny warm glint, no enlarged anime eyes.
put(10,36,'W');put(20,36,'W');
put(9,35,'S');put(10,35,'S');put(20,35,'S');put(21,35,'S');
// Ear/cheek ramps and a restrained mouth, kept inside the existing head.
run(4,38,'ML');run(26,38,'MS');
run(5,40,'MLL');run(24,40,'MMS');
run(12,40,'LLMM');run(15,41,'MM');
run(13,42,'MMMMMM');run(15,43,'SS');
run(10,44,'MMMMMMMMMMMM');
run(11,45,'MMMMMMMMMM');
// Short raglan sleeves, tiny connected torso and hands.
run(8,46,'WWWDDDDDDWWW');run(8,47,'WWADDDDDDAWW');
run(8,48,'WAACCCCCCAAW');run(8,49,'WACCCCCCCCAW');
run(8,50,'WACCCCCCCCAW');
put(5,51,'L');put(26,51,'M');put(5,52,'M');put(26,52,'S');
run(9,53,'DCCCCCCCCCCCD');
run(9,54,'DCCCCCCCCCCCD');run(10,55,'DDCCCCCCCCDD');
run(10,56,'NPPNNNNNNNNN');run(10,57,'NNNNNOONNNNN');
// One-row shoe/toe detailing; no added shins or increased leg length.
run(8,58,'WWWWW');run(18,58,'WWWWW');
run(8,59,'WWWWW');run(18,59,'WWWWW');
run(9,60,'PWWW');run(19,60,'PWWW');
const high=hi.map(r=>r.join(''));
const sources=[{id:'review.hero.boy.idle.16x32.v1',frame:[16,32],anchor:[8,32],rows:low,bands:[10,23,28,31],scale:24},
 {id:'review.hero.boy.idle.32x64.v1',frame:[32,64],anchor:[16,64],rows:high,bands:[20,46,56,62],scale:12}];
const checks=[];
const check=(ok,name)=>{assert.ok(ok,name);checks.push(name);};
// Read-only screenshot sampling at its displayed coarse grid identified these
// eight occupied rows. Copy the construction mask, never its colored artwork.
const referenceBody=['..############..','.##############.','.##############.','..############..','...##########...','...##########...','...##########...','....###..###....'];
check(low.slice(23,31).every((r,i)=>r.replace(/[^.]/g,'#')===referenceBody[i]),'16x32 torso, arms, hips and feet match supplied reference occupancy exactly');
for(const s of sources){
 check(s.rows.length===s.frame[1]&&s.rows.every(r=>r.length===s.frame[0]),s.id+': exact native dimensions');
 const raster=new Raster(...s.frame);let minx=999,miny=999,maxx=-1,maxy=-1,n=0;
 s.rows.forEach((row,y)=>[...row].forEach((k,x)=>{check(k==='.'||Boolean(palette[k]),`${s.id}: valid (${x},${y})`);if(k==='.')return;raster.dot(x,y,palette[k]);n++;minx=Math.min(minx,x);maxx=Math.max(maxx,x);miny=Math.min(miny,y);maxy=Math.max(maxy,y);}));
 s.opaqueBBox=[minx,miny,maxx+1,maxy+1];s.paintedPixels=n;s.palette=palette;
 s.status='awaiting-user-review';s.pose='south-idle';s.animation=null;
 s.reference='User-supplied comparison screenshot: broad head, 13/5/3 approximate structural row proportions; original afro/clothing design.';
 await raster.save(new URL(`hero-${s.frame.join('x')}.png`,dir).pathname);
 await writeFile(new URL(`hero-${s.frame.join('x')}.json`,dir),JSON.stringify(s,null,2)+'\n');
}
check(edits.length>80,'32x64 contains native refinements, not just enlarged blocks');
// Every SVG cell and grid coordinate is generated from the exported indexed data.
const colors={head:'#e7bd72',body:'#64b7ab',arms:'#ee967f',lower:'#8aa8dc'};
const text=(x,y,t,size=20,extra='')=>`<text x="${x}" y="${y}" font-size="${size}" ${extra}>${t}</text>`;
function panel(s,x,y,skeleton=false){
 const [w,h]=s.frame,z=s.scale,W=w*z,H=h*z;let a=[];
 a.push(`<rect x="${x}" y="${y}" width="${W}" height="${H}" fill="#edf0ec"/>`);
 s.rows.forEach((r,j)=>[...r].forEach((k,i)=>{if(k==='.')return;let fill=palette[k];if(skeleton){fill=j<s.bands[1]?colors.head:j<s.bands[2]?((i<w*.3||i>=w*.7)?colors.arms:colors.body):colors.lower;}
 a.push(`<rect x="${x+i*z}" y="${y+j*z}" width="${z}" height="${z}" fill="${fill}"/>`);}));
 for(let i=0;i<=w;i++){const major=i%10===0||i===w;a.push(`<path d="M${x+i*z} ${y}v${H}" stroke="${major?'#3e697c':'#566666'}" stroke-opacity="${major?'.9':'.3'}" stroke-width="${major?2:1}"/>`);if(major)a.push(text(x+i*z,y-14,String(i),17,'text-anchor="middle"'));}
 for(let j=0;j<=h;j++){const major=j%10===0||j===h;a.push(`<path d="M${x} ${y+j*z}h${W}" stroke="${major?'#3e697c':'#566666'}" stroke-opacity="${major?'.9':'.3'}" stroke-width="${major?2:1}"/>`);if(major)a.push(text(x-14,y+j*z+6,String(j),17,'text-anchor="end"'));}
 if(skeleton){for(const r of s.bands)a.push(`<path d="M${x} ${y+r*z}h${W}" stroke="#af4438" stroke-width="2" stroke-dasharray="6 4"/>`);}
 return a.join('');
}
function plate(skeleton=false){
 let a=[`<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="1160" viewBox="0 0 1120 1160"><rect width="1120" height="1160" fill="#faf7ef"/><g font-family="Arial, sans-serif" fill="#233337">`];
 a.push(text(64,54,skeleton?'HERO / CHIBI CONSTRUCTION':'HERO / COUNTABLE IDLE PIXELS',29,'font-weight="700"'));
 a.push(text(64,88,'One square = one native pixel. Heavy numbered lines = every 10 pixels.',19));
 a.push(text(290,138,'16 × 32',28,'text-anchor="middle" font-weight="700"'),text(828,138,'32 × 64',28,'text-anchor="middle" font-weight="700"'));
 a.push(panel(sources[0],98,182,skeleton),panel(sources[1],636,182,skeleton));
 a.push(text(290,989,'24× display · 14 × 21 painted bounds',18,'text-anchor="middle"'),text(828,989,'12× display · 28 × 42 painted bounds',18,'text-anchor="middle"'));
 if(skeleton){a.push(text(64,1040,'HEAD  13 → 26 rows    /    TORSO + ARMS  5 → 10    /    SHORTS + FEET  3 → 6',20,'font-weight="700"'),text(64,1076,'Broad head, tucked neck, short connected body, feet close beneath the hips.',19),text(64,1111,'Colored regions show construction; no walking poses or gameplay changes.',18));}
 else a.push(text(64,1040,'Same display size. The right drawing has twice the resolution on each axis.',20),text(64,1076,'Blank squares are transparent frame padding. Ruler values mark pixel boundaries.',19),text(64,1111,'Original Critz boy Hero · revision 1 · awaiting your shape review',18));
 return a.join('')+'</g></svg>';
}
for(const [name,skeleton]of [['hero-grid',false],['hero-skeleton',true]]){const svg=plate(skeleton);await writeFile(new URL(name+'.svg',dir),svg);await sharp(Buffer.from(svg)).png().toFile(new URL(name+'.png',dir).pathname);}
await writeFile(new URL('refinements.json',dir),JSON.stringify(edits,null,2)+'\n');
await writeFile(new URL('validation.json',dir),JSON.stringify({checks:checks.length,nativeRefinements:edits.length,frames:sources.map(s=>({id:s.id,frame:s.frame,opaqueBBox:s.opaqueBBox,paintedPixels:s.paintedPixels})),grid:{majorEvery:10,displayScales:[24,12],displayFrames:[[384,768],[384,768]]},artApproval:false},null,2)+'\n');
console.log(JSON.stringify({checks:checks.length,refinements:edits.length,frames:sources.map(s=>s.opaqueBBox)}));
