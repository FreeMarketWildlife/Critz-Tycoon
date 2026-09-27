import { loadAtlas } from '../src/atlas.js';

const canvas = document.querySelector('#scene');
const context = canvas.getContext('2d');
const position = document.querySelector('#position');
const grid = document.querySelector('#grid');
const status = document.querySelector('#status');
const placements = { door: [96, 128], beside: [64, 112], behind: [40, 96] };
let atlas, selected;

function draw() {
  if (!atlas) return;
  for (let y = 0; y < 160; y += 16)
    for (let x = 0; x < 240; x += 16) atlas.draw(context, 'ground.grass', x, y);
  atlas.draw(context, 'building.rootport.proof', 72, 32);
  atlas.draw(context, 'plant.flowers', 42, 128);
  atlas.draw(context, 'plant.flowers', 168, 128);
  const [x, y] = placements[position.value];
  const objects = [
    { y: 112, draw: () => atlas.draw(context, 'tree.clustered', 24, 80) },
    { y: 112, draw: () => atlas.draw(context, 'tree.clustered', 184, 80) },
    { y, draw: () => atlas.draw(context, selected.id, x - selected.groundAnchor[0], y - selected.groundAnchor[1]) },
  ];
  objects.sort((a, b) => a.y - b.y).forEach(item => item.draw());
  if (grid.checked) {
    context.fillStyle = '#325e5966';
    for (let x = 0; x < 240; x += 16) context.fillRect(x, 0, 1, 160);
    for (let y = 0; y < 160; y += 16) context.fillRect(0, y, 240, 1);
  }
  document.querySelector('#description').textContent = `${selected.candidate} · ${selected.description}`;
  for (const button of document.querySelectorAll('.candidate'))
    button.setAttribute('aria-pressed', String(button.dataset.id === selected.id));
}

// Integer CSS scaling preserves equal-sized source pixels at every viewport.
const container = document.querySelector('#scene-container');
function resize() {
  const scale = Math.max(1, Math.floor(container.clientWidth / 240));
  canvas.style.width = `${240 * scale}px`;
  canvas.style.height = `${160 * scale}px`;
}
new ResizeObserver(resize).observe(container);
position.addEventListener('change', draw);
grid.addEventListener('change', draw);

try {
  atlas = await loadAtlas('../assets/review/integration-v1/atlas.json');
  const candidates = atlas.manifest.assets.filter(a => a.candidate);
  selected = candidates[0];
  for (const candidate of candidates) {
    const button = document.createElement('button');
    button.className = 'candidate';
    button.type = 'button';
    button.dataset.id = candidate.id;
    button.setAttribute('aria-label', `${candidate.candidate}: ${candidate.description}`);
    const preview = document.createElement('canvas');
    preview.width = 16;
    preview.height = 32;
    preview.setAttribute('aria-hidden', 'true');
    atlas.draw(preview.getContext('2d'), candidate.id, 0, 0);
    const label = document.createElement('span');
    label.textContent = candidate.candidate;
    button.append(preview, label);
    button.addEventListener('click', () => { selected = candidate; draw(); });
    document.querySelector('#candidates').append(button);
  }
  position.disabled = grid.disabled = false;
  draw();
  resize();
  status.textContent = 'One PNG loaded · 23 original asset entries · awaiting visual review';
  document.documentElement.dataset.artReady = 'true';
} catch (error) {
  status.className = 'error';
  status.textContent = `The art preview could not load. ${error.message} Reload to try again.`;
  document.querySelector('#description').textContent = 'Artwork unavailable.';
}
