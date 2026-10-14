import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,mkdtemp,mkdir,writeFile,rm} from 'node:fs/promises';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {splitContactManifest,expandContactCatalogue,prepareAssetDelivery} from '../scripts/asset-delivery.mjs';

test('Delivered contact metadata restores every authored assembly, tile and B rule exactly',async()=>{
 const source=JSON.parse(await readFile('assets/playable/contact/atlas.json','utf8'));
 const {runtime,catalogue}=splitContactManifest(source);
 assert.deepEqual({...runtime,...expandContactCatalogue(JSON.parse(JSON.stringify(catalogue)))},source);
 assert.equal(runtime.tiles,undefined);assert.equal(runtime.assemblies,undefined);
 assert.ok(Buffer.byteLength(JSON.stringify(runtime))<350000);
 assert.ok(Buffer.byteLength(JSON.stringify(catalogue))<800000);
 const special=structuredClone(source);special.tiles[0].contact={...special.rule,id:'special'};
 const parts=splitContactManifest(special);assert.deepEqual({...parts.runtime,...expandContactCatalogue(parts.catalogue)},special);
});

test('Build delivery preserves nested JSON values, PNG bytes and authored sources',async()=>{
 const root=await mkdtemp(join(tmpdir(),'critz-delivery-'));
 try{
  await mkdir(join(root,'playable/contact'),{recursive:true});await mkdir(join(root,'nested'));
  const source=await readFile('assets/playable/contact/atlas.json');await writeFile(join(root,'playable/contact/atlas.json'),source);
  const values={label:'Luke’s world',alpha:0,blank:null,keys:['\n','π'],obj:{order:true}};
  await writeFile(join(root,'nested/manifest.json'),JSON.stringify(values,null,2));
  const png=Buffer.from([137,80,78,71,0,255,13,10]);await writeFile(join(root,'nested/image.png'),png);
  await prepareAssetDelivery(root);
  assert.deepEqual(JSON.parse(await readFile(join(root,'playable/contact/atlas.json'))),JSON.parse(source));
  const runtime=JSON.parse(await readFile(join(root,'playable/contact/runtime.json'))),catalogue=JSON.parse(await readFile(join(root,'playable/contact/catalogue.json')));
  assert.deepEqual({...runtime,...expandContactCatalogue(catalogue)},JSON.parse(source));
  assert.deepEqual(JSON.parse(await readFile(join(root,'nested/manifest.json'))),values);
  assert.deepEqual(await readFile(join(root,'nested/image.png')),png);
  assert.deepEqual(await readFile('assets/playable/contact/atlas.json'),source);
 }finally{await rm(root,{recursive:true,force:true});}
});
