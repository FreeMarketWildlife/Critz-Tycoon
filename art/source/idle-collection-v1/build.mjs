// Authored native cells. No image sampling, quantization, antialiasing or generated overlays.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {describe,readProjectData} from '../../../sprite-editor/model.js';
const require=createRequire(import.meta.url);
const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const home=path.dirname(new URL(import.meta.url).pathname), repo=path.resolve(home,'../../..');
const out=path.join(repo,'assets/review/idle-collection-v1');
const boy=JSON.parse(fs.readFileSync(path.join(repo,'art/source/hero-boy-v1/idle.sprite.json')));
const scaffold=JSON.parse(fs.readFileSync(path.join(repo,'sprite-editor/templates/basic-character.json')));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const boyPNG=fs.readFileSync(path.join(repo,'assets/characters/hero-boy-v1/idle-south.png'));
if(sha(boyPNG)!=='0099dd331ae2c2d995663328e52763e8b10b1df0d36854d59676ee0ac52f7883')throw Error('Approved boy baseline changed');
const C={ink:'#201008',skin:'#a87038',shade:'#784820',light:'#c48e4a',cream:'#f7edcc',white:'#f8f8f8',hair:'#28252b',hairMid:'#3b3030',hairLit:'#594333',hairHi:'#795336',navy:'#184080',navyDark:'#102644',coral:'#fc7858',redShade:'#c34d48',gold:'#dfad49',teal:'#398f98'};
class Raster {
 constructor(h=64){this.w=32;this.h=h;this.a=Array(32*h).fill(null);this.parts=Array(32*h).fill(null);this.masks={};}
 p(x,y,c,part='detail'){if(x<0||y<0||x>=32||y>=this.h)throw Error(`Clipped pixel ${x},${y}`);this.a[y*32+x]=c;this.parts[y*32+x]=c?part:null;}
 r(l,t,r,b,c,part){for(let y=t;y<=b;y++)for(let x=l;x<=r;x++)this.p(x,y,c,part);}
 stamp(x,y,rows,pal,part='hair'){rows.forEach((row,j)=>[...row].forEach((v,i)=>{if(v!=='.'&&v!==' ') {if(!pal[v])throw Error(`Unknown ${v}`);this.p(x+i,y+j,pal[v],part);}}));}
 copy(){const b=new Raster(this.h);b.a=this.a.slice();b.parts=this.parts.slice();b.masks=structuredClone(this.masks);return b;}
}
const hp={o:C.ink,d:C.hair,m:C.hairMid,l:C.hairLit,h:C.hairHi,t:C.coral,k:C.redShade};
function preserveMask(a,name,test){a.masks[name]=a.a.flatMap((c,i)=>c&&test(i%32,Math.floor(i/32),a.parts[i])?[i]:[]);}
function body(a,{adult=false,skin=C.skin,shade=C.shade,shirt=C.coral,shirtShade=C.redShade,pants=C.navy,shoe='#743248',outfit='stripe'}={}){
 const src=boy.frames[0].pixels;
 const remap={2:shirt,13:C.cream,14:C.ink,16:shade,17:skin,9:pants,34:C.hairMid,35:shoe,44:shoe,32:C.hair};
 for(let y=adult?43:45;y<=61;y++){
  const sy=adult&&y<=54?45+Math.floor((y-43)*10/12):y;
  for(let x=0;x<32;x++){
   const v=src[sy*32+x];if(!v)continue;
   const part=sy>=55?'legs':((v===17||v===16)&&sy>=48?'hands':(x<9||x>22?'arms':'torso'));
   let c=remap[v]||boy.palette[v];
   if(v===2||v===13){
    if(outfit==='solid')c=(x<11?shirt:x>21?shirtShade:shirt);
    if(outfit==='jacket')c=x>=13&&x<=18?C.cream:(x===12||x===19?shirtShade:shirt);
    if(outfit==='coat')c=x>=13&&x<=18?shirt:(x===12||x===19?'#c4c5af':C.cream);
    if(outfit==='apron')c=x>=10&&x<=21?shirt:(x<10||x>21?C.gold:shirtShade);
   }
   // Refine the shirt's interior hem without altering the approved body silhouette.
   if(v===14&&sy===53&&x>=12&&x<=19)c=shirtShade;
   if(v===13&&sy>=60)c=C.cream;
   a.p(x,y,c,part);
  }
 }
 preserveMask(a,'body',()=>true);
 preserveMask(a,'arms',(x,y,p)=>p==='arms');preserveMask(a,'hands',(x,y,p)=>p==='hands');preserveMask(a,'legs',(x,y,p)=>p==='legs');
}
function skull(a,{adult=false,skin=C.skin,shade=C.shade,light=C.light}={}){
 const dy=adult?-2:0,src=scaffold.frames[0].pixels;
 const head=[];
 for(let y=26;y<=46;y++)for(let x=0;x<32;x++){
  const v=src[y*32+x];if(!v)continue;
  // Row45/46 contain neck and shoulder colors; only copy the actual blue/outline head.
  if(y>=45&&(x<10||x>21))continue;
  if(![9,10,11,13,14].includes(v))continue;
  let c=v===14?C.ink:v===9?shade:v===10?shade:skin;
  if(v===11&&x<=8&&y>=36)c=light;
  a.p(x,y+dy,c,'skull');head.push((y+dy)*32+x);
 }
 a.masks.skull=head;
 for(const x of [12,18]){a.r(x,38+dy,x+1,41+dy,C.ink,'eyes');a.p(x,38+dy,C.cream,'eyes');}
 a.masks.eyes=[];for(const x of [12,18])for(let y=38+dy;y<42+dy;y++)for(let i=0;i<2;i++)a.masks.eyes.push(y*32+x+i);
}
function shell(a,dy=0,pal=hp){
 // Deliberately stepped crown above the bare cranium, with separated temple locks.
 a.stamp(4,26+dy,[
 '.........oooooo.........','......ooollllmmmoo......','....oolllllmmmmmmmmoo....',
 '...olllllmmmmddddmmmmo...','..ollllmmmddddddddmmmo..','..olllmmdddddddddddddmo.',
 '.olllmmdddmmmmddddddddmo.','.ollmmddmmmllmmdddddddmo.','ollmddmmmlllllmmdddddddmo',
 'olmmddmlloooollmdddmdddmo','ommdomlo....ollmddomdddmo','omdomlo......ollmoo.omdmo',
 'omdolo........olo...omdo.','omdo................odo.','odo..................o..'
 ],pal);
}
function puff(a,x,y,pal=hp,flip=false){
 const rows=['...oooo...','..olllmo..','.olhhmmdo.','olhllmmddo','olllmmdddo','ollmmdddmo','ommmdddmoo','.omdddmoo.','..omddoo..','...ooo....'];
 a.stamp(x,y,flip?rows.map(s=>[...s].reverse().join('')):rows,pal);
}
function twinPuffs(a,{dy=0,mature=false,pal=hp}={}){
 shell(a,dy,pal);puff(a,3,21+dy,pal);puff(a,19,21+dy,pal,true);
 a.stamp(9,29+dy,['.tt','ttk','tk.'],pal);a.stamp(20,29+dy,['tt.','ktt','.kt'],pal);
 if(mature){
  // Swept-back fringe exposes the forehead; hair highlights remain asymmetric.
  for(let y=34+dy;y<=37+dy;y++)for(let x=9;x<=22;x++)if(a.parts[y*32+x]==='hair')a.p(x,y,C.skin,'skull');
  a.r(7,39+dy,7,40+dy,C.gold,'accessory');a.r(24,39+dy,24,40+dy,C.gold,'accessory');
 }
}
function bob(a,dy=0,pal=hp){
 shell(a,dy,pal);
 for(let y=36+dy;y<=43+dy;y++){a.r(4,y,5,y,pal.d,'hair');a.r(26,y,27,y,pal.d,'hair');}
 a.r(5,44+dy,7,44+dy,pal.o,'hair');a.r(24,44+dy,26,44+dy,pal.o,'hair');
 a.stamp(6,30+dy,['....llllmm','...llllmmm','..llllmmdd','.llllmmdd.','llllmmdd..','llmmmdd...','lmmdd.....','mdd.......'],pal);
}
function bun(a,dy=0,pal=hp){bob(a,dy,pal);puff(a,11,20+dy,pal);a.r(12,28+dy,19,28+dy,pal.t,'hair');}
function glasses(a,y=36,color='#293445'){
 for(const x of [10,17]){a.r(x,y-1,x+4,y-1,color,'accessory');a.r(x,y+4,x+4,y+4,color,'accessory');a.r(x,y,x,y+3,color,'accessory');a.r(x+4,y,x+4,y+3,color,'accessory');}
 a.r(15,y,16,y,color,'accessory');a.p(11,y,C.white,'accessory');a.p(18,y,C.white,'accessory');
}
function hat(a,dy=-2){
 const p={o:C.ink,l:'#e4d09a',m:'#bfab77',s:'#8b8159',g:'#3b5943',h:'#78966b'};
 a.stamp(2,24+dy,[
 '..........ooooooo...........','........oollllllloo.........','.......olllllllmmmmo........',
 '......ollllllmmmmmmmo.......','.....olllllmmmmmmmmmo.......','....oghhhhgggggggggggo......',
 '..oolmmmmmmmmmmmmmmmmmoo....','.olllllllllmmmmmmmmmmmmmmoo.','..ossssssssssssssssssssso...','....oooooooooooooooooooo....'
 ],p,'headwear');
}
function croppedHair(a,dy=0,pal=hp){
 a.stamp(5,25+dy,['.....oooooo...........','...oollhhlloooo.......','..olhhlmmmmmmddoo.....','.ollmmmmmddddddddo....','ollmmdddddddddddddo...','olmmdddddddddddddddo..','ommmdddddddddddddddo..','omdddddddddddddddddo..','odddoooooooodddddddo..','oddo........oooddddo..','odo............oddo..','odo.............odo..','oo...............oo..'],pal);
}
const characters=[];
function human(id,label,role,opts,hair,detail){
 const a=new Raster();body(a,opts);skull(a,opts);const bare=a.copy(),eyeY=opts.adult?36:38;
 hair(a,opts.adult?-2:0);
 // The two eyes retain identical visible dimensions. Bangs cannot erase one eye.
 for(const x of [12,18])for(let y=eyeY-1;y<=eyeY+4;y++)for(let xx=x-1;xx<=x+2;xx++){
  const i=y*32+xx;if(a.parts[i]==='hair')a.p(xx,y,bare.a[i],bare.parts[i]);
 }
 if(opts.adult){
  // Full trousers and simple shoes distinguish adult dress without longer shins.
  for(let y=57;y<=59;y++)for(let x=7;x<=24;x++)if(a.a[y*32+x]&&a.a[y*32+x]!==C.ink)a.p(x,y,opts.pants,'legs');
  for(let x=8;x<=23;x++)if(a.a[60*32+x]===C.cream)a.p(x,60,opts.shoe,'legs');
 }
 detail?.(a);characters.push({id,label,role,a,kind:'character',notes:opts.adult?'Adult original adaptation: eye row36, compact torso extended upward by two cells; feet unchanged.':'Child body uses approved V1 occupied cells from row45 down; original hairstyle and clothing.'});return a;
}
human('hero-girl','Girl Hero','Player-named Black child',{outfit:'stripe',shoe:'#80394e'},a=>twinPuffs(a),a=>{
 // Pinker coral and burgundy footwear retain the selected concept's identity.
 for(let i=0;i<a.a.length;i++){if(a.a[i]===C.coral)a.a[i]='#fa8078';if(a.a[i]===C.redShade)a.a[i]='#c95662';}
});
human('professor-nugget','Professor Nugget','Herpetologist and mentor',{adult:true,skin:'#d29b68',shade:'#ad714f',light:'#edbb83',outfit:'coat',shirt:'#708661',pants:'#6c6043',shoe:'#514539'},(a,dy)=>{
 shell(a,dy,{...hp,d:'#9aa6a4',m:'#bcc3b9',l:'#e1e3cf',h:'#edf0df'});hat(a,dy);glasses(a,36);
},a=>{a.r(10,48,11,50,'#9aa69a','accessory');a.p(10,48,C.teal,'accessory');a.r(19,49,21,49,'#b9c4af','accessory');});
human('mom','Mom','Loving parent',{adult:true,outfit:'jacket',shirt:'#ba7082',shirtShade:'#87465e',pants:'#30476a',shoe:'#67464f'},(a,dy)=>twinPuffs(a,{dy,mature:true,pal:{...hp,t:C.gold,k:'#a67436',l:'#4d414e',h:'#64545e'}}),a=>{a.r(14,45,17,45,C.gold,'accessory');a.p(15,46,C.cream,'accessory');});
// Kaid shares the child limb scale. Only pitcher spout and handle break symmetry.
{
 const a=new Raster();body(a,{outfit:'solid',shirt:C.cream,shirtShade:'#c4c5af',skin:'#dca94d',shade:'#ad7735',pants:'#254465',shoe:'#b07538'});
 const p={o:'#163a43',d:'#366d75',m:'#69a9ae',l:'#a5d7d0',h:'#e6f1d8',a:'#df9f3a',b:'#b97c2d',c:'#f5c761'};
 a.stamp(3,26,[
 'ooooo.....................','ohhhlo..oooooooooooo......','omhhmdooohhhhhhhhhhho.....',
 '.omhhmlmmmmmmmmmmmmmo.....','..omlllllmmmmmmmmmmmo.....','...odllllllllllllmdooo...',
 '...odlmmmmmmmmmmmmdoohlo..','...olhmmmmmmmmmmmdoloolo..','..olhhmmmmmmmmmmmdo..olo..',
 '..olhmmmmmmmmmmmmmdo..odo..','..olhccccccccccccmdo..odo..','..olmccaaaaaaaaaamdo..odo..',
 '..olmccaaaaaaaaaamdooolo...','..olmccaaaaaaaaaamdlldo....','...ombbaaaaaaaaabmdoo.....',
 '...odmbbaaaaaaabmdo.......','....odmbbbbbbbbmdo........','.....odmmmmmmmmdo.........','.......oooooooo...........'
 ],p,'vessel');
 for(const x of [12,18]){a.r(x,38,x+1,41,C.ink,'eyes');a.p(x,38,C.cream,'eyes');}
 a.r(14,43,17,43,'#94562c','face');
 a.masks.eyes=[...Array(4)].flatMap((_,j)=>[12,13,18,19].map(x=>(38+j)*32+x));
 characters.push({id:'kaid',label:'Kaid',role:'Pitcher child · Glow n’ Blow',a,kind:'character',notes:'Original teal glass pitcher, amber contents. Spout left and hollow handle right are deliberate asymmetry; paired body/limbs and eyes remain symmetric.'});
}
human('rival-boy','Boy Rival','Player-named rival option',{outfit:'jacket',shirt:'#d7a541',shirtShade:'#aa7936',pants:'#363e54',shoe:'#554231'},(a,dy)=>{
 croppedHair(a,dy);a.stamp(12,24,['..ooo...','.olhmo..','olhmmdo.','ommmdddo','oddodddo'],hp);
},a=>{a.p(10,49,C.cream,'accessory');a.r(13,54,18,54,'#b2925a','accessory');});
human('rival-girl','Girl Rival','Player-named rival option',{outfit:'jacket',shirt:'#786eaf',shirtShade:'#504b7e',pants:'#314665',shoe:'#785387'},(a,dy)=>{
 bob(a,dy);a.r(5,31,26,31,'#bdb0d7','hair');a.stamp(22,28,['pp.pp','plplo','.ooo.'],{p:'#9688bd',l:'#ded4ed',o:C.ink});
});
human('aunt-ember','Aunt Ember','Adult glass artist',{adult:true,outfit:'apron',shirt:'#506b82',shirtShade:'#334956',pants:'#293849',shoe:'#5e4937'},(a,dy)=>{bun(a,dy,{...hp,t:C.gold,k:'#a37236'});glasses(a,36,'#b7c3bc');},a=>{
 a.r(10,45,11,49,'#7998a3','accessory');a.r(20,45,21,49,'#7998a3','accessory');a.r(13,49,18,51,'#354b60','accessory');a.r(14,49,17,49,'#92a9ae','accessory');
});
human('dr-fern','Dr. Fern','Vet',{adult:true,outfit:'coat',shirt:'#388d92',pants:'#245568',shoe:'#304555'},(a,dy)=>bob(a,dy,{...hp,m:'#34333f',l:'#4a4554',h:'#615767'}),a=>{
 a.r(20,46,22,48,'#b25f71','accessory');a.p(21,46,C.cream,'accessory');a.r(20,47,22,47,C.cream,'accessory');a.p(21,48,C.cream,'accessory');
});
human('juniper','Juniper','Critz shopkeeper',{adult:true,skin:'#bf8756',shade:'#885331',light:'#dea871',outfit:'jacket',shirt:'#69895d',shirtShade:'#45664f',pants:'#344564',shoe:'#755437'},(a,dy)=>croppedHair(a,dy),a=>{
 // Beard follows the rounded jaw, never a second enlarged head.
 a.stamp(8,40,['om..........mo','olmo......ommo','.olmm....mmmo.','..olmmmmmmmo..','....oooooo....'],hp,'beard');a.p(10,48,'#d8d6a0','accessory');
});
human('mina','Mina','Drug Store pharmacist',{adult:true,skin:'#b77748',shade:'#865036',light:'#d5a16c',outfit:'coat',shirt:'#8f6c9e',pants:'#475c6c',shoe:'#584352'},(a,dy)=>{bun(a,dy,{...hp,l:'#513a40',h:'#755151',t:'#a8bcaa',k:'#6d8b80'});glasses(a,36,'#685074');},a=>{
 a.r(10,48,11,49,'#a2babc','accessory');a.p(10,48,C.white,'accessory');
});
human('ollie','Ollie','Bike Shop mechanic',{adult:true,skin:'#cd955e',shade:'#996440',light:'#e5b47a',outfit:'solid',shirt:'#358b95',shirtShade:'#24646f',pants:'#344159',shoe:'#b56b45'},(a,dy)=>{
 croppedHair(a,dy);a.stamp(5,25+dy,['......oooooooo......','....ooeeeeeeefoo....','...oeeeeeeefffffo...','..oeeeeeeefffffffo..','.oeeeeeeefffffffffo.','oehhhhhefffffffffdo.','odddddddddddddddddo.','..ooooooooooooooo...'],{o:C.ink,e:'#cf8750',f:'#ae613e',h:'#edb268',d:'#78442f'},'headwear');
},a=>{a.r(10,48,11,49,'#d4d4bd','accessory');a.r(20,49,21,51,'#93afb2','accessory');a.p(20,51,C.ink,'accessory');});

// Compact animal studies use 32×32 storage, species-specific authored silhouettes.
// Small decomposer views are enlarged observational depictions, not physical world scale.
const animals=[];
function animal(id,label,role,x,y,rows,palette,notes){const a=new Raster(32);a.stamp(x,y,rows,palette,'animal');animals.push({id,label,role,a,kind:'animal',notes});return a;}
const ap={o:'#25382c',d:'#627247',m:'#a0af5f',l:'#d8d58c',h:'#f8e8ae',s:'#b59755',e:'#17251c',w:'#fff2d0'};
const gecko=animal('pebble-gecko','Pebble','Existing rescue · gecko',3,7,[
 '...............oooo.......','.............oommlloo.....','............ommlhhllmo....','............olhhhehlmo....',
 '...........omllhhhehlmo...','...........omllllhhhmo....','..........ommllllllmo.....','......o..oommmmllmoo......',
 '.....omo.ommlsmlmoo........','.....olmommlmlmmo.........','......ommllmlmmo..........','.....ommmllmlmmoo.........',
 '....omlmlmlmmo.omlo.......','...omlmlmmoo....oo........','..omllmmoo................','..olmmmo.....o............',
 '.olmmoo.....omo...........','.olmo.......omo...........','.ommo......omo............','..ommoo..oomo.............','...ommmoommo..............','....ooooooo...............'
 ],ap,'Original top-down gecko rescue study; curved segmented tail, splayed feet, warm olive/cream spots. Species identification beyond gecko is not asserted.');
// Four short, splayed limbs, independently drawn around the diagonal trunk.
gecko.stamp(22,14,['mo..','lmo.','.lmo','..oo'],ap,'animal');
gecko.stamp(8,21,['oo...','olmoo','.olmo','..omo'],ap,'animal');
animal('button-snail','Button','Existing rescue · land snail',3,12,[
 '......oooooo..............','....oosllllsoo............','...osllhhhhllso...........','..oslhhsssshhls o.........'.replaceAll(' ',''),
 '..olhssllllsshlo..........','.olhsllssllsshlo..........','.olhslsllslshhlo..........','.olhslslsslshhlo.....o..o..',
 '.olhssllllsshhlo....oe.oe..','..olhhsssshhhlo......m.m...', '..osllhhhhllso.......omo...',
 '...ossssssssoo.....oommo...', '....oddmmmmmmmmooommllmo..','...omllllllmmmlllllllmmo..','..omllllllmmmmmmmmmmmoo...', '...oooooooooooooooooo....'
 ],{...ap,s:'#946443',l:'#cf985f',h:'#efd093',m:'#b5b789',d:'#7a875f'},'Original profile snail with visible spiral shell and paired eyestalks.');
animal('isopod','Isopod','Existing rescue · decomposer',8,12,[
 '....o......o....','.....o....o.....','.....oooooo.....','...oodmmmmd oo...'.replaceAll(' ',''),
 '..odmmllllmmdo..','.odmlllmmlllmdo.','odmllmmmmmmllmdo','odmmmmllllmmmmd o'.replaceAll(' ',''),
 '.omllllllllllmo.','odmmmllllllmmmdo','.omllllllllllmo.','odmmmmllllmmmmdo','.omllllllllllmo.','odmmmmmmmmmmmmdo',
 '.odmllllllllmdo.','..odmmmmmmmmdo..','...oodmmmmdoo...','.....oooooo.....'
 ],{o:'#29323f',d:'#475967',m:'#718995',l:'#a8bac0'},'Dorsal observation-scale isopod; readable paired legs and overlapping armor plates.');
animal('springtail','Springtail','Existing rescue · decomposer',10,17,[
 '........o..o','.......o..o.','......oooo..','.....olmemo.','....olhhmo..','...olhlmoo..','..olhlmo....',
 '.olhlmo.....','olmllmo.....','omlmoo......','.omo........','..o.........','............'
 ],{o:'#51544b',m:'#b8bca4',l:'#e4e4c9',h:'#ffffe3',e:'#282e2a'},'Observation-scale springtail. Deliberately tiny compared with other study frames; not drawn at true shared physical scale.');
animal('tree-frog','Tree Frog','Future species proposal',5,10,[
 '.....oooo....oooo.....','....omlhmo..omlhmo....','....olewmo..omwelo....','....oleemo..omeelo....',
 '...omllllmoomllllmo...','..omllhhllllllhhllmo..','..olhhhhllllhhhhhhlo..','..omllllhllhllllllmo..',
 '..ommlhhhhhhhhhlmmmo..','...omllhhhhhhllmmo...','....omllllllllmo.....','...oommmmmmmmmm oo....'.replaceAll(' ',''),
 '..olmoo......oomlo...','.olllmo......omlllo..','olllmoo......oomlllo.','.ooo............ooo..'
 ],{o:'#203d30',d:'#367653',m:'#50a46e',l:'#8bc77a',h:'#dae6a0',e:'#183326',w:'#f2f6cd'},'Optional future animal visual proposal; no habitat/gameplay claim.');
animal('cherry-shrimp','Cherry Shrimp','Future aquarium proposal',3,13,[
 '......................o...','....................oo....','........oooooooo..oo......','......oomlllllllmoo.......',
 '....oomllllllmmmmeoo......','...omlllmlmmmmmmeo........','..omllmmllmmmmmmo.........','.omllmmllmmmmmoo..........',
 'omllmmllmmmmoo............','ommmmllmmmoo..............','.oommmmmmoo...............','..omooomomomo.............',
 '.olmo..o.o.o.o............','olllmo....................','omllmo....................','.oooo.....................'
 ],{o:'#713d42',m:'#e56c54',l:'#ffa282',e:'#242a35'},'Original profile freshwater shrimp proposal; legs and long antennae are single-cell strokes.');
animal('guppy','Guppy','Future aquarium proposal',3,13,[
 '..........ooo.............','.........omlmo............','..oo....ommllmoo..........','.omlo.oommlllllloo........',
 'omllmoomllhhhhlllmmo......','omlllmmllhhhhhhhlemlo.....','omlllmmlllhhhhhhllmmo.....','omllmoomllllllllmmoo......',
 '.omlo..oommmmmmoo.........','..oo.....oommo............','...........oo.............'
 ],{o:'#283e5b',m:'#518faf',l:'#9ed4d3',h:'#f5d395',e:'#151c27'},'Original fish profile proposal; this is a display-size study, not an aquarium species suitability recommendation.');
animal('stag-beetle','Stag Beetle','Future forest proposal',7,9,[
 '...o.........o...','...om.......mo...','...omo.....omo...','....omo...omo....','.....omooomo.....','.....ommmmo......',
 '...ooommmmooo....','..omoeeeeeemoo...','.omomlhhhlmommo..','..oomlllmlmoo....','..omlllllmmmmo...',
 'omomlllllmmmommo.','.oomlllllmmmoo...','..omlllllmmmmo...','omomlllllmmmommo.','.oomlllllmmmoo...',
 '...omllllmmmo....','..ooommmmmooo....','.omo.ooooo.omo...','..o.........o....'
 ],{o:'#263138',m:'#536e69',l:'#8aa78d',h:'#c8ceb1',e:'#334c4c'},'Original top-down stag beetle proposal, distinct mandibles and split elytra.');

fs.mkdirSync(out,{recursive:true});
const manifest={schemaVersion:1,id:'critz.idle-collection.v1',task:'M1.C6',status:'awaiting-user-native-art-review',runtimeIntegrated:false,approvedBaseline:'assets/characters/hero-boy-v1/idle-south.png',assets:[]};
for(const v of [...characters,...animals]){
 const palette=[null,...new Set(v.a.a.filter(Boolean))];const pixels=v.a.a.map(c=>palette.indexOf(c));
 const project={format:'fmw-sprite',version:1,name:v.label,preset:v.kind==='character'?'character':'custom',width:32,height:v.a.h,palette,bank:'custom',notes:v.notes+' Front idle/still review only; no animation or runtime integration.',frames:[{name:v.kind==='character'?'South idle':'Still study',ticks:8,pixels}]};
 const json=JSON.stringify(project,null,2)+'\n',rle=describe(project)+'\n';
 const decoded=readProjectData(JSON.parse(rle),new Set(palette.slice(1)));
 if(JSON.stringify(decoded.frames[0].pixels)!==JSON.stringify(pixels))throw Error('RLE mismatch');
 const rgba=Buffer.from(v.a.a.flatMap(c=>c?[...Buffer.from(c.slice(1),'hex'),255]:[0,0,0,0]));
 await sharp(rgba,{raw:{width:32,height:v.a.h,channels:4}}).png().toFile(path.join(out,v.id+'.png'));
 fs.writeFileSync(path.join(home,v.id+'.sprite.json'),json);fs.writeFileSync(path.join(home,v.id+'.rle.json'),rle);
 if(v.kind==='character')fs.writeFileSync(path.join(home,v.id+'.masks.json'),JSON.stringify({coordinateSystem:'native top-down; array entries are y*32+x',masks:v.a.masks,visibleParts:v.a.parts},null,2)+'\n');
 const coords=pixels.flatMap((c,i)=>c?[[i%32,Math.floor(i/32)]]:[]),bbox=[Math.min(...coords.map(c=>c[0])),Math.min(...coords.map(c=>c[1])),Math.max(...coords.map(c=>c[0]))+1,Math.max(...coords.map(c=>c[1]))+1];
 manifest.assets.push({id:'critz.'+v.id+'.idle.v1',slug:v.id,label:v.label,role:v.role,kind:v.kind,file:v.id+'.png',frame:[32,v.a.h],anchor:[16,v.a.h],bbox,paintedSize:[bbox[2]-bbox[0],bbox[3]-bbox[1]],bottomPadding:v.a.h-bbox[3],colors:palette.length-1,opaquePixels:coords.length,pixelSHA256:sha(rgba),pngSHA256:sha(fs.readFileSync(path.join(out,v.id+'.png'))),source:'art/source/idle-collection-v1/'+v.id+'.sprite.json',notes:v.notes});
}
fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
console.log(`${characters.length} characters and ${animals.length} animals exported; approved boy untouched.`);
