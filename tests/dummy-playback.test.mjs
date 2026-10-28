import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {parseProject,frameAt} from '../sprite-editor/dummy-creator-model.js';
import {projectForDraft,DATASETS,DEFAULT_DATASET} from '../sprite-editor/dummy-defaults.js';
import {walkingPreviewFrames,WALK_PREVIEW_LOOP_MS} from '../sprite-editor/dummy-playback.js';
const read=name=>readFileSync(new URL('../sprite-editor/assets/'+name,import.meta.url),'utf8');
const seed=JSON.parse(read('body-regions-seed.json')),raw=read('phil-default-20261027.json'),supplied=parseProject(raw,seed);
test('27 October supplied default is exact and retains all 29 slots and 12 drawings',()=>{
 assert.equal(createHash('sha256').update(raw).digest('hex'),'043d230c1eb241db65fbc6d62f68b474618e08d7f541b97a7fecf7629f0419a4');
 assert.equal(Object.keys(supplied.cels).length,12);
 assert.deepEqual(Object.values(supplied.directions).map(fs=>fs.length),[8,8,5,8]);
 assert.equal(supplied.activeDirection,'east');assert.equal(supplied.activeFrame,0);
 assert.equal(DATASETS[DEFAULT_DATASET].url,'./assets/phil-default-20261027.json');
 assert.equal(DATASETS['phil-supplied-20261027'].url,DATASETS[DEFAULT_DATASET].url);
 assert.deepEqual(projectForDraft(supplied,null,seed),supplied);
 const old=read('phil-default-20261022.json');assert.deepEqual(projectForDraft(supplied,old,seed),JSON.parse(old));
});
test('walking preview visits every stored slot, repeats and all, without changing authored data',()=>{
 const before=JSON.stringify(supplied);
 for(const frames of Object.values(supplied.directions)){
  const preview=walkingPreviewFrames(frames);assert.equal(preview.length,frames.length);
  assert.ok(Math.abs(preview.reduce((n,f)=>n+f.durationMs,0)-WALK_PREVIEW_LOOP_MS)<1e-9);
  let time=0;for(let i=0;i<frames.length;i++){
   assert.equal(frameAt(preview,time+.001),i);
   assert.equal(preview[i].celId,frames[i].celId);assert.equal(preview[i].referenceIndex,frames[i].referenceIndex);
   assert.ok(Math.abs(preview[i].durationMs/preview[0].durationMs-frames[i].durationMs/frames[0].durationMs)<1e-9);
   time+=preview[i].durationMs;
  }
  assert.equal(frameAt(preview,time+.001),0);
 }
 assert.equal(JSON.stringify(supplied),before);
});
