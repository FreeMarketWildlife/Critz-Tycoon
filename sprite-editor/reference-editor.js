import {fitReference, resizeReference, sampleReference} from './reference-pixels.js';

// This controller owns only the ephemeral guide. The indexed artwork model is
// deliberately absent from its API, including during drag/crop/key operations.
export function createReferenceEditor({canvas, stage, getSize, getZoom, onChange, onMessage, onStart, readImage}) {
  const $ = id => document.getElementById(id);
  let reference = null, editing = false, drag = null, cropDrag = null, loadVersion = 0;
  const sampled = document.createElement('canvas');
  const box = document.createElement('div');
  box.className = 'reference-box'; box.hidden = true;
  for (const [handle, x, y] of [['nw',0,0],['n',50,0],['ne',100,0],['e',100,50],['se',100,100],['s',50,100],['sw',0,100],['w',0,50]]) {
    const b = document.createElement('button');
    b.className = 'reference-handle'; b.dataset.handle = handle;
    b.type = 'button'; b.style.left = x + '%'; b.style.top = y + '%';
    b.setAttribute('aria-label', `Resize reference ${handle.toUpperCase()}`);
    box.append(b);
  }
  stage.append(box);
  const on = (id, event, fn) => $(id).addEventListener(event, async e => {
    try { await fn(e); } catch (error) { onMessage(error.message, true); }
  });
  const free = () => $('ref-scale').value === 'free';
  const number = (id, min, max) => Math.max(min, Math.min(max, Math.round(Number($(id).value) || 0)));
  function crop() {
    const x = number('crop-x', 0, reference.image.width - 1);
    const y = number('crop-y', 0, reference.image.height - 1);
    return {x, y, w: number('crop-w',1,reference.image.width-x), h: number('crop-h',1,reference.image.height-y)};
  }
  function rect() {
    const c = crop(), scale = Number($('ref-scale').value);
    return {x: number('ref-x',-4096,4096), y: number('ref-y',-4096,4096),
      w: free() ? number('ref-width',1,2048) : c.w*scale,
      h: free() ? number('ref-height',1,2048) : c.h*scale};
  }
  function setRect(r) {
    $('ref-x').value = Math.max(-4096, Math.min(4096, Math.round(r.x)));
    $('ref-y').value = Math.max(-4096, Math.min(4096, Math.round(r.y)));
    $('ref-width').value = Math.max(1, Math.min(2048, Math.round(r.w)));
    $('ref-height').value = Math.max(1, Math.min(2048, Math.round(r.h)));
  }
  function fit() {
    if (!reference) return;
    const c = crop(), {width, height} = getSize();
    $('ref-scale').value = 'free';
    setRect(fitReference(c.w,c.h,width,height));
    update();
  }
  function finish() {
    editing = false; drag = null;
    stage.classList.remove('reference-editing');
    $('ref-transform').textContent = 'Move / resize';
    $('ref-transform').setAttribute('aria-pressed','false');
    box.hidden = true;
    if (reference) update(); else onChange();
  }
  function start() {
    if (!reference) return;
    if (!free()) fit();
    onStart(); editing = true;
    $('show-reference').checked = true;
    stage.classList.add('reference-editing');
    $('ref-transform').textContent = 'Done positioning';
    $('ref-transform').setAttribute('aria-pressed','true');
    update();
    canvas.scrollIntoView({block:'nearest',inline:'nearest'});
    onMessage('Drag the reference to move it. Drag handles to resize. Click Done positioning to draw.');
  }
  function update() {
    if (!reference) return;
    $('ref-free-controls').hidden = !free();
    $('opacity-value').textContent = $('opacity').value + '%';
    const c = crop(), r = rect();
    $('ref-hint').textContent = free()
      ? `${c.w} × ${c.h} source → ${r.w} × ${r.h} canvas pixels. ${editing ? 'Drag to move; handles resize. Done positioning returns to drawing.' : 'Click Move / resize to adjust on the canvas.'}`
      : `${c.w} × ${c.h} source → ${r.w} × ${r.h} canvas pixels. Choose Free or Fit inside canvas to shrink a large reference.`;
    onChange();
  }
  function draw(ctx) {
    if (!reference || !$('show-reference').checked) return;
    const c = crop(), r = rect();
    ctx.save(); ctx.globalAlpha = Number($('opacity').value)/100;
    ctx.imageSmoothingEnabled = false;
    if (!free()) {
      ctx.drawImage($('remove-bg').checked ? reference.keyed : reference.image,c.x,c.y,c.w,c.h,r.x,r.y,r.w,r.h);
    } else {
      // Fast nearest preview while dragging; settle to exact area averaging on
      // release. Moving reuses the same cached sampled image.
      const method = drag?.handle && drag.handle !== 'move' ? 'nearest' : $('ref-sampling').value;
      const key = [c.x,c.y,c.w,c.h,r.w,r.h,method,$('remove-bg').checked].join(':');
      if (key !== reference.cacheKey) {
        const data = sampleReference(reference.rgba,reference.image.width,c,r.w,r.h,method,$('remove-bg').checked ? reference.rgba.subarray(0,3) : null);
        sampled.width = r.w; sampled.height = r.h;
        sampled.getContext('2d').putImageData(new ImageData(data,r.w,r.h),0,0);
        reference.cacheKey = key;
      }
      ctx.drawImage(sampled,r.x,r.y);
    }
    ctx.restore();
  }
  function renderHandles() {
    box.hidden = !(reference && editing && free() && $('show-reference').checked);
    if (box.hidden) return;
    const r = rect(), z = getZoom();
    Object.assign(box.style,{left:r.x*z+'px',top:r.y*z+'px',width:r.w*z+'px',height:r.h*z+'px'});
  }
  function drawSource() {
    if (!reference) return;
    const c = $('reference-source'), image = reference.image;
    // Keep the thumbnail bounded independently of a huge source image.
    const scale = Math.min(1,512/image.width,768/image.height);
    c.width = Math.max(1,Math.round(image.width*scale)); c.height = Math.max(1,Math.round(image.height*scale));
    const g = c.getContext('2d'), r = crop(); g.imageSmoothingEnabled = false;
    g.drawImage(image,0,0,c.width,c.height); g.fillStyle = '#0008'; g.fillRect(0,0,c.width,c.height);
    const sx=c.width/image.width,sy=c.height/image.height;
    g.drawImage(image,r.x,r.y,r.w,r.h,r.x*sx,r.y*sy,r.w*sx,r.h*sy);
    g.strokeStyle='#ddff9a';g.lineWidth=1;g.strokeRect(r.x*sx+.5,r.y*sy+.5,r.w*sx,r.h*sy);
  }
  function clear() {
    loadVersion++; reference=null; finish();
    sampled.width=1;sampled.height=1;$('reference-source').width=1;$('reference-source').height=1;
    $('reference-controls').hidden=true;
  }
  on('load-reference','click',()=>$('reference-file').click());
  on('reference-file','change',async e=>{
    const file=e.target.files[0];e.target.value='';if(!file)return;
    const version=++loadVersion,image=await readImage(file);if(version!==loadVersion)return;
    const keyed=document.createElement('canvas');keyed.width=image.width;keyed.height=image.height;
    const g=keyed.getContext('2d');g.drawImage(image,0,0);
    const im=g.getImageData(0,0,image.width,image.height),rgba=new Uint8ClampedArray(im.data),bg=rgba.subarray(0,3);
    for(let i=0;i<im.data.length;i+=4)if(im.data[i]===bg[0]&&im.data[i+1]===bg[1]&&im.data[i+2]===bg[2])im.data[i+3]=0;
    g.putImageData(im,0,0);finish();reference={image,keyed,rgba,cacheKey:null};
    $('crop-x').value=0;$('crop-y').value=0;$('crop-w').value=image.width;$('crop-h').value=image.height;
    $('ref-x').value=0;$('ref-y').value=0;$('ref-lock').checked=true;$('ref-layer').value='above';
    $('reference-controls').hidden=false;$('show-reference').checked=true;
    const size=getSize();
    if(image.width*2>size.width||image.height*2>size.height)fit();
    else {$('ref-scale').value='2';update();}
    drawSource();onMessage('Reference added above your artwork. Free fits large images; Move / resize positions them.');
  });
  on('ref-scale','change',()=>{if(!reference)return;finish();if(free())fit();else update();});
  on('ref-fit','click',()=>{fit();onMessage('Reference crop fitted and centered inside the canvas.');});
  on('ref-transform','click',()=>editing?finish():start());
  on('remove-reference','click',clear);
  for(const id of ['ref-x','ref-y','ref-layer','opacity','remove-bg','show-reference','ref-sampling'])on(id,'input',update);
  for(const id of ['crop-x','crop-y','crop-w','crop-h'])on(id,'change',()=>{if(!reference)return;const c=crop();$('crop-x').value=c.x;$('crop-y').value=c.y;$('crop-w').value=c.w;$('crop-h').value=c.h;if(free())fit();else update();drawSource();});
  for(const [id,axis] of [['ref-width','w'],['ref-height','h']])on(id,'change',()=>{
    if(!reference)return;
    const r=rect(),before=reference.lastRect||r,value=number(id,1,2048);
    const next=$('ref-lock').checked ? resizeReference(before,axis==='w'?'e':'s',axis==='w'?value-before.w:0,axis==='h'?value-before.h:0,true) : r;
    setRect(next);reference.lastRect=rect();update();
  });
  for(const id of ['ref-width','ref-height'])on(id,'focus',()=>{if(reference)reference.lastRect=rect();});

  stage.addEventListener('pointerdown',e=>{
    if(!editing||!reference||!free()||!$('show-reference').checked||e.button!==0)return;
    e.preventDefault();e.stopPropagation();
    const handle=e.target.closest('[data-handle]')?.dataset.handle||'move';
    drag={pointer:e.pointerId,handle,x:e.clientX,y:e.clientY,box:rect(),zoom:getZoom(),locked:$('ref-lock').checked};
    stage.setPointerCapture(e.pointerId);
  },true);
  stage.addEventListener('pointermove',e=>{
    if(!drag||drag.pointer!==e.pointerId)return;e.preventDefault();e.stopPropagation();
    const dx=Math.round((e.clientX-drag.x)/drag.zoom),dy=Math.round((e.clientY-drag.y)/drag.zoom);
    setRect(drag.handle==='move'?{...drag.box,x:drag.box.x+dx,y:drag.box.y+dy}:resizeReference(drag.box,drag.handle,dx,dy,drag.locked));
    update();
  },true);
  function endDrag(e){if(!drag||drag.pointer!==e.pointerId)return;e.stopPropagation();drag=null;update();}
  stage.addEventListener('pointerup',endDrag,true);stage.addEventListener('pointercancel',endDrag,true);stage.addEventListener('lostpointercapture',endDrag,true);
  // Accessible handle resizing: arrow keys adjust the corresponding handle by
  // one pixel; Shift changes ten. Escape always returns to drawing.
  stage.addEventListener('keydown',e=>{
    if(!editing)return;
    if(e.key==='Escape'){e.preventDefault();e.stopPropagation();finish();return;}
    const handle=e.target.dataset.handle,delta={ArrowLeft:[-1,0],ArrowRight:[1,0],ArrowUp:[0,-1],ArrowDown:[0,1]}[e.key];
    if(!handle||!delta)return;e.preventDefault();e.stopPropagation();const amount=e.shiftKey?10:1;
    setRect(resizeReference(rect(),handle,delta[0]*amount,delta[1]*amount,$('ref-lock').checked));update();
  });
  document.addEventListener('keydown',e=>{if(editing&&e.key==='Escape')finish();});
  window.addEventListener('blur',()=>{drag=null;cropDrag=null;onChange();});
  const source=$('reference-source');
  function sourcePos(e){const r=source.getBoundingClientRect();return [Math.max(0,Math.min(reference.image.width-1,Math.floor((e.clientX-r.left)*reference.image.width/r.width))),Math.max(0,Math.min(reference.image.height-1,Math.floor((e.clientY-r.top)*reference.image.height/r.height)))];}
  source.addEventListener('pointerdown',e=>{if(!reference||e.button!==0)return;e.preventDefault();source.setPointerCapture(e.pointerId);cropDrag={point:sourcePos(e),pointer:e.pointerId};});
  source.addEventListener('pointermove',e=>{
    if(!cropDrag||cropDrag.pointer!==e.pointerId)return;const [x,y]=sourcePos(e),[sx,sy]=cropDrag.point;
    $('crop-x').value=Math.min(x,sx);$('crop-y').value=Math.min(y,sy);$('crop-w').value=Math.abs(x-sx)+1;$('crop-h').value=Math.abs(y-sy)+1;drawSource();
  });
  function endCrop(e){if(!cropDrag||cropDrag.pointer!==e.pointerId)return;cropDrag=null;if(free())fit();else update();drawSource();}
  source.addEventListener('pointerup',endCrop);source.addEventListener('pointercancel',endCrop);source.addEventListener('lostpointercapture',endCrop);
  return {draw,renderHandles,finish,clear,hasImage:()=>!!reference,snapshot:()=>reference?{mode:$('ref-scale').value,crop:crop(),rect:rect(),editing,sampling:$('ref-sampling').value,locked:$('ref-lock').checked}:null};
}
