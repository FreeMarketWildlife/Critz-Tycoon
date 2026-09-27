// Coordinates are integer grid cells at actors' feet, rendered at x*16,y*16.
// Appearance bounds never determine collision: every solid has an explicit
// half-open [x,y,width,height] cell rectangle independent of its PNG.
export const TILE = 16;
const door = (id, name, x, y, to, spawn) => ({ id, name, x, y, type: "door", to, spawn });
const npc = (id, name, x, y, look = "adult") => ({ id, name, x, y, type: "npc", look, collision: [x, y, 1, 1] });
const item = (id, name, x, y, type = "inspect") => ({ id, name, x, y, type });
const furniture = (kind, x, y, w, h, collision, sprite = `prop.${kind}`) => ({ kind, x, y, w, h, collision, sprite });
const tree = (x, y) => furniture("tree", x, y, 2, 2, [x + 1, y + 2, 1, 1], "tree.clustered");

export const buildings = [
  { x: 2, y: 2, w: 6, h: 5, name: "HOME", scene: "yard", color: "#cc8b66", roof: "#ad5e50" },
  { x: 12, y: 2, w: 6, h: 5, name: "KAID", scene: "kaidHome", color: "#e0c787", roof: "#69999e" },
  { x: 22, y: 2, w: 6, h: 5, name: "RIVAL", scene: "rivalHome", color: "#e0cfa1", roof: "#7c89aa" },
  { x: 2, y: 11, w: 6, h: 5, name: "CRITZ", scene: "critz", color: "#e1d4a5", roof: "#67905c" },
  { x: 12, y: 11, w: 6, h: 5, name: "VET", scene: "vet", color: "#d9ddbb", roof: "#619494" },
  { x: 22, y: 11, w: 6, h: 5, name: "DRUG STORE", scene: "pharmacy", color: "#d8cbaa", roof: "#ac7b90" },
  { x: 6, y: 20, w: 6, h: 5, name: "BIKE SHOP", scene: "bike", color: "#e9cd8c", roof: "#bd8758" },
  { x: 19, y: 20, w: 6, h: 5, name: "GLOW N’ BLOW", scene: "glass", color: "#dfc495", roof: "#6b8598" },
].map(building => ({ ...building, sprite: `building.${building.scene}`, collision: [building.x, building.y, building.w, building.h] }));

const shop = (name, keeper, look = "adult", style = "shop") => ({
  name, w: 16, h: 12, style, safeSpawn: [8, 9],
  objects: [
    furniture("counter", 3, 4, 10, 2, [3, 5, 10, 1]),
    furniture("shelf", 2, 2, 3, 2, [2, 3, 3, 1]),
    furniture("shelf", 10, 2, 3, 2, [10, 3, 3, 1]),
  ],
  entities: [
    npc(keeper, name === "Glow n’ Blow" ? "Aunt Ember" : name === "Vet" ? "Dr. Fern" : name === "Critz" ? "Juniper" : name === "Drug Store" ? "Mina" : "Ollie", 8, 6, look),
    door("exit", "Rootport", 8, 11, "town", [8, 9]),
  ],
});

export const scenes = {
  bedroom: {
    name: "Your bedroom", w: 16, h: 12, style: "bedroom", safeSpawn: [8, 7],
    objects: [
      furniture("bed", 2, 3, 2, 3, [2, 4, 2, 2]),
      furniture("desk", 11, 3, 3, 2, [11, 4, 3, 1]),
      furniture("tank", 7, 2, 3, 3, [7, 3, 3, 2]),
      furniture("fern", 2, 7, 1, 2, [2, 8, 1, 1]),
      furniture("shelf", 1, 1, 2, 2, [1, 2, 2, 1], "prop.shelf.small"),
    ],
    entities: [
      item("tank", "Little Root · 25 gal", 8, 5, "tank"),
      item("sleep", "Your bed", 3, 6, "bed"),
      item("desk", "Your sketchbook", 12, 5),
      item("gecko", "A rustle behind the fern", 3, 8, "rescue"),
      door("stairs", "Downstairs", 14, 11, "house", [14, 4]),
    ],
  },
  house: {
    name: "Home · downstairs", w: 16, h: 12, style: "house", safeSpawn: [8, 10],
    objects: [
      furniture("sofa", 2, 4, 4, 2, [2, 5, 4, 1]),
      furniture("table", 6, 7, 3, 2, [6, 8, 3, 1]),
      furniture("shelf", 10, 2, 2, 2, [10, 3, 2, 1], "prop.shelf.small"),
      furniture("kitchen", 2, 2, 5, 2, [2, 3, 5, 1]),
    ],
    entities: [
      npc("mom", "Mom", 5, 6, "mom"),
      item("snail", "A tiny trail by the books", 11, 4, "rescue"),
      door("stairs", "Your bedroom", 14, 3, "bedroom", [14, 10]),
      door("exit", "The yard", 8, 11, "yard", [8, 4]),
    ],
  },
  yard: {
    name: "Home · the yard", w: 16, h: 12, style: "yard", safeSpawn: [8, 9],
    // The house sits outside the walkable yard. Its door is one cell north of
    // the first walkable row, reachable by interacting from (8,4).
    visualHouse: { x: 5, y: -2, w: 6, h: 5, sprite: "building.yard" },
    objects: [
      furniture("log", 3, 6, 2, 1, [3, 6, 2, 1]),
      furniture("leaves", 11, 7, 2, 1, null),
      furniture("planter", 11, 2, 2, 2, [11, 3, 2, 1]),
      tree(1, 3), tree(13, 3),
    ],
    entities: [
      door("home", "Inside the house", 8, 3, "house", [8, 10]),
      door("gate", "Rootport", 8, 11, "town", [5, 8]),
      item("isopods", "Movement under the log", 5, 6, "rescue"),
      item("springtails", "Tiny specks in the leaves", 11, 8, "rescue"),
      item("forage", "Collect leaf litter", 13, 6, "forage"),
    ],
  },
  town: {
    name: "Rootport", w: 32, h: 27, style: "town", safeSpawn: [16, 9],
    objects: [
      tree(9, 4), tree(19, 4), tree(1, 8), tree(10, 13),
      tree(20, 13), tree(2, 19), tree(15, 21),
      furniture("pond", 28, 11, 3, 3, [28, 11, 3, 3], "ground.water"),
    ],
    entities: [
      ...buildings.map(building => door(building.scene, building.name, building.x + 3, building.y + 5, building.scene, [8, 10])),
      npc("nugget", "Professor Nugget", 19, 17, "professor"),
      npc("rival", "Your rival", 24, 9, "rival"),
      npc("kaid", "Kaid", 11, 9, "kaid"),
      item("route", "Forest route · Liarsville", 30, 17, "route"),
      item("townSign", "Rootport directory", 8, 17, "directory"),
    ],
  },
  critz: shop("Critz", "shop-critz", "shopkeeper"),
  vet: shop("Vet", "shop-vet", "doctor"),
  pharmacy: shop("Drug Store", "shop-pharmacy", "doctor"),
  bike: shop("Bike Shop", "shop-bike", "shopkeeper"),
  glass: shop("Glow n’ Blow", "shop-glass", "glassblower"),
  kaidHome: {
    name: "Kaid’s home", w: 16, h: 12, style: "house", safeSpawn: [8, 10],
    objects: [
      furniture("sofa", 2, 4, 4, 2, [2, 5, 4, 1]),
      furniture("table", 8, 5, 3, 2, [8, 6, 3, 1]),
      furniture("shelf", 10, 2, 3, 2, [10, 3, 3, 1]),
    ],
    entities: [npc("kaid", "Kaid", 6, 7, "kaid"), door("exit", "Rootport", 8, 11, "town", [15, 8])],
  },
  rivalHome: {
    name: "Your rival’s home", w: 16, h: 12, style: "house", safeSpawn: [8, 10],
    objects: [
      furniture("sofa", 2, 4, 4, 2, [2, 5, 4, 1]),
      furniture("tank", 10, 2, 3, 3, [10, 3, 3, 2]),
      furniture("table", 6, 7, 3, 2, [6, 8, 3, 1]),
    ],
    entities: [
      npc("rivalMom", "Rival’s mom", 4, 7, "mom"),
      npc("rivalDad", "Rival’s dad", 11, 7, "adult"),
      door("exit", "Rootport", 8, 11, "town", [25, 8]),
    ],
  },
};

export function getEntities(state) {
  const list = scenes[state.scene].entities.filter(entity => entity.type !== "rescue" || (state.stage === "morning" && !state.flags.rescued.includes(entity.id)));
  const visible = state.scene === "bedroom" && state.stage === "night" ? list.filter(entity => ["tank", "desk", "sleep"].includes(entity.id)) : list;
  return visible.map(entity => entity.id === "rival" ? { ...entity, name: state.rival } : entity.id === "tank" && state.stage === "night" ? { ...entity, name: "Feed Pebble the gecko" } : entity);
}

// A acts on the current/adjacent cardinal cell; it cannot reach diagonally
// through a furniture corner. Facing breaks ties without hiding nearby actions.
export function nearestEntity(state) {
  const facing = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] }[state.player.facing] || [0, 0];
  let best = null, rank = Infinity;
  for (const entity of getEntities(state)) {
    const dx = entity.x - state.player.x, dy = entity.y - state.player.y;
    const distance = Math.abs(dx) + Math.abs(dy);
    if (distance > 1) continue;
    const score = distance - (dx === facing[0] && dy === facing[1] ? 0.25 : 0);
    if (score < rank) { best = entity; rank = score; }
  }
  return best;
}

const contains = (rect, x, y) => rect && x >= rect[0] && y >= rect[1] && x < rect[0] + rect[2] && y < rect[1] + rect[3];
export function isBlocked(sceneId, x, y, state) {
  const scene = scenes[sceneId];
  if (!scene || !Number.isInteger(x) || !Number.isInteger(y)) return true;
  const top = scene.style === "town" ? 1 : scene.style === "yard" ? 4 : 3;
  if (x < 1 || x >= scene.w || y < top || y >= scene.h) return true;
  if (scene.objects.some(object => contains(object.collision, x, y))) return true;
  if (scene.style === "town" && buildings.some(building => contains(building.collision, x, y))) return true;
  return !!state && getEntities({ ...state, scene: sceneId }).some(entity => entity.type === "npc" && contains(entity.collision, x, y));
}

// Recover only to the connected floor region containing the authored safe
// spawn. Scanning an arbitrary nearby free tile could strand a player behind
// new furniture. Selection is deterministic; no timers, I/O or story mutation.
export function safeGridPosition(sceneId, x, y, state) {
  const scene = scenes[sceneId];
  if (!scene) throw new RangeError(`Unknown scene: ${sceneId}`);
  const [sx, sy] = scene.safeSpawn;
  if (isBlocked(sceneId, sx, sy, state)) throw new Error(`Blocked safe spawn: ${sceneId}`);
  const targetX = Number.isFinite(x) ? x : sx, targetY = Number.isFinite(y) ? y : sy;
  const queue = [[sx, sy]], visited = new Set([`${sx},${sy}`]);
  let best = { x: sx, y: sy }, distance = Infinity;
  for (let i = 0; i < queue.length; i++) {
    const [cx, cy] = queue[i];
    const d = (cx - targetX) ** 2 + (cy - targetY) ** 2;
    if (d < distance || (d === distance && (cy < best.y || (cy === best.y && cx < best.x)))) { best = { x: cx, y: cy }; distance = d; }
    for (const [dx, dy] of [[0, -1], [-1, 0], [1, 0], [0, 1]]) {
      const nx = cx + dx, ny = cy + dy, key = `${nx},${ny}`;
      if (!visited.has(key) && !isBlocked(sceneId, nx, ny, state)) { visited.add(key); queue.push([nx, ny]); }
    }
  }
  return best;
}

export function transition(state, entity) {
  if (entity.type !== "door" || !scenes[entity.to]) throw new Error("Invalid scene transition.");
  const previous = state.scene;
  state.scene = entity.to;
  let [x, y] = entity.spawn;
  // Every Rootport exterior has one explicit centered threshold. Returning
  // from any shop/home places the player one cell below that same threshold.
  if (state.scene === "town") {
    const building = buildings.find(candidate => candidate.scene === previous);
    if (building) { x = building.x + 3; y = building.y + 6; }
  }
  state.player = { ...state.player, ...safeGridPosition(state.scene, x, y, state), facing: "down" };
  if (!state.flags.visited.includes(state.scene)) state.flags.visited.push(state.scene);
}
