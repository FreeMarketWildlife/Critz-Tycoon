import {CONTACT_RULE} from './contact-rules.js';
import {canonicalMask} from './water-surfaces.js';
export const COAST_FORMAT=Object.freeze({tileSize:32,registrationY:16,sideInset:CONTACT_RULE.structurePixels,roundRadius:6,minimumWaterBlock:2,loopSeconds:3.2});
export function supportedWaterMask(m){return [19,38,76,137].some(pair=>(m&pair)===pair)&&(!(m&1)||!!(m&144))&&(!(m&2)||!!(m&48))&&(!(m&4)||!!(m&96))&&(!(m&8)||!!(m&192));}
export const COAST_MASKS=[...new Set(Array.from({length:256},(_,m)=>canonicalMask(m)))].filter(supportedWaterMask);
export const COAST_CONTEXTS=Array.from({length:256},(_,m)=>m).filter(m=>COAST_MASKS.includes(canonicalMask(m)));
export function sliverCells(cells){const set=new Set(cells.map(a=>a.x+','+a.y)),on=(x,y)=>set.has(x+','+y);return cells.filter(a=>![[1,1],[1,-1],[-1,1],[-1,-1]].some(([dx,dy])=>on(a.x+dx,a.y)&&on(a.x,a.y+dy)&&on(a.x+dx,a.y+dy)));}
const disk=[];for(let y=-6;y<=6;y++)for(let x=-6;x<=6;x++)if(x*x+y*y<=36)disk.push([x,y]);
function morph(input,w,h,dilate,radius){const taps=radius===6?disk:disk.filter(([x,y])=>x*x+y*y<=radius*radius);const out=new Uint8Array(input.length);for(let y=0;y<h;y++)for(let x=0;x<w;x++){let v=dilate?0:1;for(const [dx,dy]of taps){const xx=x+dx,yy=y+dy,on=xx>=0&&xx<w&&yy>=0&&yy<h?input[yy*w+xx]:0;if(dilate?on:!on){v=dilate?1:0;break;}}out[y*w+x]=v;}return out;}
// One construction for all material pairs. Round the complete footprint before
// slicing tiles; no per-tile border, overlap, clipped return or missing diagonal.
export function compileCoastalField(cells,width,height,{registrationY=COAST_FORMAT.registrationY,sideInset=COAST_FORMAT.sideInset,verticalInset=0,roundRadius=sideInset<=5?3:6}={}){
 const seed=new Uint8Array(width*height),set=new Set(cells.map(a=>a.x+','+a.y));
 const on=(x,y)=>set.has(x+','+y);
 for(const a of cells){const left=on(a.x-1,a.y)?0:sideInset,right=on(a.x+1,a.y)?32:32-sideInset,top=on(a.x,a.y-1)?0:verticalInset,bottom=on(a.x,a.y+1)?32:32-verticalInset;for(let y=top;y<bottom;y++)for(let x=left;x<right;x++){const xx=a.x*32+x,yy=a.y*32+y+registrationY;if(xx>=0&&xx<width&&yy>=0&&yy<height)seed[yy*width+xx]=1;}}
 const closed=morph(morph(seed,width,height,true,roundRadius),width,height,false,roundRadius),wet=morph(morph(closed,width,height,false,roundRadius),width,height,true,roundRadius),signed=distanceField(wet,width,height);
 return{wet,signed,width,height};
}
// Native chamfer distance: a continuous field for the entire shoreline, reused
// for each tide frame. Pixel clusters, never blurred alpha or independent strips.
function distanceField(wet,w,h){const d=new Float32Array(w*h).fill(1000),on=(x,y)=>x>=0&&x<w&&y>=0&&y<h?wet[y*w+x]:0;for(let y=0;y<h;y++)for(let x=0;x<w;x++)if(on(x-1,y)!==wet[y*w+x]||on(x+1,y)!==wet[y*w+x]||on(x,y-1)!==wet[y*w+x]||on(x,y+1)!==wet[y*w+x])d[y*w+x]=.5;
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){const i=y*w+x;if(x)d[i]=Math.min(d[i],d[i-1]+1);if(y){d[i]=Math.min(d[i],d[i-w]+1);if(x)d[i]=Math.min(d[i],d[i-w-1]+1.4142);if(x+1<w)d[i]=Math.min(d[i],d[i-w+1]+1.4142);}}
 for(let y=h-1;y>=0;y--)for(let x=w-1;x>=0;x--){const i=y*w+x;if(x+1<w)d[i]=Math.min(d[i],d[i+1]+1);if(y+1<h){d[i]=Math.min(d[i],d[i+w]+1);if(x)d[i]=Math.min(d[i],d[i+w-1]+1.4142);if(x+1<w)d[i]=Math.min(d[i],d[i+w+1]+1.4142);}}for(let i=0;i<d.length;i++)if(!wet[i])d[i]=-d[i];return d;}
const rgb=hex=>[parseInt(hex.slice(1,3),16),parseInt(hex.slice(3,5),16),parseInt(hex.slice(5,7),16),255];
const face=['#bcaa7d','#998769','#8a7764','#8a7764','#736455','#736455','#6c6053','#625b50','#5c5b51','#416d70','#365f69','#315768'].map(rgb),side=['#a79778','#746858','#446969','#315768'].map(rgb),rim=rgb('#797762'),foam=rgb('#edf1cc'),wash=rgb('#91c8c2'),wetSand=rgb('#c3b781');
export function coastalBankPixels(field,styleAt=()=>({ground:'grass',shallow:false})){const {wet,width:w,height:h}=field,out=new Uint8ClampedArray(w*h*4),on=(x,y)=>x>=0&&x<w&&y>=0&&y<h?wet[y*w+x]:0;for(let y=0;y<h;y++)for(let x=0;x<w;x++){const i=y*w+x;if(!wet[i])continue;const style=styleAt(x,y);if(style.ground==='sand')continue;let up=0,edge=0;for(let n=1;n<=12;n++)if(!on(x,y-n)){up=n;break;}for(let n=1;n<=4;n++)if(!on(x-n,y)||!on(x+n,y)||!on(x,y+n)){edge=n;break;}let color=style.shallow?(up===1||edge===1?rim:null):up?face[up-1]:edge?side[edge-1]:null;if(color){if(!style.shallow&&up>=3&&up<=8&&x%8===3)color=rgb('#5c554c');out.set(color,i*4);}}return out;}
export function coastalWashPixels(field,frame,enabledAt=()=>true){const {signed,width:w,height:h}=field,out=new Uint8ClampedArray(w*h*4),advance=2*Math.sin((frame%32)*2*Math.PI/32);for(let y=0;y<h;y++)for(let x=0;x<w;x++){const i=y*w+x,d=signed[i];if(Math.abs(d)>6||!enabledAt(x,y))continue;const front=d-advance;let color=null;if(Math.abs(front)<=.7)color=foam;else if(front<-.7&&front>=-2.7)color=wash;else if(d<0&&d>=-4)color=wetSand;if(color)out.set(color,i*4);}return out;}
