import test from "node:test";
import assert from "node:assert/strict";
import {
  createState,
  startMorning,
  rescue,
  manage,
  tick,
  scorePost,
  publish,
  save,
  load,
  validateState,
  spend,
  SAVE_KEY,
  BACKUP_KEY,
} from "../src/state.js";
import {
  scenes,
  getEntities,
  isBlocked,
  transition,
  movePlayer,
} from "../src/world.js";
const ready = (loan = false) => {
  const s = createState("Ari", "girl", "Rowan");
  startMorning(s, loan);
  return s;
};
test("both loan branches give the 25-gallon gift; re-entry cannot duplicate money", () => {
  const a = ready(true),
    b = ready(false);
  assert.equal(a.money, 11200);
  assert.equal(a.debt, 10000);
  assert.equal(b.money, 1200);
  assert.equal(b.debt, 0);
  for (const s of [a, b]) {
    assert.equal(s.tank.gallons, 25);
    assert.equal(s.tankOwned, true);
    assert.equal(s.stage, "morning");
    assert.equal(validateState(s), true);
    assert.equal(isBlocked(s.scene, s.player.x, s.player.y), false);
  }
  startMorning(a, true);
  assert.equal(a.money, 11200);
});
test("all four rescues are safe, idempotent, and only compatible species enter the starter", () => {
  const s = ready();
  for (const id of ["gecko", "snail", "isopods", "springtails"]) {
    assert.equal(rescue(s, id), true);
    assert.equal(rescue(s, id), false);
  }
  assert.equal(s.flags.rescued.length, 4);
  assert.equal(s.tank.isopods, 6);
  assert.equal(s.tank.springtails, 12);
  assert.equal(s.tank.deaths, 0);
});
test("care has measurable causal effects and simulation is deterministic", () => {
  const a = ready(),
    b = ready();
  rescue(a, "isopods");
  rescue(b, "isopods");
  manage(a, "moss");
  manage(a, "ventilation", 3);
  manage(a, "light", 12);
  manage(b, "light", 4);
  tick(a, 6);
  tick(b, 6);
  assert.ok(a.tank.moisture < b.tank.moisture);
  assert.ok(a.tank.algae > b.tank.algae);
  assert.ok(a.tank.nutrients < b.tank.nutrients);
  const c = structuredClone(a),
    d = structuredClone(a);
  tick(c, 18);
  for (let i = 0; i < 18; i++) tick(d);
  assert.deepEqual(c, d);
});
test("good conditions permit births; dry or starved tanks pause breeding without deaths", () => {
  const s = ready();
  rescue(s, "isopods");
  rescue(s, "springtails");
  manage(s, "moss");
  tick(s, 6);
  assert.ok(s.tank.births > 0);
  const pop = s.tank.isopods + s.tank.springtails;
  tick(s, 48);
  assert.equal(s.tank.deaths, 0);
  assert.ok(s.tank.isopods + s.tank.springtails >= pop);
  assert.ok(s.tank.events.some((e) => e.includes("paused")));
});
test("care inventory and purchases cannot go negative", () => {
  const s = ready();
  assert.equal(spend(s, 1300), false);
  assert.equal(spend(s, -100), false);
  assert.equal(spend(s, 300), true);
  assert.equal(s.money, 900);
  assert.ok(manage(s, "moss").ok);
  assert.equal(manage(s, "moss").ok, false);
  assert.equal(s.inventory.moss, 0);
  assert.equal(manage(s, "light", 99).ok, false);
  for (let i = 0; i < 4; i++) manage(s, "feed");
  assert.equal(manage(s, "feed").ok, false);
});
test("Critter framing and fresh interest affect reach; revenue settles exactly once", () => {
  const s = ready();
  rescue(s, "isopods");
  rescue(s, "springtails");
  const good = { kind: "photo", frame: 55, zoom: 1.2 };
  assert.ok(
    scorePost(s, good).total > scorePost(s, { frame: 0, zoom: 1.6 }).total,
  );
  const original = s.money,
    p = publish(s, good);
  assert.ok(p.views > 0);
  assert.ok(s.money > original);
  assert.equal(scorePost(s, good).interest, 30);
  tick(s, 4);
  assert.equal(p.views, p.targetViews);
  assert.equal(s.money - original, p.revenue);
  const money = s.money;
  tick(s, 10);
  assert.equal(s.money, money);
  assert.equal(scorePost(s, good).interest, 85);
});
test("saving round-trips progression and restores a known good backup after corruption", () => {
  const m = new Map(),
    storage = {
      getItem: (k) => m.get(k) || null,
      setItem: (k, v) => m.set(k, v),
    };
  const s = ready(true);
  rescue(s, "isopods");
  publish(s, { kind: "photo", frame: 50, zoom: 1 });
  assert.ok(save(s, storage));
  assert.deepEqual(load(storage).state, s);
  tick(s);
  assert.ok(save(s, storage));
  assert.ok(m.has(BACKUP_KEY));
  m.set(SAVE_KEY, "{broken");
  assert.equal(load(storage).recovered, true);
  assert.ok(load(storage).state);
  assert.equal(
    save(s, {
      getItem() {
        throw Error("denied");
      },
    }),
    false,
  );
});
test("malformed saves and invalid numeric state are rejected, not executed", () => {
  for (const mutate of [
    (s) => (s.money = -1),
    (s) => (s.tank.moisture = NaN),
    (s) => (s.tank.isopods = null),
    (s) => (s.scene = "unknown"),
    (s) => (s.flags.rescued = ["fake"]),
    (s) => (s.version = 999),
    (s) => (s.posts = [{}]),
  ]) {
    const s = ready();
    mutate(s);
    assert.equal(validateState(s), false);
  }
});
test("scene exits return to valid positions; every interaction has a reachable approach", () => {
  for (const [id, scene] of Object.entries(scenes)) {
    const s = ready();
    s.scene = id;
    s.player = { x: 8, y: 9.5, facing: "down" };
    for (const e of getEntities(s)) {
      const approach = [];
      for (let y = 0.75; y < scene.h; y += 0.25)
        for (let x = 0.75; x < scene.w; x += 0.25)
          if (!isBlocked(id, x, y) && Math.hypot(e.x - x, e.y - y) < 1.6)
            approach.push([x, y]);
      assert.ok(approach.length, `${id}/${e.id} cannot be approached`);
      if (e.type === "door") {
        const clone = structuredClone(s);
        transition(clone, e);
        assert.equal(
          isBlocked(clone.scene, clone.player.x, clone.player.y),
          false,
          `${id} → ${e.to} blocked spawn`,
        );
      }
    }
  }
});
test("movement respects collision, normalizes diagonal speed, and supports running", () => {
  const a = ready(),
    b = ready(),
    c = ready();
  for (const s of [a, b, c]) s.player = { x: 8, y: 8, facing: "down" };
  movePlayer(a, 1, 0, 0.1);
  movePlayer(b, 1, 1, 0.1);
  movePlayer(c, 1, 0, 0.1, true);
  assert.ok(
    Math.abs(Math.hypot(b.player.x - 8, b.player.y - 8) - (a.player.x - 8)) <
      1e-8,
  );
  assert.ok(c.player.x > a.player.x);
  a.player = { x: 0.81, y: 8, facing: "left" };
  movePlayer(a, -1, 0, 0.1);
  assert.equal(a.player.x, 0.81);
});
