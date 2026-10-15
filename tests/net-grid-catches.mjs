import {writeFileSync} from 'node:fs';
import {createNetTest,stepNetTest,pressNet,releaseNet,occupiedCell,blocked,DIR} from '../art-review/net-grid-state.js';
const s=createNetTest();const log=[];
for(let tick=0;tick<30000&&s.caught.length<6;tick++){
 let direction;if(!s.swing&&!s.pendingSwing&&!s.netHeld)pressNet(s);
 if(!s.swing&&s.player.settled){
  const remaining=s.critters.filter(c=>!c.caught&&!c.escaped&&!c.escape),near=remaining.find(c=>{const q=occupiedCell(c);return Math.abs(q.x-s.cell.x)+Math.abs(q.y-s.cell.y)===1;});
  if(near){const q=occupiedCell(near);direction=q.x>s.cell.x?'right':q.x<s.cell.x?'left':q.y>s.cell.y?'down':'up';if(s.player.facing===direction){if(s.ready)releaseNet(s);direction=undefined;}}
  else {const queue=[{x:s.cell.x,y:s.cell.y,first:null}],seen=new Set([s.cell.x+','+s.cell.y]);for(const p of queue){if(remaining.some(c=>{const q=occupiedCell(c);return Math.abs(q.x-p.x)+Math.abs(q.y-p.y)===1;})){direction=p.first;break;}for(const [d,[dx,dy]]of Object.entries(DIR)){const x=p.x+dx,y=p.y+dy,k=x+','+y;if(seen.has(k)||blocked(s,x,y,'player'))continue;seen.add(k);queue.push({x,y,first:p.first||d});}}}
 }
 const n=s.caught.length;stepNetTest(s,{direction});if(s.caught.length>n)log.push({tick,kind:s.caught.at(-1).kind,swings:s.swings});
}
const report={input:'Direction/ready/swing model inputs only; observer reads state without teleport or critter mutation',caught:s.caught.length,swings:s.swings,ticks:s.tick,log};writeFileSync(process.env.CRITZ_NET_GRID_CATCH_PROOF||'docs/reviews/M1-NET3/catching-model-report.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));if(s.caught.length!==6)process.exitCode=1;
