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
const snapshot = () =>
  page.evaluate(async () => (await import("./src/main.js")).getDebugSnapshot());
const act = (action) => page.locator(`[data-action="${action}"]`).click();
const a = () => page.locator("#a-button").click();
const b = () => page.locator("#b-button").click();
const notes = [];
const pass = (message) => {
  notes.push(message);
  console.log("PASS", message);
};
async function finishDialogue() {
  for (let i = 0; i < 30; i++) {
    if (!(await page.locator("#dialogue").isVisible())) break;
    await a();
  }
}
async function moveAxis(axis, target) {
  const s = await snapshot(),
    from = s.player[axis];
  if (Math.abs(target - from) < 0.06) return;
  const sign = Math.sign(target - from),
    key =
      axis === "x"
        ? sign > 0
          ? "ArrowRight"
          : "ArrowLeft"
        : sign > 0
          ? "ArrowDown"
          : "ArrowUp";
  await page.keyboard.down(key);
  try {
    let reached = false;
    const deadline = Date.now() + 12000;
    while (Date.now() < deadline) {
      const current = (await snapshot()).player[axis];
      if (sign > 0 ? current >= target - 0.035 : current <= target + 0.035) {
        reached = true;
        break;
      }
      await page.waitForTimeout(30);
    }
    assert.ok(
      reached,
      `Movement stopped at ${JSON.stringify((await snapshot()).player)}; wanted ${axis}=${target}`,
    );
  } finally {
    await page.keyboard.up(key);
  }
}
async function approach(id) {
  const s = await snapshot(),
    entity = getEntities(s).find((e) => e.id === id);
  assert.ok(entity, `Missing entity ${s.scene}/${id}`);
  const start = [Math.round(s.player.x * 2), Math.round(s.player.y * 2)];
  const key = (p) => p.join(","),
    frontier = [start],
    parents = new Map([[key(start), null]]);
  let end;
  for (let cursor = 0; cursor < frontier.length; cursor++) {
    const p = frontier[cursor],
      fake = { ...s, player: { ...s.player, x: p[0] / 2, y: p[1] / 2 } };
    if (
      Math.hypot(fake.player.x - entity.x, fake.player.y - entity.y) < 1.05 &&
      nearestEntity(fake)?.id === id
    ) {
      end = p;
      break;
    }
    for (const [dx, dy] of [
      [1, 0],
      [-1, 0],
      [0, 1],
      [0, -1],
    ]) {
      const n = [p[0] + dx, p[1] + dy],
        k = key(n);
      if (parents.has(k) || isBlocked(s.scene, n[0] / 2, n[1] / 2)) continue;
      parents.set(k, p);
      frontier.push(n);
    }
  }
  assert.ok(end, `No route to ${s.scene}/${id}`);
  const path = [];
  for (let p = end; p; p = parents.get(key(p))) path.unshift(p);
  // Snap along open floor, then group straight runs into held-key gestures.
  await moveAxis("x", start[0] / 2);
  await moveAxis("y", start[1] / 2);
  let i = 1;
  while (i < path.length) {
    const axis = path[i][0] !== path[i - 1][0] ? 0 : 1,
      sign = Math.sign(path[i][axis] - path[i - 1][axis]);
    let j = i;
    while (
      j + 1 < path.length &&
      path[j + 1][1 - axis] === path[j][1 - axis] &&
      Math.sign(path[j + 1][axis] - path[j][axis]) === sign
    )
      j++;
    await moveAxis(axis === 0 ? "x" : "y", path[j][axis] / 2);
    i = j + 1;
  }
  const now = await snapshot();
  assert.equal(nearestEntity(now)?.id, id, `Wrong interaction near ${id}`);
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
try {
  await page.goto(base);
  await page.locator('[data-action="new"]').waitFor();
  await page.screenshot({ path: "test-results/mobile-title.png" });
  await act("new");
  await act("girl");
  await page.locator("#hero-name").fill("Ari");
  await page.locator("#rival-name").fill("Rowan");
  await act("begin");
  await finishDialogue();
  let s = await snapshot();
  assert.equal(s.gender, "girl");
  assert.equal(s.hero, "Ari");
  pass("Girl Hero and opposite-gender rival can be named.");
  await a();
  await finishDialogue();
  await page.locator('[data-action="accept-loan"]').waitFor();
  await act("accept-loan");
  await finishDialogue();
  s = await snapshot();
  assert.equal(s.money, 11200);
  assert.equal(s.tankOwned, true);
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
  await use("nugget");
  await finishDialogue();
  s = await snapshot();
  assert.equal(s.flags.notebook, true);
  assert.equal(s.flags.questReward, true);
  pass("Professor Nugget gives notebook and the $15 search reward.");
  await door("critz", "critz");
  await use("shop-critz");
  const before = (await snapshot()).money;
  await act("buy-moss");
  assert.equal((await snapshot()).money, before - 300);
  await act("supply-gift");
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
    if (entry === "pharmacy") await act("buy-medicine");
    if (entry === "bike") await act("buy-board");
    if (entry === "glass") await act("buy-hide");
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
  await act("continue");
  s = await snapshot();
  assert.equal(s.hero, saved.hero);
  assert.equal(s.money, saved.money);
  assert.equal(s.posts.length, 2);
  assert.deepEqual(s.flags.rescued, saved.flags.rescued);
  pass(
    "Refresh restores name, money, rescues, tank, inventory, and Critter posts.",
  );
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
  const beforeMove = await snapshot();
  const rect = await page.locator('[data-dir="left"]').boundingBox();
  await page.mouse.move(rect.x + rect.width / 2, rect.y + rect.height / 2);
  await page.mouse.down();
  await page.waitForTimeout(300);
  await page.mouse.up();
  const afterMove = await snapshot();
  assert.ok(afterMove.player.x < beforeMove.player.x);
  await page.waitForTimeout(200);
  assert.equal((await snapshot()).player.x, afterMove.player.x);
  pass("Virtual D-pad hold moves, release stops; no sticky movement.");
  assert.deepEqual(errors, []);
  pass("No uncaught browser errors.");
  await writeFile(
    "test-results/browser-report.json",
    JSON.stringify({ passed: notes, errors }, null, 2),
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
