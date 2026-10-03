// Edit exactly one native column. Both odd and even grids receive the requested
// operation; no parity-based no-op and no recoloring or mirrored inference.
export function treatCenterColumn(pixels,width,height,method='add-left') {
  if(!Number.isInteger(width)||!Number.isInteger(height)||width<1||height<1||width>480||height>480||pixels.length!==width*height*4)throw Error('Use a reference grid from 1 to 480 pixels per axis.');
  if(!['remove-left','remove-right','add-left','add-right'].includes(method))throw Error('Unknown center treatment.');
  const adding=method.startsWith('add'),left=method.endsWith('left');
  if(!adding&&width===1)throw Error('A one-column image cannot lose its only column. Add a column instead.');
  if(adding&&width===480)throw Error('Adding a column would exceed the 480px working grid. Reduce the grid width first.');
  // With an odd grid, leave the unique middle column in place and choose its
  // immediate neighbor. With an even grid, choose the left/right central pair.
  const column=width===1?0:left?Math.floor(width/2)-1:Math.ceil(width/2);
  const insertion=column+(left?1:0),nextWidth=width+(adding?1:-1);
  const result=new Uint8ClampedArray(nextWidth*height*4);
  for(let y=0;y<height;y++)for(let x=0;x<nextWidth;x++){
    const sx=adding?(x<insertion?x:x===insertion?column:x-1):(x<column?x:x+1);
    const source=(y*width+sx)*4;
    result.set(pixels.subarray(source,source+4),(y*nextWidth+x)*4);
  }
  return {pixels:result,width:nextWidth,height,column,method};
}

// Keep every corrected pixel. Refitting here can erase a one-column edit when
// reducing a large source to a sprite-sized overlay. Overflow is clipped by the
// drawing canvas, never silently resampled; the original remains restorable.
export function centeredReferenceOverlay(width,height,canvasWidth,canvasHeight) {
  const x=Math.round((canvasWidth-width)/2),y=Math.round((canvasHeight-height)/2);
  return {w:width,h:height,resampled:false,x,y,centerOffset:x+width/2-canvasWidth/2};
}
