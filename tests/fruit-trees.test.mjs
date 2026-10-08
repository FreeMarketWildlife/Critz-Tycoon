import test from 'node:test';
import assert from 'node:assert/strict';
import {FRUIT_TREES,fruitCells,fruitStatus,harvestFruit,cueFruitShake,fruitTreeView} from '../src/fruit-trees.js';
import {createState,startMorning,validateState,save,load,tick} from '../src/state.js';
import {scenes,isBlocked,nearestEntity} from '../src/world.js';
import {migrateGridState} from '../src/grid-save.js';
function ready(tree=FRUIT_TREES[0]){const s=createState('Ari','boy','River');startMorning(s,true);s.scene=tree.scene;s.player={x:tree.x,y:tree.y+2,facing:'up'};return s;}
const storage=()=>{const m=new Map();return {getItem:k=>m.get(k)||null,setItem:(k,v)=>m.set(k,v)};};
test('all four fruit trees keep their rooted footprint and have reachable interaction cells',()=>{
 for(const tree of FRUIT_TREES){const s=ready(tree),o=scenes[tree.scene].objects.find(o=>o.fruitId===tree.id);assert.deepEqual(o.collision,[tree.x,tree.y+1,2,1]);
  const candidates=fruitCells(tree).flatMap(([x,y])=>[[x-1,y],[x+1,y],[x,y-1],[x,y+1]]).filter(([x,y])=>!isBlocked(tree.scene,x,y));assert.ok(candidates.length);
  for(const [x,y]of candidates){s.player={x,y,facing:y>tree.y+1?'up':y<tree.y+1?'down':x<tree.x?'right':'left'};assert.equal(nearestEntity(s).id,tree.id);}
 }
});
test('harvest gives exactly three apples once per tree per 24 saved habitat hours',()=>{
 const s=ready(),tree=FRUIT_TREES[0],before=structuredClone(s);assert.deepEqual(harvestFruit(s,tree.id),{ok:true,count:3});assert.equal(s.inventory.apples,3);assert.equal(s.fruitHarvests[tree.id],8);
 assert.equal(harvestFruit(s,tree.id).reason,'growing');s.time=31.99;assert.equal(fruitStatus(s,tree.id).ripe,false);s.time=32;assert.equal(fruitStatus(s,tree.id).ripe,true);assert.equal(harvestFruit(s,tree.id).ok,true);assert.equal(s.inventory.apples,6);
 for(const k of ['money','debt','tank','flags','posts'])assert.deepEqual(s[k],before[k]);
 const t=FRUIT_TREES[1];s.scene=t.scene;s.player={x:t.x,y:t.y+2,facing:'up'};assert.equal(harvestFruit(s,t.id).ok,true);assert.equal(s.inventory.apples,9);
});
test('distant, diagonal, wrong-scene, night and full-bag attempts award nothing',()=>{
 const tree=FRUIT_TREES[0];for(const mutate of [s=>s.scene='house',s=>s.stage='night',s=>s.player.x-=1,s=>s.player.y+=1,s=>s.inventory.apples=9998]){const s=ready();mutate(s);const before=structuredClone(s);assert.equal(harvestFruit(s,tree.id).ok,false);assert.deepEqual(s,before);}
});
test('legacy saves without orchard fields stay valid and byte-shaped until first harvest',()=>{
 const s=ready();delete s.inventory.apples;delete s.fruitHarvests;const before=structuredClone(s),store=storage();assert.equal(validateState(s),true);assert.equal(save(s,store),true);const loaded=load(store).state;assert.deepEqual(loaded.inventory,before.inventory);assert.equal(loaded.fruitHarvests,undefined);assert.deepEqual(migrateGridState(loaded),loaded);
 assert.equal(harvestFruit(loaded,FRUIT_TREES[0].id).ok,true);assert.equal(save(loaded,store),true);const again=load(store).state;assert.equal(again.inventory.apples,3);assert.equal(fruitStatus(again,FRUIT_TREES[0].id).ripe,false);assert.equal(harvestFruit(again,FRUIT_TREES[0].id).reason,'growing');assert.equal(again.money,11200);assert.equal(again.debt,10000);assert.equal(again.tank.gallons,25);
});
test('optional orchard fields reject corrupt quantities, timestamps and unknown tree IDs',()=>{
 for(const apples of [-1,1.5,10001,NaN]){const s=ready();s.inventory.apples=apples;assert.equal(validateState(s),false);}
 for(const h of [null,[],{missing:8},{'apple-yard':9},{'apple-yard':-1},{'apple-yard':Infinity}]){const s=ready();s.fruitHarvests=h;assert.equal(validateState(s),false);}
});
test('shake is transient, integer-pixel, scene-local and reduced by Calm',()=>{
 const s=ready(),before=structuredClone(s),id=FRUIT_TREES[0].id;cueFruitShake(s,id,10,true);assert.equal(fruitTreeView(s,id,10.1).shake,-2);assert.equal(fruitTreeView(s,id,10.3).falling,true);assert.equal(fruitTreeView(s,id,11.1).active,false);assert.deepEqual(s,before);
 cueFruitShake(s,id,12,true,true);assert.equal(fruitTreeView(s,id,12.1).shake,0);assert.equal(fruitTreeView(s,id,12.1).falling,false);s.scene='town';assert.equal(fruitTreeView(s,id,12.1).active,false);
});

test('actual habitat ticks regrow fruit; opening-night time cannot regrow it',()=>{
 const s=ready(),id=FRUIT_TREES[0].id;harvestFruit(s,id);tick(s,23);assert.equal(fruitStatus(s,id).ripe,false);tick(s);assert.equal(fruitStatus(s,id).ripe,true);
 s.stage='night';const time=s.time;tick(s,24);assert.equal(s.time,time);
});
