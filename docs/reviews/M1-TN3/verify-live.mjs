import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const base='https://critz-tycoon.freemarketwildlife.chatgpt.site';
const proof=JSON.parse(await fs.readFile('/tmp/tn3-publication-build-proof.json','utf8'));
const commit='1ecda238d96013e71cfe4485624b2bf9d6cc7041';
const wanted=proof.files.filter(f=>f.path==='index.html'||f.path==='style.css'||f.path.startsWith('src/')||f.path.startsWith('map-editor/')&&/\.(js|css)$/.test(f.path)||/^art-review\/(coast|greenhouse|coast-complete|coast-review-art)\.(js|css)$/.test(f.path)||f.path.startsWith('assets/playable/tanoshi-outline/')||f.path.startsWith('assets/review/bench-r1/')||f.path.startsWith('assets/review/fence-r5/')||f.path.startsWith('assets/review/coastal-format/'));
const checks=[],errors=[];let next=0;
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
async function worker(){for(;;){const i=next++;if(i>=wanted.length)return;const f=wanted[i];let result;
 for(let attempt=0;attempt<3;attempt++){
  try{const r=await fetch(`${base}/${f.path}?tn3_source=${commit}`,{signal:AbortSignal.timeout(60000),headers:{'Cache-Control':'no-cache'}});assert.equal(r.status,200,f.path);const b=Buffer.from(await r.arrayBuffer());let exact=sha(b)===f.sha256,cloudflare=false;
   if(f.path==='index.html'&&!exact){const local=await fs.readFile('dist/index.html'),actual=b.toString();
    const expected=local.toString();
    // Require the entire authored page plus only one observed Cloudflare trailer.
    let at=0;while(at<expected.length&&expected[at]===actual[at])at++;
    at=expected.lastIndexOf('<',at);
    const prefix=expected.slice(0,at),suffix=expected.slice(at);
    const extra=actual.startsWith(prefix)&&actual.endsWith(suffix)?actual.slice(prefix.length,actual.length-suffix.length):'';
    cloudflare=extra.startsWith('<script>')&&extra.endsWith('</script>')&&extra.includes('/cdn-cgi/challenge-platform/')&&!extra.slice(8,-9).includes('</script>');
    exact=cloudflare;
   }
   assert.ok(exact,`${f.path} hash mismatch`);result={path:f.path,bytes:b.length,sha256:sha(b),expectedSHA256:f.sha256,exact:!cloudflare,authoredHTMLExactWithOnlyCloudflareTrailer:cloudflare||undefined};break;
  }catch(e){if(attempt===2)errors.push({path:f.path,message:e.message});else await new Promise(r=>setTimeout(r,1000));}
 }
 if(result)checks.push(result);
}}
await Promise.all(Array.from({length:6},worker));checks.sort((a,b)=>a.path.localeCompare(b.path));
await fs.writeFile('/tmp/tn3-live-source-hashes.json',JSON.stringify({sourceCommit:commit,url:base,checks,errors,scope:'All src modules, editor JS/CSS, relevant subview code, all TN3 native files and all published bench/fence/coastal native files.',checkedAtUTC:new Date().toISOString()},null,2)+'\n');
console.log(JSON.stringify({checked:checks.length,errors,exactFiles:checks.filter(c=>c.exact).length,cloudflareHTML:checks.filter(c=>c.authoredHTMLExactWithOnlyCloudflareTrailer).length}));assert.deepEqual(errors,[]);
