// Mirror subsequent edits across the vertical (Y) axis, never existing artwork.
export function mirrorPoints(width,x,y,enabled=false){
 if(!Number.isInteger(width)||width<1||!Number.isInteger(x)||!Number.isInteger(y)||x<0||x>=width||y<0)return [];
 const opposite=width-1-x;
 return enabled&&opposite!==x?[[x,y],[opposite,y]]:[[x,y]];
}
export function createMirrorToggle(beforeChange=()=>{}){
 const button=document.getElementById('mirror');
 let enabled=false;
 const render=()=>{button.setAttribute('aria-pressed',String(enabled));button.setAttribute('aria-label',`Mirror edits across vertical Y axis: ${enabled?'on':'off'}`);button.title=`Mirror left ↔ right across vertical Y axis: ${enabled?'on':'off'}. Only new edits are mirrored.`;button.querySelector('.mirror-state').textContent=enabled?'On':'Off';};
 button.addEventListener('click',()=>{beforeChange();enabled=!enabled;render();});
 render();return{get enabled(){return enabled;}};
}
