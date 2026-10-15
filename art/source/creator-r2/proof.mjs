import {readFileSync,writeFileSync} from 'node:fs';import {fileURLToPath} from 'node:url';import {compose,walkProject,holds} from '../../../character-creator/model.js';import {encodeGif} from '../../../character-creator/export.js';
const root=fileURLToPath(new URL('../../../',import.meta.url)),data=JSON.parse(readFileSync(root+'character-creator/data.json')),looks=JSON.parse(readFileSync(new URL('./review-looks.json',import.meta.url))),rendered=looks.map(look=>({...look,poses:Object.fromEntries(Object.keys(data.poses).map(d=>[d,Object.fromEntries(['idle','A','P','C'].map(p=>[p,compose(data,d,p,look.settings)]))]))}));
writeFileSync('/tmp/critz-cc1-renders.json',JSON.stringify(rendered));const expected=[];
for(const n of [2,3])for(const dr of Object.keys(data.poses)){
 const p=walkProject(data,dr,looks[n].settings);expected.push({look:n,direction:dr,palette:p.palette,frames:p.frames});
 for(const scale of [1,4]){const q=structuredClone(p);q.width*=scale;q.height*=scale;for(const f of q.frames){const original=f.pixels;f.pixels=Array.from({length:q.width*q.height},(_,i)=>original[Math.floor(Math.floor(i/q.width)/scale)*32+Math.floor((i%q.width)/scale)]);}writeFileSync(root+`docs/reviews/M1-CC1/look${n}-${dr}-walk-${scale}x.gif`,encodeGif(q,holds(dr)));}
}
writeFileSync('/tmp/critz-cc1-gif-expected.json',JSON.stringify(expected));console.log('Rendered six appearance combinations / all16poses and two look walks in all4directions.');
