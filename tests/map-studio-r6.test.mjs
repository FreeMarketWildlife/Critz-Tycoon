import test from 'node:test';
import assert from 'node:assert/strict';
import {newProject,newMap,paint,move,blocked,at,cellRecipe,ledgeMask,validationIssues,validate,placeObject,connectBuilding,resizeMap,removePassage,clone} from '../map-editor/model.js';

test('walkable exact overrides replace ledges, stairs, caves and bridges without hidden traversal',()=>{
  for (const feature of ['ledge-down','ledge-up','stairs','cave','bridge','fence']) {
    const p=newProject(),m=p.maps[0]; paint(m,5,6,feature);
    m.raw[at(m,5,6)]={id:'meadow.grass.0',blocked:false};
    assert.equal(blocked(m,5,6),false);
    const step=move(p,m.id,{x:5,y:5},'down');
    assert.deepEqual([step.x,step.y,step.jump],[5,6,false],feature);
    assert.equal(cellRecipe(m,5,6).feature,'');
    m.raw[at(m,5,6)].blocked=true;
    assert.equal(move(p,m.id,{x:5,y:5},'down'),null,feature);
  }
});
test('raw overrides remove fence and ledge branches from neighboring automatic joins',()=>{
  const p=newProject(),m=p.maps[0];
  paint(m,5,5,'fence');paint(m,6,5,'fence');
  m.raw[at(m,6,5)]={id:'meadow.grass.0',blocked:false};
  assert.equal(cellRecipe(m,5,5).feature,'fence.wood.0');
  paint(m,5,8,'ledge-down');paint(m,6,8,'ledge-down');
  m.raw[at(m,6,8)]={id:'meadow.grass.0',blocked:false};
  assert.equal(ledgeMask(m,5,8,'ledge-down'),0);
});
test('a painted ledge cannot grant a hop through deep or shallow water',()=>{
  for(const water of ['water','water-fresh-shallow-still']) {
    const p=newProject(),m=p.maps[0];paint(m,5,6,water);paint(m,5,6,'ledge-down');
    assert.equal(move(p,m.id,{x:5,y:5},'down'),null);
  }
});
test('canonical mixed-depth enclosure is checked without rejecting separate deep-only bodies',()=>{
  const p=newProject(),m=p.maps[0];
  for(let y=3;y<7;y++)for(let x=3;x<7;x++)paint(m,x,y,'water-fresh-still');
  for(let y=12;y<14;y++)for(let x=12;x<14;x++)paint(m,x,y,'water-fresh-shallow-still');
  assert.deepEqual(validate(p),[]);
  paint(m,3,3,'water-fresh-shallow-still');
  const issue=validationIssues(p).find(a=>a.code==='water-border');
  assert.ok(issue);assert.equal(issue.mapId,m.id);assert.ok(Number.isInteger(issue.x)&&Number.isInteger(issue.y));
});
test('reachability reports an enclosed Hero and passages with inaccessible directional approaches',()=>{
  const p=newProject(),m=p.maps[0],room=newMap('room');p.maps.push(room);m.spawn={x:2,y:2};
  for(const [x,y]of [[2,1],[3,2],[2,3],[1,2]])paint(m,x,y,'cliff');
  m.warps.push({x:10,y:10,direction:'up',target:room.id,tx:10,ty:10});
  room.warps.push({x:10,y:11,direction:'down',target:m.id,tx:10,ty:11});
  const before=clone(p),issues=validationIssues(p);
  assert.ok(issues.some(a=>a.code==='spawn-trapped'&&a.x===2&&a.y===2));
  assert.ok(issues.some(a=>a.code==='passage-unreachable'&&a.x===10&&a.y===10));
  assert.deepEqual(p,before,'validation must never push or edit objects');
});
test('reachable ledge and rail-gap routes are recognized using actual directional movement',()=>{
  const p=newProject(),m=p.maps[0],other=newMap('other');p.maps.push(other);m.spawn={x:5,y:5};
  for(let x=0;x<m.w;x++)paint(m,x,6,'cliff');paint(m,5,6,'grass');paint(m,5,6,'ledge-down');
  m.warps.push({x:5,y:8,direction:'down',target:other.id,tx:5,ty:5});other.warps.push({x:5,y:6,direction:'down',target:m.id,tx:5,ty:7});
  assert.equal(validationIssues(p).some(a=>a.code==='passage-unreachable'),false);
});
test('project-aware shrinking removes cropped building links and retains unrelated links and editable rooms',()=>{
  const p=newProject(),m=p.maps[0],o=placeObject(m,'cottage',12,2),room=connectBuilding(p,m.id,o),other=newMap('other');p.maps.push(other);
  m.warps.push({x:3,y:4,direction:'up',target:other.id,tx:3,ty:3});
  other.warps.push({x:3,y:4,direction:'down',target:m.id,tx:3,ty:5});
  resizeMap(m,10,20,p);
  assert.equal(m.objects.length,0);assert.equal(room.warps.length,0);assert.ok(p.maps.includes(room));
  assert.equal(m.warps.length,1);assert.equal(other.warps.length,1);
  assert.equal(validationIssues(p).some(a=>a.code==='passage-destination'),false);
});
test('cropping passage cells and removing paired passages never leave stale reciprocals',()=>{
  const p=newProject(),m=p.maps[0],o=placeObject(m,'cottage',2,2),room=connectBuilding(p,m.id,o);
  const original=clone(p);removePassage(p,m.id,m.warps[0]);
  assert.equal(m.warps.length,0);assert.equal(room.warps.length,0);
  const outside=original.maps[0],inside=original.maps[1];
  resizeMap(inside,11,8,original);
  assert.equal(inside.warps.length,0);assert.equal(outside.warps.length,0);
});
