import test from "node:test";
import assert from "node:assert/strict";
import {
  TICK_SECONDS,
  createMotion,
  advanceMotion,
  getMotionView,
  createMotionClock,
  advanceMotionClock,
  resetMotionClock,
} from "../src/movement.js";

const held = (...directions) => new Set(directions);
const open = () => true;
const make = (facing = "right") => createMotion({ x: 4, y: 5, facing });
const step = (motion, directions = held("right"), run = false, enter = open, opts) =>
  advanceMotion(motion, directions, run, enter, opts);
const repeat = (count, fn) => Array.from({ length: count }, (_, i) => fn(i));

test("walks exactly 16 integer pixels in 16 ticks and commits one tile atomically", () => {
  for (const [direction, dx, dy] of [
    ["up", 0, -1], ["down", 0, 1], ["left", -1, 0], ["right", 1, 0],
  ]) {
    const player = { x: 4, y: 5, facing: direction };
    const motion = createMotion(player);
    assert.equal(motion.player, player);
    let collisionCalls = 0;
    for (let tick = 1; tick <= 16; tick++) {
      const view = step(motion, held(direction), false, (x, y) => {
        collisionCalls++;
        assert.deepEqual([x, y], [4 + dx, 5 + dy]);
        return true;
      });
      assert.deepEqual([view.x, view.y], [64 + dx * tick, 80 + dy * tick]);
      assert.deepEqual([player.x, player.y], tick === 16 ? [4 + dx, 5 + dy] : [4, 5]);
      assert.equal(view.settled, tick === 16);
      assert.equal(view.moving, true);
    }
    assert.equal(collisionCalls, 1, "committed destination is checked once");
    assert.equal(step(motion, held()).moving, false);
  }
});

test("normal running uses 2px per tick and honors run permission", () => {
  const motion = make();
  for (let tick = 1; tick <= 8; tick++) {
    const view = step(motion, held("right"), true);
    assert.equal(view.x, 64 + tick * 2);
    assert.equal(view.action, "run");
  }
  assert.equal(motion.player.x, 5);
  const denied = step(make(), held("right"), true, open, { runAllowed: false, board: true });
  assert.equal(denied.action, "walk");
  assert.equal(denied.x, 65);
});

test("a rest tap turns for eight ticks without displacement; holding then walks", () => {
  const tap = make("down");
  const frames = [step(tap, held("right"))];
  frames.push(...repeat(7, () => step(tap, held())));
  assert.deepEqual(frames.map(f => f.pose), ["strideA", "strideA", "strideA", "strideA", "idle", "idle", "idle", "idle"]);
  for (const view of frames) {
    assert.deepEqual([view.x, view.y], [64, 80]);
    assert.equal(view.action, "turn");
    assert.equal(view.facing, "right");
  }
  assert.equal(step(tap, held()).action, "idle");
  const hold = make("down");
  repeat(8, () => step(hold));
  assert.equal(step(hold).x, 65);
});

test("held direction precedence is up, down, left, right without diagonals", () => {
  for (const [keys, selected] of [
    [["right", "left", "down", "up"], "up"],
    [["right", "left", "down"], "down"],
    [["right", "left"], "left"],
    [["right"], "right"],
  ]) {
    const view = step(make(selected), held(...keys));
    assert.equal(view.facing, selected);
    assert.equal(Math.abs(view.x - 64) + Math.abs(view.y - 80), 1);
  }
});

test("release at every walk/run tick finishes the committed tile then stops", () => {
  for (const [run, duration] of [[false, 16], [true, 8]]) {
    for (let releaseAfter = 1; releaseAfter <= duration; releaseAfter++) {
      const motion = make();
      repeat(releaseAfter, () => step(motion, held("right"), run));
      repeat(duration - releaseAfter, () => step(motion, held(), run));
      assert.equal(motion.player.x, 5);
      assert.equal(getMotionView(motion).x, 80);
      assert.equal(step(motion, held(), run).action, "idle");
      assert.equal(motion.player.x, 5);
    }
  }
});

test("mid-step direction changes wait for the boundary and do not add a rest turn", () => {
  for (let changeAfter = 1; changeAfter < 16; changeAfter++) {
    const motion = make();
    repeat(changeAfter, () => step(motion));
    repeat(16 - changeAfter, () => {
      const view = step(motion, held("down"));
      assert.equal(view.facing, "right");
      assert.equal(view.y, 80);
    });
    const next = step(motion, held("down"));
    assert.equal(next.action, "walk");
    assert.deepEqual([next.x, next.y], [80, 81]);
  }
});

test("input is held state, so a mid-step turn pressed and released is not queued", () => {
  const motion = make();
  repeat(4, () => step(motion));
  step(motion, held("up"));
  repeat(11, () => step(motion, held()));
  const next = step(motion, held());
  assert.equal(next.action, "idle");
  assert.equal(next.facing, "right");
  assert.deepEqual([next.x, next.y], [80, 80]);
});

test("walk and run preserve alternating gait across consecutive steps", () => {
  for (const [run, strideHold, idleHold] of [[false, 8, 8], [true, 5, 3]]) {
    const motion = make();
    const views = repeat(2 * (strideHold + idleHold), () => step(motion, held("right"), run));
    assert.deepEqual(views.map(v => v.pose), [
      ...Array(strideHold).fill("strideA"), ...Array(idleHold).fill("idle"),
      ...Array(strideHold).fill("strideB"), ...Array(idleHold).fill("idle"),
    ]);
    assert.equal(motion.player.x, 6);
  }
});

test("held blocked attempt keeps its 32-tick cadence without displacement", () => {
  const motion = make();
  const frames = [step(motion, held("right"), false, () => false)];
  frames.push(...repeat(31, () => step(motion, held("right"), false, () => false)));
  assert.deepEqual(frames.map(f => f.pose), [...Array(16).fill("strideA"), ...Array(16).fill("idle")]);
  for (const view of frames) {
    assert.equal(view.action, "blocked");
    assert.equal(view.moving, false);
    assert.deepEqual([view.x, view.y], [64, 80]);
  }
  assert.equal(step(motion, held()).action, "idle");
});

test("blocked changed direction or newly clear held route interrupts immediately", () => {
  const changed = make();
  step(changed, held("right"), false, () => false);
  const turnAway = step(changed, held("down"));
  assert.equal(turnAway.action, "walk");
  assert.deepEqual([turnAway.x, turnAway.y], [64, 81]);
  const cleared = make();
  repeat(5, () => step(cleared, held("right"), false, () => false));
  const newlyClear = step(cleared);
  assert.equal(newlyClear.action, "walk");
  assert.equal(newlyClear.actionTick, 1);
  assert.equal(newlyClear.x, 65);
});

test("run and board changes are sampled only at action boundaries", () => {
  const motion = make();
  step(motion);
  const frames = repeat(15, () => step(motion, held("right"), true, open, { board: true }));
  assert.ok(frames.every(f => f.action === "walk"));
  assert.equal(frames.at(-1).x, 80);
  const next = step(motion, held("right"), true, open, { board: true });
  assert.equal(next.action, "run");
  assert.equal(next.actionTicks, 6);
});

test("skateboard has integer 6/7 tick steps and exactly 1.25x run benefit over its cadence", () => {
  const board = make(), run = make();
  const durations = [];
  let previousX = 64;
  repeat(32, () => {
    const view = step(board, held("right"), true, open, { board: true });
    if (view.actionTick === 1) durations.push(view.actionTicks);
    assert.ok([2, 3].includes(view.x - previousX));
    assert.ok(Number.isInteger(view.x));
    previousX = view.x;
    step(run, held("right"), true);
  });
  assert.deepEqual(durations, [6, 7, 6, 7, 6]);
  assert.equal(board.player.x - 4, 5);
  assert.equal(run.player.x - 4, 4);
  assert.equal((board.player.x - 4) / (run.player.x - 4), 1.25);
  assert.equal(step(make(), held("right"), false, open, { board: true }).actionTicks, 16);
});

test("save-facing state stays on completed cells and reconstruction resumes safely", () => {
  const motion = make();
  repeat(10, () => step(motion));
  assert.equal(getMotionView(motion).x, 74);
  const savedPlayer = JSON.parse(JSON.stringify(motion.player));
  assert.deepEqual(savedPlayer, { x: 4, y: 5, facing: "right" });
  const restored = createMotion(savedPlayer);
  assert.equal(getMotionView(restored).x, 64);
  repeat(6, () => step(motion, held()));
  assert.equal(motion.player.x, 5);
  assert.equal(getMotionView(createMotion({ ...motion.player })).x, 80);
});

function traceAtRate(hz) {
  const motion = make("down");
  const clock = createMotionClock();
  const trace = [];
  for (let frame = 0; frame < hz * 5; frame++) {
    advanceMotionClock(clock, 1 / hz, tick => {
      const direction = tick <= 24 ? "up" : tick <= 88 ? "right" : tick <= 160 ? "down" : "left";
      const input = tick >= 17 && tick <= 24 || tick >= 180 && tick <= 195 ? held() : held(direction);
      const canEnter = (x, y) => !(tick >= 65 && tick <= 96 && x > 6);
      const view = step(motion, input, tick > 40 && tick < 160, canEnter, { board: tick >= 120 });
      trace.push(view);
    });
  }
  assert.equal(clock.droppedTicks, 0);
  assert.equal(trace.length, Math.floor(5 / TICK_SECONDS));
  return trace;
}

test("identical tick-stamped traces match at 30/60/90/120/144 Hz presentation", () => {
  const expected = traceAtRate(30);
  assert.ok(expected.length > 250);
  assert.deepEqual(new Set(expected.map(v => v.action)), new Set(["turn", "walk", "run", "blocked", "idle"]));
  for (const hz of [60, 90, 120, 144]) assert.deepEqual(traceAtRate(hz), expected, `${hz} Hz diverged`);
  assert.ok(expected.every(v => Number.isInteger(v.x) && Number.isInteger(v.y)));
});

test("long frames process at most eight ticks, drop excess whole ticks and preserve remainder", () => {
  const clock = createMotionClock();
  const calls = [];
  const result = advanceMotionClock(clock, TICK_SECONDS * 25.5, tick => calls.push(tick));
  assert.deepEqual(calls, [1, 2, 3, 4, 5, 6, 7, 8]);
  assert.equal(result.ticks, 8);
  assert.equal(result.droppedTicks, 17);
  assert.equal(clock.droppedSeconds, 17 * TICK_SECONDS);
  assert.equal(result.remainderSeconds, TICK_SECONDS / 2);
  assert.equal(advanceMotionClock(clock, TICK_SECONDS / 2, tick => calls.push(tick)).ticks, 1);
  assert.equal(clock.tick, 9);
  assert.equal(clock.droppedTicks, 17);
});

test("foreground reset removes partial elapsed time but preserves committed motion and diagnostics", () => {
  const clock = createMotionClock(), motion = make();
  advanceMotionClock(clock, TICK_SECONDS * 10.5, () => step(motion));
  assert.equal(clock.droppedTicks, 2);
  assert.equal(getMotionView(motion).x, 72);
  resetMotionClock(clock);
  assert.equal(clock.accumulator, 0);
  assert.equal(clock.droppedTicks, 2);
  const paused = getMotionView(motion);
  assert.equal(advanceMotionClock(clock, 0, () => step(motion)).ticks, 0);
  assert.deepEqual(getMotionView(motion), paused);
  advanceMotionClock(clock, TICK_SECONDS / 2, () => step(motion, held()));
  assert.equal(getMotionView(motion).x, 72);
  advanceMotionClock(clock, TICK_SECONDS * 7.5, () => step(motion, held()));
  assert.equal(motion.player.x, 5);
  assert.equal(step(motion, held()).action, "idle");
});

test("invalid fractional players and invalid clock inputs fail explicitly", () => {
  assert.throws(() => createMotion({ x: 1.5, y: 2, facing: "down" }), TypeError);
  assert.throws(() => createMotion({ x: 1, y: 2, facing: "diagonal" }), TypeError);
  assert.throws(() => createMotionClock({ maxTicksPerFrame: 0 }), TypeError);
  for (const elapsed of [-1, NaN, Infinity])
    assert.throws(() => advanceMotionClock(createMotionClock(), elapsed, () => {}), TypeError);
});
