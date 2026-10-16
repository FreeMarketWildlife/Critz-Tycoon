import {createProject,createProjectModel,parseProject,PROJECT_STORAGE,DIRECTIONS,frameAt} from './dummy-creator-model.js';
import {createMirrorToggle} from './mirror.js';
import {createWorkspace} from './workspace.js';
import {line} from './model.js';
import {WIDTH,HEIGHT,SIZE,STORAGE,PART_OPTIONS,PART_DEFINITIONS,CATEGORY_PARTS,validateSeed,pixelAt,importCorrections} from './body-regions-model.js';

// Mode adapter for the existing editor shell. Normal editor handlers are never loaded here.
const $=id=>document.getElementById(id),canvas=$('canvas'),ctx=canvas.getContext('2d'),overlay=$('overlay'),og=overlay.getContext('2d'),view=$('viewport');
document.body.classList.add('body-regions-mode');
document.title='Dummy Creator · Sprite Editor';
let referenceStarted=0,referenceHandle;
let playing=false,playElapsed=0,playStarted=0,animationHandle,referenceFrames=[],referencePlayback=false;
let seed,model,zoom=6,autoFit=true,active=1,tool='brush',drag=null,space=false,workspace,saveTimer,resizeFrame;
const mirror=createMirrorToggle(()=>finish());
const paintLabel=(x,y,id)=>{pause();model.paint(x,y,id,mirror.enabled,$('dc-side').value);};
const requestedDataset=new URL(location.href).searchParams.get('labels')||'phil-20261016';
const DATASETS={'phil-20261016':{id:'phil-20261016',name:'Phil’s supplied labels',url:'./assets/phil-region-labels-20261016.json'}};
let dataset=null,draftKey=null,initialLabels=null;
const touches=new Map();let pinch=null;
const layers={reference:{visible:true,opacity:.4},labels:{visible:true,opacity:1}};

const status=(message,error=false)=>{$('status').textContent=message;$('status').dataset.error=String(error);};
const guard=fn=>async(...args)=>{try{await fn(...args);}catch(e){status(e.message,true);}};
const on=(id,event,fn)=>$(id).addEventListener(event,guard(fn));
const saveState=$('save-state');saveState.textContent='Labels saved separately';
document.querySelector('.header-actions').replaceChildren(saveState);
for(const [id,text]of [['br-copy','Copy project'],['br-import','Import'],['br-download','Download backup']]){const b=document.createElement('button');b.id=id;b.textContent=text;if(id==='br-copy')b.className='accent';document.querySelector('.header-actions').append(b);}
document.querySelector('.project-bar').prepend(Object.assign(document.createElement('strong'),{className:'br-title',textContent:'Dummy Creator'}));
$('tools').innerHTML='<button id="br-brush" aria-label="Label brush, one native pixel" aria-pressed="true"><b>✎</b><span>Label brush</span></button><button id="br-erase" aria-label="Erase to unassigned"><b>▱</b><span>Unassigned</span></button><button id="br-pan" aria-label="Pan canvas"><b>✥</b><span>Pan</span></button>';
document.querySelector('.canvas-options').innerHTML='<label class="br-select">Part <select id="br-part" aria-label="Active body part"></select></label><label><input type="checkbox" id="grid" checked> Grid</label><label><input type="checkbox" id="guides" checked> Guides</label><label class="br-select">Identity <select id="dc-side" aria-label="Anatomical side"><option value="auto">Auto by front/back position</option><option value="left">Character left</option><option value="right">Character right</option><option value="center">Center</option></select></label><span class="br-orientation" id="dc-orientation"></span>';
const datasetBanner=document.createElement('p');datasetBanner.id='br-dataset';datasetBanner.className='br-dataset';datasetBanner.hidden=true;document.querySelector('.canvas-panel').prepend(datasetBanner);
$('canvas-info').textContent='32 × 64 · front';
$('pixel-stats').textContent='2,048 labels';
$('canvas').setAttribute('aria-label','Body-region label canvas. Brush paints one native pixel; arrows move cursor, Enter paints.');
document.querySelector('#inspector .dock-header strong').textContent='Dummy Creator';
document.querySelector('.inspector-scroll').innerHTML=`
 <p class="br-direction"><strong>Region Labels are your dummy.</strong><br>Side identity stays explicit across directions and frames.</p>
 <details id="br-parts-panel" open><summary>Parts <span>1 PIXEL BRUSH</span></summary><div class="panel-content"><div id="br-parts" role="group" aria-label="Body-part labels"></div></div></details>
 <details id="br-layers-panel" open><summary>Layers <span>32 × 64</span></summary><div class="panel-content" id="br-layers"></div></details>
 <details id="br-data-panel" open><summary>Source & corrections</summary><div class="panel-content"><p id="br-source" class="small muted">Loading local source…</p><p class="small">Projects include every direction/frame, duration and anatomical label. Reference images stay separate. Other views start as unedited copies of your supplied layout, not finished perspective drawings.</p><button id="br-reset">Reset labels…</button><button id="dc-recover">Recover earlier label draft…</button></div></details>`;
for(const [name,label]of [['reference','Supplied south walking reference'],['labels','Dummy · Region Labels']]){
 const row=document.createElement('div');row.className='br-layer';
 row.innerHTML=`<label><input id="br-${name}-visible" type="checkbox" ${layers[name].visible?'checked':''}> ${label}</label><label>Opacity <input id="br-${name}-opacity" aria-label="${label} opacity" type="range" min="0" max="100" value="${layers[name].opacity*100}"><output id="br-${name}-value">${Math.round(layers[name].opacity*100)}%</output></label>`;
 $('br-layers').append(row);
 on(`br-${name}-visible`,'change',e=>{layers[name].visible=e.target.checked;render();});
 on(`br-${name}-opacity`,'input',e=>{layers[name].opacity=Number(e.target.value)/100;$(`br-${name}-value`).textContent=e.target.value+'%';render();});
}
const dialogs=document.createElement('div');
dialogs.innerHTML=`<dialog id="br-transfer"><div class="dialog-heading"><h2 id="br-transfer-title">Corrections</h2><button id="br-close-transfer" aria-label="Close corrections">×</button></div><p id="br-transfer-note"></p><textarea id="br-text" rows="10" spellcheck="false" aria-label="Complete body-region correction JSON"></textarea><p id="br-transfer-error" role="alert"></p><div class="dialog-actions"><button id="br-select-text">Select all</button><button id="br-file">Choose backup file</button><button id="br-apply" class="accent">Import corrections</button></div></dialog>
 <dialog id="br-reset-dialog"><h2>Restore supplied layout in this frame?</h2><p>This restores your supplied Region Labels in the current frame. You can undo the reset. Download a backup first to keep a separate copy.</p><div class="dialog-actions"><button id="br-cancel-reset">Cancel</button><button id="br-confirm-reset">Reset labels</button></div></dialog>
 <input type="file" id="br-backup-input" accept="application/json,.json" hidden>`;
document.body.append(dialogs);
for(const id of ['br-copy','br-import','br-download','br-reset'])$(id).disabled=true;
on('help','click',()=>$('help-dialog').showModal());on('close-help','click',()=>$('help-dialog').close());
function setTool(next){finish();tool=next;for(const [id,t]of [['br-brush','brush'],['br-erase','erase'],['br-pan','pan']])$(id).setAttribute('aria-pressed',String(next===t));$('current-tool').textContent=next==='pan'?'Pan':next==='erase'?'Unassigned · 1px':'Label brush · 1px';canvas.style.cursor=next==='pan'?'grab':'crosshair';}
for(const [id,t]of [['br-brush','brush'],['br-erase','erase'],['br-pan','pan']])on(id,'click',()=>setTool(t));
function selectPart(id){active=id;$('br-part').value=String(id);document.querySelectorAll('#br-parts button').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.part)===id)));setTool('brush');}
on('br-part','change',e=>selectPart(Number(e.target.value)));
function save(){clearTimeout(saveTimer);try{localStorage.setItem(draftKey,model.export());$('save-state').textContent='Project saved in this browser';}catch{$('save-state').textContent='Download backup to save';status('Browser storage unavailable or full. Download a backup to keep your corrections.',true);}}
function changed(){syncFrames();render();save();}
function finish(){if(!drag)return;const painted=drag.kind==='paint'&&model?.end();drag=null;if(painted)changed();}
let cursor=[16,40],showCursor=false;
function render(){
 canvas.width=WIDTH;canvas.height=HEIGHT;canvas.style.width=WIDTH*zoom+'px';canvas.style.height=HEIGHT*zoom+'px';
 const px=view.clientWidth,py=view.clientHeight;$('zoom-plane').style.width=WIDTH*zoom+px*2+'px';$('zoom-plane').style.height=HEIGHT*zoom+py*2+'px';Object.assign($('stage').style,{left:px+'px',top:py+'px',width:WIDTH*zoom+'px',height:HEIGHT*zoom+'px'});
 ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,WIDTH,HEIGHT);
 if(seed){const fs=model.frames,shown=playing?frameAt(fs,playElapsed+performance.now()-playStarted):model.index,f=fs[shown];const refIndex=referencePlayback?Math.floor((performance.now()-referenceStarted)/100)%8:f.referenceIndex;

  if(layers.labels.visible){ctx.globalAlpha=layers.labels.opacity;f.labels.forEach((v,i)=>{if(v){ctx.fillStyle=seed.parts[v].color;ctx.fillRect(i%WIDTH,Math.floor(i/WIDTH),1,1);}});ctx.globalAlpha=1;}
  if(model.direction==='south'&&layers.reference.visible&&referenceFrames[refIndex]){ctx.globalAlpha=layers.reference.opacity;ctx.drawImage(referenceFrames[refIndex],0,0);}ctx.globalAlpha=1;
 }
 const w=WIDTH*zoom,h=HEIGHT*zoom;overlay.width=w+48;overlay.height=h+48;overlay.style.width=w+48+'px';overlay.style.height=h+48+'px';og.translate(24,24);
 if($('grid').checked&&zoom>=4){og.strokeStyle='#17241f55';og.beginPath();for(let x=0;x<=w;x+=zoom){og.moveTo(x+.5,0);og.lineTo(x+.5,h);}for(let y=0;y<=h;y+=zoom){og.moveTo(0,y+.5);og.lineTo(w,y+.5);}og.stroke();}
 if($('guides').checked){og.strokeStyle='#ee91b0';og.setLineDash([4,3]);og.beginPath();og.moveTo(16*zoom+.5,0);og.lineTo(16*zoom+.5,h);og.stroke();og.setLineDash([]);og.strokeStyle='#ade28a';og.beginPath();og.moveTo(0,62*zoom+.5);og.lineTo(w,62*zoom+.5);og.stroke();}
 if(showCursor){og.strokeStyle='#fff';og.strokeRect(cursor[0]*zoom+.5,cursor[1]*zoom+.5,zoom-1,zoom-1);}
 $('zoom-value').textContent=zoom+'×';$('undo').disabled=!model?.undoCount;$('redo').disabled=!model?.redoCount;
}
function setZoom(value,point,fit=false){
 autoFit=fit;const vr=view.getBoundingClientRect(),r=canvas.getBoundingClientRect(),p=point||{x:vr.left+view.clientWidth/2,y:vr.top+view.clientHeight/2},native={x:(p.x-r.left)/zoom,y:(p.y-r.top)/zoom};
 zoom=Math.max(1,Math.min(24,Math.round(value)));render();const next=canvas.getBoundingClientRect();view.scrollLeft+=next.left+native.x*zoom-p.x;view.scrollTop+=next.top+native.y*zoom-p.y;
}
function fit(){setZoom(Math.max(1,Math.min(12,Math.floor(Math.min((view.clientWidth-48)/WIDTH,(view.clientHeight-48)/HEIGHT)))),undefined,true);view.scrollLeft=view.clientWidth/2+WIDTH*zoom/2;view.scrollTop=view.clientHeight/2+HEIGHT*zoom/2;}
for(const [id,fn]of [['zoom-in',()=>setZoom(zoom+1)],['zoom-out',()=>setZoom(zoom-1)],['native',()=>setZoom(1)],['fit',fit]])on(id,'click',fn);
for(const id of ['grid','guides'])on(id,'change',render);
view.addEventListener('wheel',e=>{if(!e.ctrlKey&&!e.metaKey)return;e.preventDefault();finish();setZoom(zoom+(e.deltaY<0?1:-1),{x:e.clientX,y:e.clientY});},{passive:false});
canvas.addEventListener('contextmenu',e=>e.preventDefault());
canvas.addEventListener('pointerdown',e=>{
 if(!seed||![0,1,2].includes(e.button))return;pause();e.preventDefault();canvas.setPointerCapture(e.pointerId);
 if(e.pointerType==='touch'){touches.set(e.pointerId,{x:e.clientX,y:e.clientY});if(touches.size>=2){if(drag?.kind==='paint')model.cancel();drag=null;render();const [a,b]=[...touches.values()];pinch={distance:Math.hypot(a.x-b.x,a.y-b.y),zoom,mid:{x:(a.x+b.x)/2,y:(a.y+b.y)/2}};return;}}
 if(drag)return;
 if(tool==='pan'||space||e.button===1){drag={kind:'pan',pointer:e.pointerId,x:e.clientX,y:e.clientY,left:view.scrollLeft,top:view.scrollTop};return;}
 const pos=pixelAt(e.clientX,e.clientY,canvas.getBoundingClientRect());if(!pos)return;showCursor=false;model.begin();drag={kind:'paint',pointer:e.pointerId,last:pos,id:tool==='erase'||e.button===2?0:active};paintLabel(...pos,drag.id);render();
});
canvas.addEventListener('pointermove',e=>{
 if(touches.has(e.pointerId))touches.set(e.pointerId,{x:e.clientX,y:e.clientY});
 if(pinch&&touches.size>=2){const [a,b]=[...touches.values()],mid={x:(a.x+b.x)/2,y:(a.y+b.y)/2};setZoom(pinch.zoom*Math.hypot(a.x-b.x,a.y-b.y)/Math.max(1,pinch.distance),mid);view.scrollLeft-=mid.x-pinch.mid.x;view.scrollTop-=mid.y-pinch.mid.y;pinch.mid=mid;return;}
 const pos=pixelAt(e.clientX,e.clientY,canvas.getBoundingClientRect());if(pos){cursor=pos;$('coordinates').textContent=`x ${pos[0]} · y ${pos[1]} (top = 0)`;$('anatomy-hover').textContent=seed?seed.parts[model.labels[pos[1]*WIDTH+pos[0]]].name:'';}
 if(!drag||drag.pointer!==e.pointerId)return;
 if(drag.kind==='pan'){view.scrollLeft=drag.left-(e.clientX-drag.x);view.scrollTop=drag.top-(e.clientY-drag.y);return;}
 if(!pos){drag.last=null;return;}if(drag.last)line(...drag.last,...pos,(x,y)=>paintLabel(x,y,drag.id));else paintLabel(...pos,drag.id);drag.last=pos;render();
});
function pointerEnd(e){touches.delete(e.pointerId);if(touches.size<2)pinch=null;if(drag?.pointer===e.pointerId)finish();}
for(const type of ['pointerup','pointercancel','lostpointercapture'])canvas.addEventListener(type,pointerEnd);
on('undo','click',()=>{pause();finish();if(model?.undo())changed();});on('redo','click',()=>{pause();finish();if(model?.redo())changed();});
function openTransfer(mode){pause();finish();$('br-transfer-title').textContent=mode==='import'?'Import project':'Copy project';$('br-transfer-note').textContent=mode==='import'?'Paste complete correction JSON or choose a backup. Sources, registration and every label are validated before anything changes.':'All directions, frames, durations and anatomical labels are included. If clipboard access is unavailable, tap Select all, then use your device’s Copy command.';$('br-transfer-error').textContent='';$('br-apply').hidden=mode!=='import';$('br-file').hidden=mode!=='import';$('dc-recovery-choices')?.remove();$('br-text').readOnly=mode!=='import';$('br-text').value=mode==='import'?'':model.export();$('br-transfer').showModal();}
on('br-copy','click',async()=>{if(!seed)return;openTransfer('copy');try{await navigator.clipboard.writeText($('br-text').value);status('Copied complete Dummy Creator project.');}catch{status('Clipboard unavailable. Use Select all and your device’s Copy command.');}});
on('br-select-text','click',()=>{$('br-text').focus();$('br-text').select();$('br-text').setSelectionRange(0,$('br-text').value.length);});
on('br-close-transfer','click',()=>$('br-transfer').close());on('br-import','click',()=>{if(seed)openTransfer('import');});
on('br-apply','click',()=>{try{model.import($('br-text').value);changed();$('br-transfer').close();status('Imported project or active-frame corrections. '+(JSON.parse($('br-text').value).schema==='critz.body-regions.corrections'&&JSON.parse($('br-text').value).version===1?'Legacy generic categories now have front-view side IDs; every marked cell is retained. ':'')+'Undo restores your previous map.');}catch(e){$('br-transfer-error').textContent=e.message;}});
on('br-file','click',()=>$('br-backup-input').click());
on('br-backup-input','change',async e=>{const file=e.target.files[0];e.target.value='';if(!file)return;if(file.size>2000000)throw Error('Backup must be smaller than 2 MB.');$('br-text').value=await file.text();status('Backup loaded for validation. Tap Import corrections to apply.');});
on('br-download','click',()=>{if(!seed)return;finish();const url=URL.createObjectURL(new Blob([model.export()],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download='critz-dummy-creator-project.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);status('Downloaded all dummy directions and frames; no reference raster.');});
on('br-reset','click',()=>{if(seed){pause();finish();$('br-reset-dialog').showModal();}});on('br-cancel-reset','click',()=>$('br-reset-dialog').close());on('br-confirm-reset','click',()=>{model.replace(initialLabels);changed();$('br-reset-dialog').close();status((dataset?'Phil’s supplied labels':'Original RD1 region labels')+' restored. Undo is available.');});
function loadSeed(data,presetLabels=null){
 finish();seed=validateSeed(data);initialLabels=(presetLabels??seed.labels).slice();model=createProjectModel(createProject(seed,initialLabels),seed);draftKey=PROJECT_STORAGE+':'+seed.seedId+':'+dataset.id;
 datasetBanner.hidden=!dataset;datasetBanner.replaceChildren();if(dataset){datasetBanner.textContent=dataset.name+' · editable dummy · separate draft';}
 $('br-reset-dialog').querySelector('p').textContent=dataset?'Restore Phil’s supplied layout in this active frame? Your current preset edits can be recovered with Undo; download a backup first.':'Restore the original RD1 labels? You can undo the reset. Download a backup first.';
 // Historical source seed provides registration only; RD1 pixels are never rendered.
 for(const id of ['br-copy','br-import','br-download','br-reset'])$(id).disabled=false;
 $('br-parts').replaceChildren();$('br-part').replaceChildren();
 for(const option of PART_OPTIONS){
  const p=seed.parts[option.id],ids=CATEGORY_PARTS[p.category],paired=p.category!=='unassigned';
  $('br-part').add(new Option(option.name,p.id));
  const b=document.createElement('button');b.dataset.part=p.id;b.style.setProperty('--part-color',paired?`linear-gradient(to right, ${seed.parts[ids.right].color} 50%, ${p.color} 50%)`:p.color);b.textContent=option.name;
  if(paired)b.title='Anatomical '+p.category+' IDs remain stable. Front/back Auto uses viewpoint; profiles use your explicit side choice.';
  b.onclick=()=>selectPart(p.id);$('br-parts').append(b);
 }
 $('br-source').textContent=`Supplied refined SOUTH: exact 4× block extraction, 8 × 100 ms; walking, no observed idle. West/east/north reference unavailable; do not treat copied starting layouts as finished turns.`;
 status('Loaded your supplied Region Labels as the dummy. Other views are unfinished editable templates; earlier drafts are preserved.');$('save-state').textContent=dataset?'Supplied labels · separate draft':'Original labels · local edits';
 try{const saved=localStorage.getItem(draftKey);if(saved){model=createProjectModel(parseProject(saved,seed),seed);$('save-state').textContent=dataset?'Supplied dataset · restored draft':'Restored label autosave';status('Restored corrections for this exact source and registration.'+'');}}catch{status('Saved corrections do not match this source or are corrupt. They were not loaded; download a backup after editing.',true);}
 timeline.inert=false;syncFrames();selectPart(CATEGORY_PARTS.head.left);fit();document.documentElement.dataset.editorReady='true';document.documentElement.dataset.bodyRegionsReady='true';document.documentElement.dataset.dummyCreatorReady='true';
}
window.addEventListener('keydown',e=>{
 if(e.target.matches('input,textarea,select')||document.querySelector('dialog[open]'))return;const k=e.key.toLowerCase();
 if(e.metaKey||e.ctrlKey){if(k==='z'||k==='y'){e.preventDefault();$(k==='y'||e.shiftKey?'redo':'undo').click();}if(k==='s'){e.preventDefault();$('br-download').click();}return;}
 if(k===' '){e.preventDefault();space=true;}if(k==='b')setTool('brush');if(k==='e')setTool('erase');if(k==='h')setTool('pan');if(k==='+'||k==='=')setZoom(zoom+1);if(k==='-')setZoom(zoom-1);
 if(e.target===canvas){const delta={ArrowLeft:[-1,0],ArrowRight:[1,0],ArrowUp:[0,-1],ArrowDown:[0,1]}[e.key];if(delta){e.preventDefault();cursor=[Math.max(0,Math.min(WIDTH-1,cursor[0]+delta[0])),Math.max(0,Math.min(HEIGHT-1,cursor[1]+delta[1]))];showCursor=true;render();$('coordinates').textContent=`x ${cursor[0]} · y ${cursor[1]} (top = 0)`;}if(e.key==='Enter'&&model){e.preventDefault();model.begin();paintLabel(...cursor,tool==='erase'?0:active);model.end();showCursor=true;changed();}}
});
window.addEventListener('keyup',e=>{if(e.key===' ')space=false;});window.addEventListener('blur',()=>{space=false;touches.clear();pinch=null;finish();});

const timeline=document.createElement('section');timeline.className='dc-timeline';timeline.setAttribute('aria-label','Dummy direction and frames');
timeline.innerHTML=`<div class="dc-row"><label>Direction <select id="dc-direction" aria-label="Direction"><option value="south">South · front</option><option value="west">West · profile draft</option><option value="east">East · profile draft</option><option value="north">North · back draft</option></select></label><button id="dc-play">Play dummy</button><button id="dc-prev" aria-label="Previous frame">←</button><button id="dc-next" aria-label="Next frame">→</button><span id="dc-position"></span></div><div id="dc-frames" role="group" aria-label="Animation frames"></div><details id="dc-frame-options"><summary>Edit frame · add, duration & reference</summary><div class="dc-row"><button id="dc-add">Add blank</button><button id="dc-duplicate">Duplicate</button><button id="dc-delete">Delete frame</button><button id="dc-earlier">Move earlier</button><button id="dc-later">Move later</button><label>Hold ms <input id="dc-duration" aria-label="Frame duration milliseconds" type="number" min="20" max="5000" step="10"></label><label>Name <input id="dc-name" aria-label="Frame name" maxlength="80"></label><label>South ref <select id="dc-reference" aria-label="South reference frame"></select></label><label><input id="dc-reference-play" type="checkbox"> Play reference · 800 ms</label></div></details><p id="dc-draft-note" class="small muted"></p>`;
timeline.inert=true;document.querySelector('.canvas-panel').append(timeline);$('dc-frame-options').open=innerWidth>=900;$('dc-frame-options').addEventListener('toggle',()=>requestAnimationFrame(()=>autoFit?fit():render()));
for(let i=0;i<8;i++)$('dc-reference').add(new Option(`${i+1} · ${['A','A','P','P','C','C','P','P'][i]}`,i));
function pause(){if(!playing)return;playElapsed+=performance.now()-playStarted;const i=frameAt(model.frames,playElapsed);playing=false;cancelAnimationFrame(animationHandle);model.select(model.direction,i);syncFrames();render();}
function tick(){if(!playing)return;render();const i=frameAt(model.frames,playElapsed+performance.now()-playStarted);$('dc-position').textContent=`${i+1}/${model.frames.length} · playing`;animationHandle=requestAnimationFrame(tick);}
function syncFrames(){if(!model)return;const d=model.direction,profile=d==='west'||d==='east';$('dc-direction').value=d;
 if(profile&&$('dc-side').value==='auto')$('dc-side').value=d==='west'?'left':'right';$('dc-side').querySelector('option[value="auto"]').disabled=profile;
 $('dc-orientation').textContent=d==='south'?'Front: screen left = character right':d==='north'?'Back: screen left = character left':'Profile: choose character left/right explicitly; mirror writes the opposite identity';
 $('canvas-info').textContent=`32 × 64 · ${d}`;$('dc-position').textContent=`${model.index+1}/${model.frames.length} · paused`;$('dc-play').textContent=playing?'Pause dummy':'Play dummy';
 $('dc-duration').value=model.frame.durationMs;$('dc-name').value=model.frame.name;$('dc-reference').value=model.frame.referenceIndex;$('dc-reference').disabled=d!=='south';$('dc-reference-play').disabled=d!=='south';
 $('dc-draft-note').textContent=d==='south'?'Your supplied layout is the starting dummy. Editing frames does not alter the walking reference.':'Unfinished view: starts with your unchanged supplied layout. Edit its geometry here; no generated estimate has replaced your dummy.';
 $('dc-frames').replaceChildren();model.frames.forEach((f,i)=>{const b=document.createElement('button');b.textContent=String(i+1);b.setAttribute('aria-label',`Frame ${i+1}: ${f.name}`);b.setAttribute('aria-pressed',String(i===model.index));b.onclick=()=>{pause();finish();model.select(d,i);playElapsed=0;changed();};$('dc-frames').append(b);});
 $('dc-delete').disabled=model.frames.length===1;$('dc-earlier').disabled=model.index===0;$('dc-later').disabled=model.index===model.frames.length-1;
}
$('dc-direction').onchange=()=>{pause();finish();model.select($('dc-direction').value,0);$('dc-side').value=['south','north'].includes(model.direction)?'auto':model.direction==='west'?'left':'right';playElapsed=0;changed();};
on('dc-play','click',()=>{finish();if(playing){pause();save();return;}playElapsed=model.frames.slice(0,model.index).reduce((n,f)=>n+f.durationMs,0);playStarted=performance.now();playing=true;$('dc-play').textContent='Pause dummy';tick();});
for(const [id,fn]of [['dc-add',()=>model.add(true)],['dc-duplicate',()=>model.add()],['dc-delete',()=>model.remove()],['dc-earlier',()=>model.move(-1)],['dc-later',()=>model.move(1)]])on(id,'click',()=>{pause();finish();fn();playElapsed=0;changed();});
for(const [id,delta]of [['dc-prev',-1],['dc-next',1]])on(id,'click',()=>{pause();finish();model.select(model.direction,(model.index+delta+model.frames.length)%model.frames.length);playElapsed=0;changed();});
for(const [id,key,convert]of [['dc-duration','durationMs',Number],['dc-name','name',String],['dc-reference','referenceIndex',Number]])on(id,'change',e=>{pause();finish();try{model.update({[key]:convert(e.target.value)});changed();}finally{syncFrames();}});
on('dc-side','change',()=>{pause();finish();});function referenceTick(){if(!referencePlayback)return;render();referenceHandle=requestAnimationFrame(referenceTick);}on('dc-reference-play','change',e=>{referencePlayback=e.target.checked;cancelAnimationFrame(referenceHandle);referenceStarted=performance.now();if(referencePlayback)referenceTick();else render();});
on('dc-recover','click',()=>{pause();finish();const keys=[STORAGE+':'+seed.seedId,STORAGE+':'+seed.seedId+':dataset:phil-20261016'];const available=keys.filter(k=>localStorage.getItem(k));if(!available.length){status('No earlier body-region drafts found. Import a correction backup instead.');return;}openTransfer('import');$('br-transfer-note').textContent='Earlier drafts are retained unchanged. Choose one to load into the current frame, then Import. Undo restores this project.';const choices=document.createElement('div');choices.id='dc-recovery-choices';for(const k of available){const b=document.createElement('button');b.textContent=k.includes(':dataset:')?'Supplied-label draft':'Earlier default draft';b.onclick=()=>{$('br-text').value=localStorage.getItem(k);};choices.append(b);}$('dc-recovery-choices')?.remove();$('br-transfer-note').after(choices);});
$('br-apply').textContent='Import project / labels';$('br-reset').textContent='Restore supplied layout…';$('br-transfer-title').textContent='Dummy Creator project';$('br-reset-dialog').querySelector('h2').textContent='Restore supplied layout in this frame?';
$('help-dialog').querySelector('h2').textContent='Dummy Creator';$('help-dialog').querySelectorAll('p').forEach((p,i)=>p.textContent=[
'Your Region Labels are the dummy. Choose a direction and frame, then paint one native pixel. Front/back automatic sides reverse with viewpoint. Profiles require an explicit anatomical side. Mirror paints the opposite side identity; it does not infer hidden limbs.',
'Other directions begin as unchanged copies of your supplied layout, explicitly unfinished. Add blank frames or duplicate and edit. Duration controls playback; Next visits each saved frame. Nothing generates or approves new anatomy.',
'The supplied south reference has eight 100 ms frames and no observed idle. It stays separate from dummy frames. West/east/north references are unavailable until reviewed; RD1 is not rendered.',
'Copy project or Download backup preserves all directions, frames, durations and side IDs. Earlier label drafts remain recoverable and legacy correction imports affect only the active frame. Browser autosave is isolated from normal drawings and game saves. Undo/Redo also restores structural frame edits.'
][i]||'');
workspace=createWorkspace({storageKey:PROJECT_STORAGE+'.layout',defaultSections:['br-parts-panel','br-layers-panel','br-data-panel'],onResize:()=>{cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(()=>autoFit?fit():render());},onAnimationCollapse:()=>{}});
setTool('brush');render();
try{const response=await fetch('./assets/body-regions-seed.json',{cache:'no-store'});if(!response.ok)throw Error('Missing source seed');const source=validateSeed(await response.json());let labels=null;if(requestedDataset){dataset=Object.hasOwn(DATASETS,requestedDataset)?DATASETS[requestedDataset]:null;if(!dataset)throw Error('Unknown requested label dataset; no original map was substituted');const preset=await fetch(dataset.url,{cache:'no-store'});if(!preset.ok)throw Error('Requested supplied labels unavailable; no original map was substituted');labels=importCorrections(await preset.text(),source);}referenceFrames=await Promise.all(Array.from({length:8},(_,i)=>new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>resolve(image);image.onerror=()=>resolve(null);image.src=`./assets/refined-south/frame-${i}.png`;})));loadSeed(source,labels);if(referenceFrames.some(f=>!f))status('Dummy loaded. Some south reference frames are unavailable; your labels remain editable.',true);}catch(e){$('br-source').textContent='Source data unavailable. Reload to recover; saved projects remain in browser storage.';status('Source seed unavailable or invalid: '+e.message,true);workspace.showInspector();}
// QA reads label state, never source raster or ordinary project/browser storage.
export function getBodyRegionSnapshot(){return{project:model?.data,direction:model?.direction,frame:model?.index,playing,ready:!!model,referenceFramesLoaded:referenceFrames.filter(Boolean).length,referencePlaying:referencePlayback,referenceIndex:referencePlayback?Math.floor((performance.now()-referenceStarted)/100)%8:model?.frame.referenceIndex,seedId:seed?.seedId,labels:model?.labels,zoom,tool,active,mirror:mirror.enabled,dataset:dataset?.id||null,draftKey,layers:structuredClone(layers),undo:model?.undoCount,redo:model?.redoCount};}
