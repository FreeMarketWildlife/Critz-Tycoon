import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { Raster } from '../raster.mjs';
const version = process.env.CRITZ_WALK_VERSION || 'v2';
if (!['v2','v3'].includes(version)) throw Error('Unsupported walk source version');
const source = `art/source/characters-walk-${version}`, output = `assets/review/characters-walk-${version}`, review = version === 'v3' ? 'docs/reviews/M1-I3' : 'docs/reviews/M1-C3';
const order = ['hero.boy','hero.girl','mom','kaid','professor','juniper','dr-fern','mina','ollie','aunt-ember','rival-mom','rival-dad'];
const directions = ['south','west','north','east'], poses = ['idle','strideA','strideB'];
for (const p of [output, output+'/sheets', review]) await mkdir(p, {recursive:true});
const atlas = new Raster(288, order.length*32), assets = [], characters = [], checks = [];
const assert = (condition, name) => { if (!condition) throw Error(name); checks.push({name,pass:true}); };
for (const [index, id] of order.entries()) {
  const person = JSON.parse(await readFile(`${source}/${id}.json`, 'utf8'));
  const still = JSON.parse(await readFile(`art/source/characters-v2/${id}.json`, 'utf8'));
  assert(person.id === id, id+': identity');
  assert(JSON.stringify(person.palette) === JSON.stringify(still.palette), id+': original palette unchanged');
  if (version === 'v2') assert(JSON.stringify(person.frames.south.idle) === JSON.stringify(still.rows), id+': front idle unchanged');
  // v3 explicitly corrects reported idle artifacts; independently audit all
  // native pixel changes against the v2 source in check-walking-atlas.py.
  const sheet = new Raster(288,32), frames = {}, allColors = new Set();
  for (const [di,direction] of directions.entries()) {
    frames[direction] = {}; const distinct = new Set();
    for (const [pi,pose] of poses.entries()) {
      const rows = person.frames[direction][pose];
      assert(rows.length===32 && rows.every(r=>r.length===24), `${id}.${direction}.${pose}: full native frame`);
      const native = new Raster(24,32), points = [], colors = new Set();
      for (let y=0;y<32;y++) for(let x=0;x<24;x++) {
        const key=rows[y][x]; if(key==='.') continue;
        const color=person.palette[key]; if(!color || !/^#[0-9a-f]{6}$/i.test(color)) throw Error(`${id}: invalid color ${key}`);
        native.dot(x,y,color); points.push([x,y]); colors.add(color); allColors.add(color);
      }
      const xs=points.map(p=>p[0]),ys=points.map(p=>p[1]);
      const bbox=[Math.min(...xs),Math.min(...ys),Math.max(...xs)+1,Math.max(...ys)+1];
      assert(bbox[0]>=2 && bbox[2]<=22 && bbox[2]-bbox[0]<=20 && bbox[3]-bbox[1]<=26, `${id}.${direction}.${pose}: 20x26 painted budget`);
      assert(bbox[3]===(pose==='idle'?31:32), `${id}.${direction}.${pose}: stance baseline`);
      assert(colors.size<=15, `${id}.${direction}.${pose}: palette budget`);
      assert(Array.from({length:bbox[3]-bbox[1]},(_,y)=>/[^.]/.test(rows[y+bbox[1]])).every(Boolean), `${id}.${direction}.${pose}: no detached body row`);
      const hash=createHash('sha256').update(native.p).digest('hex');distinct.add(hash);
      const column=di*3+pi, frameId=`character.walk.${version}.${id}.${direction}.${pose}`;
      atlas.blit(native,column*24,index*32); sheet.blit(native,column*24,0);frames[direction][pose]=frameId;
      assets.push({id:frameId,character:id,label:person.label,direction,pose,rect:[column*24,index*32,24,32],anchor:[12,32],opaqueBBox:bbox,visibleSize:[bbox[2]-bbox[0],bbox[3]-bbox[1]],colorCount:colors.size,sha256:hash,source:`${source}/${id}.json`,status:'awaiting-user-art-review'});
    }
    assert(distinct.size===3, `${id}.${direction}: three distinct poses`);
  }
  assert(allColors.size<=15,id+': shared character palette');
  await sheet.save(`${output}/sheets/${id}.png`);
  characters.push({id,label:person.label,bodyType:still.design.bodyType,frames,sheet:`sheets/${id}.png`,gif:`gifs/${id}.gif`,design:person.design,notes:person.notes});
}
await atlas.save(output+'/atlas.png');
await atlas.scale(4).save(review+'/all-frames-4x.png');
await writeFile(output+'/atlas.json',JSON.stringify({schemaVersion:1,image:'atlas.png',size:[atlas.w,atlas.h],nativeFrame:[24,32],paintedBudget:[20,26],directions,poses,assetCount:assets.length,characterCount:characters.length,animation:{sequence:['strideA','idle','strideB','idle'],holds:[8,8,8,8],tickSeconds:280896/16777216,loopTicks:32,directionReviewTicks:96,gifTiming:'centisecond-rounded cumulative source timing'},characters,assets},null,2)+'\n');
await writeFile(review+'/native-validation.json',JSON.stringify({passed:checks.length,characterCount:characters.length,frameCount:assets.length,checks},null,2)+'\n');
console.log(`${characters.length} walking characters, ${assets.length} frames; ${checks.length} checks passed.`);
