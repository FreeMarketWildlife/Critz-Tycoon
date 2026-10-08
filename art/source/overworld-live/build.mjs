import {APPLE_POSITIONS} from '../../../src/fruit-trees.js';
// Append-only runtime edition of the approved master. Original cells stay exact.
import {Raster} from '../raster.mjs';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
const out='assets/playable/overworld';await mkdir(out,{recursive:true});
const source=JSON.parse(await readFile('art/source/overworld-v1/pixels.json','utf8'));
const original=JSON.parse(await readFile('assets/review/overworld-v1/master.json','utf8'));
const P=JSON.parse(await readFile('assets/review/overworld-v1/palette.json','utf8'));
const tiles=original.tiles.map(t=>{const p=source.tiles.find(s=>s.id===t.id),r=new Raster(32,32);p.rows.forEach((row,y)=>row.forEach((v,x)=>{if(v)r.dot(x,y,source.colors[v]);}));return {...t,r};});
const ids=new Map(tiles.map(t=>[t.id,t]));let cursor=Math.ceil((Math.max(...tiles.map(t=>t.index))+1)/32)*32;
const sections=[...original.sections],assemblies={...original.assemblies};
function group(name){cursor=Math.ceil(cursor/32)*32;sections.push({name,start:cursor});}
function add(id,r,layer='decal'){if(ids.has(id))throw Error(id);const t={id,index:cursor++,x:0,y:0,width:32,height:32,layer,r};t.x=t.index%32*32;t.y=Math.floor(t.index/32)*32;tiles.push(t);ids.set(id,t);return id;}
function slice(id,r,layer='object'){const rows=[];for(let y=0;y<r.h;y+=32){const row=[];for(let x=0;x<r.w;x+=32)row.push(add(`${id}.${x/32}.${y/32}`,r.crop(x,y,32,32),layer));rows.push(row);}assemblies[id]=rows;}
function clone(id){return ids.get(id).r.crop(0,0,32,32);}
function hex(r,x,y){return '#'+r.p.subarray((y*32+x)*4,(y*32+x)*4+3).toString('hex');}
group('Living water · four coordinated phases; banks stay fixed');
for(let f=1;f<4;f++)for(const t of original.tiles.filter(t=>t.terrain==='water')){
 const r=clone(t.id),mask=[];
 // Keep the full five-pixel shoreline band unchanged. Only interior water moves.
 for(let y=0;y<32;y++)for(let x=0;x<32;x++){
  const wet=P.water.slice(1).includes(hex(r,x,y));
  let deep=wet&&x>0&&y>0&&x<31&&y<31;for(const [dx,dy]of [[-4,0],[4,0],[0,-4],[0,4]]){const xx=x+dx,yy=y+dy;if(xx>=0&&xx<32&&yy>=0&&yy<32&&!P.water.slice(1).includes(hex(r,xx,yy)))deep=false;}
  if(deep)mask.push([x,y]);
 }
 for(const [x,y]of mask){let c=P.water[2];for(const [sx,sy,w]of [[3,7,7],[20,22,6]]){const yy=(sy+f*2)%32;if(y===yy&&x>=sx&&x<=sx+w)c=P.water[3];if(y===(yy+3)%32&&x>sx&&x<sx+w)c=P.water[1];}r.dot(x,y,c);}
 add(`anim.${t.id}.${f}`,r,'ground');
}
group('Wind flowers · rooted stems and alternating heads');
for(let v=0;v<6;v++)for(let f=1;f<=2;f++){
 const old=clone(`flowers.${v}`),r=new Raster(32,32),lean=f===1?1:-1;
 for(let y=0;y<32;y++)for(let x=0;x<32;x++){const i=(y*32+x)*4;if(!old.p[i+3])continue;const c=hex(old,x,y),shift=P.flower.includes(c)?lean:0;r.dot(x+shift,y,c);}
 add(`anim.flowers.${v}.${f}`,r);
}
group('Tall grass · resting canopy, parted step frames and foreground blades');
for(let f=0;f<4;f++){
 const r=new Raster(32,32);
 for(let y=10;y<=30;y+=10)for(let x=4;x<32;x+=8){const lean=f===1?-3:f===2?3:0,h=f===3?5:8;
  r.poly([[x-3,y],[x-4+lean,y-h+2],[x,y-3],[x+lean,y-h-2],[x+3,y-3],[x+4+lean,y-h],[x+3,y]],P.leaf[2]);r.line(x,y,x-3+lean,y-h+2,P.leaf[1]);r.line(x+1,y,x+4+lean,y-h,P.leaf[3]);r.line(x,y,x+lean,y-h-2,P.leaf[2]);r.line(x+1,y-2,x+1+lean,y-h,P.leaf[4]);r.dot(x+1+lean,y-h-1,P.leaf[5]);}
 add(`grass.living.${f}`,r);
 const front=r.crop(0,0,32,32);for(let y=0;y<20;y++)front.rect(0,y,32,1,'transparent');add(`grass.front.${f}`,front,'foreground');
}
group('Woodland history · hollow log ends and repeating mossy bark');
const log=new Raster(96,32);
log.oval(1,7,93,24,P.wood[0]);log.rect(16,5,61,24,P.wood[1]);log.rect(16,6,60,8,P.wood[3]);log.rect(16,14,62,10,P.wood[2]);
for(const [x,y,w]of [[18,10,24],[50,8,22],[26,18,33],[59,25,18],[20,27,22]]){log.rect(x,y,w,2,P.wood[0]);log.rect(x,y-1,w-2,1,P.wood[4]);}
for(const x of [2,76]){log.oval(x,4,19,27,P.wood[0]);log.oval(x+1,5,17,24,P.wood[4]);log.oval(x+4,8,12,19,P.wood[1]);log.oval(x+5,9,10,17,P.wood[0]);log.line(x+4,8,x+8,11,P.wood[2]);log.line(x+15,23,x+17,26,P.wood[1]);}
for(const [x,y,w]of [[20,4,14],[44,6,18],[61,3,11]]){log.rect(x,y,w,4,P.leaf[2]);log.rect(x+2,y,w-4,2,P.leaf[4]);log.rect(x+4,y-1,3,2,P.leaf[5]);}
log.rect(62,22,2,7,P.plaster[2]);log.oval(57,19,10,5,P.clay[3]);log.dot(61,20,P.plaster[4]);slice('log.hollow',log);
const stump=new Raster(32,32);stump.poly([[7,12],[25,12],[26,26],[30,29],[21,30],[10,29],[3,30],[6,24]],P.wood[1]);stump.rect(9,13,14,15,P.wood[2]);stump.rect(11,15,2,12,P.wood[3]);stump.oval(5,7,23,14,P.wood[0]);stump.oval(6,7,21,12,P.wood[4]);stump.oval(9,9,15,8,P.wood[2]);stump.oval(11,10,11,5,P.wood[3]);stump.line(16,10,16,13,P.wood[1]);add('stump.old',stump,'object');
const litter=new Raster(32,32);for(const [x,y]of [[3,6],[20,4],[12,16],[25,22],[5,27]]){litter.oval(x,y,7,4,P.earth[2]);litter.line(x+1,y+2,x+5,y+1,P.earth[4]);}add('leaves.litter',litter);
const fern=new Raster(32,32);for(const [x,y]of [[16,28],[9,27],[24,29]])for(let j=0;j<5;j++){fern.line(x,y,x+(j-2)*3,y-12+j,P.leaf[2]);fern.line(x+(j-2)*3,y-12+j,x+(j-2)*3+3,y-10+j,P.leaf[4]);}add('fern.wild',fern);
const marker=new Raster(32,32);marker.poly([[9,5],[22,5],[26,29],[5,29]],P.stone[0]);marker.poly([[10,6],[20,6],[22,26],[7,26]],P.stone[3]);marker.rect(10,10,9,2,P.stone[1]);marker.line(14,10,14,18,P.stone[1]);marker.line(11,13,14,10,P.stone[1]);marker.line(17,13,14,10,P.stone[1]);marker.rect(8,24,9,3,P.leaf[2]);add('marker.north',marker,'object');
group('Waterworks · flowing falls, spray and fountain droplets');
for(let f=1;f<4;f++)for(let row=0;row<3;row++){
 const r=clone(`waterfall.0.${row}`);for(let x=5;x<28;x+=6){r.rect(x,0,2,32,P.water[3]);for(let y=(f*7+x)%19;y<32;y+=19)r.rect(x,y,2,6,P.water[5]);}add(`anim.waterfall.${row}.${f}`,r,'object');
}
for(let f=0;f<4;f++){const r=new Raster(32,32);for(const [x,y]of [[5,7],[22,12],[10,23],[25,27]]){r.rect(x,(y+f*4)%29,2,3,P.water[5]);}add(`water.spray.${f}`,r,'foreground');}
group('Liarsville mill · turning wheel quarters and old clock plaque');
for(let f=0;f<4;f++){
 const r=new Raster(64,64);r.oval(3,4,58,58,P.wood[0]);r.oval(5,5,54,54,P.wood[3]);r.oval(9,9,46,46,'transparent');r.oval(10,11,44,44,P.wood[1]);r.oval(13,13,38,38,'transparent');
 for(let i=0;i<8;i++){const a=i*Math.PI/4+f*Math.PI/16,x=Math.round(32+24*Math.cos(a)),y=Math.round(32+24*Math.sin(a));r.line(31,32,x-1,y,P.wood[0]);r.line(32,32,x,y,P.wood[3]);r.line(33,32,x+1,y,P.wood[4]);r.rect(x-3,y-2,6,4,P.wood[1]);r.rect(x-3,y-2,6,1,P.wood[4]);}
 r.oval(26,26,12,12,P.stone[0]);r.oval(28,27,8,8,P.stone[2]);r.oval(29,28,4,4,P.stone[4]);slice(`mill.wheel.${f}`,r);
}
const clock=new Raster(32,32);clock.rect(2,2,28,28,P.stone[0]);clock.rect(3,3,26,26,P.stone[3]);clock.oval(5,5,22,22,P.wood[1]);clock.oval(7,7,18,18,P.plaster[4]);for(const [x,y]of [[15,8],[23,15],[15,23],[8,15]])clock.rect(x,y,2,2,P.wood[1]);clock.line(16,16,16,10,P.wood[0]);clock.line(16,16,21,18,P.wood[0]);add('clock.plaque',clock,'object');
group('Rootport storefronts · original service pictograms');
for(const kind of ['critz','vet','pharmacy','bike','glass']){
 const r=new Raster(32,32);r.rect(1,8,30,23,P.wood[0]);r.rect(2,9,28,21,P.wood[3]);r.rect(3,10,26,19,P.plaster[4]);r.rect(3,10,26,1,P.wood[4]);
 if(kind==='critz'){r.oval(8,13,16,10,P.leaf[2]);r.line(9,24,22,14,P.leaf[0]);r.line(14,20,14,15,P.leaf[4]);}
 if(kind==='vet'){r.rect(13,12,6,15,P.clay[2]);r.rect(8,16,16,6,P.clay[2]);r.rect(14,12,2,13,P.clay[4]);}
 if(kind==='pharmacy'){r.oval(6,13,20,12,P.teal[0]);r.rect(10,14,7,10,P.teal[3]);r.rect(17,14,6,10,P.plaster[3]);r.line(17,14,17,23,P.teal[0]);}
 if(kind==='bike'){for(const x of [5,20]){r.oval(x,19,9,9,P.stone[0]);r.oval(x+2,21,5,5,P.plaster[4]);}r.line(9,23,14,15,P.teal[1]);r.line(14,15,24,23,P.teal[1]);r.line(9,23,24,23,P.teal[1]);r.line(14,15,19,15,P.teal[1]);r.rect(12,13,5,2,P.stone[0]);}
 if(kind==='glass'){r.rect(7,15,18,13,P.glass[0]);r.rect(9,17,14,9,P.glass[2]);r.line(10,24,17,18,P.glass[3]);r.line(23,11,23,17,P.teal[2]);r.line(20,14,26,14,P.teal[2]);}
 add(`shop.sign.${kind}`,r,'object');
}
group('Contact edges · solid foundations joined to grass, path or paving');
const contactSources=original.tiles.filter(t=>/^wall\.(plaster|timber|stone)\.1\./.test(t.id)||/^windowbox\.(plaster|timber|stone)\.0\.1$/.test(t.id)||/^door\.wood\.(open|closed)\.0\.1$/.test(t.id));
for(const surface of ['grass','path','paving'])for(const t of contactSources){
 const r=clone(t.id),ground=clone(surface==='grass'?'ground.grass.0':`${surface}.255`);
 // Four native pixels of real surrounding ground remain inside the solid cell.
 for(let y=28;y<32;y++)for(let x=0;x<32;x++)r.p.set(ground.p.subarray((y*32+x)*4,(y*32+x)*4+4),(y*32+x)*4);
 if(t.id.startsWith('door.')){r.rect(2,25,28,2,P.stone[4]);r.rect(2,27,28,2,P.stone[1]);}
 else {r.rect(0,23,32,2,P.stone[4]);r.rect(0,25,32,2,P.stone[2]);r.rect(0,27,32,1,P.stone[0]);if(surface==='grass')for(const x of [3,21]){r.dot(x,29,P.grass[1]);r.dot(x+1,28,P.grass[2]);}}
 const id=add(`contact.${t.id}.${surface}`,r,'object');Object.assign(ids.get(id),{blocked:true,contact:{source:t.id,surface,solidThroughRow:27,groundRows:4}});
}
group('Tree contact · spreading roots beneath retained canopies');
for(const type of ['broadleaf','cypress']){
 const oldRows=assemblies[`tree.${type}`],row=oldRows.length-1,root=new Raster(64,32);
 oldRows[row].forEach((id,x)=>root.blit(clone(id),x*32,0));
 root.poly([[2,29],[6,25],[18,24],[25,20],[38,20],[45,24],[58,25],[62,29],[59,31],[5,31]],P.earth[0]);
 root.poly([[5,28],[17,26],[27,20],[37,20],[47,26],[59,28],[56,30],[8,30]],P.earth[2]);
 for(const [a,b,c,d]of [[28,20,7,28],[29,21,20,29],[36,20,56,28],[35,22,44,29]]){root.line(a,b,c,d,P.wood[0]);root.line(a,b-1,c,d-1,P.wood[2]);}
 root.rect(27,17,11,9,P.wood[1]);root.rect(29,17,3,8,P.wood[3]);
 for(const [x,y]of [[4,29],[12,30],[48,30],[58,29]]){root.rect(x,y,3,1,P.grass[1]);root.dot(x+1,y-1,P.grass[3]);}
 const bottom=[0,1].map(x=>add(`contact.tree.${type}.${x}`,root.crop(x*32,0,32,32),'foreground'));
 assemblies[`tree.${type}.rooted`]=[...oldRows.slice(0,-1),bottom];
}
group('Interior contact · skirting, side returns and visible south boundary');
for(const floor of ['wood','tile']){
 const r=new Raster(32,32);r.rect(0,0,32,32,'#deded0');r.rect(0,0,32,2,'#ece8d2');r.rect(0,20,32,8,'#9aa397');r.rect(0,20,32,2,'#c3c9b3');r.rect(0,26,32,2,'#737183');r.rect(0,28,32,4,floor==='wood'?'#dbc298':'#c7d6c5');r.rect(0,28,32,1,floor==='wood'?'#aa9274':'#96aaa1');add(`interior.base.${floor}`,r,'ground');
}
for(const side of ['left','right']){
 const r=new Raster(32,32);r.rect(0,0,32,32,'#b0bbaa');r.rect(2,0,28,32,'#c6d1bc');const x=side==='left'?28:0;r.rect(x,0,4,32,'#737183');r.rect(side==='left'?26:4,0,2,32,'#e0e2c5');add(`interior.side.${side}`,r,'ground');
}
const rim=new Raster(32,32);rim.rect(0,0,32,32,'#223038');rim.rect(0,0,32,2,'#e0e2c5');rim.rect(0,2,32,6,'#737183');rim.rect(0,8,32,2,'#344b50');add('interior.front.rim',rim,'ground');

group('Orchard apples · ripe crown, bare tree and falling pickup');
// Reuse the rooted broadleaf frame and its exact ground contact. Only fruit is new.
const appleBare=new Raster(64,64);assemblies['tree.broadleaf.rooted'].forEach((row,y)=>row.forEach((id,x)=>appleBare.blit(clone(id),x*32,y*32)));
assemblies['tree.apple.bare']=assemblies['tree.broadleaf.rooted'];
function paintApple(r,x,y){
 r.rect(x+4,y,1,3,P.wood[0]);r.line(x+5,y+1,x+8,y,P.leaf[1]);r.line(x+5,y,x+7,y-1,P.leaf[4]);
 r.poly([[x+1,y+2],[x+3,y+1],[x+5,y+2],[x+7,y+1],[x+9,y+3],[x+8,y+8],[x+6,y+10],[x+3,y+9],[x+1,y+6]],'#633b3b');
 r.poly([[x+2,y+3],[x+4,y+2],[x+5,y+3],[x+7,y+2],[x+8,y+4],[x+7,y+8],[x+4,y+8],[x+2,y+6]],'#c95445');r.rect(x+2,y+3,2,3,'#ef9163');r.dot(x+3,y+3,'#ffe0a0');r.rect(x+6,y+5,2,2,'#9b3e3c');
}
const appleRipe=appleBare.crop(0,0,64,64);for(const [x,y]of APPLE_POSITIONS)paintApple(appleRipe,x-5,y-5);slice('tree.apple.ripe',appleRipe,'foreground');
const appleIcon=new Raster(32,32);paintApple(appleIcon,11,11);add('fruit.apple',appleIcon,'foreground');

const atlas=new Raster(1024,Math.max(1024,Math.ceil(cursor/32)*32));for(const t of tiles)atlas.blit(t.r,t.x,t.y);await atlas.save(`${out}/master.png`);
const manifest={...original,assetId:'critz.overworld.live.v4',approval:'Base kit selected by user; M1.FR1 orchard additions and integrated world await feedback',imageWidth:atlas.w,imageHeight:atlas.h,sections,assemblies,tiles:tiles.map(({r,...t})=>t),animation:{stepSeconds:16*280896/16777216,waterFrames:4,flowerSequence:[0,1,0,2],grass:'movement-triggered, one-tile response; foreground foot overlap'},collision:'Authored map cells, independent of appearance'};
await writeFile(`${out}/master.json`,JSON.stringify(manifest,null,2)+'\n');
await writeFile(`${out}/palette.json`,JSON.stringify(P,null,2)+'\n');
await writeFile(`${out}/master.tsj`,JSON.stringify({type:'tileset',version:'1.10',name:'Critz overworld live v4',tilewidth:32,tileheight:32,tilecount:atlas.w*atlas.h/1024,columns:32,image:'master.png',imagewidth:atlas.w,imageheight:atlas.h,tiles:tiles.map(t=>({id:t.index,properties:[{name:'assetId',type:'string',value:t.id}]}))},null,2)+'\n');
console.log(JSON.stringify({original:original.tiles.length,total:tiles.length,allocated:cursor,size:[atlas.w,atlas.h]}));
