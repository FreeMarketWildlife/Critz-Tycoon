import {parseProject,validateProject} from './dummy-creator-model.js';
// Retain the live dataset identity: existing autosaves always win over a new seed.
export const DEFAULT_DATASET='phil-walk-draft-20261017';
export const DATASETS={
 'phil-20261016':{id:'phil-20261016',name:'Phil’s earlier supplied labels',url:'./assets/phil-region-labels-20261016.json',kind:'corrections'},
 'phil-south-20261017':{id:'phil-south-20261017',name:'Phil’s completed south',url:'./assets/phil-completed-south-20261017.json',kind:'project'},
 'phil-walk-draft-20261017':{id:'phil-walk-draft-20261017',name:'Phil’s supplied default · 27 Oct 2026',url:'./assets/phil-default-20261027.json',kind:'project',supplied:true},
 'phil-supplied-20261027':{id:'phil-supplied-20261027',name:'Phil’s supplied project · 27 Oct 2026',url:'./assets/phil-default-20261027.json',kind:'project',supplied:true},
 'phil-supplied-20261022':{id:'phil-supplied-20261022',name:'Previous supplied project · 22 Oct 2026',url:'./assets/phil-default-20261022.json',kind:'project',supplied:true},
 'phil-walk-original-20261017':{id:'phil-walk-original-20261017',name:'Original rough walking draft · 17 Oct 2026',url:'./assets/phil-rough-walk-20261017.json',kind:'project',rough:true}
};
// Pure selection, no storage writes. Invalid saved content is reported by the caller.
export function projectForDraft(preset,savedText,seed){return savedText?parseProject(savedText,seed):validateProject(preset,seed);}
