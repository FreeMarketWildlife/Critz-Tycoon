import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync}from'node:fs';
import {overworldMaps,buildings,normalizeMask} from '../src/overworld.js';
import {scenes,isBlocked,transition} from '../src/world.js';
import {animationFrame} from '../src/environment-render.js';
import {createState,startMorning,save,load,validateState,SAVE_KEY,BACKUP_KEY,PRE_WORLD_KEY,PRE_WORLD_BACKUP_KEY}from'../src/state.js';
import {migrateGridState}from'../src/grid-save.js';
const manifest=JSON.parse(readFileSync(new URL('../assets/playable/overworld/master.json',import.meta.url))),old=JSON.parse(readFileSync(new URL('../assets/review/overworld-v1/master.json',import.meta.url))),ids=new Set(manifest.tiles.map(t=>t.id));
test('all map tile references resolve and original tile IDs keep their atlas coordinates',()=>{
 for(const t of old.tiles){const now=manifest.tiles.find(n=>n.id===t.id);assert.deepEqual([now.index,now.x,now.y],[t.index,t.x,t.y]);}
 assert.equal(ids.size,manifest.tiles.length);
 for(const m of Object.values(overworldMaps)){assert.equal(m.ground.length,m.w*m.h);for(const id of [...m.ground,...m.decals.map(d=>d.id),...m.objects.flatMap(o=>o.tiles?o.tiles.flat():manifest.assemblies[o.id]?.flat()||[o.id])])assert.ok(ids.has(id),id);}
});
test('normalization covers all 47 shapes and animated IDs resolve through complete loops',()=>{assert.equal(new Set(Array.from({length:256},(_,i)=>normalizeMask(i))).size,47);for(const id of [...old.tiles.filter(t=>t.terrain==='water').map(t=>t.id),'flowers.0','flowers.5','waterfall.0.0','waterfall.0.2']){const phases=new Set();for(let t=0;t<2;t+=.07){const frame=animationFrame(id,t);assert.ok(ids.has(frame),frame);phases.add(frame);}assert.ok(phases.size>=3,id);}});
test('Rootport door approaches connect to the paved/path network rather than ending in flower beds',()=>{const m=overworldMaps.town;for(const b of buildings){for(let y=b.doorY;y<=b.doorY+1;y++)assert.equal(m.terrain[y*m.w+b.doorX],'path',b.name);}});
test('the northern forest route cannot bypass the walk-through tall-grass meadow',()=>{
 const m=overworldMaps.forest,q=[[13,31]],seen=new Set(['13,31']);for(let n=0;n<q.length;n++){const [x,y]=q[n];for(const [dx,dy]of [[0,1],[0,-1],[1,0],[-1,0]]){const a=x+dx,b=y+dy,k=`${a},${b}`;if(!seen.has(k)&&!m.grass.has(k)&&!isBlocked('forest',a,b)){seen.add(k);q.push([a,b]);}}}assert.ok(!seen.has('13,2'));
});
function oldState(scene='town'){const s=createState('Ari','boy','Robin');startMorning(s,true);s.scene=scene;s.player={x:25,y:8,facing:'up'};delete s.worldVersion;return s;}
const store=(entries,fail)=>{const data=new Map(entries);return{data,getItem:k=>data.get(k)||null,setItem:(k,v)=>{if(k===fail)throw Error('Quota');data.set(k,v);}};};
test('world migration keeps all progress and nearest familiar doorway; runs once',()=>{const s=oldState(),before=structuredClone(s),m=migrateGridState(s);assert.deepEqual(s,before);assert.deepEqual([m.player.x,m.player.y],[buildings[2].doorX,buildings[2].doorY+1]);const strip=x=>{const c=structuredClone(x);delete c.worldVersion;delete c.player.x;delete c.player.y;return c;};assert.deepEqual(strip(m),strip(s));assert.deepEqual(migrateGridState(m),m);assert.ok(validateState(m));});
test('pre-world primary and backup retain exact original bytes and abort safely on quota',()=>{
 const a=' \n'+JSON.stringify(oldState())+'\n',b=JSON.stringify(oldState('yard'));for(const fail of [undefined,PRE_WORLD_KEY,PRE_WORLD_BACKUP_KEY]){const storage=store([[SAVE_KEY,a],[BACKUP_KEY,b]],fail),m=migrateGridState(JSON.parse(a));assert.equal(save(m,storage),!fail);if(fail){assert.equal(storage.data.get(SAVE_KEY),a);assert.equal(storage.data.get(BACKUP_KEY),b);}else{assert.equal(storage.data.get(PRE_WORLD_KEY),a);assert.equal(storage.data.get(PRE_WORLD_BACKUP_KEY),b);save(m,storage);assert.equal(storage.data.get(PRE_WORLD_KEY),a);assert.deepEqual(load(storage).state,m);}}
});
test('new outdoor and waterworks saves round-trip; unknown future worlds recover from backup',()=>{for(const scene of ['forest','liarsville','waterworks']){const s=oldState(scene);s.worldVersion=2;s.player={x:scenes[scene].safeSpawn[0],y:scenes[scene].safeSpawn[1],facing:'down'};const storage=store([]);assert.equal(save(s,storage),true);assert.deepEqual(load(storage).state,s);}const good=oldState(),future={...good,worldVersion:99};assert.equal(validateState(future),false);assert.throws(()=>migrateGridState(future),/Unsupported world/);assert.deepEqual(load(store([[SAVE_KEY,JSON.stringify(future)],[BACKUP_KEY,JSON.stringify(good)]])).state,good);});
