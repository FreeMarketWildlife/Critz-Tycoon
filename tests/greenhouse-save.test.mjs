import test from 'node:test';import assert from 'node:assert/strict';
import {createState,startMorning,validateState,save,load,SAVE_KEY} from '../src/state.js';
import {initialState,pay,chooseTub,collect} from '../art-review/greenhouse-state.js';
test('optional greenhouse collection preserves v1 saves and rejects corrupt new data',()=>{
 const s=createState('Ari','girl','River');startMorning(s,true);assert.equal(validateState(s),true);
 s.lukeGreenhouse=collect(chooseTub(pay(initialState(),11),1),0);assert.equal(validateState(s),true);
 const bytes=new Map(),storage={getItem:k=>bytes.get(k)||null,setItem:(k,v)=>bytes.set(k,v)};
 assert.equal(save(s,storage),true);assert.deepEqual(load(storage).state.lukeGreenhouse,s.lukeGreenhouse);assert.ok(bytes.has(SAVE_KEY));
 const damaged=structuredClone(s);damaged.lukeGreenhouse.collection[0].kind=99;assert.equal(validateState(damaged),false);
});
