// Tile coordinates refer to a character's feet. Scenes, scenery, and interaction
// data are separate from rendering so new areas do not need new engine code.
export const TILE = 24;
const door = (id, name, x, y, to, spawn) => ({
  id,
  name,
  x,
  y,
  type: "door",
  to,
  spawn,
});
const npc = (id, name, x, y, look = "adult") => ({
  id,
  name,
  x,
  y,
  type: "npc",
  look,
});
const item = (id, name, x, y, type = "inspect") => ({ id, name, x, y, type });
const furniture = (kind, x, y, w, h) => ({ kind, x, y, w, h });
export const buildings = [
  {
    x: 2,
    y: 2,
    w: 6,
    h: 5,
    name: "HOME",
    scene: "yard",
    color: "#cc8b66",
    roof: "#ad5e50",
  },
  {
    x: 12,
    y: 2,
    w: 6,
    h: 5,
    name: "KAID",
    scene: "kaidHome",
    color: "#e0c787",
    roof: "#69999e",
  },
  {
    x: 22,
    y: 2,
    w: 6,
    h: 5,
    name: "RIVAL",
    scene: "rivalHome",
    color: "#e0cfa1",
    roof: "#7c89aa",
  },
  {
    x: 2,
    y: 11,
    w: 6,
    h: 5,
    name: "CRITZ",
    scene: "critz",
    color: "#e1d4a5",
    roof: "#67905c",
  },
  {
    x: 12,
    y: 11,
    w: 6,
    h: 5,
    name: "VET",
    scene: "vet",
    color: "#d9ddbb",
    roof: "#619494",
  },
  {
    x: 22,
    y: 11,
    w: 6,
    h: 5,
    name: "DRUG STORE",
    scene: "pharmacy",
    color: "#d8cbaa",
    roof: "#ac7b90",
  },
  {
    x: 6,
    y: 20,
    w: 6,
    h: 5,
    name: "BIKE SHOP",
    scene: "bike",
    color: "#e9cd8c",
    roof: "#bd8758",
  },
  {
    x: 19,
    y: 20,
    w: 6,
    h: 5,
    name: "GLOW N’ BLOW",
    scene: "glass",
    color: "#dfc495",
    roof: "#6b8598",
  },
];
const shop = (name, keeper, look = "adult", style = "shop") => ({
  name,
  w: 16,
  h: 12,
  style,
  objects: [
    furniture("counter", 3, 4, 10, 1.4),
    furniture("shelf", 2, 2.6, 3, 1),
    furniture("shelf", 10, 2.6, 3, 1),
  ],
  entities: [
    npc(
      keeper,
      name === "Glow n’ Blow"
        ? "Aunt Ember"
        : name === "Vet"
          ? "Dr. Fern"
          : name === "Critz"
            ? "Juniper"
            : name === "Drug Store"
              ? "Mina"
              : "Ollie",
      8,
      5.6,
      look,
    ),
    door("exit", "Rootport", 8, 10.7, "town", [8, 9]),
  ],
});
export const scenes = {
  bedroom: {
    name: "Your bedroom",
    w: 16,
    h: 12,
    style: "bedroom",
    objects: [
      furniture("bed", 2, 3, 2, 3),
      furniture("desk", 11, 3, 3, 1.4),
      furniture("tank", 7, 3, 3, 1.5),
      furniture("fern", 2, 8, 1, 1),
      furniture("shelf", 1.3, 2.1, 3, 0.7),
    ],
    entities: [
      item("tank", "Little Root · 25 gal", 8.5, 4.9, "tank"),
      item("sleep", "Your bed", 3, 6.25, "bed"),
      item("desk", "Your sketchbook", 12, 4.6),
      item("gecko", "A rustle behind the fern", 3.2, 8.3, "rescue"),
      door("stairs", "Downstairs", 13.5, 10.7, "house", [13.5, 4.2]),
    ],
  },
  house: {
    name: "Home · downstairs",
    w: 16,
    h: 12,
    style: "house",
    objects: [
      furniture("sofa", 2, 4, 4, 1.7),
      furniture("table", 6, 7, 3, 1.7),
      furniture("shelf", 10, 3, 2, 1),
      furniture("kitchen", 2, 2.5, 5, 1),
    ],
    entities: [
      npc("mom", "Mom", 4.8, 6.4, "mom"),
      item("snail", "A tiny trail by the books", 10.7, 4.4, "rescue"),
      door("stairs", "Your bedroom", 13.5, 3.1, "bedroom", [13.5, 9.7]),
      door("exit", "The yard", 8, 10.7, "yard", [8, 4.6]),
    ],
  },
  yard: {
    name: "Home · the yard",
    w: 16,
    h: 12,
    style: "yard",
    objects: [
      furniture("log", 2.5, 6, 2, 0.8),
      furniture("leaves", 11, 7, 2, 1),
      furniture("planter", 11, 3, 2, 1),
    ],
    entities: [
      door("home", "Inside the house", 8, 3.2, "house", [8, 9.7]),
      door("gate", "Rootport", 8, 10.7, "town", [5, 8.2]),
      item("isopods", "Movement under the log", 4.7, 6.4, "rescue"),
      item("springtails", "Tiny specks in the leaves", 11, 8.3, "rescue"),
      item("forage", "Collect leaf litter", 13, 6, "forage"),
    ],
  },
  town: {
    name: "Rootport",
    w: 32,
    h: 27,
    style: "town",
    objects: [],
    entities: [
      ...buildings.map((b) =>
        door(
          b.scene,
          b.name,
          b.x + 3,
          b.y + 5.3,
          b.scene,
          b.scene === "yard" ? [8, 9.7] : [8, 9.5],
        ),
      ),
      npc("nugget", "Professor Nugget", 19.2, 16.9, "professor"),
      npc("rival", "Your rival", 24.4, 8.8, "rival"),
      npc("kaid", "Kaid", 11, 8.7, "kaid"),
      item("route", "Forest route · Liarsville", 30, 17, "route"),
      item("townSign", "Rootport directory", 8.4, 16.7, "directory"),
    ],
  },
  critz: shop("Critz", "shop-critz", "shopkeeper"),
  vet: shop("Vet", "shop-vet", "doctor"),
  pharmacy: shop("Drug Store", "shop-pharmacy", "doctor"),
  bike: shop("Bike Shop", "shop-bike", "shopkeeper"),
  glass: shop("Glow n’ Blow", "shop-glass", "glassblower"),
  kaidHome: {
    name: "Kaid’s home",
    w: 16,
    h: 12,
    style: "house",
    objects: [
      furniture("sofa", 2, 4, 4, 1.7),
      furniture("table", 8, 5, 3, 1.7),
      furniture("shelf", 10, 2.7, 3, 1),
    ],
    entities: [
      npc("kaid", "Kaid", 6, 7, "kaid"),
      door("exit", "Rootport", 8, 10.7, "town", [15, 8.2]),
    ],
  },
  rivalHome: {
    name: "Your rival’s home",
    w: 16,
    h: 12,
    style: "house",
    objects: [
      furniture("sofa", 2, 4, 4, 1.7),
      furniture("tank", 10, 3, 3, 1.5),
      furniture("table", 6, 7, 3, 1.7),
    ],
    entities: [
      npc("rivalMom", "Rival’s mom", 4, 6.5, "mom"),
      npc("rivalDad", "Rival’s dad", 11, 6.5, "adult"),
      door("exit", "Rootport", 8, 10.7, "town", [25, 8.2]),
    ],
  },
};
export function getEntities(s) {
  const list = scenes[s.scene].entities.filter(
    (e) =>
      e.type !== "rescue" ||
      (s.stage === "morning" && !s.flags.rescued.includes(e.id)),
  );
  if (s.scene === "bedroom" && s.stage === "night")
    return list.filter((e) => ["tank", "desk", "sleep"].includes(e.id));
  return list.map((e) =>
    e.id === "rival"
      ? { ...e, name: s.rival }
      : e.id === "tank" && s.stage === "night"
        ? { ...e, name: "Feed Pebble the gecko" }
        : e,
  );
}
export function nearestEntity(s) {
  let best = null,
    distance = 1.65;
  for (const e of getEntities(s)) {
    const d = Math.hypot(e.x - s.player.x, e.y - s.player.y);
    if (d < distance) {
      best = e;
      distance = d;
    }
  }
  return best;
}
export function isBlocked(sceneId, x, y) {
  const scene = scenes[sceneId];
  if (
    x < 0.8 ||
    y < (scene.style === "town" ? 1 : scene.style === "yard" ? 3.6 : 3) ||
    x > scene.w - 0.8 ||
    y > scene.h - 0.65
  )
    return true;
  const obstacles = scene.style === "town" ? buildings : scene.objects;
  return obstacles.some(
    (o) =>
      x > o.x - 0.2 &&
      x < o.x + o.w + 0.2 &&
      y > o.y - 0.15 &&
      y < o.y + o.h + 0.2,
  );
}
export function movePlayer(s, dx, dy, dt, run = false) {
  if (!dx && !dy) return false;
  const length = Math.hypot(dx, dy),
    speed = run ? 5.2 : 3.15;
  const mx = (dx / length) * speed * dt,
    my = (dy / length) * speed * dt;
  if (dx) s.player.facing = dx > 0 ? "right" : "left";
  else s.player.facing = dy > 0 ? "down" : "up";
  // Axis-separated collision allows sliding along furniture and door frames.
  if (!isBlocked(s.scene, s.player.x + mx, s.player.y)) s.player.x += mx;
  if (!isBlocked(s.scene, s.player.x, s.player.y + my)) s.player.y += my;
  return true;
}
export function transition(s, entity) {
  const previous = s.scene;
  s.scene = entity.to;
  s.player = { x: entity.spawn[0], y: entity.spawn[1], facing: "down" };
  if (s.scene === "town" && previous !== "yard") {
    const b = buildings.find((b) => b.scene === previous);
    if (b) {
      s.player.x = b.x + 3;
      s.player.y = b.y + 5.9;
    }
  }
  if (!s.flags.visited.includes(s.scene)) s.flags.visited.push(s.scene);
}
