import test from 'node:test';
import assert from 'node:assert/strict';
import {treatCenterColumn,centeredReferenceOverlay} from '../sprite-editor/symmetry.js';
const pixels=values=>new Uint8ClampedArray(values.flatMap(v=>[v,v+1,v+2,v===0?0:255]));
const values=p=>[...p].filter((_,i)=>i%4===0);
for(const [width,expectations]of [[5,{'remove-left':[0,2,3,4],'remove-right':[0,1,2,4],'add-left':[0,1,1,2,3,4],'add-right':[0,1,2,3,3,4]}],[6,{'remove-left':[0,1,3,4,5],'remove-right':[0,1,2,4,5],'add-left':[0,1,2,2,3,4,5],'add-right':[0,1,2,3,3,4,5]}]]){
 test(`all four side treatments edit a ${width}px grid with exact RGBA and immutable input`,()=>{
  const row=Array.from({length:width},(_,i)=>i),input=pixels([...row,...row]),original=[...input];
  for(const [method,expected]of Object.entries(expectations)){
   const result=treatCenterColumn(input,width,2,method);
   assert.equal(result.width,expected.length);assert.deepEqual([...result.pixels],[...pixels([...expected,...expected])]);assert.deepEqual([...input],original);
  }
 });
}
test('one-column, limit and invalid input guards do not silently ignore treatment',()=>{
 for(const method of ['add-left','add-right'])assert.deepEqual(values(treatCenterColumn(pixels([9]),1,1,method).pixels),[9,9]);
 for(const method of ['remove-left','remove-right'])assert.throws(()=>treatCenterColumn(pixels([9]),1,1,method),/only column/);
 assert.throws(()=>treatCenterColumn(pixels([1,2]),2,1,'blur'));
 assert.throws(()=>treatCenterColumn(pixels([1,2]),0,1));
 assert.throws(()=>treatCenterColumn(new Uint8ClampedArray(480*4),480,1,'add-left'),/480px/);
 assert.equal(treatCenterColumn(new Uint8ClampedArray(479*4),479,1,'add-right').width,480);
});
test('placement centers even results exactly and labels native-grid odd offset without hiding edits',()=>{
 assert.deepEqual(centeredReferenceOverlay(32,42,32,64),{w:32,h:42,resampled:false,x:0,y:11,centerOffset:0});
 assert.deepEqual(centeredReferenceOverlay(31,42,32,64),{w:31,h:42,resampled:false,x:1,y:11,centerOffset:.5});
 for(const [w,h]of [[480,479],[28,480],[2,480],[320,480]]){const r=centeredReferenceOverlay(w,h,32,64);assert.equal(r.w%2,0);assert.equal(r.x+r.w/2,16);assert.ok(r.h<=64);assert.ok(r.w<=32);}
 assert.equal(centeredReferenceOverlay(30,42,31,64).centerOffset,.5);
});
