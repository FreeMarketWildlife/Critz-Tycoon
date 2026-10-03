// Native pixel authoring. All geometry is integer-cell marks, not sampled reference colors.
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const root=path.dirname(new URL(import.meta.url).pathname);
const external=process.argv[2];
if(external && path.resolve(external).startsWith(path.resolve(root,'../../../..')+path.sep))throw Error('Reference comparison must remain outside the project');
const common={O:'#19212b',H:'#201a1b',h:'#352926',j:'#503b31',k:'#6b4c37',s:'#b87949',t:'#945833',u:'#d99b60',d:'#62382c',C:'#fff1d0',c:'#d6c496',N:'#27334c',B:'#405d83',b:'#6081a7'};
const variants=[['a-afro',{T:'#348e99',L:'#62b7b7',V:'#215f70'}],['b-flat-top',{T:'#d5a02e',L:'#f1c95b',V:'#926320',N:'#25272e',B:'#42434c',b:'#61616a'}],['c-twists',{T:'#e55b4a',L:'#ff9273',V:'#a93936'}],['d-cornrows',{T:'#356aa6',L:'#6da1d0',V:'#24466d',N:'#3c4430',B:'#7d824a',b:'#a4a56b'}]];
const models=[];
for(let v=0;v<4;v++){
 const [slug,extra]=variants[v],palette={...common,...extra};
 const a=Array.from({length:64},()=>Array(32).fill('.'));
 const masks={};
 function px(x,y,c,part){if(x<0||x>31||y<0||y>63)throw Error('Outside frame');a[y][x]=c;if(part){masks[part]??=Array.from({length:64},()=>Array(32).fill(0));masks[part][y][x]=1;}}
 function run(y,l,r,c,part){for(let x=l;x<=r;x++)px(x,y,c,part);}
 function rect(l,t,r,b,c,part){for(let y=t;y<=b;y++)run(y,l,r,c,part);}
 function pair(l,t,r,b,c,part){rect(l,t,r,b,c,part);rect(31-r,t,31-l,b,c,part);}
 // Symmetric rounded skull/face construction. Hair is a separate overlay.
 const face=[12,10,8,7,6,6,6,6,6,6,6,7,8,9,11];
 face.forEach((l,i)=>{const y=30+i,r=31-l;run(y,l,r,'d','skull');if(r-l>3){run(y,l+1,r-1,'t');if(y<42)run(y,l+2,r-3,'s');if(y<39)run(y,l+2,l+3,'u');}});
 pair(4,37,7,39,'d','ears');pair(5,36,7,40,'d','ears');
 rect(5,37,7,39,'s');rect(6,37,7,38,'u');rect(24,37,26,39,'t');rect(24,37,25,38,'s');
 run(41,10,21,'s');run(42,11,20,'s');run(43,13,18,'t');
 // Tall, uncomplicated eyes: one Emerald pixel becomes a 2x4 target rectangle.
 pair(12,38,13,41,'O','eyes');
 // Neck and torso, shoulders behind arms, deliberate dark contact separation.
 rect(12,44,19,46,'d','neck');rect(13,44,18,45,'t');
 for(let y=46;y<=55;y++){const l=y===46?10:9;run(y,l,31-l,'O','torso');}
 rect(10,47,21,53,'T');rect(11,46,20,53,'T');rect(12,46,19,46,'V');
 rect(10,49,11,52,'L');rect(20,48,21,53,'V');run(54,11,20,'V');
 // Matched sleeve contours and matched hands; lighting may differ.
 for(const [y,l,r] of [[46,7,10],[47,6,10],[48,5,10],[49,5,9]])pair(l,y,r,y,'O','sleeves');
 pair(7,46,9,46,v===0||v===1?'C':'T');pair(6,47,9,48,v===0||v===1?'C':'T');pair(6,49,8,49,v===0||v===1?'c':'V');
 if(v>=2){pair(6,47,7,47,'L');if(v===2)pair(6,48,8,48,'C');}
 for(const [y,l,r] of [[49,5,8],[50,4,8],[51,4,8],[52,5,8]])pair(l,y,r,y,'d','hands');
 pair(5,50,7,51,'s');rect(5,50,7,50,'u');rect(24,51,26,51,'t');
 // Shorts: separate each leg and retain a dark crotch, without long shins.
 rect(9,55,22,57,'N','hips');pair(9,58,14,58,'N','hips');
 pair(10,55,14,57,'B');pair(10,55,12,55,'b');run(55,15,16,'B');
 pair(11,58,13,58,'t','legs');pair(11,59,13,59,'s','legs');
 // Compact sneaker silhouettes, cream uppers, colored tongues and one-row soles.
 pair(9,59,14,61,'O','feet');pair(10,59,13,60,'C');pair(10,59,11,59,'T');pair(10,61,13,61,'c');
 if(v===1||v===3){
  // Open vest / jacket: the cream insert remains narrow and continuous.
  rect(14,47,17,53,'C');rect(14,53,17,54,'c');
  rect(11,46,13,53,'T');rect(18,46,20,53,'T');
  rect(11,47,11,52,'L');rect(20,48,20,53,'V');
  rect(13,48,13,53,'V');rect(18,48,18,53,'V');
  px(12,47,'L');px(19,47,'L');
  if(v===3){px(12,48,'L');px(19,48,'L');run(50,11,12,'L');run(50,19,20,'L');}
  else {run(50,11,12,'V');run(50,19,20,'V');}
 }else if(v===2){
  rect(11,48,20,49,'C');rect(11,52,20,53,'C');
  rect(10,48,10,49,'c');rect(21,48,21,49,'c');rect(10,52,10,53,'c');rect(21,52,21,53,'c');run(47,12,19,'L');
 }else{run(47,12,16,'L');rect(11,48,11,49,'L');}
 // Distinct hair silhouettes, drafted directly on the 32-column pixel matrix.
 if(v===0){
  const rows=[[24,12,19],[25,9,22],[26,8,23],[27,6,25],[28,6,25],[29,5,26],[30,5,26],[31,4,27],[32,4,27],[33,5,26],[34,5,26]];
  for(const [y,l,r] of rows){run(y,l,r,'H','hair');if(y>24)run(y,l+1,r-1,'h');}
  run(25,12,18,'j');run(26,10,20,'j');run(27,8,13,'j');run(28,7,10,'j');run(29,6,8,'j');
  run(28,17,21,'j');run(29,20,23,'j');run(30,23,24,'j');
  run(31,11,21,'H');run(32,10,22,'H');run(33,9,23,'H');
  run(33,13,19,'s');run(34,11,21,'s');run(34,11,12,'u');
  pair(6,34,8,35,'H','hair');pair(7,36,7,36,'H','hair');
 }else if(v===1){
  for(let y=23;y<=33;y++){const l=y===23?8:y===24?6:5;run(y,l,31-l,'H','hair');if(y<31&&y>23)run(y,l+1,30-l,'h');}
  run(24,9,12,'j');run(24,15,17,'j');run(24,21,23,'j');run(25,7,9,'j');run(26,11,13,'j');run(26,18,20,'j');run(27,8,10,'j');
  rect(6,28,25,32,'H');run(33,8,23,'H');run(33,10,21,'s');run(34,7,24,'s');pair(6,33,7,35,'H','hair');
 }else if(v===2){
  const rows=[[24,11,13],[24,18,20],[25,9,23],[26,7,24],[27,6,25],[28,5,26],[29,4,26],[30,4,27],[31,5,27],[32,5,26]];
  for(const [y,l,r] of rows){run(y,l,r,'H','hair');if(y>25)run(y,l+1,r-1,'h');}
  run(26,10,14,'j');run(27,8,11,'j');run(27,18,21,'j');run(28,6,8,'j');run(29,14,17,'j');run(30,21,24,'j');
  // Individual hanging twists have staggered lengths, dark ends, and clustered upper light.
  for(const [x,top,end] of [[5,31,36],[9,30,37],[13,29,35],[17,30,36],[21,31,37],[25,32,36]]){
   rect(x,top,x+1,end,'H','hair');rect(x,top,x,Math.min(top+2,end-1),'j','hair');
  }
 }else{
  // Rounded scalp with curved cornrows: channels follow the crown, never a flat band.
  for(const [y,l] of [[25,12],[26,9],[27,8],[28,7],[29,6],[30,5],[31,5],[32,5],[33,6],[34,6]]){
   run(y,l,31-l,'H','hair');if(y>25)run(y,l+1,30-l,'t');
  }
  const braids=[[[12,25],[12,26],[13,27],[13,28],[14,29],[14,30],[14,31]],[[18,25],[18,26],[18,27],[18,28],[18,29],[18,30],[18,31]],[[9,27],[9,28],[10,29],[10,30],[11,31],[11,32]],[[22,27],[22,28],[21,29],[21,30],[21,31],[21,32]],[[6,30],[7,31],[8,32],[8,33]],[[25,30],[24,31],[24,32],[23,33]]];
  for(const strand of braids)for(let i=0;i<strand.length;i++){const [x,y]=strand[i];run(y,x,x+1,'H','hair');if(i<2)px(x,y,'j');}
  pair(6,35,7,36,'H','hair');run(33,13,19,'s');run(34,9,22,'s');
 }
 // Eyes are explicit topmost marks; hair never silently shifts their placement.
 pair(12,38,13,41,'O','eyes');
 const rows=a.map(r=>r.join(''));const used=new Set(rows.join('').replaceAll('.',''));
 const model={id:`review.hero.boy.south.idle.r8.${slug}`,frame:[32,64],anchor:[16,64],pose:'front-idle',status:'awaiting-user-art-review',method:'integer-pixel-cluster-authoring',palette:Object.fromEntries([...used].map(k=>[k,palette[k]])),rows,masks:Object.fromEntries(Object.entries(masks).map(([k,m])=>[k,m.map(r=>r.join(''))]))};
 fs.writeFileSync(path.join(root,slug+'.json'),JSON.stringify(model,null,2)+'\n');models.push(model);
}
async function png(m,file){const raw=Buffer.alloc(32*64*4);m.rows.forEach((r,y)=>[...r].forEach((k,x)=>{if(k==='.')return;const i=(y*32+x)*4;Buffer.from(m.palette[k].slice(1),'hex').copy(raw,i);raw[i+3]=255;}));await sharp(raw,{raw:{width:32,height:64,channels:4}}).png().toFile(file);return raw;}
const raws=[];for(const [i,m] of models.entries())raws.push(await png(m,path.join(root,variants[i][0]+'.png')));
async function strip(raws,file){const raw=Buffer.alloc(raws.length*32*64*4);for(let i=0;i<raws.length;i++)for(let y=0;y<64;y++)raws[i].copy(raw,(y*32*raws.length+i*32)*4,y*128,(y+1)*128);await sharp(raw,{raw:{width:32*raws.length,height:64,channels:4}}).png().toFile(file);}
await strip(raws,path.join(root,'four-heroes-native.png'));
if(external){fs.mkdirSync(external,{recursive:true});const ref=JSON.parse(fs.readFileSync(path.join(external,'brendan-reference.json')));const br=await png(ref,path.join(external,'brendan-native.png'));await strip([br,...raws],path.join(external,'five-characters-native.png'));}
console.log('Authored four native 32x64 sprites; 1x strips only. No source sampling, resizing or filtering.');
