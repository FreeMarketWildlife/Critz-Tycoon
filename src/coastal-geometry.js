import {CONTACT_RULE,contactTerrainSpan} from './contact-rules.js';
// Raised shore art shares B contact registration; depth contours remain water.
export {CONTACT_RULE};
export function coastalWaterPixel(x,y,m){const s=contactTerrainSpan(m);if(x<s.left||x>=s.right||y<16||y>=48)return false;const corners=[[s.left,16,!(m&8)&&!(m&1),1,1],[s.right-1,16,!(m&2)&&!(m&1),-1,1],[s.left,47,!(m&8)&&!(m&4),1,-1],[s.right-1,47,!(m&2)&&!(m&4),-1,-1]];for(const [cx,cy,on,sx,sy] of corners){const dx=(x-cx)*sx,dy=(y-cy)*sy;if(on&&dx<6&&dy<6&&(dx-6)**2+(dy-6)**2>36)return false;}return true;}
