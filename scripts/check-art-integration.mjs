// Static art review QA. Fresh Playwright contexts only; never uses a personal profile.
// Build first, serve dist, then run with BASE_URL (default http://localhost:5173).
import { createRequire } from 'node:module';
import { readFile, writeFile, mkdir, mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require((process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES || '/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules') + '/playwright')); }
const base = process.env.BASE_URL || 'http://localhost:5173';
const output = 'docs/reviews/M1-I1';
const report = {
  task: 'M1.I1 static art integration review',
  scope: 'Appearance review only; no movement, animation, full-game integration or user approval claimed.',
  url: base + '/art-review/integration.html',
  testedAt: new Date().toISOString(),
  isolatedBrowserContext: true,
  realBrowserProfileAccessed: false,
  checks: [], pageErrors: [], failures: [], viewports: [], screenshots: [],
  limitations: ['Desktop Chromium emulation, not physical phone Safari.', 'Visual style approval remains with the user.'],
};
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
async function check(name, action) {
  try { const detail = await action(); report.checks.push({ name, pass: true, ...(detail === undefined ? {} : { detail }) }); console.log('PASS ' + name); }
  catch (error) { report.checks.push({ name, pass: false, error: error.message }); report.failures.push(name + ': ' + error.message); console.error('FAIL ' + name + ': ' + error.message); }
}
const temp = await mkdtemp(join(tmpdir(), 'critz-art-integration-'));
let browser;
try {
  await mkdir(output, { recursive: true });
  browser = await chromium.launch({ executablePath: process.env.CHROMIUM_EXECUTABLE || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', args: ['--no-sandbox'] });
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, acceptDownloads: true });
  await context.addInitScript(() => {
    localStorage.setItem('critz-integration-test-sentinel', 'synthetic-only');
    sessionStorage.setItem('critz-integration-session-sentinel', 'synthetic-only');
  });
  const page = await context.newPage();
  page.on('pageerror', error => report.pageErrors.push(error.message));
  await page.goto(report.url);
  await page.waitForFunction(() => document.documentElement.dataset.artReady === 'true');
  await check('Served integration files equal the built dist files', async () => {
    const files = ['art-review/integration.html', 'art-review/integration.js', 'art-review/integration.css', 'src/atlas.js', 'assets/review/integration-v1/atlas.png', 'assets/review/integration-v1/atlas.json'];
    const hashes = {};
    for (const path of files) {
      const response = await context.request.get(base + '/' + path);
      assert.equal(response.status(), 200, path);
      const bytes = await response.body();
      assert.equal(sha(bytes), sha(await readFile('dist/' + path)), path);
      hashes[path] = sha(bytes);
    }
    report.testedArtifactSha256 = hashes;
  });
  await check('All 23 atlas entries and ten candidate previews preserve source pixels', async () => {
    const results = await page.evaluate(async () => {
      const manifest = await (await fetch('../assets/review/integration-v1/atlas.json')).json();
      const load = async path => { const image = new Image(); image.src = path; await image.decode(); return image; };
      const atlas = await load('../assets/review/integration-v1/atlas.png');
      const pixels = (image, rect) => {
        const canvas = document.createElement('canvas'); canvas.width = rect[2]; canvas.height = rect[3];
        const context = canvas.getContext('2d'); context.drawImage(image, ...rect, 0, 0, rect[2], rect[3]);
        return context.getImageData(0, 0, rect[2], rect[3]).data;
      };
      return Promise.all(manifest.assets.map(async entry => {
        const source = await load('../assets/review/' + entry.source);
        const original = pixels(source, entry.sourceRect || [0, 0, source.width, source.height]);
        const packed = pixels(atlas, entry.rect);
        const preview = entry.candidate ? document.querySelector(`[data-id="${entry.id}"] canvas`).getContext('2d').getImageData(0, 0, 16, 32).data : null;
        return { id: entry.id, sourceMatches: original.length === packed.length && original.every((v, i) => v === packed[i]), previewMatches: !preview || preview.every((v, i) => v === packed[i]) };
      }));
    });
    assert.equal(results.length, 23);
    assert.equal(await page.locator('.candidate').count(), 10);
    assert.ok(results.every(entry => entry.sourceMatches && entry.previewMatches), JSON.stringify(results.filter(entry => !entry.sourceMatches || !entry.previewMatches)));
    return results;
  });
  await check('Every candidate updates the selected state, description and scene', async () => {
    const states = new Set();
    for (const button of await page.locator('.candidate').all()) {
      await button.click();
      const label = await button.locator('span').innerText();
      assert.equal(await button.getAttribute('aria-pressed'), 'true');
      assert.equal(await page.locator('.candidate[aria-pressed="true"]').count(), 1);
      assert.ok((await page.locator('#description').innerText()).startsWith(label + ' · '));
      states.add(await page.locator('#scene').evaluate(canvas => canvas.toDataURL()));
    }
    assert.equal(states.size, 10);
  });
  await page.locator('.candidate').first().click();
  await check('Static placement preserves source pixels and tree canopy covers overlapping character pixels', async () => {
    const counts = {};
    for (const placement of ['door', 'beside', 'behind']) {
      await page.locator('#position').selectOption(placement);
      counts[placement] = await page.evaluate(async placement => {
        const manifest = await (await fetch('../assets/review/integration-v1/atlas.json')).json();
        const selected = manifest.assets.find(entry => entry.id === document.querySelector('.candidate[aria-pressed="true"]').dataset.id);
        const tree = manifest.assets.find(entry => entry.id === 'tree.clustered');
        const image = new Image(); image.src = '../assets/review/integration-v1/atlas.png'; await image.decode();
        const canvas = document.createElement('canvas'); canvas.width = image.width; canvas.height = image.height;
        const context = canvas.getContext('2d'); context.drawImage(image, 0, 0);
        const character = context.getImageData(...selected.rect).data;
        const foliage = context.getImageData(...tree.rect).data;
        const scene = document.querySelector('#scene').getContext('2d').getImageData(0, 0, 240, 160).data;
        const anchor = { door: [96,128], beside: [64,112], behind: [40,96] }[placement];
        const result = { visible: 0, occluded: 0, mismatches: 0 };
        for (let y = 0; y < 32; y++) for (let x = 0; x < 16; x++) {
          const ci = (y * 16 + x) * 4; if (!character[ci + 3]) continue;
          const sx = anchor[0] - 8 + x, sy = anchor[1] - 32 + y, si = (sy * 240 + sx) * 4;
          const tx = sx - 24, ty = sy - 80, ti = (ty * 32 + tx) * 4;
          const covered = placement === 'behind' && tx >= 0 && tx < 32 && ty >= 0 && ty < 32 && foliage[ti + 3] === 255;
          const expected = covered ? foliage : character, start = covered ? ti : ci;
          result[covered ? 'occluded' : 'visible']++;
          if ([0,1,2,3].some(channel => scene[si + channel] !== expected[start + channel])) result.mismatches++;
        }
        return result;
      }, placement);
      assert.equal(counts[placement].mismatches, 0, placement);
      assert.ok(counts[placement].visible > 0, placement);
    }
    assert.ok(counts.behind.occluded > 0);
    return counts;
  });
  await check('Grid toggles visible pixels and reversibly restores the original scene', async () => {
    const before = await page.locator('#scene').evaluate(canvas => canvas.toDataURL());
    await page.locator('#grid').check();
    assert.notEqual(await page.locator('#scene').evaluate(canvas => canvas.toDataURL()), before);
    await page.locator('#grid').uncheck();
    assert.equal(await page.locator('#scene').evaluate(canvas => canvas.toDataURL()), before);
  });
  await check('PNG download is byte-identical to the atlas', async () => {
    const pending = page.waitForEvent('download');
    await page.getByRole('link', { name: 'Download the PNG' }).click();
    const download = await pending;
    assert.equal(download.suggestedFilename(), 'critz-review-atlas.png');
    await download.saveAs(join(temp, 'atlas.png'));
    assert.equal(sha(await readFile(join(temp, 'atlas.png'))), sha(await readFile('dist/assets/review/integration-v1/atlas.png')));
  });
  await page.locator('#position').selectOption('door');
  for (const viewport of [{ width:320,height:568 }, { width:390,height:844 }, { width:844,height:390 }, { width:1280,height:900 }]) {
    await page.setViewportSize(viewport);
    await page.waitForTimeout(100);
    const metrics = await page.evaluate(() => {
      const canvas = document.querySelector('#scene'), bounds = canvas.getBoundingClientRect();
      const controls = [...document.querySelectorAll('button, select, label.check, a')].map(element => {
        const box = element.getBoundingClientRect();
        return { label: element.getAttribute('aria-label') || element.textContent.trim(), tag: element.tagName, width: box.width, height: box.height };
      });
      return { pageOverflow: document.documentElement.scrollWidth > innerWidth, scale: bounds.width / canvas.width, sceneClipped: bounds.width > document.querySelector('#scene-container').clientWidth, controls };
    });
    report.viewports.push({ ...viewport, ...metrics });
    await check(`No overflow or scene clipping at ${viewport.width}×${viewport.height}; integer native scaling`, () => {
      assert.equal(metrics.pageOverflow, false); assert.equal(metrics.sceneClipped, false); assert.ok(Number.isInteger(metrics.scale));
    });
    await check(`All controls and links have 44px targets at ${viewport.width}×${viewport.height}`, () => {
      const small = metrics.controls.filter(control => control.width < 44 || control.height < 44);
      assert.deepEqual(small, []);
    });
    const path = `${output}/integration-${viewport.width}x${viewport.height}.png`;
    await page.screenshot({ path, fullPage: true }); report.screenshots.push(path);
  }
  await check('Missing animation and pending review are explicitly labeled; scene remains static', async () => {
    const text = await page.locator('body').innerText();
    assert.match(text, /Side, back, walk and run poses/);
    assert.match(text, /Mom, Kaid and Professor Nugget/);
    assert.match(text, /front-facing idle poses/);
    assert.match(text, /Art approval and a separate tile-movement proof are still pending/);
    assert.match(text, /static scale and layering check, not a movement demo/);
    const before = await page.locator('#scene').evaluate(canvas => canvas.toDataURL());
    await page.waitForTimeout(250);
    assert.equal(await page.locator('#scene').evaluate(canvas => canvas.toDataURL()), before);
  });
  await check('Synthetic local and session storage remain unchanged', async () => {
    assert.deepEqual(await page.evaluate(() => ({ local: { ...localStorage }, session: { ...sessionStorage } })), { local: { 'critz-integration-test-sentinel': 'synthetic-only' }, session: { 'critz-integration-session-sentinel': 'synthetic-only' } });
  });
  await context.close();
  await check('Missing atlas shows an error, disables controls and causes no uncaught exception', async () => {
    const failureContext = await browser.newContext();
    await failureContext.route('**/assets/review/integration-v1/atlas.png', route => route.abort('failed'));
    const failurePage = await failureContext.newPage();
    failurePage.on('pageerror', error => report.pageErrors.push(error.message));
    await failurePage.goto(report.url);
    await failurePage.waitForSelector('#status.error');
    assert.match(await failurePage.locator('#status').innerText(), /could not load.*Reload to try again/);
    assert.equal(await failurePage.locator('#position').isDisabled(), true);
    assert.equal(await failurePage.locator('#grid').isDisabled(), true);
    assert.equal(await failurePage.locator('#description').innerText(), 'Artwork unavailable.');
    assert.equal(await failurePage.locator('.candidate').count(), 0);
    const path = `${output}/integration-missing-atlas.png`;
    await failurePage.screenshot({ path, fullPage: true }); report.screenshots.push(path);
    await failureContext.close();
  });
  await check('Zero uncaught page errors', () => assert.deepEqual(report.pageErrors, []));
} catch (error) {
  report.failures.push(error.stack || error.message);
} finally {
  if (browser) await browser.close();
  await rm(temp, { recursive: true, force: true });
  report.pass = report.failures.length === 0;
  report.passedChecks = report.checks.filter(check => check.pass).length;
  report.totalChecks = report.checks.length;
  await mkdir('docs/verification', { recursive: true });
  await writeFile('docs/verification/ART_INTEGRATION.json', JSON.stringify(report, null, 2) + '\n');
  if (!report.pass) process.exitCode = 1;
}
