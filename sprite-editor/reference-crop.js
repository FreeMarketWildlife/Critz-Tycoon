// A non-destructive source-image crop. Selection never reaches the art model.
export function createReferenceCrop({getReference,applyCrop,onMessage}) {
  const $=id=>document.getElementById(id),dialog=$('reference-crop-dialog'),canvas=$('crop-preview'),g=canvas.getContext('2d');
  let source=null,selection=null,drag=null;
  const fields=['x','y','w','h'];
  function render(){
    if(!source)return;
    const {image}=source,sx=canvas.width/image.width,sy=canvas.height/image.height;
    g.clearRect(0,0,canvas.width,canvas.height);g.imageSmoothingEnabled=false;
    g.drawImage(image,0,0,canvas.width,canvas.height);g.fillStyle='#06110caa';g.fillRect(0,0,canvas.width,canvas.height);
    if(selection){const {x,y,w,h}=selection;g.clearRect(x*sx,y*sy,w*sx,h*sy);g.drawImage(image,x,y,w,h,x*sx,y*sy,w*sx,h*sy);g.strokeStyle='#d8ff91';g.lineWidth=2;g.strokeRect(x*sx+1,y*sy+1,Math.max(1,w*sx-2),Math.max(1,h*sy-2));}
  }
  function read(){
    if(!source)return;
    const values=fields.map(k=>Number($('ref-crop-'+k).value));const [x,y,w,h]=values;
    const valid=values.every(Number.isInteger)&&x>=0&&y>=0&&w>=1&&h>=1&&x+w<=source.image.width&&y+h<=source.image.height;
    selection=valid?{x,y,w,h}:null;$('apply-reference-crop').disabled=!valid;
    $('ref-crop-message').textContent=valid?`Selected ${w} × ${h} source pixels at (${x}, ${y}). Apply fits this crop into your canvas.`:'Enter a whole-pixel rectangle inside the source image.';
    render();
  }
  function set(r){for(const k of fields)$('ref-crop-'+k).value=r[k];read();}
  function point(e){const r=canvas.getBoundingClientRect();return{x:Math.max(0,Math.min(source.image.width-1,Math.floor((e.clientX-r.left)*source.image.width/r.width))),y:Math.max(0,Math.min(source.image.height-1,Math.floor((e.clientY-r.top)*source.image.height/r.height)))};}
  $('ref-crop-open').onclick=()=>{
    source=getReference();if(!source){onMessage('Add a reference image first.',true);return;}
    drag=null;const {image}=source,scale=Math.min(1,900/image.width,650/image.height);canvas.width=Math.max(1,Math.round(image.width*scale));canvas.height=Math.max(1,Math.round(image.height*scale));
    $('ref-crop-source-size').textContent=`Source image: ${image.width} × ${image.height} px. Drag a rectangle or enter exact source coordinates (top-left origin).`;
    set(source.crop);dialog.showModal();
  };
  for(const k of fields)$('ref-crop-'+k).addEventListener('input',read);
  $('ref-crop-reset').onclick=()=>set({x:0,y:0,w:source.image.width,h:source.image.height});
  for(const id of ['reference-crop-close','cancel-reference-crop'])$(id).onclick=()=>dialog.close();
  canvas.addEventListener('pointerdown',e=>{if(e.button!==0||!source)return;e.preventDefault();drag={...point(e),pointer:e.pointerId};canvas.setPointerCapture(e.pointerId);set({x:drag.x,y:drag.y,w:1,h:1});});
  canvas.addEventListener('pointermove',e=>{if(!drag||drag.pointer!==e.pointerId)return;const p=point(e);set({x:Math.min(p.x,drag.x),y:Math.min(p.y,drag.y),w:Math.abs(p.x-drag.x)+1,h:Math.abs(p.y-drag.y)+1});});
  for(const event of ['pointerup','pointercancel','lostpointercapture'])canvas.addEventListener(event,()=>{drag=null;});
  $('apply-reference-crop').onclick=()=>{read();if(!selection)return;try{applyCrop({...selection});dialog.close();}catch(e){$('ref-crop-message').textContent=e.message;}};
  dialog.addEventListener('close',()=>{source=null;selection=null;drag=null;canvas.width=1;canvas.height=1;});
}
