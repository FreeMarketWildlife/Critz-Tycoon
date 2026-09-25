# Verification — playable foundation

## Executed successfully

- `npm run check`: syntax checks for all four game modules.
- `npm run build`: static production output generated; no runtime dependencies.
- `npm test`: 10 passing deterministic domain/world tests.
- `node tests/browser.mjs`: 14 passing Chromium integration checkpoints, no uncaught page errors. This run used a local Chromium binary because the cloud browser could not reach localhost.
- `git diff --check`: no whitespace errors.

### Systems coverage

Both loan branches; idempotent gift/loan; all rescues and nonlethal behavior; quantitative management effects; deterministic multi-hour progression; births and paused breeding; inventory and affordability; framing and fresh-interest scoring; exactly-once ad payouts; save round trips, malformed-state rejection, storage failure and backup recovery; scene exit spawn validity; approachable interactions; collision, diagonal normalization and run speed.

### Browser coverage

The main integration run did not inject quest flags or teleport the player. It walked collision-aware paths through the world using held keyboard input.

1. Select and name a girl Hero and an opposite-gender rival.
2. Complete the opening, accept Kaid’s loan, receive the 25-gallon tank.
3. Walk through bedroom, house, and yard and rescue all four animal groups.
4. Talk to Professor Nugget; receive notebook and $15 reward.
5. Enter Critz, purchase moss, claim the free kit.
6. Enter Vet, Drug Store, Bike Shop, and Glow n’ Blow; buy the prescription, skateboard, and cork hide.
7. Enter both neighboring homes and talk to residents.
8. Deliver the prescription to Mom; return upstairs to the tank.
9. Plant, feed, mist, change lighting, observe, and inspect Stats.
10. Pan/zoom a photo, publish on Critter, observe reach and earnings.
11. Complete a six-second simulated-video recording and post it.
12. Save and reload; verify names, money, inventory, rescues, tank and posts persist.
13. Check panel/controller bounds at 320×568, 390×844, 844×390 and 1280×900.
14. Hold/release the virtual D-pad and verify movement stops on release.
15. Check for uncaught browser errors: none.

Generated screenshots and the machine-readable report are in ignored `test-results/`. Selected preview screenshots are in `docs/screenshots/`.

## Fixes made during verification

- Moved the first-morning spawn out of the bed’s collision rectangle.
- Bounded scrollable menus to the space above the virtual controller.
- Kept controller buttons on-screen in small portrait and landscape layouts.
- Paused/cancelled simulated recording when another menu opens.
- Allowed saved positions across the full walkable southern edge of town.
- Added validation for saved snapshot image data and history records.

## Limitations and follow-up

- Browser verification is Chromium with phone-sized viewports and touch-capable context; **not a physical iPhone or Safari test**. Verify Safari keyboard resizing, safe areas, multi-touch and long sessions on a real phone before release.
- No audio, gamepad support, installed PWA/offline cache, cloud save, localization, or reduced-motion-specific animation mode beyond transition reduction.
- Original art is code-drawn foundation art. Add richer creature animations, palette passes and environmental detail as content expands.
- One starter terrarium, compressed simulation, nonlethal populations and simulated video are intentional scope limits. This is not a realistic husbandry simulator yet.
- No public deployment was created by this change. README provides exact local/LAN launch instructions and static-host build instructions.
