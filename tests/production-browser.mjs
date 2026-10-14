// Sequential runner: one production server and one isolated browser suite at
// a time. Keeps snapshots/logs out of historical review directories.
import {spawn} from 'node:child_process';import {mkdir,writeFile} from 'node:fs/promises';import {join} from 'node:path';
const base=process.env.TEST_URL||'http://127.0.0.1:5221',out=process.env.TEST_OUTPUT_DIR||'test-results/production';
await mkdir(out,{recursive:true});
const suites=['technical-browser','editor-view-browser','browser','lifecycle-browser','screen-browser','home-care-browser','all-integration-browser','map-editor-browser','map-studio-r3-browser','map-studio-r4-browser','map-studio-r6-browser','map-studio-r7-browser','map-studio-r8-browser','fence-r5-browser','coastal-browser','coast-complete-browser','ui-browser','stairs-browser'];
const results=[];
for(const suite of suites){
 const directory=join(out,suite);await mkdir(directory,{recursive:true});const start=Date.now();
 const child=spawn(process.execPath,['tests/'+suite+'.mjs'],{env:{...process.env,TEST_URL:base,TEST_BASE:base,TEST_OUTPUT_DIR:directory,CODEX_PRIMARY_RUNTIME_NODE_MODULES:process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES||'/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules',CHROMIUM_EXECUTABLE:process.env.CHROMIUM_EXECUTABLE||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'},stdio:['ignore','pipe','pipe']});
 let output='';child.stdout.on('data',b=>output+=b);child.stderr.on('data',b=>output+=b);
 const exitCode=await new Promise(resolve=>{child.once('error',e=>{output+=e.stack;resolve(-1);});child.once('exit',resolve);});
 const result={suite,exitCode,ms:Date.now()-start,printedPassGroups:output.split('\n').filter(s=>s.startsWith('PASS ')).length};results.push(result);await writeFile(join(directory,'run.log'),output);console.log(JSON.stringify(result));
}
await writeFile(join(out,'suite-results.json'),JSON.stringify({url:base,results,allPassed:results.every(r=>r.exitCode===0)},null,2)+'\n');
if(results.some(r=>r.exitCode!==0))process.exitCode=1;
