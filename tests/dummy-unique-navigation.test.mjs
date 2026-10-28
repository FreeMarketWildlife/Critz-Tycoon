import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createProjectModel} from '../sprite-editor/dummy-creator-model.js';
const read=name=>JSON.parse(readFileSync(new URL('../sprite-editor/assets/'+name,import.meta.url)));
const seed=read('body-regions-seed.json'),project=read('phil-default-20261022.json');

test('unique navigation follows drawing strip in every direction, wraps and skips all repeated slots',()=>{
 for(const direction of ['south','west','east','north']){
  const m=createProjectModel(project,seed),cels=Object.values(m.data.cels).filter(c=>c.direction===direction);
  for(let slot=0;slot<m.data.directions[direction].length;slot++)for(const delta of [-1,1]){
   m.select(direction,slot);const before=m.data,current=cels.findIndex(c=>c.id===m.frame.celId);
   m.selectUnique(delta);
   const target=cels[(current+delta+cels.length)%cels.length].id;
   assert.equal(m.frame.celId,target);
   assert.equal(m.index,m.frames.findIndex(f=>f.celId===target));
   assert.equal(m.direction,direction);
   assert.deepEqual(m.data.directions,before.directions);
   assert.deepEqual(m.data.cels,before.cels);
   assert.equal(m.undoCount,0);
  }
 }
});

test('independent identical drawings stay selectable; reordered animation does not reorder drawings',()=>{
 const m=createProjectModel(project,seed);m.select('south',0);m.add();
 const duplicate=m.frame.celId,original=m.frames[0].celId;
 assert.deepEqual(m.labels,m.frames[0].labels);m.move(-1);
 const cels=Object.values(m.data.cels).filter(c=>c.direction==='south');
 m.selectUnique(1);assert.equal(m.frame.celId,original);
 m.selectUnique(-1);assert.equal(m.frame.celId,duplicate);
 assert.equal(cels.at(-1).id,duplicate);
});

test('single unique drawing keeps selected repeated slot and all project data unchanged',()=>{
 const m=createProjectModel(read('phil-completed-south-20261017.json'),seed);
 m.add(false,true);const before=m.data;
 m.selectUnique(1);assert.deepEqual(m.data,before);
 m.selectUnique(-1);assert.deepEqual(m.data,before);
});
