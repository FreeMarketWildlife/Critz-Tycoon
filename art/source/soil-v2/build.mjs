// Quiet original earth, retaining Critz's complete native terrain joining geometry.
// Existing Critz underlays are read-only; no reference-game pixels are consumed.
import fs from 'node:fs';import path from 'node:path';import {createRequire} from 'node:module';import {Pixels,indexed} from '../living-collection-v1/pixels.mjs';
const require=createRequire(import.meta.url),sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp'),root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'../../..'),out=path.join(root,'assets/playable/soil-v2');fs.mkdirSync(out,{recursive:true});
const master=JSON.parse(fs.readFileSync(path.join(root,'assets/playable/overworld/master.json'))),bank=await sharp(path.join(root,'assets/playable/overworld/master.png')).ensureAlpha().raw().toBuffer();
function tile(id){const t=master.tiles.find(t=>t.id===id);if(!t)throw Error(id);const p=new Pixels(32,32);for(let y=0;y<32;y++)for(let x=0;x<32;x++){const i=((t.y+y)*1024+t.x+x)*4;p.p(x,y,'#'+bank.subarray(i,i+3).toString('hex'));}return p;}
function normalize(n){for(const [bit,a,b]of [[16,1,2],[32,2,4],[64,4,8],[128,8,1]])if(!(n&a)||!(n&b))n&=~bit;return n;}
const masks=[...new Set(Array.from({length:256},(_,i)=>normalize(i)))].sort((a,b)=>a-b);
export function within(x,y,m){const east=x>=16,south=y>=16,dx=east?31-x:x,dy=south?31-y:y,vx=!!(m&(east?2:8)),vy=!!(m&(south?4:1)),diag=!!(m&(south?(east?32:64):(east?16:128)));if(!vx&&!vy)return dx>=5&&dy>=5&&(dx>=9||dy>=9||(dx-9)**2+(dy-9)**2<=16);if(!vx)return dx>=5;if(!vy)return dy>=5;if(!diag&&dx<5&&dy<5)return dx*dx+dy*dy>=25;return true;}
const soil=new Pixels(32,32);soil.rect(0,0,31,31,'#ac926b');
// Few connected earth planes; no regular rows, wood rails or random grain fields.
soil.stamp(7,9,['.mmm....','mdddm...','.ddddm..','..dddmm.','....mm..'],{m:'#a38a63',d:'#997f5b'});
soil.stamp(20,22,['..ll.','.lll.','llm..','.m...'],{l:'#bca276',m:'#b29a70'});
soil.line(18,7,20,7,'#bca276');soil.p(19,8,'#b29a70');soil.line(8,23,9,23,'#997f5b');
const props=JSON.parse(fs.readFileSync(path.join(root,'assets/review/coastal-format/props.json'))),sandEntry=props.assets.find(a=>a.id==='sand.0'),sandBytes=await sharp(path.join(root,'assets/review/coastal-format',props.image)).extract({left:sandEntry.x,top:sandEntry.y,width:32,height:32}).ensureAlpha().raw().toBuffer(),sand=new Pixels(32,32);
for(let y=0;y<32;y++)for(let x=0;x<32;x++)sand.p(x,y,'#'+sandBytes.subarray((y*32+x)*4,(y*32+x)*4+3).toString('hex'));
const bases={grass:tile('meadow.grass.0'),path:tile('meadow.path.255.0'),paving:tile('ground.paving'),sand},entries=[],images=[];
function add(id,p,meta={}){const n=entries.length;entries.push({id,x:n%16*32,y:Math.floor(n/16)*32,width:32,height:32,layer:'ground',blocked:false,...meta});images.push(p);}
add('ground.soil',soil);
for(const [under,base]of Object.entries(bases)){
 const family=[];
 for(const mask of masks){const p=base.clone();for(let y=0;y<32;y++)for(let x=0;x<32;x++)if(within(x,y,mask)){const edge=[[1,0],[-1,0],[0,1],[0,-1]].some(([dx,dy])=>!within(Math.max(0,Math.min(31,x+dx)),Math.max(0,Math.min(31,y+dy)),mask));p.p(x,y,edge?'#92795a':soil.get(x,y));}
  add(under==='sand'?`ME3.blend.soil.sand.${mask}`:`blend.soil.${under}.${mask}`,p,{terrain:'soil',under,neighborMask:mask});family.push(p);
  if(under==='grass')add(`soil.${mask}`,p,{terrain:'soil',under,neighborMask:mask});
 }
 const project={...indexed('Quiet soil · '+under,family),notes:'M1.OV1 quiet original earth over unchanged Critz underlay; canonical 47 joining contexts. No collision inferred from pixels.'};fs.writeFileSync(path.join(root,'art/source/soil-v2',`soil-${under}.sprite.json`),JSON.stringify(project)+'\n');
}
const sheet=new Pixels(512,Math.ceil(images.length/16)*32);images.forEach((p,i)=>sheet.blit(p,i%16*32,Math.floor(i/16)*32));await sharp(sheet.rgba(),{raw:{width:sheet.w,height:sheet.h,channels:4}}).png().toFile(path.join(out,'atlas.png'));fs.writeFileSync(path.join(out,'atlas.json'),JSON.stringify({schemaVersion:1,image:'atlas.png',size:[sheet.w,sheet.h],imageWidth:sheet.w,imageHeight:sheet.h,tiles:entries,assets:entries.map(t=>({id:t.id,rect:[t.x,t.y,32,32],anchor:[0,0]})),task:'M1.OV1',originalUnderlays:'assets/playable/overworld/master.png',provenance:'Original native soil planes; exact existing Critz underlays; no Emerald images',approval:'new appearance awaits morning review'},null,2)+'\n');console.log('Quiet soil: 47 masks × four exact underlays; 236 native tiles including world aliases.');
