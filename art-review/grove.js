import {loadAtlas} from '../src/atlas.js';
import {TICK_SECONDS} from '../src/movement.js';
import {MusicDirector} from '../src/audio/director.js';
const $=id=>document.getElementById(id),canvas=$('button'),c=canvas.getContext('2d');
const observed=new Set(),notes={look:'Two feelers test the way ahead before the foot follows.',nibble:'The head lowers for a tiny nibble; the shell stays steady.',tuck:'A short pause lets the feelers draw close to the shell.'};
let atlas,action='glide',time=0,last=0,musicOn=false;
const music=new MusicDirector({storage:{getItem:()=>JSON.stringify({enabled:false,volume:.25}),setItem:()=>{}},onChange:s=>{if(musicOn&&s.error)$('status').textContent=s.error;}});
music.update({scene:'critz',stage:'morning',dayClock:{minute:720,remainder:0}},'');
$('calm').checked=matchMedia('(prefers-reduced-motion: reduce)').matches;
function draw(){
 c.imageSmoothingEnabled=false;c.clearRect(0,0,32,32);
 const id=action==='glide'?'button-snail':'button-'+action,frames=atlas.manifest.assets.filter(a=>a.id.startsWith(id+'.'));
 let tick=$('calm').checked?0:time/TICK_SECONDS%frames.reduce((s,f)=>s+f.ticks,0),frame=frames[0];
 for(const f of frames){if(tick<f.ticks){frame=f;break;}tick-=f.ticks;}
 atlas.draw(c,frame.id,0,0);
 // Grid is a separate presentation layer: rendering never changes the asset.
 if($('grid').checked){canvas.style.width=canvas.style.height='256px';const grid=$('pixel-grid')||document.createElement('canvas');if(!grid.id){grid.id='pixel-grid';grid.width=grid.height=288;grid.style.cssText='position:absolute;width:288px;height:288px;pointer-events:none';canvas.parentElement.style.position='relative';canvas.parentElement.append(grid);}grid.hidden=false;const g=grid.getContext('2d');g.clearRect(0,0,288,288);g.font='8px monospace';g.textAlign='right';for(let i=0;i<=32;i++){g.strokeStyle=i===16?'#cd8e3b':i%10===2||i===32?'#38624699':'#38624628';g.beginPath();g.moveTo(16+i*8,16);g.lineTo(16+i*8,272);g.stroke();g.strokeStyle=(32-i)%10===0||i===0?'#38624699':'#38624628';g.beginPath();g.moveTo(16,16+i*8);g.lineTo(272,16+i*8);g.stroke();if((32-i)%10===0||i===0)g.fillText(32-i,12,18+i*8);}g.fillStyle='#386246';g.textAlign='center';g.fillText('16',144,12);}else if($('pixel-grid'))$('pixel-grid').hidden=true;
}
for(const b of document.querySelectorAll('[data-action]'))b.onclick=()=>{action=b.dataset.action;time=0;document.querySelectorAll('[data-action]').forEach(a=>a.setAttribute('aria-pressed',a===b));if(notes[action]){observed.add(action);$('observation').textContent=notes[action];$('notes').replaceChildren(...[...observed].map(id=>{const li=document.createElement('li');li.textContent=notes[id];return li;}));$('write-note').disabled=observed.size<3;}draw();};
$('write-note').onclick=()=>{$('reward').textContent='Notebook: Button moves at Button’s pace. Watch first; change one thing at a time.';$('write-note').disabled=true;};
$('music').onclick=()=>{musicOn=!musicOn;music.setEnabled(musicOn);$('music').textContent=musicOn?'Music on':'Music off';$('music').setAttribute('aria-pressed',musicOn);};
document.addEventListener('visibilitychange',()=>{last=0;music.setVisible(!document.hidden);});window.addEventListener('pagehide',()=>music.dispose());
try{atlas=await loadAtlas(new URL('../assets/playable/button-v2/atlas.json',import.meta.url));$('status').textContent='Button is ready. A slow foot wave, a steady shell.';requestAnimationFrame(function frame(now){if(last&&!document.hidden)time+=Math.min(.1,(now-last)/1000);last=now;draw();requestAnimationFrame(frame);});}catch(e){$('error').hidden=false;$('error').textContent='The artwork could not load: '+e.message;}
