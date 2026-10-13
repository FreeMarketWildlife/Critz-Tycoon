import test from 'node:test';import assert from 'node:assert/strict';
import {newProject,newMap,paint,placeObject,objectAt,objectsAt,blocked,at,connectBuilding,exportProject,importProject,clone} from '../map-editor/model.js';
import {copySelection,pasteSelection,moveStamp,sampleCell,paintLayer,floodLayer,mapCamera} from '../map-editor/authoring.js';

test('canopies can overlap props while occupied cells stay distinct and picking favors footprints',()=>{
 const p=newProject(),m=p.maps[0],tree=placeObject(m,'tree',5,5),bench=placeObject(m,'bench',5,5);
 assert.equal(typeof bench,'object');assert.equal(objectAt(m,5,5),bench);assert.equal(objectAt(m,5,6),tree);
 assert.equal(objectsAt(m,5,5).length,2);assert.equal(typeof placeObject(m,'planter',5,6),'string');
 assert.deepEqual(importProject(exportProject(p)),p);
});
test('occupied bounds allow registered canopy overhang and retain v1 coordinates on import',()=>{
 const p=newProject(),m=p.maps[0],o=placeObject(m,'tree',3,-1);assert.equal(typeof o,'object');assert.ok(blocked(m,3,0));
 assert.equal(typeof placeObject(m,'tree',3,-2),'string');assert.deepEqual(importProject(exportProject(p)),p);
});
test('all-layer selection copy/paste is lossless for cells but gives clones new identities and no copied passages',()=>{
 const p=newProject(),m=p.maps[0],o=placeObject(m,'cottage',2,2);connectBuilding(p,m.id,o);m.spawn={x:1,y:1};
 paint(m,2,2,'soil');m.raw[at(m,3,2)]={id:'meadow.grass.0',blocked:false};paint(m,6,2,'flowers');
 const original=clone(p),clip=copySelection(p,m.id,{x:2,y:2,w:5,h:5}),out=pasteSelection(p,m.id,clip,11,2),target=out.project.maps[0];
 assert.deepEqual(p,original);assert.equal(target.objects.length,2);assert.notEqual(target.objects[1].id,o.id);assert.equal(target.objects[1].name,o.name);
 assert.deepEqual(target.warps,m.warps);assert.deepEqual(out.project.maps[1],p.maps[1]);assert.deepEqual(target.spawn,m.spawn);
 for(let y=0;y<5;y++)for(let x=0;x<5;x++){assert.equal(target.terrain[at(target,11+x,2+y)],m.terrain[at(m,2+x,2+y)]);assert.equal(target.features[at(target,11+x,2+y)],m.features[at(m,2+x,2+y)]);}
 assert.deepEqual(target.raw[at(target,12,2)],m.raw[at(m,3,2)]);assert.deepEqual(importProject(exportProject(out.project)),out.project);
});
test('partial props are rejected only when copying Props; doorway-only selection does not copy a building',()=>{
 const p=newProject(),m=p.maps[0];placeObject(m,'tree',4,4);
 assert.throws(()=>copySelection(p,m.id,{x:4,y:5,w:1,h:1}),/cuts through/);
 assert.doesNotThrow(()=>copySelection(p,m.id,{x:4,y:5,w:1,h:1},['ground']));
 const building=placeObject(m,'cottage',10,2);assert.equal(copySelection(p,m.id,{x:12,y:6,w:1,h:1}).objects.length,0);assert.ok(building.id);
});
test('copying only occupied tree cells retains native overhang when pasted at a map edge',()=>{
 const p=newProject(),m=p.maps[0];placeObject(m,'tree',4,4);const clip=copySelection(p,m.id,{x:4,y:5,w:2,h:1},['objects']);
 const out=pasteSelection(p,m.id,clip,8,0);assert.equal(out.objects[0].y,-1);assert.ok(blocked(out.project.maps[0],8,0));assert.deepEqual(importProject(exportProject(out.project)),out.project);
});
test('repeated paste rejects overlap and bounds atomically, without editing originals or copied data',()=>{
 const p=newProject(),m=p.maps[0];placeObject(m,'tree',4,4);const clip=copySelection(p,m.id,{x:4,y:5,w:2,h:1},['objects']),copy=clone(clip);
 const a=pasteSelection(p,m.id,clip,8,5),b=pasteSelection(a.project,m.id,clip,12,5);
 assert.equal(new Set(b.project.maps[0].objects.map(o=>o.id)).size,3);const before=clone(b.project);
 assert.throws(()=>pasteSelection(b.project,m.id,clip,8,5),/overlaps/);assert.throws(()=>pasteSelection(b.project,m.id,clip,19,19),/whole selection/);assert.deepEqual(b.project,before);assert.deepEqual(clip,copy);
});
test('explicit layer paint, erase and flood leave other layers and links intact; Auto retains legacy restoration',()=>{
 const p=newProject(),m=p.maps[0];paint(m,3,3,'flowers');m.raw[at(m,3,3)]={id:'meadow.grass.0',blocked:false};m.warps.push({x:3,y:3,direction:'up',target:m.id,tx:3,ty:4});
 paintLayer(p,m.id,3,3,'soil','ground');assert.equal(m.features[at(m,3,3)],'flowers');assert.ok(m.raw[at(m,3,3)]);
 floodLayer(p,m.id,3,3,'path','ground');assert.equal(m.features[at(m,3,3)],'flowers');assert.ok(m.raw[at(m,3,3)]);
 paintLayer(p,m.id,3,3,'','features',{erase:true});assert.equal(m.features[at(m,3,3)],'');assert.ok(m.raw[at(m,3,3)]);assert.equal(m.warps.length,1);
 paintLayer(p,m.id,3,3,'','raw',{erase:true});assert.equal(m.raw[at(m,3,3)],undefined);assert.equal(m.warps.length,1);
 paint(m,3,3,'flowers');paintLayer(p,m.id,3,3,'grass');assert.equal(m.features[at(m,3,3)],'');assert.equal(m.warps.length,1);
});
test('layer-limited paste preserves existing props, features, exact collision and travel',()=>{
 const p=newProject(),m=p.maps[0];paint(m,2,2,'soil');placeObject(m,'planter',8,8);paint(m,8,8,'flowers');m.raw[at(m,8,8)]={id:'meadow.grass.0',blocked:false};m.warps.push({x:9,y:8,direction:'up',target:m.id,tx:9,ty:9});
 const clip=copySelection(p,m.id,{x:2,y:2,w:1,h:1},['ground']),out=pasteSelection(p,m.id,clip,8,8).project.maps[0];
 assert.equal(out.terrain[at(out,8,8)],'soil');assert.deepEqual(out.objects,m.objects);assert.deepEqual(out.features,m.features);assert.deepEqual(out.raw,m.raw);assert.deepEqual(out.warps,m.warps);
});
test('paste and placement cannot block an existing passage, arrival or building approach',()=>{
 const p=newProject(),m=p.maps[0],room=newMap('room');p.maps.push(room);paint(m,2,2,'cliff');
 m.warps.push({x:8,y:8,direction:'up',target:room.id,tx:2,ty:2});room.warps.push({x:2,y:3,direction:'down',target:m.id,tx:8,ty:9});
 const clip=copySelection(p,m.id,{x:2,y:2,w:1,h:1},['ground']);assert.throws(()=>pasteSelection(p,m.id,clip,8,8),/existing passage/);assert.throws(()=>pasteSelection(p,m.id,clip,8,9),/existing arrival/);
 const o=placeObject(m,'cottage',12,2);assert.equal(typeof placeObject(m,'planter',14,6),'string');assert.equal(typeof placeObject(m,'planter',14,7),'string');assert.ok(o.id);
});
test('transactional moves preserve object identity and paired door destinations, with failure leaving source untouched',()=>{
 const p=newProject(),m=p.maps[0],o=placeObject(m,'cottage',2,2);connectBuilding(p,m.id,o);const original=clone(p),out=moveStamp(p,m.id,o.id,3,3);
 assert.deepEqual(p,original);assert.equal(out.maps[0].objects[0].id,o.id);assert.deepEqual([out.maps[0].warps[0].x,out.maps[0].warps[0].y],[5,7]);assert.deepEqual([out.maps[1].warps[0].tx,out.maps[1].warps[0].ty],[5,8]);
 assert.throws(()=>moveStamp(p,m.id,o.id,19,19));assert.deepEqual(p,original);
});
test('eyedropper prioritizes props or an explicit layer and preserves raw collision without edits',()=>{
 const p=newProject(),m=p.maps[0];placeObject(m,'tree',4,4);placeObject(m,'bench',4,4);paint(m,4,4,'soil');paint(m,4,4,'flowers');m.raw[at(m,4,4)]={id:'meadow.grass.0',blocked:false};const before=clone(p);
 assert.deepEqual(sampleCell(m,4,4),{kind:'stamp',value:'bench'});assert.deepEqual(sampleCell(m,4,4,'ground'),{kind:'brush',value:'soil'});assert.deepEqual(sampleCell(m,4,4,'features'),{kind:'brush',value:'flowers'});assert.deepEqual(sampleCell(m,4,4,'raw'),{kind:'raw',id:'meadow.grass.0',blocked:false});assert.deepEqual(p,before);
});
test('playtest camera clamps large maps and centers undersized interiors',()=>{
 const m=newMap();assert.deepEqual(mapCamera(m,{x:0,y:0}),{x:0,y:0});assert.deepEqual(mapCamera(m,{x:19,y:19}),{x:160,y:320});
 assert.deepEqual(mapCamera(newMap('room','Room',11,9),{x:5,y:7}),{x:-64,y:-16});
});
test('repeat authoring cannot create a project exceeding its v1 imported prop limit',()=>{
 const p=newProject(),m=newMap('map-1','Limit',128,128);p.maps=[m];
 m.objects=Array.from({length:4096},(_,i)=>({id:'existing-'+i,type:'planter',name:'Planter',x:i%128,y:Math.floor(i/128)}));
 const clip=copySelection(p,m.id,{x:0,y:0,w:1,h:1},['objects']),before=clone(p);
 assert.throws(()=>pasteSelection(p,m.id,clip,50,100),/limit/);assert.equal(typeof placeObject(m,'planter',50,100),'string');assert.deepEqual(p,before);
 assert.deepEqual(importProject(exportProject(p)),p);
});
test('Props-only erase acts on occupied cells while retaining overhead art and other cell layers',()=>{
 const p=newProject(),m=p.maps[0],tree=placeObject(m,'tree',4,4),bench=placeObject(m,'bench',4,4);paint(m,4,4,'flowers');m.raw[at(m,4,4)]={id:'meadow.grass.0',blocked:false};
 paintLayer(p,m.id,4,4,'','objects',{erase:true});assert.equal(m.objects.includes(bench),false);assert.ok(m.objects.includes(tree));
 paintLayer(p,m.id,4,4,'','objects',{erase:true});assert.ok(m.objects.includes(tree));assert.equal(m.features[at(m,4,4)],'flowers');assert.ok(m.raw[at(m,4,4)]);
});
