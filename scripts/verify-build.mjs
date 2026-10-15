// Check every delivered file: JSON values are exact; all other bytes stay exact.
import assert from 'node:assert/strict';import {readFile,readdir,writeFile} from 'node:fs/promises';
import {join} from 'node:path';import {createHash} from 'node:crypto';
import {expandContactCatalogue} from '../src/contact-catalogue.js';
const result={exactFiles:0,equalAssetJson:0,generatedFiles:[],files:[]};
const hash=data=>createHash('sha256').update(data).digest('hex');
const ignored=name=>['__pycache__','node_modules','.DS_Store'].includes(name)||name.startsWith('._')||/\.py[cod]$/.test(name);
async function verify(path){
 const source=await readFile(path),built=await readFile('dist/'+path);
 if(path==='src/asset-urls.js'){
  assert.equal(built.toString(),"// Generated production asset URLs.\nexport const CONTACT_MANIFEST='../assets/playable/contact/runtime.json';\n");result.generatedFiles.push(path);
 }else if(/^(assets|docs|art)\//.test(path)&&path.endsWith('.json')){
  assert.deepEqual(JSON.parse(built),JSON.parse(source),path);result.equalAssetJson++;
 }else{assert.ok(source.equals(built),path+' differs from source');result.exactFiles++;}
 result.files.push({path,bytes:built.length,sha256:hash(built)});
}
async function walk(path){for(const entry of await readdir(path,{withFileTypes:true})){if(ignored(entry.name))continue;const p=join(path,entry.name);if(entry.isDirectory())await walk(p);else await verify(p);}}
for(const file of ['index.html','style.css','icon.svg'])await verify(file);
for(const dir of ['src','sprite-editor','map-editor','music','art-review','assets','docs','art'])await walk(dir);
const source=JSON.parse(await readFile('assets/playable/contact/atlas.json')),
 runtime=JSON.parse(await readFile('dist/assets/playable/contact/runtime.json')),
 catalogue=JSON.parse(await readFile('dist/assets/playable/contact/catalogue.json'));
assert.deepEqual({...runtime,...expandContactCatalogue(catalogue)},source);
for(const path of ['assets/playable/contact/runtime.json','assets/playable/contact/catalogue.json']){
 const bytes=await readFile('dist/'+path);result.generatedFiles.push(path);result.files.push({path,bytes:bytes.length,sha256:hash(bytes)});
}
const found=[];async function inventory(dir){for(const e of await readdir(dir,{withFileTypes:true})){const p=join(dir,e.name);if(e.isDirectory())await inventory(p);else found.push(p.slice(5));}}await inventory('dist');
assert.deepEqual(found.sort(),result.files.map(f=>f.path).sort(),'Unexpected or missing package files');
result.files.sort((a,b)=>a.path.localeCompare(b.path));result.packageFingerprint=hash(JSON.stringify(result.files));
result.protectedHeroSHA256=hash(await readFile('assets/characters/hero-boy-v1/idle-south.png'));
if(process.env.TEST_BUILD_PROOF)await writeFile(process.env.TEST_BUILD_PROOF,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({exactFiles:result.exactFiles,equalAssetJson:result.equalAssetJson,generatedFiles:result.generatedFiles,packageFingerprint:result.packageFingerprint,protectedHeroSHA256:result.protectedHeroSHA256},null,2));
