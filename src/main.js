import {
  createState,
  startMorning,
  rescue,
  rescueInfo,
  manage,
  tick,
  scorePost,
  publish,
  save,
  load,
  spend,
  dollars,
  conditions,
  objective,
  HOUR_SECONDS,
} from "./state.js";
import {
  scenes,
  getEntities,
  nearestEntity,
  movePlayer,
  transition,
  isBlocked,
} from "./world.js";
import { renderWorld, renderTank, character } from "./art.js";
const $ = (id) => document.getElementById(id);
const esc = (s) =>
  String(s).replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
let loaded = load(),
  state = loaded.state || createState(),
  panelName = "",
  dialogue = null,
  dialogueDone = null;
let gender = "boy",
  running = false,
  moving = false,
  transitioning = false,
  simAccumulator = 0,
  lastTime = performance.now(),
  visualTime = 0,
  toastTimer,
  sceneTimer,
  capture = null,
  recording = 0;
let camera = { kind: "photo", frame: 50, zoom: 1 },
  down = new Set(),
  lastSaved = 0;
const canvas = $("world"),
  panel = $("panel"),
  overlay = $("overlay");
const button = (action, label, cls = "primary full", extra = "") =>
  `<button class="${cls}" data-action="${action}" ${extra}>${label}</button>`;
function toast(message) {
  if (!message) return;
  clearTimeout(toastTimer);
  $("toast").textContent = message;
  $("toast").hidden = false;
  toastTimer = setTimeout(() => ($("toast").hidden = true), 3400);
}
function persist(quiet = true) {
  const ok = save(state);
  if (!ok)
    toast(
      "Could not save on this browser. Free storage or enable local storage.",
    );
  else if (!quiet) toast("Progress saved on this device.");
  return ok;
}
function hud() {
  $("location").textContent =
    state.scene === "bedroom"
      ? `${state.hero}’s room`
      : scenes[state.scene].name;
  $("clock").textContent =
    state.stage === "night"
      ? "NIGHT 01"
      : `DAY ${Math.floor(state.time / 24) + 1} · ${String(state.time % 24).padStart(2, "0")}:00`;
  $("money").textContent = dollars(state.money);
  $("quest").textContent = objective(state);
}
function fitOverlay() {
  const controls = $("controller").getBoundingClientRect();
  if (innerWidth > innerHeight && innerHeight < 600) {
    overlay.style.bottom = "0px";
    overlay.style.right = `${Math.max(202, innerWidth - controls.left + 6)}px`;
  } else {
    overlay.style.right = "0px";
    overlay.style.bottom = `${Math.max(8, innerHeight - controls.top + 3)}px`;
  }
}
function showPanel(
  name,
  title,
  html,
  { back = true, eyebrow = "", keep = false } = {},
) {
  if (name !== "view") recording = 0;
  const scroll = keep ? panel.scrollTop : 0;
  panelName = name;
  down.clear();
  overlay.hidden = false;
  fitOverlay();
  panel.innerHTML = `${eyebrow ? `<div class="eyebrow">${eyebrow}</div>` : ""}<div class="panel-heading"><h2 id="panel-title">${title}</h2>${back ? button("back", "×", "close", 'aria-label="Close or go back"') : ""}</div>${html}`;
  panel.scrollTop = scroll;
  requestAnimationFrame(() => {
    const first = panel.querySelector("input,button:not(.close)");
    if (first && !keep) first.focus({ preventScroll: true });
  });
}
function closePanel() {
  panelName = "";
  overlay.hidden = true;
  down.clear();
  recording = 0;
  capture = null;
  hud();
}
function titleScreen() {
  showPanel(
    "title",
    "A little world, alive.",
    `<p>Some beginnings are small enough to fit in a glass tank.</p><canvas id="welcome-tank" class="welcome-art" width="400" height="148"></canvas>${loaded.state ? button("continue", `Continue ${esc(loaded.state.hero)}’s story`) : ""}${button("new", loaded.state ? "Start a new story" : "Begin your story", loaded.state ? "secondary full" : "primary full")}<p class="hint">A cozy ecosystem RPG · original playable chapter<br>Touch controls or keyboard. Progress stays on this browser.</p>${loaded.recovered ? '<div class="notice">Your previous backup was recovered. You can continue safely.</div>' : ""}${loaded.damaged ? '<div class="notice">The saved file could not be read. Start a new story to recover.</div>' : ""}`,
    { back: false, eyebrow: "CRITZ: TYCOON / CHAPTER 01" },
  );
}
function setup() {
  gender = "boy";
  showPanel(
    "setup",
    "Who’s moving in?",
    `<p>You’re ten. You love tiny creatures. This is your story.</p><div class="choices"><button class="choice selected" data-action="boy" aria-pressed="true"><canvas id="boy-preview" class="hero-preview" width="22" height="29"></canvas>Boy</button><button class="choice" data-action="girl" aria-pressed="false"><canvas id="girl-preview" class="hero-preview" width="22" height="29"></canvas>Girl</button></div><label class="field-label" for="hero-name">Your name</label><input id="hero-name" type="text" placeholder="e.g. Ari" maxlength="16" autocomplete="off"><label class="field-label" for="rival-name">Your rival’s name <span id="rival-gender">(girl)</span></label><input id="rival-name" type="text" placeholder="e.g. Rowan" maxlength="16" autocomplete="off">${button("begin", "Let’s go to Rootport →")}<p class="hint">Opening: a difficult night at home. Every animal survives.</p>`,
    { back: false, eyebrow: "A NEW BEGINNING" },
  );
  for (const g of ["boy", "girl"]) {
    const c = $(g + "-preview").getContext("2d");
    character(c, 11, 26, { gender: g });
  }
}
function say(lines, done) {
  down.clear();
  dialogue = lines.map((l) => (typeof l === "string" ? ["", l] : l));
  dialogueDone = done;
  nextDialogue();
}
function nextDialogue() {
  if (!dialogue) return;
  if (!dialogue.length) {
    dialogue = null;
    $("dialogue").hidden = true;
    const cb = dialogueDone;
    dialogueDone = null;
    if (cb) cb();
    return;
  }
  const [speaker, body, beat] = dialogue.shift();
  if (beat) state.storyBeat = beat;
  $("speaker").textContent = speaker || "ROOTPORT";
  $("dialogue-text").textContent = body;
  $("dialogue").hidden = false;
  $("interact-prompt").hidden = true;
}
function opening() {
  say([
    [state.hero, "Just one more cricket, Pebble. Then we both have to sleep."],
    ["", "Walk with the D-pad. Press A when you’re near Pebble’s tank."],
  ]);
}
function openingIncident() {
  say(
    [
      [state.hero, "There you go. The mighty hunter strikes again.", "feeding"],
      [
        "Mom",
        `${state.hero}? I… I can’t get everything to quiet down tonight.`,
        "mom",
      ],
      [state.hero, "Mom? Please be careful—"],
      [
        "",
        "Mom bursts into the room. In the middle of her distress, she knocks the tanks from their stands.",
        "broken",
      ],
      [
        "",
        "Glass scatters. Tiny feet dart for cover. Every animal gets away safely.",
      ],
      [
        "Mom",
        "Oh, sweetheart. I’m so sorry. Step back from the glass. I’ll clean it up.",
      ],
      [state.hero, "I know you didn’t want this. I just… need to find them."],
      ["Kaid", "I heard the crash. What happened? Are you okay?", "kaid"],
      [state.hero, "I am. The tanks aren’t. Everybody’s hiding somewhere."],
      [
        "Kaid",
        "Then we’ll find everybody. First: early birthday delivery! Twenty-five gallons of possibilities.",
      ],
      [
        "Kaid",
        "Aunt Ember made the glass at Glow n’ Blow. I picked the corners. Rounded. Very important.",
      ],
      [
        "Kaid",
        "I can also lend you $100 from my savings. No interest. You decide when to pay it back.",
      ],
    ],
    () => loan(),
  );
}
function loan() {
  showPanel(
    "loan",
    "A little help from Kaid",
    `<p>The <b>25-gallon tank is a gift</b> either way. You have ${dollars(state.money)} and a small starter kit.</p><div class="notice">“Friends don’t come with repayment timers.” — Kaid</div>${button("accept-loan", "Accept the $100 loan")}${button("decline-loan", "Decline · start with $12", "secondary full")}<p class="hint">Optional, interest-free. Repay any time you can afford it. Declining means a slower start.</p>`,
    { back: false, eyebrow: "AN EARLY BIRTHDAY PRESENT" },
  );
}
function finishNight(accept) {
  startMorning(state, accept);
  delete state.storyBeat;
  closePanel();
  persist();
  hud();
  say(
    [
      [
        "",
        "Later, the glass is cleared away. Kaid’s new tank rests safely on its stand. The house grows quiet.",
      ],
      ["", "The next morning…"],
      [
        "Mom",
        "I’m sorry about last night. I love you. I’m getting help, and I’ll help with the search.",
      ],
      [
        "Kaid",
        "Look behind the fern, by the books, and out in the yard. I saw something tiny under that old log.",
      ],
      [
        "",
        "Your starter kit has moss and leaf litter. Tap Start for the notebook, town guide, and saving.",
      ],
    ],
    () => announce("A new morning · Rootport"),
  );
}
function announce(label) {
  clearTimeout(sceneTimer);
  $("scene-label").textContent = label;
  $("scene-label").classList.add("visible");
  sceneTimer = setTimeout(
    () => $("scene-label").classList.remove("visible"),
    2400,
  );
}
function travel(entity) {
  if (transitioning) return;
  transitioning = true;
  down.clear();
  $("fade").classList.add("on");
  setTimeout(() => {
    transition(state, entity);
    hud();
    persist();
    announce(scenes[state.scene].name);
    $("fade").classList.remove("on");
    transitioning = false;
  }, 160);
}
function interact() {
  if (transitioning) return;
  if (dialogue) {
    nextDialogue();
    return;
  }
  if (panelName) {
    confirmPanel();
    return;
  }
  const e = nearestEntity(state);
  if (!e) {
    toast("Walk closer to a person, doorway, or sparkling hiding spot.");
    return;
  }
  if (e.type === "door") {
    travel(e);
    return;
  }
  if (e.type === "rescue") {
    if (rescue(state, e.id)) {
      const isSmall = ["isopods", "springtails"].includes(e.id);
      say(
        [
          [state.hero, `Found you! ${rescueInfo[e.id].name} — safe and sound.`],
          [
            "",
            isSmall
              ? "You settle them into Little Root’s damp leaf litter. They begin exploring their new home."
              : "Mom calls the Vet. A safe temporary care box is ready; you can visit any time.",
          ],
          [
            "",
            `${state.flags.rescued.length} of 4 animal groups are safe.${state.flags.rescued.length === 4 ? " Professor Nugget should hear the good news." : ""}`,
          ],
        ],
        () => {
          persist();
          hud();
        },
      );
    }
    return;
  }
  switch (e.id) {
    case "tank":
      state.stage === "night" ? openingIncident() : tankMenu();
      break;
    case "sleep":
      state.stage === "night"
        ? say([[state.hero, "Pebble gets dinner first."]])
        : showPanel(
            "sleep",
            "Rest for a while?",
            `<p>Advance 8 habitat hours. Your animals keep living while you rest. Check food and moisture first.</p>${button("rest", "Rest · 8 hours")}${button("back", "Stay awake", "secondary full")}`,
          );
      break;
    case "desk":
      notebook();
      break;
    case "mom": {
      const lines = [
        [
          "Mom",
          `Morning, ${state.hero}. Whatever today brings, I’m glad we get to start it together.`,
        ],
      ];
      if (state.inventory.medicine) {
        state.inventory.medicine--;
        state.flags.medicineDelivered = true;
        lines.push([
          "Mom",
          "Thank you for picking up my prescription. The pharmacist and I have a plan. You don’t have to manage this alone.",
        ]);
        persist();
      } else
        lines.push([
          "Mom",
          "I’m arranging support for my treatment. In this chapter, there’s no weekly prescription deadline. Go enjoy your little world.",
        ]);
      say(lines);
      break;
    }
    case "nugget":
      meetNugget();
      break;
    case "kaid":
      kaidMenu();
      break;
    case "rival":
      state.flags.metRival = true;
      persist();
      say([
        [
          state.rival,
          "I spent all morning getting the perfect reflection in my tank photo. All morning!",
        ],
        [state.hero, "Did the animals mind?"],
        [
          state.rival,
          "They kept moving. Which… actually made the video better.",
        ],
        [
          state.rival,
          "Mom and Dad helped set up my lights. Come over sometime. And post something — I want to see your tank.",
        ],
      ]);
      break;
    case "rivalMom":
      say([
        [
          "Rival’s mom",
          `${state.rival} is out comparing camera angles again. We help with the tanks, but the patience is all theirs.`,
        ],
      ]);
      break;
    case "rivalDad":
      say([
        [
          "Rival’s dad",
          "A stable stand and a good routine. Those are my contributions. The tiny jungle is our kid’s work.",
        ],
      ]);
      break;
    case "forage":
      if (state.time - (state.flags.lastForage ?? -10) < 6) {
        toast(
          "Let the yard rest. More litter will be ready in 6 habitat hours.",
        );
      } else {
        state.inventory.litter += 2;
        state.flags.lastForage = state.time;
        persist();
        toast("Collected 2 portions of clean leaf litter.");
      }
      break;
    case "route":
      say([
        [
          "Forest route",
          "The path to Liarsville runs beyond these trees. This first chapter stays in Rootport.",
        ],
        [
          state.hero,
          "A whole route of little lives to discover. Someday soon.",
        ],
      ]);
      break;
    case "townSign":
      directory();
      break;
    default:
      if (e.id.startsWith("shop-")) shop(e.id.slice(5));
  }
}
function meetNugget() {
  if (!state.flags.notebook) {
    state.flags.notebook = true;
    state.notebookEntries.push(
      "Professor Nugget gave you a field notebook. Observe first; change one thing at a time.",
    );
    persist();
    say(
      [
        [
          "Professor Nugget",
          "There you are! I’m Nugget. Herpetologist, notebook enthusiast, occasional misplaced-pencil detective.",
        ],
        [
          "Professor Nugget",
          "This notebook is yours. Sketch what you notice. Animals tell us what they need, if we learn to look.",
        ],
        [
          "Professor Nugget",
          "A gecko needs much more than a sealed jar. For your first living system, start with moss and little decomposers.",
        ],
        [
          "",
          "Field notebook received. Open it with Start or the notebook button.",
        ],
      ],
      () => {
        if (state.flags.rescued.length === 4) meetNugget();
      },
    );
    return;
  }
  if (state.flags.rescued.length === 4 && !state.flags.questReward) {
    state.flags.questReward = true;
    state.money += 1500;
    persist();
    say(
      [
        [
          "Professor Nugget",
          "All four accounted for! Careful observation paid off.",
        ],
        [
          "Professor Nugget",
          "Here’s $15 from our community habitat fund. Put it toward their new beginning.",
        ],
        [
          "",
          "Search completed · $15 earned. Pebble and Button are safe at the Vet.",
        ],
      ],
      hud,
    );
    return;
  }
  say([
    [
      "Professor Nugget",
      state.flags.rescued.length < 4
        ? "Check the bedroom fern, the downstairs bookshelf, the yard log, and the leaf pile. They’re hiding, not lost."
        : "Change one thing at a time. Then observe for a few hours. Your notebook is a better tool than a guess.",
    ],
  ]);
}
function kaidMenu() {
  showPanel(
    "kaid",
    "Kaid",
    `<p>“Aunt Ember handles all the hot glass. I draw tank ideas, decorate cool glass, and sweep up. Official corner inspector.”</p><div class="notice">${state.debt ? `Your loan: ${dollars(state.debt)} · no interest or deadline.` : "No outstanding loan. “You bring the ideas. I’ll bring the snacks.”"}</div>${state.debt ? button("repay", `Repay ${dollars(state.debt)}`, "primary full", state.money < state.debt ? "disabled" : "") : ""}${button("back", "See you around", "secondary full")}`,
  );
}
function tankMenu() {
  showPanel(
    "tank",
    "Little Root",
    `<canvas id="tank-preview" class="tank-canvas" width="400" height="200"></canvas><p class="hint">25-gallon ventilated terrarium · a gift from Kaid</p><div class="menu-list">${menuRow("manage", "⌘", "Manage", "Shape the habitat. Care for its little residents.")}${menuRow("stats", "▥", "Stats", "Conditions, populations, and changes over time.")}${menuRow("view", "◉", "View", "Watch closely. Frame a moment. Share it on Critter.")}</div>`,
    { eyebrow: "YOUR FIRST LIVING WORLD" },
  );
}
function menuRow(action, icon, title, desc) {
  return `<button class="menu-row" data-action="${action}"><span class="menu-icon">${icon}</span><span><strong>${title}</strong><small>${desc}</small></span><span class="chevron">›</span></button>`;
}
function supply(label, desc, action, price, disabled = false) {
  return `<div class="supply-row"><div><strong>${label}</strong><small>${desc}</small></div>${button(action, price, "", disabled ? "disabled" : "")}</div>`;
}
function managePanel(keep = false) {
  const t = state.tank;
  showPanel(
    "manage",
    "A habitat in your hands",
    `<canvas id="tank-preview" class="tank-canvas" width="400" height="200"></canvas><div class="stat-grid"><div class="stat"><label>Substrate moisture</label><strong data-live="moisture">${t.moisture}%</strong><small>Aim for 55–80% in this model</small></div><div class="stat"><label>Leaf litter remaining</label><strong data-live="food">${t.food}%</strong><small>Keep above 8% for breeding</small></div></div><div class="setting"><div class="setting-header">Daily light <span>${t.light} h</span></div><p>Long days encourage algae. Eight hours is a useful starting point.</p><div class="segments">${[4, 8, 12].map((n) => button("light", `${n} hours`, n === t.light ? "selected" : "", `data-value="${n}" aria-pressed="${n === t.light}"`)).join("")}</div></div><div class="setting"><div class="setting-header">Ventilation</div><p>More fresh air dries substrate faster. A low vent setting can limit activity.</p><div class="segments">${["Low", "Balanced", "Open"].map((n, i) => button("ventilation", n, t.ventilation === i + 1 ? "selected" : "", `data-value="${i + 1}" aria-pressed="${t.ventilation === i + 1}"`)).join("")}</div></div>${supply("Mist the substrate", "+14 moisture · clean water", "mist", "Free")}${supply("Plant moss", `${t.plants}/6 planted · ${state.inventory.moss} in your kit`, "moss", "Plant", state.inventory.moss < 1 || t.plants >= 6)}${supply("Add leaf litter", `+25 food · ${state.inventory.litter} portions in your kit`, "feed", "Feed", state.inventory.litter < 1)}${supply("Clean glass & excess waste", "Less algae and waste; a few microbes are removed", "clean", "Clean")}${button("observe", "Observe · 1 habitat hour", "secondary full")}<p class="hint">One habitat hour passes every 8 seconds while playing. Time pauses in dialogue and the pause menu. This is a simplified learning model.</p>`,
    { keep },
  );
}
function stat(label, value, hint = "", live = "") {
  return `<div class="stat"><label>${label}</label><strong ${live ? `data-live="${live}"` : ""}>${value}</strong>${hint ? `<small>${hint}</small>` : ""}</div>`;
}
function statsPanel(keep = false) {
  const t = state.tank,
    c = conditions(t),
    old = t.history.at(-7);
  showPanel(
    "stats",
    "Life, by the numbers",
    `<span class="badge">LITTLE ROOT · HOUR <span data-live="hours">${t.hours}</span></span><div class="stat-grid">${stat("Isopods", t.isopods, "Leaf-litter recyclers", "isopods")}${stat("Springtails", t.springtails, "Tiny decomposers", "springtails")}${stat("Moss plantings", t.plants + "/6", "Shelter and moisture retention")}${stat("Daily light", t.light + " hours", "Ventilation: " + ["Low", "Balanced", "Open"][t.ventilation - 1])}${stat("Moisture", t.moisture + "%", "Target 55–80%", "moisture")}${stat("Leaf litter", t.food + "%", "Breeding needs at least 8%", "food")}${stat("Waste", t.waste + "%", "Microbes and springtails reduce it", "waste")}${stat("Nutrients", t.nutrients + "%", "Decomposition adds; plants use", "nutrients")}${stat("Microbe index", t.microbes, "Simplified activity index, not a count", "microbes")}${stat("Algae cover", t.algae + "%", "Light and dampness encourage it", "algae")}${stat("Births", t.births, "Over the life of this habitat", "births")}${stat("Deaths", 0, "Nonlethal learning mode in this slice")}</div><div class="notice">Activity: <b data-live="activity">${c.activity}/100</b>. Poor conditions slow animals and pause breeding. No animal deaths are simulated in this chapter.</div><h3>Recent trend</h3><p id="trend">${old ? `Over the last ${t.hours - old.hour} hours: moisture ${Math.round(t.moisture - old.moisture)} points, population ${t.isopods + t.springtails - old.population >= 0 ? "+" : ""}${t.isopods + t.springtails - old.population}.` : "Observe for a few hours to build a trend."}</p><h3>Habitat journal</h3><div id="habitat-events">${t.events.map((e) => `<div class="journal-entry"><p>${esc(e)}</p></div>`).join("")}</div>${button("observe", "Observe · 1 habitat hour", "secondary full")}`,
    { keep },
  );
}
function viewPanel() {
  capture = null;
  recording = 0;
  showPanel(
    "view",
    "Find a little wonder",
    `<canvas id="view-canvas" class="tank-canvas" width="400" height="200"></canvas><p class="hint">Frame the moss and moving animals. Your choices affect composition.</p><div class="segments">${button("photo-mode", "Photo", camera.kind === "photo" ? "selected" : "")}${button("video-mode", "6-second simulated video", camera.kind === "video" ? "selected" : "")}</div><label class="field-label" for="frame">Pan the frame</label><input type="range" id="frame" min="0" max="100" value="${camera.frame}"><label class="field-label" for="zoom">Zoom</label><input type="range" id="zoom" min="100" max="160" value="${camera.zoom * 100}"><div id="camera-scores"></div>${button("capture", camera.kind === "photo" ? "◉ Take photo" : "● Record simulated video")}<p class="hint">Photos become in-game snapshots. Videos are simulated Critter clips; no real video file is recorded.</p>`,
    { eyebrow: "VIEW / CRITTER CAMERA" },
  );
  cameraScores();
}
function cameraScores() {
  const box = $("camera-scores");
  if (box) {
    const sc = scorePost(state, camera);
    box.innerHTML = `<div class="score-row"><span>Composition</span><b>${sc.composition}/100</b></div><div class="score-row"><span>Animal activity</span><b>${sc.activity}/100</b></div>`;
  }
}
function takeCapture() {
  const temp = document.createElement("canvas");
  temp.width = 400;
  temp.height = 200;
  renderTank(temp, state.tank, visualTime, camera);
  capture = { ...camera, image: temp.toDataURL("image/png") };
  const sc = scorePost(state, capture);
  showPanel(
    "capture",
    "A moment worth sharing",
    `<img class="tank-canvas" src="${capture.image}" alt="Your framed terrarium snapshot"><p>${capture.kind === "video" ? "6-second simulated tank clip" : "Tank photograph"} · Little Root</p>${scoreRows(sc)}<div class="notice">Estimated reach: <b>${sc.targetViews.toLocaleString()} views</b> over 4 habitat hours. Game ad rate: $1.20 per 1,000 views.</div>${button("publish", "Post to Critter")}${button("retake", "Reframe this moment", "secondary full")}<p class="hint">Score weights: activity 25%, composition 20%, appearance 25%, rarity 10%, audience interest 20%. Videos add 15% reach.</p>`,
    { eyebrow: "CRITTER / POST PREVIEW" },
  );
}
function scoreRows(sc) {
  return [
    ["activity", "Animal activity"],
    ["composition", "Composition"],
    ["appearance", "Tank appearance"],
    ["rarity", "Species rarity"],
    ["interest", "Audience interest"],
  ]
    .map(
      ([k, n]) =>
        `<div class="score-row"><span>${n}</span><b>${sc[k]}/100</b></div>`,
    )
    .join("");
}
function critterPanel(keep = false) {
  showPanel(
    "critter",
    "Your corner of Critter",
    `<div class="notice">Lifetime ad earnings: <b>${dollars(state.lifetimeEarned)}</b><br>Reach grows over 4 habitat hours. Posting the same tank within 6 hours lowers audience interest.</div>${state.posts.length ? state.posts.map((p) => `<article class="post"><div class="post-header"><b>@${esc(state.hero)} · Little Root</b><span>${p.kind === "video" ? "SIMULATED VIDEO" : "PHOTO"}</span></div><img src="${p.image.startsWith("data:image/png;base64,") ? p.image : ""}" alt="Saved tank snapshot"><div class="post-numbers"><span><b>${p.views.toLocaleString()}</b>views</span><span><b>${p.likes}</b>likes · ${p.comments} replies</span><span><b>${dollars(p.revenue)}</b>earned</span></div><p class="hint">${p.age < 4 ? "Finding its audience…" : "Reach complete"} · ${p.engagement}% engagement · score ${p.scores?.total ?? "—"}/100</p></article>`).join("") : "<p>Your first post is waiting to happen. Go to your bedroom tank and choose View.</p>"}${state.posts.length ? button("observe", "Let an hour pass", "secondary full") : ""}`,
    { eyebrow: "SMALL WORLDS. SHARED.", keep },
  );
}
function refreshLive() {
  for (const el of panel.querySelectorAll("[data-live]")) {
    const key = el.dataset.live;
    el.textContent =
      key === "activity"
        ? `${conditions(state.tank).activity}/100`
        : state.tank[key] +
          (["moisture", "food", "waste", "nutrients", "algae"].includes(key)
            ? "%"
            : "");
  }
  cameraScores();
  if (panelName === "stats") {
    $("habitat-events").innerHTML = state.tank.events
      .map((e) => `<div class="journal-entry"><p>${esc(e)}</p></div>`)
      .join("");
    const old = state.tank.history.at(-7),
      t = state.tank;
    if (old)
      $("trend").textContent =
        `Over ${t.hours - old.hour} hours: moisture ${Math.round(t.moisture - old.moisture)} points; population ${t.isopods + t.springtails - old.population >= 0 ? "+" : ""}${t.isopods + t.springtails - old.population}.`;
  }
}
function shop(type) {
  if (type === "critz")
    showPanel(
      "shop-critz",
      "Critz",
      `<p>Juniper: “Start with good habitat. The animals will tell you the rest.”</p><span class="badge">YOUR POCKET · ${dollars(state.money)}</span>${supply("Moss cutting", "Adds shelter and holds moisture", "buy-moss", "$3", state.money < 300)}${supply("Leaf litter · 3 portions", "Food for isopods and springtails", "buy-litter", "$1.50", state.money < 150)}${!state.flags.supplyGift ? button("supply-gift", "Collect a free welcome kit", "secondary full") : ""}<p class="hint">Live animal sales and additional habitat types arrive in future chapters.</p>`,
      { eyebrow: "PET SHOP / JUNIPER" },
    );
  if (type === "vet")
    showPanel(
      "shop-vet",
      "Small patients, big care",
      `<p>Dr. Fern: “Every escapee is safe. Your larger friends stay here while you prepare suitable homes.”</p>${["gecko", "snail"].map((id) => `<div class="journal-entry"><strong>${rescueInfo[id].name}</strong><p>${state.flags.rescued.includes(id) ? "Found, examined, and resting in a separate care habitat." : "Ready to help when you find them."}</p></div>`).join("")}<div class="notice">Free checkup: ${state.tank.moisture < 55 ? "Little Root needs misting." : state.tank.moisture > 80 ? "Little Root is very damp. Increase airflow and allow it to dry." : "Little Root’s moisture looks comfortable."} ${state.tank.food < 8 ? "Add leaf litter soon." : "Keep watching food and waste."}</div>${button("vet-talk", "Ask about gecko care", "secondary full")}`,
      { eyebrow: "ROOTPORT VET / DR. FERN" },
    );
  if (type === "pharmacy")
    showPanel(
      "shop-pharmacy",
      "Rootport Drug Store",
      `<p>Mina: “Your mom’s prescription is ready. We’re helping her make a treatment plan.”</p>${supply("Mom’s prescription", state.flags.medicineDelivered ? "Already delivered for this chapter" : state.inventory.medicine ? "Already in your bag · take it to Mom" : "One-week supply · take it to Mom", "buy-medicine", "$20", state.money < 2000 || state.inventory.medicine > 0 || state.flags.medicineDelivered)}<p class="hint">No recurring deadline or tank-breaking event is active in this first chapter.</p>`,
      { eyebrow: "PHARMACY / MINA" },
    );
  if (type === "bike")
    showPanel(
      "shop-bike",
      "A little more momentum",
      `<p>Ollie: “The safest fast wheels in Rootport? These little cruisers.”</p>${supply("Cruiser skateboard", "Run mode becomes 25% faster outdoors", "buy-board", state.flags.board ? "Owned" : "$45", state.money < 4500 || state.flags.board)}<p class="hint">Toggle RUN below the screen. Hold Shift on a keyboard. Bikes and OneWheels are planned.</p>`,
      { eyebrow: "BIKE SHOP / OLLIE" },
    );
  if (type === "glass")
    showPanel(
      "shop-glass",
      "Glow n’ Blow",
      `<p>Aunt Ember: “Kaid designs the shapes. I do the hot work. No ten-year-olds near the furnace.”</p>${supply("Carved cork hide", "A visible shelter · +8 appearance points", "buy-hide", state.tank.hide ? "Owned" : "$6", state.money < 600 || state.tank.hide)}<div class="notice">“That 25-gallon birthday tank? Rounded corners, as requested by the boss.”</div><p class="hint">Larger tanks, including a possible 50-gallon upgrade, are planned. Your starter gift stays 25 gallons.</p>`,
      { eyebrow: "GLASS SHOP / AUNT EMBER" },
    );
}
function pause() {
  showPanel(
    "pause",
    "Take a breath.",
    `<span class="badge">DAY ${Math.floor(state.time / 24) + 1} · ${dollars(state.money)}</span><p>Habitat time is paused here.</p><div class="menu-list">${menuRow("resume", "▷", "Back to the world", "Keep exploring Rootport.")}${menuRow("notebook", "▤", "Field notebook", `${state.flags.rescued.length}/4 animal groups safe · notes & goals`)}${menuRow("critter", "◉", "Critter", `${state.posts.length} posts · ${dollars(state.lifetimeEarned)} earned`)}${menuRow("directory", "⌖", "Town guide", "Shops, directions, and controls.")}${menuRow("bag", "◇", "Your bag", "Supplies, savings, and Kaid’s loan.")}</div>${button("save", "Save progress", "secondary full")}<p class="hint">Autosaves after actions and every 15 seconds. No offline time passes. This browser has one save slot.</p>${button("title", "Return to title", "secondary full")}`,
    { eyebrow: "PAUSE / CRITZ: TYCOON" },
  );
}
function notebook() {
  showPanel(
    "notebook",
    "The little things matter.",
    `<div class="notice">${esc(objective(state))}</div>${!state.flags.notebook ? "<p>Your own scrap notes, for now. Meet Professor Nugget near the Vet for a field notebook.</p>" : ""}${Object.entries(
      rescueInfo,
    )
      .map(
        ([id, a]) =>
          `<div class="journal-entry"><strong>${state.flags.rescued.includes(id) ? "✓" : "◇"} ${a.name}</strong><p>${state.flags.rescued.includes(id) ? a.description : a.location}</p></div>`,
      )
      .join(
        "",
      )}<h3>Today’s notes</h3>${state.notebookEntries.length ? state.notebookEntries.map((n) => `<div class="journal-entry"><p>${esc(n)}</p></div>`).join("") : "<p>A fresh page. A new beginning.</p>"}<p class="hint">This chapter uses a compressed, simplified ecosystem. Later chapters will add richer study, sketches, and species-specific habitats.</p>`,
    {
      eyebrow: state.flags.notebook
        ? "PROFESSOR NUGGET’S FIELD NOTEBOOK"
        : "YOUR NOTES",
    },
  );
}
function directory() {
  showPanel(
    "directory",
    "Welcome to Rootport",
    `<p>From home: bedroom stairs → downstairs → yard gate. Town’s streets connect three rows of buildings.</p><div class="map-grid"><span><b>Northwest</b>Your home & yard</span><span><b>North center</b>Kaid’s home</span><span><b>Northeast</b>Your rival’s home</span><span><b>Middle west</b>Critz · moss & litter</span><span><b>Middle center</b>Vet · Professor Nugget nearby</span><span><b>Middle east</b>Drug Store · medicine</span><span><b>Southwest</b>Bike Shop · skateboard</span><span><b>Southeast</b>Glow n’ Blow · glass & decor</span></div><h3>Make yourself at home</h3><p>D-pad / arrows / WASD: walk.<br>A / Z / Enter: interact or confirm.<br>B / X / Escape: go back.<br>Start / P: pause. RUN / Shift: move faster.<br>In menus, tap choices or use ↑ ↓ and A.</p><p class="hint">Press A near a doorway to enter. Look for sparkles when searching. The eastern forest route to Liarsville is planned.</p>`,
  );
}
function bag() {
  showPanel(
    "bag",
    "What you’re carrying",
    `<div class="stat-grid">${stat("Savings", dollars(state.money))}${stat("Kaid’s loan", dollars(state.debt))}${stat("Moss cuttings", state.inventory.moss)}${stat("Leaf litter", state.inventory.litter)}${stat("Prescriptions", state.inventory.medicine)}${stat("Skateboard", state.flags.board ? "Owned" : "None")}</div><p>Clean water for misting is free. Collect two portions of leaf litter from the yard every six habitat hours.</p>${state.debt ? button("repay", `Repay Kaid · ${dollars(state.debt)}`, "secondary full", state.money < state.debt ? "disabled" : "") : ""}`,
  );
}
function back() {
  if (dialogue) {
    nextDialogue();
    return;
  }
  if (["title", "setup", "loan", "confirm-new"].includes(panelName)) return;
  if (["manage", "stats", "view"].includes(panelName)) {
    recording = 0;
    tankMenu();
    return;
  }
  if (panelName === "capture") {
    viewPanel();
    return;
  }
  if (panelName) {
    closePanel();
    return;
  }
  pause();
}
function confirmPanel() {
  const active = document.activeElement;
  if (
    panel.contains(active) &&
    active.tagName === "BUTTON" &&
    !active.disabled
  ) {
    active.click();
    return;
  }
  const btn = panel.querySelector("button:not(.close):not(:disabled)");
  btn?.focus();
}
function moveMenu(dir) {
  const controls = [...panel.querySelectorAll("button:not(:disabled),input")];
  if (!controls.length) return;
  const index = controls.indexOf(document.activeElement);
  controls[
    (index + (dir === "up" || dir === "left" ? -1 : 1) + controls.length) %
      controls.length
  ].focus();
}
function doAction(action, el) {
  if (["boy", "girl"].includes(action)) {
    gender = action;
    for (const b of panel.querySelectorAll(".choice")) {
      b.classList.toggle("selected", b.dataset.action === action);
      b.setAttribute("aria-pressed", b.dataset.action === action);
    }
    $("rival-gender").textContent = gender === "boy" ? "(girl)" : "(boy)";
    return;
  }
  if (
    ["mist", "moss", "feed", "clean", "light", "ventilation"].includes(action)
  ) {
    const result = manage(state, action, Number(el.dataset.value));
    toast(result.message);
    if (result.ok) {
      persist();
      managePanel(true);
      hud();
    }
    return;
  }
  if (action.startsWith("buy-")) {
    const goods = {
      moss: [300, () => state.inventory.moss++, "critz"],
      litter: [150, () => (state.inventory.litter += 3), "critz"],
      medicine: [2000, () => state.inventory.medicine++, "pharmacy"],
      board: [4500, () => (state.flags.board = true), "bike"],
      hide: [600, () => (state.tank.hide = true), "glass"],
    };
    const g = goods[action.slice(4)];
    if (g && spend(state, g[0])) {
      g[1]();
      persist();
      hud();
      shop(g[2]);
      toast("All yours. Added to your supplies.");
    }
    return;
  }
  switch (action) {
    case "new":
      if (loaded.state)
        showPanel(
          "confirm-new",
          "Start fresh?",
          `<p>This replaces your browser’s existing save when the new story begins.</p>${button("confirm-new", "Start a new story")}${button("cancel-new", "Keep my current story", "secondary full")}`,
          { back: false },
        );
      else setup();
      break;
    case "confirm-new":
      setup();
      break;
    case "cancel-new":
      titleScreen();
      break;
    case "begin": {
      const hero = $("hero-name").value.trim(),
        rival = $("rival-name").value.trim();
      if (!hero || !rival) {
        toast("Give both characters a name to begin.");
        (!hero ? $("hero-name") : $("rival-name")).focus();
        return;
      }
      state = createState(hero, gender, rival);
      loaded = { state: null };
      simAccumulator = 0;
      closePanel();
      persist();
      hud();
      opening();
      break;
    }
    case "continue":
      state = loaded.state;
      closePanel();
      if (state.stage === "night") {
        state.scene = "bedroom";
        state.player = { x: 7.6, y: 5.4, facing: "up" };
        delete state.storyBeat;
        opening();
      }
      hud();
      break;
    case "accept-loan":
      finishNight(true);
      break;
    case "decline-loan":
      finishNight(false);
      break;
    case "back":
      back();
      break;
    case "manage":
      managePanel();
      break;
    case "stats":
      statsPanel();
      break;
    case "view":
      viewPanel();
      break;
    case "photo-mode":
      camera.kind = "photo";
      viewPanel();
      break;
    case "video-mode":
      camera.kind = "video";
      viewPanel();
      break;
    case "capture":
      if (camera.kind === "video") {
        recording = 6;
        el.disabled = true;
        el.textContent = "● Recording… 6s";
      } else takeCapture();
      break;
    case "retake":
      viewPanel();
      break;
    case "publish":
      if (capture) {
        publish(state, capture);
        capture = null;
        persist();
        hud();
        critterPanel();
        toast("Posted! Your first viewers are finding it.");
      }
      break;
    case "critter":
      critterPanel();
      break;
    case "notebook":
      notebook();
      break;
    case "directory":
      directory();
      break;
    case "bag":
      bag();
      break;
    case "resume":
      closePanel();
      break;
    case "save":
      persist(false);
      break;
    case "title":
      persist();
      loaded = load();
      titleScreen();
      break;
    case "repay":
      if (state.debt && spend(state, state.debt)) {
        state.debt = 0;
        persist();
        hud();
        if (panelName === "bag") bag();
        else kaidMenu();
        toast("Kaid’s loan repaid. “You remembered. Thanks, friend.”");
      }
      break;
    case "observe":
      tick(state);
      persist();
      hud();
      if (panelName === "stats") statsPanel(true);
      else if (panelName === "critter") critterPanel(true);
      else refreshLive();
      toast("One habitat hour passes.");
      break;
    case "rest":
      tick(state, 8);
      closePanel();
      persist();
      hud();
      announce("Eight quiet hours later");
      break;
    case "supply-gift":
      if (!state.flags.supplyGift) {
        state.flags.supplyGift = true;
        state.inventory.litter += 3;
        state.inventory.moss++;
        persist();
        shop("critz");
        toast("Welcome kit: 1 moss cutting and 3 leaf-litter portions.");
      }
      break;
    case "vet-talk":
      closePanel();
      say([
        [
          "Dr. Fern",
          "Geckos need appropriate temperatures, ventilation, fresh water, and the right food. Their needs depend on the species.",
        ],
        [
          "Dr. Fern",
          "Pebble stays with us until you have a suitable setup. A sealed plant terrarium isn’t a gecko home.",
        ],
      ]);
      break;
  }
}
panel.addEventListener("click", (e) => {
  const el = e.target.closest("[data-action]");
  if (el && !el.disabled) doAction(el.dataset.action, el);
});
panel.addEventListener("input", (e) => {
  if (e.target.id === "frame") camera.frame = Number(e.target.value);
  if (e.target.id === "zoom") camera.zoom = Number(e.target.value) / 100;
  cameraScores();
});
function bindPress(el, onDown, onUp = () => {}) {
  el.addEventListener("pointerdown", (e) => {
    e.preventDefault();
    el.setPointerCapture(e.pointerId);
    el.classList.add("pressed");
    onDown(e);
  });
  for (const name of ["pointerup", "pointercancel", "lostpointercapture"])
    el.addEventListener(name, (e) => {
      el.classList.remove("pressed");
      onUp(e);
    });
  el.addEventListener("contextmenu", (e) => e.preventDefault());
}
for (const b of document.querySelectorAll("[data-dir]"))
  bindPress(
    b,
    () => {
      if (panelName) moveMenu(b.dataset.dir);
      else down.add(b.dataset.dir);
    },
    () => down.delete(b.dataset.dir),
  );
bindPress($("a-button"), interact);
bindPress($("b-button"), back);
$("start").addEventListener("click", () => {
  if (dialogue || ["title", "setup", "loan", "confirm-new"].includes(panelName))
    return;
  panelName === "pause" ? closePanel() : pause();
});
$("run").addEventListener("click", () => {
  running = !running;
  $("run").setAttribute("aria-pressed", running);
});
$("dialogue-next").addEventListener("click", nextDialogue);
$("journal-shortcut").addEventListener("click", () => {
  if (!dialogue && state.stage === "morning" && !panelName) notebook();
});
const keyDirs = {
  ArrowUp: "up",
  w: "up",
  ArrowDown: "down",
  s: "down",
  ArrowLeft: "left",
  a: "left",
  ArrowRight: "right",
  d: "right",
};
document.addEventListener("keydown", (e) => {
  const textInput = e.target.tagName === "INPUT";
  if (textInput) {
    if (e.key === "Escape") {
      e.target.blur();
      e.preventDefault();
    }
    if (e.key === "Enter" && panelName === "setup") {
      e.preventDefault();
      doAction("begin");
    }
    if (e.key !== "Tab") return;
  }
  if (e.key === "Tab" && panelName) {
    const items = [...panel.querySelectorAll("button:not(:disabled),input")];
    const first = items[0],
      last = items.at(-1);
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
    return;
  }
  const dir = keyDirs[e.key];
  if (dir) {
    e.preventDefault();
    if (panelName) {
      if (!e.repeat) moveMenu(dir);
    } else down.add(dir);
    return;
  }
  if (["z", "Z", "Enter", " "].includes(e.key)) {
    e.preventDefault();
    if (!e.repeat) interact();
  }
  if (["x", "X", "Escape"].includes(e.key)) {
    e.preventDefault();
    if (!e.repeat) back();
  }
  if (["p", "P"].includes(e.key)) {
    e.preventDefault();
    if (
      !dialogue &&
      !["title", "setup", "loan", "confirm-new"].includes(panelName)
    ) {
      panelName === "pause" ? closePanel() : pause();
    }
  }
});
let shift = false;
document.addEventListener("keydown", (e) => {
  if (e.key === "Shift") shift = true;
});
document.addEventListener("keyup", (e) => {
  if (keyDirs[e.key]) down.delete(keyDirs[e.key]);
  if (e.key === "Shift") shift = false;
});
function clearInput() {
  down.clear();
  shift = false;
  document
    .querySelectorAll(".pressed")
    .forEach((b) => b.classList.remove("pressed"));
}
window.addEventListener("blur", clearInput);
window.addEventListener("resize", fitOverlay);
document.addEventListener("visibilitychange", () => {
  clearInput();
  lastTime = performance.now();
  if (document.hidden && !["title", "setup", "confirm-new"].includes(panelName))
    persist();
});
window.addEventListener("pagehide", () => {
  if (!["title", "setup", "confirm-new"].includes(panelName)) persist();
});
function frame(now) {
  const dt = Math.min(0.05, (now - lastTime) / 1000);
  lastTime = now;
  if (!document.hidden) {
    visualTime += dt;
    moving = false;
    if (!panelName && !dialogue && !transitioning) {
      const dx = Number(down.has("right")) - Number(down.has("left")),
        dy = Number(down.has("down")) - Number(down.has("up"));
      moving = movePlayer(
        state,
        dx,
        dy,
        dt *
          (state.flags.board &&
          ["town", "yard"].includes(state.scene) &&
          (running || shift)
            ? 1.25
            : 1),
        running || shift,
      );
    }
    const live =
      state.stage === "morning" &&
      !dialogue &&
      !transitioning &&
      (!panelName ||
        ["manage", "stats", "view", "critter", "tank"].includes(panelName));
    if (live) {
      simAccumulator += dt;
      if (simAccumulator >= HOUR_SECONDS) {
        simAccumulator -= HOUR_SECONDS;
        tick(state);
        hud();
        refreshLive();
        if (panelName === "critter") critterPanel(true);
      }
    }
    if (
      now - lastSaved > 15000 &&
      !["title", "setup", "confirm-new"].includes(panelName)
    ) {
      persist();
      lastSaved = now;
    }
    renderWorld(canvas, state, visualTime, moving);
    for (const id of ["tank-preview", "view-canvas"]) {
      const target = $(id);
      if (target)
        renderTank(
          target,
          state.tank,
          visualTime,
          id === "view-canvas" ? { ...camera, reticle: true } : {},
        );
    }
    const welcome = $("welcome-tank");
    if (welcome)
      renderTank(
        welcome,
        { ...state.tank, plants: 5, isopods: 8, springtails: 18 },
        visualTime,
      );
    if (recording > 0) {
      recording -= dt;
      const btn = panel.querySelector('[data-action="capture"]');
      if (btn) btn.textContent = `● Recording… ${Math.ceil(recording)}s`;
      if (recording <= 0) takeCapture();
    }
    const near = nearestEntity(state);
    $("interact-prompt").hidden = !!(dialogue || panelName || !near);
    if (near && !dialogue && !panelName)
      $("interact-prompt").innerHTML = `<b>A</b> ${esc(near.name)}`;
  }
  requestAnimationFrame(frame);
}
// Recover an out-of-bounds position gracefully if a future map edit moves walls.
if (loaded.state && isBlocked(state.scene, state.player.x, state.player.y)) {
  state.player = { x: 8, y: 9.5, facing: "down" };
}
hud();
titleScreen();
requestAnimationFrame(frame);
// Read-only development snapshot for integration tests and balancing tools.
export function getDebugSnapshot() {
  return structuredClone(state);
}
