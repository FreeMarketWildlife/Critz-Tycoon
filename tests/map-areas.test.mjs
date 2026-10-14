import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';
import {AREAS,selectedArea,areaHref,areaDraftKey} from '../map-editor/areas.js';import {importProject,exportProject,move,validationIssues,SAVE_KEY} from '../map-editor/model.js';
const raw=readFileSync(new URL('../map-editor/areas/rootport.json',import.meta.url),'utf8');
test('Named Rootport preserves the submitted layout, object IDs, Hero start and reciprocal cottage links',()=>{
 const p=importProject(raw),m=p.maps[0];assert.equal(p.name,'Rootport');assert.equal(m.name,'Rootport');assert.equal(p.active,'grove-review');assert.deepEqual([m.w,m.h],[22,16]);assert.equal(m.terrain.length,352);assert.equal(m.features.length,352);assert.deepEqual(m.spawn,{x:9,y:8});assert.deepEqual(m.objects.map(o=>[o.id,o.type,o.x,o.y]),[['obj-1792004091741-0','cottage',5,2]]);
 const inside=move(p,m.id,{x:7,y:7},'up');assert.equal(inside.map,'room-obj-1792004091741-0');const outside=move(p,inside.map,{x:5,y:7},'down');assert.deepEqual({x:outside.x,y:outside.y,map:outside.map},{x:7,y:7,map:m.id});assert.deepEqual(importProject(exportProject(p)),p);
 assert.equal(validationIssues(p).filter(i=>i.code==='water-width').length,1,'Preserve the supplied narrow water cells for editing, without silently rewriting them');
});
test('Area revisions isolate local drafts and reject unknown area names',()=>{
 const a=selectedArea('rootport');assert.equal(AREAS.length,1);assert.equal(areaHref(a.id),'?area=rootport');assert.notEqual(areaDraftKey(a),SAVE_KEY);assert.notEqual(areaDraftKey(a),areaDraftKey({...a,revision:2}));assert.equal(selectedArea('../../outside'),null);assert.throws(()=>areaHref('outside'));
});
