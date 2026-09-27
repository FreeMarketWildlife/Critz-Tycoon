# Native habitat close-up

`src/tank-render.js` replaces the old prototype habitat drawing with original row-authored pixel sprites and the playable atlas's soil, glass, leaf, cream and wood palette families. It exports the same `renderTank(canvas, tank, time, camera)` API. Root integration changes only the import in `src/main.js`; the historical gallery can retain its prototype renderer.

The existing 400×200 Critter snapshots are composed at 200×100 and scaled exactly 2×. The 400×148 title card is composed at 200×74. Plants, litter, hiding place, isopods, springtails, algae, waste and high-moisture droplets remain driven by the corresponding tank state. Stress slows animal motion. No state fields, simulation clocks, scoring, earnings or capture dimensions are changed. Pan and zoom sample integer source rectangles into a native raster with nearest-neighbor sampling; magnification is a presentation choice, not exploration motion.

`TANK_SPRITES` exports editable rows for the original organisms, leaf litter, stone, log, hide, frond and moss. Drawing uses only opaque integer rectangles and nearest-neighbor image copies; it contains no ellipses, antialiasing, translucent light bands or fractional object positions. This is a code-native source extension consistent with the current environment authoring workflow, not a replacement generated illustration.

Style and final user acceptance remain pending. Technical image checks must not be described as user approval.
