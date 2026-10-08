// Original Critz native pixels. Reference images are never sampled or copied.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {Raster as NativeRaster} from '../raster.mjs';
class Raster extends NativeRaster { line(x,y,xx,yy,c){return super.line(Math.round(x),Math.round(y),Math.round(xx),Math.round(yy),c);} }
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'../../..');
const source=path.join(root,'art/source/luke-greenhouse'),out=path.join(root,'assets/review/luke-greenhouse');
const C={ink:'#281d22',skin:'#edb88d',skinShade:'#c98870',skinLight:'#ffe1b1',hair:'#59362a',hairShade:'#382724',hairLight:'#8c5635',shirt:'#913e4d',shirtShade:'#652f43',shirtLight:'#b75b62',pants:'#405866',pantsShade:'#2c3c50',boot:'#725043',bootLight:'#a57855',white:'#fff2d2',blue:'#36b4ed',blueDark:'#236989'};
function color(r,x,y){const i=(y*r.w+x)*4;return r.p[i+3]?'#'+r.p.subarray(i,i+3).toString('hex'):null;}
function bounds(r){let l=r.w,t=r.h,rr=0,b=0,n=0;for(let y=0;y<r.h;y++)for(let x=0;x<r.w;x++)if(r.p[(y*r.w+x)*4+3]){l=Math.min(l,x);t=Math.min(t,y);rr=Math.max(rr,x+1);b=Math.max(b,y+1);n++;}return {bounds:[l,t,rr,b],occupied:n};}
function copyRegion(a,b,box,dx=0,dy=0){for(let y=box[1];y<box[3];y++)for(let x=box[0];x<box[2];x++){const c=color(b,x,y);if(c)a.dot(x+dx,y+dy,c);}}
const boy=JSON.parse(fs.readFileSync(path.join(root,'art/source/hero-boy-v1/idle.sprite.json')));
const template=JSON.parse(fs.readFileSync(path.join(root,'sprite-editor/templates/basic-character.json')));
const masks={skull:[],eyes:[],torso:[],arms:[],hands:[],legs:[]};
function front(){const a=new Raster(32,64),remap={2:C.shirt,13:C.shirt,14:C.ink,16:C.skinShade,17:C.skin,9:C.pants,34:C.pantsShade,35:C.boot,44:C.boot,32:C.ink};
 for(let y=43;y<=61;y++){const sy=y<=54?45+Math.floor((y-43)*10/12):y;for(let x=0;x<32;x++){const v=boy.frames[0].pixels[sy*32+x];if(!v)continue;let col=remap[v]||boy.palette[v];if([2,13].includes(v))col=x<12?C.shirtLight:x>21?C.shirtShade:C.shirt;if(v===13&&sy>=60)col=C.bootLight;a.dot(x,y,col);const part=sy>=55?'legs':([16,17].includes(v)&&sy>=48?'hands':(x<9||x>22?'arms':'torso'));masks[part].push(y*32+x);}}
 for(let y=26;y<=46;y++)for(let x=0;x<32;x++){const v=template.frames[0].pixels[y*32+x];if(y>=45&&(x<10||x>21))continue;if(![9,10,11,13,14].includes(v))continue;a.dot(x,y-2,v===14?C.ink:([9,10].includes(v)?C.skinShade:C.skin));masks.skull.push((y-2)*32+x);}
 // Original swept brown crown, short temples and full beard. Anatomical masks remain separate.
 a.poly([[5,32],[5,28],[8,25],[12,23],[21,23],[26,26],[27,32],[25,36],[23,34],[22,30],[17,32],[11,31],[8,35],[6,36]],C.hairShade);
 a.poly([[6,31],[8,27],[12,25],[20,24],[24,26],[25,29],[20,29],[16,31],[11,30],[8,33]],C.hair);
 a.line(9,28,17,25,C.hairLight);a.line(9,29,15,27,C.hairLight);a.line(18,26,22,26,C.hairLight);
 for(const x of [12,18]){a.rect(x,36,2,4,C.ink);a.dot(x,36,C.white);a.rect(x,37,2,2,C.blue);a.dot(x+1,39,C.blueDark);for(let y=36;y<40;y++)for(let xx=x;xx<x+2;xx++)masks.eyes.push(y*32+xx);}
 a.line(11,34,14,34,C.hair);a.line(17,34,20,34,C.hair);
 a.dot(14,40,C.skinShade);a.dot(17,40,C.skinShade);a.rect(15,39,2,2,C.skinLight);
 a.poly([[7,39],[9,40],[11,41],[13,40],[15,41],[17,41],[19,40],[21,41],[23,40],[25,39],[24,43],[22,45],[19,46],[12,46],[9,44]],C.hairShade);
 a.poly([[9,41],[12,42],[14,42],[15,43],[17,43],[18,42],[21,42],[23,41],[22,44],[19,45],[13,45],[10,43]],C.hair);
 a.poly([[7,36],[9,37],[10,40],[13,41],[13,44],[10,44],[8,42]],C.hair);a.poly([[24,36],[22,37],[21,40],[18,41],[18,44],[21,44],[23,42]],C.hair);a.line(8,38,9,41,C.hairLight);a.line(21,40,22,38,C.hairShade);a.rect(14,42,4,1,C.skinLight);a.rect(15,43,2,1,C.ink);a.dot(11,42,C.hairLight);a.dot(12,43,C.hairLight);a.dot(13,44,C.hairLight);
 a.rect(14,47,4,1,C.shirtShade);a.dot(15,49,C.shirtLight);
 return a;
}
function back(front){const a=front.crop(0,0,32,64);for(let y=23;y<=46;y++)for(let x=0;x<32;x++)if(color(a,x,y)){let c=(x<8||x>23||y===46)?C.hairShade:x<14?C.hairLight:C.hair;if(y>=44&&x>=12&&x<=19)c=C.skinShade;a.dot(x,y,c);}for(let y=25;y<42;y++){if(y%4===0)a.line(10,y,16,y-1,C.hair);if(y%4===2)a.line(20,y,23,y+1,C.hairShade);}return a;}
function profile(east){const a=new Raster(32,64),X=x=>east?x:31-x;function rect(x,y,w,h,c){for(let j=y;j<y+h;j++)for(let i=x;i<x+w;i++)a.dot(X(i),j,c);}function poly(p,c){a.poly(p.map(([x,y])=>[X(x),y]),c);}
 rect(13,42,8,4,C.ink);rect(14,43,6,2,C.skinShade);
 poly([[11,45],[20,44],[23,47],[24,53],[22,56],[10,56],[9,52],[9,48]],C.ink);poly([[11,46],[20,45],[22,48],[22,54],[11,54],[10,50]],C.shirt);rect(11,47,3,5,C.shirtLight);rect(11,55,12,4,C.ink);rect(12,55,10,3,C.pants);rect(11,58,11,3,C.pantsShade);rect(10,60,14,2,C.ink);rect(11,60,12,1,C.bootLight);
 rect(13,47,6,8,C.ink);rect(14,47,4,4,C.shirtLight);rect(14,51,4,4,C.skin);rect(17,52,1,2,C.skinShade);
 poly([[8,26],[13,23],[20,24],[24,27],[25,31],[23,34],[25,38],[26,40],[24,43],[21,45],[12,44],[8,41],[6,35],[6,30]],C.ink);
 poly([[12,29],[21,29],[23,34],[24,38],[25,39],[23,42],[20,43],[13,42],[10,37]],C.skin);
 poly([[7,29],[9,26],[14,24],[21,25],[23,28],[23,31],[18,32],[16,35],[13,36],[12,41],[9,39],[7,35]],C.hair);poly([[8,29],[11,26],[15,25],[20,26],[17,28],[12,30]],C.hairLight);
 rect(20,36,2,4,C.ink);rect(20,36,1,1,C.white);rect(20,37,2,2,C.blue);rect(14,37,2,3,C.skinShade);
 poly([[14,40],[18,42],[21,41],[24,40],[24,43],[21,45],[16,46],[12,44],[11,41]],C.hairShade);poly([[13,41],[16,43],[19,43],[21,44],[17,45],[14,44]],C.hair);rect(22,41,2,1,C.skinLight);
 return a;
}
function stride(idle,phase,side=false){const a=new Raster(32,64),s=phase?1:-1;copyRegion(a,idle,[0,0,32,55],0,2);if(!side){copyRegion(a,idle,[7,55,15,62],s*2,s===1?2:-2);copyRegion(a,idle,[17,55,25,62],-s*2,s===1?-2:2);a.rect(12,57,8,2,C.pants);a.rect(15,58,2,2,C.ink);copyRegion(a,idle,phase?[3,46,9,55]:[23,46,29,55],0,-1);}else{a.poly([[13-s*3,56],[17-s*3,56],[17-s*3,61],[11-s*3,62],[10-s*3,60]],C.ink);a.rect(13-s*3,57,3,4,C.pantsShade);a.rect(11-s*3,61,6,1,C.boot);a.poly([[15+s*3,57],[19+s*3,57],[21+s*3,62],[20+s*3,64],[13+s*3,64],[13+s*3,62]],C.ink);a.rect(15+s*3,58,3,4,C.pants);a.rect(14+s*3,62,6,1,C.bootLight);}return a;}
const idle=front(),north=back(idle),west=profile(false),east=profile(true),character=[];[idle,north,west,east].forEach((f,i)=>character.push(stride(f,true,i>1),f,stride(f,false,i>1),f));
const fishSpecs=[
 ['marmalade','Marmalade','ranchu','#f7a844','#f8d889','#ba5936','orange'],['lemon-drop','Lemon Drop','ranchu','#f6d165','#fff0bb','#b88747','lemon'],['dumpling','Dumpling','ranchu','#e8e4cb','#fff6d8','#aaa9a0','cap'],['milk-tea','Milk Tea','ranchu','#c49469','#f1d8a7','#805847','saddle'],['sesame','Sesame','ranchu','#50555a','#839095','#2c343e','dark'],['confetti','Confetti','ranchu','#e9d6a9','#fff0cd','#ae8969','calico'],['peaches','Peaches','ranchu','#efb28a','#ffe0b3','#b87264','cheeks'],['inkblot','Inkblot','ranchu','#e6e4d8','#fff4da','#a5b5b5','panda'],
 ['ember','Ember','oranda','#eb8b3f','#ffd477','#a74332','orange'],['mooncap','Mooncap','oranda','#e9e7d5','#fff8e3','#9dabae','cap'],['caramel','Caramel','oranda','#b08459','#ddbd87','#6b4d41','saddle'],['speckles','Speckles','oranda','#e2d3ae','#fff2d4','#9d9fa0','calico'],['sunset','Sunset','oranda','#efaa6b','#ffe2ab','#b85c53','redtail'],['snowball','Snowball','oranda','#e8ede8','#fff9df','#aabdbc','white'],['pepper','Pepper','oranda','#697d88','#a7b8b7','#3b455c','dark'],['tangerine','Tangerine','oranda','#f3af43','#ffe38a','#be673d','cheeks']
].map(([id,name,variety,body,light,shade,pattern],row)=>({id,name,variety,body,light,shade,pattern,row}));
function fish(f,top,phase){const a=new Raster(32,32),o='#423642',p=phase?1:0;const tail=f.variety==='oranda'?1:0; const shape=f.row%4;
 // Side form faces left; top form faces up. Tail fans move about their attached peduncle.
 if(!top){
 a.poly([[23,15],[28,8-p-tail],[30,8-p],[29,15],[31,21+p],[28,24+p],[23,19]],o);a.poly([[23,16],[28,11-p-tail],[28,16],[29,21+p],[27,22+p],[23,18]],f.body);a.line(25,17,28,13-p,f.light);a.line(25,18,28,21+p,f.light);
 if(f.variety==='oranda'){a.poly([[12,11],[16,5],[20,6],[23,14]],o);a.poly([[14,11],[17,7],[19,8],[21,13]],f.body);a.line(17,8,18,11,f.light);}
 a.poly([[6,10],[10,8],[17,8],[23,11],[25,16],[24,20],[20,24],[12,25],[7,22],[4,18],[4,13]],o);a.poly([[7,11],[11,9],[17,9],[22,12],[24,16],[23,20],[19,23],[12,24],[8,21],[5,17],[5,13]],f.body);a.poly([[7,12],[11,10],[17,10],[21,12],[19,15],[13,15],[8,17],[6,16]],f.light);a.poly([[8,21],[14,22],[19,21],[23,18],[23,21],[19,24],[12,24]],f.shade);
 // Puffy headgrowth scallops and compact rounded cheeks, not a stretched carp.
 a.poly([[5,11],[6,8],[9,7],[11,8],[13,7],[16,9],[15,13],[13,15],[7,15]],f.pattern==='cap'?'#dd6b4c':f.body);a.line(6,10,9,9,f.light);a.line(11,9,13,9,f.light);
 applyPattern(a,f,false);
 a.rect(6,15,3,4,o);a.dot(6,15,'#fff9e1');a.dot(8,18,f.shade);a.rect(3,18,3,3,f.shade);a.rect(3,18,2,1,f.light);a.dot(4,19,o);a.dot(5,20,f.body);a.dot(8,20,f.light);
 a.poly([[15,18],[19+p,19],[18+p,23],[15,21]],f.shade);a.line(16,19,18+p,20,f.light);a.poly([[12,24],[16,24],[14,27],[11,26]],o);a.line(12,25,14,25,f.body);
 }else{
 a.poly([[13,22],[7-p-tail,28],[8,30],[14,28],[16,25],[18,28],[24+p,30],[25,27],[19,21]],o);a.poly([[14,23],[9-p,28],[14,26],[16,24],[19,27],[23+p,28],[18,22]],f.body);a.line(12,26,10,28,f.light);a.line(19,26,22,28,f.light);
 a.poly([[10,7],[13,5],[19,5],[22,8],[24,12],[23,18],[20,23],[12,23],[8,18],[7,12]],o);a.poly([[11,7],[14,6],[18,6],[21,8],[23,13],[22,18],[19,22],[13,22],[9,17],[8,12]],f.body);a.poly([[12,8],[16,7],[19,9],[18,18],[15,21],[11,18],[10,12]],f.light);a.poly([[21,10],[23,13],[22,18],[19,22],[16,22],[19,18]],f.shade);
 a.poly([[10,8],[10,5],[12,3],[15,4],[18,3],[21,5],[21,9],[19,11],[12,11]],f.pattern==='cap'?'#d3664d':f.body);a.line(12,5,14,5,f.light);a.line(17,5,19,6,f.light);applyPattern(a,f,true);
 a.rect(8,9,2,3,o);a.dot(8,9,'#fff8da');a.rect(22,9,2,3,o);a.dot(22,9,'#fff8da');a.rect(15,3,2,2,f.shade);a.dot(15,3,f.light);
 a.poly([[8,13],[4-p,15],[6-p,18],[9,17]],f.shade);a.line(5-p,15,7,16,f.light);a.poly([[23,13],[27+p,15],[25+p,18],[22,17]],f.shade);a.line(24,16,26+p,15,f.light);
 if(f.variety==='oranda'){a.line(16,12,16,20,o);a.line(17,13,17,19,f.shade);a.line(15,12,15,18,f.light);}
 }
 // Individual morphology cues survive silhouette mode: short split tail, broad tail,
 // pom-pom headgrowth, or side cheek fans. These are original game individuals.
 if(top){if(f.row%8>=4){a.rect(8,28,3,2,'transparent');a.rect(21,28,3,2,'transparent');a.rect(14,26,4,2,f.shade);}if(shape===1){a.poly([[10,25],[7,26],[8,29],[13,27]],o);a.line(9,27,11,26,f.light);a.poly([[21,25],[24,26],[23,29],[18,27]],o);a.line(20,26,22,27,f.body);}if(shape===2){a.rect(12,2,3,2,f.body);a.rect(17,2,3,2,f.body);}if(shape===3){a.poly([[8,11],[5,10],[4,12],[6,14],[9,14]],f.shade);a.poly([[23,11],[26,10],[27,12],[25,14],[22,14]],f.shade);}}
 return a;
}
function fishFront(f,phase){const a=new Raster(32,32),o='#423642';
 // Paired side fins and fan-tail peeking below the round body.
 a.poly([[8,22],[5,28],[11,27],[15,29],[20,27],[26,28],[23,22]],o);a.poly([[9,23],[8,26],[13,25],[16,27],[20,25],[23,26],[22,23]],f.body);
 a.poly([[7,15],[2,13+phase],[1,17],[4,20],[8,19]],o);a.poly([[24,15],[29,13+phase],[30,17],[27,20],[23,19]],o);a.line(3,16,6,18,f.light);a.line(25,18,28,16,f.light);
 a.poly([[9,7],[14,5],[18,5],[23,7],[26,13],[26,20],[22,25],[9,25],[5,20],[5,13]],o);a.poly([[10,8],[14,6],[18,6],[22,8],[25,13],[25,19],[21,24],[10,24],[6,19],[6,13]],f.body);a.poly([[10,10],[15,8],[20,10],[21,17],[18,22],[10,22],[7,18],[8,13]],f.light);a.poly([[22,11],[25,14],[25,19],[21,24],[12,24],[10,22],[20,22],[23,18]],f.shade);
 a.poly([[7,10],[7,7],[10,4],[13,5],[15,3],[18,4],[20,4],[24,7],[24,10],[21,13],[10,13]],f.pattern==='cap'?'#dc7151':f.body);a.line(10,6,12,6,f.light);a.line(15,5,18,6,f.light);a.line(21,7,22,8,f.light);applyPattern(a,f,true);
 // Two expressive eyes and a puckered circular mouth; no smiling human teeth.
 for(const x of [8,21]){a.rect(x,13,3,4,o);a.dot(x,13,'#fff8e5');a.dot(x+2,16,f.shade);}
 a.oval(12,16,8,7,f.shade);a.oval(13,17,6,5,f.light);a.oval(14,18,4,3,o);a.dot(10,19,f.body);a.dot(21,19,f.body);
 return a;
}
function tubCloseup(){const a=new Raster(240,160);a.rect(0,0,240,160,'#8e8c70');a.oval(3,3,234,154,'#14232b');a.oval(7,6,226,146,'#45565b');a.oval(12,10,216,137,'#182e38');a.oval(17,14,206,128,'#29555d');a.oval(24,19,193,113,'#356a6e');a.oval(30,24,180,99,'#3e7373');a.line(65,14,174,14,'#749592');a.line(64,145,172,145,'#0b1924');a.line(65,147,171,147,'#53656a');
 for(const [x,y,sz] of [[38,56,1.3],[50,49,1.5],[64,43,1.0],[181,120,1.3],[194,113,1.2],[202,101,.95],[181,44,1.1],[193,56,.9],[171,39,.75],[35,83,.85]])plant(a,x,y,sz);for(const [x,y] of [[58,34],[65,37],[72,33],[76,38],[170,122],[162,124],[155,120]]){a.oval(x,y,7,4,'#6b995e');a.dot(x+2,y,'#b4c77a');a.dot(x+3,y+3,'#426d55');}a.line(56,113,72,113,'#699292');a.line(74,115,85,115,'#699292');a.line(137,37,151,37,'#63928f');a.line(130,39,137,39,'#63928f');return a;}
function applyPattern(a,f,top){const mask=Array.from(a.p);const shape=(pts,c)=>{const p=new Raster(32,32);p.poly(pts,c);for(let y=7;y<24;y++)for(let x=6;x<24;x++)if(mask[(y*32+x)*4+3]&&color(p,x,y)&&color(a,x,y)!=='#423642')a.dot(x,y,c);};
 if(f.pattern==='panda'){shape(top?[[9,12],[15,11],[17,14],[15,17],[9,16]]:[[10,10],[16,10],[18,14],[15,17],[10,15]],'#3e454f');shape([[19,18],[24,18],[24,23],[19,22]],'#3e454f');}
 if(f.pattern==='calico'){shape([[14,9],[19,10],[21,13],[16,14],[13,12]],'#d78651');shape([[8,19],[11,18],[14,20],[13,23],[10,23]],'#e09a53');for(const [x,y] of [[10,12],[12,15],[18,17],[20,20],[15,21],[22,14]])a.rect(x,y,1+(x%2),2,'#546675');}
 if(f.pattern==='saddle'){shape(top?[[10,13],[23,13],[23,17],[10,17]]:[[14,9],[19,9],[21,15],[18,19],[15,17]],f.shade);}
 if(f.pattern==='cheeks'){shape(top?[[9,8],[13,8],[13,12],[9,12]]:[[6,17],[10,18],[12,21],[8,22]],'#e27e6f');}
 if(f.pattern==='redtail'){shape([[19,17],[25,15],[25,23],[20,24]],'#d86a50');}
 if(f.pattern==='lemon'){shape([[6,8],[14,7],[15,11],[9,13]],'#e7ae36');}
}
function tinyFish(f,top,phase){const a=new Raster(16,16),o='#34404a',p=phase?1:0;
 // Independently drawn16px clusters for world props; no scaling of32px studies.
 if(top){a.poly([[6,10],[3-p,14],[6,13],[8,12],[10,13],[13+p,14],[10,10]],o);a.line(5,13,7,11,f.body);a.line(9,11,11,13,f.light);a.poly([[5,3],[10,3],[12,5],[12,9],[10,12],[5,12],[3,9],[3,6]],o);a.poly([[5,4],[10,4],[11,6],[11,9],[9,11],[6,11],[4,9],[4,6]],f.body);a.rect(5,5,4,5,f.light);a.rect(6,2,4,3,f.pattern==='cap'?'#df7751':f.body);a.dot(6,2,f.light);a.dot(3,6,'#232e3b');a.dot(12,6,'#232e3b');a.line(3,8,1,9+p,f.shade);a.line(12,8,14,9+p,f.shade);if(f.variety==='oranda')a.line(8,6,8,10,f.shade);if(f.pattern==='calico'){a.rect(8,5,2,2,'#dc915b');a.dot(5,9,'#596977');a.dot(9,8,'#596977');}if(f.pattern==='panda'){a.rect(5,6,3,2,'#475361');a.rect(9,9,2,2,'#475361');}if(f.pattern==='saddle')a.rect(4,7,7,2,f.shade);
 }else{a.poly([[11,7],[14,3-p],[15,5],[14,8],[15,12],[13,11],[11,9]],o);a.line(12,8,14,5,f.body);a.line(12,9,14,11,f.light);if(f.variety==='oranda')a.poly([[6,5],[9,2],[10,5]],f.shade);a.poly([[3,5],[7,4],[10,5],[12,7],[12,10],[9,12],[4,12],[2,10],[1,7]],o);a.poly([[3,6],[7,5],[10,6],[11,8],[10,10],[8,11],[4,11],[2,9],[2,7]],f.body);a.rect(4,6,5,2,f.light);a.line(5,11,9,11,f.shade);a.rect(2,5,4,2,f.pattern==='cap'?'#dd7151':f.body);a.dot(3,5,f.light);a.dot(2,8,'#232e3b');a.dot(3,8,'#fff4d3');a.dot(1,10,f.shade);a.line(7,9,8,10+p,f.shade);if(f.pattern==='panda')a.rect(6,6,3,3,'#475361');if(f.pattern==='calico'){a.rect(7,6,2,2,'#dc915b');a.dot(5,9,'#596977');a.dot(9,9,'#596977');}if(f.pattern==='saddle')a.rect(6,5,3,5,f.shade);}
 return a;}
function plant(a,x,y,s=1){const d='#294f46',m='#447d55',h='#82ad68';a.line(x,y,x,y-14*s,d);a.poly([[x,y-2],[x-8*s,y-7*s],[x-7*s,y-12*s],[x-2*s,y-9*s]],m);a.line(x-6*s,y-10*s,x-2*s,y-6*s,h);a.poly([[x,y-4],[x+7*s,y-8*s],[x+8*s,y-14*s],[x+3*s,y-12*s]],m);a.line(x+5*s,y-11*s,x+2*s,y-7*s,h);a.poly([[x,y-8*s],[x-3*s,y-16*s],[x,y-20*s],[x+3*s,y-15*s]],m);a.line(x,y-17*s,x,y-11*s,h);}
function tub(variant=0){const a=new Raster(96,64);a.oval(2,22,92,39,'#45484b');a.oval(3,13,90,48,'#19252d');a.rect(4,27,88,17,'#19252d');a.oval(1,5,94,43,'#101d26');a.oval(4,7,88,36,'#45535a');a.oval(7,10,82,29,'#182f37');a.oval(10,11,76,25,'#29535a');a.oval(13,12,70,19,'#37686a');a.line(20,11,65,11,'#75948a');a.line(16,12,19,12,'#75948a');a.line(8,24,9,31,'#6d7b79');a.line(7,33,14,39,'#56676b');a.line(15,40,27,43,'#56676b');a.line(28,44,63,44,'#56676b');a.line(13,49,19,53,'#2b3b44');a.line(20,54,72,54,'#2b3b44');for(const x of [12,26,70,83])a.line(x,42,x,47,'#0d1922');plant(a,18,28,.8);plant(a,25,25,.9);plant(a,31,22,.6);plant(a,68,25,.9);plant(a,77,26,.8);plant(a,83,27,.55);if(variant%2){plant(a,43,21,.55);plant(a,54,22,.65);}if(variant>=2){plant(a,19,34,.6);plant(a,71,33,.7);}for(const [x,y] of [[33,16],[38,19],[55,15],[60,17],[19,30],[25,32],[29,28],[67,28],[75,30],[79,25],[37,14],[59,20]]){a.oval(x,y,5,3,'#729268');a.dot(x+1,y,'#a7bc76');}a.line(42,29,51,29,'#699798');a.line(53,31,59,31,'#699798');a.rect(36,47,23,9,'#121f28');a.line(38,49,56,49,'#4d5e64');return a;}
function tank(){const a=new Raster(96,64);a.rect(3,15,90,44,'#283a40');a.rect(4,16,88,2,'#8b9c8d');a.rect(7,20,82,24,'#3b8790');a.rect(8,21,80,12,'#68aeb0');a.rect(8,36,80,8,'#416f76');a.rect(8,43,80,3,'#bdac78');a.line(11,24,18,24,'#b7d6cb');a.line(68,25,82,25,'#b7d6cb');a.line(12,26,16,26,'#b7d6cb');plant(a,20,43,.8);plant(a,71,43,.8);a.rect(78,22,7,15,'#293e49');a.rect(80,22,2,14,'#536971');a.line(81,18,81,22,'#333b42');a.rect(4,47,88,11,'#716452');a.rect(7,50,39,6,'#4e534a');a.rect(49,50,39,6,'#4e534a');a.rect(42,51,2,3,'#c7b481');a.rect(52,51,2,3,'#c7b481');a.rect(5,58,86,2,'#25363b');a.rect(7,60,80,2,'#81755b');a.rect(7,18,1,27,'#a9c7ba');a.rect(87,18,2,27,'#315765');a.rect(3,13,90,3,'#d2d3a9');a.rect(4,12,88,1,'#5e776d');return a;}
function floor(){const a=new Raster(32,32);a.rect(0,0,32,32,'#bba985');for(let y=0;y<32;y+=8){a.rect(0,y,32,1,'#968c72');for(let x=(y%16===0?0:8);x<32;x+=16){a.rect(x,y,1,8,'#968c72');a.rect(x+2,y+2,12,1,'#c8b793');}}a.rect(7,5,3,1,'#afa080');a.rect(24,21,3,1,'#afa080');return a;}
function tile(kind){if(kind===0||kind===1){const a=floor();if(kind===1){a.rect(10,8,2,2,'#a99a7d');a.rect(25,16,2,1,'#d0bc94');}return a;}const a=new Raster(32,32);a.rect(0,0,32,32,'#81a9a0');a.rect(3,3,26,24,'#acd0bb');a.poly([[3,3],[21,3],[3,21]],'#c1debf');a.rect(0,0,3,32,'#466a60');a.rect(3,0,1,32,'#d0dec0');a.rect(29,0,3,32,'#466a60');a.rect(0,0,32,3,'#587e6e');a.rect(0,29,32,3,'#587e6e');a.line(6,24,23,7,'#bddbcb');if(kind===3){a.rect(0,23,32,5,'#4b695e');a.rect(0,28,32,4,'#91866a');}if(kind===4){a.rect(0,0,32,32,'#3b6656');a.rect(2,0,4,32,'#91b593');a.rect(8,0,2,32,'#c6d5a9');a.rect(28,0,4,32,'#254f48');}if(kind===5){const f=floor();a.blit(f,0,0);a.rect(0,0,32,6,'#4a6559');a.rect(0,6,32,4,'#d1c4a0');a.rect(1,11,30,15,'#779282');a.rect(3,13,26,11,'#a4b59a');a.line(4,15,27,15,'#567b6b');a.line(4,21,27,21,'#567b6b');}if(kind===6){a.rect(0,0,32,32,'#668878');a.rect(0,25,32,7,'#b4a17e');a.rect(1,25,30,2,'#d3bd93');}if(kind===7){const f=floor();a.blit(f,0,0);a.oval(4,14,24,15,'#66594b');a.rect(8,18,16,11,'#997652');a.rect(7,16,18,5,'#b99260');plant(a,16,20,.75);}return a;}
function greenhouse(tiles){const a=new Raster(320,192); // Original 10×6 assembly, visible roof planes and short front wall.
 a.poly([[10,57],[41,11],[279,11],[310,57],[310,172],[10,172]],'#33584f');a.poly([[17,56],[44,16],[276,16],[303,56]],'#94bcb0');a.poly([[17,58],[303,58],[290,78],[30,78]],'#5d9b8c');
 for(let x=42;x<292;x+=32){a.line(x,17,x-24,55,'#517d70');a.line(x+2,17,x-22,55,'#d1dfb9');a.line(x-24,56,x-12,75,'#afd0ab');}a.rect(39,10,242,4,'#385f52');a.rect(42,11,236,2,'#cfdaa9');a.rect(14,55,292,5,'#3c6959');a.rect(16,55,288,2,'#c4d5a9');
 for(let x=16;x<304;x+=32){a.blit(tiles[2],x,79);a.blit(tiles[3],x,111);a.blit(tiles[6],x,143);}a.rect(15,77,290,3,'#244f46');a.rect(14,80,4,96,'#3c6857');a.rect(302,80,4,96,'#31564b');
 // Door on center-right cell: exterior anchor x160; keep one32px threshold.
 a.rect(144,111,32,64,'#294e45');a.rect(147,114,26,48,'#6c9b85');a.rect(150,117,20,37,'#a9c7ab');a.rect(149,117,2,38,'#dbe3ba');a.rect(169,118,2,37,'#466e61');a.rect(168,143,3,3,'#deb95e');a.rect(148,158,24,4,'#426953');a.rect(144,172,32,6,'#d2c5a0');a.rect(142,177,36,5,'#8f8a70');a.line(143,177,176,177,'#e0d3b0');
 a.rect(112,84,96,22,'#456f52');a.rect(114,86,92,18,'#eadbae');a.line(115,87,204,87,'#fff0c3');
 // Tiny original goldfish sign, centered and readable without rasterizing font.
 const sign=fish(fishSpecs[0],false,0);a.blit(sign,144,80);
 // Foundation contact with explicit boundary paving within last32px cell.
 for(let x=17;x<303;x+=32){if(x+31>=144&&x<=176)continue;a.rect(x,174,31,3,'#c7b58e');a.rect(x,177,31,2,'#5e6857');}a.blit(tile(7),38,145);a.blit(tile(7),250,145);return a;}
async function save(name,r){await r.save(path.join(out,name+'.png'));const palette=[null];const pixels=[];for(let y=0;y<r.h;y++)for(let x=0;x<r.w;x++){const c=color(r,x,y);let idx=palette.indexOf(c);if(idx<0){idx=palette.length;palette.push(c);}pixels.push(idx);}const data={format:'fmw-sprite',version:1,name,width:r.w,height:r.h,palette,frames:[{name:'native',ticks:8,pixels}]};fs.writeFileSync(path.join(source,name+'.sprite.json'),JSON.stringify(data)+'\n');return {path:`assets/review/luke-greenhouse/${name}.png`,width:r.w,height:r.h,paletteColors:palette.length-1,sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(out,name+'.png'))).digest('hex'),...bounds(r)};}
const lukeSheet=new Raster(128,256);character.forEach((f,i)=>lukeSheet.blit(f,(i%4)*32,Math.floor(i/4)*64));const fishSheet=new Raster(128,512),silhouetteSheet=new Raster(64,512);fishSpecs.forEach(f=>{for(let p=0;p<2;p++){fishSheet.blit(fish(f,false,p),p*32,f.row*32);const top=fish(f,true,p);fishSheet.blit(top,64+p*32,f.row*32);const sh=new Raster(32,32);for(let y=0;y<32;y++)for(let x=0;x<32;x++)if(color(top,x,y))sh.dot(x,y,'#16373c');silhouetteSheet.blit(sh,p*32,f.row*32);}});
const tinySheet=new Raster(64,256);fishSpecs.forEach(f=>{for(let p=0;p<2;p++){tinySheet.blit(tinyFish(f,true,p),p*16,f.row*16);tinySheet.blit(tinyFish(f,false,p),32+p*16,f.row*16);}});
const tubVariants=new Raster(384,64);for(let i=0;i<4;i++)tubVariants.blit(tub(i),i*96,0);
const frontSheet=new Raster(64,512);fishSpecs.forEach(f=>{frontSheet.blit(fishFront(f,0),0,f.row*32);frontSheet.blit(fishFront(f,1),32,f.row*32);});
const tiles=Array.from({length:8},(_,i)=>tile(i)),tileSheet=new Raster(256,32);tiles.forEach((t,i)=>tileSheet.blit(t,i*32,0));
const meta={schemaVersion:1,status:'awaiting-user-visual-review',task:'M1.LG1',coordinateSystem:'native top-down integer pixels',character:{frame:[32,64],anchor:[16,64],directions:['south','north','west','east'],columns:['strideA','idle','strideB','idle'],holds:[8,8,8,8],tickMs:280896/16777216*1000,frames:character.map(bounds)},fish:{frame:[32,32],columns:['side0','side1','top0','top1'],silhouetteColumns:['top0','top1'],frontColumns:['front0','front1'],topOrientation:'north',sideOrientation:'west',world:{frame:[16,16],columns:['top0','top1','side0','side1'],note:'Independently authored native world clusters, never downsized32px sprite'},individuals:fishSpecs},tiles:{frame:[32,32],columns:['brick-floor-a','brick-floor-b','glass-wall','wall-base','green-rib','door-threshold','foundation','potted-plant']},props:{tub:{extent:[96,64],groundFootprint:[3,2],sortAnchor:[48,64]},tank:{extent:[96,64],groundFootprint:[3,2],sortAnchor:[48,64]},greenhouse:{extent:[320,192],doorRectangle:[144,111,32,64],threshold:[144,172,32,10]}},assets:{}};
for(const [id,r] of Object.entries({'luke':lukeSheet,'luke-idle':idle,'fish':fishSheet,'silhouettes':silhouetteSheet,'fish-front':frontSheet,'fish-world':tinySheet,'tub-closeup':tubCloseup(),'tub':tub(),'tub-variants':tubVariants,'tank-wall':tank(),'tiles':tileSheet,'greenhouse':greenhouse(tiles)}))meta.assets[id]=await save(id,r);
fs.writeFileSync(path.join(source,'luke.masks.json'),JSON.stringify({coordinateSystem:'native top-down; index=y*32+x',masks},null,2)+'\n');
fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify(meta,null,2)+'\n');
const contact=new Raster(320,256);contact.rect(0,0,320,256,'#d9dcc1');for(let d=0;d<4;d++)contact.blit(character[d*4+1],12+d*44,0);contact.blit(tub(),201,7);contact.blit(tank(),201,76);fishSpecs.forEach((f,i)=>contact.blit(fishFront(f,0),(i%8)*38+8,144+Math.floor(i/8)*42));await contact.save(path.join(out,'contact-native.png'));await contact.scale(3).save(path.join(out,'contact-3x.png'));
const checks={binaryAlpha:true,idle:bounds(idle),idleAnatomicalSymmetry:{},fishCount:fishSpecs.length,characterFrameCount:character.length};for(const [key,ids] of Object.entries(masks)){const s=new Set(ids);checks.idleAnatomicalSymmetry[key]=ids.every(i=>s.has(Math.floor(i/32)*32+31-i%32));if(!checks.idleAnatomicalSymmetry[key])throw Error('Asymmetric mask '+key);}for(const r of [lukeSheet,fishSheet,silhouetteSheet])for(let i=3;i<r.p.length;i+=4)if(![0,255].includes(r.p[i]))throw Error('Nonbinary alpha');fs.writeFileSync(path.join(out,'checks.json'),JSON.stringify(checks,null,2)+'\n');console.log(JSON.stringify(checks));
