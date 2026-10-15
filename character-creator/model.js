// Pure BS2 appearance composition. No game state, anatomical dummy or storage.
export const DEFAULTS=Object.freeze({hair:'twists',hairColor:'original',skin:'original',eyes:'classic',ears:'folded',shoes:'trail',nose:'none',mouth:'none'});
export const OPTIONS=Object.freeze({hair:['twists','crop','bald'],hairColor:['original','black','warm'],skin:['original','deep','warm'],eyes:['classic','short','amber'],ears:['folded','soft'],shoes:['trail','forest','midnight'],nose:['none','small'],mouth:['none','line','smile']});
export const SKIN=Object.freeze({original:['#744539','#a66845','#c38a58'],deep:['#51352f','#7d4e39','#a16c48'],warm:['#88523c','#b67a4c','#d39b68']});
const HAIR={original:{},black:{'#322a31':'#242330','#4c3739':'#34303a','#705044':'#49404b'},warm:{'#322a31':'#3c2c2d','#4c3739':'#684133','#705044':'#936345'}};
const SHOE={trail:{},forest:{'#ae454a':'#3f6554','#ed745c':'#74936a'},midnight:{'#ae454a':'#3d536e','#ed745c':'#7689a0'}};
const ix=([x,y])=>y*32+x;
export function settings(input={}){const out={...DEFAULTS};for(const key in OPTIONS)if(OPTIONS[key].includes(input[key]))out[key]=input[key];return out;}
export function compose(data,direction='south',pose='idle',input={}){
 const s=settings(input),p=data.poses[direction]?.[pose];if(!p)throw Error('Unknown direction or pose');
 const colors=data.palette,read=name=>p.layers[name].map(i=>colors[i]),base=read('base'),ramp=SKIN[s.skin],skinMap=Object.fromEntries(SKIN.original.map((c,i)=>[c,ramp[i]])),recolor=c=>skinMap[c]||c,pixels=base.map(recolor);
 // Source clothing/shoes are the standard character template, not an opaque
 // outfit hiding a second smaller body. These registered material sites alone vary.
 for(const pt of p.shoes){const i=ix(pt);pixels[i]=SHOE[s.shoes][base[i]]||base[i];}
 if(s.eyes==='short'){
  const bottom=Math.max(-1,...p.eyes.map(q=>q[1]));for(const pt of p.eyes)if(pt[1]===bottom)pixels[ix(pt)]=ramp[2];
 }else if(s.eyes==='amber'){
  const bottom=Math.max(-1,...p.eyes.map(q=>q[1]));for(const pt of p.eyes)if(pt[1]===bottom-1)pixels[ix(pt)]='#b67c38';
 }
 if(s.ears==='soft')for(const pt of p.ears){const i=ix(pt);if(SKIN.original.includes(base[i]))pixels[i]=ramp[1];}
 for(const key of ['nose','mouth'])if(s[key]!=='none'){
  const sites=key==='mouth'&&s.mouth==='smile'?p.smile:p[key];for(const pt of sites)pixels[ix(pt)]=ramp[0];
 }
 if(s.hair==='twists'){
  for(const pt of p.hairHiddenScalp)pixels[ix(pt)]=null;
  // Hair-dependent exposed skin shadows use the selected skin ramp too.
  read('hairShade').forEach((c,i)=>{if(c)pixels[i]=recolor(c);});
 }
 if(s.hair!=='bald')read(s.hair==='crop'?'crop':'hair').forEach((c,i)=>{if(c)pixels[i]=HAIR[s.hairColor][c]||c;});
 return pixels;
}
export function holds(direction){return direction==='south'?[100,100,100,100,100,100,100,100]:[70,60,70,70,70,60,70,70];}
export function slotAt(direction,elapsed){const ds=holds(direction),total=ds.reduce((a,b)=>a+b,0);let t=((elapsed%total)+total)%total;for(let i=0;i<8;i++){if(t<ds[i])return i;t-=ds[i];}return 7;}
export function slotStart(direction,slot){return holds(direction).slice(0,slot).reduce((a,b)=>a+b,0);}
export function walkPose(data,direction,elapsed){return data.order[slotAt(direction,elapsed)];}
function indexedProject(data,frames,name,notes){
 const palette=[null],lookup=new Map();return {format:'fmw-sprite',version:1,name,preset:'character',width:32,height:64,palette,bank:'custom',notes,frames:frames.map(f=>({...f,pixels:f.pixels.map(c=>{if(!c)return 0;if(!lookup.has(c)){lookup.set(c,palette.length);palette.push(c);}return lookup.get(c);})}))};
}
export function project(data,input={}){
 const frames=[];for(const dr of Object.keys(data.poses))for(const po of ['idle','A','P','C'])frames.push({name:`${dr} ${po}`,ticks:dr==='south'?6:4,pixels:compose(data,dr,po,input)});
 const out=indexedProject(data,frames,'Critz Hero · static pose collection','CC1 review only. Sixteen UNIQUE STATIC POSES, not a walking timeline. Anchor16,64. BS2 foundation; PM1 excluded.');
 out.critzReview={kind:'unique-static-poses',anchor:[16,64],settings:settings(input),walk:{order:data.order,durationsMs:Object.fromEntries(Object.keys(data.poses).map(dr=>[dr,holds(dr)])),ticksPerSlot:{south:6,north:4,west:4,east:4},timing:'Original source export holds; not emulator observation'}};return out;
}
export function walkProject(data,direction,input={}){return indexedProject(data,data.order.map((po,i)=>({name:`${direction} slot${i} ${po}`,ticks:direction==='south'?6:4,pixels:compose(data,direction,po,input)})),'Critz Hero · '+direction+' walk','CC1 existing8-slot walk; original ticks6South/4NWE. Anchor16,64. Selected appearance.');}
