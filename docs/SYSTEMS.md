# Systems and balancing reference

All money is integer cents. All simulation calculations are deterministic. Animations use elapsed render time but never decide births, reach, or money.

## Architecture

`state.js` is pure domain logic (save/load accepts an injected storage adapter). `world.js` stores maps and handles navigation. `art.js` only draws. `main.js` binds gameplay state, dialogue, DOM panels, controller events, and the animation loop. There are no runtime libraries or network calls.

Coordinates represent character feet in 24px world tiles. Movement normalizes diagonals; walking is 3.15 tiles/sec and running 5.2. A skateboard increases outdoor running by 25%. Collision uses axis-separated movement. Interaction chooses the nearest entity within 1.65 tiles. Rooms transition through A-triggered doors and valid explicit spawn coordinates. The town scrolls inside a 384×288 canvas.

One habitat hour = 8 real seconds of active play. Simulation pauses in dialogue, title/setup, shops, bag/notebook/town guide, pause, and capture preview. It continues in exploration and tank/manage/stats/view/Critter screens. Browser backgrounding pauses the loop; no offline catch-up. Observe advances one hour, rest advances eight (not necessarily until the next 08:00).

## Tank model

This is a deliberately compressed learning model. Percentages are bounded 0–100. Microbes are an index, not a counted population. No real-life species care claims follow from these coefficients.

Each hour, in order:

1. Moisture change = `−(0.65 + ventilation × 0.55) + plants × 0.15`.
2. Microbial processing = `microbes × 0.025 × clamp(moisture / 50, 0, 1)`.
3. Consumption = `isopods × 0.12 + springtails × 0.025`; subtract from litter.
4. Waste change = `consumption × 0.6 + (litter > 70 ? 2 : 0) − microbialProcessing − springtails × 0.025`.
5. Nutrient change = `microbialProcessing × 0.9 − plants × 0.23`.
6. Microbe index changes +0.6 if moisture >40 and food >0, otherwise −0.5. Clamp index to 5–85.
7. Algae change = `(lightHours − 7) × 0.3 + (moisture > 82 ? 0.5 : −0.35) − springtails × 0.008`.
8. Thriving means moisture 55–80, litter ≥8, waste <45 and ventilation ≥2. Stress decreases 5 if thriving, increases 3 otherwise. Stress over 50 slows isopod animation.
9. Every sixth hour, thriving established populations gain one isopod (cap 24) and up to three springtails (cap 60). Otherwise a message explains the binding constraint. These compressed births are not realistic reproduction times.
10. Append a history sample; retain 24 samples and 12 event messages.

Actions: mist +14 moisture; add moss +1 plant (6 max, uses 1 cutting); litter +25 food/+4 waste (uses 1 portion); cleaning −18 waste/−14 algae/−3 microbes; lighting 4/8/12 hours; ventilation low/balanced/open = 1/2/3. All bounds clamp. Moss is an integer shelter/planting count; actual plant growth, starvation deaths, disease, oxygen chemistry and full nutrient conservation are future work. The tank is not a sealed gecko habitat.

Activity = mean of moisture comfort (`clamp(100 − abs(67 − moisture) × 2.3)`), food availability (`min(100, food × 5)`), air (60 for low, otherwise 100), and cleanliness (`clamp(100 − waste × 0.75)`). It is used for visible activity/photography alongside individually inspectable conditions, not as a universal ecosystem health score.

## Critter

A draft has `kind`, pan `frame` (0–100), zoom (1–1.6), and a PNG snapshot. Real six-second capture countdowns produce simulated video posts; no video encoder or camera/microphone access exists.

- Activity: habitat activity when animals are present, otherwise 12.
- Composition: `clamp(100 − abs(frame − 55) × 1.3 − abs(zoom − 1.2) × 45, 15, 100)`.
- Appearance: `clamp(30 + plants × 11 + (hide ? 8 : 0) − algae × 0.45 − waste × 0.22)`.
- Rarity: common decomposers 25, otherwise 10. No random rare-species rewards.
- Interest: 85 normally, 30 when the last post is under six habitat hours old.
- Weighted score: 25% activity + 20% composition + 25% appearance + 10% rarity + 20% interest, rounded.
- Target views: `(120 + score × 22) × (video ? 1.15 : 1)`, rounded.
- Initial reach: 35%; each of the next four hours adds 16.25% of the target, reaching 100%.
- Engagement: `2 + score × 0.075` percent, one decimal place. Likes = rounded views × engagement. Replies = floor(likes / 18).
- Revenue = floor(views × 0.12) cents, i.e. a fictional **$1.20 per 1,000 views**. Each update credits only the difference from already-paid revenue; reloading cannot repay old earnings.
- Retain 12 recent posts and lifetime earnings. Scores are stored with each post. There is no real platform connection or actual advertising.

## Economy and recovery

Base savings $12; optional loan +$100 / debt $100. Rescue reward $15 once. Moss $3; litter (3 portions) $1.50; prescription $20 once per chapter, delivered to Mom; skateboard $45; cork hide $6. Pet shop gives 1 free moss and 3 litter portions once. Yard foraging gives 2 litter portions every 6 habitat hours. Water and cleaning are free. Declining the loan cannot permanently lock the player out of basic care or earnings.

## Save contract

Storage keys: `critz-tycoon.save.v1` and `.backup`. Save after actions, every 15 seconds during play, and on page-hide/background. The previous valid snapshot becomes the backup. Load validates schema, core numeric bounds, scene, characters, inventory, rescues, and post structure before accepting it. Corrupt primary saves fall back to the previous valid save; unrecoverable saves show a notice. Storage failure shows a toast, not a false success. No external data is fetched. User-entered names are escaped before HTML rendering. Version changes should add explicit migrations; do not silently reinterpret old saves.

A partially completed opening resumes at its start; completed loan decisions resume in the morning. New Story requires confirmation if a saved story exists. One origin/browser is one slot; serving on a new port or host creates a separate slot.
