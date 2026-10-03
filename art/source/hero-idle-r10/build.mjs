import fs from 'node:fs';import path from 'node:path';import {createRequire} from 'node:module';import {describe,validateProject} from '../../../sprite-editor/model.js';
const require=createRequire(import.meta.url),sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const root=path.dirname(new URL(import.meta.url).pathname),repo=path.resolve(root,'../../..'),out=path.join(repo,'assets/review/hero-idle-r10');
const source=JSON.parse(fs.readFileSync(path.join(repo,'docs/reviews/M1-C4/revision-7/c-twists.json')));
const a=source.rows.map(r=>[...r].map(k=>k==='.'?null:source.palette[k]));const mask=a.map(r=>r.map(Boolean));
const outline=mask.map((r,y)=>r.map((v,x)=>v&&[[1,0],[-1,0],[0,1],[0,-1]].some(([dx,dy])=>!mask[y+dy]?.[x+dx])));
const changes=[];
for(let y=0;y<64;y++)for(let x=0;x<32;x++){
 const old=a[y][x];if(!old)continue;
 const eye=(x===12||x===13||x===18||x===19)&&y>=38&&y<=41;
 if(outline[y][x])a[y][x]='#000000';
 else if(y>=38&&!eye){
  const rgb=[...Buffer.from(old.slice(1),'hex')];
  if(Math.max(...rgb)<80){
   if(y<=44)a[y][x]='#764b35';
   else if(y<=48&&y>=45&&x>=12&&x<=19)a[y][x]=old; // preserve neck contact shading
   else if(y<=53)a[y][x]=(x<9||x>22)?'#92583c':'#36343e';
   else if(y<=57)a[y][x]='#2e3d5d';
   else if(y===58)a[y][x]='#92583c';
   else a[y][x]='#343d50';
  }
 }
 if(a[y][x]!==old)changes.push({x,y,from:old,to:a[y][x],reason:outline[y][x]?'one-pixel black exterior':'repaint inner dark band as material shadow'});
}
const palette=[null,...new Set(a.flat().filter(Boolean))],pixels=a.flat().map(c=>palette.indexOf(c));
const p={format:'fmw-sprite',version:1,name:'Boy Hero · Orange stripes and twists',preset:'character',width:32,height:64,palette,bank:'custom',notes:'32x64 front idle; source-faithful R7 twists cleanup. 2 transparent bottom rows. Symmetric anatomy; retained original hair/color variation. One-pixel black outer boundary. No palette reduction. Awaiting visual review.',frames:[{name:'Idle south',ticks:8,pixels}]};
validateProject(p,new Set(palette.slice(1)));
fs.writeFileSync(path.join(root,'hero.sprite.json'),JSON.stringify(p,null,2)+'\n');fs.writeFileSync(path.join(root,'hero.rle.json'),describe(p)+'\n');fs.writeFileSync(path.join(root,'changes.json'),JSON.stringify(changes,null,2)+'\n');fs.writeFileSync(path.join(root,'outline.json'),JSON.stringify(outline.map(r=>r.map(Number).join('')),null,2)+'\n');
const raw=Buffer.from(a.flat().flatMap(c=>c?[...Buffer.from(c.slice(1),'hex'),255]:[0,0,0,0]));await sharp(raw,{raw:{width:32,height:64,channels:4}}).png().toFile(path.join(out,'hero.png'));
fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify({schemaVersion:1,id:'hero.boy.orange-stripes.idle.south',file:'hero.png',frame:[32,64],anchor:[16,64],transparentBottomRows:2,direction:'south',state:'idle',animation:false,status:'awaiting-user-visual-review',runtimeIntegrated:false,paletteCount:palette.length-1,source:'../../../art/source/hero-idle-r10/hero.sprite.json'},null,2)+'\n');
// Countable review proof, generated from these exact native cells, never baked into hero.png.
let svg='<svg xmlns="http://www.w3.org/2000/svg" width="460" height="880"><rect width="460" height="880" fill="#faf7ef"/><g font-family="Arial" fill="#29383d"><text x="35" y="28" font-size="18">Boy Hero · 32×64 · front idle</text><text x="35" y="50" font-size="13">One cell = one pixel · 2 empty bottom rows</text><rect x="50" y="78" width="384" height="768" fill="#edf0eb"/>';
for(let y=0;y<64;y++)for(let x=0;x<32;x++)if(a[y][x])svg+=`<rect x="${50+x*12}" y="${78+y*12}" width="12" height="12" fill="${a[y][x]}"/>`;
for(let x=0;x<=32;x++)svg+=`<path d="M${50+x*12} 78v768" stroke="#526c75" stroke-opacity=".19"/>`;
for(let y=0;y<=64;y++){const h=64-y,major=h%10===0||h===64;svg+=`<path d="M50 ${78+y*12}h384" stroke="#526c75" stroke-opacity="${major?.8:.19}"/>`;if(major)svg+=`<text x="42" y="${82+y*12}" text-anchor="end" font-size="12">${h}</text>`;}
svg+='<path d="M242 73v778" stroke="#cc3e80"/>';for(const x of [0,10,16,20,30,32])svg+=`<text x="${50+x*12}" y="867" text-anchor="middle" font-size="12">${x}</text>`;svg+='</g></svg>';
await sharp(Buffer.from(svg)).png().toFile(path.join(repo,'docs/reviews/M1-C4/revision-10/hero-grid.png'));
console.log(JSON.stringify({changes:changes.length,palette:palette.length-1,pixels:pixels.filter(Boolean).length}));
