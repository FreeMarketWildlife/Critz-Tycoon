import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {SIZE,validateSeed,validateLabels,createLabelModel,exportCorrections,importCorrections,pixelAt,STORAGE} from '../sprite-editor/body-regions-model.js';
const fixture=()=>({schema:'critz.body-regions.seed',version:1,seedId:'RD1-test',width:32,height:64,source:{reference:{id:'ref',gifSha256:'a'.repeat(64),frame:2},dummy:{id:'dummy',sha256:'b'.repeat(64)},segmentation:{id:'regions',sha256:'c'.repeat(64)}},registration:{crop:[0,0,128,192],displayDivisor:4,native:[32,48],translation:[0,16],centerlineX:15.5,contactEdgeY:62,facing:'front',leftRight:'character-relative; left is screen-right'},parts:Array.from({length:14},(_,id)=>({id,name:'Part '+id,color:'#123456'})),referenceRGBA:Array(SIZE*4).fill(0),dummyRGBA:Array(SIZE*4).fill(0),labels:Array(SIZE).fill(0)});
test('approved public preload retains pinned reference, RD1 dummy, complete labels and character-relative sides',()=>{
 const seed=validateSeed(JSON.parse(readFileSync(new URL('../sprite-editor/assets/body-regions-seed.json',import.meta.url))));
 assert.equal(seed.source.reference.gifSha256,'5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e');
 assert.equal(seed.source.dummy.sha256,'606a6305a9a3bc9473a8cf6314ad86188627b6e107cfbaa97ff7e0d9a64100f8');
 assert.equal(seed.labels.filter(v=>v===14).length,8);assert.equal(seed.labels.filter(v=>v===15).length,8);assert.equal(seed.parts[14].key,'leftEye');assert.equal(seed.parts[15].key,'rightEye');
 for(const id of [6,8,10,12,14,16,18,20,22])assert.ok(seed.labels.every((v,i)=>v!==id||i%32>=16));
 for(const id of [7,9,11,13,15,17,19,21,23])assert.ok(seed.labels.every((v,i)=>v!==id||i%32<16));
 assert.deepEqual(importCorrections(exportCorrections(seed,seed.labels),seed),seed.labels);
});
test('complete 2048-cell correction roundtrip binds exact source, seed, parts and registration, no raster',()=>{
 const seed=validateSeed(fixture()),labels=Array.from({length:SIZE},(_,i)=>i%28),text=exportCorrections(seed,labels),data=JSON.parse(text);
 assert.deepEqual(importCorrections(text,seed),labels);assert.equal(data.labels.length,2048);assert.equal(Object.hasOwn(data,'referenceRGBA'),false);assert.equal(Object.hasOwn(data,'dummyRGBA'),false);assert.notEqual(STORAGE,'fmw.sprite-editor.v1');
 for(const edit of [d=>d.version=3,d=>d.width=64,d=>d.seedId='wrong',d=>d.source.dummy.sha256='d'.repeat(64),d=>d.registration.translation=[0,15],d=>d.parts[6].name='Right',d=>d.labels.pop(),d=>d.labels[3]=28,d=>d.labels[3]=1.5,d=>d.labels[3]='1',d=>d.surprise=true]){const d=structuredClone(data);edit(d);assert.throws(()=>importCorrections(JSON.stringify(d),seed));}
});
test('hostile and corrupt JSON never changes model or prototypes',()=>{
 const seed=fixture(),model=createLabelModel(seed.labels),before=model.labels;
 for(const text of ['null','[]','{','x'.repeat(100001),JSON.stringify({...JSON.parse(exportCorrections(seed,seed.labels)),source:JSON.parse('{"__proto__":{"polluted":true}}')})])assert.throws(()=>model.replace(importCorrections(text,seed)));
 assert.deepEqual(model.labels,before);assert.equal({}.polluted,undefined);
});
test('seed rejects corrupt raster, semantic IDs, registration and identity before loading',()=>{
 assert.equal(validateSeed(fixture()).labels.length,SIZE);
 assert.throws(()=>validateLabels(Array(SIZE)));const sparse=fixture();delete sparse.dummyRGBA[5];assert.throws(()=>validateSeed(sparse));
 for(const edit of [s=>s.referenceRGBA.pop(),s=>s.dummyRGBA[0]=-1,s=>s.parts[3].id=4,s=>s.parts[1].color='red',s=>s.labels[0]=99,s=>s.registration.leftRight='screen-relative',s=>s.source.dummy={id:'missing hash'},s=>s.seedId='../wrong']){const s=fixture();edit(s);assert.throws(()=>validateSeed(s));}
});
test('one stroke one undo, revisited cells restore originals, redo invalidates on new edit',()=>{
 const model=createLabelModel(Array(SIZE).fill(0));model.begin();model.paint(3,4,6);model.paint(4,4,6);model.paint(3,4,7);model.paint(-1,2,9);model.paint(32,2,9);assert.equal(model.end(),true);assert.equal(model.undoCount,1);assert.equal(model.labels[4*32+3],7);
 model.undo();assert.equal(model.labels[4*32+3],0);assert.equal(model.labels[4*32+4],0);assert.equal(model.redoCount,1);model.redo();assert.equal(model.labels[4*32+3],7);
 model.begin();model.paint(0,0,0);assert.equal(model.end(),false);assert.equal(model.undoCount,1);model.undo();model.begin();model.paint(31,63,13);model.end();assert.equal(model.redoCount,0);assert.equal(model.labels[2047],13);
 const original=model.labels;model.replace(Array(SIZE).fill(0));model.undo();assert.deepEqual(model.labels,original);assert.equal(model.labels[2047],13);
});
test('transition to two-finger navigation cancels the tentative first finger stroke with no history changes',()=>{
 const model=createLabelModel(Array(SIZE).fill(0));model.begin();model.paint(4,5,6);model.end();model.undo();const before=model.labels,history=[model.undoCount,model.redoCount];model.begin();model.paint(8,9,10);model.paint(9,9,10);model.paint(8,9,11);model.cancel();assert.deepEqual(model.labels,before);assert.deepEqual([model.undoCount,model.redoCount],history);assert.equal(model.end(),false);model.redo();assert.equal(model.labels[5*32+4],6);
});
test('screen point maps to exactly one top-left-origin native pixel across integer zoom and offsets',()=>{
 for(const zoom of [1,2,3,6,12,24]){const rect={left:-17,top:31,width:32*zoom,height:64*zoom};for(const [x,y]of [[0,0],[31,63],[16,40],[8,59]])assert.deepEqual(pixelAt(rect.left+(x+.5)*zoom,rect.top+(y+.5)*zoom,rect),[x,y]);assert.equal(pixelAt(rect.left-1,rect.top,rect),null);assert.equal(pixelAt(rect.left+rect.width,rect.top,rect),null);}
});
