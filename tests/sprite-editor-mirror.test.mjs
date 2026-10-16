import test from 'node:test';
import assert from 'node:assert/strict';
import {mirrorPoints} from '../sprite-editor/mirror.js';
import {createLabelModel,SIZE} from '../sprite-editor/body-regions-model.js';
test('vertical mirror reflects from either edge and visits an odd center only once',()=>{
 assert.deepEqual(mirrorPoints(32,0,3,true),[[0,3],[31,3]]);
 assert.deepEqual(mirrorPoints(32,31,3,true),[[31,3],[0,3]]);
 assert.deepEqual(mirrorPoints(5,2,0,true),[[2,0]]);
 assert.deepEqual(mirrorPoints(5,1,0,false),[[1,0]]);
 assert.deepEqual(mirrorPoints(5,-1,0,true),[]);
});
test('mirrored labels and erase are one undoable stroke; off leaves the opposite side alone',()=>{
 const model=createLabelModel(Array(SIZE).fill(0));
 model.begin();model.paint(0,0,3,true);model.paint(1,0,3,true);model.paint(31,0,3,true);model.end();
 assert.equal(model.undoCount,1);assert.deepEqual(model.labels.slice(0,32),[3,3,...Array(28).fill(0),3,3]);
 model.undo();assert.ok(model.labels.every(v=>v===0));model.redo();assert.equal(model.labels[31],3);
 model.begin();model.paint(31,0,0,true);model.end();assert.equal(model.labels[0],0);assert.equal(model.labels[31],0);
 model.undo();assert.equal(model.labels[0],3);assert.equal(model.labels[31],3);
 model.begin();model.paint(0,0,4);model.end();assert.equal(model.labels[0],4);assert.equal(model.labels[31],3);
});
test('cancelling a mirrored touch stroke restores both sides without consuming history',()=>{
 const m=createLabelModel(Array(SIZE).fill(0));m.begin();m.paint(3,2,4,true);m.cancel();
 assert.ok(m.labels.every(v=>v===0));assert.equal(m.undoCount,0);
});
