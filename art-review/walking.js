import {loadAtlas} from '../src/atlas.js';
import {createReviewClock, poseAt, directionAt} from './walking-timing.js';
const $=id=>document.getElementById(id), clock=createReviewClock();
const backgrounds={dark:'#17333c',paper:'#e8e2c9',green:'#849e72'};
const poseNames={strideA:'First stride',idle:'Passing pose',strideB:'Other stride'};
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
let atlas, selected, ready=false, playing=!reduced.matches, cycle=true, manualDirection='south', background='dark', request=null, suspended=document.hidden, previousKey='';
const cards=[];
function current(){return {direction:cycle?directionAt(clock.tick):manualDirection,pose:poseAt(clock.tick)};}
function paint(canvas,person,direction,pose,padding=0){
  const ctx=canvas.getContext('2d');ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,canvas.width,canvas.height);
  if(padding){ctx.fillStyle=backgrounds[background];ctx.fillRect(0,0,canvas.width,canvas.height);}
  atlas.draw(ctx,person.frames[direction][pose],padding,padding);
}
function render(force=false){
  if(!ready)return;const {direction,pose}=current(),key=`${direction}:${pose}:${selected.id}:${background}`;
  if(!force&&key===previousKey)return;previousKey=key;
  paint($('portrait'),selected,direction,pose,4);$('portrait-stage').style.background=backgrounds[background];$('pose-label').textContent=poseNames[pose];
  for(const canvas of document.querySelectorAll('[data-pose]')){paint(canvas,selected,direction,canvas.dataset.pose);canvas.setAttribute('aria-label',`${selected.label}: ${direction} ${poseNames[canvas.dataset.pose]}`);}
  for(const card of cards)paint(card.canvas,card.person,direction,pose);
  for(const button of document.querySelectorAll('[data-direction]'))button.setAttribute('aria-pressed',String(button.dataset.direction===direction));
}
function select(person){selected=person;$('character-name').textContent=person.label;$('character-kind').textContent=person.bodyType;
  $('portrait').setAttribute('aria-label',`${person.label} walking; use Pause and Next pose to inspect`);
  $('download-character').href=new URL(`../assets/review/characters-walk-v3/${person.gif}`,import.meta.url);$('download-character').download=`critz-${person.id}-walking.gif`;
  $('download-sheet').href=new URL(`../assets/review/characters-walk-v3/${person.sheet}`,import.meta.url);$('download-sheet').download=`critz-${person.id}-walking.png`;
  for(const card of cards)card.button.setAttribute('aria-pressed',String(card.person.id===person.id));render(true);
}
function frame(now){request=null;if(!ready||!playing||suspended)return;clock.advance(now);render();request=requestAnimationFrame(frame);}
function schedule(){if(request!==null)cancelAnimationFrame(request);request=null;clock.resetBaseline();$('play').textContent=playing?'Pause':'Play';$('play').setAttribute('aria-label',playing?'Pause all walking animations':'Play all walking animations');if(ready&&playing&&!suspended)request=requestAnimationFrame(frame);}
$('play').onclick=()=>{playing=!playing;schedule();};
$('step').onclick=()=>{playing=false;clock.nextPose();schedule();render();};
$('cycle').onchange=()=>{manualDirection=current().direction;cycle=$('cycle').checked;clock.restart();render(true);};
for(const button of document.querySelectorAll('[data-direction]'))button.onclick=()=>{manualDirection=button.dataset.direction;cycle=false;$('cycle').checked=false;clock.restart();render(true);};
for(const button of document.querySelectorAll('[data-bg]'))button.onclick=()=>{background=button.dataset.bg;for(const b of document.querySelectorAll('[data-bg]'))b.setAttribute('aria-pressed',String(b===button));render(true);};
function suspension(value){suspended=value;schedule();}
document.addEventListener('visibilitychange',()=>suspension(document.hidden));window.addEventListener('blur',()=>suspension(true));window.addEventListener('focus',()=>suspension(document.hidden));
reduced.addEventListener('change',event=>{if(event.matches){playing=false;schedule();}});
try{
  atlas=await loadAtlas(new URL('../assets/review/characters-walk-v3/atlas.json',import.meta.url));
  for(const person of atlas.manifest.characters){const button=document.createElement('button');button.className='cast-card';button.dataset.character=person.id;button.setAttribute('aria-label',`Inspect ${person.label}`);button.setAttribute('aria-pressed','false');
    const canvas=document.createElement('canvas');canvas.width=24;canvas.height=32;canvas.setAttribute('aria-hidden','true');const name=document.createElement('strong');name.textContent=person.label;const label=document.createElement('small');label.textContent=person.bodyType;
    button.append(canvas,name,label);button.onclick=()=>select(person);$('cast').append(button);cards.push({button,canvas,person});}
  ready=true;document.querySelectorAll('button,input').forEach(e=>e.disabled=false);select(atlas.manifest.characters[0]);schedule();document.documentElement.dataset.reviewReady='true';
}catch(error){$('error').hidden=false;$('error').textContent=`The walking artwork could not load. Reload to try again. ${error.message}`;$('character-name').textContent='Artwork unavailable';$('pose-label').textContent='';}
export function getWalkReviewSnapshot(){return {ready,playing,suspended,tick:clock.tick,...current(),selected:selected?.id,background,cycle,characters:cards.length,frames:atlas?.manifest.assetCount,droppedMs:clock.droppedMs};}
