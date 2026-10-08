import test from "node:test";
import assert from "node:assert/strict";
import { createState, startMorning, rescue, manage, publish, tick, validateState, save, load, SAVE_KEY } from "../src/state.js";
import { TILE, scenes, buildings, getEntities, nearestEntity, isBlocked, safeGridPosition, transition } from "../src/world.js";
import { GRID_VERSION, migrateGridState } from "../src/grid-save.js";

const directions = [[0, -1], [-1, 0], [1, 0], [0, 1]];
function ready(scene = "bedroom", loan = false) {
  const state = createState("Ari", "girl", "Rowan");
  startMorning(state, loan);
  state.scene = scene;
  state.player = { x: scenes[scene].safeSpawn[0], y: scenes[scene].safeSpawn[1], facing: "down" };
  return state;
}
function reachable(state, start = state.player) {
  assert.equal(isBlocked(state.scene, start.x, start.y, state), false, `${state.scene}: invalid BFS start`);
  const queue = [[start.x, start.y]], seen = new Set([`${start.x},${start.y}`]);
  for (let index = 0; index < queue.length; index++) {
    const [x, y] = queue[index];
    for (const [dx, dy] of directions) {
      const nx = x + dx, ny = y + dy, key = `${nx},${ny}`;
      if (!seen.has(key) && !isBlocked(state.scene, nx, ny, state)) { seen.add(key); queue.push([nx, ny]); }
    }
  }
  return seen;
}
const requiredIds = {
  bedroom: ["tank", "sleep", "desk", "gecko", "stairs"],
  house: ["mom", "snail", "stairs", "exit"],
  yard: ["home", "gate", "isopods", "springtails", "forage", "apple-yard"],
  town: ["yard", "kaidHome", "rivalHome", "critz", "vet", "pharmacy", "bike", "glass", "nugget", "rival", "kaid", "route", "townSign", "spring", "apple-rootport"],
  forest: ["south","north","hollowLog","spillway","milepost","apple-mossway"],
  liarsville: ["south","waterworks","millHouse","cottage","seeds","townStory","apple-liarsville"],
  waterworks: ["exit","ledger","model","bell"],
  critz: ["shop-critz", "exit"], vet: ["shop-vet", "exit"], pharmacy: ["shop-pharmacy", "exit"],
  bike: ["shop-bike", "exit"], glass: ["shop-glass", "exit"], kaidHome: ["kaid", "exit"], rivalHome: ["rivalMom", "rivalDad", "exit"],
};

test("grid world preserves original scene IDs and adds the connected northern world and original interaction IDs", () => {
  assert.equal(TILE, 16);
  assert.deepEqual(Object.keys(scenes).sort(), Object.keys(requiredIds).sort());
  for (const [id, scene] of Object.entries(scenes)) {
    assert.deepEqual(scene.entities.map(entity => entity.id).sort(), requiredIds[id].sort(), id);
    for (const entity of scene.entities) {
      assert.ok(Number.isInteger(entity.x) && Number.isInteger(entity.y), `${id}/${entity.id}`);
      if (entity.type === "door") assert.ok(entity.spawn.every(Number.isInteger));
    }
    for (const object of scene.objects) {
      assert.equal(typeof object.sprite, "string");
      assert.ok([object.x, object.y, object.w, object.h].every(Number.isInteger));
      if (object.collision) assert.ok(object.collision.every(Number.isInteger));
    }
  }
});

test("every interaction is reachable from its safe spawn by cardinal steps, including NPC occupancy", () => {
  for (const id of Object.keys(scenes)) {
    const state = ready(id), cells = reachable(state);
    for (const entity of getEntities(state)) {
      const approaches = [[entity.x, entity.y], ...directions.map(([dx, dy]) => [entity.x + dx, entity.y + dy])];
      assert.ok(approaches.some(([x, y]) => cells.has(`${x},${y}`)), `${id}/${entity.id} has no reachable approach`);
      if (entity.type === "npc") assert.equal(cells.has(`${entity.x},${entity.y}`), false, `${id}/${entity.id} should occupy a cell`);
    }
    // No free cells are isolated behind new obstacles. This also makes every
    // migrated position in this map reconnect to the canonical spawn.
    const scene = scenes[id];
    for (let y = 0; y < scene.h; y++) for (let x = 0; x < scene.w; x++)
      if (!isBlocked(id, x, y, state)) assert.ok(cells.has(`${x},${y}`), `${id}: stranded cell ${x},${y}`);
  }
});

test("every entrance and exit returns to its origin scene with a reachable safe spawn", () => {
  let tested = 0;
  for (const [id, scene] of Object.entries(scenes)) for (const exit of scene.entities.filter(entity => entity.type === "door")) {
    const state = ready(id);
    transition(state, exit);
    assert.equal(state.scene, exit.to);
    assert.ok(Number.isInteger(state.player.x) && Number.isInteger(state.player.y));
    assert.equal(isBlocked(state.scene, state.player.x, state.player.y, state), false);
    const cells = reachable(state);
    const returnDoor = getEntities(state).find(entity => entity.type === "door" && entity.to === id);
    assert.ok(returnDoor, `${id} → ${exit.to}: no return door`);
    assert.ok([[returnDoor.x, returnDoor.y], ...directions.map(([dx,dy]) => [returnDoor.x+dx,returnDoor.y+dy])].some(([x,y]) => cells.has(`${x},${y}`)));
    transition(state, returnDoor);
    assert.equal(state.scene, id);
    assert.equal(isBlocked(id, state.player.x, state.player.y, state), false);
    tested++;
  }
  assert.equal(tested, 26);
  for (const building of buildings) {
    const threshold = scenes.town.entities.find(entity => entity.id === building.scene);
    assert.equal(threshold.x, building.doorX);
    assert.equal(threshold.y, building.doorY);
    assert.equal(isBlocked("town", threshold.x, threshold.y), false);
    const state = ready(building.scene);
    const exit = scenes[building.scene].entities.find(entity => entity.type === "door" && entity.to === "town");
    transition(state, exit);
    assert.deepEqual([state.player.x, state.player.y], [threshold.x, threshold.y + 1]);
  }
});

test("explicit footprints block every occupied cell and reject fractional movement without deriving collision from art", () => {
  for (const [id, scene] of Object.entries(scenes)) {
    for (const object of [...scene.objects, ...(id === "town" ? buildings : [])]) {
      if (!object.collision) continue;
      const [left, top, width, height] = object.collision;
      for (let y = top; y < top + height; y++) for (let x = left; x < left + width; x++)
        assert.equal(isBlocked(id, x, y), true, `${id}/${object.kind || object.scene} leaks at ${x},${y}`);
    }
    const [x,y] = scene.safeSpawn;
    assert.equal(isBlocked(id,x+0.5,y),true);
    assert.equal(isBlocked(id,x,y+0.5),true);
    assert.equal(isBlocked(id,0,y),true);
    assert.equal(isBlocked(id,scene.w,y),true);
    assert.equal(isBlocked(id,x,scene.h),true);
    assert.equal(isBlocked(id,NaN,y),true);
  }
  const leaves = scenes.yard.map.decals.find(object => object.id === "leaves.litter");
  assert.equal(isBlocked("yard",leaves.x,leaves.y),false);
  const tree = scenes.town.objects.find(object => object.kind === "tree");
  assert.equal(isBlocked("town",tree.x,tree.y),false, "canopy is not the trunk footprint");
  const mom = scenes.house.entities.find(entity => entity.id === "mom");
  assert.equal(isBlocked("house",mom.x,mom.y),false);
  assert.equal(isBlocked("house",mom.x,mom.y,ready("house")),true);
});

test("cardinal interaction cannot reach through a diagonal furniture corner and retains story filtering", () => {
  const state = ready();
  state.player = { x: 9, y: 6, facing: "up" };
  assert.equal(nearestEntity(state),null);
  state.player = { x: 8, y: 6, facing: "up" };
  assert.equal(nearestEntity(state).id,"tank");
  state.stage="night";
  assert.deepEqual(getEntities(state).map(entity=>entity.id),["tank","sleep","desk"]);
  assert.equal(nearestEntity(state).name,"Feed Pebble the gecko");
  state.stage="morning";
  state.flags.rescued=["gecko"];
  assert.equal(getEntities(state).some(entity=>entity.id==="gecko"),false);
  state.scene="town";
  assert.equal(getEntities(state).find(entity=>entity.id==="rival").name,"Rowan");
});

test("safe-grid recovery deterministically selects the closest connected walkable cell", () => {
  for (const id of Object.keys(scenes)) {
    const state = ready(id), cells = [...reachable(state)].map(key=>key.split(",").map(Number));
    for (const [x,y] of [[7.6,5.4],[3.5,6.5],[0,0],[31.9,26.9],[8,5],[8,9.5]]) {
      const result=safeGridPosition(id,x,y,state);
      const squared=(result.x-x)**2+(result.y-y)**2;
      assert.equal(isBlocked(id,result.x,result.y,state),false);
      assert.ok(cells.every(([cx,cy])=>squared <= (cx-x)**2+(cy-y)**2),id);
      assert.deepEqual(safeGridPosition(id,x,y,state),result);
    }
    assert.deepEqual(safeGridPosition(id,NaN,undefined,state),{x:scenes[id].safeSpawn[0],y:scenes[id].safeSpawn[1]});
  }
  assert.throws(()=>safeGridPosition("missing",1,1),/Unknown scene/);
});

function progressFixture(scene,loan) {
  const state=ready(scene,loan);
  for (const id of ["gecko","snail","isopods","springtails"]) rescue(state,id);
  manage(state,"moss"); manage(state,"ventilation",3);
  publish(state,{kind:"photo",frame:55,zoom:1.2}); tick(state,2);
  state.flags.notebook=true;
  state.flags.supplyGift=true;
  state.inventory.medicine=1;
  state.inventory.filter=1;
  state.savedAt="2026-09-26T12:00:00.000Z";
  state.player={x:scene==="town"?24.4:7.6,y:scene==="town"?8.8:5.4,facing:"left",customPositionMetadata:"retained"};
  delete state.gridVersion; // createState now defaults to grid v1; this fixture is a legacy save.
  return state;
}
function withoutPosition(state) {
  const copy=structuredClone(state);
  delete copy.gridVersion;
  delete copy.worldVersion;
  delete copy.player.x;
  delete copy.player.y;
  return copy;
}
test("legacy fractional saves migrate in all scenes and both loan paths without changing any nonposition progress", () => {
  for(const scene of Object.keys(scenes)) for(const loan of [false,true]) {
    const original=progressFixture(scene,loan);
    assert.equal(validateState(original),true);
    const bytes=JSON.stringify(original);
    const migrated=migrateGridState(original);
    assert.equal(JSON.stringify(original),bytes,"input/raw recoverable save changed");
    assert.notEqual(migrated,original);
    assert.notEqual(migrated.tank,original.tank,"clone aliases original progress");
    assert.equal(migrated.gridVersion,GRID_VERSION);
    assert.equal(validateState(migrated),true);
    assert.equal(isBlocked(scene,migrated.player.x,migrated.player.y,migrated),false);
    assert.deepEqual(withoutPosition(migrated),withoutPosition(original));
    assert.deepEqual(migrateGridState(migrated),migrated,"migration not idempotent");
    const entries=new Map([[SAVE_KEY,bytes]]);
    const storage={getItem:key=>entries.get(key)||null,setItem:(key,value)=>entries.set(key,value)};
    assert.equal(save(migrated,storage),true);
    assert.deepEqual(load(storage).state,migrated,"migrated v1 save did not round-trip");
    assert.equal(JSON.stringify(original),bytes);
  }
});

test("partial night opening migrates without skipping beats; unsupported grid versions fail without mutating source", () => {
  for(const beat of [undefined,"feeding","broken","kaid"]) {
    const state=createState("Ari","boy","Rowan");
    delete state.gridVersion;
    state.player={x:7.6,y:5.4,facing:"up"};
    if(beat)state.storyBeat=beat;
    const original=structuredClone(state),migrated=migrateGridState(state);
    assert.deepEqual(state,original);
    assert.deepEqual(withoutPosition(migrated),withoutPosition(state));
    assert.equal(migrated.stage,"night");
    assert.equal(migrated.tankOwned,false);
    assert.equal(migrated.flags.loanDecided,false);
    assert.equal(migrated.money,1200);
  }
  const future=ready();future.gridVersion=999;
  const original=structuredClone(future);
  assert.throws(()=>migrateGridState(future),/Unsupported grid version/);
  assert.deepEqual(future,original);
});
