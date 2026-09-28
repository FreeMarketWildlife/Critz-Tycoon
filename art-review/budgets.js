// Isolated review: no game state imports, persistence, or approval writes.
import {loadAtlas} from '../src/atlas.js';
import {scenes,isBlocked} from '../src/world.js';
import {createMotion,getMotionView,advanceMotion,createMotionClock,advanceMotionClock,resetMotionClock} from '../src/movement.js';
const $=id=>document.getElementById(id),budgets=[16,24],room=scenes.bedroom;
let art,environment,entries,role='mom',running=!matchMedia('(prefers-reduced-motion: reduce)').matches,auto=true,guides=false;
let motion=createMotion({x:8,y:7,facing:'down'}),clock=createMotionClock(),last=performance.now(),leg=0,ready=false;
const held=new Map(), keyboard=new Set(),targets=[[8,9],[6,9],[6,7],[8,7]];
const context={scene:'bedroom',stage:'morning',flags:{rescued:[]},player:motion.player};
function clearInput(){held.clear();keyboard.clear();document.querySelectorAll('.held').forEach(e=>e.classList.remove('held'));resetMotionClock(clock);last=performance.now();}
function keys(){return new Set([...keyboard,...held.values()]);}
function controls(){
 $('play').textContent=running?'Pause':'Play';$('play').setAttribute('aria-pressed',String(running));
 $('auto').textContent=auto?'Auto walk on':'Auto walk off';$('auto').setAttribute('aria-pressed',String(auto));
 document.querySelectorAll('[data-character]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.character===role)));
}
function reset(){clearInput();motion=createMotion({x:8,y:7,facing:'down'});leg=0;context.player=motion.player;render();}
function tick(){
 let dirs=keys();
 if(auto){
  const p=motion.player,v=getMotionView(motion);let target=targets[leg];
  if(v.settled&&p.x===target[0]&&p.y===target[1]){leg=(leg+1)%targets.length;target=targets[leg];}
  dirs=new Set([p.x<target[0]?'right':p.x>target[0]?'left':p.y<target[1]?'down':'up']);
 }
 advanceMotion(motion,dirs,false,(x,y)=>!isBlocked('bedroom',x,y,context));
}
function assetFor(budget,view){return entries.get(`compare.${role}.${budget}.${view.facing}.${view.pose}`);}
function actor(c,budget,view,x,y){const a=assetFor(budget,view);art.draw(c,a.id,x-a.anchor[0],y-a.anchor[1]);
 if(guides){c.lineWidth=1;c.strokeStyle='#f3c96b';c.strokeRect(x-a.anchor[0]+.5,y-31.5,budget-1,31);c.strokeStyle='#dcf0db';c.strokeRect(x-7.5,y-15.5,15,15);c.fillStyle='#efaa7e';c.fillRect(x-2,y,5,1);}}
function prop(c,o){const e=environment.manifest.assets.find(a=>a.id===o.sprite);environment.draw(c,o.sprite,(o.x+o.w/2)*16-e.anchor[0],(o.y+o.h)*16-e.anchor[1]);}
function renderRoom(canvas,budget,view){const c=canvas.getContext('2d');c.imageSmoothingEnabled=false;c.fillStyle='#223038';c.fillRect(0,0,240,160);c.save();c.translate(-8,-24);
 for(let y=0;y<room.h;y++)for(let x=0;x<=room.w;x++)environment.draw(c,y<3?'wall.interior':x===0||x===room.w?'wall.interior.side':'floor.wood',x*16,y*16);
 const rug=environment.manifest.assets.find(a=>a.id==='rug');environment.draw(c,'rug',128-rug.anchor[0],128-rug.anchor[1]);
 const stairs=environment.manifest.assets.find(a=>a.id==='stairs.down');environment.draw(c,'stairs.down',224-stairs.anchor[0],176-stairs.anchor[1]);
 const list=room.objects.map(o=>({y:(o.y+o.h)*16,draw:()=>prop(c,o)}));list.push({y:view.y,draw:()=>actor(c,budget,view,view.x,view.y)});list.sort((a,b)=>a.y-b.y).forEach(o=>o.draw());c.restore();
}
function render(){if(!ready)return;const view=getMotionView(motion);
 for(const budget of budgets){const c=$(`close${budget}`).getContext('2d');c.imageSmoothingEnabled=false;c.fillStyle='#142e35';c.fillRect(0,0,64,48);c.fillStyle='#24424a';c.fillRect(0,40,64,8);c.fillStyle='#48625f';c.fillRect(0,40,64,1);actor(c,budget,view,32,40);renderRoom($(`room${budget}`),budget,view);}
 const direction={down:'South',up:'North',left:'West',right:'East'}[view.facing];
 const description=`${art.manifest.characters.find(c=>c.id===role).label} · ${direction} · ${view.action==='idle'?'Standing':view.action==='blocked'?'At an obstacle':'Walking'}`;
 if($('motion-status').textContent!==description)$('motion-status').textContent=description;
}
function metrics(){for(const budget of budgets){const a=entries.get(`compare.${role}.${budget}.down.idle`),b=a.opaqueBBox;$(`metrics${budget}`).textContent=`Visible front: ${b[2]-b[0]} × ${b[3]-b[1]} px · ${a.colorCount} colors`;}}
function fit(){for(const budget of budgets){const canvas=$(`room${budget}`),width=canvas.parentElement.clientWidth;const scale=Math.max(1,Math.floor(width/240));canvas.style.width=`${240*scale}px`;canvas.style.height=`${160*scale}px`;}
 // Same source viewport, same native scale, same scroll position on both sides.
 const scrollers=budgets.map(b=>$(`room${b}`).parentElement);const center=Math.max(0,(240-scrollers[0].clientWidth)/2);scrollers.forEach(s=>s.scrollLeft=center);}
$('play').onclick=()=>{running=!running;clearInput();controls();};
$('step').onclick=()=>{running=false;clearInput();advanceMotionClock(clock,280896/16777216,tick);controls();render();};
$('auto').onclick=()=>{auto=!auto;clearInput();if(auto)reset();controls();};
$('reset').onclick=reset;
$('guides').onchange=()=>{guides=$('guides').checked;render();};
const directions={ArrowUp:'up',ArrowDown:'down',ArrowLeft:'left',ArrowRight:'right',w:'up',s:'down',a:'left',d:'right'};
for(const b of document.querySelectorAll('[data-dir]')){
 b.onpointerdown=e=>{e.preventDefault();b.setPointerCapture(e.pointerId);auto=false;running=true;held.set(e.pointerId,b.dataset.dir);b.classList.add('held');controls();};
 for(const event of ['pointerup','pointercancel','lostpointercapture'])b.addEventListener(event,e=>{held.delete(e.pointerId);b.classList.remove('held');});
}
document.addEventListener('keydown',e=>{if(!ready||e.target.matches('input,select'))return;const dir=directions[e.key];if(dir){e.preventDefault();auto=false;running=true;keyboard.add(dir);controls();}else if(e.key===' '&&e.target===document.body){e.preventDefault();$('play').click();}});
document.addEventListener('keyup',e=>keyboard.delete(directions[e.key]));
window.addEventListener('blur',clearInput);document.addEventListener('visibilitychange',clearInput);window.addEventListener('resize',fit);
let scrolling=false;for(const b of budgets){const s=$(`room${b}`).parentElement;s.onscroll=()=>{if(scrolling)return;scrolling=true;$(`room${b===16?24:16}`).parentElement.scrollLeft=s.scrollLeft;requestAnimationFrame(()=>scrolling=false);};}
function frame(now){const dt=Math.max(0,(now-last)/1000);last=now;if(!document.hidden&&running)advanceMotionClock(clock,dt,tick);else resetMotionClock(clock);render();requestAnimationFrame(frame);}
try{
 [art,environment]=await Promise.all([loadAtlas(new URL('../assets/review/budget-comparison/atlas.json',import.meta.url)),loadAtlas(new URL('../assets/playable/atlas.json',import.meta.url))]);
 entries=new Map(art.manifest.assets.map(a=>[a.id,a]));if(!art.manifest.characters.some(c=>c.id===role))role=art.manifest.characters[0].id;
 $('characters').replaceChildren(...art.manifest.characters.map(char=>{const b=document.createElement('button');b.dataset.character=char.id;b.textContent=char.label;b.onclick=()=>{role=char.id;clearInput();metrics();controls();render();};return b;}));
 ready=true;document.querySelectorAll('button,input').forEach(e=>e.disabled=false);document.documentElement.dataset.reviewReady='true';metrics();controls();fit();render();last=performance.now();requestAnimationFrame(frame);
}catch(error){$('error').hidden=false;$('error').textContent=`The comparison artwork could not load. Your game save is untouched. Reload to try again. ${error.message}`;$('motion-status').textContent='Artwork unavailable.';}
export function getComparisonSnapshot(){return {ready,role,running,auto,guides,motion:getMotionView(motion),tick:clock.tick,frameIds:ready?budgets.map(b=>assetFor(b,getMotionView(motion)).id):[],scroll:budgets.map(b=>$(`room${b}`).parentElement.scrollLeft)};}
