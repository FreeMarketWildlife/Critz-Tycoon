import fs from 'node:fs';import path from 'node:path';
import {out,repo,hash} from './pixels.mjs';import {makeCharacters} from './characters.mjs';import {makeCritters} from './critters.mjs';import {makeHabitats} from './habitats.mjs';
const baseline=JSON.parse(fs.readFileSync(path.join(repo,'assets/review/idle-collection-v1/manifest.json')));
for(const a of baseline.assets){if(hash(fs.readFileSync(path.join(repo,'assets/review/idle-collection-v1',a.file)))!==a.pngSHA256)throw Error('Idle baseline changed: '+a.slug);}
if(hash(fs.readFileSync(path.join(repo,'assets/characters/hero-boy-v1/idle-south.png')))!=='0099dd331ae2c2d995663328e52763e8b10b1df0d36854d59676ee0ac52f7883')throw Error('Approved boy changed');
fs.mkdirSync(out,{recursive:true});
const characters=await makeCharacters();console.log('12 characters: four directions each.');
const {result:critters,rasters}=await makeCritters();console.log('10 critters: species-specific motion.');
const habitats=await makeHabitats(rasters);console.log('3 animated habitats, layers and world props.');
fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify({schemaVersion:1,id:'critz.living-collection.v1',task:'M1.C7',status:'awaiting-user-motion-and-habitat-review',runtimeIntegrated:false,characters,critters,habitats},null,2)+'\n');
