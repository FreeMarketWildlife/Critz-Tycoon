import {iconButton} from './dummy-icons.js';
export function createDummyHotbar({getState,setTool,revealCanvas,step,toggle,togglePlayback}){
  const view=document.getElementById('viewport'),area=document.createElement('div');area.className='dh-workarea';view.before(area);area.append(view);
  const rail=document.createElement('div');rail.id='dh-hotbar';rail.setAttribute('role','toolbar');rail.setAttribute('aria-label','Canvas hotbar');rail.setAttribute('aria-orientation','vertical');area.append(rail);
  const menu=document.createElement('div');menu.id='dh-pencil-menu';menu.hidden=true;menu.setAttribute('role','menu');menu.setAttribute('aria-label','Pencil tools');area.append(menu);
  const buttons={},tools=[['brush','brush','Pencil'],['fill','fill','Fill'],['line','line','Line'],['erase','erase','Erase']];let drawTool='brush',last='';
  const button=(id,glyph,label,caption)=>{const b=document.createElement('button');b.type='button';b.id='dh-'+id;iconButton(b,glyph,label,caption);rail.append(b);buttons[id]=b;return b;};
  button('move','hand','Move canvas','Move').onclick=()=>choose('pan');
  const pencil=button('pencil','brush','Pencil tools','Pencil');pencil.setAttribute('aria-haspopup','menu');pencil.setAttribute('aria-expanded','false');pencil.setAttribute('aria-controls',menu.id);
  pencil.onclick=()=>{const s=getState();revealCanvas();if(tools.some(([t])=>t===s.tool)){menu.hidden=!menu.hidden;pencil.setAttribute('aria-expanded',String(!menu.hidden));if(!menu.hidden)menu.querySelector('[aria-checked=true]').focus();}else choose(drawTool);};
  button('picker','picker','Eyedropper: pick dummy part and side','Pick').onclick=()=>choose('picker');
  button('play','play','Play dummy','Play').onclick=()=>{close();revealCanvas();togglePlayback();};
  button('next','next','Forward to next unique drawing','+1').onclick=()=>{close();revealCanvas();step(1);};
  button('prev','previous','Backward to previous unique drawing','−1').onclick=()=>{close();revealCanvas();step(-1);};
  button('reference','eye','Toggle reference visibility','Ref').onclick=()=>{close();revealCanvas();toggle('reference');};
  button('dummy','dummy','Toggle dummy visibility','Dummy').onclick=()=>{close();revealCanvas();toggle('labels');};
  for(const [tool,glyph,label]of tools){const b=document.createElement('button');b.type='button';b.dataset.tool=tool;b.setAttribute('role','menuitemradio');iconButton(b,glyph,label,label);b.onclick=()=>{drawTool=tool;choose(tool);pencil.focus();};menu.append(b);}
  function close(focus=false){menu.hidden=true;pencil.setAttribute('aria-expanded','false');if(focus)pencil.focus();}
  function choose(tool){close();revealCanvas();setTool(tool);sync();}
  function sync(){
    const s=getState(),key=JSON.stringify([s.ready,s.tool,s.playing,s.layers.reference.visible,s.layers.labels.visible]);if(key===last)return;last=key;
    iconButton(buttons.play,s.playing?'pause':'play',s.playing?'Pause dummy':'Play dummy',s.playing?'Pause':'Play');
    buttons.play.setAttribute('aria-pressed',String(!!s.playing));
    if(tools.some(([t])=>t===s.tool))drawTool=s.tool;
    const [,glyph,label]=tools.find(([t])=>t===drawTool);iconButton(pencil,glyph,label+' tools',label);
    for(const b of Object.values(buttons))b.disabled=!s.ready;
    for(const [id,pressed]of [['move',s.tool==='pan'],['pencil',tools.some(([t])=>t===s.tool)],['picker',s.tool==='picker'],['reference',s.layers.reference.visible],['dummy',s.layers.labels.visible]])buttons[id].setAttribute('aria-pressed',String(pressed));
    for(const b of menu.children)b.setAttribute('aria-checked',String(b.dataset.tool===drawTool));
  }
  menu.addEventListener('keydown',e=>{const items=[...menu.children],i=items.indexOf(document.activeElement);if(e.key==='Escape'){e.preventDefault();e.stopPropagation();close(true);}else if(['ArrowDown','ArrowUp','Home','End'].includes(e.key)){e.preventDefault();items[e.key==='Home'?0:e.key==='End'?items.length-1:(i+(e.key==='ArrowDown'?1:items.length-1))%items.length].focus();}});
  rail.addEventListener('keydown',e=>{if(!['ArrowUp','ArrowDown','Home','End'].includes(e.key))return;const items=[...rail.children].filter(b=>!b.disabled),i=items.indexOf(document.activeElement);e.preventDefault();items[e.key==='Home'?0:e.key==='End'?items.length-1:(i+(e.key==='ArrowDown'?1:items.length-1))%items.length]?.focus();});
  document.addEventListener('pointerdown',e=>{if(!menu.hidden&&!menu.contains(e.target)&&!pencil.contains(e.target))close();});
  new MutationObserver(()=>{if(!document.body.classList.contains('compact-dummy'))close();}).observe(document.body,{attributes:true,attributeFilter:['class']});
  sync();return {sync};
}
