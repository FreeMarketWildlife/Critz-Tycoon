import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {describe,validateProject} from '../../../sprite-editor/model.js';
const require=createRequire(import.meta.url),sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const root=path.dirname(new URL(import.meta.url).pathname),repo=path.resolve(root,'../../..'),out=path.join(repo,'assets/review/hero-idle-r9');
const input=JSON.parse(fs.readFileSync(path.join(root,'user-template.rle.json'))),palette=input.palette;
const source=input.frames[0].rows.map(row=>{const a=[];for(let i=0;i<row.length;i+=2)a.push(...Array(row[i+1]).fill(row[i]));if(a.length!==32)throw Error('Invalid row');return a;});
const external=process.argv[2];if(external&&path.resolve(external).startsWith(repo+path.sep))throw Error('Reference must stay external');
const slugs=['a-afro','b-flat-top','c-twists','d-cornrows'],all=[],metadata=[];
for(let v=0;v<4;v++){
 const a=source.map(r=>r.map(k=>k?17:0)),hair=Array.from({length:64},()=>Array(32).fill(false));
 const set=(x,y,k)=>{if(a[y][x])a[y][x]=k;};
 const run=(y,l,r,k)=>{for(let x=l;x<=r;x++)set(x,y,k);};
 const rect=(l,t,r,b,k)=>{for(let y=t;y<=b;y++)run(y,l,r,k);};
 const pair=(l,t,r,b,k)=>{rect(l,t,r,b,k);rect(31-r,t,31-l,b,k);};
 const cloth=[4,3,1,10][v],light=[5,19,2,11][v],shade=[21,17,15,9][v];
 // Preserve every template anatomy cell. Change paint, never scale or reconstruct its body.
 for(let y=26;y<62;y++)for(let x=0;x<32;x++)if(a[y][x]){
  if(y<=45)a[y][x]=17;
  else if(y<=54)a[y][x]=(x<9||x>22)?17:cloth;
  else if(y<=57)a[y][x]=v===3?23:26;
  else a[y][x]=13;
 }
 // Rounded face planes, compact ears and exact exported eye rectangles.
 for(let y=30;y<=43;y++){
  const xs=source[y].map((k,x)=>k?x:-1).filter(x=>x>=0),l=Math.min(...xs),r=Math.max(...xs);
  run(y,l+1,l+2,18);run(y,r-2,r-1,16);
 }
 run(43,10,21,17);run(44,11,20,16);run(45,12,19,16);
 pair(5,37,6,39,16);set(5,37,18);pair(12,38,13,41,8);
 // Raglan sleeves, one-pixel cuffs and matched hands at the user's actual positions.
 for(let y=46;y<=49;y++)for(let x=0;x<32;x++)if(a[y][x]&&(x<11||x>20))a[y][x]=v<2?19:cloth;
 pair(6,49,8,49,v<2?18:shade);
 pair(5,50,7,52,17);rect(5,50,7,50,18);rect(24,52,26,52,16);
 // Shirt light/shadow clusters, no copied 2x2 source blocks.
 rect(10,48,10,52,light);rect(21,48,21,53,shade);run(53,11,20,shade);
 if(v===0){run(47,13,17,light);run(48,11,12,light);run(54,12,19,shade);}
 if(v===1||v===3){
  rect(14,47,17,53,19);run(53,14,17,18);rect(13,49,13,53,shade);rect(18,49,18,53,shade);
  run(47,11,12,light);run(47,19,20,light);set(12,48,light);set(19,48,light);
  if(v===3){run(50,10,11,11);run(50,20,21,11);}
 }else if(v===2){for(const y of [48,51]){run(y,10,21,19);run(y+1,11,20,19);}run(47,13,19,2);}
 // Only single-pixel contact seams; do not preserve the template's wide dark belt.
 run(46,13,18,15);pair(8,50,8,52,15);
 for(let y=55;y<=57;y++){run(y,9,14,v===3?23:v===1?26:9);run(y,17,22,v===3?23:v===1?26:9);}
 pair(10,55,13,55,v===3?24:v===1?27:10);run(56,15,16,v===3?22:26);run(57,15,16,26);
 // Retain the user's shoe silhouettes, refine their paint and dark contact edges.
 pair(10,57,13,57,16);pair(9,58,12,58,cloth);pair(9,59,13,60,13);pair(12,60,13,60,19);
 // Hairstyles have their own native-cell contours over the symmetric skull.
 function hr(y,l,r,k){for(let x=l;x<=r;x++){a[y][x]=v<3?(k===15?14:k===16?15:k):k;hair[y][x]=true;}}
 function hb(l,t,r,b,k){for(let y=t;y<=b;y++)hr(y,l,r,k);}
 if(v===0){
  for(const [y,l] of [[24,12],[25,9],[26,8],[27,7],[28,6],[29,5],[30,5],[31,4],[32,4],[33,5]])hr(y,l,31-l,15);
  hr(25,12,18,16);hr(26,10,16,16);hr(27,8,12,16);hr(28,7,9,16);hr(28,18,21,16);hr(29,21,23,16);
  hr(32,11,20,14);hr(33,10,12,14);hr(33,20,22,14);hb(6,34,8,35,15);hb(23,34,25,35,15);
 }else if(v===1){
  for(let y=23;y<=32;y++)hr(y,y===23?8:y===24?6:5,y===23?23:y===24?25:26,15);
  hr(24,9,12,16);hr(24,16,18,16);hr(25,7,9,16);hr(25,21,23,16);hr(26,11,13,16);hr(27,17,19,16);
  hr(32,9,22,14);hb(6,33,7,35,15);hb(24,33,25,35,15);
 }else if(v===2){
  for(const [y,l] of [[25,9],[26,7],[27,6],[28,5],[29,4],[30,4],[31,5],[32,5]])hr(y,l,31-l,15);
  hr(24,11,13,15);hr(24,18,20,15);hr(26,10,14,16);hr(27,8,10,16);hr(27,18,21,16);hr(28,6,8,16);
  for(const [x,t,b] of [[5,31,36],[9,30,37],[13,29,35],[17,30,36],[21,31,37],[25,32,36]]){hb(x,t,x+1,b,15);hb(x,t,x,Math.min(t+2,b-1),16);hr(b,x,x+1,14);}
 }else{
  for(const [y,l] of [[25,12],[26,9],[27,8],[28,7],[29,6],[30,5],[31,5],[32,5]])hr(y,l,31-l,16);
  for(const strand of [[[12,25],[12,26],[13,27],[13,28],[14,29],[14,30],[14,31]],[[18,25],[18,26],[18,27],[18,28],[18,29],[18,30],[18,31]],[[9,27],[9,28],[10,29],[10,30],[11,31],[11,32]],[[22,27],[22,28],[21,29],[21,30],[21,31],[21,32]],[[6,30],[7,31],[8,32],[8,33]],[[25,30],[24,31],[24,32],[23,33]]])for(const [x,y]of strand)hr(y,x,x,14);
  hb(6,34,7,35,15);hb(24,34,25,35,15);
 }
 // Exactly one occupied-cell boundary layer. No stroke dilation or doubled outline.
 const occupied=a.map(r=>r.map(Boolean)),outline=occupied.map((r,y)=>r.map((on,x)=>on&&[[1,0],[-1,0],[0,1],[0,-1]].some(([dx,dy])=>!occupied[y+dy]?.[x+dx])));
 for(let y=0;y<64;y++)for(let x=0;x<32;x++)if(outline[y][x])a[y][x]=hair[y][x]?14:y<46?15:26;
 pair(12,38,13,41,8);
 const project={format:'fmw-sprite',version:1,name:['Hero · Afro','Hero · Flat-top','Hero · Twists','Hero · Cornrows'][v],preset:'character',width:32,height:64,palette,bank:'wildlife',notes:'Front idle. User RLE anatomy; one-native-pixel exterior outline. Unapproved art review; animation deferred.',frames:[{name:'Idle south',ticks:8,pixels:a.flat()}]};
 validateProject(project,new Set(palette.slice(1)));
 const slug=slugs[v];fs.writeFileSync(path.join(root,slug+'.sprite.json'),JSON.stringify(project,null,2)+'\n');fs.writeFileSync(path.join(root,slug+'.rle.json'),describe(project)+'\n');
 fs.writeFileSync(path.join(root,slug+'-masks.json'),JSON.stringify({bodyTemplate:source.map(r=>r.map(k=>k?1:0).join('')),hair:hair.map(r=>r.map(Number).join('')),outline:outline.map(r=>r.map(Number).join(''))},null,2)+'\n');
 const raw=Buffer.from(a.flatMap(r=>r.flatMap(k=>k?[...Buffer.from(palette[k].slice(1),'hex'),255]:[0,0,0,0])));
 await sharp(raw,{raw:{width:32,height:64,channels:4}}).png().toFile(path.join(out,slug+'.png'));all.push(raw);
 metadata.push({id:`hero.boy.idle.south.${slug}`,file:slug+'.png',source:`../../../art/source/hero-idle-r9/${slug}.sprite.json`,frame:[32,64],anchor:[16,64],direction:'south',state:'idle',animation:false,status:'awaiting-user-visual-review',outlineThickness:1});
}
async function strip(raws,file){const b=Buffer.alloc(raws.length*32*64*4);raws.forEach((r,i)=>{for(let y=0;y<64;y++)r.copy(b,(y*raws.length*32+i*32)*4,y*128,(y+1)*128);});await sharp(b,{raw:{width:raws.length*32,height:64,channels:4}}).png().toFile(file);}
await strip(all,path.join(out,'four-idles.png'));fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify({schemaVersion:1,frame:[32,64],runtimeIntegrated:false,assets:metadata},null,2)+'\n');
if(external){fs.mkdirSync(external,{recursive:true});const r=JSON.parse(fs.readFileSync('/Users/tanoshi/.codex/visualizations/2026/10/03/hero-revision-8/brendan-reference.json'));const br=Buffer.from(r.rows.flatMap(row=>[...row].flatMap(k=>k==='.'?[0,0,0,0]:[...Buffer.from(r.palette[k].slice(1),'hex'),255])));await strip([br,...all],path.join(external,'five-idles-native.png'));}
console.log('Four PNGs, native strips, editor projects, exact RLE, masks and metadata exported.');
