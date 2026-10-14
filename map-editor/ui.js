// Presentation state is transient. Project content and save slots stay in editor.js.
const $=id=>document.getElementById(id);
export function organizePalette(){
 for(const b of document.querySelectorAll('#materials [data-brush]'))if(b.dataset.brush.startsWith('water'))$('water-materials').append(b);
 syncTabs();
}
function syncTabs(){document.querySelectorAll('[data-tab]').forEach(b=>b.tabIndex=b.getAttribute('aria-selected')==='true'?0:-1);}
export function setupStudioUI(){
 const palette=$('build-drawer'),project=$('project-drawer'),phone=matchMedia('(max-width: 760px)');
 const syncBuild=()=>$('open-build').setAttribute('aria-expanded',String(palette.open));
 function closeBuild(){palette.close();syncBuild();}
 function openBuild(){if(palette.open)return;if(phone.matches)palette.showModal();else palette.show();syncBuild();}
 function responsive(){palette.close();if(!phone.matches&&!document.body.classList.contains('focus-mode'))palette.setAttribute('open','');syncBuild();}
 responsive();phone.addEventListener('change',responsive);palette.addEventListener('close',syncBuild);
 $('open-build').onclick=()=>palette.open?closeBuild():openBuild();$('close-build').onclick=closeBuild;
 $('project-panel').onclick=()=>project.showModal();$('close-project').onclick=()=>project.close();
 $('project-copy').onclick=()=>{$('copy').click();project.close();};
 const saved=$('saved'),mirror=()=>{$('project-save-state').textContent=saved.textContent;};new MutationObserver(mirror).observe(saved,{childList:true,characterData:true,subtree:true});mirror();
 $('help').onclick=()=>$('help-dialog').showModal();
 // Dismiss menus after an action and keep only one menu expanded at a time.
 document.querySelectorAll('.popover').forEach(menu=>{
  menu.addEventListener('toggle',()=>{if(menu.open)document.querySelectorAll('.popover').forEach(other=>{if(other!==menu)other.open=false;});});
  menu.addEventListener('click',e=>{if(e.target.closest('button')){menu.open=false;if(menu.id==='more-tools')$('viewport').focus({preventScroll:true});}});
 });
 document.addEventListener('pointerdown',e=>{document.querySelectorAll('.popover[open]').forEach(menu=>{if(!menu.contains(e.target))menu.open=false;});});
 document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('.popover[open]').forEach(menu=>menu.open=false);});
 $('focus-mode').onclick=()=>{
  const focused=document.body.classList.toggle('focus-mode');$('focus-mode').setAttribute('aria-pressed',String(focused));
  $('focus-mode').setAttribute('aria-label',focused?'Exit focus mode':'Focus canvas');if(focused)closeBuild();else if(!phone.matches)openBuild();
 };
 // Phone picker behaves like a tool tray: selecting returns to the canvas.
 palette.addEventListener('click',e=>{if(phone.matches&&e.target.closest('[data-brush],[data-stamp],[data-tile],#move-stamp')){closeBuild();$('viewport').focus({preventScroll:true});}});
 document.querySelector('.tabs').addEventListener('click',syncTabs);
 document.querySelector('.tabs').addEventListener('keydown',e=>{
  const tabs=[...document.querySelectorAll('[data-tab]')],index=tabs.indexOf(document.activeElement);if(index<0)return;
  const next=e.key==='ArrowRight'?(index+1)%tabs.length:e.key==='ArrowLeft'?(index+tabs.length-1)%tabs.length:e.key==='Home'?0:e.key==='End'?tabs.length-1:null;
  if(next!==null){e.preventDefault();tabs[next].click();tabs[next].focus();}
 });
 // Closing the project sheet before an action avoids stacked modal workflows.
 project.addEventListener('click',e=>{if(e.target.closest('#import,#download,#export-png,#new-project'))project.close();});
 for(const dialog of [palette,project,$('help-dialog')])dialog.addEventListener('click',e=>{
  if(e.target!==dialog)return;const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();
 });
}
