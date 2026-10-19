// Responsive chrome only. Move existing controls, never clone project state.
export function createDummyMobile({onResize,onClose}) {
  const $=id=>document.getElementById(id);
  const media=matchMedia('(max-width: 1100px), (pointer: coarse) and (max-width: 1400px)');
  const tabs=[['canvas','Canvas'],['draw','Draw'],['frames','Frames'],['view','View'],['file','File']];
  const nav=document.createElement('nav');nav.className='dm-tabs';nav.setAttribute('role','tablist');nav.setAttribute('aria-label','Editor workspace');
  const sheet=document.createElement('section');sheet.id='dm-sheet';sheet.className='dm-sheet';sheet.hidden=true;
  sheet.innerHTML='<div class="dm-sheet-heading"><strong id="dm-heading"></strong><button type="button" id="dm-close" aria-label="Return to canvas">Done</button></div><div class="dm-sheet-scroll"></div>';
  const panels=new Map(),buttons=new Map(),moves=[];let compact=false,selected='canvas';
  const undo=document.createElement('div');undo.className='dm-history';undo.setAttribute('aria-label','Edit history');
  for(const [id,label]of tabs){
    const b=document.createElement('button');b.id='dm-tab-'+id;b.type='button';b.textContent=label;b.setAttribute('role','tab');b.setAttribute('aria-selected',String(id==='canvas'));b.tabIndex=id==='canvas'?0:-1;
    b.setAttribute('aria-controls',id==='canvas'?'viewport':'dm-panel-'+id);nav.append(b);buttons.set(id,b);
    if(id!=='canvas'){const p=document.createElement('div');p.id='dm-panel-'+id;p.className='dm-tab-panel';p.hidden=true;p.setAttribute('role','tabpanel');p.setAttribute('aria-labelledby',b.id);panels.set(id,p);sheet.querySelector('.dm-sheet-scroll').append(p);}
    b.addEventListener('click',()=>select(id));
    b.addEventListener('keydown',e=>{const k=tabs.findIndex(([name])=>name===id);const next=e.key==='ArrowRight'?(k+1)%tabs.length:e.key==='ArrowLeft'?(k+tabs.length-1)%tabs.length:e.key==='Home'?0:e.key==='End'?tabs.length-1:null;if(next===null)return;e.preventDefault();select(tabs[next][0]);buttons.get(tabs[next][0]).focus();});
  }
  function select(id,focus=false){
    onClose();selected=id;sheet.hidden=id==='canvas';document.body.dataset.dummyTab=id;
    for(const [name,b]of buttons){b.setAttribute('aria-selected',String(name===id));b.tabIndex=name===id?0:-1;}
    for(const [name,p]of panels)p.hidden=name!==id;
    $('dm-heading').textContent=tabs.find(([name])=>name===id)[1];
    sheet.querySelector('.dm-sheet-scroll').scrollTop=0;
    if(focus)buttons.get(id).focus();onResize();
  }
  function move(node,target){if(!node)return;const placeholder=document.createComment('responsive control home');node.before(placeholder);moves.push([node,placeholder]);target.append(node);}
  $('workspace').append(sheet);document.querySelector('main').append(nav);document.querySelector('.app-header').append(undo);
  $('dm-close').onclick=()=>select('canvas',true);
  document.addEventListener('keydown',e=>{if(compact&&selected!=='canvas'&&e.key==='Escape'&&!document.querySelector('dialog[open]')){e.preventDefault();select('canvas',true);}});
  // Selecting a facing or a part immediately returns the drawing surface.
  $('dc-facing').addEventListener('click',e=>{if(compact&&e.target.closest('[data-dc-facing]'))select('canvas');});
  $('br-parts').addEventListener('click',e=>{if(compact&&e.target.closest('button'))select('canvas');});
  function apply(){
    if(compact===media.matches)return;
    compact=media.matches;document.body.classList.toggle('compact-dummy',compact);
    if(compact){
      move($('undo'),undo);move($('redo'),undo);
      move($('dc-facing'),panels.get('draw'));
      const drawTools=document.createElement('div');drawTools.className='dm-drawing-tools';panels.get('draw').append(drawTools);
      move($('tools'),drawTools);move(document.querySelector('.tool-options'),drawTools);
      const options=document.querySelector('.canvas-options');
      for(const n of [...options.querySelectorAll('.br-select')])move(n,panels.get('draw'));
      move($('dc-orientation'),panels.get('draw'));move($('br-parts-panel'),panels.get('draw'));
      move(document.querySelector('.dc-timeline'),panels.get('frames'));
      move(options,panels.get('view'));move($('br-layers-panel'),panels.get('view'));move($('dc-reference-panel'),panels.get('view'));
      for(const id of ['save-state','br-import','br-download','br-dataset','br-data-panel','help'])move($(id),panels.get('file'));
      // Always open compact devices on Canvas, regardless of old desktop docks.
      select('canvas');
    }else{
      onClose();for(const [node,placeholder]of moves.reverse()){placeholder.replaceWith(node);}moves.length=0;
      for(const panel of panels.values())for(const n of [...panel.children])if(n.classList.contains('dm-drawing-tools'))n.remove();
      sheet.hidden=true;delete document.body.dataset.dummyTab;onResize();
    }
  }
  media.addEventListener('change',apply);apply();
  return {revealCanvas(){if(compact)select('canvas');},snapshot:()=>({compact,tab:selected})};
}
