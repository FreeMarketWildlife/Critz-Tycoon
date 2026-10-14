# M1.ME10 — Build more, manage less

User requests: research Mario Maker and other strong map editors; remove wasted space and technical clutter; make the interface collapsible, fun and understandable. This is an authoring UI change, with existing native art and all map/save semantics preserved.

## Primary-source research

- [Nintendo's Super Mario Maker manual](https://www.nintendo.com/eu/media/downloads/games_8/emanuals/nintendo_3ds_2/supermariomakerfornintendo3ds/ElectronicManual_Nintendo3DS_SuperMarioMakerForNintendo3DS_EN.pdf), pages12–18, inspected October14 2026: visual element palette and touch placement, explicit Undo/Eraser, Save/Load, Trial Play and Hide Icons to regain space. Reviewed the official creation and techniques sections. This is the official3DS edition; no claim of having observed Mario Maker2 gameplay. The Mario Maker2 promotional site timed out.
- [Tiled introduction](https://docs.mapeditor.org/en/stable/manual/introduction/), stable1.12.2 documentation, inspected October14 2026: stamp brush, automatic terrain transitions, separate object layers and project setup. Its documentation separates tile painting, object authoring and project setup. These patterns inform Critz; Nintendo/Tiled artwork and layouts are not copied.

## What changed

- The right notebook is gone from the permanent layout. The map now fills the right side:1152×706 at1440×960 with the palette open, wider when collapsed.
- Build uses native previews, clear Terrain / Props / Advanced tabs and collapsible Ground / Water / Features. Water variants have actual depth/motion labels instead of undefined names. Search finds all tools and exposes matching hidden groups; empty groups disappear during search.
- Six common drawing tools stay in one strip. Pick, Hero start and passages live under More tools. Size/name, new maps, links and validation live under map actions. Grid/collision/layers live under View. Selection controls appear when needed.
- Project contains backup/open/PNG/share, area bases, collapsible notes, cell inspection and New blank world. Phone sharing remains available. Save feedback and unreadable-draft recovery stay visible in the drawer.
- Focus hides the toolbox and drawing strip. Help explains the three-step pick/build/test loop and keeps shortcuts/technical guidance collapsed.
- On phones, Build opens as a native modal bottom tray. Choosing an item closes it and returns focus to the canvas. Project/Help support Escape/backdrop dismissal; modal focus stays inside. Desktop tabs support arrow/Home/End navigation.
- Canvas shortcuts B/R/F/E/S/H/I select tools. Existing arrows/Enter, selection copy/paste, undo/redo and Space-drag remain. Ordinary nonmodal palette does not disable canvas keyboard editing.

Removed permanent content: review slogans/links, Emerald map-size table, contact-lab promotion, repeated implementation prose and unrelated editor links. Existing guides/review routes still exist at their original URLs.

## Verification

All browser tests use fresh isolated Playwright contexts with synthetic storage; real browser drafts/saves are never used.

-313 unit tests and standard syntax checks pass.
-22 general browser groups: paint/rectangle/fill, undo/redo, prop placement/movement/drag, exact overrides, clipboard/reimport, malformed imports, autosave/save isolation, downloads, maps/connections, disposable Hero walking/ledge/boulder/warp tests, validation, tablet and touch controls, corrupt draft retention and no runtime/missing-asset errors.
-7 named-area groups: exact first Rootport load, revision draft persistence, share, mobile, corrupt/unknown fail-closed behavior and generic-draft preservation.
-6 bench groups: hop/seated lock/front-only exit in all four directions, searchable phone props, no errors.
-15 usability groups: collapse/reopen, search categories, exact painting/history, keyboard editing with open desktop palette, ARIA tabs, View/layers, Focus, single-modal share/download/test/help,320/390 phone,844×390 landscape,1024 tablet, actual touch placement and no browser exceptions.

The first new test exposed a hidden Fit button at320px; it is now retained. The final screenshot review caught a cramped desktop palette in844×390 landscape after the initial version55 publication; the follow-up uses the modal tray and a compact toolbar there, with an explicit minimum800×190 canvas assertion. The older general drag test used a fixed screen location that became outside the map under the larger canvas; it now targets an actual free map cell. These repairs were followed by passing runs.

Screenshots: [before](before.png), [desktop](desktop.png), [phone](viewport-390x844.png), [phone Build](build-390.png), [320px](viewport-320x640.png), [landscape](viewport-844x390.png), [touch](phone-touch.png). Reports under `general/`, `areas/`, `benches/`, and `ui-checks.json`; source and production runs pass all50 browser groups (15+22+7+6). Hosted receipts are recorded separately.

Visual usability is for the user to judge. No physical iPhone/Safari testing is claimed. No new game art, terrain geometry, collision, saved-world format or approval gate changes.
