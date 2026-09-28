// Exact native export. Storage frames are not scaled or resampled.
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {Raster} from '../raster.mjs';
const root='art/source/budget-comparison',out='assets/review/budget-comparison';
await mkdir(out,{recursive:true});await mkdir('docs/reviews/M1-C1',{recursive:true});
const roles=process.argv.includes('--kaid-only')?['kaid']:['mom','kaid','nugget'];
const data=await Promise.all(roles.map(async r=>JSON.parse(await readFile(`${root}/${r}.json`,'utf8'))));
const atlas=new Raster(288,data.length*64),proof=new Raster(288,data.length*64),entries=[],characters=[],checks=[];
function assert(ok,name){if(!ok)throw new Error(name);checks.push({name,pass:true});}
for(let row=0;row<data.length;row++){
 const char=data[row],metadata={id:char.character,label:char.label,budgets:{}};
 assert(Object.keys(char.palette).length<=15,`${char.character}: palette <=15 opaque colors`);
 for(const [bi,budget] of ['16','24'].entries()){
  const spec=char.budgets[budget],w=Number(budget);assert(spec.frame[0]===w&&spec.frame[1]===32,`${char.character}/${budget}: frame dimensions`);
  assert(spec.anchor[0]===w/2&&spec.anchor[1]===32,`${char.character}/${budget}: ground anchor`);
  const ids={},frames=[];
  for(const [di,dir] of ['down','up','left','right'].entries()){
   ids[dir]={};
   for(const [pi,pose] of ['idle','strideA','strideB'].entries()){
    const rows=spec.directions[dir][pose];assert(rows.length===32&&rows.every(r=>r.length===w),`${char.character}/${budget}/${dir}/${pose}: full untrimmed rows`);
    const frame=new Raster(w,32);let minX=w,minY=32,maxX=-1,maxY=-1,count=0;const colors=new Set();
    for(let y=0;y<32;y++)for(let x=0;x<w;x++){const p=rows[y][x];if(p==='.')continue;if(!char.palette[p])throw new Error(`Unknown palette symbol ${p}`);frame.dot(x,y,char.palette[p]);colors.add(char.palette[p]);minX=Math.min(minX,x);maxX=Math.max(maxX,x);minY=Math.min(minY,y);maxY=Math.max(maxY,y);count++;}
    assert(count>0&&maxY===(pose==='idle'?30:31),`${char.character}/${budget}/${dir}/${pose}: foot baseline`);
    const id=`compare.${char.character}.${budget}.${dir}.${pose}`,x=(di*3+pi)*24,y=row*64+bi*32;
    atlas.blit(frame,x,y);proof.blit(frame,x+12-w/2,y);
    const hash=createHash('sha256').update(frame.p).digest('hex');frames.push(hash);
    entries.push({id,rect:[x,y,w,32],anchor:spec.anchor,character:char.character,budget:Number(budget),direction:dir,pose,opaqueBBox:[minX,minY,maxX+1,maxY+1],paintedPixels:count,colorCount:colors.size,sha256:hash,status:'comparison-awaiting-user-choice'});
    ids[dir][pose]=id;
   }
  }
  assert(new Set(frames).size>=10,`${char.character}/${budget}: distinct directional/gait drawings`);
  metadata.budgets[budget]={frame:spec.frame,anchor:spec.anchor,frames:ids};
 }
 characters.push(metadata);
}
await atlas.save(`${out}/atlas.png`);await proof.scale(4).save('docs/reviews/M1-C1/frames-4x.png');
await writeFile(`${out}/atlas.json`,JSON.stringify({schemaVersion:1,image:'atlas.png',size:[atlas.w,atlas.h],status:'comparison-awaiting-user-choice',characters,assets:entries,animation:{tickSeconds:280896/16777216,walkTicksPerTile:16,holds:[8,8,8,8],cycle:['strideA','idle','strideB','idle']}},null,2)+'\n');
await writeFile('docs/reviews/M1-C1/asset-validation.json',JSON.stringify({passed:checks.length,checks,assetCount:entries.length,sourceRoles:roles,atlasSha256:createHash('sha256').update(await readFile(`${out}/atlas.png`)).digest('hex')},null,2)+'\n');
console.log(`Exported ${entries.length} exact native frames; ${checks.length} checks passed.`);
