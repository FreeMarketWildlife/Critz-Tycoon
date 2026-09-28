// Native still exports: source rows are never scaled to fit the pixel budget.
import {readFile,readdir,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {Raster} from '../raster.mjs';
const source='art/source/characters-v2',out='assets/review/characters-v2',review='docs/reviews/M1-C2';
for(const p of [out,out+'/individual',review])await mkdir(p,{recursive:true});
const order=['hero.boy','hero.girl','mom','kaid','professor','juniper','dr-fern','mina','ollie','aunt-ember','rival-mom','rival-dad'];
const files=(await readdir(source)).filter(p=>p.endsWith('.json'));
const people=(await Promise.all(files.map(async p=>({...JSON.parse(await readFile(source+'/'+p,'utf8')),source:source+'/'+p})))).sort((a,b)=>order.indexOf(a.id)-order.indexOf(b.id));
if(!people.length)throw new Error('No character sources');
const atlas=new Raster(6*24,Math.ceil(people.length/6)*32),dark=new Raster(6*32,Math.ceil(people.length/6)*40),light=new Raster(dark.w,dark.h),assets=[],checks=[];
dark.rect(0,0,dark.w,dark.h,'#17333c');light.rect(0,0,light.w,light.h,'#d6d6b6');
const ids=new Set(),hashes=new Set();
const assert=(pass,name)=>{if(!pass)throw new Error(name);checks.push({name,pass:true});};
for(const [i,p] of people.entries()){
 assert(!ids.has(p.id),p.id+': unique character identity');ids.add(p.id);
 assert(p.rows.length===32&&p.rows.every(r=>r.length===24),p.id+': full24×32 source rows');
 assert(Object.keys(p.palette).length<=15,p.id+': palette at most15 opaque colors');
 const native=new Raster(24,32);let minX=24,minY=32,maxX=-1,maxY=-1,count=0;const colors=new Set(),rowCounts=Array(32).fill(0);
 for(let y=0;y<32;y++)for(let x=0;x<24;x++){const k=p.rows[y][x];if(k==='.')continue;if(!p.palette[k]||!/^#[0-9a-f]{6}$/i.test(p.palette[k]))throw new Error(p.id+`: invalid color at ${x},${y}`);native.dot(x,y,p.palette[k]);colors.add(p.palette[k]);minX=Math.min(x,minX);maxX=Math.max(x,maxX);minY=Math.min(y,minY);maxY=Math.max(y,maxY);count++;rowCounts[y]++;}
 assert(count>0,p.id+': all painted symbols resolve to valid palette colors');
 assert(minX>=2&&maxX<=21&&minY>=5&&maxY===30,p.id+':20×26 budget and common idle baseline');
 assert(rowCounts.slice(minY,31).every(n=>n>0),p.id+': no detached body scanline');
 assert(p.design.headHeight+p.design.bodyHeight===31-minY&&p.design.headHeight>=13&&p.design.headHeight<=16&&p.design.bodyHeight>=9&&p.design.bodyHeight<=11,p.id+': annotated compact head/body construction');
 assert(colors.size<=15,p.id+': actual painted palette budget');
 const hash=createHash('sha256').update(native.p).digest('hex');assert(!hashes.has(hash),p.id+': unique native drawing');hashes.add(hash);
 const col=i%6,row=Math.floor(i/6);atlas.blit(native,col*24,row*32);dark.blit(native,col*32+4,row*40+4);light.blit(native,col*32+4,row*40+4);
 await native.save(`${out}/individual/${p.id}.png`);
 assets.push({id:`character.v2.${p.id}.south.idle`,character:p.id,label:p.label,rect:[col*24,row*32,24,32],anchor:[12,32],direction:'south',pose:'idle',opaqueBBox:[minX,minY,maxX+1,maxY+1],visibleSize:[maxX-minX+1,maxY-minY+1],paintedPixels:count,colorCount:colors.size,colors:[...colors],sha256:hash,png:`individual/${p.id}.png`,source:p.source,design:p.design,status:'awaiting-user-art-review'});
}
await atlas.save(out+'/atlas.png');await dark.save(review+'/lineup-native.png');await dark.scale(4).save(review+'/lineup-4x.png');await dark.scale(8).save(review+'/lineup-8x.png');await light.scale(8).save(review+'/lineup-light-8x.png');
await writeFile(out+'/atlas.json',JSON.stringify({schemaVersion:1,image:'atlas.png',size:[atlas.w,atlas.h],nativeFrame:[24,32],paintedBudget:[20,26],animation:null,status:'still-design-review',assetCount:assets.length,assets},null,2)+'\n');
await writeFile(review+'/native-validation.json',JSON.stringify({passed:checks.length,characterCount:assets.length,checks,atlasSha256:createHash('sha256').update(await readFile(out+'/atlas.png')).digest('hex')},null,2)+'\n');
console.log(`${assets.length} stills exported; ${checks.length} native checks passed.`);
