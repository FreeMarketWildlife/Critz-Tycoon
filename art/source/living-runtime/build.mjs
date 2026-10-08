// Lossless packing only. The user-selected C7 source files remain immutable.
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {Raster} from '../raster.mjs';
const source=JSON.parse(await readFile('assets/review/living-collection-v1/manifest.json','utf8'));
const items=[...source.characters,...source.critters,...source.habitats];
for(const h of source.habitats)for(const layer of ['back','foreground','world-prop'])items.push({slug:`${h.slug}-${layer}`,source:`art/source/living-collection-v1/${h.slug}-${layer}.sprite.json`,kind:layer});
const assets=[],frames=[];let x=0,y=0,row=0;
for(const item of items){const s=JSON.parse(await readFile(item.source,'utf8'));for(let i=0;i<s.frames.length;i++){
 if(x+s.width>1024){x=0;y+=row;row=0;}const pixels=new Raster(s.width,s.height);
 s.frames[i].pixels.forEach((v,n)=>{if(v)pixels.dot(n%s.width,Math.floor(n/s.width),s.palette[v]);});
 const hash=createHash('sha256').update(pixels.p).digest('hex');if(item.frames&&hash!==item.frames[i].rgbaSHA256)throw Error(`Source drift: ${item.slug}/${i}`);
 assets.push({id:`${item.slug}.${i}`,rect:[x,y,s.width,s.height],anchor:[s.width/2,s.height],ticks:s.frames[i].ticks,rgbaSHA256:hash,source:item.source,sourceFrame:i});frames.push({pixels,x,y});x+=s.width;row=Math.max(row,s.height);
}}
const height=Math.ceil((y+row)/64)*64,sheet=new Raster(1024,height);for(const f of frames)sheet.blit(f.pixels,f.x,f.y);
await mkdir('assets/playable/living',{recursive:true});await sheet.save('assets/playable/living/atlas.png');
await writeFile('assets/playable/living/atlas.json',JSON.stringify({schemaVersion:1,image:'atlas.png',size:[1024,height],provenance:'M1.C7 living-collection-v1: exact indexed RGBA, no resampling',assets},null,2)+'\n');
console.log(`Packed ${assets.length} exact frames into 1024×${height}`);
