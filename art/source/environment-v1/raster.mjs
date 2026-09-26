// Integer-pixel authoring only: no Canvas antialiasing or image dependencies.
import { deflateSync } from 'node:zlib';
import { writeFile } from 'node:fs/promises';
const crcTable = Array.from({length:256},(_,n)=>{for(let k=0;k<8;k++) n=n&1?0xedb88320^(n>>>1):n>>>1;return n>>>0;});
const crc = b => {let n=0xffffffff;for(const v of b)n=crcTable[(n^v)&255]^(n>>>8);return(n^0xffffffff)>>>0;};
const chunk = (t,b) => {const h=Buffer.alloc(8),end=Buffer.alloc(4);h.writeUInt32BE(b.length);h.write(t,4);end.writeUInt32BE(crc(Buffer.concat([Buffer.from(t),b])));return Buffer.concat([h,b,end]);};
export class Raster {
  constructor(w,h){this.w=w;this.h=h;this.p=Buffer.alloc(w*h*4);}
  dot(x,y,c){x=Math.floor(x);y=Math.floor(y);if(x<0||y<0||x>=this.w||y>=this.h)return;const i=(y*this.w+x)*4;const rgb=c==='transparent'?[0,0,0,0]:[parseInt(c.slice(1,3),16),parseInt(c.slice(3,5),16),parseInt(c.slice(5,7),16),255];this.p.set(rgb,i);}
  rect(x,y,w,h,c){for(let yy=y;yy<y+h;yy++)for(let xx=x;xx<x+w;xx++)this.dot(xx,yy,c);}
  line(x,y,x2,y2,c){const dx=Math.abs(x2-x),sx=x<x2?1:-1,dy=-Math.abs(y2-y),sy=y<y2?1:-1;let e=dx+dy;while(true){this.dot(x,y,c);if(x===x2&&y===y2)break;const v=2*e;if(v>=dy){e+=dy;x+=sx;}if(v<=dx){e+=dx;y+=sy;}}}
  poly(points,c){const minY=Math.floor(Math.min(...points.map(p=>p[1]))),maxY=Math.ceil(Math.max(...points.map(p=>p[1])));for(let y=minY;y<=maxY;y++){const xs=[];for(let i=0,j=points.length-1;i<points.length;j=i++){const a=points[i],b=points[j];if((a[1]>y)!==(b[1]>y))xs.push(a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]));}xs.sort((a,b)=>a-b);for(let i=0;i<xs.length;i+=2)for(let x=Math.ceil(xs[i]);x<xs[i+1];x++)this.dot(x,y,c);}}
  oval(x,y,w,h,c){for(let yy=y;yy<y+h;yy++)for(let xx=x;xx<x+w;xx++)if(((xx-x+.5)/w-.5)**2+((yy-y+.5)/h-.5)**2<=.25)this.dot(xx,yy,c);}
  blit(other,x,y){for(let j=0;j<other.h;j++)for(let i=0;i<other.w;i++){const d=((y+j)*this.w+x+i)*4,s=(j*other.w+i)*4;if(other.p[s+3]&&x+i>=0&&y+j>=0&&x+i<this.w&&y+j<this.h)this.p.set(other.p.subarray(s,s+4),d);}}
  crop(x,y,w,h){const r=new Raster(w,h);for(let j=0;j<h;j++)for(let i=0;i<w;i++){const s=((y+j)*this.w+x+i)*4;if(x+i>=0&&y+j>=0&&x+i<this.w&&y+j<this.h)r.p.set(this.p.subarray(s,s+4),(j*w+i)*4);}return r;}
  scale(n){const r=new Raster(this.w*n,this.h*n);for(let y=0;y<r.h;y++)for(let x=0;x<r.w;x++){const i=(Math.floor(y/n)*this.w+Math.floor(x/n))*4;r.p.set(this.p.subarray(i,i+4),(y*r.w+x)*4);}return r;}
  async save(path){const head=Buffer.alloc(13);head.writeUInt32BE(this.w,0);head.writeUInt32BE(this.h,4);head[8]=8;head[9]=6;const rows=Buffer.alloc((this.w*4+1)*this.h);for(let y=0;y<this.h;y++)this.p.copy(rows,y*(this.w*4+1)+1,y*this.w*4,(y+1)*this.w*4);await writeFile(path,Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk('IHDR',head),chunk('IDAT',deflateSync(rows)),chunk('IEND',Buffer.alloc(0))]));}
}
