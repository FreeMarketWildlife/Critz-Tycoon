// Original native rows for two independently drawn Kaid pixel budgets.
import {writeFile} from 'node:fs/promises';
const palette={O:'#25313e',D:'#365e69',T:'#4d919d',C:'#81bdc4',H:'#b4dddd',W:'#e5edd3',A:'#d9942f',G:'#edb64a',L:'#f2d074',B:'#a56b31',N:'#30465e',P:'#566981',F:'#c5bc92'};
const blank=w=>Array.from({length:32},()=>Array(w).fill('.'));
const stamp=(rows,lines,y,x=0)=>lines.forEach((line,j)=>[...line].forEach((p,i)=>{if(p!=='.'&&rows[y+j]&&x+i>=0&&x+i<rows[0].length)rows[y+j][x+i]=p;}));
const fill=(r,x,y,w,h,p)=>{for(let j=y;j<y+h;j++)for(let i=x;i<x+w;i++)if(r[j]&&i>=0&&i<r[0].length)r[j][i]=p;};
const small={
 down:[
 '..ODDOOOO.......','..OCHHHHCO......','...OTCCTDO......','..OHCCHHCOTO....',
 '..OHCCCCCOTCO...','.OHWLLLGGCOTCO..','.OCLGOAGOLCOCO..','.OCAGGAGGACTCO..',
 '..OTAGGGAOTDO...','...OTAAATO......','....ODDDO.......',
 ],
 up:[
 '.......OOOOODD..','......OCHHHHCO..','......ODTCCTO...','....OTOCCHHCHO..',
 '...OCTOCCCCCCHO.','..OTCOLGGGLLWHO.','..OCOCLGGGGGLCO.','..OCTCAGGGGGACO.',
 '...ODTOAGGGAOTO.','......OTAAATO...','.......ODDDO....',
 ],
 left:[
 '....ODDOOO......','....OCHHHCO.....','.....OTCCDO.....','....OHCCHCOTO...',
 '...OHCACCCOTCO..','..OHHWLGGCOTCO..','...OLGOAGCOTCO..','...OLGGGACOTCO..',
 '....OAGGAOTDO...','.....OTAATO.....','......ODDO......',
 ],
 right:[
 '.....OOOOODD....','....OCHHHHCO....','....ODTCCTO.....','...OTCCHHHCO....',
 '..OTOCCTOACHO...','.OTCOCGLWWHHOO..','.OCOCCGGOGLO....','.OTCOCAGGGLO....',
 '..ODTOAGGAO.....','.....OTAATO.....','......ODDO......',
 ]};
const large={
 down:[
 '....ODDOOOOOO...........', '....OTHHHHHHHO..........','.....ODTCCCCDO..........','....OHHCCCHHHCO.........',
 '...OHHCCCCCCCCTOO.......','...OHCCCTTCCCCOTCO......','..OHHCCCCCCCCCTCOCO.....','..OHWLLLLLLLGGCOTCO.....',
 '..OHCLGOOGGGOGGCOTCO....','..OTCLGOOGGGOGGCOTCO....','...OTAGGGAGGGGATCTO.....','...OTAGGGGGGGGATTO......',
 '....OTAGGGGGGAOTO.......','.....OTTAAAAATTO........','......ODTTTTDO..........','.......OOOOOO...........',
 ],
 up:[
 '..........OOOOOODDO.....','.........OHHHHHHHTO.....','.........ODCCCCTDO......','........OCHHHCCCHHO.....',
 '......OOTCCCCCCCCHHO....','.....OCTOCCCCTTCCCHO....','....OCOCTCCCCCCCCHHHO...','....OCTOCGGLLLLLLLWHO...',
 '....OCTOCGGGGGGGGGLCHO..','....OCTOCGGGGGGGGGLCTO..','.....OTCTAGGGGGGGGATO...', '......OTTAGGGGGGGGATO...',
 '.......OTOAGGGGGGATO....','........OTTAAAAATTO.....','.........ODTTTTDO.......','..........OOOOOO........',
 ],
 left:[
 '.......ODDOOOO..........','.......OTHHHHHO.........','........ODCCCDO.........','.......OHHCCCHCOO.......',
 '......OHHCCCCCCOTCO.....','.....OHCACCCCCCTCOCO....','....OHHCWLLLGGCOTCTO....','.....OHHLLLOGGCOTCTO....',
 '.....OHCLLLOGGCOTCTO....','.....OTCGGGAGGCOTCTO....','......OTGGGGGATCTTO.....','......OTAGGGAATTO.......',
 '.......OTTAAATTO........','........ODTTTDO.........','.........OOOOO..........','..........OO............',
 ],
 right:[
 '.........OOOOODDO.......','........OHHHHHCTO.......','........ODCCCCTO........','......OOTCHHCHHCO.......',
 '.....OCTOCCCCCCCHHO.....','....OCOCTCCCCCCACCHO....','....OTCOCCGGLLLWCCHHO...', '....OTCOCCGGOLLHHHO.....',
 '....OTCOCCGGOLLHCHO.....','....OTCOCCGGAGGGCTO.....','.....OTTCAGGGGGTTO......','......OTTAGGGGAATO......',
 '.......OTTAAATTO........','........ODTTTDO.........','.........OOOOO..........','..........OO............',
 ]};
function make(w,dir,pose){
 const r=blank(w), big=w===24, cx=w/2;stamp(r,(big?large:small)[dir],big?5:11);
 // Each direction has its own head geometry; the physical handle and spout
 // have distinct silhouettes. Only small torso gait pixels change per stride.
 const top=big?21:22;
 const front=dir==='down', back=dir==='up';
 if(front||back){
  stamp(r,big?['...ODWWWWDO...','..OFWWWWWWFO..','.OBOWWWWWWOB O.'.replace(' ',''),'..BOFWFFWFOB..','...ONPPPNO....','...ONNPNNO....']:['..ODWWDO..','.OBWWWWBO.','.OBWFFWBO.','..ONPPNO..','..ONNNNO..'],top,cx-(big?7:5));
  if(back)fill(r,cx-3,top+1,6,2,'W');
  const gap=big?3:2;
  fill(r,cx-gap-1,28,3,2,'N');fill(r,cx+1,28,3,2,'N');
  fill(r,cx-gap-1,30,3,1,'O');fill(r,cx+1,30,3,1,'O');
  if(pose!=='idle'){
   const a=pose==='strideA';const foot=a?cx-gap-1:cx+1;const rear=a?cx+1:cx-gap-1;
   fill(r,foot,30,3,2,'O');fill(r,rear,30,3,2,'.');fill(r,rear,29,3,1,'O');
   const arm=a?cx-(big?6:5):cx+(big?4:3);fill(r,arm,top+2,2,3,'B');fill(r,arm,top+2,1,1,'L');
  }
 }else{
  const left=dir==='left', x=cx-3;
  stamp(r,big?['.ODWWWDO.','OOWWWWFO.','OOWWFBOO.','.OWWFBO..','.ONPPNO..','..ONNNO..']:['.ODWWDO.','OOWWWFO.','.OWFBO..','.ONPNO..','..ONNO..'],top,x-1);
  fill(r,cx-3,28,3,2,'N');fill(r,cx+1,28,2,2,'P');fill(r,cx-3,30,3,1,'O');fill(r,cx+1,30,3,1,'O');
  if(pose!=='idle'){
   fill(r,cx-4,28,9,4,'.');const a=pose==='strideA';
   fill(r,cx-3-(a?1:0),28,3,2,'N');fill(r,cx+(a?2:0),29,3,2,'P');
   fill(r,cx-4,30,4,1,'O');fill(r,cx+1,31,4,1,'O');
   if(!a){for(let y=28;y<32;y++)r[y]=[...r[y]].reverse();}
   const armX=left?cx-2:cx+1;fill(r,armX+(a?-1:1),top+2,2,3,'B');
  }
 }
 return r.map(row=>row.join(''));
}
const data={character:'kaid',label:'Kaid',palette,budgets:{}};
for(const w of [16,24]){const directions={};for(const d of ['down','up','left','right'])directions[d]=Object.fromEntries(['idle','strideA','strideB'].map(p=>[p,make(w,d,p)]));data.budgets[w]={frame:[w,32],anchor:[w/2,32],directions};}
await writeFile('art/source/budget-comparison/kaid.json',JSON.stringify(data,null,2)+'\n');
