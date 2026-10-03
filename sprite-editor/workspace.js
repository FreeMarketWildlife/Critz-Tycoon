// Dock sizes/visibility are UI preferences, isolated from sprite and game saves.
export function createWorkspace({onResize, onAnimationCollapse}) {
  const $=id=>document.getElementById(id),root=$('workspace');
  const KEY='fmw.sprite-editor.layout.v1';
  const defaults=()=>({tools:true,inspector:innerWidth>=900,animation:false,toolsWidth:58,inspectorWidth:290,timelineHeight:185,sections:{}});
  let state=defaults(),focusSnapshot=null,drag=null,persistTimer;
  try {const saved=JSON.parse(localStorage.getItem(KEY));if(saved&&typeof saved==='object'){
    for(const k of ['tools','inspector','animation'])if(typeof saved[k]==='boolean')state[k]=saved[k];
    for(const k of ['toolsWidth','inspectorWidth','timelineHeight'])if(Number.isFinite(saved[k]))state[k]=saved[k];
    if(saved.sections&&typeof saved.sections==='object')state.sections=saved.sections;
  }} catch {}
  function clamp(){state.toolsWidth=Math.max(48,Math.min(180,state.toolsWidth));state.inspectorWidth=Math.max(240,Math.min(520,innerWidth*.45,state.inspectorWidth));state.timelineHeight=Math.max(135,Math.min(Math.max(135,root.clientHeight*.48),state.timelineHeight));}
  function save(){clearTimeout(persistTimer);persistTimer=setTimeout(()=>{try{localStorage.setItem(KEY,JSON.stringify(focusSnapshot||state));}catch{}},120);}
  function apply(persist=true){
    clamp();root.style.setProperty('--tools-width',state.toolsWidth+'px');root.style.setProperty('--inspector-width',state.inspectorWidth+'px');root.style.setProperty('--timeline-height',state.timelineHeight+'px');
    root.dataset.tools=state.tools;root.dataset.inspector=state.inspector;root.dataset.wideTools=state.toolsWidth>=110;
    for(const key of ['tools','inspector','animation'])$('toggle-'+key).setAttribute('aria-expanded',String(state[key]));
    $('timeline').dataset.collapsed=String(!state.animation);$('animation-content').hidden=!state.animation;$('animation-resize').hidden=!state.animation;
    $('collapse-animation').setAttribute('aria-expanded',String(state.animation));$('collapse-animation').querySelector('.chevron').textContent=state.animation?'▾':'▸';
    $('focus-mode').setAttribute('aria-pressed',String(!!focusSnapshot));
    for(const [id,value,min,max] of [['tools-resize',state.toolsWidth,48,180],['inspector-resize',state.inspectorWidth,240,520],['animation-resize',state.timelineHeight,135,Math.max(135,Math.round(root.clientHeight*.48))]]){const el=$(id);el.setAttribute('aria-valuenow',Math.round(value));el.setAttribute('aria-valuemin',min);el.setAttribute('aria-valuemax',max);}
    if(persist)save();onResize();
  }
  function toggle(key){focusSnapshot=null;state[key]=!state[key];if(key==='animation'&&!state.animation)onAnimationCollapse();apply();}
  for(const key of ['tools','inspector','animation'])$('toggle-'+key).onclick=()=>toggle(key);
  $('collapse-animation').onclick=()=>toggle('animation');$('close-inspector').onclick=()=>{if(state.inspector)toggle('inspector');};
  $('focus-mode').onclick=()=>{if(focusSnapshot){state=focusSnapshot;focusSnapshot=null;}else{focusSnapshot=structuredClone(state);state={...state,tools:false,inspector:false,animation:false};onAnimationCollapse();}apply();};
  $('reset-layout').onclick=()=>{focusSnapshot=null;state=defaults();for(const d of document.querySelectorAll('.inspector details'))d.open=['palette-panel','reference-panel'].includes(d.id);apply();};
  for(const d of document.querySelectorAll('.inspector details')){
    if(typeof state.sections[d.id]==='boolean')d.open=state.sections[d.id];
    d.addEventListener('toggle',()=>{state.sections[d.id]=d.open;if(focusSnapshot)focusSnapshot.sections[d.id]=d.open;save();});
  }
  const configurations={'tools-resize':['toolsWidth',1,'x',58],'inspector-resize':['inspectorWidth',-1,'x',290],'animation-resize':['timelineHeight',-1,'y',185]};
  for(const [id,[property,direction,axis,initial]]of Object.entries(configurations)){
    const el=$(id);
    el.addEventListener('pointerdown',e=>{if(e.button!==0)return;e.preventDefault();drag={id,property,direction,axis,pointer:e.pointerId,start:axis==='x'?e.clientX:e.clientY,value:state[property]};el.setPointerCapture(e.pointerId);el.classList.add('dragging');});
    el.addEventListener('pointermove',e=>{if(!drag||drag.id!==id||drag.pointer!==e.pointerId)return;state[property]=drag.value+((axis==='x'?e.clientX:e.clientY)-drag.start)*direction;apply(false);});
    const end=()=>{if(drag?.id===id){drag=null;el.classList.remove('dragging');apply();}};
    el.addEventListener('pointerup',end);el.addEventListener('pointercancel',end);el.addEventListener('lostpointercapture',end);
    el.addEventListener('dblclick',()=>{state[property]=initial;apply();});
    el.addEventListener('keydown',e=>{const sign={ArrowLeft:-1,ArrowRight:1,ArrowUp:-1,ArrowDown:1}[e.key];if(!sign)return;e.preventDefault();state[property]+=sign*direction*(e.shiftKey?40:10);apply();});
  }
  window.addEventListener('resize',()=>apply(false));
  // ResizeObserver reports the actual drawable area after collapse/drag/font load.
  new ResizeObserver(()=>onResize()).observe($('viewport'));
  apply(false);
  return {revealCanvas(){if(innerWidth<900&&state.inspector){state.inspector=false;apply();}},showAnimation(){if(!state.animation){state.animation=true;apply();}},showInspector(){if(!state.inspector){state.inspector=true;apply();}},snapshot:()=>structuredClone(state)};
}
