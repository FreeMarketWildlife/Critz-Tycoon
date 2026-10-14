import {setupStudioUI,organizePalette} from './ui.js';
import {AREAS,selectedArea,areaDraftKey,areaHref} from './areas.js';
import {HeldDirections,directionForKey,keyInputSource} from '../src/held-input.js';
import {worldViewport} from '../src/world-space.js';
import {readSettings} from '../src/ui-settings.js';
import {EDIT_LAYERS,sameProjectContent,rectBetween,copySelection,pasteSelection,moveStamp,sampleCell,paintLayer,floodLayer,mapCamera} from './authoring.js';
import {tickMapTest,finishMapJump} from './test-motion.js';
import {createMotion,advanceMotion,getMotionView,TICK_SECONDS} from '../src/movement.js';
import {toolMatches} from './tool-search.js';
import{SAVE_KEY,MATERIALS,FEATURES,PRESETS,STAMPS,DIRS,connectBuilding,doorCell,relocateDoorLinks,eraseAt,clone,at,inside,newMap,newProject,demoProject,reviewProject,fenceReviewProject,groveReviewProject,benchReviewProject,editorRepairReviewProject,authoringReviewProject,paint,flood,resizeMap,blocked,placementError,placeObject,objectFootprint,objectAt,move,validate,validationIssues,removePassage,setPassage,importProject,exportProject,exportChat}from'./model.js';
import{MapRenderer}from'./render.js';
const $=id=>document.getElementById(id),renderer=new MapRenderer(),canvas=$('map'),ctx=canvas.getContext('2d'),viewport=$('viewport');
const areaId=new URLSearchParams(location.search).get('area'),area=selectedArea(areaId),draftKey=area?areaDraftKey(area):SAVE_KEY;
const reviewId=new URLSearchParams(location.search).get('review'),review=!areaId&&['me3','me4','me5','me6','me7','grove','bench'].includes(reviewId);
let project=review?(reviewId==='bench'?benchReviewProject():reviewId==='me7'?authoringReviewProject():reviewId==='me6'?editorRepairReviewProject():reviewId==='grove'?groveReviewProject():reviewId==='me5'?fenceReviewProject():reviewProject(reviewId)):demoProject(),undo=[],redo=[],mode='paint',brush='grass',stamp=null,raw=null,zoom=1,ox=40,oy=40,point={x:0,y:0},drag=null,settingsAdd=false,connectionPoint=null,testState=null,space=false,loaded=false,pageActive=true,saveTimer,tileLimit=100,recovery=false,selection=null,selectionAnchor=null,clipboard=null,editLayer='auto',pasteOffset={x:0,y:0};
const layerLabels={auto:'all content',ground:'Ground',features:'Features',raw:'Exact tiles',objects:'Props'};
for(const type of ['click','change'])document.addEventListener(type,e=>{if(!loaded&&e.target.closest?.('button,input,select,textarea')){e.preventDefault();e.stopImmediatePropagation();}},true);
const labels={grass:'Grass',path:'Dirt path',paving:'Concrete',soil:'Garden soil',water:'Water',sand:'Sand beach',cliff:'Mountain',fence:'Wood fence','fence-picket':'White picket fence','fence-barbed':'Barbed wire fence',tallgrass:'Tall grass',flowers:'Flowers',bridge:'Bridge',stairs:'Cliff stairs',cave:'Cliff opening','ledge-down':'Ledge ↓','ledge-up':'Ledge ↑','ledge-left':'Ledge ←','ledge-right':'Ledge →'};
for(const kind of MATERIALS.filter(k=>k.startsWith('water-'))){const [,body,...state]=kind.split('-');labels[kind]=`${body==='fresh'?'Fresh':'Ocean'} ${state.includes('shallow')?'shallow':'deep'} · ${state.includes('moving')?'moving':'still'}`;}
const map=()=>project.maps.find(m=>m.id===project.active);
for(const entry of AREAS)$('areas').add(new Option(entry.name,entry.id));$('areas').value=area?.id||AREAS[0].id;$('load-area').onclick=()=>{cancelStroke();persistDraft();location.assign(areaHref($('areas').value));};
let renderedMap=null;
function positionCanvas(){canvas.style.transform=`translate(${ox}px,${oy}px) scale(${zoom})`;$('zoom-label').textContent=Math.round(zoom*100)+'%';updateCursor();}
function status(s){$('status').textContent=s;}
function snapshot(){return JSON.stringify(project);}
function remember(){undo.push(snapshot());if(undo.length>80)undo.shift();redo=[];}
function persistDraft(){const pending=saveTimer!=null;clearTimeout(saveTimer);saveTimer=null;if(!pending||!loaded)return;if(review){$('saved').textContent='Review sandbox · your saved draft is untouched';return;}if(recovery){$('saved').textContent='Unreadable draft retained. Download or import to recover.';return;}try{localStorage.setItem(draftKey,exportProject(project));$('saved').textContent=(area?'● '+area.name+' draft saved on this device':'● Draft saved on this device');}catch{$('saved').textContent='Draft could not save. Download a project backup.';status('Storage is unavailable or full. Use Save project.');}}
function save(){if(review){$('saved').textContent='Review sandbox · your saved draft is untouched';return;}clearTimeout(saveTimer);saveTimer=setTimeout(persistDraft,150);}
function refresh(){const m=map();canvas.width=m.w*32;canvas.height=m.h*32;renderer.draw(ctx,m,{project,grid:$('grid').checked,collision:$('collision').checked});renderedMap=m;positionCanvas();$('map-dimensions').textContent=`${m.w} × ${m.h} cells · 32px`;$('undo').disabled=!undo.length;$('redo').disabled=!redo.length;$('world-name').textContent=project.name;updateCursor();}
function changed(message){refresh();save();if(message)status(message);}
function normalizeInteraction(){const m=map();point.x=Math.max(0,Math.min(m.w-1,point.x));point.y=Math.max(0,Math.min(m.h-1,point.y));if(selection&&(selection.mapId!==project.active||!inside(m,selection.rect.x,selection.rect.y)||!inside(m,selection.rect.x+selection.rect.w-1,selection.rect.y+selection.rect.h-1))){selection=null;selectionAnchor=null;}if(selectionAnchor&&!inside(m,selectionAnchor.x,selectionAnchor.y))selectionAnchor=null;}
function sync(){normalizeInteraction();const select=$('maps');select.replaceChildren();for(const m of project.maps)select.add(new Option(m.name,m.id));select.value=project.active;$('notes').value=project.notes;refresh();}
function fit(){const m=map();zoom=Math.min(2,Math.max(.125,Math.min((viewport.clientWidth-48)/(m.w*32),(viewport.clientHeight-50)/(m.h*32))));ox=Math.round((viewport.clientWidth-m.w*32*zoom)/2);oy=Math.round((viewport.clientHeight-m.h*32*zoom)/2);if(renderedMap!==m)refresh();else positionCanvas();}
function setZoom(z,x=viewport.clientWidth/2,y=viewport.clientHeight/2){z=Math.max(.125,Math.min(4,z));ox=x-(x-ox)*z/zoom;oy=y-(y-oy)*z/zoom;zoom=z;positionCanvas();}
function setMode(value){
 if(drag)cancelStroke();if(['rectangle','fill','select','eyedropper','paste'].includes(value))stamp=null;
 mode=value;document.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.mode===mode));$('move-stamp').setAttribute('aria-pressed',mode==='move');
 $('selection-label').textContent=['paint','rectangle','fill'].includes(mode)?(stamp?STAMPS[stamp].name:raw?raw:labels[brush]):({spawn:'Set Hero start',warp:'Place passage',pan:'Pan canvas',erase:'Erase selected layer',move:'Move a prop',select:'Select a rectangle',eyedropper:'Pick from '+editLayer,paste:'Place copied selection'}[mode]||mode);
 updateCursor();
}
function chooseLayer(layer){if(editLayer!=='auto'){editLayer=layer;$('edit-layer').value=layer;}}
function selectBrush(value){chooseLayer(MATERIALS.includes(value)?'ground':'features');brush=value;stamp=null;raw=null;if(!['paint','rectangle','fill'].includes(mode))setMode('paint');setMode(mode);document.querySelectorAll('[data-brush]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.brush===brush));document.querySelectorAll('[data-stamp],[data-tile]').forEach(b=>b.setAttribute('aria-pressed','false'));}
function selectStamp(type){chooseLayer('objects');stamp=type;raw=null;setMode('paint');document.querySelectorAll('[data-stamp]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.stamp===type));document.querySelectorAll('[data-brush],[data-tile]').forEach(b=>b.setAttribute('aria-pressed','false'));}
function selectRaw(id,isBlocked){chooseLayer('raw');raw=id;stamp=null;setMode('paint');$('raw-block').checked=isBlocked;renderTiles();document.querySelectorAll('[data-brush],[data-stamp]').forEach(b=>b.setAttribute('aria-pressed','false'));}
function commitProject(next,message){if(sameProjectContent(next,project)){if(message)status('No map content changed.');return false;}remember();project=next;sync();save();if(message)status(message);return true;}
function transaction(operation,message){cancelStroke();try{const next=clone(project);operation(next);return commitProject(next,message);}catch(e){status(e.message);return false;}}
function placeStamp(type,x,y){return transaction(p=>{const m=p.maps.find(m=>m.id===p.active),o=placeObject(m,type,x,y);if(typeof o==='string')throw Error(o);},STAMPS[type].name+' placed.');}
function locationOf(e){const r=viewport.getBoundingClientRect();return{x:Math.floor((e.clientX-r.left-ox)/zoom/32),y:Math.floor((e.clientY-r.top-oy)/zoom/32)};}
const stampGhost=document.createElement('canvas'),footprintGhost=document.createElement('div'),selectionOverlay=document.createElement('div'),pasteGhost=document.createElement('canvas');
for(const [el,id]of [[stampGhost,'stamp-preview'],[footprintGhost,'footprint-preview'],[selectionOverlay,'selection-overlay'],[pasteGhost,'paste-preview']]){el.id=id;el.hidden=true;el.setAttribute('aria-hidden','true');viewport.append(el);}
const setBox=(el,r)=>Object.assign(el.style,{left:ox+r.x*zoom+'px',top:oy+r.y*zoom+'px',width:r.w*zoom+'px',height:r.h*zoom+'px'});
function updateStampGhost(){
 const moving=drag?.kind==='object',o=moving?{...drag.object,x:drag.object.x+point.x-drag.start.x,y:drag.object.y+point.y-drag.start.y}:stamp&&mode==='paint'?{type:stamp,x:point.x,y:point.y}:null;
 stampGhost.hidden=!loaded||!o||!inside(map(),point.x,point.y);footprintGhost.hidden=stampGhost.hidden;if(stampGhost.hidden)return;
 const s=STAMPS[o.type],bounds=renderer.objectBounds(o);stampGhost.width=bounds.w;stampGhost.height=bounds.h;
 const gc=stampGhost.getContext('2d');gc.translate(-bounds.x,-bounds.y);renderer.drawObject(gc,o);setBox(stampGhost,bounds);
 const fp=objectFootprint(o);setBox(footprintGhost,{x:fp.x*32,y:fp.y*32,w:fp.w*32,h:fp.h*32});
 const error=placementError(map(),o.type,o.x,o.y,{ignoreObject:moving?drag.object:null});footprintGhost.classList.toggle('invalid',!!error);footprintGhost.title=error||'Clear ground footprint';
}
function updateSelection(){
 const rect=mode==='paste'&&clipboard?{...point,w:clipboard.w,h:clipboard.h}:selection?.mapId===project.active?selection.rect:null;
 selectionOverlay.hidden=!rect;pasteGhost.hidden=mode!=='paste'||!clipboard;
 if(rect){setBox(selectionOverlay,{x:rect.x*32,y:rect.y*32,w:rect.w*32,h:rect.h*32});selectionOverlay.classList.toggle('pasting',mode==='paste');selectionOverlay.classList.toggle('invalid',rect.x<0||rect.y<0||rect.x+rect.w>map().w||rect.y+rect.h>map().h);}
 if(!pasteGhost.hidden)setBox(pasteGhost,{x:point.x*32+pasteOffset.x,y:point.y*32+pasteOffset.y,w:pasteGhost.width,h:pasteGhost.height});
 $('selection-tools').hidden=!(selection||clipboard||['select','paste'].includes(mode));$('copy-selection').disabled=!selection||selection.mapId!==project.active;$('paste-selection').disabled=!clipboard;$('paste-selection').setAttribute('aria-pressed',mode==='paste');
 $('selection-info').textContent=mode==='paste'&&clipboard?`${clipboard.w} × ${clipboard.h} · ${clipboard.layers.map(a=>layerLabels[a]).join(', ')}` : selection?`${selection.rect.w} × ${selection.rect.h} · ${layerLabels[editLayer]}`:'Drag a rectangle or Shift + arrows';
}
viewport.addEventListener('pointerleave',()=>{stampGhost.hidden=footprintGhost.hidden=true;});
function updateCursor(){
 updateStampGhost();updateSelection();const valid=inside(map(),point.x,point.y),s=stamp?STAMPS[stamp]:{w:1,h:1};$('cursor').hidden=!valid||['pan','paste'].includes(mode);
 Object.assign($('cursor').style,{left:ox+point.x*32*zoom+'px',top:oy+point.y*32*zoom+'px',width:s.w*32*zoom+'px',height:s.h*32*zoom+'px'});
 if(!valid)return;const m=map(),i=at(m,point.x,point.y),o=renderer.pickObject(m,point.x,point.y);
 $('coordinates').textContent=`Cell ${point.x}, ${point.y}`;$('cell-details').textContent=`${point.x}, ${point.y} · ${labels[m.terrain[i]]}${m.features[i]?' · '+labels[m.features[i]]:''}${o?' · '+o.name:''} · ${blocked(m,point.x,point.y)?'Blocked':'Walkable'}${m.raw[i]?' · exact tile '+m.raw[i].id:''}`;
}
function apply(x,y){const cell=at(map(),x,y);if(drag?.kind==='paint'&&drag.seen){if(drag.seen.has(cell))return;drag.seen.add(cell);}paintLayer(project,project.active,x,y,brush,editLayer,{erase:mode==='erase',raw:raw?{id:raw,blocked:$('raw-block').checked}:null});}
function copyRegion(){
 if(!selection||selection.mapId!==project.active){status('Select a rectangle first.');return;}
 try{
  const rect=selection.rect,next=copySelection(project,project.active,rect,editLayer==='auto'?EDIT_LAYERS:[editLayer]);
  const m=map(),objects=next.objects?m.objects.filter(o=>next.objects.some(a=>a.sourceId===o.id)):[];
  const boxes=[{x:rect.x*32,y:rect.y*32,w:rect.w*32,h:rect.h*32},...objects.map(o=>renderer.objectBounds(o))];
  const left=Math.floor(Math.min(...boxes.map(b=>b.x))),top=Math.floor(Math.min(...boxes.map(b=>b.y))),right=Math.ceil(Math.max(...boxes.map(b=>b.x+b.w))),bottom=Math.ceil(Math.max(...boxes.map(b=>b.y+b.h)));
  pasteGhost.width=right-left;pasteGhost.height=bottom-top;const gc=pasteGhost.getContext('2d');gc.translate(-left,-top);
  const preview={...m,terrain:next.layers.includes('ground')?m.terrain:Array(m.w*m.h).fill('grass'),features:next.layers.includes('features')?m.features:Array(m.w*m.h).fill(''),raw:next.layers.includes('raw')?m.raw:{},objects,warps:[]};
  renderer.draw(gc,preview,{markers:false,transparent:true,layers:next.layers,bounds:{x:left,y:top,w:right-left,h:bottom-top}});
  pasteOffset={x:left-rect.x*32,y:top-rect.y*32};clipboard=next;updateCursor();viewport.focus();status(`Copied ${rect.w} × ${rect.h} · ${next.layers.map(a=>layerLabels[a]).join(', ')}. Passages and Hero start stay put.`);
 }catch(e){status(e.message);}
}
function startPaste(){if(!clipboard){status('Copy a selection first.');return;}setMode('paste');viewport.focus();status('Click or Enter to place. Repeat to stamp again; Escape cancels.');}
function placeRegion(){try{const next=pasteSelection(project,project.active,clipboard,point.x,point.y);commitProject(next.project,`Placed ${clipboard.w} × ${clipboard.h}. Repeat to place again; Escape cancels.`);}catch(e){selectionOverlay.classList.add('invalid');status(e.message);}}
function pick(){try{const result=sampleCell(map(),point.x,point.y,editLayer,{boundsFor:o=>{const b=renderer.objectBounds(o);return {x:b.x/32,y:b.y/32,w:b.w/32,h:b.h/32};}});if(result.kind==='stamp')selectStamp(result.value);else if(result.kind==='raw')selectRaw(result.id,result.blocked);else selectBrush(result.value);status('Picked '+(result.value?(labels[result.value]||STAMPS[result.value]?.name):result.id)+'.');}catch(e){status(e.message);}}
$('copy-selection').onclick=copyRegion;$('paste-selection').onclick=startPaste;$('cancel-selection').onclick=()=>{cancelStroke();selection=null;selectionAnchor=null;setMode('paint');status('Selection canceled. Copied content is still available.');};
$('edit-layer').onchange=()=>{
 cancelStroke();editLayer=$('edit-layer').value;
 if(!['select','eyedropper','paste','erase'].includes(mode)){
  if(editLayer==='ground')selectBrush(MATERIALS.includes(brush)?brush:'grass');
  if(editLayer==='features')selectBrush(FEATURES.includes(brush)&&brush?brush:'flowers');
  if(editLayer==='objects')selectStamp(stamp||'tree');
  if(editLayer==='raw')selectRaw(raw||'meadow.grass.0',raw?$('raw-block').checked:false);
 }
 updateCursor();status(editLayer==='auto'?'Auto: terrain restores automatic edges; Erase removes features, exact tiles, props and passages.':`Editing ${editLayer} only. Other layers and passages stay put.`);
};
function line(a,b){let x=a.x,y=a.y;const dx=Math.abs(b.x-x),sx=x<b.x?1:-1,dy=-Math.abs(b.y-y),sy=y<b.y?1:-1;let err=dx+dy;for(let guard=0;guard<512;guard++){apply(x,y);if(x===b.x&&y===b.y)break;const e=2*err;if(e>=dy){err+=dy;x+=sx;}if(e<=dx){err+=dx;y+=sy;}}}
function cancelStroke(){
 if(!drag)return;const old=drag;drag=null;
 if(old.before){project=JSON.parse(old.before);save();}
 if(old.kind==='select'){selection=old.selection;selectionAnchor=old.anchor;}
 if(old.kind==='pan'){ox=old.ox;oy=old.oy;positionCanvas();return;}
 refresh();
}
function undoAction(forward=false){cancelStroke();const context={id:map().id,w:map().w,h:map().h},from=forward?redo:undo,to=forward?undo:redo;if(!from.length)return;to.push(snapshot());project=JSON.parse(from.pop());sync();if(map().id!==context.id||map().w!==context.w||map().h!==context.h)fit();save();status(forward?'Redone.':'Undone.');}
function finishStroke(){
 if(!drag)return;const old=drag;
 if(old.kind==='rectangle'){for(let y=Math.max(0,Math.min(old.start.y,point.y));y<=Math.min(map().h-1,Math.max(old.start.y,point.y));y++)for(let x=Math.max(0,Math.min(old.start.x,point.x));x<=Math.min(map().w-1,Math.max(old.start.x,point.x));x++)apply(x,y);}
 drag=null;
 if(old.kind==='pan'){positionCanvas();return;}
 if(old.before&&snapshot()!==old.before){undo.push(old.before);if(undo.length>80)undo.shift();redo=[];changed('Map updated. Undo restores this whole stroke.');}else {refresh();if(old.before)save();}
}
viewport.addEventListener('pointerdown',e=>{
 if(!loaded||e.button>1)return;if(drag)cancelStroke();point=locationOf(e);viewport.focus();
 if(e.button===1||space||mode==='pan'){drag={kind:'pan',x:e.clientX,y:e.clientY,ox,oy};viewport.setPointerCapture(e.pointerId);return;}
 if(mode==='paste'){placeRegion();return;}if(!inside(map(),point.x,point.y))return;
 if(mode==='select'){drag={kind:'select',start:{...point},selection,anchor:selectionAnchor?{...selectionAnchor}:null};selection={mapId:project.active,rect:rectBetween(point,point)};selectionAnchor={...point};viewport.setPointerCapture(e.pointerId);updateCursor();return;}
 if(mode==='eyedropper'){pick();return;}if(mode==='warp'){openConnections(point);return;}
 if(mode==='spawn'){if(blocked(map(),point.x,point.y)){status('Hero needs a clear walking cell.');return;}transaction(p=>p.maps.find(m=>m.id===p.active).spawn={...point},'Hero start moved.');return;}
 if(mode==='move'){const o=renderer.pickObject(map(),point.x,point.y);if(!o){status('Select a prop footprint or its canopy to move.');return;}drag={kind:'object',object:o,start:{...point}};viewport.setPointerCapture(e.pointerId);updateCursor();return;}
 if(stamp&&mode==='paint'){placeStamp(stamp,point.x,point.y);return;}
 if(mode==='fill'){if(!MATERIALS.includes(brush)||raw||stamp||!['auto','ground'].includes(editLayer)){status('Fill works with Ground or Auto.');return;}transaction(p=>floodLayer(p,p.active,point.x,point.y,brush,editLayer),'Connected ground filled.');return;}
 clearTimeout(saveTimer);drag={kind:mode==='rectangle'?'rectangle':'paint',start:{...point},last:{...point},seen:new Set(),before:snapshot()};viewport.setPointerCapture(e.pointerId);
 if(drag.kind==='paint'){apply(point.x,point.y);refresh();}
});
viewport.addEventListener('pointermove',e=>{
 point=locationOf(e);
 if(drag?.kind==='pan'){ox=drag.ox+e.clientX-drag.x;oy=drag.oy+e.clientY-drag.y;positionCanvas();}
 else if(drag?.kind==='paint'){line(drag.last,point);drag.last={...point};refresh();}
 else if(drag?.kind==='select'){const end={x:Math.max(0,Math.min(map().w-1,point.x)),y:Math.max(0,Math.min(map().h-1,point.y))};selection={mapId:project.active,rect:rectBetween(drag.start,end)};updateCursor();}
 else updateCursor();
});
viewport.addEventListener('pointerup',e=>{
 if(drag?.kind==='object'){point=locationOf(e);const old=drag;drag=null;try{commitProject(moveStamp(project,project.active,old.object.id,old.object.x+point.x-old.start.x,old.object.y+point.y-old.start.y),'Prop moved with its doorway and identity.');}catch(e){status(e.message);}refresh();}
 else finishStroke();
});
viewport.addEventListener('pointercancel',cancelStroke);viewport.addEventListener('lostpointercapture',cancelStroke);viewport.addEventListener('contextmenu',e=>e.preventDefault());
viewport.addEventListener('wheel',e=>{e.preventDefault();if(e.ctrlKey||e.metaKey){const r=viewport.getBoundingClientRect();setZoom(zoom*Math.exp(-e.deltaY*.008),e.clientX-r.left,e.clientY-r.top);}else{ox-=e.deltaX;oy-=e.deltaY;positionCanvas();}},{passive:false});
viewport.addEventListener('dragover',e=>{e.preventDefault();point=locationOf(e);updateCursor();});viewport.addEventListener('drop',e=>{e.preventDefault();const type=e.dataTransfer.getData('application/x-critz-stamp');if(!STAMPS[type])return;point=locationOf(e);placeStamp(type,point.x,point.y);});
for(const i of ['fresh','ocean'])for(const t of ['still','moving','shallow-still','shallow-moving'])labels[`water-${i}-${t}`]=`${i==='fresh'?'Freshwater':'Ocean'} · ${t.replaceAll('-',' ')}`;
function buildPalette(){for(const kind of [...MATERIALS,...FEATURES.filter(f=>f)]){const b=document.createElement('button');b.className='brush';b.dataset.brush=kind;b.setAttribute('aria-pressed',kind==='grass');const c=document.createElement('canvas');c.width=c.height=32;const m=newMap();m.terrain.fill(kind==='cliff'?'cliff':'grass');if(MATERIALS.includes(kind))m.terrain[0]=kind;else m.features[0]=kind;c.getContext('2d').drawImage(renderer.preview(m,0,0),0,0);b.append(c,document.createTextNode(labels[kind]));b.onclick=()=>selectBrush(kind);$(MATERIALS.includes(kind)?'materials':'features').append(b);}for(const[type,s]of Object.entries(STAMPS)){const b=document.createElement('button'),c=document.createElement('canvas');renderer.thumbnail(type,c);b.dataset.stamp=type;b.draggable=true;b.title=`${s.name} · ${s.w} × ${s.h} placement cells · ${s.footprint[2]} × ${s.footprint[3]} solid cells${s.treeArt?" · transparent canopy overhang":""}`;b.append(c,document.createTextNode(s.name));b.onclick=()=>selectStamp(type);b.ondragstart=e=>{selectStamp(type);e.dataTransfer.setData('application/x-critz-stamp',type);};$('stamps').append(b);}renderTiles();}
function renderTiles(){const q=[$('toolbox-search').value,$('tile-search').value].join(' '),sheet=$('sheet').value,allowed=sheet==='all'?null:new Set(renderer[sheet==='world'?'world':sheet==='contact'?'contact':sheet==='revision'?'revision':'extra'].m.tiles.map(t=>t.id));const entries=[...renderer.tiles.values()].filter(t=>(!allowed||allowed.has(t.id))&&toolMatches(q,t.id,t.label||''));$('tiles').replaceChildren();for(const t of entries.slice(0,tileLimit)){const b=document.createElement('button'),c=document.createElement('canvas');c.width=c.height=32;renderer.drawTile(c.getContext('2d'),t.id,0,0);b.append(c);b.dataset.tile=t.id;b.title=t.label?`${t.label} · ${t.id}`:t.id;b.setAttribute('aria-label',t.id);b.setAttribute('aria-pressed',raw===t.id);b.onclick=()=>{selectRaw(t.id,t.blocked??t.layer!=='ground');status(t.id+' selected. Set collision before painting.');};$('tiles').append(b);}$('tile-count').textContent=`${Math.min(tileLimit,entries.length)} of ${entries.length} tiles`;$('more-tiles').hidden=entries.length<=tileLimit;}
setupStudioUI();
$('tile-search').oninput=$('sheet').onchange=()=>{tileLimit=100;renderTiles();};$('more-tiles').onclick=()=>{tileLimit+=100;renderTiles();};
$('toolbox-search').oninput=()=>{const q=$('toolbox-search').value;document.querySelectorAll('.palette-group').forEach(g=>{if(q.trim()){if(!g.hasAttribute('data-before-search'))g.dataset.beforeSearch=String(g.open);g.open=true;}else if(g.hasAttribute('data-before-search')){g.open=g.dataset.beforeSearch==='true';delete g.dataset.beforeSearch;}});for(const b of document.querySelectorAll('[data-brush],[data-stamp]'))b.hidden=!toolMatches(q,b.dataset.brush||b.dataset.stamp,b.textContent);for(const tab of ['terrain','stamps','tiles'])$(tab+'-panel').hidden=q.trim()?false:document.querySelector('[data-tab="'+tab+'"]').getAttribute('aria-selected')!=='true';tileLimit=100;renderTiles();document.querySelectorAll('.palette-group').forEach(g=>g.hidden=Boolean(q.trim())&&!g.querySelector('[data-brush]:not([hidden])'));if(q.trim()){for(const [tab,selector]of [['terrain','[data-brush]:not([hidden])'],['stamps','[data-stamp]:not([hidden])'],['tiles','[data-tile]']])$(tab+'-panel').hidden=!$(tab+'-panel').querySelector(selector);}const count=document.querySelectorAll('[data-brush]:not([hidden]),[data-stamp]:not([hidden]),[data-tile]').length;$('search-results').hidden=!q.trim();$('search-results').textContent=count?`${count} tools shown. Select a result to build.`:'No matching tools. Try house, door, stairs or water.';};
document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{$('toolbox-search').value='';$('toolbox-search').oninput();document.querySelectorAll('[data-tab]').forEach(a=>a.setAttribute('aria-selected',a===b));for(const tab of['terrain','stamps','tiles'])$(tab+'-panel').hidden=tab!==b.dataset.tab;});document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>setMode(b.dataset.mode));$('move-stamp').onclick=()=>{stamp=null;raw=null;setMode('move');};$('undo').onclick=()=>undoAction();$('redo').onclick=()=>undoAction(true);$('grid').onchange=$('collision').onchange=refresh;$('zoom-in').onclick=()=>setZoom(zoom*1.25);$('zoom-out').onclick=()=>setZoom(zoom/1.25);$('fit').onclick=fit;$('maps').onchange=()=>{cancelStroke();selection=null;selectionAnchor=null;project.active=$('maps').value;fit();save();};
function mapSettings(add=false){cancelStroke();if(add&&project.maps.length>=16){status('Project limit: 16 maps.');return;}settingsAdd=add;$('settings-title').textContent=add?'Add another map':'Map settings';$('map-name').value=add?'New area':map().name;$('width').value=add?20:map().w;$('height').value=add?20:map().h;$('preset').value='custom';$('settings-error').textContent='';$('settings-dialog').showModal();}
$('preset').add(new Option('Custom size','custom'));PRESETS.forEach(([name,w,h],i)=>$('preset').add(new Option(`${name} · ${w} × ${h}`,String(i))));$('preset').onchange=()=>{if($('preset').value==='custom')return;const[,w,h]=PRESETS[+$('preset').value];$('width').value=w;$('height').value=h;};$('map-settings').onclick=()=>mapSettings();$('add-map').onclick=()=>mapSettings(true);$('apply-settings').onclick=()=>{try{
 const w=Number($('width').value),h=Number($('height').value),name=$('map-name').value.trim()||'Untitled map',next=clone(project),m=next.maps.find(m=>m.id===next.active),candidate=newMap('map-'+Date.now(),name,w,h);
 if(next.maps.reduce((n,m)=>n+m.w*m.h,0)+(settingsAdd?0:-m.w*m.h)+w*h>65536)throw Error('Project limit: 65,536 cells.');
 if(settingsAdd){next.maps.push(candidate);next.active=candidate.id;}else{resizeMap(m,w,h,next);m.name=name;}
 const changed=commitProject(next,'Map ready.');sync();fit();if(!changed)status('Map settings unchanged. History is retained.');$('settings-dialog').close();
}catch(e){$('settings-error').textContent=e.message;}};
function download(blob,name){const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
$('download').onclick=()=>{cancelStroke();download(new Blob([exportProject(project)],{type:'application/json'}),'critz-world.json');};
$('copy').onclick=async()=>{cancelStroke();const text=exportChat(project);$('data-title').textContent='Copy your world';$('data-description').textContent='Paste this complete text into chat. It includes terrain, buildings, collision rules, notes and map links.';$('data-text').value=text;$('data-text').readOnly=true;$('apply-import').hidden=$('open-file').hidden=true;$('data-error').textContent='';$('data-dialog').showModal();$('data-text').select();try{await navigator.clipboard.writeText(text);$('data-error').textContent='Copied. Paste it into chat when you’re ready.';}catch{$('data-error').textContent='Copy the selected text, or download Save project.';}};
$('import').onclick=()=>{cancelStroke();$('data-title').textContent='Open a map project';$('data-description').textContent='Paste exported map JSON or choose a project file. Import replaces this workspace; Undo restores it.';$('data-text').value='';$('data-text').readOnly=false;$('apply-import').hidden=$('open-file').hidden=false;$('data-error').textContent='';$('data-dialog').showModal();};$('open-file').onclick=()=>$('file-input').click();$('file-input').onchange=async()=>{const f=$('file-input').files[0];if(!f)return;if(f.size>6000000){$('data-error').textContent='File exceeds 6 MB.';return;}$('data-text').value=await f.text();$('file-input').value='';};$('apply-import').onclick=()=>{try{
 const imported=importProject($('data-text').value,new Set(renderer.tiles.keys()));recovery=false;const updated=commitProject(imported,'Project imported. Undo restores the previous world.');sync();fit();if(!updated){save();status('Project unchanged; recovery/save state refreshed. History is retained.');}$('data-dialog').close();
}catch(e){$('data-error').textContent=e.message;}};
$('export-png').onclick=()=>{cancelStroke();const m=map(),c=document.createElement('canvas');c.width=m.w*32;c.height=m.h*32;renderer.draw(c.getContext('2d'),m,{project,markers:false});c.toBlob(b=>download(b,'critz-map.png'));};
$('new-project').onclick=()=>{cancelStroke();recovery=false;const updated=commitProject(newProject(),'Blank world started. Undo restores your previous project.');sync();fit();if(!updated)save();};
$('notes').onchange=()=>{const notes=$('notes').value.slice(0,10000);transaction(p=>{p.notes=notes;},'Map notes updated.');};

function openConnections(p=null){cancelStroke();const building=p?objectAt(map(),p.x,p.y):null;if(building&&doorCell(building))p=doorCell(building);connectionPoint=p?{...p}:null;$('create-room').hidden=!building||!doorCell(building);if(building&&doorCell(building))$('direction').value='up';const m=map();$('target-map').replaceChildren();for(const t of project.maps)$('target-map').add(new Option(t.name,t.id));$('target-map').value=project.maps.find(t=>t.id!==m.id)?.id||m.id;const dest=project.maps.find(t=>t.id===$('target-map').value);$('target-x').value=dest.spawn.x;$('target-y').value=dest.spawn.y;$('edge-fields').hidden=!!p;$('warp-fields').hidden=!p;$('connection-help').textContent=p?`Passage at cell ${p.x}, ${p.y}. Walking onto this cell in the chosen direction goes to the arrival cell. Add a separate return passage if needed.`:'Connect the current map’s outer edge to another map. An offset of 0 aligns their top or left boundaries.';$('connection-error').textContent='';$('existing-connections').replaceChildren();const list=p?m.warps:m.connections;list.forEach((c,i)=>{const row=document.createElement('div');row.className='connection-row';row.append(document.createTextNode(`${c.direction} → ${project.maps.find(m=>m.id===c.target)?.name||c.target}${p?' at '+c.x+','+c.y:' (offset '+c.offset+')'}`));const b=document.createElement('button');b.textContent='Remove';b.onclick=()=>{remember();if(p)removePassage(project,m.id,c);else list.splice(i,1);if(!p){const target=project.maps.find(t=>t.id===c.target),opposite={up:'down',down:'up',left:'right',right:'left'}[c.direction];if(target)target.connections=target.connections.filter(a=>!(a.direction===opposite&&a.target===m.id));}changed('Connection removed.');$('connection-dialog').close();};row.append(b);$('existing-connections').append(row);});$('connection-dialog').showModal();}
$('create-room').onclick=()=>{const o=objectAt(map(),connectionPoint.x,connectionPoint.y);try{const candidate=clone(project),copy=candidate.maps.find(m=>m.id===project.active).objects.find(t=>t.id===o.id);const room=connectBuilding(candidate,project.active,copy);commitProject(candidate,`Door linked to ${room.name}, with a return exit. Test by walking north into the doorway.`);$('connection-dialog').close();}catch(e){$('connection-error').textContent=e.message;}};
$('connections').onclick=()=>openConnections();$('target-map').onchange=()=>{const t=project.maps.find(m=>m.id===$('target-map').value);$('target-x').value=t.spawn.x;$('target-y').value=t.spawn.y;};$('save-connection').onclick=()=>{try{
 const next=clone(project),m=next.maps.find(m=>m.id===next.active),target=next.maps.find(m=>m.id===$('target-map').value),direction=$('direction').value;
 if(connectionPoint){setPassage(next,m.id,{...connectionPoint,target:target.id,tx:Number($('target-x').value),ty:Number($('target-y').value),direction});}
 else{
  const offset=Number($('offset').value);if(target===m)throw Error('Choose a different map for an edge connection.');
  if(!Number.isInteger(offset)||Math.abs(offset)>128)throw Error('Use an integer offset between −128 and 128.');
  const opposite={up:'down',down:'up',left:'right',right:'left'}[direction];
  if(m.connections.some(c=>c.direction===direction)||target.connections.some(c=>c.direction===opposite))throw Error('An edge is already connected. Remove its existing link first.');
  m.connections.push({direction,target:target.id,offset});target.connections.push({direction:opposite,target:m.id,offset:-offset});
 }
 const changed=commitProject(next,'Maps connected. Try walking through in Test.');if(!changed)status('Passage unchanged. Paired returns and history are retained.');$('connection-dialog').close();
}catch(e){$('connection-error').textContent=e.message;}};

$('validate').onclick=()=>{
 cancelStroke();const issues=validationIssues(project);$('check-results').replaceChildren();
 if(!issues.length){const p=document.createElement('p');p.textContent='No unsafe water layouts, broken links or unreachable exits found. Walk the map to check your intended routes.';$('check-results').append(p);}
 for(const issue of issues){
  const row=document.createElement('div'),p=document.createElement('p'),button=document.createElement('button');row.className='check-issue';p.textContent=issue.message;
  button.textContent=`Show ${issue.x},${issue.y}`;button.dataset.issue=issue.code;
  button.onclick=()=>{
   $('check-dialog').close();project.active=issue.mapId;point={x:issue.x,y:issue.y};sync();
   zoom=Math.max(.5,zoom);ox=Math.round(viewport.clientWidth/2-(point.x+.5)*32*zoom);oy=Math.round(viewport.clientHeight/2-(point.y+.5)*32*zoom);
   refresh();viewport.focus();status(issue.message);
  };
  row.append(p,button);$('check-results').append(row);
 }
 $('check-dialog').showModal();
};document.querySelectorAll('[data-close]').forEach(b=>b.onclick=()=>b.closest('dialog').close());
const play=$('play'),pc=play.getContext('2d'),testInput=new HeldDirections();let lastTick=0,frameId=null;
function fitPlay(){const r=$('play-view').getBoundingClientRect(),field=worldViewport(r.width,r.height,readSettings(localStorage).worldZoom);if(!field)return;const {width,height,scale}=field;if(play.width!==width)play.width=width;if(play.height!==height)play.height=height;play.style.width=`${width*scale}px`;play.style.height=`${height*scale}px`;}
function startTest(){cancelStroke();const m=map();if(blocked(m,m.spawn.x,m.spawn.y)){status('Move Hero start to a clear walking cell before testing.');$('validate').click();return;}testState={project:clone(project),map:m.id,player:{...m.spawn,facing:'down'},animation:null};testState.motion=createMotion(testState.player);testState.pendingTime=0;testInput.clear();lastTick=performance.now();testState.time=lastTick;$('test-dialog').showModal();play.focus();drawTest(testState.time);if(frameId===null&&!document.hidden&&pageActive)frameId=requestAnimationFrame(frame);}
function drawTest(now){if(!testState)return;const t=testState,m=t.project.maps.find(m=>m.id===t.map),p={...t.player};if(t.motion&&!t.animation){const v=getMotionView(t.motion);Object.assign(p,{px:v.x*2,py:v.y*2,pose:v.pose,moving:v.moving,actionTick:v.actionTick});}if(t.animation){const a=t.animation,u=Math.min(1,(now-a.start)/a.duration);p.px=a.x*32+((a.tx??p.x)-a.x)*32*u;p.py=a.y*32+((a.ty??p.y)-a.y)*32*u;p.moving=true;p.jump=a.jump;p.progress=u;if(a.bench){p.sitting=a.bench==='enter'?u>=.7:u<.25;p.seat=a.dest.seat||a.from.seat;p.facing=p.sitting?p.seat.facing:a.bench==='enter'?a.from.facing:a.dest.facing;p.bench=a.bench;}if(u===1){finishMapJump(t,now);}}fitPlay();pc.imageSmoothingEnabled=false;pc.fillStyle='#253d34';pc.fillRect(0,0,play.width,play.height);t.camera=mapCamera(m,p,play.width,play.height);t.viewport={width:play.width,height:play.height};const {x:camX,y:camY}=t.camera;pc.save();pc.translate(-camX,-camY);renderer.draw(pc,m,{project:t.project,player:p,dust:t.dust,time:now,markers:false,bounds:{x:camX,y:camY,w:play.width,h:play.height}});pc.restore();$('test-map-name').textContent=m.name;}
function tickTest(now){const t=testState;if(!t)return;const event=tickMapTest(t,testInput.latest(),now);if(event==='bench-enter')$('test-status').textContent='Hop onto seat · facing locks. Release, then move toward the open front to exit.';if(event==='bench-exit')$('test-status').textContent='Leaving through the bench front.';if(event==='jump')$('test-status').textContent='One-way ledge · hopping to clear ground.';if(event==='transition'){testInput.clear();$('test-status').textContent='Entered '+t.project.maps.find(m=>m.id===t.map).name;}}

function frame(now){frameId=null;if(!testState||document.hidden||!pageActive)return;const elapsed=Math.min(100,Math.max(0,now-lastTick));lastTick=now;testState.pendingTime+=elapsed;testState.time+=elapsed;while(testState.pendingTime>=TICK_SECONDS*1000){testState.pendingTime-=TICK_SECONDS*1000;tickTest(testState.time);}drawTest(testState.time);frameId=requestAnimationFrame(frame);}
$('test').onclick=startTest;$('exit-test').onclick=()=>$('test-dialog').close();$('test-dialog').addEventListener('close',()=>{testState=null;testInput.clear();if(frameId!==null)cancelAnimationFrame(frameId);frameId=null;status('Back to your draft. Test movements and pushed boulders were discarded.');});document.querySelectorAll('[data-dir]').forEach(b=>{b.onpointerdown=e=>{e.preventDefault();testInput.press('pointer:'+e.pointerId,b.dataset.dir);b.setPointerCapture(e.pointerId);};b.onpointerup=b.onpointercancel=b.onlostpointercapture=e=>testInput.release('pointer:'+e.pointerId);});
window.addEventListener('keydown',e=>{
 if(!loaded)return;
 const direction=directionForKey(e.key);
 if(testState){if(direction){e.preventDefault();testInput.press(keyInputSource(e),direction);}return;}
 if(e.target.matches('input,textarea,select')||e.target.isContentEditable||document.querySelector('dialog:modal'))return;
 const key=e.key.toLowerCase(),modifier=e.ctrlKey||e.metaKey,onMap=document.activeElement===viewport;
 if(modifier&&key==='z'){e.preventDefault();undoAction(e.shiftKey);return;}
 if(onMap&&modifier&&key==='c'){e.preventDefault();copyRegion();return;}
 if(onMap&&modifier&&key==='v'){e.preventDefault();startPaste();return;}
 if(e.code==='Space'&&onMap){space=true;e.preventDefault();}
 if(e.key==='Escape'){e.preventDefault();cancelStroke();selection=null;selectionAnchor=null;setMode('paint');status('Canceled. Map content and copied selection are retained.');return;}
 if(!onMap)return;
 const shortcut={b:'paint',r:'rectangle',f:'fill',e:'erase',s:'select',h:'pan'}[key];if(shortcut&&!modifier&&!e.altKey){e.preventDefault();setMode(shortcut);return;}
 if(key==='i'&&!modifier){e.preventDefault();setMode('eyedropper');status('Pick a cell from the selected layer.');return;}
 if(direction){
  e.preventDefault();const old={...point},[dx,dy]=DIRS[direction];point.x=Math.max(0,Math.min(map().w-1,point.x+dx));point.y=Math.max(0,Math.min(map().h-1,point.y+dy));
  if(mode==='select'&&e.shiftKey){selectionAnchor??=old;selection={mapId:project.active,rect:rectBetween(selectionAnchor,point)};}else if(mode==='select')selectionAnchor=null;
  updateCursor();return;
 }
 if(e.key==='Enter'){
  e.preventDefault();if(mode==='paste'){placeRegion();return;}if(mode==='eyedropper'){pick();return;}
  if(mode==='select'){selectionAnchor={...point};selection={mapId:project.active,rect:rectBetween(point,point)};updateCursor();return;}
  if(mode==='warp'){openConnections(point);return;}if(mode==='pan'||mode==='move')return;
  if(mode==='spawn'){if(blocked(map(),point.x,point.y)){status('Hero needs a clear walking cell.');return;}transaction(p=>p.maps.find(m=>m.id===p.active).spawn={...point},'Hero start moved.');return;}
  if(stamp){placeStamp(stamp,point.x,point.y);return;}
  if(mode==='fill'){if(!MATERIALS.includes(brush)||raw||!['auto','ground'].includes(editLayer)){status('Fill works with Ground or Auto.');return;}transaction(p=>floodLayer(p,p.active,point.x,point.y,brush,editLayer),'Connected ground filled.');return;}
  transaction(p=>paintLayer(p,p.active,point.x,point.y,brush,editLayer,{erase:mode==='erase',raw:raw?{id:raw,blocked:$('raw-block').checked}:null}),'Cell updated.');
 }
});
window.addEventListener('keyup',e=>{if(e.code==='Space')space=false;testInput.release(keyInputSource(e));});
function syncPageVisibility(){space=false;testInput.clear();lastTick=performance.now();if(document.hidden||!pageActive){cancelStroke();if(frameId!==null)cancelAnimationFrame(frameId);frameId=null;persistDraft();}else if(testState&&frameId===null)frameId=requestAnimationFrame(frame);}
window.addEventListener('blur',()=>{space=false;testInput.clear();cancelStroke();});document.addEventListener('visibilitychange',syncPageVisibility);window.addEventListener('pagehide',()=>{pageActive=false;syncPageVisibility();});window.addEventListener('pageshow',()=>{pageActive=true;syncPageVisibility();});
new ResizeObserver(()=>{if(loaded)positionCanvas();}).observe(viewport);
// Read-only inspection hook for isolated browser QA; game state is never imported.
export function inspect(){return{project:clone(project),mode,brush,stamp,raw,zoom,ox,oy,editLayer,point:{...point},selection:clone(selection),clipboard:clipboard?{w:clipboard.w,h:clipboard.h,layers:[...clipboard.layers],objects:clipboard.objects?.length||0}:null,history:{undo:undo.length,redo:redo.length},test:testState?clone({map:testState.map,camera:testState.camera,viewport:testState.viewport,player:testState.player,benchWaitRelease:testState.benchWaitRelease,motion:getMotionView(testState.motion),animation:testState.animation,dust:testState.dust,time:testState.time,hops:testState.hops||0,landings:testState.landings||0}):null};}
try{await renderer.load();if(areaId&&!area)throw Error('Unknown area. Choose an area from the loader.');if(area){const response=await fetch(new URL(area.path,import.meta.url));if(!response.ok)throw Error('Could not load '+area.name+' base. Reload to retry.');project=importProject(await response.text(),new Set(renderer.tiles.keys()));}try{const saved=review?null:localStorage.getItem(draftKey);if(saved){project=importProject(saved,new Set(renderer.tiles.keys()));$('saved').textContent=area?'● '+area.name+' draft restored · base revision '+area.revision:'● Saved draft restored';}else $('saved').textContent=review?'Review sandbox · your saved draft is untouched':area?area.name+' base · revision '+area.revision+' · edits save separately':'Example clearing · make it yours';}catch(e){recovery=true;$('saved').textContent='Unreadable draft retained. Import a backup to recover.';status(e.message);}buildPalette();organizePalette();sync();loaded=true;fit();status(recovery?'Your stored draft was not overwritten. Import a backup or start a new blank world.':'Ready. Paint terrain, drop a building, then take Hero for a walk.');if(new URLSearchParams(location.search).get('play')==='1'&&!recovery){startTest();$('exit-test').textContent='Edit this map';document.title='Your world · Critz';}}catch(e){status('Editor could not load: '+e.message);$('saved').textContent='Reload to retry loading the tiles.';console.error(e);}
