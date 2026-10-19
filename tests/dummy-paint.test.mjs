import test from 'node:test';
import assert from 'node:assert/strict';
import {connectedLabelPixels} from '../sprite-editor/dummy-paint.js';
test('fill follows exact four-connected IDs, excluding diagonal islands and row wrap',()=>{
 const labels=[1,0,0,1,1,0,0,0,1,0,1,0];const before=labels.slice();
 assert.deepEqual(connectedLabelPixels(labels,0,0,4,3),[[0,0],[0,1],[0,2]]);
 assert.deepEqual(connectedLabelPixels(labels,3,0,4,3),[[3,0]]);
 assert.deepEqual(connectedLabelPixels(labels,2,2,4,3),[[2,2]]);assert.deepEqual(labels,before);
});
test('fill can select a full blank canvas without mutation, and rejects out-of-frame starts',()=>{
 const labels=Array(2048).fill(0);assert.equal(connectedLabelPixels(labels,31,63).length,2048);assert.deepEqual(labels,Array(2048).fill(0));
 for(const [x,y]of [[-1,0],[32,0],[0,64],[0,-1],[.5,1]])assert.deepEqual(connectedLabelPixels(labels,x,y),[]);
});
