import {coastalWaterPixel,CONTACT_RULE} from '../../../src/coastal-geometry.js';import {WATER_MASKS} from '../../../src/water-surfaces.js';
console.log(JSON.stringify({contactRule:CONTACT_RULE,masks:Object.fromEntries(WATER_MASKS.map(m=>[m,Buffer.from(Array.from({length:2048},(_,i)=>coastalWaterPixel(i%32,Math.floor(i/32),m)?1:0)).toString('base64')]))}));
