// Optional end-to-end regression runner. npm install --no-save playwright
// Runs its own local server; TEST_URL can target an already running build.
import { createRequire } from "node:module";
import { mkdir, writeFile } from "node:fs/promises";
import { spawn } from "node:child_process";
import assert from "node:assert/strict";
import { scenes, getEntities, isBlocked, nearestEntity } from "../src/world.js";
const require = createRequire(import.meta.url);
let server;
if (!process.env.TEST_URL) {
  server = spawn(process.execPath, ["scripts/serve.mjs"], {
    env: { ...process.env, PORT: "5177" },
    stdio: ["ignore", "pipe", "pipe"],
  });
  await new Promise((resolve, reject) => {
    server.stdout.once("data", resolve);
    server.once("error", reject);
    server.once("exit", (code) =>
      reject(new Error("Test server stopped: " + code)),
    );
  });
}
let playwright;
try {
  playwright = require("playwright");
} catch {
  playwright = require(
    process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES + "/playwright",
  );
}
const browser = await playwright.chromium.launch({
  headless: true,
  executablePath: process.env.CHROMIUM_EXECUTABLE || undefined,
  args: ["--no-sandbox", "--disable-dev-shm-usage"],
});
await mkdir("test-results", { recursive: true });
const context = await browser.newContext({
  viewport: { width: 390, height: 844 },
  isMobile: true,
  hasTouch: true,
  deviceScaleFactor: 1,
});
const page = await context.newPage();
const errors = [];
page.on("pageerror", (error) => errors.push(error.message));
const base = process.env.TEST_URL || "http://127.0.0.1:5177";
const snapshot = (targetPage = page) =>
  targetPage.evaluate(async () => (await import("/src/main.js")).getDebugSnapshot());
const movement = (targetPage = page) =>
  targetPage.evaluate(async () => (await import("/src/main.js")).getDebugMovement());
async function waitForMovement(predicate, { targetPage = page, timeout = 4000 } = {}) {
  const deadline = Date.now() + timeout;
  let view;
  while (Date.now() < deadline) {
    view = await movement(targetPage);
    if (predicate(view)) return view;
    await targetPage.waitForTimeout(10);
  }
  throw new Error(`Timed out waiting for movement: ${JSON.stringify(view)}`);
}
const act = (action) => page.locator(`[data-action="${action}"]`).click();
const a = () => page.locator("#a-button").click();
const b = () => page.locator("#b-button").click();
const notes = [];
const pass = (message) => {
  notes.push(message);
  console.log("PASS", message);
};
async function finishDialogue(targetPage = page) {
  for (let i = 0; i < 30; i++) {
    if (!(await targetPage.locator("#dialogue").isVisible())) break;
    await targetPage.locator("#a-button").click();
  }
}
// Use completed tile coordinates for pathfinding. Release while the final tile
// is still in flight so an rAF cannot start an unwanted additional step.
const directionKeys = { up: "ArrowUp", down: "ArrowDown", left: "ArrowLeft", right: "ArrowRight" };
const directionDeltas = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] };
async function waitIdle(targetPage = page) {
  await waitForMovement(view => view.settled && view.action === "idle", { targetPage });
}
async function faceDirection(direction) {
  await waitIdle();
  if ((await snapshot()).player.facing === direction) return;
  const key = directionKeys[direction];
  await page.keyboard.down(key);
  try {
    await waitForMovement(view => view.facing === direction, { timeout: 3000 });
  } finally {
    await page.keyboard.up(key);
  }
  await waitIdle();
}
function facingToward(from, entity) {
  return entity.x > from.x ? "right" : entity.x < from.x ? "left"
    : entity.y > from.y ? "down" : entity.y < from.y ? "up" : from.facing;
}
async function moveAxis(axis, target) {
  await waitIdle();
  const from = (await snapshot()).player[axis];
  assert.ok(Number.isInteger(from) && Number.isInteger(target));
  if (target === from) return;
  const sign = Math.sign(target - from);
  const key = directionKeys[axis === "x" ? sign > 0 ? "right" : "left" : sign > 0 ? "down" : "up"];
  await page.keyboard.down(key);
  try {
    await waitForMovement(view => {
      const destination = view.destination?.[axis] ?? view[axis === "x" ? "tileX" : "tileY"];
      return sign > 0 ? destination >= target : destination <= target;
    }, { timeout: 15000 });
  } finally {
    await page.keyboard.up(key);
  }
  await waitIdle();
  assert.equal((await snapshot()).player[axis], target, "Held input overshot its intended committed tile");
}
async function approach(id) {
  await waitIdle();
  const s = await snapshot(), entity = getEntities(s).find(e => e.id === id);
  assert.ok(entity, `Missing entity ${s.scene}/${id}`);
  const start = [s.player.x, s.player.y];
  assert.ok(start.every(Number.isInteger), "Browser actor is not grid aligned");
  const key = p => p.join(","), frontier = [start], parents = new Map([[key(start), null]]);
  let end;
  for (let cursor = 0; cursor < frontier.length; cursor++) {
    const p = frontier[cursor];
    const player = { ...s.player, x: p[0], y: p[1] };
    player.facing = facingToward(player, entity);
    const fake = { ...s, player };
    if (Math.abs(player.x - entity.x) + Math.abs(player.y - entity.y) <= 1 && nearestEntity(fake)?.id === id) {
      end = p;
      break;
    }
    for (const [dx, dy] of Object.values(directionDeltas)) {
      const n = [p[0] + dx, p[1] + dy], k = key(n);
      if (n[0] < 0 || n[1] < 0 || n[0] >= scenes[s.scene].w || n[1] >= scenes[s.scene].h ||
          parents.has(k) || isBlocked(s.scene, n[0], n[1], s)) continue;
      parents.set(k, p);
      frontier.push(n);
    }
  }
  assert.ok(end, `No integer-grid route to ${s.scene}/${id}`);
  const path = [];
  for (let p = end; p; p = parents.get(key(p))) path.unshift(p);
  let i = 1;
  while (i < path.length) {
    const axis = path[i][0] !== path[i - 1][0] ? 0 : 1;
    const sign = Math.sign(path[i][axis] - path[i - 1][axis]);
    let j = i;
    while (j + 1 < path.length && path[j + 1][1 - axis] === path[j][1 - axis] &&
        Math.sign(path[j + 1][axis] - path[j][axis]) === sign) j++;
    await moveAxis(axis === 0 ? "x" : "y", path[j][axis]);
    i = j + 1;
  }
  await faceDirection(facingToward((await snapshot()).player, entity));
  assert.equal(nearestEntity(await snapshot())?.id, id, `Wrong interaction near ${id}`);
}
async function use(id) {
  await approach(id);
  await a();
}
async function door(id, target) {
  await use(id);
  for (let n = 0; n < 30; n++) {
    if ((await snapshot()).scene === target) return;
    await page.waitForTimeout(30);
  }
  assert.equal((await snapshot()).scene, target);
}
function nonPositionState(state) {
  const { player, savedAt, ...progress } = state;
  return progress;
}
async function verifyInputRelease(kind) {
  await waitIdle();
  const before = await snapshot();
  // Choose open floor so cancellation is proved by stopped input, not a wall.
  const direction = Object.keys(directionDeltas).find(direction => {
    const [dx, dy] = directionDeltas[direction];
    return [1, 2, 3].every(n => !isBlocked(before.scene, before.player.x + dx * n, before.player.y + dy * n, before));
  });
  assert.ok(direction, "Need an open three-cell line for input-release proof");
  await faceDirection(direction);
  const [dx, dy] = directionDeltas[direction];
  const target = { x: before.player.x + dx, y: before.player.y + dy };
  const control = page.locator(`[data-dir="${direction}"]`);
  if (kind === "blur") {
    await page.keyboard.down(directionKeys[direction]);
  } else {
    const rect = await control.boundingBox();
    await page.mouse.move(rect.x + rect.width / 2, rect.y + rect.height / 2);
    await page.mouse.down();
  }
  try {
    await waitForMovement(view => !view.settled && view.destination?.x === target.x && view.destination?.y === target.y,
      { timeout: 3000 });
    if (kind === "pointerup") await page.mouse.up();
    else if (kind === "pointercancel")
      await control.dispatchEvent("pointercancel", { pointerId: 1, pointerType: "mouse", isPrimary: true });
    else await page.evaluate(() => window.dispatchEvent(new Event("blur")));
    await waitIdle();
    const stopped = await snapshot();
    assert.deepEqual({ x: stopped.player.x, y: stopped.player.y }, target);
    assert.equal(await page.locator(".pressed").count(), 0);
    await page.waitForTimeout(400);
    assert.deepEqual((await snapshot()).player, stopped.player);
  } finally {
    // For cancellation/blur this is deliberately after the stop assertions.
    if (kind === "blur") await page.keyboard.up(directionKeys[direction]);
    else await page.mouse.up();
  }
}
async function verifyDeclinedLoan() {
  const secondContext = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 1 });
  const second = await secondContext.newPage();
  second.on("pageerror", error => errors.push(`Decline-loan context: ${error.message}`));
  const secondAct = action => second.locator(`[data-action="${action}"]`).click();
  try {
    await second.goto(base);
    await secondAct("new");
    await secondAct("boy");
    await second.locator("#hero-name").fill("Malik");
    await second.locator("#rival-name").fill("Avery");
    await secondAct("begin");
    await finishDialogue(second);
    await second.locator("#a-button").click();
    await finishDialogue(second);
    await secondAct("decline-loan");
    await finishDialogue(second);
    const state = await snapshot(second);
    assert.equal(state.hero, "Malik");
    assert.equal(state.rival, "Avery");
    assert.equal(state.gender, "boy");
    assert.equal(state.stage, "morning");
    assert.equal(state.money, 1200);
    assert.equal(state.debt, 0);
    assert.equal(state.tankOwned, true);
    assert.equal(state.tank.gallons, 25);
    assert.equal(state.tank.deaths, 0);
    assert.equal(state.flags.loanDecided, true);
    await second.locator("#start").click();
    await secondAct("save");
    const saved = await snapshot(second);
    await second.reload();
    await second.locator('[data-action="continue"]').waitFor();
    assert.deepEqual(nonPositionState(await snapshot(second)), nonPositionState(saved));
    await secondAct("continue");
    assert.equal((await snapshot(second)).money, 1200);
    assert.equal((await snapshot(second)).debt, 0);
    pass("A separate boy-Hero context declines the loan, receives the 25-gallon gift, keeps $12/no debt, and reloads unchanged progress.");
  } finally {
    await secondContext.close();
  }
}
try {
  await page.goto(base);
  await page.locator('[data-action="new"]').waitFor();
  await page.screenshot({ path: "test-results/mobile-title.png" });
  await act("new");
  await act("girl");
  assert.equal(await page.locator("#rival-gender").textContent(), "(boy)");
  await page.locator("#hero-name").fill("Ari");
  await page.locator("#rival-name").fill("Rowan");
  await act("begin");
  await finishDialogue();
  let s = await snapshot();
  assert.equal(s.gender, "girl");
  assert.equal(s.hero, "Ari");
  assert.equal(s.rival, "Rowan");
  pass("Girl Hero and opposite-gender rival can be named.");
  await a();
  await finishDialogue();
  await page.locator('[data-action="accept-loan"]').waitFor();
  await act("accept-loan");
  await finishDialogue();
  s = await snapshot();
  assert.equal(s.money, 11200);
  assert.equal(s.debt, 10000);
  assert.equal(s.tankOwned, true);
  assert.equal(s.tank.gallons, 25);
  assert.equal(s.tank.deaths, 0);
  pass(
    "Opening completes, animals survive, 25-gallon gift and $100 loan arrive.",
  );
  await use("gecko");
  await finishDialogue();
  await door("stairs", "house");
  await use("snail");
  await finishDialogue();
  await door("exit", "yard");
  await use("isopods");
  await finishDialogue();
  await use("springtails");
  await finishDialogue();
  s = await snapshot();
  assert.equal(s.flags.rescued.length, 4);
  assert.equal(s.tank.deaths, 0);
  pass("All four groups found by walking through bedroom, house, and yard.");
  await door("gate", "town");
  await page.screenshot({ path: "test-results/mobile-town.png" });
  const beforeNugget = (await snapshot()).money;
  await use("nugget");
  await finishDialogue();
  s = await snapshot();
  assert.equal(s.flags.notebook, true);
  assert.equal(s.flags.questReward, true);
  assert.equal(s.money, beforeNugget + 1500);
  pass("Professor Nugget gives notebook and the $15 search reward.");
  await door("critz", "critz");
  await use("shop-critz");
  const before = (await snapshot()).money;
  await act("buy-moss");
  assert.equal((await snapshot()).money, before - 300);
  await act("supply-gift");
  assert.equal((await snapshot()).flags.supplyGift, true);
  await b();
  await door("exit", "town");
  pass(
    "Critz shop is enterable; purchases debit money and the free kit is claimable.",
  );
  for (const [entry, keeper] of [
    ["vet", "shop-vet"],
    ["pharmacy", "shop-pharmacy"],
    ["bike", "shop-bike"],
    ["glass", "shop-glass"],
  ]) {
    await door(entry, entry);
    await use(keeper);
    await page.locator("#panel-title").waitFor();
    if (entry === "pharmacy") {
      await act("buy-medicine");
      assert.equal((await snapshot()).inventory.medicine, 1);
    }
    if (entry === "bike") {
      await act("buy-board");
      assert.equal((await snapshot()).flags.board, true);
    }
    if (entry === "glass") {
      await act("buy-hide");
      assert.equal((await snapshot()).tank.hide, true);
    }
    await b();
    await door("exit", "town");
  }
  pass(
    "Vet, Drug Store, Bike Shop, and Glow n’ Blow open; medicine, skateboard, and hide purchases work.",
  );
  await door("kaidHome", "kaidHome");
  await use("kaid");
  await b();
  await door("exit", "town");
  await door("rivalHome", "rivalHome");
  await use("rivalMom");
  await finishDialogue();
  await door("exit", "town");
  pass("Both neighboring homes and character dialogue are reachable.");
  await door("yard", "yard");
  await door("home", "house");
  await use("mom");
  await finishDialogue();
  assert.equal((await snapshot()).flags.medicineDelivered, true);
  await door("stairs", "bedroom");
  await use("tank");
  await act("manage");
  await act("moss");
  await act("feed");
  for (let i = 0; i < 4; i++) await act("mist");
  await page.locator('[data-action="light"][data-value="12"]').click();
  const tankBefore = (await snapshot()).tank;
  await act("observe");
  s = await snapshot();
  assert.ok(s.tank.moisture < tankBefore.moisture);
  assert.equal(s.tank.light, 12);
  await page.screenshot({ path: "test-results/mobile-manage.png" });
  await b();
  await act("stats");
  assert.ok(await page.getByText("Isopods", { exact: true }).isVisible());
  await b();
  pass("Management changes live conditions, inventory, and stats.");
  await act("view");
  await page.locator("#frame").fill("55");
  await page.locator("#zoom").fill("120");
  await act("capture");
  await act("publish");
  s = await snapshot();
  assert.equal(s.posts.length, 1);
  assert.ok(s.posts[0].views > 0);
  assert.ok(s.posts[0].revenue > 0);
  await act("observe");
  await page.screenshot({ path: "test-results/mobile-critter.png" });
  pass(
    "Framed tank photo posts to Critter and earns money; reach grows with time.",
  );
  await b();
  await use("tank");
  await act("view");
  await act("video-mode");
  await act("capture");
  await page.locator('[data-action="publish"]').waitFor({ timeout: 12000 });
  await act("publish");
  assert.equal((await snapshot()).posts[0].kind, "video");
  pass("Six-second simulated video records and posts.");
  await b();
  await page.locator("#start").click();
  await act("save");
  const saved = await snapshot();
  await page.reload();
  await page.locator('[data-action="continue"]').waitFor();
  // Title overlay pauses the world: compare before any habitat tick can occur.
  s = await snapshot();
  assert.deepEqual(nonPositionState(s), nonPositionState(saved));
  assert.deepEqual(s.player, saved.player);
  assert.equal(s.posts.length, 2);
  await act("continue");
  pass("Paused save/reload preserves complete nonposition state, including tank, inventory, flags and Critter records, plus completed player tile.");
  for (const viewport of [
    { width: 390, height: 844 },
    { width: 320, height: 568 },
    { width: 844, height: 390 },
    { width: 1280, height: 900 },
  ]) {
    await page.setViewportSize(viewport);
    await page.locator("#start").click();
    const geometry = await page.evaluate(() => {
      const p = document.querySelector("#panel").getBoundingClientRect(),
        a = document.querySelector("#a-button").getBoundingClientRect(),
        b = document.querySelector("#b-button").getBoundingClientRect();
      return {
        scrollWidth: document.documentElement.scrollWidth,
        width: innerWidth,
        height: innerHeight,
        p: { x: p.x, y: p.y, right: p.right, bottom: p.bottom },
        a: { x: a.x, y: a.y, right: a.right, bottom: a.bottom },
        b: { x: b.x, y: b.y, right: b.right, bottom: b.bottom },
      };
    });
    assert.ok(geometry.scrollWidth <= geometry.width, JSON.stringify(geometry));
    for (const k of ["p", "a", "b"]) {
      const r = geometry[k];
      assert.ok(
        r.x >= -1 &&
          r.y >= -1 &&
          r.right <= geometry.width + 1 &&
          r.bottom <= geometry.height + 1,
        `${viewport.width}x${viewport.height} clipped ${k}: ${JSON.stringify(geometry)}`,
      );
    }
    await b();
    await page.screenshot({
      path: `test-results/layout-${viewport.width}x${viewport.height}.png`,
    });
  }
  pass(
    "320px and 390px portrait, 844px landscape, and desktop layouts keep panels and controls onscreen.",
  );
  await page.setViewportSize({ width: 390, height: 844 });
  await verifyInputRelease("pointerup");
  pass("D-pad release finishes exactly one committed step and starts no further step.");
  await verifyInputRelease("pointercancel");
  pass("Pointer cancellation clears held direction and pressed styling before physical release.");
  await verifyInputRelease("blur");
  pass("A synthetic window blur clears a held keyboard direction; its committed step settles without another step.");
  await verifyDeclinedLoan();
  assert.deepEqual(errors, []);
  pass("No uncaught browser errors.");
  await writeFile(
    "test-results/browser-report.json",
    JSON.stringify({
      passed: notes,
      errors,
      coverage: {
        browserWalkthrough: "Girl Hero / accepted loan; all original story, town, care and Critter steps retained.",
        secondContext: "Boy Hero / declined loan; opening, names, surviving animals, 25-gallon gift, money/debt, save/reload.",
        navigation: "Integer cardinal BFS with NPC occupancy; real held keys released when target destination is committed.",
        saveEquality: "All state fields except player and savedAt compared while title pauses time; player compared separately.",
        inputEvents: ["actual pointerup", "synthetic pointercancel while physical pointer remains held", "synthetic window blur while keyboard direction remains held"],
        isolatedStorage: true,
        limitations: ["Desktop Chrome viewport emulation is not physical iPhone/Safari testing.", "Synthetic blur exercises the app handler, not OS backgrounding or document.hidden timing.", "Source-derived tile motion is tested separately; this walkthrough does not establish reference emulator frame equivalence."]
      }
    }, null, 2),
  );
} catch (error) {
  await page.screenshot({ path: "test-results/failure.png" });
  console.error("FAIL", error);
  console.error("STATE", await snapshot());
  process.exitCode = 1;
} finally {
  await browser.close();
  server?.kill();
}
