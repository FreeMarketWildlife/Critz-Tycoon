// Build-only delivery transforms. Authored manifests and every PNG stay exact.
import {readdir,readFile,writeFile} from 'node:fs/promises';
import {join} from 'node:path';
export {expandContactCatalogue} from '../src/contact-catalogue.js';

export function splitContactManifest(source) {
  const {tiles,assemblies,...runtime}=source;
  const rule=JSON.stringify(source.rule);
  const catalogue={schemaVersion:1,rule:source.rule,assemblies,
    tiles:tiles.map(tile=>JSON.stringify(tile.contact)===rule?{...tile,contact:1}:tile)};
  return {runtime,catalogue};
}

export async function prepareAssetDelivery(root) {
  const contact=join(root,'playable/contact/atlas.json');
  const {runtime,catalogue}=splitContactManifest(JSON.parse(await readFile(contact,'utf8')));
  await writeFile(join(root,'playable/contact/runtime.json'),JSON.stringify(runtime));
  await writeFile(join(root,'playable/contact/catalogue.json'),JSON.stringify(catalogue));
  let files=0,beforeBytes=0,afterBytes=0;
  async function compact(directory) {
    for(const entry of await readdir(directory,{withFileTypes:true})){
      const path=join(directory,entry.name);
      if(entry.isDirectory())await compact(path);
      else if(entry.name.endsWith('.json')){
        const source=await readFile(path,'utf8'),result=JSON.stringify(JSON.parse(source));
        beforeBytes+=Buffer.byteLength(source);afterBytes+=Buffer.byteLength(result);files++;
        await writeFile(path,result);
      }
    }
  }
  await compact(root);return {files,beforeBytes,afterBytes};
}
