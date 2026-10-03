// Indexed, binary-alpha pixels. Rendering overlays never enter this model.
export const TICK_MS = 280896 / 16777216 * 1000;
export const MAX_PIXELS = 2_000_000;
export const PRESETS = [
  ['character','Character · standard overworld',32,64,true],
  ['battle','Battle sprite · front / back',128,128,true],
  ['small','Small overworld / item',32,32,false],
  ['large','Large overworld sprite',64,64,false],
  ['party','UI party icon',64,64,false],
  ['tile','Environment tile',16,16,false],
  ['block','Environment map block',32,32,false],
  ['rock','Rock / small prop',32,32,false],
  ['building','Building · 5 × 5 map blocks',160,160,false],
  ['screen','GBA screen · Emerald 2×',480,320,false],
  ['custom','Custom canvas',32,32,false],
];
export function makeProject(palette, preset='character', width, height) {
  const p=PRESETS.find(p=>p[0]===preset)||PRESETS[0];
  width??=p[2];height??=p[3];
  return {format:'fmw-sprite',version:1,name:'Untitled sprite',preset:p[0],width,height,palette:[null,...palette],bank:'hero',notes:'',frames:[{name:'Idle',ticks:8,pixels:Array(width*height).fill(0)}]};
}
export function validateProject(p,allowed) {
  if(!p||p.format!=='fmw-sprite'||p.version!==1)throw Error('This is not a Free Market Wildlife sprite project.');
  if(!Number.isInteger(p.width)||!Number.isInteger(p.height)||p.width<1||p.height<1||p.width>480||p.height>480)throw Error('Canvas dimensions must be whole pixels from 1 to 480.');
  if(!Array.isArray(p.frames)||p.frames.length<1||p.frames.length>64||p.width*p.height*p.frames.length>MAX_PIXELS)throw Error('Project exceeds 64 frames or 2 million pixels.');
  if(!Array.isArray(p.palette)||p.palette[0]!==null||p.palette.length>256||p.palette.slice(1).some(c=>typeof c!=='string'||!allowed.has(c.toLowerCase())))throw Error('Project contains colors outside the Critz palette banks.');
  if(!PRESETS.some(a=>a[0]===p.preset))throw Error('Unknown canvas preset.');
  for(const f of p.frames)if(!f||!Number.isInteger(f.ticks)||f.ticks<1||f.ticks>600||!Array.isArray(f.pixels)||f.pixels.length!==p.width*p.height||f.pixels.some(v=>!Number.isInteger(v)||v<0||v>=p.palette.length))throw Error('Invalid frame pixels or timing.');
  if(typeof p.name!=='string'||p.name.length>100||typeof p.notes!=='string'||p.notes.length>10000||p.frames.some(f=>typeof f.name!=='string'||f.name.length>80))throw Error('Invalid project text.');
  if(isCharacter(p)&&usedColors(p).size>15)throw Error('Character projects allow 15 opaque colors plus transparency.');
  return p;
}
export const isCharacter=p=>PRESETS.find(a=>a[0]===p.preset)?.[4];
export const usedColors=p=>new Set(p.frames.flatMap(f=>[...new Set(f.pixels)].filter(Boolean)));
export function line(x0,y0,x1,y1,visit) {
  const dx=Math.abs(x1-x0),sx=x0<x1?1:-1,dy=-Math.abs(y1-y0),sy=y0<y1?1:-1;let err=dx+dy;
  for(;;){visit(x0,y0);if(x0===x1&&y0===y1)break;const e=2*err;if(e>=dy){err+=dy;x0+=sx;}if(e<=dx){err+=dx;y0+=sy;}}
}
export function fill(pixels,w,h,x,y,color) {
  if(x<0||x>=w||y<0||y>=h)return;
  const old=pixels[y*w+x];if(old===color)return;const stack=[y*w+x];pixels[y*w+x]=color;
  while(stack.length){const i=stack.pop(),cx=i%w;for(const n of [cx>0?i-1:-1,cx<w-1?i+1:-1,i-w,i+w])if(n>=0&&n<pixels.length&&pixels[n]===old){pixels[n]=color;stack.push(n);}}
}
export function nearest(r,g,b,palette) {let best=1,score=Infinity;for(let i=1;i<palette.length;i++){const c=palette[i],d=(r-parseInt(c.slice(1,3),16))**2+(g-parseInt(c.slice(3,5),16))**2+(b-parseInt(c.slice(5,7),16))**2;if(d<score){score=d;best=i;}}return best;}
export function bounds(pixels,w,h){let l=w,t=h,r=-1,b=-1;pixels.forEach((v,i)=>{if(v){const x=i%w,y=Math.floor(i/w);l=Math.min(l,x);t=Math.min(t,y);r=Math.max(r,x);b=Math.max(b,y);}});return r<0?null:[l,t,r+1,b+1];}
export function describe(p){return JSON.stringify({format:'fmw-sprite-exact-rle',version:1,name:p.name,preset:p.preset,width:p.width,height:p.height,coordinateSystem:'Top-left (0,0); x increases right, y down. Each row is [paletteIndex, runLength] pairs. Expand each row to exactly width pixels. Index 0 is fully transparent; all other pixels are fully opaque. No smoothing.',palette:p.palette,tickMilliseconds:TICK_MS,anchor:[p.width/2,p.height],notes:p.notes,artBible:'Emerald 2×; original Critz colors. Canvas size is not painted height. Anatomy and pose proportions require separately measured reference annotations. This data does not certify art approval. Reference overlays excluded.',frames:p.frames.map(f=>({name:f.name,ticks:f.ticks,durationMilliseconds:f.ticks*TICK_MS,opaqueBounds:bounds(f.pixels,p.width,p.height),rows:Array.from({length:p.height},(_,y)=>{const a=[];for(let x=0;x<p.width;x++){const v=f.pixels[y*p.width+x];if(a.length&&a[a.length-2]===v)a[a.length-1]++;else a.push(v,1);}return a;})}))},null,2);}
// GIF89a uses literal LZW codes and periodic clears, avoiding lossy color conversion.
export function gifBytes(p){
 const bytes=[],put=(...a)=>bytes.push(...a),word=n=>put(n&255,n>>8&255),str=s=>put(...[...s].map(c=>c.charCodeAt(0)));
 str('GIF89a');word(p.width);word(p.height);put(0xf7,0,0);
 for(let i=0;i<256;i++){const c=p.palette[i]||'#000000';put(parseInt(c.slice(1,3),16),parseInt(c.slice(3,5),16),parseInt(c.slice(5,7),16));}
 put(0x21,0xff,11);str('NETSCAPE2.0');put(3,1,0,0,0);
 let elapsed=0,rounded=0;
 for(const f of p.frames){elapsed+=f.ticks*TICK_MS/10;const next=Math.round(elapsed),delay=Math.max(2,next-rounded);rounded=next;
 put(0x21,0xf9,4,9);word(delay);put(0,0,0x2c);word(0);word(0);word(p.width);word(p.height);put(0,8);
 const data=[];let acc=0,bits=0;const code=c=>{acc|=c<<bits;bits+=9;while(bits>=8){data.push(acc&255);acc>>>=8;bits-=8;}};
 for(let i=0;i<f.pixels.length;i++){if(i%200===0)code(256);code(f.pixels[i]);}code(257);if(bits)data.push(acc&255);
 for(let i=0;i<data.length;i+=255){const part=data.slice(i,i+255);put(part.length,...part);}put(0);
 }put(0x3b);return new Uint8Array(bytes);
}
