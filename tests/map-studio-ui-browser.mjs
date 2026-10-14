import {createRequire} from 'node:module';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {importProject} from '../map-editor/model.js';
const require=createRequire(import.meta.url);
const {chromium}=require((process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES||'/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules')+'/playwright');
const url=process.env.TEST_URL||'http://localhost:5240',out=process.env.TEST_OUTPUT_DIR||'docs/reviews/M1-ME10';
await mkdir(out,{recursive:true});
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const context=await browser.newContext({viewport:{width:1440,height:960}}),page=await context.newPage(),checks=[],errors=[];
page.on('pageerror',e=>errors.push(e.message));
const ready=()=>page.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));
const inspect=()=>page.evaluate(async()=>(await import('/map-editor/editor.js')).inspect());
const pass=s=>{checks.push(s);console.log('PASS '+s);};
async function cell(x,y){const s=await inspect(),b=await page.locator('#viewport').boundingBox();return {x:b.x+s.ox+(x+.5)*32*s.zoom,y:b.y+s.oy+(y+.5)*32*s.zoom};}
try{
 await page.goto(url+'/map-editor/?area=rootport');await ready();
 const expected=importProject(await readFile(new URL('../map-editor/areas/rootport.json',import.meta.url),'utf8'));
 assert.deepEqual((await inspect()).project,expected);
 const desktop=await page.locator('#viewport').boundingBox();assert.ok(desktop.width>=1100&&desktop.height>=700);
 await page.screenshot({path:out+'/desktop.png'});pass('Rootport opens unchanged with a1152×706 desktop canvas');
 await page.locator('#close-build').click();assert.equal(await page.locator('#open-build').getAttribute('aria-expanded'),'false');assert.ok((await page.locator('#viewport').boundingBox()).width>desktop.width);await page.locator('#open-build').click();pass('Toolbox collapses and reopens without changing the project');
 await page.locator('#toolbox-search').fill('water');assert.equal(await page.locator('#water-group').getAttribute('open'),'');assert.ok(await page.locator('[data-brush=water]').isVisible());await page.locator('[data-brush=water]').click();await page.locator('#toolbox-search').fill('');assert.equal(await page.locator('#water-group').getAttribute('open'),null);pass('Global search reveals collapsed water tools and restores category state');
 await page.locator('#viewport').focus();await page.keyboard.press('b');let c=await cell(18,13);await page.mouse.click(c.x,c.y);assert.equal((await inspect()).project.maps[0].terrain[13*22+18],'water');await page.locator('#undo').click();assert.deepEqual((await inspect()).project,expected);await page.locator('#redo').click();assert.equal((await inspect()).project.maps[0].terrain[13*22+18],'water');await page.locator('#undo').click();pass('Actual pointer paint, undo and redo retain exact Rootport content');
 await page.locator('#more-tools summary').click();await page.locator('[data-mode=warp]').click();assert.equal((await inspect()).mode,'warp');assert.equal(await page.locator('#viewport').evaluate(e=>e===document.activeElement),true);await page.locator('#viewport').focus();for(const [key,mode] of [['r','rectangle'],['f','fill'],['e','erase'],['s','select'],['h','pan'],['i','eyedropper'],['b','paint']]){await page.keyboard.press(key);assert.equal((await inspect()).mode,mode);}
 await page.keyboard.press('Enter');assert.equal((await inspect()).project.maps[0].terrain[13*22+18],'water');await page.keyboard.press('Control+z');assert.deepEqual((await inspect()).project,expected);pass('Canvas keyboard tools and Enter painting work with the desktop palette open');
 await page.locator('#tab-terrain').focus();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('#tab-stamps').getAttribute('aria-selected'),'true');assert.equal(await page.locator('#tab-terrain').getAttribute('tabindex'),'-1');await page.locator('#tab-terrain').click();pass('Palette tabs support arrow navigation and roving focus');
 await page.locator('.view-options summary').click();await page.locator('#collision').check();await page.locator('#edit-layer').selectOption('features');assert.equal((await inspect()).editLayer,'features');await page.locator('#collision').uncheck();await page.locator('#edit-layer').selectOption('auto');await page.locator('.view-options summary').click();pass('View options retain collision and explicit layer controls');
 await page.locator('#focus-mode').click();assert.equal(await page.locator('.tool-bar').isVisible(),false);assert.equal(await page.locator('#build-drawer').isVisible(),false);await page.locator('#focus-mode').click();assert.equal(await page.locator('.tool-bar').isVisible(),true);pass('Focus mode reclaims canvas space and reverses cleanly');
 await page.locator('#project-panel').click();await page.locator('#project-copy').click();assert.equal(await page.locator('#project-drawer').isVisible(),false);assert.equal(await page.locator('#data-dialog').isVisible(),true);assert.equal(JSON.parse(await page.locator('#data-text').inputValue()).name,'Rootport');await page.locator('#data-dialog [data-close]').click();pass('Project share opens a single export dialog with full editable data');
 await page.locator('#project-panel').click();const download=page.waitForEvent('download');await page.locator('#download').click();assert.equal((await download).suggestedFilename(),'critz-world.json');pass('Project backup download works from the drawer');
 await page.locator('#test').click();await page.waitForSelector('#test-dialog[open]');assert.ok((await inspect()).test);await page.locator('#exit-test').click();assert.deepEqual((await inspect()).project,expected);pass('Quick Hero test returns to the same authored map');
 await page.locator('#help').click();await page.keyboard.press('Escape');assert.equal(await page.locator('#help-dialog').isVisible(),false);pass('Help is discoverable and dismisses with Escape');
 for(const size of [{width:390,height:844},{width:320,height:640},{width:844,height:390},{width:1024,height:768}]){
  await page.setViewportSize(size);await page.locator('#fit').click();assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth&&document.documentElement.scrollHeight<=innerHeight),true);
  const v=await page.locator('#viewport').boundingBox();assert.ok(v.width>250&&v.height>100);if(size.height<=500)assert.ok(v.width>=800&&v.height>=190,'Short landscape keeps a useful canvas');
  if(size.width<=760||(size.height<=500&&size.width<=1100)){
   assert.equal(await page.locator('#build-drawer').isVisible(),false);await page.locator('#open-build').click();assert.equal(await page.locator('#build-drawer').evaluate(d=>d.matches(':modal')),true);
   await page.locator('#toolbox-search').fill('bench');assert.equal(await page.locator('[data-stamp]:visible').count(),4);await page.screenshot({path:out+'/build-'+size.width+'.png'});await page.locator('[data-stamp=bench]').click();assert.equal(await page.locator('#build-drawer').isVisible(),false);assert.equal((await inspect()).stamp,'bench');
   await page.locator('#project-panel').click();await page.locator('#project-copy').click();assert.equal(await page.locator('#data-dialog').isVisible(),true);await page.locator('#data-dialog [data-close]').click();
  }
  await page.screenshot({path:out+'/viewport-'+size.width+'x'+size.height+'.png'});
 }
 pass('320/390px phone, short landscape and tablet fit; modal Build returns selected props to canvas');
 // A true touch context exercises tray selection and map placement, without real user storage.
 const touch=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true}),p=await touch.newPage();p.on('pageerror',e=>errors.push(e.message));await p.goto(url+'/map-editor/?area=rootport');await p.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Ready.'));await p.locator('#open-build').tap();await p.locator('#toolbox-search').fill('flowers');await p.locator('[data-brush=flowers]').tap();const st=await p.evaluate(async()=>(await import('/map-editor/editor.js')).inspect()),vb=await p.locator('#viewport').boundingBox();await p.touchscreen.tap(vb.x+st.ox+18.5*32*st.zoom,vb.y+st.oy+13.5*32*st.zoom);assert.equal((await p.evaluate(async()=>(await import('/map-editor/editor.js')).inspect())).project.maps[0].features[13*22+18],'flowers');await p.screenshot({path:out+'/phone-touch.png'});await touch.close();pass('Actual touch selection paints the intended cell after the tray closes');
 assert.deepEqual(errors,[]);pass('No browser exceptions');
}finally{await writeFile(out+'/ui-checks.json',JSON.stringify({url,checks,errors},null,2)+'\n');await browser.close();}
