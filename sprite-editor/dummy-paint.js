// Flood membership is frozen before painting so mirrored writes cannot change it.
export function connectedLabelPixels(labels,x,y,width=32,height=64){
  if(!Number.isInteger(x)||!Number.isInteger(y)||x<0||y<0||x>=width||y>=height)return [];
  const target=labels[y*width+x],seen=new Uint8Array(width*height),queue=[y*width+x],result=[];seen[queue[0]]=1;
  for(let n=0;n<queue.length;n++){
    const i=queue[n],px=i%width,py=Math.floor(i/width);result.push([px,py]);
    for(const j of [px>0?i-1:-1,px<width-1?i+1:-1,py>0?i-width:-1,py<height-1?i+width:-1])if(j>=0&&!seen[j]&&labels[j]===target){seen[j]=1;queue.push(j);}
  }
  return result;
}
