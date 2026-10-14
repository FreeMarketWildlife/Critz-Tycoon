import test from 'node:test';
import assert from 'node:assert/strict';
import {createState,startMorning,validateState,save,load,SAVE_KEY,BACKUP_KEY} from '../src/state.js';
import {migrateGridState} from '../src/grid-save.js';
import {scenes,isBlocked,fenceCrossing,transition,nearestEntity,getEntities} from '../src/world.js';
import {BEAR_ART,BEAR_CLOSED,BEAR_ASIDE,routeBear} from '../src/route-bear.js';
import {worldViewport,centeredCamera,heroFocus,normalizeZoom} from '../src/world-space.js';
import {readSettings,writeSettings,UI_SETTINGS_KEY} from '../src/ui-settings.js';
import {newMap,placeObject,objectFootprint,objectArtBounds,objectDepth,blocked,exportProject,importProject,newProject} from '../map-editor/model.js';
const fixture=(scene='forest',x=9,y=22)=>{const s=createState('Ari','girl','River');startMorning(s,true);s.scene=scene;s.player={x,y,facing:'up'};return s;};
function reachable(s){const q=[scenes[s.scene].safeSpawn],seen=new Set(q.map(p=>p.join(',')));for(let i=0;i<q.length;i++){const [x,y]=q[i];for(const [dx,dy]of [[1,0],[-1,0],[0,1],[0,-1]]){const a=x+dx,b=y+dy,k=`${a},${b}`;if(!seen.has(k)&&!isBlocked(s.scene,a,b,s)&&!fenceCrossing(s.scene,{x,y},{x:a,y:b})){seen.add(k);q.push([a,b]);}}}return seen;}
test('resting bear closes the actual route throat, leaves southern play intact, and talks from every occupied cell',()=>{
 const solidBefore=new Set(scenes.forest.map.solid),s=fixture(),baseline=reachable({...s,omitRouteBear:true}),closed=reachable(s),bear=routeBear(s);
 assert.deepEqual(bear.collision,BEAR_CLOSED);assert.equal(baseline.size,559);assert.equal(closed.size,207);
 for(const x of [8,9,10]){assert.ok(isBlocked('forest',x,21,s));s.player={x,y:22,facing:'up'};assert.equal(nearestEntity(s).id,'route-bear');}
 assert.ok(closed.has('13,32'));assert.ok(!closed.has('13,2'));assert.ok(!closed.has('9,20'));
 assert.deepEqual(scenes.forest.map.solid,solidBefore);assert.equal(scenes.forest.map.solid.has('9,21'),false);
 assert.match(bear.text,/blocked for now/);assert.ok(!getEntities(s).some(e=>e.id==='route-bear'&&e.type==='npc'));
});
test('established access moves the visible bear aside and preserves all original remaining connected floor',()=>{
 const s=fixture();s.liarsvilleBearAccess=true;const cells=reachable(s),base=reachable({...s,omitRouteBear:true});
 assert.deepEqual(routeBear(s).collision,BEAR_ASIDE);assert.equal(cells.size,556);
 for(const key of base)assert.equal(cells.has(key),!['17,22','18,22','19,22'].includes(key),key);
 for(const key of ['13,2','13,3','13,32','9,20'])assert.ok(cells.has(key));
});
test('legacy north, fractional, footprint and visited saves retain access before recovery; new southern saves remain blocked',()=>{
 for(const [scene,x,y,history]of [['forest',9,20,[]],['forest',9.25,20.25,[]],['forest',9,21,[]],['forest',9,22,['liarsville']],['liarsville',14,28,[]],['waterworks',8,9,[]]]){
  const s=fixture(scene,x,y);delete s.liarsvilleBearAccess;delete s.gridVersion;delete s.worldVersion;s.flags.visited.push(...history);const bytes=JSON.stringify(s),next=migrateGridState(s);
  assert.equal(JSON.stringify(s),bytes);assert.equal(next.liarsvilleBearAccess,true);assert.ok(validateState(next));assert.deepEqual(migrateGridState(next),next);
  for(const k of ['hero','gender','rival','flags','inventory','money','debt','tank','posts'])assert.deepEqual(next[k],s[k],k);
  if(scene==='forest'&&y<21)assert.ok(next.player.y<21);
 }
 const south=migrateGridState(fixture());assert.equal(south.liarsvilleBearAccess,false);assert.deepEqual(south.player,{x:9,y:22,facing:'up'});
});
test('north-origin transitions cannot strand prior travelers and compatibility saves preserve exact old backup bytes',()=>{
 const s=fixture('liarsville',14,28),old=JSON.stringify(s,null,2),data=new Map([[SAVE_KEY,old]]),store={getItem:k=>data.get(k)||null,setItem:(k,v)=>data.set(k,v)};
 transition(s,scenes.liarsville.entities.find(e=>e.to==='forest'));assert.equal(s.liarsvilleBearAccess,true);assert.deepEqual([s.player.x,s.player.y],[13,3]);
 assert.ok(save(s,store));assert.equal(store.getItem(BACKUP_KEY),old);assert.equal(load(store).state.liarsvilleBearAccess,true);
 for(const value of [null,1,'true',[],{}])assert.equal(validateState({...s,liarsvilleBearAccess:value}),false);
 delete s.liarsvilleBearAccess;assert.ok(validateState(s));assert.equal(validateState(undefined),false);
});
test('editor bear uses the same independent footprint, draw bounds, front depth, collision and v1 project roundtrip',()=>{
 const p=newProject(),m=p.maps[0],o=placeObject(m,'bear',5,5);assert.equal(typeof o,'object');assert.deepEqual(objectFootprint(o),{x:5,y:5,w:3,h:1});assert.deepEqual(objectArtBounds(o),{x:5,y:4,w:3,h:3});assert.equal(objectDepth(o),6);
 for(let y=4;y<=6;y++)for(let x=4;x<=8;x++)assert.equal(blocked(m,x,y),y===5&&x>=5&&x<8);
 assert.deepEqual(importProject(exportProject(p)),p);assert.deepEqual(BEAR_ART.drawOffset,[0,-32]);assert.deepEqual(BEAR_ART.groundAnchor,[48,80]);
});
test('exactly three scales retain the widest default and use integer native pixels at both closer phone levels',()=>{
 for(const [w,h]of [[320,568],[390,844],[844,390],[1280,900],[1920,1080]]){const fields=[0,1,2].map(z=>worldViewport(w,h,z));assert.ok(fields[0].scale<fields[1].scale&&fields[1].scale<fields[2].scale);for(const f of fields){assert.equal(f.width%2,0);assert.equal(f.height%2,0);assert.ok(f.width*f.scale>=w&&f.height*f.scale>=h);}assert.ok(Number.isInteger(fields[1].scale)&&Number.isInteger(fields[2].scale));}
 for(const value of [undefined,null,-1,3,1.2,'2',NaN,Infinity])assert.equal(normalizeZoom(value),0);
});
test('stable Hero body focus stays centered at every edge/corner, every zoom and both identities without map clamps',()=>{
 for(const gender of ['boy','girl'])for(const z of [0,1,2])for(const size of [[390,620],[844,242],[1280,700]]){const f=worldViewport(...size,z);for(const foot of [{x:16,y:32},{x:624,y:32},{x:16,y:640},{x:624,y:640},{x:-16,y:-32},{x:277,y:413}]){const cam=centeredCamera(foot,f.width,f.height,gender),focus=heroFocus(foot,gender);assert.equal(focus.x-cam.x,f.width/2);assert.equal(focus.y-cam.y,f.height/2);assert.ok(Number.isInteger(cam.x)&&Number.isInteger(cam.y));}}
});
test('zoom preference defaults safely, roundtrips all levels, keeps old preferences, and never writes adventure progress',()=>{
 const data=new Map([[SAVE_KEY,'synthetic-progress']]),store={getItem:k=>data.get(k),setItem:(k,v)=>data.set(k,v)};
 for(const old of ['{"frame":"ocean","calm":true}','null','[]','broken']){data.set(UI_SETTINGS_KEY,old);assert.equal(readSettings(store).worldZoom,0);}
 for(const worldZoom of [0,1,2]){assert.ok(writeSettings(store,{frame:'sunset',calm:true,worldZoom}));assert.deepEqual(readSettings(store),{frame:'sunset',calm:true,worldZoom});}
 assert.equal(data.get(SAVE_KEY),'synthetic-progress');assert.equal(writeSettings({setItem(){throw Error('quota');}},readSettings(store)),false);
 for(const bad of [3,-1,'1',1.25]){data.set(UI_SETTINGS_KEY,JSON.stringify({worldZoom:bad}));assert.equal(readSettings(store).worldZoom,0);}
});
