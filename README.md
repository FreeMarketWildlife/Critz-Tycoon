# Critz: Tycoon

A playable, mobile-first ecosystem RPG. Explore Rootport, recover your escaped animals, care for Kaid’s birthday tank, and share a tiny living world on Critter. Original code-drawn pixel art; no accounts, services, game engine, or runtime dependencies.

## Play on your phone

[Play Critz: Tycoon](https://critz-tycoon.freemarketwildlife.chatgpt.site). Open in Safari or Chrome; sign in with the owner’s ChatGPT account if prompted. No local server is needed for this hosted version.

## Play locally

Requires Node.js 20 or newer. No dependency installation is needed.

```bash
git clone https://github.com/FreeMarketWildlife/Critz-Tycoon.git
cd Critz-Tycoon
git switch main
npm run dev
```

Open **http://localhost:5173**. To play on a phone on the same Wi-Fi, open `http://YOUR_COMPUTER_LAN_IP:5173`; allow the local server through your computer’s firewall if needed. The server binds to `0.0.0.0` for LAN play. Use a private trusted network.

For an existing checkout, skip cloning and run from its directory. If npm is unavailable on the original development machine, use the exact bundled-Node command in [project status](docs/PROJECT_STATUS.md#launch-and-reproduce-baseline).

```bash
npm test          # deterministic systems + world checks
npm run check    # syntax checks
npm run build    # writes the static game to dist/
npm run preview  # serves dist/ on port 5173
```

Set `PORT` to choose another port. Serve `dist/` with any static host; all asset paths are relative, including deployment under a repository subpath. Opening `index.html` directly as a file will not load ES modules reliably.

## Controls

| Action | Touch | Keyboard |
| --- | --- | --- |
| Walk | Hold D-pad | Arrows / WASD |
| Interact / confirm | A | Z / Enter / Space |
| Back / cancel | B | X / Escape |
| Pause | Start | P |
| Move faster | Toggle RUN | Hold Shift |
| Menu choice | Tap, or D-pad then A | Arrows, Tab, Enter |

Press A near people, hiding places, tanks, and doors. Doors do not require pixel-perfect alignment. Menus scroll independently; the game does not scroll on movement. Progress autosaves after actions, on leaving the page, and every 15 seconds. Start → Save provides a manual save. Reload → Continue restores it. One save slot per browser/origin, with a previous-valid-save backup. No cloud saves or offline simulation.

## Playable now

- Named boy/girl Black child Hero; named opposite-gender rival.
- Opening night, the broken tanks, Kaid’s 25-gallon gift, optional $100 interest-free loan, and the first morning.
- Connected bedroom, downstairs, yard, town, both neighbors’ homes, and all five named shops.
- Four rescue groups: Pebble the gecko, Button the garden snail, six isopods, and twelve springtails. Every animal survives. Gecko and snail receive separate temporary care at the Vet.
- Professor Nugget’s notebook and a $15 rescue reward; NPC conversations, inventory, money, purchases, and optional loan repayment.
- Bedroom tank → **Manage / Stats / View**. Misting, light duration, ventilation, moss planting, feeding, cleaning, and observation all work.
- Deterministic terrarium model: moisture, litter, waste, nutrients, microbial activity, moss, algae, isopods, springtails, births, population limits, history, and causal event messages.
- Animated tank camera with pan/zoom, saved photo snapshots, six-second **simulated** videos, and an actual in-game Critter feed. Visible scoring factors determine views, engagement, and paid-in-cents game revenue.
- Working shop goods: moss, leaf litter, prescription pickup/delivery, a faster outdoor skateboard, and a visible cork hide. Free care advice, welcome supplies, and repeatable yard foraging make the no-loan path recoverable.
- Touch controller, keyboard controls, responsive portrait/landscape layout, local save validation and backup recovery.

## Deliberately planned, not implemented

Additional tanks and placement, aquariums/paludariums, species-specific larger-animal habitats, realistic reproduction/husbandry timescales, deaths/ecological collapse, automation, richer notebook sketches, commissions/shipping, animal sales, audience milestones, the recurring weekly medication setback, Liarsville/forest exploration, later biomes/snorkeling, bikes/OneWheels, music/sound, real exported video, cloud save and PWA offline installation.

The pharmacy purchase exists, but **no weekly deadline or repeat tank-breaking event is active**. Time freezes in dialogue, pause, shop, notebook, and posting-preview screens; tank/camera/feed screens continue. A habitat hour takes 8 seconds of active play. This is a forgiving game model, not real-world husbandry guidance. No animal deaths are simulated in this first chapter. Critter’s revenue and algorithm are fictional and transparent, not a promise about actual social platforms.

## Development

- `src/main.js`: gameplay flow, dialogue, DOM menus, input, lifecycle.
- `src/world.js`: scene data, interactions, collision and transitions.
- `src/state.js`: pure state, simulation, economy, posting and save validation.
- `src/art.js`: original Canvas tilework, sprites, and tank renderer.
- `docs/GAME_VISION.md`: confirmed full vision and proposed future ideas.
- `docs/SYSTEMS.md`: exact simulation and scoring rules.
- `docs/QA.md`: verification scope and remaining limitations.

Optional browser regression tests (development only):

```bash
npm install --no-save playwright
npx playwright install chromium
node tests/browser.mjs
```

The browser suite starts its own local server and walks the actual world using keyboard input rather than teleporting progress. It checks the main story, rescues, shops, tank management, posting, refresh, and responsive bounds. Screenshots and the report go into ignored `test-results/`. `getDebugSnapshot()` is an exported read-only copy for tests and balancing tools, not a mutable game-state backdoor.

**Current development:** the visual-foundation audit and production plan. Read [project status](docs/PROJECT_STATUS.md), [milestones and review gates](docs/PROJECT_PLAN.md), [art bible](docs/ART_BIBLE.md), and [reference measurements](docs/REFERENCE_MEASUREMENTS.md) before changing the game. Work directly on `main`. M0 changes documents only; the next proposed deliverable is an original character lineup and one bedroom composition for visual approval. Habitat upgrades, commissions and multiple tanks remain future work.

The playable foundation was found in [existing PR #1](https://github.com/FreeMarketWildlife/Critz-Tycoon/pull/1) at `191e3a6` and incorporated into `main` alongside the M0 documents. See project status for the verified Git state and launch commands.
