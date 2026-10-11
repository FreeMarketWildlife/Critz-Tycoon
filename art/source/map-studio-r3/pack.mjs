import {readFile,writeFile} from 'node:fs/promises';
import {spawnSync} from 'node:child_process';
import {Raster} from '../raster.mjs';
import {compileContactPixels} from '../../../src/contact-rules.js';
const out='assets/review/map-studio-r3',items=JSON.parse(await readFile(out+'/sources.json','utf8'));
const entries=[],images=[];let x=0,y=0,row=0;
for(const item of items){const decoded=spawnSync(process.env.PYTHON_BIN||'python3',['-c','from PIL import Image;import sys;sys.stdout.buffer.write(Image.open(sys.argv[1]).convert("RGBA").tobytes())',out+'/'+item.image]);if(decoded.status)throw Error(decoded.stderr.toString());let r=new Raster(item.w,item.h);r.p.set(decoded.stdout);let offsetY=0;if(item.footprint&&!item.registered){const compiled=compileContactPixels(r.p,r.w,r.h,item);r=new Raster(compiled.w,compiled.h);r.p.set(compiled.pixels);offsetY=compiled.offsetY;item.contact=compiled.contact;}if(x+r.w>1024){x=0;y+=row;row=0;}entries.push({...item,rect:[x,y,r.w,r.h],offsetY});images.push(r);x+=r.w;row=Math.max(row,r.h);}
const sheet=new Raster(1024,y+row);entries.forEach((e,i)=>sheet.blit(images[i],e.rect[0],e.rect[1]));await sheet.save(out+'/atlas.png');await writeFile(out+'/atlas.json',JSON.stringify({image:'atlas.png',tileSize:32,approval:'M1.ME3 Map Studio visual review; accepted adventure art unchanged',assets:entries,tiles:entries.filter(e=>e.id.startsWith('ME3.')).map(e=>({id:e.id,x:e.rect[0],y:e.rect[1],width:32,height:32,label:e.label,layer:e.layer,blocked:e.blocked}))},null,2)+'\n');console.log(entries.length+' packed review entries');
