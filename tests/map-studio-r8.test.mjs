import test from 'node:test';import assert from 'node:assert/strict';
import {newProject,newMap,placeObject,connectBuilding,setPassage,exportProject,importProject,clone,paint} from '../map-editor/model.js';
import {sameProjectContent} from '../map-editor/authoring.js';

test('room creation respects the same total-cell limit as project import, without partial mutation',()=>{
 const p=newProject();for(let i=1;i<=3;i++)p.maps.push(newMap('big-'+i,'Big',128,128));p.maps.push(newMap('almost','Almost',128,124),newMap('small','Small',14,8));const o=placeObject(p.maps[0],'cottage',2,2),before=clone(p);
 assert.equal(p.maps.reduce((n,m)=>n+m.w*m.h,0),65536);assert.throws(()=>connectBuilding(p,p.active,o),/65,536/);assert.deepEqual(p,before);assert.deepEqual(importProject(exportProject(p)),p);
});
test('colliding sanitized custom object IDs yield valid distinct room IDs and lossless project roundtrip',()=>{
 const p=newProject(),m=p.maps[0];for(const [x,id]of [[2,'a!'],[10,'a?']]){const o=placeObject(m,'cottage',x,2);o.id=id;connectBuilding(p,m.id,o);}
 assert.deepEqual(p.maps.slice(1).map(m=>m.id),['room-a','room-1-a']);assert.deepEqual(importProject(exportProject(p)),p);assert.deepEqual(m.objects.map(o=>o.id),['a!','a?']);
});
test('import never coerces or truncates object IDs into duplicates',()=>{
 for(const id of [1,undefined,'','x'.repeat(101)]){
  const p=newProject();p.maps[0].objects=[{id:'1',type:'planter',name:'A',x:1,y:1},{id,type:'planter',name:'B',x:2,y:1}];assert.throws(()=>importProject(exportProject(p)),/Object IDs/);
 }
});
test('unchanged passage updates retain the paired return and do not mutate any data',()=>{
 const p=newProject(),m=p.maps[0],o=placeObject(m,'cottage',2,2);connectBuilding(p,m.id,o);const before=clone(p);
 assert.equal(setPassage(p,m.id,{...m.warps[0]}),false);assert.deepEqual(p,before);
});
test('passage updates reject impossible direction, blocked approach and out-of-bounds arrival atomically',()=>{
 const p=newProject(),m=p.maps[0],o=placeObject(m,'cottage',2,2);connectBuilding(p,m.id,o);const before=clone(p),w=m.warps[0];
 assert.throws(()=>setPassage(p,m.id,{...w,direction:'right'}),/approach/);assert.throws(()=>setPassage(p,m.id,{...w,tx:999}),/clear walking/);assert.deepEqual(p,before);
 const q=newProject(),a=q.maps[0],b=newMap('other');q.maps.push(b);paint(a,5,6,'cliff');const snapshot=clone(q);
 assert.throws(()=>setPassage(q,a.id,{x:5,y:5,direction:'up',target:b.id,tx:5,ty:5}),/approach/);assert.deepEqual(q,snapshot);
});
test('identical project content ignores JSON key order while retaining significant map/object array order',()=>{
 const p=newProject(),m=p.maps[0],o=placeObject(m,'cottage',2,2);connectBuilding(p,m.id,o);placeObject(m,'planter',10,10);
 const imported=importProject(exportProject(p));assert.equal(sameProjectContent(p,imported),true);
 const reordered=clone(p);reordered.maps[0].objects.reverse();assert.equal(sameProjectContent(p,reordered),false);
 const changed=clone(p);changed.maps[0].terrain[0]='soil';assert.equal(sameProjectContent(p,changed),false);
});
