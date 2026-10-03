import {sampleReference} from './reference-pixels.js';
import {evenReference,centeredEvenOverlay} from './symmetry.js';

export function createSymmetryWorkshop({getReference,getCanvasSize,applyReference,onMessage}) {
  const $=id=>document.getElementById(id),dialog=$('symmetry-dialog');
  let source=null,prepared=null,base=null,lastInput='',timer;
  function paint(id,pixels,width,height,after=false,center=null){
    const canvas=$(id),g=canvas.getContext('2d');
    const pane=canvas.parentElement;
    const availableWidth=Math.max(24,pane.clientWidth-58),availableHeight=Math.max(24,pane.clientHeight-58);
    const z=Math.max(1,Math.min(10,Math.floor(Math.min(availableWidth/width,availableHeight/height))));
    canvas.width=width*z+24;canvas.height=height*z+24;g.clearRect(0,0,canvas.width,canvas.height);
    for(let y=0;y<height;y++)for(let x=0;x<width;x++){g.fillStyle=(x+y)%2?'#d1d8c9':'#b9c4b0';g.fillRect(12+x*z,12+y*z,z,z);}
    const native=document.createElement('canvas');native.width=width;native.height=height;
    native.getContext('2d').putImageData(new ImageData(new Uint8ClampedArray(pixels),width,height),0,0);
    g.imageSmoothingEnabled=false;g.drawImage(native,12,12,width*z,height*z);
    if(z>=4){g.strokeStyle='#10281935';g.lineWidth=1;g.beginPath();for(let x=0;x<=width;x++){g.moveTo(12+x*z+.5,12);g.lineTo(12+x*z+.5,12+height*z);}for(let y=0;y<=height;y++){g.moveTo(12,12+y*z+.5);g.lineTo(12+width*z,12+y*z+.5);}g.stroke();}
    if(center!==null&&!after){g.fillStyle='#ffd57f55';g.fillRect(12+center*z,12,z,height*z);}
    g.strokeStyle=after?'#d8ff91':'#ffbe75';g.lineWidth=1;g.setLineDash(after?[]:[3,3]);g.beginPath();g.moveTo(12+width*z/2+.5,5);g.lineTo(12+width*z/2+.5,19+height*z);g.stroke();g.setLineDash([]);
  }
  function update(){
    prepared=null;$('symmetry-apply').disabled=true;
    try{
      const width=Number($('symmetry-width').value),height=Number($('symmetry-height').value);
      if(!Number.isInteger(width)||!Number.isInteger(height)||width<1||width>480||height<1||height>480)throw Error('Enter whole pixel dimensions from 1 to 480.');
      const key=width+':'+height;
      if(key!==lastInput){base=sampleReference(source.rgba,source.width,source.crop,width,height,'nearest',source.background);lastInput=key;}
      const next=evenReference(base,width,height,$('symmetry-method').value);
      paint('symmetry-before',base,width,height,false,width%2?Math.floor(width/2):null);paint('symmetry-after',next.pixels,next.width,next.height,true);
      $('symmetry-before-label').textContent=`Before · ${width} × ${height} · axis x=${width/2}`;
      $('symmetry-after-label').textContent=`After · ${next.width} × ${height} · axis x=${next.width/2}`;
      const size=getCanvasSize(),placement=centeredEvenOverlay(next.width,height,size.width,size.height);
      prepared={...next,placement};
      let description=next.changed?`${width} → ${next.width}: ${$('symmetry-method').value==='duplicate'?'the center column becomes two identical columns':'the center column is removed'}. All other pixels stay exact.`:'This grid is already even. Its centerline already falls between columns.';
      description+=` Overlay center: x=${size.width/2}.`;
      if(placement.resampled)description+=` The ${next.width} × ${height} reference is larger than this canvas, so its overlay is shown at ${placement.w} × ${placement.h} with nearest pixels. For an enlarged screenshot, set its true native grid first.`;
      $('symmetry-explanation').textContent=description;
      $('symmetry-apply').textContent=next.changed?'Use corrected reference':'Center this reference';$('symmetry-apply').disabled=false;
    }catch(e){$('symmetry-explanation').textContent=e.message;}
  }
  function setSize(width,height){$('symmetry-width').value=width;$('symmetry-height').value=height;update();}
  $('symmetry-open').onclick=()=>{
    source=getReference();if(!source){onMessage('Add a reference image first.',true);return;}
    lastInput='';base=null;prepared=null;
    $('symmetry-method').value='duplicate';
    $('symmetry-source-info').textContent=`Selected source crop: ${source.crop.w} × ${source.crop.h}. Shown overlay: ${source.rect.w} × ${source.rect.h}. Choose the pixel grid you want to correct.`;
    dialog.showModal();
    const native=source.crop.w<=480&&source.crop.h<=480;
    setSize(native?source.crop.w:Math.min(480,source.rect.w),native?source.crop.h:Math.min(480,source.rect.h));
  };
  for(const id of ['symmetry-width','symmetry-height'])$(id).addEventListener('input',()=>{prepared=null;$('symmetry-apply').disabled=true;clearTimeout(timer);timer=setTimeout(update,100);});
  $('symmetry-method').onchange=update;
  $('symmetry-source-size').onclick=()=>{if(source.crop.w>480||source.crop.h>480){onMessage('Source exceeds the 480px workshop grid. Enter its native pixel dimensions or use shown size.',true);$('symmetry-explanation').textContent='This source is too large to treat each screenshot pixel as a sprite pixel. Enter its true native grid, or use shown size.';return;}setSize(source.crop.w,source.crop.h);};
  $('symmetry-shown-size').onclick=()=>setSize(Math.min(480,source.rect.w),Math.min(480,source.rect.h));
  for(const id of ['symmetry-close','symmetry-cancel'])$(id).onclick=()=>dialog.close();
  window.addEventListener('resize',()=>{if(dialog.open&&source)update();});
  dialog.addEventListener('close',()=>{clearTimeout(timer);source=null;base=null;prepared=null;});
  $('symmetry-apply').onclick=()=>{if(!prepared)return;try{applyReference(prepared);dialog.close();onMessage('Even-width reference centered. Your artwork is unchanged; Restore original reference reverses this.');}catch(e){$('symmetry-explanation').textContent=e.message;}};
}
