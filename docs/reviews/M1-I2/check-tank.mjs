// Run with node; CRITZ_CANVAS_MODULE may point to a bundled canvas module.
const { createCanvas } = await import(process.env.CRITZ_CANVAS_MODULE || '@napi-rs/canvas');
import { writeFile } from 'node:fs/promises';
import { renderTank } from '../../../src/tank-render.js';
globalThis.document = {createElement: () => createCanvas(1,1)};
const t={plants:5,food:70,hide:true,isopods:12,springtails:24,algae:12,waste:18,moisture:65,stress:10};
const results=[];
const check=(name,pass)=>results.push({name,pass});
function snapshot(tank=t,time=12,camera={},width=400,height=200){const c=createCanvas(width,height);renderTank(c,tank,time,camera);return c;}
const raw=c=>Buffer.from(c.getContext('2d').getImageData(0,0,c.width,c.height).data);
const stateBefore=JSON.stringify(t),normal=snapshot();
check('no-tank-state-mutation',JSON.stringify(t)===stateBefore);
check('same-state-time-camera-deterministic',raw(normal).equals(raw(snapshot())));
check('all-output-opaque',raw(normal).every((v,i)=>i%4!==3||v===255));
check('exact-two-by-two-presentation',(()=>{const p=raw(normal);for(let y=0;y<200;y++)for(let x=0;x<400;x++)for(let k=0;k<4;k++)if(p[(y*400+x)*4+k]!==p[((y-y%2)*400+x-x%2)*4+k])return false;return true;})());
for(const [field,value]of [['plants',0],['food',0],['hide',false],['isopods',0],['springtails',0],['algae',80],['waste',80],['moisture',90],['stress',80]])check(`${field}-visibly-affects-render`,!raw(normal).equals(raw(snapshot({...t,[field]:value}))));
check('native-animation-changes-over-time',!raw(normal).equals(raw(snapshot(t,13))));
check('pan-affects-frame',!raw(normal).equals(raw(snapshot(t,12,{frame:90}))));
check('zoom-affects-frame',!raw(normal).equals(raw(snapshot(t,12,{zoom:1.6}))));
check('reticle-affects-frame',!raw(normal).equals(raw(snapshot(t,12,{reticle:true}))));
check('title-card-size-preserved',snapshot(t,12,{},400,148).toBuffer('image/png').length>0);
await writeFile(new URL('tank-native-review.png',import.meta.url),normal.toBuffer('image/png'));
await writeFile(new URL('tank-zoom-review.png',import.meta.url),snapshot(t,12,{zoom:1.6,reticle:true}).toBuffer('image/png'));
await writeFile(new URL('tank-validation.json',import.meta.url),JSON.stringify({task:'M1.I2',checks:results,passed:results.filter(r=>r.pass).length,total:results.length,limitations:['Canvas implementation check using @napi-rs/canvas; browser integration and user acceptance remain separate.']},null,2)+'\n');
console.log(JSON.stringify({passed:results.filter(r=>r.pass).length,total:results.length,failed:results.filter(r=>!r.pass)}));
if(results.some(r=>!r.pass))process.exitCode=1;
