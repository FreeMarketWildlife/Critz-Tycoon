import {DEFAULTS,OPTIONS,compose,project,walkProject,holds,slotAt,slotStart} from './model.js';
import {encodeGif} from './export.js';
const data=await fetch('./data.json').then(r=>{if(!r.ok)throw Error('Hero layers unavailable');return r.json();});
const labels={hair:['Hair',['Twists','Close crop','Bald']],hairColor:['Hair color',['Original brown','Soft black','Warm brown']],skin:['Skin tone',['Original brown','Deep brown','Warm brown']],eyes:['Eyes',['Classic','Short','Amber']],ears:['Ears',['Folded','Soft']],shoes:['Shoes',['Trail red','Forest','Midnight']],nose:['Nose',['None','Small']],mouth:['Mouth',['None','Small line','Smile']]};
let chosen={...DEFAULTS},direction='south',running=false,walking=false,slow=false,elapsed=0,previous=performance.now(),lastKey='';
const $=s=>document.querySelector(s),hero=$('#hero'),native=$('#native'),names={south:'Front',north:'Back',west:'Left',east:'Right'};
for(const key of Object.keys(OPTIONS)){
 const row=document.createElement('div');row.className='control';const label=document.createElement('label');label.htmlFor=key;label.textContent=labels[key][0];const select=document.createElement('select');select.id=key;
 OPTIONS[key].forEach((value,i)=>select.add(new Option(labels[key][1][i],value)));select.value=chosen[key];select.addEventListener('change',()=>{chosen[key]=select.value;lastKey='';$('#notice').textContent='Look updated across all directions and walk poses.';});row.append(label,select);$('#controls').append(row);
}
export function paint(canvas,pixels){const ctx=canvas.getContext('2d'),im=ctx.createImageData(32,64);pixels.forEach((c,i)=>{if(!c)return;im.data[i*4]=parseInt(c.slice(1,3),16);im.data[i*4+1]=parseInt(c.slice(3,5),16);im.data[i*4+2]=parseInt(c.slice(5,7),16);im.data[i*4+3]=255;});ctx.putImageData(im,0,0);}
function state(){const slot=walking?slotAt(direction,elapsed):null;return {chosen:{...chosen},direction,running,walking,slow,elapsed,slot,pose:slot===null?'idle':data.order[slot]};}
function draw(now){if(running)elapsed+=(now-previous)/(slow?4:1);previous=now;const s=state();
 // Derive every visible pose before caching: lineup compares the same phase in
 // all views; only the main view's original direction timing drives playback.
 const visible=[...document.querySelectorAll('[data-lineup]')].map(c=>({canvas:c,direction:c.dataset.lineup,pose:s.pose}));const key=JSON.stringify([chosen,direction,s.pose,s.slot,running,slow,visible.map(x=>[x.direction,x.pose])]);
 if(key!==lastKey){lastKey=key;const pixels=compose(data,direction,s.pose,chosen);paint(hero,pixels);paint(native,pixels);$('#poseLabel').textContent=`${names[direction]} · ${s.pose==='idle'?'Idle':`${running?'Walking':'Paused'} · ${s.pose} · ${s.slot+1}/8`}${slow&&walking?' · Slow':''}`;for(const v of visible)paint(v.canvas,compose(data,v.direction,v.pose,chosen));}
 requestAnimationFrame(draw);
}
function updateMotion(){const b=$('#walk');b.textContent=running?'Pause walk':walking?'Resume walk':'Play walk';b.setAttribute('aria-pressed',String(running));}
function face(dr){if(dr===direction)return;const slot=slotAt(direction,elapsed),fraction=(elapsed%holds(direction).reduce((a,b)=>a+b,0)-slotStart(direction,slot))/holds(direction)[slot];direction=dr;if(walking)elapsed=slotStart(dr,slot)+Math.max(0,fraction)*holds(dr)[slot];document.querySelectorAll('[data-direction]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.direction===dr)));lastKey='';}
document.querySelectorAll('[data-direction]').forEach(b=>b.addEventListener('click',()=>face(b.dataset.direction)));
$('#walk').onclick=()=>{running=!running;walking=true;previous=performance.now();updateMotion();lastKey='';};
$('#slow').onclick=()=>{slow=!slow;$('#slow').setAttribute('aria-pressed',String(slow));lastKey='';};
$('#step').onclick=()=>{const next=walking?(slotAt(direction,elapsed)+1)%8:0;walking=true;running=false;elapsed=slotStart(direction,next);updateMotion();lastKey='';};
$('#idle').onclick=()=>{running=false;walking=false;elapsed=0;updateMotion();lastKey='';};
$('#turn').onclick=()=>{const order=['south','west','north','east'];face(order[(order.indexOf(direction)+1)%4]);};
$('#reset').onclick=()=>{chosen={...DEFAULTS};for(const key in chosen)$('#'+key).value=chosen[key];running=false;walking=false;slow=false;elapsed=0;face('south');$('#slow').setAttribute('aria-pressed','false');updateMotion();lastKey='';$('#notice').textContent='Original Hero look and idle pose restored.';};
function download(blob,name){const a=document.createElement('a'),url=URL.createObjectURL(blob);a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
$('#png').onclick=()=>{const s=state(),canvas=document.createElement('canvas');canvas.width=32;canvas.height=64;paint(canvas,compose(data,direction,s.pose,chosen));canvas.toBlob(blob=>{if(blob)download(blob,`critz-hero-${direction}-${s.pose}.png`);});$('#notice').textContent='Saved this exact pose as a transparent native-size PNG.';};
$('#project').onclick=()=>{download(new Blob([JSON.stringify(project(data,chosen))+'\n'],{type:'application/json'}),'critz-hero-static-poses.sprite.json');$('#notice').textContent='Saved16 static poses with separate walk order and timing metadata.';};
$('#gif').onclick=()=>{download(new Blob([encodeGif(walkProject(data,direction,chosen),holds(direction))],{type:'image/gif'}),`critz-hero-${direction}-walk.gif`);$('#notice').textContent='Saved this direction’s existing walk at its original timing.';};
// Pure inspection only; no browser storage, game state or save integration.
window.__creator={data,compose:(dr,po,s=chosen)=>compose(data,dr,po,s),snapshot:state,project:()=>project(data,chosen),walkProject:()=>walkProject(data,direction,chosen)};
requestAnimationFrame(draw);
