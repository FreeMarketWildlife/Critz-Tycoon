// Original south-idle pixel drawing. Each symbol is exactly one native pixel.
import {writeFile} from 'node:fs/promises';
const palette={O:'#222b3a',D:'#356775',T:'#539ba6',C:'#86c5c8',H:'#c1e3db',W:'#f3ecd0',A:'#d88d29',G:'#edb54e',L:'#f4d17b',B:'#a96c30',N:'#314861',P:'#536c88',F:'#c7b994'};
// A rounded vessel, readable separate eyes, asymmetric spout and open handle.
// Head occupies14 rows; clothing and connected feet occupy10.
const head=[
 '..OOO....OOOOOO.....',
 '.OHHCO..OHHHHHHO....',
 '.OCHHCOOCTCCCCTO....',
 '..OTCHHCCCHHHCTO....',
 '...OTCCCCCCCCTTOO...',
 '...OHCCTCCCCCCOTCO..',
 '..OHCCCCCCCCCCOTCHO.',
 '..OHWLLLLLLLGGCO.CO.',
 '..OHCLGOGGGOGGCO.CO.',
 '..OTCLGOGGGOGGCO.CO.',
 '...OTGGGAGGGGATCTO..',
 '...OTAGGGGGGAATTO...',
 '....OTTAAAAAATTO....',
 '.....ODTTTTTDO......',
];
const body=[
 '.....ODWWWWDO.......',
 '....OWWWWWWWWO......',
 '...OLWWWWWWWWLO.....',
 '...OBOWWWWWWOB O....'.replace(' ',''),
 '...OBOFWWWWFOBO.....',
 '....OONPPPPNOO......',
 '.....ONNPPNNO.......',
 '.....OGNOONGO.......',
 '.....OWNOONWO.......',
 '....OOPNOONPOO......',
];
const rows=Array(7).fill('.'.repeat(24));
for(const line of [...head,...body]){if(line.length>20)throw new Error(line);rows.push('..'+line.padEnd(20,'.')+'..');}
rows.push('.'.repeat(24));
const data={id:'kaid',label:'Kaid',palette,rows,design:{bodyType:'compact pitcher child',age:'child',headBounds:[3,7,21,21],chinRow:20,shoulderRow:21,headHeight:14,bodyHeight:10,frame:[24,32],anchor:[12,32],signature:['rounded teal pitcher with amber contents','spout left / loop handle right','cream tee and navy shorts with connected legs'],changes:['shorter rounded vessel construction','two deliberate1×2 eyes','pelvis and legs connected; former blank row removed'],identitySource:'docs/GAME_VISION.md',status:'awaiting-user-art-review',bodyBounds:[5,21,17,31],annotationBoundsFormat:'left,top,right-exclusive,bottom-exclusive'}};
await writeFile('art/source/characters-v2/kaid.json',JSON.stringify(data,null,2)+'\n');
