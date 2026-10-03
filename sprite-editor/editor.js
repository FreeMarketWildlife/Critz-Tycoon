import {createWorkspace} from './workspace.js';
import {createReferenceEditor} from './reference-editor.js';
import {PRESETS,TICK_MS,MAX_PIXELS,makeProject,validateProject,isCharacter,usedColors,line,fill,nearest,bounds,describe,gifBytes} from './model.js';
const $=id=>document.getElementById(id),canvas=$('canvas'),ctx=canvas.getContext('2d'),overlay=$('overlay'),og=overlay.getContext('2d'),view=$('viewport');
const STORAGE='fmw.sprite-editor.v1';
let autoFit=true,pointerAnchor=null,backgroundPan=null,zoomAnchor=null;
let banks,allowed,project,frame=0,tool='pencil',color=1,zoom=6,history=[],future=[],stroke=null,space=false,playing=false,playFrame=0,lastTime=0,elapsed=0,saveTimer,renderPending=false;
const scratch=document.createElement('canvas');
const status=(message,error=false)=>{$('status').textContent=message;$('status').dataset.error=error;};
const guarded=fn=>async(...args)=>{try{await fn(...args);}catch(e){status(e.message,true);}};
const listen=(id,event,fn)=>$(id).addEventListener(event,guarded(fn));
const clone=()=>structuredClone(project);
function pushHistory(before=clone()){history.push(before);const limit=Math.max(2,Math.min(40,Math.floor(4_000_000/(project.width*project.height*project.frames.length))));while(history.length>limit)history.shift();future=[];}
function autosave(){clearTimeout(saveTimer);$('save-state').textContent='Saving locally…';saveTimer=setTimeout(()=>{try{localStorage.setItem(STORAGE,JSON.stringify(project));$('save-state').textContent='Saved in this browser';}catch{$('save-state').textContent='Download a project to save';status('Browser storage is unavailable or full. Use Save project to keep your work.',true);}},220);}
function changed(){autosave();renderAll();}
function stop(){playing=false;$('play').textContent='▶ Play';elapsed=0;renderAll();}
function restore(p){project=p;frame=Math.min(frame,p.frames.length-1);if(!banks.some(b=>b.id===p.bank))p.bank=banks[0].id;color=Math.min(color,p.palette.length-1);stop();renderAll();autosave();}
function commit(action){stop();const before=clone();action();try{validateProject(project,allowed);}catch(e){project=before;throw e;}pushHistory(before);changed();}
function bank(){return banks.find(b=>b.id===project.bank)||banks[0];}
function index(hex){let i=project.palette.indexOf(hex);if(i<0){project.palette.push(hex);i=project.palette.length-1;}return i;}
function activePixels(){return project.frames[frame].pixels;}
function imageFrame(target,f=project.frames[frame]){target.width=project.width;target.height=project.height;const g=target.getContext('2d'),im=g.createImageData(project.width,project.height);f.pixels.forEach((v,i)=>{if(v){const c=project.palette[v];im.data[i*4]=parseInt(c.slice(1,3),16);im.data[i*4+1]=parseInt(c.slice(3,5),16);im.data[i*4+2]=parseInt(c.slice(5,7),16);im.data[i*4+3]=255;}});g.putImageData(im,0,0);g.imageSmoothingEnabled=false;return target;}
function renderCanvas(){
 if(!project)return;const w=project.width,h=project.height;
 if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;}
 const padX=view.clientWidth,padY=view.clientHeight;
 $('zoom-plane').style.width=w*zoom+padX*2+'px';$('zoom-plane').style.height=h*zoom+padY*2+'px';$('stage').style.left=padX+'px';$('stage').style.top=padY+'px';
 canvas.style.width=w*zoom+'px';canvas.style.height=h*zoom+'px';$('stage').style.width=w*zoom+'px';$('stage').style.height=h*zoom+'px';ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,w,h);
 if($('ref-layer').value==='behind')reference.draw(ctx);
 if($('onion').checked&&!playing){for(const [i,tint] of [[frame-1,'#72d9c0'],[frame+1,'#d699c8']])if(project.frames[i]){imageFrame(scratch,project.frames[i]);const g=scratch.getContext('2d');g.globalCompositeOperation='source-in';g.fillStyle=tint;g.fillRect(0,0,w,h);g.globalCompositeOperation='source-over';ctx.globalAlpha=.25;ctx.drawImage(scratch,0,0);ctx.globalAlpha=1;}}
 imageFrame(scratch,project.frames[playing?playFrame:frame]);ctx.drawImage(scratch,0,0);
 if($('ref-layer').value==='above')reference.draw(ctx);
 drawGuides();reference.renderHandles();renderPreview();
 const colors=usedColors(project);$('pixel-stats').textContent=`${colors.size}${isCharacter(project)?'/31':''} colors · ${w} × ${h} px`;
}
function drawGuides(){
 const w=project.width*zoom,h=project.height*zoom;overlay.width=w+48;overlay.height=h+48;overlay.style.width=w+48+'px';overlay.style.height=h+48+'px';og.clearRect(0,0,w+48,h+48);og.translate(24,24);
 if($('grid').checked&&zoom>=4){og.strokeStyle='#15271e33';og.lineWidth=1;og.beginPath();for(let x=0;x<=w;x+=zoom){og.moveTo(x+.5,0);og.lineTo(x+.5,h);}for(let y=0;y<=h;y+=zoom){og.moveTo(0,y+.5);og.lineTo(w,y+.5);}og.stroke();}
 if($('guides').checked){og.font='9px ui-monospace,monospace';og.textAlign='right';og.textBaseline='middle';const step=zoom>=3?10:50;for(let y=0;y<=project.height;y++){if((project.height-y)%step&&y!==0)continue;og.strokeStyle='#50877a88';og.beginPath();og.moveTo(0,y*zoom+.5);og.lineTo(w,y*zoom+.5);og.stroke();og.fillStyle='#bcccbc';og.fillText(String(project.height-y),-5,y*zoom);}
 og.strokeStyle='#b55563';og.lineWidth=1;og.setLineDash([4,3]);og.beginPath();og.moveTo(w/2+.5,0);og.lineTo(w/2+.5,h);og.stroke();og.setLineDash([]);og.textAlign='center';og.fillStyle='#d7a9ac';og.fillText(`x${project.width/2}`,w/2,-10);og.fillStyle='#bcccbc';og.textAlign='left';og.fillText('0',0,-10);og.textAlign='right';og.fillText(String(project.width),w,-10);}
}
function renderPreview(){const p=$('preview');imageFrame(p,project.frames[playing?playFrame:frame]);const scale=Number($('preview-scale').value);p.style.width=project.width*scale+'px';p.style.height=project.height*scale+'px';$('preview-label').textContent=`${scale}× · artwork only · ${playing?'playing':project.frames[frame].name}`;}
function renderFrames(){const box=$('frames');box.replaceChildren();project.frames.forEach((f,i)=>{const b=document.createElement('button');b.className='frame-card';b.setAttribute('aria-pressed',i===frame);b.setAttribute('aria-label',`Frame ${i+1}: ${f.name}`);b.title=`${f.name} · ${f.ticks} ticks`;const c=document.createElement('canvas');imageFrame(c,f);const label=document.createElement('span');label.textContent=String(i+1).padStart(2,'0')+' · '+f.ticks+'t';b.append(c,label);b.onclick=()=>{stop();frame=i;renderAll();};box.append(b);});$('frame-count').textContent=`${String(project.frames.length).padStart(2,'0')} FRAME${project.frames.length===1?'':'S'}`;}
function renderPalette(){
 const box=$('swatches');box.replaceChildren();
 for(const slot of bank().slots){
  const transparent=slot.slot===0,hex=slot.hex.toLowerCase(),i=transparent?0:index(hex),b=document.createElement('button');
  if(transparent)b.className='transparent-swatch';else b.style.background=hex;
  b.title=`${String(slot.slot).padStart(2,'0')} · ${slot.name} · ${slot.hex} · ${slot.group}`;
  b.setAttribute('aria-label',`Color ${slot.hex}: ${slot.name}`);b.setAttribute('aria-pressed',i===color);
  b.onclick=()=>{color=i;renderPalette();workspace.revealCanvas();};box.append(b);
 }
 const hex=project.palette[color]||'#00000000',slot=bank().slots.find(s=>s.hex.toLowerCase()===hex.toLowerCase());
 $('color-chip').style.background=color?hex:'transparent';$('color-chip').classList.toggle('transparent-swatch',!color);
 $('color-value').textContent=hex.toUpperCase();$('color-value').title=slot?.name||'Preserved legacy color';
 $('color-name').textContent=slot?.name||'Preserved legacy color';$('palette-count').textContent='32 slots';
}
function renderAll(){if(!project)return;renderPalette();renderCanvas();renderFrames();$('project-name').value=project.name;$('preset').value=project.preset;$('bank').value=project.bank;$('notes').value=project.notes;$('frame-name').value=project.frames[frame].name;$('ticks').value=project.frames[frame].ticks;$('timing').textContent=`${Math.round(project.frames[frame].ticks*TICK_MS)} ms · ${Math.round(project.frames.reduce((a,f)=>a+f.ticks,0)*TICK_MS)} ms loop`;$('canvas-info').textContent=`${project.width} × ${project.height} px`;$('zoom-value').textContent=zoom+'×';$('undo').disabled=!history.length;$('redo').disabled=!future.length;$('delete-frame').disabled=project.frames.length===1;$('earlier').disabled=frame===0;$('later').disabled=frame===project.frames.length-1;}
function requestRender(){if(renderPending)return;renderPending=true;requestAnimationFrame(()=>{renderPending=false;renderCanvas();});}
function selectTool(t){reference.finish();tool=t;document.querySelectorAll('[data-tool]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.tool===tool));$('current-tool').textContent=tool[0].toUpperCase()+tool.slice(1)+(tool==='pencil'?' · 1px':'');canvas.style.cursor=tool==='pan'?'grab':'crosshair';}
function setZoom(value,anchor,fromFit=false){
 autoFit=fromFit;
 const v=view.getBoundingClientRect(),before=canvas.getBoundingClientRect();
 const point=anchor||{x:v.left+view.clientWidth/2,y:v.top+view.clientHeight/2};
 // Use the actual canvas origin, including its centering margin and scroll.
 // Viewport-only ratios lose this offset and snap the image toward a corner.
 const reuse=!fromFit&&zoomAnchor&&zoomAnchor.x===point.x&&zoomAnchor.y===point.y&&zoomAnchor.left===view.scrollLeft&&zoomAnchor.top===view.scrollTop&&zoomAnchor.width===view.clientWidth&&zoomAnchor.height===view.clientHeight;
 const pixel=reuse?zoomAnchor.pixel:{x:(point.x-before.left)/zoom,y:(point.y-before.top)/zoom};
 zoom=Math.max(1,Math.min(24,Math.floor(Math.sqrt(8_000_000/(project.width*project.height))),Math.round(value)));
 renderCanvas();$('zoom-value').textContent=zoom+'×';
 const after=canvas.getBoundingClientRect();
 view.scrollLeft+=after.left+pixel.x*zoom-point.x;
 view.scrollTop+=after.top+pixel.y*zoom-point.y;
 // Browsers round scroll offsets. Reuse the intended pixel across a wheel
 // burst so subpixel rounding cannot accumulate into visible drift.
 zoomAnchor={...point,pixel,left:view.scrollLeft,top:view.scrollTop,width:view.clientWidth,height:view.clientHeight};
}
function fit(){setZoom(Math.max(1,Math.min(12,Math.floor(Math.min((view.clientWidth-64)/project.width,(view.clientHeight-64)/project.height)))),undefined,true);view.scrollLeft=view.clientWidth/2+project.width*zoom/2;view.scrollTop=view.clientHeight/2+project.height*zoom/2;zoomAnchor=null;}
function position(e){const r=canvas.getBoundingClientRect();return [Math.floor((e.clientX-r.left)/zoom),Math.floor((e.clientY-r.top)/zoom)];}
function paint(x,y,c){if(x<0||y<0||x>=project.width||y>=project.height)return;activePixels()[y*project.width+x]=c;if($('mirror').checked)activePixels()[y*project.width+project.width-1-x]=c;}
function canPaint(c){if(!c||!isCharacter(project))return true;const used=usedColors(project);if(!used.has(c)&&used.size>=31){status('31-color budget reached. Use an existing color or erase one first.',true);return false;}return true;}
canvas.addEventListener('pointerdown',e=>{if(e.button!==0&&e.button!==2&&e.button!==1)return;if(stroke)return;e.preventDefault();stop();const [x,y]=position(e);if(x<0||y<0||x>=project.width||y>=project.height)return;canvas.setPointerCapture(e.pointerId);
 if(tool==='pan'||space||e.button===1){stroke={pan:true,px:e.clientX,py:e.clientY,sx:view.scrollLeft,sy:view.scrollTop};return;}
 if(tool==='picker'){color=activePixels()[y*project.width+x];renderPalette();return;}
 const c=tool==='eraser'||e.button===2?0:color;if(!canPaint(c))return;stroke={before:clone(),start:[x,y],last:[x,y],c};
 if(tool==='fill'){fill(activePixels(),project.width,project.height,x,y,c);if($('mirror').checked)fill(activePixels(),project.width,project.height,project.width-1-x,y,c);}
 else paint(x,y,c);requestRender();});
canvas.addEventListener('pointermove',e=>{const [x,y]=position(e);$('coordinates').textContent=`x ${Math.max(0,Math.min(project.width-1,x))} · Y ${project.height-1-Math.max(0,Math.min(project.height-1,y))}`;if(!stroke)return;if(stroke.pan){view.scrollLeft=stroke.sx-(e.clientX-stroke.px);view.scrollTop=stroke.sy-(e.clientY-stroke.py);return;}
 const tx=Math.max(0,Math.min(project.width-1,x)),ty=Math.max(0,Math.min(project.height-1,y));
 if(tool==='line'||tool==='rectangle'){project.frames[frame].pixels=[...stroke.before.frames[frame].pixels];const [sx,sy]=stroke.start;if(tool==='line')line(sx,sy,tx,ty,(a,b)=>paint(a,b,stroke.c));else{line(sx,sy,tx,sy,(a,b)=>paint(a,b,stroke.c));line(tx,sy,tx,ty,(a,b)=>paint(a,b,stroke.c));line(tx,ty,sx,ty,(a,b)=>paint(a,b,stroke.c));line(sx,ty,sx,sy,(a,b)=>paint(a,b,stroke.c));}}
 else if(tool!=='fill')line(...stroke.last,tx,ty,(a,b)=>paint(a,b,stroke.c));stroke.last=[tx,ty];requestRender();});
function endStroke(){if(!stroke)return;const s=stroke;stroke=null;if(s.before){if(s.before.frames[frame].pixels.some((v,i)=>v!==activePixels()[i])){pushHistory(s.before);changed();}else renderAll();}}
canvas.addEventListener('pointerup',endStroke);canvas.addEventListener('pointercancel',endStroke);canvas.addEventListener('lostpointercapture',endStroke);canvas.addEventListener('contextmenu',e=>e.preventDefault());
document.querySelectorAll('[data-tool]').forEach(b=>b.onclick=()=>selectTool(b.dataset.tool));
listen('undo','click',()=>{endStroke();if(!history.length)return;future.push(clone());restore(history.pop());status('Undone.');});listen('redo','click',()=>{if(!future.length)return;history.push(clone());restore(future.pop());status('Redone.');});
for(const id of ['grid','guides','onion'])listen(id,'change',renderCanvas);listen('preview-scale','change',renderPreview);
listen('zoom-in','click',()=>setZoom(zoom+1));listen('zoom-out','click',()=>setZoom(zoom-1));listen('native','click',()=>setZoom(1));listen('fit','click',fit);
view.addEventListener('wheel',e=>{if(!e.deltaY)return;e.preventDefault();setZoom(zoom+(e.deltaY<0?1:-1),{x:e.clientX,y:e.clientY});},{passive:false});
view.addEventListener('pointermove',e=>{pointerAnchor={x:e.clientX,y:e.clientY};if(backgroundPan&&e.pointerId===backgroundPan.id){view.scrollLeft=backgroundPan.left-(e.clientX-backgroundPan.x);view.scrollTop=backgroundPan.top-(e.clientY-backgroundPan.y);}});
view.addEventListener('pointerleave',()=>{pointerAnchor=null;});
view.addEventListener('pointerdown',e=>{if(stroke||!(space||tool==='pan'||e.button===1)||e.target.closest('button')||![0,1].includes(e.button))return;e.preventDefault();backgroundPan={id:e.pointerId,x:e.clientX,y:e.clientY,left:view.scrollLeft,top:view.scrollTop};view.setPointerCapture(e.pointerId);});
for(const event of ['pointerup','pointercancel','lostpointercapture'])view.addEventListener(event,()=>{backgroundPan=null;});
listen('bank','change',()=>{project.bank=$('bank').value;color=index(bank().colors[0]);renderPalette();autosave();status('Palette selected. Existing pixels keep their exact colors.');});
listen('project-name','change',()=>commit(()=>project.name=$('project-name').value.trim()||'Untitled sprite'));
listen('notes','change',()=>commit(()=>project.notes=$('notes').value));listen('frame-name','change',()=>commit(()=>project.frames[frame].name=$('frame-name').value.trim()||`Frame ${frame+1}`));listen('ticks','change',()=>{const n=Number($('ticks').value);if(!Number.isInteger(n)||n<1||n>600){$('ticks').value=project.frames[frame].ticks;throw Error('Use a whole-number hold between 1 and 600 ticks.');}commit(()=>project.frames[frame].ticks=n);});
listen('clear-frame','click',()=>commit(()=>activePixels().fill(0)));
function addFrame(duplicate){if(project.frames.length>=64||(project.frames.length+1)*project.width*project.height>MAX_PIXELS)throw Error('Frame limit reached (64 frames / 2 million pixels).');commit(()=>{const f=duplicate?structuredClone(project.frames[frame]):{name:`Frame ${project.frames.length+1}`,ticks:8,pixels:Array(project.width*project.height).fill(0)};if(duplicate)f.name=f.name.slice(0,73)+' copy';project.frames.splice(frame+1,0,f);frame++;});}
listen('add-frame','click',()=>addFrame(false));listen('duplicate','click',()=>addFrame(true));listen('delete-frame','click',()=>{if(project.frames.length<=1)return;commit(()=>{project.frames.splice(frame,1);frame=Math.min(frame,project.frames.length-1);});});
for(const [id,d] of [['earlier',-1],['later',1]])listen(id,'click',()=>{if(frame+d<0||frame+d>=project.frames.length)return;commit(()=>{[project.frames[frame],project.frames[frame+d]]=[project.frames[frame+d],project.frames[frame]];frame+=d;});});
listen('play','click',()=>{if(playing){stop();return;}endStroke();playing=true;playFrame=frame;elapsed=0;lastTime=performance.now();$('play').textContent='Ⅱ Pause';});
function animate(now){if(playing){if(!document.hidden){elapsed+=Math.min(now-lastTime,1000);while(elapsed>=project.frames[playFrame].ticks*TICK_MS){elapsed-=project.frames[playFrame].ticks*TICK_MS;playFrame=(playFrame+1)%project.frames.length;}renderCanvas();[...$('frames').children].forEach((b,i)=>b.classList.toggle('playing',i===playFrame));}lastTime=now;}requestAnimationFrame(animate);}requestAnimationFrame(animate);
document.addEventListener('visibilitychange',()=>{lastTime=performance.now();});window.addEventListener('blur',()=>{space=false;endStroke();if(playing)stop();});
let pendingPreset='character';
function newDialog(id){pendingPreset=id;const p=PRESETS.find(a=>a[0]===id);$('new-width').value=p[2];$('new-height').value=p[3];$('preset-description').textContent=p[1]+' · '+p[2]+' × '+p[3]+' pixels';$('new-width').disabled=id!=='custom'&&id!=='building';$('new-height').disabled=id!=='custom'&&id!=='building';$('new-dialog').showModal();$('preset').value=project.preset;}
listen('preset','change',()=>newDialog($('preset').value));listen('new-project','click',()=>newDialog(project.preset));
listen('create-canvas','click',e=>{e.preventDefault();const w=Number($('new-width').value),h=Number($('new-height').value);if(!Number.isInteger(w)||!Number.isInteger(h)||w<1||h<1||w>480||h>480)throw Error('Choose whole-pixel dimensions from 1 to 480.');if(pendingPreset==='building'&&(w%32||h%32))throw Error('Building dimensions must be multiples of 32px.');const p=makeProject(bank().colors,pendingPreset,w,h);p.bank=project.bank;commit(()=>{project=p;frame=0;});reference.clear();$('new-dialog').close();fit();status('New canvas ready. Undo restores your previous project.');});
function filename(ext){return (project.name.replace(/[^a-z0-9_-]+/gi,'-').replace(/^-|-$/g,'')||'sprite')+ext;}
function download(blob,name){const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),10000);status('Downloaded '+name);}
function png(c,name){c.toBlob(blob=>{if(blob)download(blob,name);else status('PNG export failed.',true);},'image/png');}
listen('save-project','click',()=>download(new Blob([JSON.stringify(project)],{type:'application/json'}),filename('.fmw.json')));
listen('export-png','click',()=>{const c=document.createElement('canvas');imageFrame(c);png(c,filename(`-frame-${frame+1}.png`));});
listen('export-sheet','click',()=>{const c=document.createElement('canvas');const cols=Math.min(project.frames.length,Math.floor(4096/project.width));c.width=project.width*cols;c.height=project.height*Math.ceil(project.frames.length/cols);const g=c.getContext('2d');project.frames.forEach((f,i)=>{imageFrame(scratch,f);g.drawImage(scratch,(i%cols)*project.width,Math.floor(i/cols)*project.height);});png(c,filename(`-sheet-${cols}cols.png`));});
listen('export-gif','click',()=>download(new Blob([gifBytes(project)],{type:'image/gif'}),filename('.gif')));
listen('export-data','click',()=>download(new Blob([describe(project)],{type:'application/json'}),filename('.pixels.json')));
listen('copy','click',async()=>{const text=describe(project);try{await navigator.clipboard.writeText(text);status('Copied exact colors, every pixel, frame timing, and art notes for ChatGPT.');}catch{$('copy-text').value=text;$('copy-dialog').showModal();$('copy-text').select();}});
listen('close-copy','click',()=>$('copy-dialog').close());listen('help','click',()=>$('help-dialog').showModal());listen('close-help','click',()=>$('help-dialog').close());
listen('open-project','click',()=>$('project-file').click());listen('project-file','change',async e=>{const file=e.target.files[0];e.target.value='';if(!file)return;if(file.size>25_000_000)throw Error('Project file exceeds 25 MB.');const p=validateProject(JSON.parse(await file.text()),allowed);p.bank=banks[0].id;commit(()=>{project=p;frame=0;});reference.clear();fit();status('Project opened. Undo restores the previous workspace.');});
async function readImage(file){if(file.size>20_000_000)throw Error('Choose an image under 20 MB.');const url=URL.createObjectURL(file);try{const img=new Image();img.src=url;await img.decode();if(img.naturalWidth*img.naturalHeight>16_000_000)throw Error('Reference images must contain fewer than 16 million pixels.');return img;}finally{URL.revokeObjectURL(url);}}
listen('import-png','click',()=>$('art-file').click());listen('art-file','change',async e=>{const file=e.target.files[0];e.target.value='';if(!file)return;const img=await readImage(file),w=project.width,h=project.height;if(img.width%w||img.height%h)throw Error(`Image must be ${w} × ${h}, or a sheet of whole ${w} × ${h} frames. Use Reference overlay for other sizes.`);const count=img.width/w*(img.height/h);if(count>64||count*w*h>MAX_PIXELS)throw Error('Sheet exceeds the frame or pixel limit.');const temp=document.createElement('canvas');temp.width=img.width;temp.height=img.height;const g=temp.getContext('2d');g.drawImage(img,0,0);const rgba=g.getImageData(0,0,img.width,img.height).data,colors=[null,...bank().colors];const newFrames=[];for(let fy=0;fy<img.height;fy+=h)for(let fx=0;fx<img.width;fx+=w){const pixels=[];for(let y=0;y<h;y++)for(let x=0;x<w;x++){const i=((fy+y)*img.width+fx+x)*4;pixels.push(rgba[i+3]<128?0:nearest(rgba[i],rgba[i+1],rgba[i+2],colors));}newFrames.push({name:`Imported ${newFrames.length+1}`,ticks:8,pixels});}commit(()=>{project.palette=colors;project.frames=newFrames;frame=0;color=1;});status(`Imported ${count} frame(s), snapped to ${bank().label}. Undo restores prior artwork.`);});
const reference = createReferenceEditor({
  canvas, stage: $('stage'),
  getSize: () => ({width: project.width, height: project.height}),
  getZoom: () => zoom,
  onChange: requestRender,
  onMessage: status,
  onStart: () => { endStroke(); stop(); workspace.revealCanvas(); },
  readImage,
});
let layoutFrame;
const workspace=createWorkspace({
 onResize:()=>{cancelAnimationFrame(layoutFrame);layoutFrame=requestAnimationFrame(()=>{if(!project)return;if(autoFit)fit();else setZoom(zoom);});},
 onAnimationCollapse:()=>{if(playing)stop();}
});
window.addEventListener('keydown',e=>{if(e.target.matches('input,select,textarea')||document.querySelector('dialog[open]'))return;const key=e.key.toLowerCase();if(e.metaKey||e.ctrlKey){if(key==='z'){e.preventDefault();$(e.shiftKey?'redo':'undo').click();}if(key==='y'){e.preventDefault();$('redo').click();}if(key==='s'){e.preventDefault();$('save-project').click();}return;}if(stroke)return;const tools={b:'pencil',e:'eraser',f:'fill',i:'picker',l:'line',r:'rectangle',h:'pan'};if(tools[key])selectTool(tools[key]);if(key===' '){e.preventDefault();space=true;}if(key==='+'||key==='='){e.preventDefault();setZoom(zoom+1,pointerAnchor);}if(key==='-'){e.preventDefault();setZoom(zoom-1,pointerAnchor);}});window.addEventListener('keyup',e=>{if(e.key===' ')space=false;});
async function init(){const response=await fetch('./palettes.json');if(!response.ok)throw Error('Palette files could not load. Reload the editor.');const data=await response.json();banks=data.banks.filter(b=>!b.legacy);allowed=new Set(data.banks.flatMap(b=>b.colors));project=makeProject(banks[0].colors);for(const p of PRESETS){const o=new Option(`${p[1]} — ${p[2]} × ${p[3]}`,p[0]);$('preset').add(o);}for(const b of banks)$('bank').add(new Option(b.label,b.id));try{const saved=localStorage.getItem(STORAGE);if(saved){project=validateProject(JSON.parse(saved),allowed);status('Restored your last local workspace.');$('save-state').textContent='Restored from this browser';}}catch{status('Could not restore local draft. Open a downloaded project or start drawing.',true);}
 if(!banks.some(b=>b.id===project.bank))project.bank=banks[0].id;renderAll();fit();document.documentElement.dataset.editorReady='true';}
init().catch(e=>{status(e.message,true);document.querySelectorAll('button,input,select').forEach(b=>b.disabled=true);});
// Read-only QA snapshot. Contains artwork, never browser storage or reference images.
export function getSnapshot(){return{project:structuredClone(project),frame,zoom,tool,color,playing,playFrame,hasReference:reference.hasImage(),reference:reference.snapshot(),history:history.length,layout:workspace.snapshot()};}
