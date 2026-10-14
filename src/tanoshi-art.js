import {loadAtlas} from './atlas.js';
let atlas,sizes;
export async function loadTanoshiArt(){[atlas,sizes]=await Promise.all([loadAtlas(new URL('../assets/playable/tanoshi/atlas.json',import.meta.url)),loadAtlas(new URL('../assets/playable/tanoshi-sizes/atlas.json',import.meta.url))]);}
export function drawTanoshi(c,individual){
  // Explicit bottom-center cell registration. Decorative discovery actors have
  // no blocker; neither rays nor tail infer collision or overhead projection.
  (individual.size?sizes:atlas).draw(c,individual.size||individual.variant,individual.x*32,individual.y*32);
}
