import test from 'node:test';
import assert from 'node:assert/strict';
import {fitReference,resizeReference,sampleReference} from '../sprite-editor/reference-pixels.js';

test('large portrait and landscape references fit inside with native-pixel dimensions and centering',()=>{
 assert.deepEqual(fitReference(250,434,32,64),{x:0,y:4,w:32,h:56});
 assert.deepEqual(fitReference(4000,1000,32,64),{x:0,y:28,w:32,h:8});
 assert.deepEqual(fitReference(16,32,32,64),{x:0,y:0,w:32,h:64});
});
test('locked corner/edge resizing preserves ratio and opposite anchor, unlocked stretches',()=>{
 const b={x:4,y:10,w:20,h:40};
 assert.deepEqual(resizeReference(b,'se',10,0,true),{x:4,y:10,w:30,h:60});
 assert.deepEqual(resizeReference(b,'nw',-10,-20,true),{x:-6,y:-10,w:30,h:60});
 assert.deepEqual(resizeReference(b,'e',10,0,false),{x:4,y:10,w:30,h:40});
 assert.deepEqual(resizeReference(b,'n',0,-10,false),{x:4,y:0,w:20,h:50});
 const r=resizeReference(b,'se',100000,100000,true);assert.equal(r.h,2048);assert.equal(r.w,1024);
 assert.ok(resizeReference(b,'se',-100,-100,false).w>=1);
});
test('area sampling averages every covered source pixel, nearest chooses center',()=>{
 const source=new Uint8ClampedArray([255,0,0,255, 0,0,255,255, 0,255,0,255, 255,255,255,255]);
 assert.deepEqual([...sampleReference(source,2,{x:0,y:0,w:2,h:2},1,1)],[128,128,128,255]);
 assert.deepEqual([...sampleReference(source,2,{x:0,y:0,w:2,h:2},1,1,'nearest')],[255,255,255,255]);
 assert.deepEqual([...sampleReference(source,2,{x:1,y:0,w:1,h:1},1,1)],[0,0,255,255]);
});
test('fractional footprint weighting and transparent RGB do not contaminate colors',()=>{
 const row=new Uint8ClampedArray([255,0,0,255, 0,0,255,255, 0,255,0,255]);
 assert.deepEqual([...sampleReference(row,3,{x:0,y:0,w:3,h:1},2,1)],[170,0,85,255,0,170,85,255]);
 const transparent=new Uint8ClampedArray([255,0,0,255, 0,0,0,0]);
 assert.deepEqual([...sampleReference(transparent,2,{x:0,y:0,w:2,h:1},1,1)],[255,0,0,128]);
 assert.deepEqual([...sampleReference(row,3,{x:0,y:0,w:2,h:1},1,1,'average',[255,0,0])],[0,0,255,128]);
});
test('constant colors survive arbitrary up/down sampling and crop boundaries',()=>{
 const data=new Uint8ClampedArray(17*19*4);for(let i=0;i<data.length;i+=4)data.set([24,99,173,255],i);
 for(const [w,h]of [[7,11],[32,64],[3,2],[1,1]]){const got=sampleReference(data,17,{x:2,y:3,w:15,h:16},w,h);for(let i=0;i<got.length;i+=4)assert.deepEqual([...got.subarray(i,i+4)],[24,99,173,255]);}
});
