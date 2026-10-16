import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';
import {validateSeed,importCorrections,PART_DEFINITIONS,migrateLegacyLabels} from '../sprite-editor/body-regions-model.js';
const read=p=>JSON.parse(readFileSync(new URL(p,import.meta.url))),seed=validateSeed(read('../sprite-editor/assets/body-regions-seed.json')),old=read('./fixtures/body-regions-phil-v1.json'),preset=read('../sprite-editor/assets/phil-region-labels-20261016.json');
test('Phil supplied preset matches his exact migrated markings, retaining every category and occupied cell',()=>{
 const migrated=importCorrections(JSON.stringify(old),seed),actual=importCorrections(JSON.stringify(preset),seed);assert.deepEqual(actual,migrated);assert.equal(old.labels.filter(Boolean).length,740);assert.equal(actual.filter(Boolean).length,740);assert.equal(actual.filter((id,i)=>id!==old.labels[i]).length,570);assert.deepEqual(actual,migrateLegacyLabels(old.labels));for(let i=0;i<2048;i++)assert.equal(PART_DEFINITIONS[actual[i]].category,PART_DEFINITIONS[old.labels[i]].category);
 assert.equal(preset.version,2);assert.equal(preset.parts[14].key,'leftEye');assert.equal(preset.parts[15].side,'right');assert.equal(preset.parts[16].category,'head');assert.deepEqual(preset.registration,old.registration);assert.deepEqual(preset.source,old.source);
});
