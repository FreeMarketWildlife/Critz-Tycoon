import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {SIZE,PART_OPTIONS,PART_IDS,anatomicalPartId,createLabelModel,validateSeed,exportCorrections,importCorrections} from '../sprite-editor/body-regions-model.js';
const seed=validateSeed(JSON.parse(readFileSync(new URL('../sprite-editor/assets/body-regions-seed.json',import.meta.url))));
test('unified paired options retain all stable v1 anatomical IDs and distinct colors',()=>{
 assert.deepEqual(PART_OPTIONS.slice(6).map(p=>p.name),['Arm','Hand','Leg','Foot / shoe']);
 assert.equal(PART_OPTIONS.length,10);assert.equal(PART_IDS.length,28);
 for(const id of [6,8,10,12]){assert.equal(anatomicalPartId(id,0),id+1);assert.equal(anatomicalPartId(id,31),id);assert.equal(anatomicalPartId(id+1,0),id+1);assert.equal(anatomicalPartId(id+1,31),id);assert.notEqual(seed.parts[id].color,seed.parts[id+1].color);}
});
test('painting from either side produces opposite anatomical pair IDs in one undoable mirrored stroke',()=>{
 for(const id of [6,8,10,12])for(const x of [0,15,16,31]){
  const m=createLabelModel(Array(SIZE).fill(0));m.begin();m.paintAnatomical(x,12,id,true,'front');m.end();
  assert.equal(m.labels[12*32+x],anatomicalPartId(id,x));assert.equal(m.labels[12*32+31-x],anatomicalPartId(id,31-x));assert.equal(m.undoCount,1);
  const after=m.labels;m.undo();assert.ok(m.labels.every(v=>v===0));m.redo();assert.deepEqual(m.labels,after);
  m.begin();m.paintAnatomical(x,12,0,true,'front');m.end();assert.equal(m.labels[12*32+x],0);assert.equal(m.labels[12*32+31-x],0);m.undo();assert.deepEqual(m.labels,after);
 }
});
test('mirror off still infers the painted side only; head/torso have no side swap',()=>{
 const m=createLabelModel(Array(SIZE).fill(0));m.begin();m.paintAnatomical(3,4,6);m.end();assert.equal(m.labels[4*32+3],7);assert.equal(m.labels[4*32+28],0);
 for(const id of [0]){m.begin();m.paintAnatomical(15,2,id,true);m.end();assert.equal(m.labels[2*32+15],id);assert.equal(m.labels[2*32+16],id);}
});
test('unsupported facings do not guess paired identity; exact odd center is ambiguous',()=>{
 assert.equal(anatomicalPartId(6,2,5,'front'),24);assert.equal(anatomicalPartId(4,2,5,'front'),4);
 for(const facing of ['back','west','east','side']){const m=createLabelModel(Array(SIZE).fill(0));m.begin();assert.throws(()=>m.paintAnatomical(3,4,6,true,facing),/front view only/);m.end();assert.ok(m.labels.every(v=>v===0));}
 for(const facing of ['back','west','east'])assert.throws(()=>validateSeed({...seed,registration:{...seed.registration,facing}}));
});
test('legacy saved labels including unusual/crossed assignments import and export unchanged',()=>{
 const old=Array.from({length:SIZE},(_,i)=>i%28),text=exportCorrections(seed,old),m=createLabelModel(importCorrections(text,seed));
 const expected=old;
 assert.deepEqual(m.labels,expected);assert.equal(exportCorrections(seed,m.labels),text);
 m.begin();m.paintAnatomical(0,0,6,true);m.end();const edited=m.labels;assert.equal(edited[0],7);assert.equal(edited[31],6);assert.deepEqual(edited.slice(32),expected.slice(32));
 m.undo();assert.deepEqual(m.labels,expected);m.redo();assert.deepEqual(importCorrections(exportCorrections(seed,m.labels),seed),edited);
});
