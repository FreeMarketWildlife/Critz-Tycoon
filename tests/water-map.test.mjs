import test from 'node:test';
import assert from 'node:assert/strict';
import {newMap,paint,at} from '../map-editor/model.js';
import {waterComponents,waterUnderlay,shoreGrounds} from '../src/water-map.js';
import {compileCoastalField,coastalBankPixels,coastalWashPixels} from '../src/coastal-format.js';

test('disconnected shallow and deep bodies retain independent depth contracts',()=>{
  const m=newMap();
  for(let y=3;y<7;y++)for(let x=3;x<7;x++)paint(m,x,y,'water-fresh-still');
  for(let y=12;y<14;y++)for(let x=12;x<14;x++)paint(m,x,y,'water-fresh-shallow-still');
  const {components}=waterComponents(m);
  assert.deepEqual(components.map(c=>[c.cells.length,c.mixed]),[[16,false],[4,false]]);
  paint(m,3,3,'water-fresh-shallow-still');
  assert.deepEqual(waterComponents(m).components.map(c=>c.mixed),[true,false]);
});
test('water margins retain actual land materials and never wrap across map rows',()=>{
  for(const ground of ['sand','path','soil','paving']){
    const m=newMap();m.terrain.fill(ground);paint(m,5,5,'water');
    assert.deepEqual(waterUnderlay(m,5,5),Array(4).fill(ground));
  }
  const m=newMap();paint(m,0,5,'water');paint(m,m.w-1,4,'sand');
  assert.equal(shoreGrounds(m,0,5).some(a=>a.kind==='sand'),false);
  m.raw[at(m,0,5)]={id:'meadow.grass.0',blocked:false};
  assert.equal(waterComponents(m).cells.length,0);
});
test('cropped component fields retain exact global wet pixels, banks and wash frames',()=>{
  const layouts=[
    [[0,0,3,3],[7,7,3,3]], [[2,2,4,4],[7,2,3,4]],
    [[2,2,3,3],[5,5,3,3]], [[0,8,4,4],[8,0,4,4]],
    [[1,1,10,10]], [[2,2,8,2],[2,4,2,6],[8,4,2,6],[2,8,8,2]],
  ];
  for(const rectangles of layouts){
    const m=newMap('proof','Proof',12,12);
    for(const [x,y,w,h]of rectangles)for(let b=y;b<y+h;b++)for(let a=x;a<x+w;a++)paint(m,a,b,'water');
    if(rectangles.length===1)for(let y=4;y<8;y++)for(let x=4;x<8;x++)paint(m,x,y,'grass');
    const layout=waterComponents(m),global=compileCoastalField(layout.cells,m.w*32,m.h*32+32);
    const wet=new Uint8Array(global.wet.length),bank=new Uint8ClampedArray(wet.length*4),waves=[0,8,16,24].map(()=>new Uint8ClampedArray(wet.length*4));
    for(const body of layout.components){
      const b=body.bounds,f=compileCoastalField(body.cells.map(a=>({x:a.x-b.x/32,y:a.y-b.y/32})),b.w,b.h),rgba=coastalBankPixels(f),wash=[0,8,16,24].map(n=>coastalWashPixels(f,n));
      for(let y=0;y<b.h;y++)for(let x=0;x<b.w;x++){
        const i=y*b.w+x,j=(y+b.y)*global.width+x+b.x;
        wet[j]|=f.wet[i];
        if(rgba[i*4+3])bank.set(rgba.subarray(i*4,i*4+4),j*4);
        for(let n=0;n<waves.length;n++)if(wash[n][i*4+3])waves[n].set(wash[n].subarray(i*4,i*4+4),j*4);
      }
    }
    assert.deepEqual(wet,global.wet);
    assert.deepEqual(bank,coastalBankPixels(global));
    for(const [n,frame]of [0,8,16,24].entries())assert.deepEqual(waves[n],coastalWashPixels(global,frame));
  }
});
