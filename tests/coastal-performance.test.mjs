import test from 'node:test';import assert from 'node:assert/strict';
import {morphCoastalMask,coastalBankPixels,compileCoastalField} from '../src/coastal-format.js';

function reference(input,w,h,dilate,radius){
 const taps=[];for(let y=-radius;y<=radius;y++)for(let x=-radius;x<=radius;x++)if(x*x+y*y<=radius*radius)taps.push([x,y]);
 const out=new Uint8Array(input.length);
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){let value=dilate?0:1;for(const [dx,dy]of taps){const xx=x+dx,yy=y+dy,on=xx>=0&&xx<w&&yy>=0&&yy<h?input[yy*w+xx]:0;if(dilate?on:!on){value=dilate?1:0;break;}}out[y*w+x]=value;}return out;
}
test('Fast disk passes equal independent per-tap morphology at all borders, holes and radii',()=>{
 let seed=17;const random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/2**32;};
 for(const [w,h]of [[1,1],[7,11],[32,29],[65,53]])for(const fill of [0,.1,.5,.9,1]){
  const input=Uint8Array.from({length:w*h},()=>Number(random()<fill));
  for(const radius of [0,3,6])for(const dilate of [false,true])assert.deepEqual(morphCoastalMask(input,w,h,dilate,radius),reference(input,w,h,dilate,radius));
 }
});
test('Distance skip changes no authored shore pixels, including thin curves and holes',()=>{
 const cells=[];for(let y=1;y<7;y++)for(let x=1;x<9;x++)if(!(x>=4&&x<=5&&y>=3&&y<=4))cells.push({x,y});
 const field=compileCoastalField(cells,320,288);
 for(const shallow of [false,true])for(const ground of ['grass','sand']){
  const style=()=>({ground,shallow});assert.deepEqual(coastalBankPixels(field,style),coastalBankPixels({...field,signed:undefined},style));
 }
});
