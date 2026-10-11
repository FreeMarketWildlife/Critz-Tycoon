import {createRequire} from 'node:module';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {newProject,placeObject,exportProject,SAVE_KEY} from '../map-editor/model.js';
const require=createRequire(import.meta.url),{chromium}=require('/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const url=process.env.TEST_URL||'http://localhost:5180',out=process.env.TEST_OUTPUT_DIR||'test-results/me3',checks=[],errors=[];
await mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE||'/Users/tanoshi/Library/Caches/ms-playwright/chromium-1217/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'});
const context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage();
page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('favicon.ico'))errors.push(r.url());});
const pass=s=>{checks.push(s);console.log('PASS '+s);},inspect=()=>page.evaluate(async()=>(await import('/map-editor/editor.js')).inspect());
async function ready(){await page.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));}
async function fixture(p){await page.locator('#import').click();await page.locator('#data-text').fill(exportProject(p));await page.locator('#apply-import').click();await page.waitForSelector('#data-dialog',{state:'hidden'});}
async function step(key){await page.keyboard.down(key);await page.waitForTimeout(270);await page.keyboard.up(key);await page.waitForTimeout(330);}
try{
 await page.goto(url+'/map-editor/');await ready();
 await page.locator('#toolbox-search').fill('house');assert.ok(await page.locator('[data-stamp=cottage]').isVisible());assert.ok(await page.locator('[data-stamp=garden]').isVisible());assert.equal(await page.locator('[data-stamp=tree]').isVisible(),false);
 await page.locator('#toolbox-search').fill('ocean shallow');assert.ok(await page.locator('[data-brush=water-ocean-shallow-moving]').isVisible());assert.equal(await page.locator('[data-brush=water-fresh-still]').isVisible(),false);
 await page.locator('#toolbox-search').fill('no-such-unicorn');assert.match(await page.locator('#search-results').innerText(),/No matching/);
 await page.locator('#toolbox-search').fill('house roof');assert.ok(await page.locator('[data-tile]').count()>0);pass('Search finds houses, water and native modules across categories, and explains empty results');
 await page.locator('#toolbox-search').fill('');
 const p=newProject(),m=p.maps[0];placeObject(m,'cottage',2,2);m.spawn={x:4,y:7};await fixture(p);
 await page.locator('#validate').click();assert.match(await page.locator('#check-results').innerText(),/no linked doorway/);await page.locator('#check-dialog [data-close]').click();
 await page.locator('[data-mode=warp]').click();const s=await inspect(),box=await page.locator('#viewport').boundingBox();await page.mouse.click(box.x+s.ox+4.5*32*s.zoom,box.y+s.oy+6.5*32*s.zoom);
 await page.locator('#create-room').click();const linked=await inspect();assert.equal(linked.project.maps.length,2);assert.equal(linked.project.maps[1].warps[0].target,m.id);pass('Passage creates a real room and reciprocal exit in one action');
 await page.locator('#test').click();await page.keyboard.down('ArrowUp');await page.waitForTimeout(70);let current=await inspect();assert.equal(current.test.map,m.id);assert.equal(current.test.motion.action,'turn');await page.waitForTimeout(200);current=await inspect();assert.equal(current.test.map,m.id);assert.equal(current.test.motion.action,'walk');await page.screenshot({path:out+'/door-opening.png'});await page.keyboard.up('ArrowUp');await page.waitForTimeout(220);current=await inspect();assert.notEqual(current.test.map,m.id);assert.deepEqual([current.test.player.x,current.test.player.y],[5,7]);pass('Game movement turns, commits the entrance step, then travels to the room');
 await page.screenshot({path:out+'/room.png'});await step('ArrowDown');current=await inspect();assert.equal(current.test.map,m.id);assert.deepEqual([current.test.player.x,current.test.player.y],[4,7]);pass('Walking south through the room exit returns to the clear exterior approach');
 await page.locator('#exit-test').click();
 await page.evaluate(key=>localStorage.setItem(key,'draft-sentinel'),SAVE_KEY);await page.goto(url+'/map-editor/?review=me3');await ready();assert.equal(await page.evaluate(key=>localStorage.getItem(key),SAVE_KEY),'draft-sentinel');assert.equal((await inspect()).project.maps.length,4);await page.locator('#grid').uncheck();await page.screenshot({path:out+'/review-desktop.png'});await writeFile(out+'/review-native.png',Buffer.from((await page.locator('#map').evaluate(c=>c.toDataURL())).split(',')[1],'base64'));
 await page.locator('#export-png').click();pass('Dedicated building/ledge review retains the saved draft and exposes all three connected buildings');
 await page.locator('#test').click();await page.screenshot({path:out+'/review-walking.png'});await page.locator('#exit-test').click();assert.equal(await page.evaluate(key=>localStorage.getItem(key),SAVE_KEY),'draft-sentinel');pass('Review playtest does not save over the real map draft');
 const phone=await context.newPage();await phone.setViewportSize({width:390,height:844});await phone.goto(url+'/map-editor/?review=me3');await phone.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));assert.equal(await phone.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await phone.locator('#toolbox-search').fill('door');assert.ok(await phone.locator('[data-stamp=cottage]').isVisible());await phone.screenshot({path:out+'/review-phone.png',fullPage:true});await phone.locator('#test').click();await phone.screenshot({path:out+'/review-phone-walking.png'});pass('390px review and toolbox search fit the phone layout');await phone.close();
 assert.deepEqual(errors,[]);pass('No missing review assets or browser exceptions');
}finally{await writeFile(out+'/report.json',JSON.stringify({checks,errors},null,2)+'\n');await browser.close();}
