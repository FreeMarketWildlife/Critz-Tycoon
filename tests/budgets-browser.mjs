import {createRequire} from 'node:module';
const require = createRequire(import.meta.url);
const {chromium} = require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES ? process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES + '/playwright' : 'playwright');
import assert from 'node:assert/strict';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const base = process.env.CRITZ_REVIEW_URL || 'http://localhost:5181/art-review/budgets.html';
const output = process.env.CRITZ_QA_OUTPUT || 'test-results/budgets';
const expectedRoles = (process.env.CRITZ_EXPECTED_ROLES || 'mom,kaid,professor').split(',');
const report = { url: base, startedAt: new Date().toISOString(), checks: [], screenshots: [] };
await mkdir(output, { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_EXECUTABLE, headless: true });
const contexts = [];
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
async function check(name, fn) {
  try { const details = await fn(); report.checks.push({ name, status: 'pass', details }); console.log(`PASS ${name}`); }
  catch (error) { report.checks.push({ name, status: 'fail', error: error.stack }); console.error(`FAIL ${name}: ${error.message}`); }
}
async function context(options = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, ...options }); contexts.push(ctx);
  await ctx.addInitScript(() => {
    const sentinel = JSON.stringify({ syntheticQA: true, marker: 'never mutate or load this as real progress' });
    const original = Storage.prototype.setItem;
    const keys = ['critz-tycoon.save.v1', 'critz-tycoon.save.v1.backup', 'critz-tycoon.save.v1.pre-grid', 'critz-tycoon.save.v1.pre-grid.backup', 'comparison-qa-sentinel'];
    keys.forEach(key => original.call(localStorage, key, sentinel));
    window.__qaStorageBaseline = JSON.stringify(Object.fromEntries(keys.map(key => [key, localStorage.getItem(key)])));
    window.__qaStorageWrites = [];
    for (const method of ['setItem', 'removeItem', 'clear']) {
      const implementation = Storage.prototype[method];
      Storage.prototype[method] = function(...args) { window.__qaStorageWrites.push({ method, args }); return implementation.apply(this, args); };
    }
  });
  return ctx;
}
async function snapshot(page) { return page.evaluate(async () => (await import('./budgets.js')).getComparisonSnapshot()); }
async function until(page, predicate, label, timeout = 7000) {
  const expires = Date.now() + timeout;
  let last;
  while (Date.now() < expires) { last = await snapshot(page); if (predicate(last)) return last; await sleep(15); }
  throw new Error(`${label}: ${JSON.stringify(last)}`);
}
async function pause(page) { if ((await snapshot(page)).running) await page.locator('#play').click(); return until(page, s => !s.running, 'pause'); }
async function manualReset(page) {
  await pause(page);
  if ((await snapshot(page)).auto) await page.locator('#auto').click();
  await page.locator('#reset').click();
}
function matchingFrames(s) {
  assert.equal(s.frameIds.length, 2);
  assert.deepEqual(s.frameIds, [16, 24].map(b => `compare.${s.role}.${b}.${s.motion.facing}.${s.motion.pose}`));
  assert.ok(Number.isInteger(s.motion.x) && Number.isInteger(s.motion.y));
}
async function storageUntouched(page) {
  const data = await page.evaluate(() => ({ writes: window.__qaStorageWrites, before: window.__qaStorageBaseline, after: JSON.stringify(Object.fromEntries(Object.keys(JSON.parse(window.__qaStorageBaseline)).map(key => [key, localStorage.getItem(key)]))) }));
  assert.deepEqual(data.writes, []); assert.equal(data.after, data.before); return { syntheticSaveKeys: 5, writes: 0 };
}
async function screenshot(page, name) { const target = path.join(output, name); await page.screenshot({ path: target, fullPage: true }); report.screenshots.push(target); return target; }

try {
  const ctx = await context({ reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  const pageErrors = [], requests = [];
  page.on('pageerror', error => pageErrors.push(error.message));
  page.on('request', request => requests.push({ method: request.method(), url: request.url() }));
  await page.goto(base, { waitUntil: 'networkidle' });
  await until(page, s => s.ready, 'ready');

  await check('all requested characters and both budgets are available', async () => {
    const roles = await page.locator('[data-character]').evaluateAll(nodes => nodes.map(n => n.dataset.character));
    assert.deepEqual([...roles].sort(), [...expectedRoles].sort());
    for (const role of roles) { await page.locator(`[data-character="${role}"]`).click(); const s = await snapshot(page); assert.equal(s.role, role); matchingFrames(s); }
    return { roles };
  });
  await check('reduced motion begins paused with no simulation advancement', async () => {
    const a = await snapshot(page); assert.equal(a.running, false); await sleep(180); const b = await snapshot(page); assert.equal(b.tick, a.tick); return { initialTick: a.tick };
  });
  await check('pause and a single fixed-tick step', async () => {
    await pause(page); const before = await snapshot(page);
    await page.locator('#step').click(); const after = await snapshot(page);
    assert.equal(after.tick, before.tick + 1); assert.equal(after.motion.tick, before.motion.tick + 1); assert.equal(after.running, false); matchingFrames(after);
    await sleep(130); assert.equal((await snapshot(page)).tick, after.tick); return { before: before.tick, after: after.tick };
  });
  await check('auto loop covers all four directions and idle plus both alternating strides in shared phase', async () => {
    await page.locator('#reset').click(); if (!(await snapshot(page)).auto) await page.locator('#auto').click();
    await page.locator('#play').click();
    const directions = new Set(), poses = new Set(); const samples = []; const expires = Date.now() + 8500;
    while (Date.now() < expires && (directions.size < 4 || poses.size < 3)) {
      const s = await snapshot(page); matchingFrames(s); directions.add(s.motion.facing); poses.add(s.motion.pose); samples.push({ tick: s.tick, facing: s.motion.facing, pose: s.motion.pose, x: s.motion.x, y: s.motion.y }); await sleep(20);
    }
    await pause(page); assert.deepEqual([...directions].sort(), ['down','left','right','up']); assert.deepEqual([...poses].sort(), ['idle','strideA','strideB']);
    return { directions: [...directions], poses: [...poses], sampleCount: samples.length, first: samples[0], last: samples.at(-1) };
  });
  await check('keyboard release completes a committed tile, then stops', async () => {
    await manualReset(page); await page.keyboard.down('ArrowDown');
    const inFlight = await until(page, s => s.motion.action === 'walk' && s.motion.actionTick > 0 && s.motion.actionTick < 12, 'walking within tile');
    assert.equal(inFlight.motion.tileY, 7); await page.keyboard.up('ArrowDown');
    const end = await until(page, s => s.motion.action === 'idle' && s.motion.settled, 'idle after release');
    assert.equal(end.motion.x, 128); assert.equal(end.motion.y, 128); assert.equal(end.motion.tileY, 8); assert.equal(end.auto, false);
    await sleep(350); assert.equal((await snapshot(page)).motion.y, 128); await pause(page); return { from: [8,7], destination: [8,8] };
  });
  await check('pointer cancellation clears held input', async () => {
    await manualReset(page); const button = page.locator('[data-dir="down"]'); const box = await button.boundingBox();
    await page.mouse.move(box.x + box.width/2, box.y + box.height/2); await page.mouse.down();
    await until(page, s => s.motion.action === 'walk' && s.motion.actionTick < 12, 'pointer walking');
    await button.dispatchEvent('pointercancel', { pointerId: 1, pointerType: 'mouse', bubbles: true }); await page.mouse.up();
    const stop = await until(page, s => s.motion.action === 'idle', 'pointer canceled and settled');
    assert.equal(await page.locator('.held').count(), 0); await sleep(400); const later = await snapshot(page); assert.equal(later.motion.x, stop.motion.x); assert.equal(later.motion.y, stop.motion.y); await pause(page);
    return { stoppedAt: [stop.motion.x, stop.motion.y] };
  });
  await check('window blur clears held keyboard input', async () => {
    await manualReset(page); await page.keyboard.down('ArrowDown'); await until(page, s => s.motion.action === 'walk' && s.motion.actionTick < 12, 'keyboard walking');
    await page.evaluate(() => window.dispatchEvent(new Event('blur'))); await page.keyboard.up('ArrowDown');
    const stop = await until(page, s => s.motion.action === 'idle', 'blur settled'); await sleep(400); const later = await snapshot(page);
    assert.equal(later.motion.x, stop.motion.x); assert.equal(later.motion.y, stop.motion.y); await pause(page); return { stoppedAt: [stop.motion.x,stop.motion.y] };
  });
  await check('reset restores position and initial facing', async () => {
    await pause(page); await page.locator('#reset').click(); const s = await snapshot(page);
    assert.equal(s.motion.x,128); assert.equal(s.motion.y,112); assert.equal(s.motion.facing,'down'); assert.equal(s.motion.action,'idle'); assert.equal(s.motion.tick,0); return { position: [s.motion.x,s.motion.y] };
  });
  await check('frame guides change both canvases and are reversible', async () => {
    await pause(page); await page.locator('#guides').uncheck(); const before = await page.locator('.sprite-stage canvas').evaluateAll(cs => cs.map(c => c.toDataURL()));
    await page.locator('#guides').check(); assert.equal((await snapshot(page)).guides,true); const after = await page.locator('.sprite-stage canvas').evaluateAll(cs => cs.map(c => c.toDataURL()));
    assert.notEqual(before[0],after[0]); assert.notEqual(before[1],after[1]);
    await screenshot(page,'desktop-guides-1280x900.png'); await page.locator('#guides').uncheck(); const restored = await page.locator('.sprite-stage canvas').evaluateAll(cs => cs.map(c => c.toDataURL())); assert.deepEqual(restored,before);
  });
  for (const viewport of [{width:320,height:568},{width:390,height:844},{width:844,height:390},{width:1280,height:900}]) {
    await check(`integer canvas presentation and overflow containment at ${viewport.width}×${viewport.height}`, async () => {
      await page.setViewportSize(viewport); await sleep(90);
      const data = await page.evaluate(() => ({ bodyWidth: document.documentElement.scrollWidth, viewport: innerWidth,
        canvases: [...document.querySelectorAll('canvas')].map(c => ({ id:c.id, native:[c.width,c.height],display:[c.getBoundingClientRect().width,c.getBoundingClientRect().height],imageRendering:getComputedStyle(c).imageRendering })),
        stages: [...document.querySelectorAll('.room-stage')].map(s => ({ width:s.clientWidth,content:s.scrollWidth,scroll:s.scrollLeft })) }));
      assert.ok(data.bodyWidth <= data.viewport, `document overflows: ${JSON.stringify(data)}`);
      for (const c of data.canvases) { const sx = c.display[0]/c.native[0],sy=c.display[1]/c.native[1]; assert.equal(sx,sy); assert.ok(Number.isInteger(sx) && sx>=1, JSON.stringify(c)); assert.ok(['pixelated','crisp-edges'].includes(c.imageRendering)); }
      assert.equal(data.canvases[0].display[0],data.canvases[2].display[0]); assert.equal(data.canvases[1].display[0],data.canvases[3].display[0]);
      if (viewport.width < 480) {
        assert.ok(data.stages.every(s => s.content > s.width));
        await page.locator('.room-stage').first().evaluate(s => { s.scrollLeft = s.scrollWidth - s.clientWidth; }); await sleep(120);
        const s = await snapshot(page); assert.ok(Math.abs(s.scroll[0]-s.scroll[1])<=1, `scroll mismatch: ${s.scroll}`);
        await page.locator('.room-stage').last().evaluate(s => { s.scrollLeft = 0; }); await sleep(120);
        const reverse = await snapshot(page); assert.ok(reverse.scroll.every(x => x===0));
      }
      await screenshot(page,`comparison-${viewport.width}x${viewport.height}.png`); return data;
    });
  }
  for (const role of expectedRoles) {
    if (await page.locator(`[data-character="${role}"]`).count()) {
      await page.locator(`[data-character="${role}"]`).click(); await screenshot(page,`${role}-comparison-desktop.png`);
    }
  }
  await check('isolated synthetic saves are untouched and no game entrypoint or mutating request is used', async () => {
    const storage = await storageUntouched(page); assert.deepEqual(pageErrors,[]); assert.ok(requests.every(r => ['GET','HEAD'].includes(r.method)));
    assert.ok(!requests.some(r => /\/src\/(main|state|grid-save)\.js(?:$|\?)/.test(r.url))); return { ...storage, pageErrors, requestCount: requests.length };
  });
  await check('default motion preference starts playback', async () => {
    const normal = await context({reducedMotion:'no-preference'}); const p = await normal.newPage(); await p.goto(base,{waitUntil:'networkidle'}); const s = await until(p,x=>x.ready&&x.tick>0,'default autoplay'); assert.equal(s.running,true); await storageUntouched(p); return {tick:s.tick};
  });
  await check('artwork load failure is visible and controls stay disabled', async () => {
    const broken = await context({reducedMotion:'reduce'}); const p = await broken.newPage(); await p.route('**/assets/review/budget-comparison/atlas.json',route=>route.abort()); await p.goto(base,{waitUntil:'networkidle'});
    await p.locator('#error').waitFor({state:'visible'}); assert.match(await p.locator('#error').textContent(),/could not load/); assert.equal(await p.locator('button:not(:disabled),input:not(:disabled)').count(),0);
    assert.equal(await p.locator('#motion-status').textContent(),'Artwork unavailable.'); await storageUntouched(p); await screenshot(p,'load-failure.png'); return { message: await p.locator('#error').textContent() };
  });
} catch (error) { report.fatal = error.stack; console.error(error); }
finally { for (const ctx of contexts) await ctx.close(); await browser.close(); report.finishedAt = new Date().toISOString(); report.passed=report.checks.filter(c=>c.status==='pass').length;report.failed=report.checks.filter(c=>c.status==='fail').length; await writeFile(path.join(output,'browser-report.json'),JSON.stringify(report,null,2)+'\n'); }
if(report.fatal||report.failed) process.exitCode=1;
