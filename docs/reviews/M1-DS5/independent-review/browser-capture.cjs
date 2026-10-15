const fs=require('fs');
const {chromium}=require('/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
  const dir='/tmp/ds5-browser-trace';fs.mkdirSync(dir,{recursive:true});
  const b=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
  const c=await b.newContext({viewport:{width:704,height:384},deviceScaleFactor:1});const p=await c.newPage();
  let html='<style>html,body{margin:0;background:#eee8d1}body{display:grid;grid-template-columns:352px 352px}img{display:block;width:352px;height:192px}</style>';
  for(const speed of ['normal','slow'])for(const dr of ['west','east']){
    const bytes=fs.readFileSync(__dirname+'/paired-'+dr+'-'+speed+'-INTERNAL.gif');
    html+='<img alt="'+dr+' '+speed+'" src="data:image/gif;base64,'+bytes.toString('base64')+'">';
  }
  await p.setContent(html);await p.locator('img').evaluateAll(es=>Promise.all(es.map(e=>e.decode())));
  for(let i=0;i<48;i++){await p.screenshot({path:dir+'/capture-'+i+'.png'});await p.waitForTimeout(83+(i*13)%41);}
  await b.close();console.log('48 actual isolated Chrome playback snapshots saved');
})().catch(e=>{console.error(e);process.exit(1)});
