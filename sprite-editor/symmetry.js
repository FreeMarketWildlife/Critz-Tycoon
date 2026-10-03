import {fitReference} from './reference-pixels.js';

// Preserve exact RGBA values and column order. No averaging, palette changes,
// mirrored recoloring, or inference about anatomy is involved in this operation.
export function evenReference(pixels,width,height,method='duplicate') {
  if(!Number.isInteger(width)||!Number.isInteger(height)||width<1||height<1||width>480||height>480||pixels.length!==width*height*4)throw Error('Use a reference grid from 1 to 480 pixels per axis.');
  if(!['duplicate','remove'].includes(method))throw Error('Unknown center treatment.');
  if(width%2===0)return {pixels:new Uint8ClampedArray(pixels),width,height,changed:false,center:null};
  if(width===1&&method==='remove')throw Error('A one-column image cannot lose its only column. Duplicate it instead.');
  const center=Math.floor(width/2),nextWidth=width+(method==='duplicate'?1:-1);
  const result=new Uint8ClampedArray(nextWidth*height*4);
  for(let y=0;y<height;y++)for(let x=0;x<nextWidth;x++){
    const sx=method==='duplicate'?(x<=center?x:x-1):(x<center?x:x+1);
    const source=(y*width+sx)*4;
    result.set(pixels.subarray(source,source+4),(y*nextWidth+x)*4);
  }
  return {pixels:result,width:nextWidth,height,changed:true,center};
}

export function centeredEvenOverlay(width,height,canvasWidth,canvasHeight) {
  if(canvasWidth%2||canvasWidth<2)throw Error('Choose an even-width canvas to center this reference between two pixel columns.');
  if(width%2)throw Error('The corrected reference must have an even width.');
  if(width<=canvasWidth&&height<=canvasHeight)return {x:(canvasWidth-width)/2,y:Math.round((canvasHeight-height)/2),w:width,h:height,resampled:false};
  const r=fitReference(width,height,canvasWidth,canvasHeight);
  // An even display width is needed too: integer movement cannot center an odd
  // display width on the boundary axis of an even canvas.
  r.w=Math.max(2,Math.min(canvasWidth,2*Math.round(r.w/2)));
  r.x=(canvasWidth-r.w)/2;r.resampled=true;
  return r;
}
