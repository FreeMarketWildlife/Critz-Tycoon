// Review-only registered appearance composition; no game or browser storage imports.
export const DEFAULTS=Object.freeze({hair:'twists',hairColor:'original',skin:'original',eyes:'classic',ears:'classic',shoes:'original',nose:'none',mouth:'none'});
export const OPTIONS=Object.freeze({hair:['twists','bald'],hairColor:['original','black','warm'],skin:['original','deep','warm'],eyes:['classic','short'],ears:['classic','soft'],shoes:['original','coral','forest'],nose:['none','hint'],mouth:['none','hint']});
export const SKIN={original:['#744539','#a66845','#c38a58'],deep:['#51352f','#7d4e39','#a16c48'],warm:['#88523c','#b67a4c','#d39b68']};
const HAIR={original:{},black:{'#4e3938':'#34303a','#65463d':'#49404b','#825b47':'#62505a'},warm:{'#4e3938':'#5b3b30','#65463d':'#80563c','#825b47':'#a9784c'}};
const SHOE={original:{},coral:{'#3e515e':'#914e50','#637a85':'#bf7670','#9aafb2':'#e0b1a0'},forest:{'#3e515e':'#3f5c51','#637a85':'#658a68','#9aafb2':'#a6b99a'}};
export function settings(input={}){const out={...DEFAULTS};for(const key in OPTIONS)if(OPTIONS[key].includes(input[key]))out[key]=input[key];return out;}
const ix=([x,y])=>y*32+x;
export function compose(data,direction='south',pose='idle',input={},view='dressed'){
 const s=settings(input),p=data.poses[direction]?.[pose];if(!p)throw Error('Unknown direction or pose');
 const colors=data.palette,layer=name=>p.layers[name].map(i=>colors[i]),body=layer(view==='foundation'?'neutral-body':'body-render-with-selected-skin');
 if(view==='foundation')return body;
 const ramp=SKIN[s.skin],skinMap=Object.fromEntries(SKIN.original.map((c,i)=>[c,ramp[i]]));
 const recolor=c=>skinMap[c]||c;
 const pixels=body.map(recolor);
 // Face edits are registered on body surface before independent hair/garments.
 if(s.eyes==='short'){
  const bottom=Math.max(...p.eyes.map(pt=>pt[1]));for(const pt of p.eyes)if(pt[1]===bottom)pixels[ix(pt)]=ramp[1];
 }
 if(s.ears==='soft')for(const pt of p.ears){const i=ix(pt);if(SKIN.original.includes(body[i]))pixels[i]=ramp[1];}
 for(const key of ['nose','mouth'])if(s[key]==='hint')for(const pt of p[key]){const i=ix(pt);if(SKIN.original.includes(body[i]))pixels[i]=ramp[0];}
 if(view==='body')return pixels;
 for(const name of ['hair','shirt','shorts','shoes','pack','straps']){
  if(name==='hair'&&s.hair==='bald')continue;
  const changes=name==='hair'?HAIR[s.hairColor]:name==='shoes'?SHOE[s.shoes]:{};
  layer('overlay-'+name).forEach((c,i)=>{if(c)pixels[i]=changes[c]||c;});
 }
 return pixels;
}
export function project(data,input={}){
 const palette=[null],lookup=new Map(),frames=[];
 for(const dr of Object.keys(data.poses))for(const po of ['idle','A','P','C']){
  const pixels=compose(data,dr,po,input).map(c=>{if(!c)return 0;if(!lookup.has(c)){lookup.set(c,palette.length);palette.push(c);}return lookup.get(c);});
  frames.push({name:`${dr} ${po}`,ticks:6,pixels});
 }
 return {format:'fmw-sprite',version:1,name:'Critz Hero · creator review',preset:'character',width:32,height:64,palette,bank:'custom',notes:'M1.CC1 review only. Anchor16,64. Sixteen unique poses; A,A,P,P,C,C,P,P walk. No game save changes.',frames};
}
export function walkPose(data,dr,elapsed,slow=false){
 // Preserve the recorded native source timing, not an emulator-derived claim.
 const durations=dr==='south'?Array(8).fill(100):[70,60,70,70,70,60,70,70],factor=slow?4:1;
 let t=((elapsed% (durations.reduce((a,b)=>a+b,0)*factor))+durations.reduce((a,b)=>a+b,0)*factor)%(durations.reduce((a,b)=>a+b,0)*factor);
 for(let i=0;i<8;i++){if(t<durations[i]*factor)return data.order[i];t-=durations[i]*factor;}return 'P';
}
