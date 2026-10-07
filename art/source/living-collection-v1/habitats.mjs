import fs from 'node:fs';import path from 'node:path';
import {Pixels,out,sharp,saveAsset,home,indexed} from './pixels.mjs';
const P={edge:'#173c42',metal:'#31585b',trim:'#668c88',glint:'#cfede0',sand:'#c8ae76',sandLight:'#e4d2a0',soil:'#5b4835',soilLight:'#826447',rock:'#657b76',rockLight:'#9bab92',rockDark:'#425852',wood:'#755039',woodLight:'#a6774b',woodDark:'#453b2d',leaf:'#398361',leafLight:'#7cbd7a',leafDark:'#225744',moss:'#82a966'};
function leaf(a,x,y,dx,dy,c){const px=-dy*.35,py=dx*.35,mx=x+dx*.55,my=y+dy*.55;a.polygon([[x,y],[Math.round(mx-px),Math.round(my-py)],[x+dx,y+dy],[Math.round(mx+px),Math.round(my+py)]],c);a.line(x,y,x+dx,y+dy,P.leafLight);}
function plant(a,x,y,h,type=0){
 const top=y-h;a.line(x,y,x-1,top,P.leafDark);a.line(x+1,y,x,top,P.leaf);
 for(let k=0;k<4;k++){const yy=y-5-k*Math.floor(h/5),len=type?9:6;leaf(a,x,yy,-len-k%2*3,-4-k%2*2,k%2?P.leaf:P.leafDark);leaf(a,x+1,yy-3,len,-4,k%2?P.leafLight:P.leaf);}
 leaf(a,x,top+6,-3,-7,P.leafLight);
}
function broadPlant(a,x,y,h){
 a.line(x,y,x, y-h,P.leafDark);a.line(x+1,y,x+1,y-h,P.leaf);
 for(let k=0;k<3;k++)for(const s of [-1,1]){
  const yy=y-5-k*Math.floor(h/4)-(s===1?4:0),dx=s*(10+k%2*3),tip=[x+dx,yy-7];
  a.polygon([[x,yy],[x+s*3,yy-8],[tip[0],tip[1]-2],[tip[0]+s*2,tip[1]+2],[x+s*6,yy+1]],P.leafDark);
  a.polygon([[x+s,yy-1],[x+s*4,yy-7],[tip[0],tip[1]-1],[x+s*6,yy-1]],k%2?'#59a46e':'#75b87b');
  a.line(x,yy,tip[0],tip[1],'#aad198');
 }
}
function ribbon(a,x,y,h){
 a.polygon([[x,y],[x-4,y-h+10],[x-2,y-h],[x+1,y-h+8],[x+3,y]],P.leaf);
 a.line(x,y-4,x-2,y-h+4,P.leafLight);
 a.polygon([[x+3,y],[x+5,y-h+16],[x+10,y-h+6],[x+8,y-h+21],[x+6,y]],P.leafDark);
}
function rock(a,x,y,w,h){a.polygon([[x-w/2|0,y],[x-w/2+2|0,y-h+4],[x-1,y-h],[x+w/2-3|0,y-h+2],[x+w/2|0,y-3]],P.rockDark);a.polygon([[x-w/2+2|0,y-3],[x-w/2+4|0,y-h+5],[x,y-h+2],[x+w/2-4|0,y-h+4],[x+2,y-4]],P.rock);a.line(x-w/2+4|0,y-h+5,x-1,y-h+2,P.rockLight);}
function branch(a,x,y){a.polygon([[x-7,y],[x-2,y-29],[x-9,y-40],[x-6,y-43],[x+2,y-32],[x+7,y-51],[x+10,y-51],[x+9,y-27],[x+24,y-36],[x+25,y-32],[x+9,y-21],[x+6,y]],P.woodDark);a.polygon([[x-4,y],[x+1,y-28],[x+7,y-46],[x+4,y-25],[x+6,y-20],[x+3,y]],P.wood);a.line(x-2,y-4,x+2,y-28,P.woodLight);a.line(x+5,y-23,x+21,y-32,P.woodLight);}
function hardware(a,type){
 a.polygon([[7,14],[20,5],[179,5],[187,14],[179,18],[7,18]],P.edge);
 a.line(20,7,177,7,P.trim);a.line(12,14,178,14,P.glint);
 // Vented top and service lamp: a living enclosure does not read as a sealed jar.
 for(let x=25;x<=166;x+=5)a.line(x,9,x+2,9,type==='aquarium'?'#87b8b0':'#182f31');
 a.rect(8,15,11,114,P.edge);a.line(12,19,12,111,P.trim);
 a.polygon([[177,17],[187,13],[187,114],[177,121]],'#274e52');
 a.line(180,24,180,108,P.trim);a.line(183,24,183,41,P.glint);
 a.rect(9,112,178,117,P.edge);a.line(12,113,176,113,P.trim);
 a.polygon([[9,118],[178,118],[187,113],[187,137],[178,143],[9,143]],P.woodDark);
 a.rect(12,120,175,139,P.wood);a.rect(16,123,91,136,'#896348');a.rect(96,123,171,136,'#896348');
 a.line(16,123,90,123,P.woodLight);a.line(96,123,170,123,P.woodLight);
 a.line(16,136,90,136,P.woodDark);a.line(96,136,170,136,P.woodDark);
 a.rect(85,128,87,130,'#e0c38a');a.rect(100,128,102,130,'#e0c38a');
 a.rect(18,141,26,143,P.edge);a.rect(160,141,168,143,P.edge);
}
function interior(type){
 const a=new Pixels(192,144),fg=new Pixels(192,144);
 const aquatic=type==='aquarium',pal=type==='paludarium';
 a.rect(12,18,176,111,aquatic?'#235b70':pal?'#244d47':'#3d5b49');
 if(aquatic){
  a.rect(13,23,176,48,'#33768a');a.rect(13,49,176,78,'#2b687b');a.rect(13,79,176,109,'#255b6a');
  a.line(14,24,174,24,'#8bc8c5');a.line(24,26,87,26,'#5399a5');
  // Filter, lift tube and intake remain behind the plants/fish.
  a.rect(153,19,164,57,P.edge);a.rect(155,21,162,53,'#496f73');a.rect(156,57,159,91,P.edge);
  for(let y=63;y<=86;y+=4)a.line(156,y,159,y,P.trim);
  a.polygon([[13,102],[58,98],[94,105],[140,98],[176,102],[176,111],[13,111]],P.sand);
  a.line(13,102,52,99,P.sandLight);a.line(100,104,135,99,P.sandLight);
  ribbon(a,29,103,57);ribbon(a,39,103,47);plant(a,53,102,46);plant(a,157,104,37);branch(a,107,105);
  rock(a,99,107,33,17);rock(a,123,108,22,15);rock(a,71,108,20,12);
  broadPlant(fg,27,109,25);broadPlant(fg,163,110,30);plant(fg,143,110,16);
 }else if(type==='terrarium'){
  a.rect(14,21,175,44,'#476f52');a.rect(14,45,175,85,'#3b624a');
  // Cork back, visible dry substrate, ventilation and a separate shallow dish.
  for(const x of [23,71,129,160]){a.polygon([[x,21],[x+8,21],[x+5,99],[x-5,99]],P.woodDark);a.line(x+2,27,x-1,85,P.wood);}
  a.polygon([[13,102],[42,94],[71,100],[110,96],[144,101],[176,97],[176,111],[13,111]],P.soil);
  a.line(17,103,48,97,P.soilLight);a.line(101,99,120,98,P.soilLight);
  branch(a,115,99);rock(a,72,103,32,17);rock(a,90,104,20,12);
  a.polygon([[62,103],[62,96],[67,92],[78,92],[84,97],[84,103]],P.woodDark);a.rect(66,97,79,103,'#283b2c');
  broadPlant(a,36,99,53);broadPlant(a,152,101,64);plant(fg,24,109,23,1);plant(fg,163,108,30);
  a.polygon([[122,103],[126,100],[147,100],[151,103],[147,108],[126,108]],P.rockDark);a.rect(128,102,145,104,'#759d99');a.line(130,102,141,102,P.glint);
 }else{
  // A retained land bank and gentle shore visibly separate land from water.
  a.rect(14,21,176,65,'#37674e');a.rect(14,66,176,111,'#295f69');
  a.polygon([[13,68],[54,62],[85,68],[101,83],[118,88],[121,111],[13,111]],P.soil);
  a.polygon([[13,66],[52,60],[84,65],[98,78],[85,77],[57,70],[13,74]],P.moss);
  a.line(120,89,173,89,'#6eb2b0');a.line(131,92,160,92,'#428894');
  broadPlant(a,35,72,42);plant(a,65,70,31);branch(a,78,76);ribbon(a,161,107,29);
  rock(a,98,92,28,22);rock(a,116,104,22,13);rock(a,137,109,25,13);
  plant(fg,27,100,23);plant(fg,163,108,20);
  // Waterfall on the back wall feeds a pool; stepped rock lip stays distinct.
  rock(a,147,72,23,19);rock(a,149,55,20,20);rock(a,147,39,16,11);
  a.rect(144,31,151,76,P.rockDark);a.rect(146,35,149,75,'#6bb5b8');a.line(146,35,146,72,'#b3e2d3');
  rock(a,147,80,22,7);a.line(140,80,152,80,'#8fceca');
 }
 // Deliberate clustered substrate/leaf-litter accents, never per-pixel noise.
 for(const [x,y]of [[22,106],[45,103],[57,109],[92,110],[132,109],[151,108],[168,106]]){a.line(x,y,x+2,y,aquatic?P.sandLight:P.soilLight);}
 hardware(fg,type);fg.line(16,30,16,55,P.glint);fg.line(18,32,18,43,'#75a5a0');fg.line(171,79,171,102,'#76a4a0');
 return {back:a,front:fg};
}
function smallProp(type){
 // Separate native 96×96 world prop, not a downsample of the close-up raster.
 const a=new Pixels(96,96),wet=type!=='terrarium';
 a.polygon([[5,31],[16,23],[83,23],[91,31],[91,74],[83,80],[5,80]],P.edge);
 a.rect(8,32,82,70,wet?'#2b687b':'#3b624a');a.line(17,25,81,25,P.trim);a.line(8,31,82,31,P.glint);
 a.rect(8,65,82,71,wet?P.sand:P.soil);a.line(10,36,10,47,P.glint);a.line(86,35,86,68,P.trim);
 a.rect(8,74,82,88,P.wood);a.rect(10,76,44,85,'#896348');a.rect(48,76,80,85,'#896348');a.p(40,80,P.sandLight);a.p(52,80,P.sandLight);
 a.rect(11,88,17,93,P.edge);a.rect(73,88,79,93,P.edge);
 if(type==='paludarium'){a.polygon([[8,52],[32,48],[51,61],[53,69],[8,69]],P.soil);a.line(8,52,30,49,P.moss);}
 plant(a,23,66,23);plant(a,71,66,27);rock(a,48,68,21,12);
 for(let x=19;x<=77;x+=5)a.p(x,27,wet?P.trim:P.edge);
 return a;
}
export async function makeHabitats(animals){const metas=[];
 for(const type of ['aquarium','terrarium','paludarium']){
  const layers=interior(type),frames=[];
  for(let f=0;f<16;f++){
   const a=layers.back.clone(),phase=f%4;
   if(type==='aquarium'){
    const x=72+Math.round(Math.sin(f/16*Math.PI*2)*21),y=39+Math.round(Math.cos(f/16*Math.PI*2)*3);
    let fish=animals.guppy[phase],turnOffset=0;
    if(Math.cos(f/16*Math.PI*2)<0){const xs=fish.a.flatMap((c,i)=>c?[i%32]:[]);turnOffset=Math.min(...xs)+Math.max(...xs)-31;const turned=new Pixels(32,32);for(let yy=0;yy<32;yy++)for(let xx=0;xx<32;xx++)turned.p(xx,yy,fish.get(31-xx,yy));fish=turned;}
    a.blit(fish,x+turnOffset,y); // Turning preserves the painted body's center.
    for(let b=0;b<4;b++){const yy=85-((f*2+b*17)%58);a.p(162+b%2*3,yy,'#88c4c7');a.p(163+b%2*3,yy-1,'#b3e2d3');}
   }else if(type==='terrarium'){
    a.blit(animals['pebble-gecko'][phase],77+Math.round(Math.sin(f/16*Math.PI*2)*3),64);
   }else{
    a.blit(animals['mangrove-crab'][phase],48+Math.round(Math.sin(f/16*Math.PI*2)*7),45);
    for(let y=40+f%4;y<75;y+=7)a.line(147,y,149,y,'#b3e2d3');
   }
   a.blit(layers.front);frames.push(a);
  }
  const label={aquarium:'Planted Aquarium',terrarium:'Woodland Terrarium',paludarium:'Creekbank Paludarium'}[type];
  metas.push(await saveAsset(type,label,'habitat',frames,{nativeCloseup:[192,144],worldProp:[96,96],featuredAnimal:{aquarium:'guppy',terrarium:'pebble-gecko',paludarium:'mangrove-crab'}[type],notes:'Original layered habitat art. One featured species per scene; schematic art, not a care specification or gallon-volume claim. No game simulation changes.'}));
  const prop=smallProp(type),dir=path.join(out,type);
  for(const [name,p]of [['back',layers.back],['foreground',layers.front],['world-prop',prop]]){
   await sharp(p.rgba(),{raw:{width:p.w,height:p.h,channels:4}}).png().toFile(path.join(dir,name+'.png'));
   fs.writeFileSync(path.join(home,`${type}-${name}.sprite.json`),JSON.stringify(indexed(label+' '+name,[p]))+'\n');
  }
 }
 return metas;
}
