import test from "node:test";
import assert from "node:assert/strict";
import { createState, startMorning, rescue, publish, tick, save, load, validateState, SAVE_KEY, BACKUP_KEY, PRE_GRID_KEY, PRE_GRID_BACKUP_KEY } from "../src/state.js";
import { migrateGridState } from "../src/grid-save.js";

// In-memory fixtures only. No browser or system storage is read by these tests.
function syntheticStorage(entries = [], { failGet, failSet } = {}) {
  const data = new Map(entries), writes = [];
  return { data, writes,
    getItem(key) { if (failGet?.(key)) throw Error("Synthetic read failure"); return data.get(key) ?? null; },
    setItem(key, value) { writes.push([key,value]); if (failSet?.(key)) throw Error("Synthetic write failure"); data.set(key,value); },
  };
}
function legacy(loan = false) {
  const state = createState("Ari", "girl", "Rowan");
  startMorning(state,loan);
  rescue(state,"isopods");rescue(state,"springtails");
  publish(state,{kind:"photo",frame:55,zoom:1.2});tick(state,2);
  state.inventory.medicine=1;
  state.flags.notebook=true;
  state.player={x:7.6,y:5.4,facing:"up"};
  state.savedAt="2026-09-26T12:00:00.000Z";
  delete state.gridVersion;
  return state;
}
// Deliberate whitespace, tabs, CRLF and Unicode prove byte preservation rather
// than JSON parse/reserialize equivalence.
const raw = state => "\t \r\n" + JSON.stringify(state,null,"\t").replaceAll("\n","\r\n") + "\r\n ";

test("first grid save archives both legacy slots byte-for-byte before overwrite; later saves keep archives immutable", () => {
  const primary=legacy(true), backup=legacy(false), primaryBytes=raw(primary), backupBytes=raw(backup);
  const storage=syntheticStorage([[SAVE_KEY,primaryBytes],[BACKUP_KEY,backupBytes]]);
  const migrated=migrateGridState(load(storage).state);
  assert.equal(save(migrated,storage),true);
  assert.equal(storage.data.get(PRE_GRID_KEY),primaryBytes);
  assert.equal(storage.data.get(PRE_GRID_BACKUP_KEY),backupBytes);
  assert.deepEqual(storage.writes.map(([key])=>key),[PRE_GRID_KEY,PRE_GRID_BACKUP_KEY,BACKUP_KEY,SAVE_KEY]);
  assert.deepEqual(load(storage).state,migrated);
  for(let i=0;i<3;i++){tick(migrated);assert.equal(save(migrated,storage),true);}
  assert.equal(storage.data.get(PRE_GRID_KEY),primaryBytes);
  assert.equal(storage.data.get(PRE_GRID_BACKUP_KEY),backupBytes);
  assert.equal(storage.writes.filter(([key])=>key===PRE_GRID_KEY).length,1);
  assert.equal(storage.writes.filter(([key])=>key===PRE_GRID_BACKUP_KEY).length,1);
  assert.deepEqual(JSON.parse(storage.data.get(PRE_GRID_KEY)),primary);
  assert.deepEqual(JSON.parse(storage.data.get(PRE_GRID_BACKUP_KEY)),backup);
});

test("failure of either archive write aborts before either original normal slot changes", () => {
  for(const failedKey of [PRE_GRID_KEY,PRE_GRID_BACKUP_KEY]) {
    const primaryBytes=raw(legacy(true)), backupBytes=raw(legacy(false));
    const storage=syntheticStorage([[SAVE_KEY,primaryBytes],[BACKUP_KEY,backupBytes]],{failSet:key=>key===failedKey});
    const migrated=migrateGridState(JSON.parse(primaryBytes)), before=structuredClone(migrated);
    assert.equal(save(migrated,storage),false,failedKey);
    assert.equal(storage.data.get(SAVE_KEY),primaryBytes);
    assert.equal(storage.data.get(BACKUP_KEY),backupBytes);
    assert.equal(storage.writes.some(([key])=>key===SAVE_KEY||key===BACKUP_KEY),false);
    assert.deepEqual(migrated,before,"failed archival must not mark the in-memory state saved");
  }
});

test("normal backup failure aborts the primary write and leaves the in-memory savedAt unchanged", () => {
  const previous=migrateGridState(legacy()), previousBytes=raw(previous), oldBackupBytes=raw(legacy(true));
  const storage=syntheticStorage([[SAVE_KEY,previousBytes],[BACKUP_KEY,oldBackupBytes]],{failSet:key=>key===BACKUP_KEY});
  const next=structuredClone(previous);tick(next);const before=structuredClone(next);
  assert.equal(save(next,storage),false);
  assert.equal(storage.data.get(SAVE_KEY),previousBytes);
  assert.equal(storage.data.get(BACKUP_KEY),oldBackupBytes);
  assert.equal(storage.writes.some(([key])=>key===SAVE_KEY),false);
  assert.deepEqual(next,before);
});

test("failed primary write retains original primary and both archived legacy saves without advancing savedAt", () => {
  const primaryBytes=raw(legacy(true)),backupBytes=raw(legacy(false));
  const storage=syntheticStorage([[SAVE_KEY,primaryBytes],[BACKUP_KEY,backupBytes]],{failSet:key=>key===SAVE_KEY});
  const migrated=migrateGridState(JSON.parse(primaryBytes)),before=structuredClone(migrated);
  assert.equal(save(migrated,storage),false);
  assert.equal(storage.data.get(SAVE_KEY),primaryBytes);
  assert.equal(storage.data.get(PRE_GRID_KEY),primaryBytes);
  assert.equal(storage.data.get(PRE_GRID_BACKUP_KEY),backupBytes);
  assert.deepEqual(migrated,before);
  assert.deepEqual(load(storage).state,JSON.parse(primaryBytes));
});

test("a valid legacy backup remains recoverable when primary is corrupt before migration", () => {
  const backupBytes=raw(legacy(true));
  const storage=syntheticStorage([[SAVE_KEY,"{damaged"],[BACKUP_KEY,backupBytes]]);
  const recovered=load(storage);
  assert.equal(recovered.recovered,true);
  const migrated=migrateGridState(recovered.state);
  assert.equal(save(migrated,storage),true);
  assert.equal(storage.data.get(PRE_GRID_BACKUP_KEY),backupBytes);
  assert.equal(storage.data.get(BACKUP_KEY),backupBytes,"malformed primary replaced valid backup");
  assert.equal(storage.data.has(PRE_GRID_KEY),false);
  assert.deepEqual(load(storage).state,migrated);
});

test("load falls back through normal backup, original primary archive and original backup archive", () => {
  const good=legacy(true),bytes=raw(good);
  const keys=[SAVE_KEY,BACKUP_KEY,PRE_GRID_KEY,PRE_GRID_BACKUP_KEY];
  for(let index=0;index<keys.length;index++) {
    const entries=keys.map((key,i)=>[key,i===index?bytes:"{broken"]);
    const storage=syntheticStorage(entries),result=load(storage);
    assert.deepEqual(result.state,good,keys[index]);
    assert.equal(result.recovered,index>0);
    assert.equal(storage.writes.length,0,"load may not mutate recovery slots");
  }
  const damaged=load(syntheticStorage(keys.map(key=>[key,"{broken"])));
  assert.equal(damaged.state,null);
  assert.equal(damaged.damaged,true);
});

test("storage read failure does not prevent loading an independently available backup", () => {
  const bytes=raw(legacy());
  const storage=syntheticStorage([[BACKUP_KEY,bytes]],{failGet:key=>key===SAVE_KEY});
  const result=load(storage);
  assert.equal(result.recovered,true);
  assert.deepEqual(result.state,JSON.parse(bytes));
  const state=migrateGridState(JSON.parse(bytes)),before=structuredClone(state);
  assert.equal(save(state,storage),false);
  assert.equal(storage.writes.length,0);
  assert.deepEqual(state,before);
});

test("supported primary wins over old archives; occupied archive bytes are never overwritten", () => {
  const state=migrateGridState(legacy(true)),oldPrimary=raw(legacy(false)),oldBackup=raw(legacy(true));
  tick(state,2);
  const storage=syntheticStorage([[SAVE_KEY,raw(state)],[PRE_GRID_KEY,oldPrimary],[PRE_GRID_BACKUP_KEY,oldBackup]]);
  assert.deepEqual(load(storage).state,state);
  // Even a manually restored legacy primary cannot replace the original
  // immutable archive; ordinary backup retains that restored primary instead.
  const restored=legacy(false),restoredBytes=raw(restored);
  storage.data.set(SAVE_KEY,restoredBytes);
  assert.equal(save(migrateGridState(restored),storage),true);
  assert.equal(storage.data.get(PRE_GRID_KEY),oldPrimary);
  assert.equal(storage.data.get(PRE_GRID_BACKUP_KEY),oldBackup);
  assert.equal(storage.data.get(BACKUP_KEY),restoredBytes);
});

test("unsupported grid markers are rejected so a good backup loads instead of migration crashing", () => {
  const good=legacy(true),future=migrateGridState(good);future.gridVersion=999;
  assert.equal(validateState(good),true);
  assert.equal(validateState(future),false);
  const storage=syntheticStorage([[SAVE_KEY,raw(future)],[BACKUP_KEY,raw(good)]]);
  const result=load(storage);
  assert.equal(result.recovered,true);
  assert.deepEqual(result.state,good);
  assert.doesNotThrow(()=>migrateGridState(result.state));
  assert.equal(save(future,storage),false);
  assert.equal(storage.writes.length,0);
});

test("invalid state cannot write any slot and a fresh grid game does not create legacy archives", () => {
  const storage=syntheticStorage(),state=createState("Ari","girl","Rowan");
  const invalid=structuredClone(state);invalid.money=-1;
  assert.equal(save(invalid,storage),false);
  assert.equal(storage.writes.length,0);
  assert.equal(save(state,storage),true);
  assert.equal(storage.data.has(PRE_GRID_KEY),false);
  assert.equal(storage.data.has(PRE_GRID_BACKUP_KEY),false);
  assert.equal(storage.data.has(BACKUP_KEY),false);
  assert.deepEqual(load(storage).state,state);
});
