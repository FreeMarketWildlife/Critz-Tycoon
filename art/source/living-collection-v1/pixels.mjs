import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {describe,readProjectData,gifBytes} from '../../../sprite-editor/model.js';
const require=createRequire(import.meta.url);
export const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
export const home=path.dirname(new URL(import.meta.url).pathname),repo=path.resolve(home,'../../..'),out=path.join(repo,'assets/review/living-collection-v1');
export const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
export class Pixels{
 constructor(w=32,h=64){this.w=w;this.h=h;this.a=Array(w*h).fill(null);}
 p(x,y,c){if(x<0||y<0||x>=this.w||y>=this.h)throw Error(`Clipped ${x},${y} in ${this.w}x${this.h}`);this.a[y*this.w+x]=c;}
 get(x,y){return this.a[y*this.w+x]||null;}
 rect(l,t,r,b,c){for(let y=t;y<=b;y++)for(let x=l;x<=r;x++)this.p(x,y,c);}
 line(x,y,xx,yy,c){let dx=Math.abs(xx-x),dy=-Math.abs(yy-y),sx=x<xx?1:-1,sy=y<yy?1:-1,err=dx+dy;while(true){this.p(x,y,c);if(x===xx&&y===yy)break;const e=2*err;if(e>=dy){err+=dy;x+=sx;}if(e<=dx){err+=dx;y+=sy;}}}
 polygon(points,c){const ys=points.map(p=>p[1]);for(let y=Math.min(...ys);y<=Math.max(...ys);y++){const xs=[];for(let i=0;i<points.length;i++){let [x1,y1]=points[i],[x2,y2]=points[(i+1)%points.length];if((y1<=y&&y2>y)||(y2<=y&&y1>y))xs.push(x1+(y-y1)*(x2-x1)/(y2-y1));}xs.sort((a,b)=>a-b);for(let i=0;i<xs.length;i+=2)for(let x=Math.ceil(xs[i]);x<=Math.floor(xs[i+1]);x++)this.p(x,y,c);}}
 stamp(x,y,rows,pal){rows.forEach((row,j)=>[...row].forEach((v,i)=>{if(v!=='.'&&v!==' '){if(!pal[v])throw Error(v);this.p(x+i,y+j,pal[v]);}}));}
 blit(src,dx=0,dy=0,box=[0,0,src.w,src.h],map=c=>c){for(let y=box[1];y<box[3];y++)for(let x=box[0];x<box[2];x++){const c=src.get(x,y);if(c)this.p(x+dx,y+dy,map(c,x,y));}}
 clone(){const p=new Pixels(this.w,this.h);p.a=this.a.slice();return p;}
 rgba(){return Buffer.from(this.a.flatMap(c=>c?[...Buffer.from(c.slice(1),'hex'),255]:[0,0,0,0]));}
}
export function loadProject(file){const p=JSON.parse(fs.readFileSync(file));return {project:p,frames:p.frames.map(f=>{const a=new Pixels(p.width,p.height);a.a=f.pixels.map(i=>p.palette[i]);return a;})};}
export function indexed(label,frames,ticks=8){const palette=[null,...new Set(frames.flatMap(p=>p.a.filter(Boolean)))];return {format:'fmw-sprite',version:1,name:label,preset:frames[0].h===64&&frames[0].w===32?'character':'custom',width:frames[0].w,height:frames[0].h,palette,bank:'custom',notes:'M1.C7 original animation/habitat review; no runtime integration. Exact native pixels; no smoothing.',frames:frames.map((p,i)=>({name:'Pose '+i,ticks:Array.isArray(ticks)?ticks[i]:ticks,pixels:p.a.map(c=>palette.indexOf(c))}))};}
export async function saveAsset(slug,label,kind,frames,extra={},ticks=8){
 const dir=path.join(out,slug);fs.mkdirSync(dir,{recursive:true});
 const p=indexed(label,frames,ticks),rle=describe(p);
 const decoded=readProjectData(JSON.parse(rle),new Set(p.palette.slice(1)));
 if(JSON.stringify(decoded.frames)!==JSON.stringify(p.frames))throw Error('Editor round trip failed');
 fs.writeFileSync(path.join(home,slug+'.sprite.json'),JSON.stringify(p)+'\n');fs.writeFileSync(path.join(home,slug+'.rle.json'),rle+'\n');
 const meta={id:'critz.'+slug+'.motion.v1',slug,label,kind,frame:[p.width,p.height],anchor:[p.width/2,p.height],palette:p.palette,source:`art/source/living-collection-v1/${slug}.sprite.json`,ticks:p.frames.map(f=>f.ticks),tickMs:280896/16777216*1000,frames:[],...extra};
 for(let i=0;i<frames.length;i++){const raw=frames[i].rgba();await sharp(raw,{raw:{width:p.width,height:p.height,channels:4}}).png().toFile(path.join(dir,`frame-${i}.png`));meta.frames.push({index:i,rgbaSHA256:hash(raw)});}
 const columns=kind==='character'?4:Math.min(4,frames.length),rows=Math.ceil(frames.length/columns),sheet=new Pixels(p.width*columns,p.height*rows);
 frames.forEach((f,i)=>sheet.blit(f,i%columns*p.width,Math.floor(i/columns)*p.height));
 await sharp(sheet.rgba(),{raw:{width:sheet.w,height:sheet.h,channels:4}}).png().toFile(path.join(dir,'sheet.png'));
 fs.writeFileSync(path.join(dir,'motion.gif'),gifBytes(p));
 if(kind==='character')for(let d=0;d<4;d++)fs.writeFileSync(path.join(dir,['south','north','west','east'][d]+'.gif'),gifBytes({...p,frames:p.frames.slice(d*4,d*4+4)}));
 fs.writeFileSync(path.join(dir,'manifest.json'),JSON.stringify(meta,null,2)+'\n');return meta;
}
