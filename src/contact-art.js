import {CONTACT_RULE} from './contact-rules.js';
import {loadAtlas} from './atlas.js';
let atlas,manifest,entries,orchard,orchardEntries;
export async function loadContactArt(){if(atlas)return;const url=new URL('../assets/playable/contact/atlas.json',import.meta.url),r=await fetch(url);if(!r.ok)throw Error('Approved B contact manifest unavailable');manifest=await r.json();atlas=new Image();atlas.src=new URL(manifest.image,url).href;await atlas.decode();entries=new Map(manifest.assets.map(a=>[a.id,a]));orchard=await loadAtlas(new URL('../assets/playable/home-v2/atlas.json',import.meta.url));orchardEntries=new Set(orchard.manifest.fruitContactIds);}
export function drawContactArt(c,id,x,y){const a=entries?.get(id);if(!a)throw Error('Missing B contact assembly '+id);if(orchardEntries?.has(id.replace(/:ripe$/,'')))orchard.draw(c,id.endsWith(':ripe')?'orchard-ripe':'orchard-bare',x,y+a.offsetY);else c.drawImage(atlas,...a.rect,Math.round(x),Math.round(y+a.offsetY),a.w,a.h);return a;}
export const contactArtInfo=()=>({rule:CONTACT_RULE,assemblies:entries?.size||0});

export const contactEntry=id=>entries?.get(id);
export const contactSheet=()=>({m:manifest,img:atlas});
export const contactFrontiers=scene=>manifest?.frontiers?.[scene]||[];
