import {REGIONS,RAMPS,regionAt,matchesRegion,shadeColor,symmetryCounts} from './construction-model.js';
export function createConstruction({getProject,getFrame,onChange,onTemplate,onColor,onReplace,onMessage}){
 const $=id=>document.getElementById(id);let template=null,cache=null,cacheKey='',usedKey='';
 const compatible=()=>{const p=getProject();return !!template&&p?.width===32&&p?.height===64;};
 const region=()=>$('construction-region').value;
 for(const [id,label]of REGIONS)$('construction-region').add(new Option(label,id));
 for(const r of RAMPS)$('shade-ramp').add(new Option(r.label,r.id));
 function ramps(){const box=$('ramp-swatches');box.replaceChildren();const ramp=RAMPS.find(r=>r.id===$('shade-ramp').value);for(const [i,hex]of ramp.colors.entries()){const b=document.createElement('button');b.style.background=hex;b.title=`${i===0?'Darkest':i===ramp.colors.length-1?'Lightest':'Midtone'} · ${hex.toUpperCase()}`;b.setAttribute('aria-label',`Ramp color ${hex}`);b.onclick=()=>onColor(hex);box.append(b);}}
 for(const id of ['construction-show','construction-region','construction-opacity','construction-layer','construction-clip','protect-outline','alpha-lock'])$(id).addEventListener('input',()=>{cacheKey='';if(id==='construction-region'){if(['head','eyes'].includes(region()))$('shade-ramp').value='head';if(region()==='body')$('shade-ramp').value='body';ramps();}onChange();});
 $('shade-ramp').onchange=ramps;ramps();
 $('template-start').onclick=()=>{if(!template)return;$('construction-show').checked=false;$('construction-clip').checked=false;$('protect-outline').checked=false;$('alpha-lock').checked=false;$('construction-region').value='all';onTemplate(structuredClone(template));};
 $('template-guide').onclick=()=>{if(!compatible()){onMessage('The skeleton guide uses a 32 × 64 character canvas. Start from skeleton to use that size.',true);return;}$('clean-view').checked=false;$('construction-show').checked=true;$('construction-layer').value='above';cacheKey='';onChange();onMessage('Your skeleton is a separate guide. Its pixels are excluded from exports.');};
 $('construction-inspect').onclick=()=>$('construction-dialog').showModal();$('construction-close').onclick=()=>$('construction-dialog').close();
 $('replace-color').onclick=()=>onReplace(Number($('replace-source').value),$('replace-scope').value==='all');
 function canEdit(x,y,pixels){
  const p=getProject();if(x<0||y<0||x>=p.width||y>=p.height)return false;
  if($('alpha-lock').checked&&!pixels[y*p.width+x])return false;
  if(compatible()){
   if($('protect-outline').checked&&regionAt(template,x,y)==='outline')return false;
   if($('construction-clip').checked&&!matchesRegion(template,region(),x,y))return false;
  }
  return true;
 }
 function draw(ctx,layer){
  if(!compatible()||!$('construction-show').checked||$('construction-layer').value!==layer)return;
  const key=region();if(key!==cacheKey||!cache){cache=document.createElement('canvas');cache.width=32;cache.height=64;const im=cache.getContext('2d').createImageData(32,64);template.frames[0].pixels.forEach((k,i)=>{if(!k)return;const hex=template.palette[k];im.data[i*4]=parseInt(hex.slice(1,3),16);im.data[i*4+1]=parseInt(hex.slice(3,5),16);im.data[i*4+2]=parseInt(hex.slice(5,7),16);im.data[i*4+3]=matchesRegion(template,region(),i%32,Math.floor(i/32))?255:35;});cache.getContext('2d').putImageData(im,0,0);cacheKey=key;}
  ctx.save();ctx.globalAlpha=Number($('construction-opacity').value)/100;ctx.imageSmoothingEnabled=false;ctx.drawImage(cache,0,0);ctx.restore();
 }
 function update(){
  const p=getProject();if(!p)return;const ok=compatible();
  for(const id of ['construction-show','construction-region','construction-opacity','construction-layer','construction-clip','protect-outline','template-guide'])$(id).disabled=!ok;
  $('construction-availability').textContent=ok?'32 × 64 · exact user template':'Guide needs a 32 × 64 canvas';
  const def=REGIONS.find(r=>r[0]===region());$('region-description').textContent=def[2];$('construction-opacity-value').textContent=$('construction-opacity').value+'%';
  const locks=[];if(ok&&$('construction-clip').checked)locks.push(def[1]);if(ok&&$('protect-outline').checked)locks.push('outline protected');if($('alpha-lock').checked)locks.push('alpha locked');$('paint-limits').textContent=locks.length?'Paint: '+locks.join(' · '):'';
  const frame=getFrame(),pairs=symmetryCounts(frame.pixels,p.width,p.height);$('symmetry-report').textContent=`${pairs.silhouette} silhouette pairs differ · ${pairs.color} color pairs differ${p.width%2?' · odd center column':''}`;
  const used=[...new Set(frame.pixels)].filter(Boolean).sort((a,b)=>a-b),key=used.map(i=>`${i}:${p.palette[i]}`).join(',');
  if(key!==usedKey){const select=$('replace-source'),old=select.value;select.replaceChildren();for(const i of used)select.add(new Option(p.palette[i].toUpperCase(),String(i)));if(used.includes(Number(old)))select.value=old;usedKey=key;}
  $('replace-color').disabled=!used.length;
 }
 return {setTemplate(p){template=p;update();},canEdit,draw,update,shade:(hex,direction)=>shadeColor(hex,direction,$('shade-ramp').value),inspect(x,y){if(!compatible())return '';const r=regionAt(template,x,y),label=REGIONS.find(a=>a[0]===r)?.[1]||'Outside skeleton';const k=template.frames[0].pixels[y*32+x],hex=template.palette[k];return label+(hex&&['#184080','#3878b8','#707078'].includes(hex)?' · shadow':'');},snapshot:()=>({compatible:compatible(),region:region(),shown:$('construction-show').checked,clip:$('construction-clip').checked,protectOutline:$('protect-outline').checked,alphaLock:$('alpha-lock').checked,ramp:$('shade-ramp').value})};
}
