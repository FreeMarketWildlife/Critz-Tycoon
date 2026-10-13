import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {treePlacement,treeStyle,TREE_FILES} from '../src/tree-art.js';
import {STAMPS,groveReviewProject,validate,blocked,exportProject,importProject} from '../map-editor/model.js';
const metadata=JSON.parse(fs.readFileSync(new URL('../assets/review/trees-r2/objects.json',import.meta.url)));
test('transparent trees register artwork, sort anchor and two-cell footprint independently',()=>{
 assert.equal(metadata.assets.length,TREE_FILES.length);
 for(const a of metadata.assets){const p=treePlacement(a,5,7),[left,top,w,h]=a.collisionRectPixels;
  assert.deepEqual([p.x+left,p.y+top,w,h],[160,224,64,32]);
  assert.equal(p.depth,p.y+a.sortAnchorPixels[1]);
  assert.equal(p.y+a.groundAnchorPixels[1],272);
 }
});
test('all tree editor styles keep two ground cells and round-trip without changing old tree semantics',()=>{
 const p=groveReviewProject();assert.deepEqual(validate(p,new Set()),[]);
 const q=importProject(exportProject(p),new Set());assert.deepEqual(q,p);
 for(const type of ['tree','cypress','willow','palm']){const o=p.maps[0].objects.find(o=>o.type===type),s=STAMPS[type];
  assert.deepEqual(s.footprint.slice(2),[2,1]);
  assert.ok(blocked(p.maps[0],o.x,o.y+s.footprint[1]));
  assert.ok(blocked(p.maps[0],o.x+1,o.y+s.footprint[1]));
  assert.equal(blocked(p.maps[0],o.x,o.y+s.footprint[1]+1),false);
 }
});
test('world tree selection uses rooted species and nearby water while preserving fruit identity',()=>{
 assert.equal(treeStyle({id:'tree.cypress.rooted'}),'tiered-cedar');
 assert.equal(treeStyle({type:'palm'}),'coastal-palm');
 const map={w:10,h:10,terrain:Array(100).fill('grass')};map.terrain[45]='water';
 assert.equal(treeStyle({id:'tree.broadleaf.rooted',collision:[4,5,2,1]},'forest',map),'soft-willow');
 assert.equal(treeStyle({id:'tree.broadleaf.rooted',collision:[4,5,2,1]},'yard',map),'old-grove');
});
