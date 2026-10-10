import {TUBS} from './greenhouse-state.js';
// All cast shadows live in this disposable native-pixel mask, never in sprites.
export function paintShadowMask(c,{enabled,time=0,calm=false,inside=true,actors=[]}){
  c.clearRect(0,0,416,544);if(!enabled)return;
  c.fillStyle='#183b39';
  if(inside){
    c.save();c.beginPath();c.rect(32,96,352,424);c.clip();
    const drift=calm?0:Math.round(Math.sin(time*.23)*3);
    for(let y=96;y<520;y++)for(const x of [42,138,234,330])c.fillRect(x+Math.floor((y-96)/4)+drift,y,3,1);
    for(let row=0;row<5;row++){const y=106+row*83;for(let i=0;i<4;i++){const x=39+i*7+drift;c.fillRect(x,y+i*3,12-i,3);c.fillRect(416-x-12+i,y+i*3,12-i,3);}}
    for(const t of TUBS){c.fillRect(t.x*32+6,t.y*32+60,88,7);c.fillRect(t.x*32+92,t.y*32+10,6,50);}
    c.restore();
  }else c.fillRect(52,250,312,10);
  for(const a of actors)c.fillRect(Math.round((a.x+.5)*32)-10,Math.round((a.y+1)*32)-4,20,3);
}
export function sparkle(c,x,y,time,calm=false,scale=1){
  c.save();c.fillStyle='#fff2ba';const phase=calm?0:Math.floor(time*4)%4;
  for(let i=0;i<3;i++){const xx=Math.round(x+[-12,10,4][i]*scale),yy=Math.round(y+[-8,4,-13][i]*scale),r=(i+phase)%3===0?2:1;c.fillRect(xx-r,yy,r*2+1,1);c.fillRect(xx,yy-r,1,r*2+1);}c.restore();
}
// Temporary exuberant palettes keep outlines and face contrast readable.
export function shinySheet(source,variant){
  const canvas=document.createElement('canvas');canvas.width=source.width;canvas.height=source.height;const c=canvas.getContext('2d');c.drawImage(source,0,0);const data=c.getImageData(0,0,canvas.width,canvas.height);
  const palettes=[[[74,240,206],[199,88,255]],[[255,103,198],[80,219,255]],[[165,243,65],[255,138,44]],[[123,109,255],[255,191,74]],[[255,101,98],[120,247,182]],[[61,187,255],[246,111,243]],[[245,236,60],[159,91,255]],[[254,137,47],[83,224,215]],[[201,107,255],[166,246,81]],[[255,113,174],[252,221,62]],[[57,222,157],[108,137,255]],[[99,211,253],[255,156,84]]];
  const pair=palettes[variant%12];for(let i=0;i<data.data.length;i+=4){const d=data.data;if(!d[i+3])continue;const l=(d[i]+d[i+1]+d[i+2])/3;if(l<78||l>239)continue;const x=(i/4)%canvas.width,y=Math.floor(i/4/canvas.width),col=pair[(Math.floor(x/5)+Math.floor(y/6))%2],v=.48+l/360;for(let j=0;j<3;j++)d[i+j]=Math.min(255,Math.round(col[j]*v));}c.putImageData(data,0,0);return canvas;
}
