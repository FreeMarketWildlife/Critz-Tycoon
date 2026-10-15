import {createMotionClock,advanceMotionClock} from '../src/movement.js';
import {createNetTest,stepNetTest,startSwing,catchCenter,netPose,RULES,MEADOW,catchTile} from './net-grid-state.js';
const $=id=>document.getElementById(id),canvas=$('world'),ctx=canvas.getContext('2d'),viewport=$('viewport');
const ASSET='../assets/review/net-r1/',CRITTER='../assets/review/living-collection-v1/';
const images={},keys=new Set(),pointers=new Map();let s=createNetTest(),loaded=false,paused=true,latched=false,charging=false,debug=false,last=0,acc=0,scale=1,camera={x:0,y:0},directionOrder=[],closeView=true;const motionClock=createMotionClock();
const KEYDIR={ArrowUp:'up',ArrowDown:'down',ArrowLeft:'left',ArrowRight:'right',w:'up',s:'down',a:'left',d:'right'};
const isSwing=key=>key===' '||key==='z'||key==='Enter';
const image=path=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(Error('Could not load '+path));im.src=path;});
const announce=t=>$('live').textContent=t;
function resize(){const box=viewport.getBoundingClientRect();scale=closeView?Math.max(2,Math.floor(Math.min(box.width/480,box.height/320))):(box.width<480?box.width/480:Math.max(1,Math.floor(Math.min(box.width/480,box.height/320))));canvas.width=Math.ceil(box.width/scale);canvas.height=Math.ceil(box.height/scale);canvas.style.width=canvas.width*scale+'px';canvas.style.height=canvas.height*scale+'px';ctx.imageSmoothingEnabled=false;}
new ResizeObserver(resize).observe(viewport);
function clearInput(){keys.clear();directionOrder=[];pointers.clear();charging=false;s.player.moving=false;s.ready=latched;document.querySelectorAll('.pressed').forEach(b=>b.classList.remove('pressed'));}
function readyUI(){s.ready=latched||charging;$('ready').setAttribute('aria-pressed',String(s.ready));}
function toggleReady(){if(paused||!loaded||s.swing)return;latched=!latched;readyUI();}
function charge(){if(paused||!loaded||s.swing||charging)return;charging=true;readyUI();$('swing').classList.add('pressed');}
function release(swing=true){if(!charging)return;charging=false;readyUI();$('swing').classList.remove('pressed');if(swing&&!paused)startSwing(s);}
function directionDown(token,dir){directionOrder=directionOrder.filter(k=>k.token!==token);directionOrder.push({token,dir});}
function directionUp(token){directionOrder=directionOrder.filter(k=>k.token!==token);}
function currentDirection(){return directionOrder.at(-1)?.dir;}
for(const button of document.querySelectorAll('[data-dir]')){
 button.addEventListener('pointerdown',e=>{e.preventDefault();if(paused)return;button.setPointerCapture(e.pointerId);pointers.set(e.pointerId,button);directionDown(e.pointerId,button.dataset.dir);button.classList.add('pressed');});
 const finish=e=>{directionUp(e.pointerId);pointers.delete(e.pointerId);button.classList.remove('pressed');};
 button.addEventListener('pointerup',finish);button.addEventListener('pointercancel',finish);button.addEventListener('lostpointercapture',finish);
}
$('swing').addEventListener('pointerdown',e=>{e.preventDefault();if(paused)return;$('swing').setPointerCapture(e.pointerId);pointers.set(e.pointerId,'swing');charge();});
$('swing').addEventListener('pointerup',e=>{if(pointers.get(e.pointerId)==='swing')release();pointers.delete(e.pointerId);});
$('swing').addEventListener('pointercancel',e=>{release(false);pointers.delete(e.pointerId);});
$('swing').addEventListener('lostpointercapture',e=>{if(pointers.has(e.pointerId)){release(false);pointers.delete(e.pointerId);}});
// Assistive technology click activation has no pointerdown/up pair.
$('swing').addEventListener('click',e=>{if(e.detail===0&&!paused){charge();release();}});
$('ready').onclick=toggleReady;
window.addEventListener('keydown',e=>{if(KEYDIR[e.key]||isSwing(e.key)||['r','Escape','b'].includes(e.key))e.preventDefault();if(e.repeat)return;
 if(e.key==='Escape'||e.key==='b'){if(loaded)paused?resume():openBag();return;}if(paused)return;
 if(KEYDIR[e.key]){keys.add(e.key);directionDown(e.key,KEYDIR[e.key]);}else if(isSwing(e.key)){keys.add(e.key);charge();}else if(e.key==='r')toggleReady();
});
window.addEventListener('keyup',e=>{if(KEYDIR[e.key]){directionUp(e.key);keys.delete(e.key);}if(isSwing(e.key)){keys.delete(e.key);release();}});
window.addEventListener('blur',()=>{clearInput();if(loaded&&!paused)openBag();});document.addEventListener('visibilitychange',()=>{if(document.hidden){clearInput();if(loaded&&!paused)openBag();}});
function resume(){if(!loaded)return;paused=false;$('panel').hidden=true;clearInput();readyUI();last=0;acc=0;motionClock.accumulator=0;}
$('begin').onclick=resume;
function openBag(){paused=true;clearInput();$('panel-title').textContent='Your little catches';$('begin').textContent='Back to the meadow';$('bag-actions').hidden=false;
 const content=$('panel-content');content.replaceChildren();const p=document.createElement('p');p.textContent=`${s.caught.length} of 6 caught · ${s.swings} swings`;content.append(p);
 for(const kind of ['button-snail','stag-beetle','isopod']){const caught=s.caught.filter(c=>c.kind===kind);if(!caught.length)continue;const row=document.createElement('div');row.className='catch-row';const im=document.createElement('img');im.src=CRITTER+kind+'/frame-0.png';im.alt='';const label=document.createElement('span');label.textContent=`${caught[0].name} × ${caught.length}`;row.append(im,label);content.append(row);}
 const hint=document.createElement('p');hint.className='subtle';hint.textContent='Hold SWING / Space to creep, release to swing. READY / R keeps the net ready. Move beside a critter and face its tile. A swing waits for your current step to finish. Fast steps startle beetles. Catches last until reload or release. Nothing is saved.';content.append(hint);$('panel').hidden=false;$('begin').focus();}
$('bag').onclick=()=>paused?resume():openBag();$('release').onclick=()=>{s=createNetTest();latched=false;charging=false;$('count').textContent='0 / 6';announce('All critters released into the meadow.');resume();};$('grid').onchange=()=>debug=$('grid').checked;$('zoom').onchange=()=>{closeView=$('zoom').value==='close';resize();};
function rect(c,x,y,w,h,color){c.fillStyle=color;c.fillRect(Math.round(x),Math.round(y),w,h);}
function pixelOval(c,x,y,rx,ry,color){for(let dy=-ry;dy<=ry;dy++){const w=Math.round(rx*Math.sqrt(Math.max(0,1-dy*dy/(ry*ry))));rect(c,x-w,y+dy,w*2+1,1,color);}}
const ground=document.createElement('canvas');ground.width=RULES.width;ground.height=RULES.height;const g=ground.getContext('2d');
// Every terrain cell is an authored 32px tile. Ground is decorative/walkable.
for(let y=0;y<14;y++)for(let x=0;x<20;x++){
 const px=x*32,py=y*32,path=MEADOW[y][x]==='path';rect(g,px,py,32,32,path?'#bbbc7d':'#79a85e');
 if(path){rect(g,px+6,py+9,3,1,'#d3cd95');rect(g,px+23,py+25,3,1,'#a8aa6d');}
 else if((x*3+y*7)%5===0){rect(g,px+11,py+22,7,2,'#6c9b53');rect(g,px+13,py+20,3,3,'#6c9b53');rect(g,px+11,py+19,1,3,'#a4c879');}
 // Walkable ground joins within the tile; no structure or static collider.
 if(!path&&MEADOW[y-1]?.[x]==='path')rect(g,px,py,32,2,'#a9b473');
 if(!path&&MEADOW[y]?.[x-1]==='path')rect(g,px,py,2,32,'#a9b473');
}
for(const [tx,ty]of [[3,3],[15,3],[16,10],[2,9],[13,12],[6,2]]){const x=tx*32+16,y=ty*32+14;rect(g,x,y+5,2,5,'#416c43');rect(g,x-2,y+7,3,2,'#416c43');rect(g,x-2,y,6,4,'#f1d686');rect(g,x,y-2,2,8,'#f1d686');rect(g,x,y+1,2,2,'#c27e51');}
function frameFor(){return s.player.frame;}

function tool(){return images['net-'+s.player.facing+'-'+netPose(s)];}
function drawPlayer(){const p=s.player,x=Math.round(p.x),y=Math.round(p.y),hero=images['hero-'+p.facing+'-'+frameFor()];
 pixelOval(ctx,x,y-1,10,3,'#527e48');const n=tool();if(p.facing==='up')ctx.drawImage(n,x-64,y-80);
 ctx.drawImage(hero,x-16,y-64);
 if(p.facing!=='up'){ctx.drawImage(n,x-64,y-80);
 // The original hand surface sits over the grip. No floating replacement anatomy.
 const crop=p.facing==='left'?[5,47,7,7]:p.facing==='right'?[21,47,7,7]:[23,47,7,7];
 ctx.drawImage(hero,...crop,x-16+crop[0],y-64+crop[1],crop[2],crop[3]);}
}
function drawCritter(c){const frame=Math.floor(s.time/(c.alert?.09:.16))%4;ctx.drawImage(images[c.kind+'-'+frame],Math.round(c.x)-16,Math.round(c.y)-24);
 if(c.alert){const x=c.x,y=c.y-26;rect(ctx,x,y,2,5,'#f4db8f');rect(ctx,x,y+7,2,2,'#f4db8f');}}
function render(){if(!loaded)return;
 camera={x:Math.round(Math.max(0,Math.min(RULES.width-canvas.width,s.player.x-canvas.width/2))),y:Math.round(Math.max(0,Math.min(RULES.height-canvas.height,s.player.y-canvas.height/2)))};
 if(canvas.width>RULES.width)camera.x=-Math.floor((canvas.width-RULES.width)/2);if(canvas.height>RULES.height)camera.y=-Math.floor((canvas.height-RULES.height)/2);
 rect(ctx,0,0,canvas.width,canvas.height,'#79a85e');ctx.save();ctx.translate(-camera.x,-camera.y);ctx.drawImage(ground,0,0);
 const actors=[...s.critters.filter(c=>!c.caught).map(c=>({y:c.y,draw:()=>drawCritter(c)})),{y:s.player.y,draw:drawPlayer}].sort((a,b)=>a.y-b.y);actors.forEach(a=>a.draw());
 if(s.effect?.kind==='catch'){const f=s.effect,t=f.age,x=Math.round(f.x),y=Math.round(f.y);if(t<.75){
  if(t>.3)ctx.drawImage(images[f.critter+'-0'],x-16,y-24-Math.round(Math.sin(Math.min(1,(t-.3)/.4)*Math.PI/2)*18));
  for(let i=0;i<4;i++){const a=i*Math.PI/2+.5,r=9+t*13;rect(ctx,x+Math.cos(a)*r,y-8+Math.sin(a)*r,2,2,'#f4efd7');}
 }}
 if(s.effect?.kind==='miss'&&s.effect.age<.18){const e=s.effect;rect(ctx,e.x-13,e.y+4,4,1,'#d4c48b');rect(ctx,e.x+10,e.y+4,4,1,'#d4c48b');}
 if(debug){const c=catchTile(s);ctx.strokeStyle='#f4df8b';ctx.lineWidth=1;ctx.strokeRect(c.x*32+.5,c.y*32+.5,31,31);for(let x=0;x<640;x+=32){ctx.strokeStyle='#52794b';ctx.beginPath();ctx.moveTo(x+.5,0);ctx.lineTo(x+.5,448);ctx.stroke();}for(let y=0;y<448;y+=32){ctx.beginPath();ctx.moveTo(0,y+.5);ctx.lineTo(640,y+.5);ctx.stroke();}}

 ctx.restore();}
function animate(now){if(!last)last=now;const elapsed=Math.min(.1,(now-last)/1000);last=now;
 if(!paused&&loaded){advanceMotionClock(motionClock,elapsed,()=>{const before=s.caught.length;stepNetTest(s,{directions:directionOrder.map(k=>k.dir)});if(s.caught.length>before){$('count').textContent=s.caught.length+' / 6';announce('Caught '+s.caught.at(-1).name+'. '+s.caught.length+' of 6 critters.');}});}else motionClock.accumulator=0;

 render();requestAnimationFrame(animate);}
try{const jobs=[];for(const d of ['down','up','left','right']){for(const p of ['idle','A','P','C'])jobs.push(['hero-'+d+'-'+p,ASSET+'hero-'+d+'-'+p+'.png']);for(const p of ['carry','ready','windup','sweep','strike','follow','recover'])jobs.push(['net-'+d+'-'+p,ASSET+'net-'+d+'-'+p+'.png']);}for(const c of ['button-snail','stag-beetle','isopod'])for(let f=0;f<4;f++)jobs.push([c+'-'+f,CRITTER+c+'/frame-'+f+'.png']);await Promise.all(jobs.map(async([key,path])=>images[key]=await image(path)));loaded=true;$('begin').disabled=false;$('begin').textContent='Try the net';document.documentElement.dataset.ready='true';resize();requestAnimationFrame(animate);}catch(e){$('begin').textContent='Artwork could not load';announce(e.message);$('panel-content').textContent=e.message;}
// Read-only QA snapshot. Tests use actual input; no mutation/teleport hook.
export function getNetSnapshot(){return structuredClone({state:s,paused,loaded,latched,charging,debug,pose:netPose(s),direction:currentDirection(),canvas:{width:canvas.width,height:canvas.height,scale},camera});}
