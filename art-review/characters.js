// Still-art review only. No animation loop, game state, input simulation or storage.
import {loadAtlas} from '../src/atlas.js';
import {scenes} from '../src/world.js';
const $=id=>document.getElementById(id);
const backgrounds={dark:'#17333c',paper:'#e8e2c9',green:'#849e72'};
let art,environment,selected,background='dark',guides=false,ready=false;
function drawPortrait(){
 const c=$('portrait').getContext('2d');c.imageSmoothingEnabled=false;c.fillStyle=backgrounds[background];c.fillRect(0,0,32,40);
 if(guides){c.fillStyle=background==='paper'?'#cfbfa3':'#36565a';for(let y=0;y<40;y++)for(let x=0;x<32;x++)if((x+y)%2)c.fillRect(x,y,1,1);}
 art.draw(c,selected.id,4,4);
 if(guides){c.lineWidth=1;c.strokeStyle='#f5bd62';c.strokeRect(6.5,9.5,19,25);c.fillStyle='#f5bd62';c.fillRect(13,35,7,1);}
 $('portrait-stage').style.background=backgrounds[background];
}
function drawRoom(){
 const canvas=$('room'),c=canvas.getContext('2d'),room=scenes.bedroom;c.imageSmoothingEnabled=false;c.fillStyle='#26363a';c.fillRect(0,0,240,160);c.save();c.translate(-8,-24);
 for(let y=0;y<room.h;y++)for(let x=0;x<=room.w;x++)environment.draw(c,y<3?'wall.interior':x===0||x===room.w?'wall.interior.side':'floor.wood',x*16,y*16);
 const anchored=(id,x,y)=>{const a=environment.manifest.assets.find(a=>a.id===id);environment.draw(c,id,x-a.anchor[0],y-a.anchor[1]);};
 anchored('rug',128,128);anchored('stairs.down',224,176);
 const objects=room.objects.map(o=>({y:(o.y+o.h)*16,draw:()=>anchored(o.sprite,(o.x+o.w/2)*16,(o.y+o.h)*16)}));
 objects.push({y:112,draw:()=>art.draw(c,selected.id,128-12,112-32)});objects.sort((a,b)=>a.y-b.y).forEach(o=>o.draw());c.restore();
}
function select(asset){
 selected=asset;$('character-name').textContent=asset.label;$('character-kind').textContent=asset.design.bodyType||'Original Critz character';
 const signatures=asset.design.signature||asset.design.signatureFeatures||[];$('character-design').textContent=Array.isArray(signatures)?signatures.join(' · '):signatures;
 $('ink-size').textContent=asset.visibleSize.join(' × ')+' px';$('color-count').textContent=asset.colorCount;
 $('proportion').textContent=asset.design.headHeight&&asset.design.bodyHeight?`${asset.design.headHeight} / ${asset.design.bodyHeight} px`:'Compact chibi';
 $('palette').replaceChildren(...asset.colors.map(color=>{const span=document.createElement('span');span.className='swatch';span.style.background=color;span.title=color;span.setAttribute('aria-label',color);return span;}));
 $('download-character').href=new URL(`../assets/review/characters-v2/${asset.png}`,import.meta.url);$('download-character').download=`critz-${asset.character}-24x32.png`;
 document.querySelectorAll('[data-character]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.character===asset.character)));
 drawPortrait();drawRoom();
}
function fit(){const canvas=$('room'),scale=Math.max(1,Math.floor(canvas.parentElement.clientWidth/240));canvas.style.width=240*scale+'px';canvas.style.height=160*scale+'px';}
for(const button of document.querySelectorAll('[data-bg]'))button.onclick=()=>{background=button.dataset.bg;document.querySelectorAll('[data-bg]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));drawPortrait();};
$('guides').onchange=()=>{guides=$('guides').checked;drawPortrait();};window.addEventListener('resize',fit);
try{
 [art,environment]=await Promise.all([loadAtlas(new URL('../assets/review/characters-v2/atlas.json',import.meta.url)),loadAtlas(new URL('../assets/playable/atlas.json',import.meta.url))]);
 const cards=art.manifest.assets.map(asset=>{const button=document.createElement('button');button.className='cast-card';button.dataset.character=asset.character;button.setAttribute('aria-label',`Inspect ${asset.label}`);button.setAttribute('aria-pressed','false');
  const canvas=document.createElement('canvas');canvas.width=24;canvas.height=32;canvas.setAttribute('aria-hidden','true');canvas.getContext('2d').imageSmoothingEnabled=false;art.draw(canvas.getContext('2d'),asset.id,0,0);
  const label=document.createElement('strong');label.textContent=asset.label;const note=document.createElement('small');note.textContent=asset.design.bodyType||'Compact chibi';button.append(canvas,label,note);button.onclick=()=>select(asset);return button;});
 $('cast').replaceChildren(...cards);$('cast-count').textContent=`${cards.length} native designs · 1 still frame each`;
 $('roster-note').textContent=`${cards.length} native designs cover the currently located cast. The requested 102-character roster has not been located; its source/count is awaiting clarification.`;
 ready=true;document.querySelectorAll('button,input').forEach(e=>e.disabled=false);document.documentElement.dataset.reviewReady='true';select(art.manifest.assets[0]);fit();
}catch(error){$('error').hidden=false;$('error').textContent=`The character artwork could not load. Reload to try again. ${error.message}`;$('character-name').textContent='Artwork unavailable';}
export function getCharacterReviewSnapshot(){return {ready,selected:selected?.character,background,guides,frameCount:art?.manifest.assets.length,animation:false};}
