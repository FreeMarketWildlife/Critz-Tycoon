# M 1.C 2 still-character browser verification

Final run: 15 checks pass; 0 failed. Tested all 12 native designs at http://localhost: 5181/art-review/characters.html using isolated headless Chrome contexts.

Coverage: every character selected and every label/body type/design signature measured at 320×568, 390×844, 844×390 and 1280×900; exact 8× portrait/4× cards and integer native room scale; no horizontal overflow or clipped controls; background and reversible pixel-guide controls; keyboard activation, visible focus and tab reachability; phone touch controls; native PNG downloads match all 12 source files byte-for-byte; static canvas pixels, no animation frames or CSS animation; no game-state imports, runtime errors, storage reads or storage writes; missing JSON/PNG error displays and disabled controls.

The selected card's name contrast is 8.24: 1; the smaller body label is 5.94: 1 after opacity compositing. Dark selected-state hover retains the same colors.

Visually inspected: complete 12-character desktop and narrow-phone cast grids, narrow-phone selected studio, full landscape page and touch phone studio. Text wraps cleanly; character pixels retain uniform scale. Physical iPhone/Safari was not tested. These checks are not user art acceptance.

`browser-report.json` contains the final actual results. `tested-review-sha 256.json` fingerprints the reviewed page, atlas and shared rendering/world dependencies. The repeatable runner is `tests/characters-browser.mjs`.

Initial final-batch run had a timeout waiting for the 11th consecutive browser download event after 10 successful downloads. The requested file itself returned 200. The final harness verifies each download in a fresh isolated context; all 12 then passed exact byte comparison without any application change. The original report is retained as `browser-report-before-download-isolation.json` to distinguish that browser/harness event from application results.

Screenshots: `characters-{width}x{height}.png` full pages; `studio-{width}x{height}.png` selected detail; `cast-{width}x{height}.png` complete cast. `touch-phone-studio.png` shows the final character on a grass background in mobile touch emulation. `guides-desktop.png` shows inspection guides. Failure screenshots document both missing atlas cases.
