import {createMirrorToggle} from './mirror.js';
import {createWorkspace} from './workspace.js';
import {line} from './model.js';
import {WIDTH,HEIGHT,SIZE,STORAGE,PART_OPTIONS,validateSeed,createLabelModel,pixelAt,exportCorrections,importCorrections} from './body-regions-model.js';

// Mode adapter for the existing editor shell. Normal editor handlers are never loaded here.
const $=id=>document.getElementById(id),canvas=$('canvas'),ctx=canvas.getContext('2d'),overlay=$('overlay'),og=overlay.getContext('2d'),view=$('viewport');
document.body.classList.add('body-regions-mode');
document.title='Body regions · Sprite Editor';
let seed,model,zoom=6,autoFit=true,active=1,tool='brush',drag=null,space=false,workspace,saveTimer,resizeFrame;
const mirror=createMirrorToggle(()=>finish());
const paintLabel=(x,y,id)=>model.paintAnatomical(x,y,id,mirror.enabled,seed.registration.facing);
const touches=new Map();let pinch=null;
const layers={reference:{visible:true,opacity:.4},dummy:{visible:true,opacity:1},labels:{visible:true,opacity:.6}};
const rasters={};
const status=(message,error=false)=>{$('status').textContent=message;$('status').dataset.error=String(error);};
const guard=fn=>async(...args)=>{try{await fn(...args);}catch(e){status(e.message,true);}};
const on=(id,event,fn)=>$(id).addEventListener(event,guard(fn));
const saveState=$('save-state');saveState.textContent='Labels saved separately';
document.querySelector('.header-actions').replaceChildren(saveState);
for(const [id,text]of [['br-copy','Copy Corrections'],['br-import','Import'],['br-download','Download backup']]){const b=document.createElement('button');b.id=id;b.textContent=text;if(id==='br-copy')b.className='accent';document.querySelector('.header-actions').append(b);}
document.querySelector('.project-bar').prepend(Object.assign(document.createElement('strong'),{className:'br-title',textContent:'Body-region corrections'}));
$('tools').innerHTML='<button id="br-brush" aria-label="Label brush, one native pixel" aria-pressed="true"><b>✎</b><span>Label brush</span></button><button id="br-erase" aria-label="Erase to unassigned"><b>▱</b><span>Unassigned</span></button><button id="br-pan" aria-label="Pan canvas"><b>✥</b><span>Pan</span></button>';
document.querySelector('.canvas-options').innerHTML='<label class="br-select">Part <select id="br-part" aria-label="Active body part"></select></label><label><input type="checkbox" id="grid" checked> Grid</label><label><input type="checkbox" id="guides" checked> Guides</label><span class="br-orientation">Front: screen left = character right · paired colors automatic</span>';
$('canvas-info').textContent='32 × 64 · front';
$('pixel-stats').textContent='2,048 labels';
$('canvas').setAttribute('aria-label','Body-region label canvas. Brush paints one native pixel; arrows move cursor, Enter paints.');
document.querySelector('#inspector .dock-header strong').textContent='Body regions';
document.querySelector('.inspector-scroll').innerHTML=`
 <p class="br-direction"><strong>Character’s left = screen right.</strong><br>Front view only · paired colors follow each painted side</p>
 <details id="br-parts-panel" open><summary>Parts <span>1 PIXEL BRUSH</span></summary><div class="panel-content"><div id="br-parts" role="group" aria-label="Body-part labels"></div></div></details>
 <details id="br-layers-panel" open><summary>Layers <span>FIXED REGISTRATION</span></summary><div class="panel-content" id="br-layers"></div></details>
 <details id="br-data-panel" open><summary>Source & corrections</summary><div class="panel-content"><p id="br-source" class="small muted">Loading local source…</p><p class="small">Only labels change. Copy and backup include all 2,048 cells and source identities; reference images are excluded from correction exports.</p><button id="br-reset">Reset labels…</button><button id="br-load-seed">Load seed file…</button></div></details>`;
for(const [name,label]of [['reference','Reference'],['dummy','RD1 dummy'],['labels','Region labels']]){
 const row=document.createElement('div');row.className='br-layer';
 row.innerHTML=`<label><input id="br-${name}-visible" type="checkbox" ${layers[name].visible?'checked':''}> ${label}</label><label>Opacity <input id="br-${name}-opacity" aria-label="${label} opacity" type="range" min="0" max="100" value="${layers[name].opacity*100}"><output id="br-${name}-value">${Math.round(layers[name].opacity*100)}%</output></label>`;
 $('br-layers').append(row);
 on(`br-${name}-visible`,'change',e=>{layers[name].visible=e.target.checked;render();});
 on(`br-${name}-opacity`,'input',e=>{layers[name].opacity=Number(e.target.value)/100;$(`br-${name}-value`).textContent=e.target.value+'%';render();});
}
const dialogs=document.createElement('div');
dialogs.innerHTML=`<dialog id="br-transfer"><div class="dialog-heading"><h2 id="br-transfer-title">Corrections</h2><button id="br-close-transfer" aria-label="Close corrections">×</button></div><p id="br-transfer-note"></p><textarea id="br-text" rows="10" spellcheck="false" aria-label="Complete body-region correction JSON"></textarea><p id="br-transfer-error" role="alert"></p><div class="dialog-actions"><button id="br-select-text">Select all</button><button id="br-file">Choose backup file</button><button id="br-apply" class="accent">Import corrections</button></div></dialog>
 <dialog id="br-reset-dialog"><h2>Reset body-region labels?</h2><p>This restores the original RD1 labels for this source. You can undo the reset. Download a backup first to keep a separate copy.</p><div class="dialog-actions"><button id="br-cancel-reset">Cancel</button><button id="br-confirm-reset">Reset labels</button></div></dialog>
 <input type="file" id="br-backup-input" accept="application/json,.json" hidden><input type="file" id="br-seed-input" accept="application/json,.json" hidden>`;
document.body.append(dialogs);
for(const id of ['br-copy','br-import','br-download','br-reset'])$(id).disabled=true;
$('help-dialog').querySelector('h2').textContent='Correct the body-region map';
$('help-dialog').querySelectorAll('p').forEach((p,i)=>{p.textContent=[
 'Choose a named part and paint on the existing canvas. Arm, Hand, Leg and Foot / shoe automatically choose the anatomical left/right ID and its color. Each brush point changes one native pixel. Drag to draw a continuous stroke; Undo and Redo work per stroke. Unassigned erases a label. You can label empty canvas cells too.',
 'Character-relative left is screen right in this front view. Reference, RD1 dummy and region labels have independent visibility and opacity. Their registration stays fixed. Grid and Guides do not change labels.',
 'Use + / − or Fit for sharp integer zoom. Pan tool or Space-drag moves the view; two fingers pan and pinch over the canvas. Arrow keys move the keyboard cursor; Enter paints. B brush, E unassigned, H pan, Command/Control Z undo, Shift Z redo.',
 'Copy Corrections always provides selectable JSON, including all 2,048 labels and exact source identities. Download backup saves the same data. Import rejects mismatched sources or registration. Label autosaves are isolated from ordinary sprite projects and game saves. Source images never enter correction files or autosaves.'
 ][i]||'';});
on('help','click',()=>$('help-dialog').showModal());on('close-help','click',()=>$('help-dialog').close());
function setTool(next){finish();tool=next;for(const [id,t]of [['br-brush','brush'],['br-erase','erase'],['br-pan','pan']])$(id).setAttribute('aria-pressed',String(next===t));$('current-tool').textContent=next==='pan'?'Pan':next==='erase'?'Unassigned · 1px':'Label brush · 1px';canvas.style.cursor=next==='pan'?'grab':'crosshair';}
for(const [id,t]of [['br-brush','brush'],['br-erase','erase'],['br-pan','pan']])on(id,'click',()=>setTool(t));
function selectPart(id){active=id;$('br-part').value=String(id);document.querySelectorAll('#br-parts button').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.part)===id)));setTool('brush');}
on('br-part','change',e=>selectPart(Number(e.target.value)));
function save(){clearTimeout(saveTimer);try{localStorage.setItem(STORAGE+':'+seed.seedId,exportCorrections(seed,model.labels));$('save-state').textContent='Labels saved in this browser';}catch{$('save-state').textContent='Download backup to save';status('Browser storage unavailable or full. Download a backup to keep your corrections.',true);}}
function changed(){render();save();}
function finish(){if(!drag)return;const painted=drag.kind==='paint'&&model?.end();drag=null;if(painted)changed();}
function raster(bytes){const c=document.createElement('canvas');c.width=WIDTH;c.height=HEIGHT;c.getContext('2d').putImageData(new ImageData(new Uint8ClampedArray(bytes),WIDTH,HEIGHT),0,0);return c;}
let cursor=[16,40],showCursor=false;
function render(){
 canvas.width=WIDTH;canvas.height=HEIGHT;canvas.style.width=WIDTH*zoom+'px';canvas.style.height=HEIGHT*zoom+'px';
 const px=view.clientWidth,py=view.clientHeight;$('zoom-plane').style.width=WIDTH*zoom+px*2+'px';$('zoom-plane').style.height=HEIGHT*zoom+py*2+'px';Object.assign($('stage').style,{left:px+'px',top:py+'px',width:WIDTH*zoom+'px',height:HEIGHT*zoom+'px'});
 ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,WIDTH,HEIGHT);
 if(seed){for(const name of ['dummy','reference'])if(layers[name].visible){ctx.globalAlpha=layers[name].opacity;ctx.drawImage(rasters[name],0,0);}ctx.globalAlpha=1;
  if(layers.labels.visible){ctx.globalAlpha=layers.labels.opacity;model.labels.forEach((v,i)=>{if(v){ctx.fillStyle=seed.parts[v].color;ctx.fillRect(i%WIDTH,Math.floor(i/WIDTH),1,1);}});ctx.globalAlpha=1;}
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
 if(!seed||![0,1,2].includes(e.button))return;e.preventDefault();canvas.setPointerCapture(e.pointerId);
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
on('undo','click',()=>{finish();if(model?.undo())changed();});on('redo','click',()=>{finish();if(model?.redo())changed();});
function openTransfer(mode){finish();$('br-transfer-title').textContent=mode==='import'?'Import corrections':'Copy Corrections';$('br-transfer-note').textContent=mode==='import'?'Paste complete correction JSON or choose a backup. Sources, registration and every label are validated before anything changes.':'All 2,048 labels are included. If clipboard access is unavailable, tap Select all, then use your device’s Copy command.';$('br-transfer-error').textContent='';$('br-apply').hidden=mode!=='import';$('br-file').hidden=mode!=='import';$('br-text').readOnly=mode!=='import';$('br-text').value=mode==='import'?'':exportCorrections(seed,model.labels);$('br-transfer').showModal();}
on('br-copy','click',async()=>{if(!seed)return;openTransfer('copy');try{await navigator.clipboard.writeText($('br-text').value);status('Copied all 2,048 labels and source identities.');}catch{status('Clipboard unavailable. Use Select all and your device’s Copy command.');}});
on('br-select-text','click',()=>{$('br-text').focus();$('br-text').select();$('br-text').setSelectionRange(0,$('br-text').value.length);});
on('br-close-transfer','click',()=>$('br-transfer').close());on('br-import','click',()=>{if(seed)openTransfer('import');});
on('br-apply','click',()=>{try{const labels=importCorrections($('br-text').value,seed);model.replace(labels);changed();$('br-transfer').close();status('Imported all 2,048 labels. Undo restores your previous map.');}catch(e){$('br-transfer-error').textContent=e.message;}});
on('br-file','click',()=>$('br-backup-input').click());
on('br-backup-input','change',async e=>{const file=e.target.files[0];e.target.value='';if(!file)return;if(file.size>100000)throw Error('Backup must be smaller than 100 KB.');$('br-text').value=await file.text();status('Backup loaded for validation. Tap Import corrections to apply.');});
on('br-download','click',()=>{if(!seed)return;finish();const url=URL.createObjectURL(new Blob([exportCorrections(seed,model.labels)],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download='critz-body-region-corrections.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);status('Downloaded correction backup: 2,048 labels, no reference raster.');});
on('br-reset','click',()=>{if(seed){finish();$('br-reset-dialog').showModal();}});on('br-cancel-reset','click',()=>$('br-reset-dialog').close());on('br-confirm-reset','click',()=>{model.replace(seed.labels);changed();$('br-reset-dialog').close();status('Original RD1 region labels restored. Undo is available.');});
on('br-load-seed','click',()=>$('br-seed-input').click());
on('br-seed-input','change',async e=>{const file=e.target.files[0];e.target.value='';if(!file)return;if(file.size>200000)throw Error('Seed file is too large.');const next=validateSeed(JSON.parse(await file.text()));if(seed&&!confirm('Load this source seed? Download a backup first if you need your current corrections.'))return;loadSeed(next);});
function loadSeed(data){
 finish();seed=validateSeed(data);model=createLabelModel(seed.labels);rasters.reference=raster(seed.referenceRGBA);rasters.dummy=raster(seed.dummyRGBA);
 for(const id of ['br-copy','br-import','br-download','br-reset'])$(id).disabled=false;
 $('br-parts').replaceChildren();$('br-part').replaceChildren();
 for(const option of PART_OPTIONS){
  const p=seed.parts[option.id],paired=p.id>=6;
  $('br-part').add(new Option(option.name+(paired?' · automatic sides':''),p.id));
  const b=document.createElement('button');b.dataset.part=p.id;b.style.setProperty('--part-color',paired?`linear-gradient(to right, ${seed.parts[p.id+1].color} 50%, ${p.color} 50%)`:p.color);b.textContent=option.name;
  if(paired)b.title='Front: screen left → character right; screen right → character left. Each side keeps its distinct color and ID.';
  b.onclick=()=>selectPart(p.id);$('br-parts').append(b);
 }
 $('br-source').textContent=`${seed.seedId} · reference ${seed.source.reference.gifSha256?.slice(0,12)||seed.source.reference.id} · dummy ${seed.source.dummy.sha256.slice(0,12)}`;
 status('Reference, RD1 dummy and region labels loaded. Choose a part to correct.');$('save-state').textContent='Original labels · saved locally';
 try{const saved=localStorage.getItem(STORAGE+':'+seed.seedId);if(saved){model=createLabelModel(importCorrections(saved,seed));$('save-state').textContent='Restored label autosave';status('Restored corrections for this exact source and registration.');}}catch{status('Saved corrections do not match this source or are corrupt. They were not loaded; download a backup after editing.',true);}
 selectPart(1);fit();document.documentElement.dataset.editorReady='true';document.documentElement.dataset.bodyRegionsReady='true';
}
window.addEventListener('keydown',e=>{
 if(e.target.matches('input,textarea,select')||document.querySelector('dialog[open]'))return;const k=e.key.toLowerCase();
 if(e.metaKey||e.ctrlKey){if(k==='z'||k==='y'){e.preventDefault();$(k==='y'||e.shiftKey?'redo':'undo').click();}if(k==='s'){e.preventDefault();$('br-download').click();}return;}
 if(k===' '){e.preventDefault();space=true;}if(k==='b')setTool('brush');if(k==='e')setTool('erase');if(k==='h')setTool('pan');if(k==='+'||k==='=')setZoom(zoom+1);if(k==='-')setZoom(zoom-1);
 if(e.target===canvas){const delta={ArrowLeft:[-1,0],ArrowRight:[1,0],ArrowUp:[0,-1],ArrowDown:[0,1]}[e.key];if(delta){e.preventDefault();cursor=[Math.max(0,Math.min(WIDTH-1,cursor[0]+delta[0])),Math.max(0,Math.min(HEIGHT-1,cursor[1]+delta[1]))];showCursor=true;render();$('coordinates').textContent=`x ${cursor[0]} · y ${cursor[1]} (top = 0)`;}if(e.key==='Enter'&&model){e.preventDefault();model.begin();paintLabel(...cursor,tool==='erase'?0:active);model.end();showCursor=true;changed();}}
});
window.addEventListener('keyup',e=>{if(e.key===' ')space=false;});window.addEventListener('blur',()=>{space=false;touches.clear();pinch=null;finish();});
workspace=createWorkspace({storageKey:STORAGE+'.layout',defaultSections:['br-parts-panel','br-layers-panel','br-data-panel'],onResize:()=>{cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(()=>autoFit?fit():render());},onAnimationCollapse:()=>{}});
setTool('brush');render();
try{const response=await fetch('./assets/body-regions-seed.json',{cache:'no-store'});if(!response.ok)throw Error('Missing source seed');loadSeed(await response.json());}catch(e){$('br-source').textContent='Source seed unavailable. Reload the editor, or use Load seed file to open a saved copy.';status('Source seed unavailable or invalid: '+e.message,true);workspace.showInspector();}
// QA reads label state, never source raster or ordinary project/browser storage.
export function getBodyRegionSnapshot(){return{ready:!!model,seedId:seed?.seedId,labels:model?.labels,zoom,tool,active,mirror:mirror.enabled,layers:structuredClone(layers),undo:model?.undoCount,redo:model?.redoCount};}
