import {DEFAULTS,OPTIONS,compose,project,walkPose} from './model.js';
const data=await fetch('./data.json').then(r=>{if(!r.ok)throw Error('Hero layers unavailable');return r.json();});
const labels={hair:['Hair',['Twists','Bald']],hairColor:['Hair color',['Original brown','Soft black','Warm brown']],skin:['Skin tone',['Original brown','Deep brown','Warm brown']],eyes:['Eyes',['Classic','Short']],ears:['Ears',['Classic','Soft shading']],shoes:['Shoes',['Trail blue','Coral accent','Forest accent']],nose:['Nose',['None','Tiny hint']],mouth:['Mouth',['None','Tiny hint']]};
let chosen={...DEFAULTS},direction='south',walking=false,slow=false,view='dressed',start=performance.now(),lastKey='';
const $=s=>document.querySelector(s),hero=$('#hero'),native=$('#native');
for(const key of Object.keys(OPTIONS)){
 const row=document.createElement('div');row.className='control';const label=document.createElement('label');label.htmlFor=key;label.textContent=labels[key][0];const select=document.createElement('select');select.id=key;
 OPTIONS[key].forEach((value,i)=>{const o=new Option(labels[key][1][i],value);select.add(o);});select.value=chosen[key];select.addEventListener('change',()=>{chosen[key]=select.value;lastKey='';$('#notice').textContent='Look updated across all directions and walk poses.';});row.append(label,select);$('#controls').append(row);
}
function paint(canvas,pixels){const ctx=canvas.getContext('2d'),im=ctx.createImageData(32,64);pixels.forEach((c,i)=>{if(!c)return;im.data[i*4]=parseInt(c.slice(1,3),16);im.data[i*4+1]=parseInt(c.slice(3,5),16);im.data[i*4+2]=parseInt(c.slice(5,7),16);im.data[i*4+3]=255;});ctx.putImageData(im,0,0);}
const names={south:'Front',north:'Back',west:'Left',east:'Right'};
function draw(now){const pose=walking?walkPose(data,direction,now-start,slow):'idle',key=JSON.stringify([chosen,direction,pose,walking,slow,view]);if(key!==lastKey){lastKey=key;const pixels=compose(data,direction,pose,chosen,view);paint(hero,pixels);paint(native,pixels);$('#poseLabel').textContent=`${names[direction]} · ${walking?'Walking':'Idle'}${slow&&walking?' · Slow':''}`;for(const c of document.querySelectorAll('[data-lineup]')){const dr=c.dataset.lineup;paint(c,compose(data,dr,walking?walkPose(data,dr,now-start,slow):'idle',chosen,view));}}requestAnimationFrame(draw);}
function face(dr){direction=dr;document.querySelectorAll('[data-direction]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.direction===dr)));lastKey='';}
document.querySelectorAll('[data-direction]').forEach(b=>b.addEventListener('click',()=>face(b.dataset.direction)));
$('#walk').onclick=()=>{walking=!walking;start=performance.now();$('#walk').setAttribute('aria-pressed',String(walking));$('#walk').textContent=walking?'Pause walk':'Walk';lastKey='';};
$('#slow').onclick=()=>{slow=!slow;start=performance.now();$('#slow').setAttribute('aria-pressed',String(slow));lastKey='';};
$('#turn').onclick=()=>{const order=['south','west','north','east'];face(order[(order.indexOf(direction)+1)%4]);};
$('#view').onchange=e=>{view=e.target.value;lastKey='';};
$('#reset').onclick=()=>{chosen={...DEFAULTS};for(const key in chosen)$('#'+key).value=chosen[key];view='dressed';$('#view').value=view;lastKey='';$('#notice').textContent='Original Hero look restored.';};
function download(blob,name){const a=document.createElement('a'),url=URL.createObjectURL(blob);a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
$('#png').onclick=()=>{const canvas=document.createElement('canvas');canvas.width=32;canvas.height=64;const pose=walking?walkPose(data,direction,performance.now()-start,slow):'idle';paint(canvas,compose(data,direction,pose,chosen));canvas.toBlob(blob=>{if(blob)download(blob,`critz-hero-${direction}-${pose}.png`);});$('#notice').textContent='Saved your dressed Hero as a transparent native-size PNG.';};
$('#project').onclick=()=>{download(new Blob([JSON.stringify(project(data,chosen))+'\n'],{type:'application/json'}),'critz-hero.sprite.json');$('#notice').textContent='Saved all16 unique poses for the Sprite Editor.';};
// Inspection exposes pure snapshot data only; it never touches game state or saves.
window.__creator={data,compose:(dr,po,s=chosen,v='dressed')=>compose(data,dr,po,s,v),snapshot:()=>({chosen:{...chosen},direction,walking,slow,view}),project:()=>project(data,chosen)};
requestAnimationFrame(draw);
