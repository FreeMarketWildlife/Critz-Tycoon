// Relaxed walking preview: retain every authored slot and its relative hold.
// This is a view-only cadence; project timing and gameplay remain unchanged.
export const WALK_PREVIEW_LOOP_MS=800;
export function walkingPreviewFrames(frames){
 const total=frames.reduce((n,f)=>n+f.durationMs,0);
 return frames.map(f=>({...f,durationMs:f.durationMs*WALK_PREVIEW_LOOP_MS/total}));
}
