// Synthetic, isolated lifecycle and save-migration checks. No real profile.
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { mkdir, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { createState, startMorning, rescue, publish, SAVE_KEY, BACKUP_KEY,
  PRE_GRID_KEY, PRE_GRID_BACKUP_KEY } from "../src/state.js";
import { isBlocked } from "../src/world.js";

const require = createRequire(import.meta.url);
let playwright;
try { playwright = require("playwright"); }
catch { playwright = require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES + "/playwright"); }
const base = process.env.TEST_URL || "http://127.0.0.1:5178";
const output = process.env.TEST_OUTPUT_DIR || "test-results";
await mkdir(output, { recursive: true });
const browser = await playwright.chromium.launch({ headless: true,
  executablePath: process.env.CHROMIUM_EXECUTABLE || undefined,
  args: ["--no-sandbox", "--disable-dev-shm-usage"] });
const passed = [], errors = [];
const pass = name => { passed.push(name); console.log("PASS", name); };
const snapshot = page => page.evaluate(async () => (await import("/src/main.js")).getDebugSnapshot());
const motion = page => page.evaluate(async () => (await import("/src/main.js")).getDebugMovement());
async function until(read, predicate, timeout = 4000) {
  const deadline = Date.now() + timeout;
  let value;
  while (Date.now() < deadline) {
    value = await read();
    if (predicate(value)) return value;
    await new Promise(resolve => setTimeout(resolve, 10));
  }
  throw new Error(`Timeout: ${JSON.stringify(value)}`);
}
const idle = page => until(() => motion(page), value => value.settled && value.action === "idle");
function fixture(scene = "bedroom", x = 8, y = 8, facing = "right") {
  const state = createState("Lifecycle Hero", "girl", "River");
  startMorning(state, true);
  rescue(state, "isopods");
  rescue(state, "springtails");
  publish(state, { kind: "photo", frame: 55, zoom: 1.2 });
  state.gridVersion = 1;
  state.scene = scene;
  state.player = { x, y, facing };
  return state;
}
async function withStorage(entries, check, { failWrites = false } = {}) {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await context.addInitScript(({ entries, origin, failWrites }) => {
    if (location.origin !== origin) return;
    if (!sessionStorage.getItem("lifecycle-fixture-ready")) {
      for (const [key, raw] of Object.entries(entries)) localStorage.setItem(key, raw);
      sessionStorage.setItem("lifecycle-fixture-ready", "1");
    }
    if (failWrites) {
      const setItem = Storage.prototype.setItem;
      Storage.prototype.setItem = function(key, value) {
        if (this === localStorage) throw new DOMException("Synthetic quota failure", "QuotaExceededError");
        return setItem.call(this, key, value);
      };
    }
  }, { entries, origin: new URL(base).origin, failWrites });
  const page = await context.newPage();
  page.on("pageerror", error => errors.push(error.message));
  try {
    await page.goto(base);
    await page.locator('[data-action="continue"]').waitFor();
    await check(page);
  } finally { await context.close(); }
}
const withFixture = (state, check) => withStorage({ [SAVE_KEY]: JSON.stringify(state) }, check);
async function begin(page) {
  await page.locator('[data-action="continue"]').click();
  await idle(page);
}
async function startStep(page, key) {
  await page.keyboard.down(key);
  return until(() => motion(page), value => value.action === "walk" && !value.settled);
}
async function setHidden(page, hidden) {
  return page.evaluate(async hidden => {
    Object.defineProperty(document, "hidden", { configurable: true, get: () => hidden });
    Object.defineProperty(document, "visibilityState", { configurable: true, get: () => hidden ? "hidden" : "visible" });
    document.dispatchEvent(new Event("visibilitychange"));
    return (await import("/src/main.js")).getDebugMovement();
  }, hidden);
}
const stableMotion = ({ x, y, pose, action, actionTick, tileX, tileY, tick }) => ({ x, y, pose, action, actionTick, tileX, tileY, tick });
function progress(state, { savedAt = true } = {}) {
  const result = structuredClone(state);
  delete result.player;
  delete result.gridVersion;
  if (!savedAt) delete result.savedAt;
  return result;
}
const rawSaves = page => page.evaluate(keys => Object.fromEntries(keys.map(key => [key, localStorage.getItem(key)])),
  [SAVE_KEY, BACKUP_KEY, PRE_GRID_KEY, PRE_GRID_BACKUP_KEY]);
async function saveViaUI(page) {
  await page.locator("#start").click();
  await page.locator('[data-action="save"]').click();
}
const hash = bytes => createHash("sha256").update(bytes).digest("hex");
async function fingerprints() {
  return Object.fromEntries(await Promise.all(["src/main.js", "src/movement.js", "src/state.js", "src/world.js", "src/grid-save.js"].map(async path => {
    const response = await fetch(new URL(path, base + "/"));
    assert.equal(response.status, 200);
    return [path, hash(Buffer.from(await response.arrayBuffer()))];
  })));
}
const beforeHashes = await fingerprints();
let failure = null;
try {
  await withFixture(fixture(), async page => {
    await begin(page);
    const started = await startStep(page, "ArrowRight");
    const hidden = await setHidden(page, true);
    const domainBefore = await snapshot(page);
    await page.waitForTimeout(600);
    assert.deepEqual(stableMotion(await motion(page)), stableMotion(hidden));
    assert.equal((await snapshot(page)).time, domainBefore.time);
    assert.equal((await snapshot(page)).tank.hours, domainBefore.tank.hours);
    const resumed = await setHidden(page, false);
    assert.deepEqual(stableMotion(resumed), stableMotion(hidden));
    await idle(page);
    const finished = await snapshot(page);
    assert.deepEqual([finished.player.x, finished.player.y], [started.destination.x, started.destination.y]);
    assert.equal((await motion(page)).clock.droppedTicks, hidden.clock.droppedTicks);
    await page.waitForTimeout(350);
    assert.deepEqual((await snapshot(page)).player, finished.player);
    await page.keyboard.up("ArrowRight");
  });
  pass("Synthetic visibility hide freezes committed motion and habitat time; resume retains the step, clears held input and produces no catch-up ticks.");

  await withFixture(fixture(), async page => {
    await begin(page);
    const started = await startStep(page, "ArrowRight");
    await page.locator("#start").click();
    await page.locator('[data-action="resume"]').waitFor();
    const paused = await motion(page);
    assert.equal(paused.settled, false);
    await page.waitForTimeout(400);
    assert.deepEqual(stableMotion(await motion(page)), stableMotion(paused));
    await page.locator('[data-action="resume"]').click();
    await idle(page);
    const finished = await snapshot(page);
    assert.deepEqual([finished.player.x, finished.player.y], [started.destination.x, started.destination.y]);
    await page.waitForTimeout(350);
    assert.deepEqual((await snapshot(page)).player, finished.player);
    await page.keyboard.up("ArrowRight");
  });
  pass("Pause menu freezes an in-flight step and its pose; resume completes exactly that tile without restoring held input.");

  await withFixture(fixture("bedroom", 8, 7, "up"), async page => {
    await begin(page);
    await startStep(page, "ArrowUp");
    await page.keyboard.press("z");
    assert.equal((await motion(page)).settled, false);
    assert.equal(await page.locator("#overlay").isVisible(), false);
    await page.locator('[data-action="manage"]').waitFor({ state: "visible" });
    assert.deepEqual([(await snapshot(page)).player.x, (await snapshot(page)).player.y], [8, 6]);
    assert.equal((await motion(page)).settled, true);
    await page.keyboard.up("ArrowUp");
  });
  pass("A pressed mid-step waits for the completed adjacent tile before opening the tank interaction.");

  await withFixture(fixture("bedroom", 14, 9, "down"), async page => {
    await begin(page);
    await startStep(page, "ArrowDown");
    await page.keyboard.press("z");
    assert.equal((await snapshot(page)).scene, "bedroom");
    assert.equal((await motion(page)).settled, false);
    await until(() => page.locator("#fade").getAttribute("class"), value => (value || "").split(/\s+/).includes("on"));
    const source = await snapshot(page);
    assert.equal(source.scene, "bedroom");
    assert.deepEqual([source.player.x, source.player.y], [14, 10]);
    assert.equal((await motion(page)).settled, true);
    await until(() => snapshot(page), value => value.scene === "house");
    const destination = await snapshot(page);
    assert.deepEqual([destination.player.x, destination.player.y], [14, 4]);
    assert.equal(isBlocked(destination.scene, destination.player.x, destination.player.y, destination), false);
    await page.keyboard.up("ArrowDown");
  });
  pass("A pressed mid-step completes the source tile before fade and warp, then arrives at the authored safe destination.");

  for (const [x, y, facing, key] of [[1, 10, "left", "ArrowLeft"], [15, 10, "right", "ArrowRight"], [8, 11, "down", "ArrowDown"], [5, 3, "up", "ArrowUp"]]) {
    await withFixture(fixture("bedroom", x, y, facing), async page => {
      await begin(page);
      await page.keyboard.down(key);
      const blocked = await until(() => motion(page), value => value.action === "blocked");
      assert.equal(blocked.actionTicks, 32);
      await page.keyboard.up(key);
      const stop = await until(async () => {
        const view = await motion(page);
        assert.deepEqual([view.x, view.y], [x * 16, y * 16]);
        assert.deepEqual([view.tileX, view.tileY], [x, y]);
        return view;
      }, value => value.action === "idle");
      assert.ok(stop.tick - blocked.tick >= 32 - blocked.actionTick);
    });
  }
  pass("All four scene-edge directions use a 32-tick blocked action, finish after release and never change position.");

  const legacy = fixture("house", 5.2, 6.4, "left");
  delete legacy.gridVersion;
  const backup = fixture("yard", 7.6, 9.4, "up");
  delete backup.gridVersion;
  backup.hero = "Backup Hero";
  backup.money += 177;
  const primaryRaw = JSON.stringify(legacy, null, 2) + "\n";
  const backupRaw = JSON.stringify(backup, null, 4) + "\n\n";
  await withStorage({ [SAVE_KEY]: primaryRaw, [BACKUP_KEY]: backupRaw }, async page => {
    const migrated = await snapshot(page);
    assert.deepEqual(progress(migrated), progress(legacy));
    assert.equal(migrated.gridVersion, 1);
    assert.ok(Number.isInteger(migrated.player.x) && Number.isInteger(migrated.player.y));
    assert.equal(isBlocked(migrated.scene, migrated.player.x, migrated.player.y, migrated), false);
    assert.deepEqual(await rawSaves(page), { [SAVE_KEY]: primaryRaw, [BACKUP_KEY]: backupRaw, [PRE_GRID_KEY]: null, [PRE_GRID_BACKUP_KEY]: null });
    await begin(page);
    await saveViaUI(page);
    let stored = await rawSaves(page);
    assert.equal(stored[PRE_GRID_KEY], primaryRaw);
    assert.equal(stored[PRE_GRID_BACKUP_KEY], backupRaw);
    assert.equal(JSON.parse(stored[SAVE_KEY]).gridVersion, 1);
    assert.deepEqual(progress(JSON.parse(stored[SAVE_KEY]), { savedAt: false }), progress(legacy, { savedAt: false }));
    await page.locator('[data-action="save"]').click();
    stored = await rawSaves(page);
    assert.equal(stored[PRE_GRID_KEY], primaryRaw);
    assert.equal(stored[PRE_GRID_BACKUP_KEY], backupRaw);
  });
  pass("Legacy fractional primary loads without nonposition changes or initial writes; UI save retains both exact pre-grid raw archives across repeated saves.");

  await withStorage({ [SAVE_KEY]: "{damaged-primary", [BACKUP_KEY]: backupRaw }, async page => {
    const recovered = await snapshot(page);
    assert.deepEqual(progress(recovered), progress(backup));
    assert.equal(recovered.gridVersion, 1);
    assert.equal(isBlocked(recovered.scene, recovered.player.x, recovered.player.y, recovered), false);
    assert.match(await page.locator(".notice").textContent(), /recovered/i);
    assert.equal((await rawSaves(page))[BACKUP_KEY], backupRaw);
    await begin(page);
    await saveViaUI(page);
    const stored = await rawSaves(page);
    assert.equal(stored[PRE_GRID_KEY], null);
    assert.equal(stored[PRE_GRID_BACKUP_KEY], backupRaw);
    assert.equal(stored[BACKUP_KEY], backupRaw);
    assert.deepEqual(progress(JSON.parse(stored[SAVE_KEY]), { savedAt: false }), progress(backup, { savedAt: false }));
  });
  pass("Corrupt-primary recovery loads the valid legacy backup unchanged, and UI save preserves its exact pre-grid archive and normal backup.");
  const quotaLegacy = fixture("bedroom", 8.2, 6.4, "right");
  delete quotaLegacy.gridVersion;
  quotaLegacy.tank.moisture = 40;
  const quotaRaw = JSON.stringify(quotaLegacy, null, 3) + "\n";
  await withStorage({ [SAVE_KEY]: quotaRaw, [BACKUP_KEY]: backupRaw }, async page => {
    const originalStorage = { [SAVE_KEY]: quotaRaw, [BACKUP_KEY]: backupRaw, [PRE_GRID_KEY]: null, [PRE_GRID_BACKUP_KEY]: null };
    assert.deepEqual(progress(await snapshot(page)), progress(quotaLegacy));
    await begin(page);
    await page.locator("#a-button").click();
    await page.locator('[data-action="manage"]').click();
    await page.locator('[data-action="mist"]').click();
    assert.equal((await snapshot(page)).tank.moisture, 54);
    await page.locator("#start").click();
    const unsaved = await snapshot(page);
    await page.locator('[data-action="save"]').click();
    assert.match(await page.locator("#panel-status").textContent(), /Could not save/i);
    await page.locator('[data-action="title"]').click();
    assert.equal(await page.locator('[data-action="resume"]').isVisible(), true);
    assert.equal(await page.locator('[data-action="continue"]').count(), 0);
    const retained = await snapshot(page);
    assert.deepEqual(retained, unsaved);
    assert.equal(retained.gridVersion, 1);
    assert.ok(Number.isInteger(retained.player.x) && Number.isInteger(retained.player.y));
    assert.deepEqual(await rawSaves(page), originalStorage);
    // Explicit reload naturally discards unsaved care changes. It must still
    // load/migrate the exact preserved legacy save while writes stay denied.
    await page.reload();
    await page.locator('[data-action="continue"]').waitFor();
    const restored = await snapshot(page);
    assert.deepEqual(progress(restored), progress(quotaLegacy));
    assert.equal(restored.tank.moisture, 40);
    await begin(page);
    const step = await startStep(page, "ArrowRight");
    await page.keyboard.up("ArrowRight");
    await idle(page);
    const moved = await snapshot(page);
    assert.deepEqual([moved.player.x, moved.player.y], [step.destination.x, step.destination.y]);
    assert.ok(Number.isInteger(moved.player.x) && Number.isInteger(moved.player.y));
    assert.deepEqual(await rawSaves(page), originalStorage);
  }, { failWrites: true });
  pass("Synthetic quota failure keeps Save/Title in the paused current grid state with unsaved care changes; old bytes remain exact and reload/Continue still migrates and moves without writes.");
  assert.deepEqual(errors, []);
  pass("No uncaught browser errors in isolated lifecycle, migration or quota-failure contexts.");
} catch (error) {
  failure = { message: error.message, stack: error.stack };
  console.error("FAIL", error);
  process.exitCode = 1;
} finally {
  const afterHashes = await fingerprints();
  await writeFile(`${output}/lifecycle-report.json`, JSON.stringify({
    testedAt: new Date().toISOString(), url: base, browser: await browser.version(),
    passed, errors, failure, beforeHashes, afterHashes,
    runtimeFilesUnchangedDuringRun: JSON.stringify(beforeHashes) === JSON.stringify(afterHashes),
    isolation: "Fresh browser contexts with synthetic localStorage fixtures; no real browser profile or user saves accessed.",
    limitations: [
      "Visibility is a synthetic document.hidden/visibilityState override plus visibilitychange event, not OS suspension or a physical-device background test.",
      "Timing uses source-derived movement rules. No Emerald emulator/hardware captures establish first/last presented action frames or total door timing.",
      "Browser polling checks phase stability and action completion, not every rendered video frame.",
      "Migration browser coverage uses representative primary, backup-recovery and quota-failure legacy fixtures. Exhaustive scene/loan/progress combinations belong to separate domain tests.",
      "Desktop Chrome mobile emulation does not establish physical iPhone/Safari behavior."
    ]
  }, null, 2) + "\n");
  await browser.close();
}
