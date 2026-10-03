import test from 'node:test';
import assert from 'node:assert/strict';
import {evenReference,centeredEvenOverlay} from '../sprite-editor/symmetry.js';
function rows(values){return new Uint8ClampedArray(values.flatMap(v=>[v,v+1,v+2,v?255:0]));}
test('duplicate center makes 31→32 with exact RGBA and symmetric pairs',()=>{
 const row=[...Array.from({length:15},(_,i)=>i+1),90,...Array.from({length:15},(_,i)=>15-i)],input=rows([...row,...row]),before=[...input];
 const next=evenReference(input,31,2,'duplicate');assert.equal(next.width,32);assert.equal(next.center,15);assert.deepEqual([...input],before);
 for(let y=0;y<2;y++)for(let x=0;x<32;x++){const i=(y*32+x)*4,j=(y*32+31-x)*4;assert.deepEqual([...next.pixels.slice(i,i+4)],[...next.pixels.slice(j,j+4)]);const sx=x<=15?x:x-1;assert.deepEqual([...next.pixels.slice(i,i+4)],[...input.slice((y*31+sx)*4,(y*31+sx)*4+4)]);}
});
test('remove center makes 33→32 without shifting or recoloring other columns',()=>{
 const input=rows(Array.from({length:33},(_,i)=>i)),next=evenReference(input,33,1,'remove');assert.equal(next.width,32);
 for(let x=0;x<32;x++)assert.equal(next.pixels[x*4],x<16?x:x+1);
 assert.equal(next.pixels[3],0);
});
test('even input is unchanged; asymmetric colors stay asymmetric; minimal and invalid inputs',()=>{
 const even=rows([1,2,3,4]);assert.deepEqual([...evenReference(even,4,1).pixels],[...even]);assert.equal(evenReference(even,4,1).changed,false);
 assert.deepEqual([...evenReference(rows([1,2,3]),3,1).pixels.filter((_,i)=>i%4===0)],[1,2,2,3]);
 assert.equal(evenReference(rows([8]),1,1).width,2);assert.throws(()=>evenReference(rows([8]),1,1,'remove'),/only column/);
 assert.throws(()=>evenReference(even,0,1));assert.throws(()=>evenReference(even,4,1,'blur'));
});
test('corrected overlay stays even and centered on integer boundary, including downsampling',()=>{
 assert.deepEqual(centeredEvenOverlay(32,42,32,64),{x:0,y:11,w:32,h:42,resampled:false});
 for(const [w,h]of [[480,479],[28,480],[2,480],[320,480]]){const r=centeredEvenOverlay(w,h,32,64);assert.equal(r.w%2,0);assert.equal(r.x+r.w/2,16);assert.ok(r.h<=64);assert.ok(r.w<=32);}
 assert.throws(()=>centeredEvenOverlay(32,42,31,64),/even-width canvas/);
});
