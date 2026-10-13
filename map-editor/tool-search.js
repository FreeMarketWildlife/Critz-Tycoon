const aliases={cottage:'house home building door entrance',garden:'house home building door entrance',shop:'building store door entrance',stairs:'steps staircase climb cliff',cave:'door opening entrance exit',fence:'rail barrier gate',tree:'broadleaf canopy roots forest grove',willow:'tree canopy roots forest hanging',palm:'tree canopy roots fronds coast',cypress:'tree canopy roots forest',water:'pond lake river sea ocean shore',path:'road trail dirt',paving:'road concrete stone',soil:'garden dirt earth',bridge:'crossing deck',boulder:'rock stone push',ledge:'jump hop cliff edge'};
export function toolMatches(query,id,label='') {
 const terms=query.toLowerCase().trim().split(/\s+/).filter(Boolean);
 const words=`${id} ${id.replaceAll(/[.:_-]/g,' ')} ${label} ${Object.entries(aliases).filter(([key])=>id.includes(key)).map(([,v])=>v).join(' ')}`.toLowerCase();
 return terms.every(term=>words.includes(term));
}
