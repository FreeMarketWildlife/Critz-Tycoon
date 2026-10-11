import test from 'node:test';
import assert from 'node:assert/strict';
import {newProject,paint,placeObject,blocked,move,connectBuilding,doorCell,relocateDoorLinks,ledgeMask,validate,exportProject,importProject,cellRecipe,groundRecipe,MATERIALS,eraseAt} from '../map-editor/model.js';
import {readFileSync} from 'node:fs';
import {toolMatches} from '../map-editor/tool-search.js';

test('toolbox search finds semantic names and aliases across every category',()=>{
 assert.ok(toolMatches('house door','cottage','Cottage'));
 assert.ok(toolMatches('steps','stairs','Cliff stairs'));
 assert.ok(toolMatches('jump left','ledge-left'));
 assert.ok(toolMatches('roof','ME3.cottage.roof'));
 assert.equal(toolMatches('ocean shallow','water-fresh-still'),false);
 assert.ok(toolMatches('ocean shallow','water-ocean-shallow-still'));
});
test('one action creates a traversable north-facing doorway and south-facing return exit',()=>{
 const p=newProject(),m=p.maps[0],o=placeObject(m,'cottage',2,2),d=doorCell(o),room=connectBuilding(p,m.id,o);
 const entry=move(p,m.id,{x:d.x,y:d.y+1},'up');assert.equal(entry.map,room.id);
 assert.equal(blocked(room,entry.x,entry.y),false);
 const exit=move(p,room.id,{x:entry.x,y:entry.y},'down');assert.equal(exit.map,m.id);
 assert.deepEqual([exit.x,exit.y],[d.x,d.y+1]);
 assert.equal(move(p,m.id,{x:d.x-1,y:d.y},'right'),null);
 assert.equal(move(p,m.id,{x:d.x+1,y:d.y},'left'),null);
 assert.equal(blocked(m,d.x-1,d.y),true);assert.equal(blocked(m,d.x+1,d.y),true);
 assert.deepEqual(validate(p),[]);assert.deepEqual(importProject(exportProject(p)),p);
});
test('moving a house carries its entrance and the return destination together',()=>{
 const p=newProject(),m=p.maps[0],o=placeObject(m,'shop',2,2),room=connectBuilding(p,m.id,o),old={x:o.x,y:o.y};
 m.spawn={x:1,y:1};o.x=8;o.y=7;relocateDoorLinks(p,m.id,o,old);
 assert.deepEqual([m.warps[0].x,m.warps[0].y],[11,11]);
 assert.deepEqual([room.warps[0].tx,room.warps[0].ty],[11,12]);
 assert.deepEqual(validate(p),[]);
});
test('room creation rejects blocked approaches, duplicate passages and map limits without mutation',()=>{
 const p=newProject(),m=p.maps[0],o=placeObject(m,'garden',2,2);paint(m,4,7,'fence');
 const before=exportProject(p);assert.throws(()=>connectBuilding(p,m.id,o),/Clear/);assert.equal(exportProject(p),before);
 paint(m,4,7,'erase');connectBuilding(p,m.id,o);assert.throws(()=>connectBuilding(p,m.id,o),/already linked/);
});
test('validation reports absent doors, roads blocked by fences, bad stairs and ledge landings',()=>{
 const p=newProject(),m=p.maps[0];placeObject(m,'cottage',2,2);
 paint(m,12,3,'path');paint(m,12,3,'fence');paint(m,12,6,'water');paint(m,12,6,'stairs');
 paint(m,12,9,'ledge-down');paint(m,12,10,'cliff');
 const issues=validate(p).join('\n');for(const text of ['no linked doorway','fence blocks the road','cannot cross water','blocked landing'])assert.ok(issues.includes(text),text);
 assert.equal(blocked(m,12,6),true);
});
test('ledges connect along their tangent only and preserve directional two-cell hops',()=>{
 for(const dir of ['up','down','left','right']){
  const p=newProject(),m=p.maps[0],f='ledge-'+dir,horizontal=['up','down'].includes(dir),[dx,dy]=horizontal?[1,0]:[0,1];
  for(let i=-1;i<=1;i++)paint(m,8+i*dx,8+i*dy,f);
  assert.equal(ledgeMask(m,8,8,f),3);assert.equal(ledgeMask(m,8-dx,8-dy,f),2);assert.equal(ledgeMask(m,8+dx,8+dy,f),1);
  paint(m,8-dx,8-dy,'erase');assert.equal(ledgeMask(m,8,8,f),2);
 }
});
test('three-material corners use the adjacent ground before a conflicting diagonal',()=>{
 const p=newProject(),m=p.maps[0];m.terrain.fill('soil');paint(m,7,8,'path');paint(m,7,7,'paving');
 assert.ok(cellRecipe(m,8,8).quadrants[0].startsWith('blend.soil.path.'),cellRecipe(m,8,8).quadrants[0]);
});

test('every revised sand/surface neighbor shape resolves a native tile for every material pair',()=>{const paths=['assets/playable/overworld/master.json','assets/review/map-editor/master.json','assets/review/map-studio-r3/atlas.json'],ids=new Set(paths.flatMap(path=>JSON.parse(readFileSync(path)).tiles.map(t=>t.id)));for(const kind of MATERIALS)for(const under of MATERIALS)for(let mask=0;mask<256;mask++){const p=newProject(),m=p.maps[0];m.terrain.fill(under);m.terrain[8*m.w+8]=kind;for(const[dx,dy,b]of [[0,-1,1],[1,0,2],[0,1,4],[-1,0,8],[1,-1,16],[1,1,32],[-1,1,64],[-1,-1,128]])if(mask&b)m.terrain[(8+dy)*m.w+8+dx]=kind;for(const id of groundRecipe(m,8,8))assert.ok(ids.has(id),id);}});

test('erasing a building removes both door links while retaining its editable interior',()=>{const p=newProject(),m=p.maps[0],o=placeObject(m,'cottage',2,2),room=connectBuilding(p,m.id,o);eraseAt(p,m.id,2,2);assert.equal(m.objects.length,0);assert.equal(m.warps.length,0);assert.equal(room.warps.length,0);assert.equal(p.maps.length,2);});
