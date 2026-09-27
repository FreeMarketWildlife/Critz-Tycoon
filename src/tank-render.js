// Native-pixel habitat close-up. Appearance only: never mutates tank state,
// simulation timing, camera scores, snapshots, or Critter payout rules.
// Matches the warm soil/cool glass/clustered leaf family of the playable atlas.
const P = {
  ink: '#50546b', deep: '#3b656b', back: '#739f98', backLight: '#8bb4a5',
  glass: '#a5d9d2', glassDark: '#5e9aab', glassLight: '#d0e1c5',
  soil: '#96744f', soilDark: '#6f594b', soilLight: '#b69a64',
  wood: '#a77c56', woodDark: '#735c49', woodLight: '#dec091',
  leafDark: '#3d794a', leaf: '#70a856', leafLight: '#9bca69', moss: '#5e975a',
  cream: '#e6e5cb', white: '#f4edcc', slate: '#737d79', slateLight: '#adb5a0',
  algae: '#80a663', waste: '#5b4b3f', amber: '#c8a365', redLeaf: '#b88460',
};

// Original, reusable row-authored native sprites. Every painted sample is an
// opaque integer pixel; no ellipse, fractional rectangle, blur or alpha wash.
export const TANK_SPRITES = {
  isopodA: ['...2222.....', '..2333321...', '.123343321..', '123434343211', '.123333321..', '..1.1.1.1...'],
  isopodB: ['...2222.....', '..2333321...', '.123343321..', '123434343211', '.123333321..', '.1.1.1.1....'],
  springtailA: ['.22.', '2211', '.1..'],
  springtailB: ['.22.', '2211', '1.1.'],
  leafA: ['...2221.', '.223321.', '2233221.', '.22211..', '..11....'],
  leafB: ['..111...', '.12221..', '1223321.', '.12221..', '..121...', '...1....'],
  stone: ['...222222...', '..23333332..', '.2334333332.', '233333333332', '222333322222', '.122222221..'],
  log: ['......3333333333333333333.......', '...2333333333333333333333332....', '..23322222222222222222222222...', '.2332222222222222222222222222..', '233222222222211111222222222221.', '232122222222222222222222222221.', '232132222222222222222222222221.', '232132222222222222222222222211.', '.2322222211111112222222222211..', '..22222222222222222222222211...', '...111111111111111111111111....'],
  hide: ['.....333333333333.....', '...3322222222222233...', '..332222222222222233..', '.32222222222222222223.', '3222222221111222222223', '3222222111111112222223', '2222221111111111222222', '2222211111111111122222', '1111111111111111111111'],
  frond: ['.......3........', '......233.......', '......223.......', '...33.22........', '..332222....3...', '...22222..3333..', '......2233322...', '...3..22222.....', '..333222........', '...22222...33...', '......22..3333..', '......2233322...', '...33.22222.....', '..333222........', '...22222..33....', '......22.3333...', '......223322....', '....332222......', '...33322........', '....2222........', '......22........', '......11........'],
  moss: ['....333..33......333......', '..3333333333...3333333....', '.3322223322333332222333..', '332222222222222222222233.', '.2222222222222222222222..', '..11111111111111111111...'],
};

function rect(context, x, y, w, h, color) {
  context.fillStyle = color;
  context.fillRect(Math.round(x), Math.round(y), Math.max(1, Math.round(w)), Math.max(1, Math.round(h)));
}
function pixels(context, rows, x, y, colors, flip = false) {
  const width = Math.max(...rows.map(row => row.length));
  for (let row = 0; row < rows.length; row++) for (let col = 0; col < rows[row].length; col++) {
    const code = rows[row][col];
    if (code !== '.') rect(context, x + (flip ? width - 1 - col : col), y + row, 1, 1, colors[Number(code) - 1]);
  }
}
const buffers = new WeakMap();
function bufferFor(canvas, width, height) {
  let buffer = buffers.get(canvas);
  if (!buffer) {
    buffer = {scene: document.createElement('canvas'), view: document.createElement('canvas')};
    buffers.set(canvas, buffer);
  }
  if (buffer.scene.width !== width + 40 || buffer.scene.height !== height) {
    buffer.scene.width = width + 40; buffer.scene.height = height;
    buffer.view.width = width; buffer.view.height = height;
  }
  return buffer;
}
const clamp = (value, min, max) => Math.max(min, Math.min(max, Number.isFinite(value) ? value : min));

export function renderTank(canvas, tank, time = 0, {frame = 50, zoom = 1, reticle = false} = {}) {
  // Existing 400x200 snapshots remain 400x200; the welcome image remains
  // 400x148. Both are composed at exact half resolution then presented at 2x.
  const width = Math.ceil(canvas.width / 2), height = Math.ceil(canvas.height / 2);
  const {scene, view} = bufferFor(canvas, width, height);
  const c = scene.getContext('2d'), v = view.getContext('2d'), target = canvas.getContext('2d');
  c.imageSmoothingEnabled = v.imageSmoothingEnabled = target.imageSmoothingEnabled = false;
  const worldWidth = scene.width, bottom = Math.floor(height * 0.81);
  rect(c, 0, 0, worldWidth, height, P.back);
  rect(c, 0, 0, worldWidth, 12, P.backLight);
  rect(c, 0, 12, worldWidth, 2, '#81aba0');
  rect(c, 0, bottom - 8, worldWidth, 8, '#65958b');
  // A calm glass backdrop and short contact colors keep native silhouettes clear.
  for (const x of [21, 87, 166, 226]) {
    rect(c, x, 17, 1, Math.max(1, bottom - 30), '#8fb9ac');
    rect(c, x + 1, 18, 1, Math.max(1, bottom - 32), '#82afa4');
  }
  rect(c, 0, bottom, worldWidth, height - bottom, P.soilDark);
  rect(c, 0, bottom, worldWidth, 3, P.soilLight);
  rect(c, 0, bottom + 3, worldWidth, 7, P.soil);
  rect(c, 0, bottom + 10, worldWidth, 1, '#806249');
  for (let i = 0; i < 45; i++) rect(c, (i * 43 + 8) % worldWidth,
    bottom + 4 + (i * 7) % Math.max(1, height - bottom - 6), i % 3 ? 2 : 1, 1,
    [P.soilLight, P.soilDark, '#a28459'][i % 3]);

  pixels(c, TANK_SPRITES.log, Math.floor(worldWidth * 0.47), bottom - 11, [P.woodDark, P.wood, P.woodLight]);
  pixels(c, TANK_SPRITES.stone, Math.floor(worldWidth * 0.69), bottom - 5, [P.ink, P.slate, P.slateLight, P.cream]);
  pixels(c, TANK_SPRITES.stone, Math.floor(worldWidth * 0.73), bottom - 4, [P.ink, P.slate, P.slateLight, P.cream], true);
  if (tank.hide) pixels(c, TANK_SPRITES.hide, Math.floor(worldWidth * 0.27), bottom - 9, [P.deep, P.wood, P.woodLight]);

  const plants = Math.floor(clamp(tank.plants, 0, 6));
  for (let i = 0; i < plants; i++) {
    const x = 34 + (i * 37) % (worldWidth - 64), sway = Math.round(Math.sin(time * 0.8 + i));
    const extra = i % 3 * 5;
    rect(c, x + 7, bottom - 16 - extra, 2, 16 + extra, P.leafDark);
    pixels(c, TANK_SPRITES.frond, x + sway, bottom - 21 - extra, [P.leafDark, P.leaf, P.leafLight], i % 2 === 1);
    pixels(c, TANK_SPRITES.moss, x - 4, bottom - 4, [P.leafDark, P.moss, P.leafLight]);
  }
  const food = Math.floor(clamp(tank.food, 0, 100) / 6);
  for (let i = 0; i < food; i++) pixels(c, TANK_SPRITES[i % 2 ? 'leafA' : 'leafB'],
    10 + (i * 31) % (worldWidth - 25), bottom - 4 - i % 3,
    [P.woodDark, i % 2 ? P.redLeaf : P.amber, P.woodLight], i % 3 === 1);

  const stressFactor = tank.stress > 50 ? 0.3 : 1;
  const walkFrame = Math.floor(time * 7 * stressFactor) % 2;
  for (let i = 0; i < Math.min(24, tank.isopods || 0); i++) {
    const x = 12 + Math.floor((i * 31 + time * (1.5 + i % 3) * stressFactor) % (worldWidth - 30));
    const y = bottom - 6 - (i % 3) * 5;
    pixels(c, TANK_SPRITES[walkFrame ? 'isopodA' : 'isopodB'], x, y,
      [P.ink, '#828b83', '#b8bca6', '#e4e1c2']);
  }
  for (let i = 0; i < Math.min(35, tank.springtails || 0); i++) {
    const x = 8 + Math.floor((i * 23 + time * stressFactor) % (worldWidth - 16));
    const hop = Math.sin(time * 2 * stressFactor + i) > 0.95 ? 2 : 0;
    pixels(c, TANK_SPRITES[hop ? 'springtailB' : 'springtailA'], x, bottom - 3 - (i % 6) * 2 - hop,
      ['#b9c5a7', P.white]);
  }
  for (let i = 0; i < Math.floor(clamp(tank.waste, 0, 100) / 9); i++) {
    const x = 16 + (i * 47) % (worldWidth - 30);
    rect(c, x, bottom - 1, 3, 2, P.waste); rect(c, x + 1, bottom - 2, 2, 1, P.soilDark);
  }
  for (let i = 0; i < Math.floor(clamp(tank.algae, 0, 100) / 4); i++) {
    const x = 7 + i * 29 % (worldWidth - 14), y = 19 + i * 17 % Math.max(1, bottom - 23);
    rect(c, x, y, 4, 2, P.algae); rect(c, x + 1, y - 1, 2, 1, '#a1bc7d');
  }
  if (tank.moisture > 78) for (let i = 0; i < 14; i++) {
    const x = 12 + i * 17 % (worldWidth - 24), y = 8 + i * 23 % Math.max(1, bottom - 16);
    rect(c, x, y, 1, 2, P.glassLight); rect(c, x, y + 2, 2, 1, P.glassDark);
  }

  const z = clamp(zoom, 1, 1.6), cropWidth = Math.round(width / z), cropHeight = Math.round(height / z);
  const sourceX = Math.round((worldWidth - cropWidth) / 2 + (clamp(frame, 0, 100) - 50) * 0.3);
  const sourceY = Math.round((height - cropHeight) / 2);
  v.drawImage(scene, sourceX, sourceY, cropWidth, cropHeight, 0, 0, width, height);
  rect(v, 0, 0, width, 2, P.cream); rect(v, 0, 2, width, 1, P.glassDark);
  rect(v, 0, height - 2, width, 2, P.deep);
  rect(v, 0, 0, 2, height, P.glass); rect(v, width - 2, 0, 2, height, P.glassDark);
  rect(v, 4, 6, 1, height - 15, P.glassLight);
  for (let x = 9; x < width - 5; x += 4) rect(v, x, 1, 1, 1, P.deep);
  if (reticle) {
    const pad = 8, len = 6;
    for (const [x, y, dx, dy] of [[pad,pad,1,1],[width-pad-1,pad,-1,1],[pad,height-pad-1,1,-1],[width-pad-1,height-pad-1,-1,-1]]) {
      rect(v, x + (dx < 0 ? -len : 0), y, len + 1, 1, P.white);
      rect(v, x, y + (dy < 0 ? -len : 0), 1, len + 1, P.white);
    }
    // Sparse solid marks preserve a clear composition guide without alpha haze.
    for (let y = pad + 5; y < height - pad; y += 5) for (const x of [Math.round(width/3),Math.round(width*2/3)]) rect(v,x,y,1,1,P.glass);
    for (let x = pad + 5; x < width - pad; x += 5) for (const y of [Math.round(height/3),Math.round(height*2/3)]) rect(v,x,y,1,1,P.glass);
  }
  target.clearRect(0, 0, canvas.width, canvas.height);
  target.drawImage(view, 0, 0, width, height, 0, 0, canvas.width, canvas.height);
}
