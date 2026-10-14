// Published starting bases are immutable files; every revision gets a separate
// local draft slot. Updating a base never silently replaces an older draft.
export const AREAS=Object.freeze([{id:'rootport',name:'Rootport',revision:1,path:'./areas/rootport.json'}]);
export function selectedArea(id){return AREAS.find(a=>a.id===id)||null;}
export function areaDraftKey(area){return `critz.map-editor.area.${area.id}.r${area.revision}.v1`;}
export function areaHref(id){if(!selectedArea(id))throw Error('Unknown area');return '?area='+encodeURIComponent(id);}
