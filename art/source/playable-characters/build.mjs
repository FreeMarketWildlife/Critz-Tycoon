// Export audited native chibi rows without scaling, mirroring or redrawing.
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { Raster } from '../raster.mjs';
const source = 'art/source/characters-walk-v3';
const out = 'assets/playable/characters';
const order = ['hero.boy','hero.girl','mom','kaid','professor','juniper','dr-fern','mina','ollie','aunt-ember','rival-mom','rival-dad'];
const directions = {down:'south',up:'north',left:'west',right:'east'};
const modes = ['walk','run'], poses = ['idle','strideA','strideB'];
const sheet = new Raster(288, order.length * 64), assets = [], characters = {};
await mkdir(out,{recursive:true});
for (const [row,id] of order.entries()) {
  const person = JSON.parse(await readFile(`${source}/${id}.json`,'utf8'));
  const mapping = {frame:[24,32],anchor:[12,32],directions:{},status:'playable-review',
    runArtwork:'Corrected walk poses reused at the existing run cadence; dedicated run poses pending.'};
  for (const [di,[direction,nativeDirection]] of Object.entries(directions).entries()) {
    mapping.directions[direction] = {};
    for (const [mi,mode] of modes.entries()) {
      mapping.directions[direction][mode] = {};
      for (const [pi,pose] of poses.entries()) {
        const rows = person.frames[nativeDirection][pose];
        if (rows.length!==32 || rows.some(r=>r.length!==24)) throw Error(`Invalid native rows: ${id}`);
        const native = new Raster(24,32);
        for (let y=0;y<32;y++) for(let x=0;x<24;x++) {
          const key = rows[y][x];
          if(key!=='.') {
            if(!/^#[0-9a-f]{6}$/i.test(person.palette[key]||'')) throw Error(`Invalid palette: ${id}`);
            native.dot(x,y,person.palette[key]);
          }
        }
        const frameId = `char.${id}.${direction}.${mode}.${pose}`, x = (di*3+pi)*24, y = row*64+mi*32;
        sheet.blit(native,x,y);
        assets.push({id:frameId,rect:[x,y,24,32],anchor:[12,32],character:id,direction,mode,pose,
          mirrored:false,status:'playable-review',source:`${source}/${id}.json`,
          sourceFrame:`character.walk.v3.${id}.${nativeDirection}.${pose}`});
        mapping.directions[direction][mode][pose] = frameId;
      }
    }
  }
  characters[id] = mapping;
}
await sheet.save(`${out}/atlas.png`);
await writeFile(`${out}/atlas.json`,JSON.stringify({schemaVersion:1,image:'atlas.png',size:[sheet.w,sheet.h],status:'playable-review',assets,characters},null,2)+'\n');
console.log(`Exported ${assets.length} playable entries for ${order.length} native character designs.`);
