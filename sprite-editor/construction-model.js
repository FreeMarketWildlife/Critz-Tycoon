// Semantic labels belong to this user-authored template, never to arbitrary
// colored artwork. The mask stays fixed when the user changes paint colors.
export const REGIONS=[
 ['all','Whole skeleton','All 720 occupied template cells, including the outline.'],
 ['head','Head','Rounded cranium and face. Eye landmarks remain at x12–13 and x18–19, rows38–41.'],
 ['eyes','Eye landmarks','Two 2 × 4 landmarks; these white cells are construction markers.'],
 ['body','Body / torso','Main torso plane and the shaded shoulder/neck area beneath the head.'],
 ['left-arm','Left arm / hand','Screen-left arm and hand volume; pink is a region label.'],
 ['right-arm','Right arm / hand','Screen-right arm and hand volume; pink is a region label.'],
 ['pelvis','Pelvis / upper legs','Green connects the torso to the two legs.'],
 ['left-leg','Left leg / foot','Screen-left lower leg and foot volume; coral is a region label.'],
 ['right-leg','Right leg / foot','Screen-right lower leg and foot volume; coral is a region label.'],
 ['shading','Shading','Medium/deep blue head shading and dark-gray torso shading.'],
 ['outline','Outline / separations','Dark-brown silhouette edge and internal form separations.']
];
export const RAMPS=[
 {id:'head',label:'Head · deep → light',colors:['#184080','#3878b8','#68b0e0']},
 {id:'body',label:'Body · shadow → base',colors:['#707078','#9898a0']},
 {id:'foliage',label:'Foliage',colors:['#083018','#185828','#388840','#68b858','#a0e068','#d8f880']},
 {id:'earth',label:'Earth / skin',colors:['#482810','#784820','#a87038','#d0a068','#f8d8b0']},
 {id:'coral',label:'Warm accents',colors:['#e84038','#fc7858','#fcd080']},
 {id:'teal',label:'Teal',colors:['#289870','#48d098','#a0f8d0']},
 {id:'stone',label:'Stone',colors:['#282830','#484850','#707078','#9898a0','#c0c0c8','#e0e0e8']}
];
export function regionAt(template,x,y){
 if(x<0||y<0||x>=32||y>=64)return 'empty';
 const hex=template.palette[template.frames[0].pixels[y*32+x]]?.toLowerCase();
 if(!hex)return 'empty';
 return {'#201008':'outline','#68b0e0':'head','#3878b8':'head','#184080':'head','#f8f8f8':'eyes','#707078':'body','#9898a0':'body','#f85888':x<16?'left-arm':'right-arm','#388840':'pelvis','#fc7858':x<16?'left-leg':'right-leg'}[hex]||'empty';
}
export function matchesRegion(template,region,x,y){
 const actual=regionAt(template,x,y);
 if(region==='all')return actual!=='empty';
 if(region==='head')return actual==='head'||actual==='eyes';
 if(region==='shading')return ['#184080','#3878b8','#707078'].includes(template.palette[template.frames[0].pixels[y*32+x]]?.toLowerCase());
 return region===actual;
}
export function shadeColor(hex,direction,rampId){
 const ramp=RAMPS.find(r=>r.id===rampId);const at=ramp?.colors.indexOf(hex?.toLowerCase());
 if(at===undefined||at<0)return hex;
 return ramp.colors[Math.max(0,Math.min(ramp.colors.length-1,at+direction))];
}
export function symmetryCounts(pixels,width,height){
 let silhouette=0,color=0;
 for(let y=0;y<height;y++)for(let x=0;x<Math.floor(width/2);x++){
  const a=pixels[y*width+x],b=pixels[y*width+width-1-x];
  if(Boolean(a)!==Boolean(b))silhouette++;if(a!==b)color++;
 }
 return {silhouette,color};
}
