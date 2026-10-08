// Original Critz lighting follows the existing saved simulation clock.
// Emerald's door animation is a reference; its lighting is not being reproduced.
export const OPEN_ENTRANCES=new Set(['glass','waterworks']);
export function daylight(state){const hour=state.stage==='night'?22:((state.time%24)+24)%24;return {hour,strength:hour<6||hour>=20?0:hour<8?(hour-6)/2:hour<=17?1:(20-hour)/3};}
export function doorPresentation(scene,state){const open=OPEN_ENTRANCES.has(scene);return {open,mat:!open,beam:open?daylight(state).strength:0};}
export function drawThreshold(c,e,scene,state){const {open,beam}=doorPresentation(scene,state),x=e.x*32+16,y=e.y*32+16;
 if(open){c.fillStyle='#45606a';c.fillRect(x-18,y-4,36,14);c.fillStyle='#c7c4a0';c.fillRect(x-16,y-2,32,8);
  if(beam){c.save();c.globalAlpha=.23*beam;c.fillStyle='#fff4bd';for(let d=0;d<64;d+=2){const spread=Math.floor(d/8);c.fillRect(x-14-spread,y-d,28+spread*2,2);}c.restore();c.fillStyle=beam>.5?'#f6e4a4':'#b5bdad';c.fillRect(x-15,y,30,4);}
 }else{c.fillStyle='#344b50';c.fillRect(x-20,y-6,40,16);c.fillStyle='#b99b66';c.fillRect(x-18,y-4,36,12);c.fillStyle='#647e70';c.fillRect(x-15,y-2,30,8);c.fillStyle='#d1be8a';for(let i=-12;i<=12;i+=6)c.fillRect(x+i,y,2,4);}
}
export function applyLighting(c,state,inside=false){const d=daylight(state),night=1-d.strength;c.save();c.fillStyle=inside?`rgba(26,35,66,${night*.16})`:`rgba(19,30,65,${night*.48})`;c.fillRect(0,0,480,320);if(d.hour>=17&&d.hour<20){c.fillStyle='rgba(222,134,70,.10)';c.fillRect(0,0,480,320);}c.restore();return d;}

// Exterior thresholds also belong to the pavement: crossing sideways must not
// pull the player into a building. Interior exits are approached southwards.
export function approachesDoor(outside,destinationOutside,door,facing){
 if(door.entryFacing)return facing===door.entryFacing;
 if(outside&&destinationOutside&&door.id!=='yard')return true;
 if(outside)return facing==='up';
 return facing===(door.id==='stairs'&&door.y<6?'up':'down');
}
