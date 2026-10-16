import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';
import {validateSeed,exportCorrections,importCorrections,createLabelModel,migrateLegacyLabels,PART_IDS,PART_DEFINITIONS,PART_OPTIONS,CATEGORY_PARTS,anatomicalPartId} from '../sprite-editor/body-regions-model.js';
const current=()=>validateSeed(JSON.parse(readFileSync(new URL('../sprite-editor/assets/body-regions-seed.json',import.meta.url))));
const legacy=()=>{const s=current();s.version=1;s.parts=s.parts.slice(0,14).map(({id,name,color})=>({id,name,color}));s.parts[3].color='#fcf1d9';s.parts[12].color='#bbbbbb';s.labels=s.labels.map(id=>({14:3,15:3,16:1,17:1,18:2,19:2,20:4,21:4,22:5,23:5})[id]??id);return s;};
test('legacy migration preserves every marked cell/category/source and all already explicit anatomical identities',()=>{
 const old=legacy();old.labels[0]=3;old.labels[31]=3;old.labels[30]=7;const s=validateSeed(old);assert.equal(s.version,2);assert.equal(s.parts.length,28);assert.deepEqual(s.labels,migrateLegacyLabels(old.labels));assert.equal(s.labels.filter(Boolean).length,old.labels.filter(Boolean).length);assert.deepEqual(s.referenceRGBA,old.referenceRGBA);assert.deepEqual(s.dummyRGBA,old.dummyRGBA);assert.deepEqual(s.source,old.source);assert.deepEqual(s.registration,old.registration);
 for(let i=0;i<2048;i++){assert.equal(PART_DEFINITIONS[s.labels[i]].category,PART_DEFINITIONS[old.labels[i]].category);if(old.labels[i]>=6)assert.equal(s.labels[i],old.labels[i]);}
 for(let id=0;id<14;id++){assert.equal(s.parts[id].id,old.parts[id].id);assert.equal(s.parts[id].name,old.parts[id].name);assert.equal(s.parts[id].key,PART_IDS[id]);}
 assert.equal(s.parts[14].key,'leftEye');assert.equal(s.parts[15].key,'rightEye');assert.equal(s.parts[12].color,'#0047ff');assert.equal(s.labels[30],7);assert.equal(old.parts[3].color,'#fcf1d9');
});
test('all ten categories resolve correct opposite IDs/colors, single-stroke undo and erase from both sides',()=>{
 const s=current();assert.equal(PART_OPTIONS.length,10);for(const option of PART_OPTIONS)for(const x of [0,15,16,31]){
  const m=createLabelModel(s.labels),before=m.labels,category=PART_DEFINITIONS[option.id].category,ids=CATEGORY_PARTS[category];m.begin();m.paintAnatomical(x,3,option.id,true);m.end();const after=m.labels;
  assert.equal(after[3*32+Math.min(x,31-x)],ids.right);assert.equal(after[3*32+Math.max(x,31-x)],ids.left);if(option.id){assert.notEqual(s.parts[ids.left].color,s.parts[ids.right].color);assert.equal(s.parts[ids.left].side,'left');assert.equal(s.parts[ids.right].side,'right');}
  m.undo();assert.deepEqual(m.labels,before);m.redo();assert.deepEqual(m.labels,after);m.begin();m.paintAnatomical(x,3,0,true);m.end();assert.equal(m.labels[3*32+x],0);assert.equal(m.labels[3*32+31-x],0);
 }
});
test('odd center uses an explicit center identity and new explicit metadata survives export even when crossing sides',()=>{
 for(const option of PART_OPTIONS){const id=anatomicalPartId(option.id,2,5,'front');assert.equal(id,CATEGORY_PARTS[PART_DEFINITIONS[option.id].category].center);assert.equal(PART_DEFINITIONS[id].side,id===0?'none':'center');}
 const s=current(),labels=s.labels.slice();labels[0]=14;labels[31]=15;labels[16]=1;const out=JSON.parse(exportCorrections(s,labels));assert.equal(out.version,2);assert.equal(out.parts.length,28);assert.equal(out.parts[14].category,'eye');assert.equal(out.parts[14].side,'left');assert.equal(out.parts[14].key,'leftEye');assert.deepEqual(importCorrections(JSON.stringify(out),s),labels);
});
test('v1 backups migrate generics only; v2 validates machine identity/side/category and rejects mismatched source',()=>{
 const s=current(),old=legacy(),data=JSON.parse(exportCorrections(s,s.labels));data.version=1;data.parts=old.parts;data.labels=Array.from({length:2048},(_,i)=>i%14);assert.deepEqual(importCorrections(JSON.stringify(data),s),migrateLegacyLabels(data.labels));
 // Old display colors are cosmetic; IDs/names/source remain bound, never inferred from colors.
 data.parts[3].color='#ffffff';assert.deepEqual(importCorrections(JSON.stringify(data),s),migrateLegacyLabels(data.labels));
 for(const edit of [d=>d.parts[3].name='Wrong',d=>d.parts[12].id=13,d=>d.parts[3].extra=true,d=>d.labels[0]=14,d=>d.source.dummy.sha256='f'.repeat(64)]){const bad=structuredClone(data);edit(bad);assert.throws(()=>importCorrections(JSON.stringify(bad),s));}
 const out=JSON.parse(exportCorrections(s,s.labels));for(const edit of [d=>d.parts[14].key='rightEye',d=>d.parts[14].side='right',d=>d.parts[16].category='arm',d=>d.parts[12].color='#bbbbbb']){const bad=structuredClone(out);edit(bad);assert.throws(()=>importCorrections(JSON.stringify(bad),s));}
});
