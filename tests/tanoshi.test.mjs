import test from 'node:test';
import assert from 'node:assert/strict';
import {createState,startMorning,save,load,validateState,SAVE_KEY,BACKUP_KEY} from '../src/state.js';
import {TANOSHI,discoverTanoshi,foundTanoshi} from '../src/tanoshi.js';
import {scenes,getEntities,isBlocked,nearestEntity,canStep} from '../src/world.js';
const storage=()=>{const data=new Map();return {getItem:k=>data.get(k)||null,setItem:(k,v)=>data.set(k,v),data};};
test('Tanoshi greetings are exactly once, durable, and do not affect protected progress',()=>{
  for(const loan of [false,true]){
    const state=createState('Ari','girl','River');startMorning(state,loan);
    const before=structuredClone(state);
    for(const t of TANOSHI){state.scene=t.scene;state.player={x:t.x+1,y:t.y,facing:'left'};assert.equal(discoverTanoshi(state,t.id).first,true);assert.equal(discoverTanoshi(state,t.id).first,false);}
    assert.equal(foundTanoshi(state).length,TANOSHI.length);
    for(const key of ['hero','gender','rival','money','debt','flags','inventory','tank','posts','notebookEntries'])assert.deepEqual(state[key],before[key],key);
    const store=storage();assert.ok(save(state,store));assert.deepEqual(load(store).state.tanoshiDiscoveries,TANOSHI.map(t=>t.id));
  }
});
test('Missing optional field retains legacy saves and exact backup bytes',()=>{
  const old=createState();delete old.gridVersion;delete old.worldVersion;
  const bytes=JSON.stringify(old),store=storage();store.setItem(SAVE_KEY,bytes);
  const state=load(store).state;assert.deepEqual(state,old);assert.ok(validateState(state));assert.equal(foundTanoshi(state).length,0);
  state.scene='bedroom';state.player={x:6,y:6,facing:'left'};assert.ok(discoverTanoshi(state,'tanoshi-blush').first);assert.ok(save(state,store));assert.equal(store.getItem(BACKUP_KEY),bytes);
  assert.equal(load(store).state.hero,old.hero);
});
test('Tanoshi never block old cells, entrances, rescues or the opening tank action',()=>{
  const state=createState();assert.equal(nearestEntity(state).id,'tank');
  assert.ok(getEntities(state).some(e=>e.id==='tanoshi-blush'));
  for(const t of TANOSHI){state.scene=t.scene;assert.equal(isBlocked(t.scene,t.x,t.y,state),false);
    const queue=[scenes[t.scene].safeSpawn],seen=new Set(queue.map(p=>p.join(',')));
    for(let n=0;n<queue.length;n++){const [x,y]=queue[n];state.player={x,y,facing:'down'};for(const [dx,dy]of [[0,-1],[1,0],[0,1],[-1,0]]){const a=x+dx,b=y+dy,k=[a,b].join(',');if(!seen.has(k)&&canStep(state,a,b)){seen.add(k);queue.push([a,b]);}}}
    assert.ok(seen.has([t.x,t.y].join(',')),t.id+' is unreachable');
  }
});
test('Greeting rejects distant, wrong-scene and unknown encounters; malformed saves cannot overwrite good progress',()=>{
  const state=createState();assert.equal(discoverTanoshi(state,'tanoshi-mint'),null);assert.equal(discoverTanoshi(state,'tanoshi-blush'),null);assert.equal(discoverTanoshi(state,'unknown'),null);
  const store=storage();assert.ok(save(state,store));const old=store.getItem(SAVE_KEY);
  for(const bad of [null,{},['unknown'],['tanoshi-blush','tanoshi-blush']]){state.tanoshiDiscoveries=bad;assert.equal(validateState(state),false);assert.equal(save(state,store),false);assert.equal(store.getItem(SAVE_KEY),old);}
});
