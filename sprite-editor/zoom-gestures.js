// Keep pixel-art zoom integral, but consume gesture distance rather than events.
const clamp=(v,min,max)=>Math.max(min,Math.min(max,v));
export function createWheelZoom(){
 let remainder=0,lastTime=-Infinity,direction=0;
 return{reset(){remainder=0;lastTime=-Infinity;direction=0;},
 next(event,current,now=performance.now(),min=1,max=24){
  const unit=event.deltaMode===1?16:event.deltaMode===2?800:1;
  const raw=event.deltaY*unit;if(!Number.isFinite(raw)||!raw)return current;
  const sign=Math.sign(raw);if(now-lastTime>1000||sign!==direction)remainder=0;
  lastTime=now;direction=sign;
  // Two ordinary notches, or equivalent accumulated fine movement, per level.
  // Even an extreme page-mode event contributes at most half a level.
  remainder+=clamp(raw,-60,60);
  const steps=Math.trunc(remainder/120);remainder-=steps*120;
  const next=clamp(current-steps,min,max);
  if(next===min&&sign>0||next===max&&sign<0)remainder=0;
  return next;
 }};
}
export function createPinchZoom(startZoom,min=1,max=24){
 let lastScale=1,intent=startZoom;
 return{next(scale,current){
  if(!Number.isFinite(scale)||scale<=0)return current;
  // Half the logarithmic sensitivity: doubling finger distance grows zoom by √2.
  const desired=intent*Math.sqrt(scale/lastScale);lastScale=scale;
  intent=clamp(clamp(desired,intent-.75,intent+.75),min,max);
  const step=intent>=current+.65?1:intent<=current-.65?-1:0;
  return clamp(current+step,min,max);
 }};
}
