# Visual foundation production plan

## M1.WA1 — Water/wildlife and world clock

**Implemented, checks passed; publication in progress; awaiting visual review.** User requests animated water, rock turtles, dawn/dusk fish and a Stardew-style clock/daylight cycle at half speed. [Concrete playable review](reviews/M1-WA1/README.md). Adventure clock/sleep rules are implemented; new wildlife pixels remain in a separate review scene before integration. No fee/energy system, save-key change or wider milestone acceptance. Clean release checks:173 unit tests,12 new browser scenarios,17 adventure regressions and independent native art/syntax validation. Next: verified push/publication, then user feedback on appearance and motion.

## M1.LG2 — Luke greenhouse refinement

**Implemented, tested, pushed and published; awaiting user visual/feel review.** Compact symmetric greenhouse, centered door/four tubs per side, mirrored equipment, saved optional shadow layer, rare ordinary Dorothy, looping golden hopper and hidden1% shiny catches are implemented in the separate review. Clean export passes156 unit tests,19 greenhouse browser checks and17 adventure regressions, plus native-art validation. Preserve LG1 economy/saves and accepted adventure. User praise approves LG1 direction, not new LG2 motion or broader M1/M2 gates. Source `6690add` is pushed; deployment `appgdep_6ac9810bc12481918900fdfbe46781e1` succeeded. Next: user visual/play feedback on the [published greenhouse](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/greenhouse.html); no LG2 publication work remains. [Evidence](reviews/M1-LG2/README.md).


## M1.CT1 — Transition-tile contact lab

**Implemented, tested, pushed and published; awaiting user choice.** Separate A/B/C/D house/wall/cliff comparison uses one native assembly method, whole blocked transition cells, a labeled fine-approach proposal versus current tile-step spacing, optional bump haptics and Copy choice. [Deliverable and pinned source evidence](reviews/M1-CT1/README.md). Clean checks:166 unit,13 contact browser,22 map-editor regression scenarios and native art/footprint checks. Original atlases, accepted controllers and saves remain unchanged. Source `afb979c` is published at the existing phone site’s `/art-review/contact-lab/` route with successful deployment evidence in status; committed greenhouse work is retained unchanged. Next: collect the user’s material split and movement preference before integration. No M1/M2 gate is self-approved.

## M1.ME1 — Terrain-aware map editor

**Implemented, tested, pushed and published; art/feel approval pending.** Latest user request authorizes a separate map editor, not hidden bases or accepted-world replacement. [Deliverable and source-derived map presets](reviews/M1-ME1/README.md). Terrain transitions, fences, mountain/opening/stair/directed-ledge cells, semantic stamps, copy/import/export, map links and isolated Hero testing are ready. Clean checks: 150 unit, 22 editor, 10 sprite-editor and 17 adventure browser scenarios; original world/Hero atlases remain unchanged. Preserve unrelated unfinished character work. Source `88c0689` is published at the existing phone site’s `/map-editor/` route with successful deployment evidence in status. Next: the user authors/tests a map and pastes Copy for chat; refine that concrete map/editor feedback. No broader M1/M2 gate is self-approved.

## M1.LG1 — Luke’s Greenhouse playable review

**Implementation, clean checks, push and publication complete; user visual/feel approval pending.** Latest user request authorizes Luke’s new character, eight-tub greenhouse and $100 silhouette-scoop encounter as the active focused implementation. [Deliverable](reviews/M1-LG1/README.md). Original native art, enter/decline/eject/pay/select/catch/reveal/browse/re-enter loop and isolated persistent review collection are implemented. Luke alone sells goldfish; current name supersedes Nuggets. Other creator cameos remain planned. New appearance/motion await the user; broader M1/M2 gates remain open. The clean export passes135 unit checks,14 greenhouse browser checks,17 adventure scenarios and independent native-art validation. Source `f223e83` is published at the existing phone site’s `/art-review/greenhouse.html` route with successful deployment evidence in status. Next: concrete user review feedback before world/save integration. Other creator cameos remain planned; no gate is self-approved.


## MUSIC.03 — Approved MIDI integration

The user accepted the thirty-track MUSIC.02 rewrite and authorized permanent assets, removal of rejected tracks, local MIDI architecture and appropriate in-game placements. **Implemented, tested, pushed and published.** Keep one canonical MIDI collection in `assets/audio/`, retain editable sources, decode/synthesize the actual files in a background worker, and choose scene/story/habitat cues with fades and persistent Music/volume controls. Preserve game saves and other review gates. [Architecture](AUDIO_ARCHITECTURE.md) · [Evidence](reviews/MUSIC-03/README.md). Exact next action: refine concrete in-game listening feedback on the published build.

## M1.E3 — Richer terrain and clear paths

**Implemented, tested, pushed and published; user visual feedback pending.** Richer native grass/dirt and connected turf islands; 33 misplaced fence cells removed from roads, rooted flowers/ferns kept on planted ground. All 644 prior tile pixels/animations remain exact. [Deliverable](reviews/M1-E3/README.md). Source `77a2fbb` is live after 120 unit, five native pixel and 101 browser checks. Next: user terrain/layout feedback; no wider milestone is self-approved.

## M1.UI2 — Uninterrupted play area

**Implemented, tested, pushed and published; user presentation feedback pending.** Automatic tips and top chrome are removed; the world fills available screen space while preserving square pixels, fixed dialogue and touch controls. Status/help and save feedback live in player-opened menus. [Deliverable](reviews/M1-UI2/README.md). Source `8afa556` is live after 115 unit and 88 browser checks. Next: user presentation feedback; no wider milestone is self-approved.

## M1.FR1 — Shakeable fruit trees

**Implemented, tested, pushed and published; fruit-tree visual/feel feedback pending.** Four apple trees use existing broadleaf footprints; A shakes three apples into the Bag with falling fruit, saved harvests and 24-hour regrowth. [Deliverable](reviews/M1-FR1/README.md). Source `089908a` is live after 115 unit and 71 browser checks. Next: user visual/feel feedback; no broader milestone is self-approved.

## M1.CF1 — Dialogue stability and contact alignment

**Implemented, tested, pushed and published; user visual/contact feedback pending.** Speech retains a fixed camera; indoor/outdoor cell anchors agree, blocked input releases immediately, and 51 new foundation/root/room boundary tiles make contact readable. [Deliverable](reviews/M1-CF1/README.md). Source `0a86c91` is live after 108 unit and 77 clean-release browser checks. Next: user visual/feel feedback; no wider milestone is self-approved.

## M1.BH1 — Rear building overlap

**Implemented, tested, pushed and published; traversal feedback pending.** Every freestanding building has at least one reachable rear row, with two behind Old Waterworks; solid walls and roof/chimney occlusion remain. [Deliverable](reviews/M1-BH1/README.md). Source `86c310e` is published after 104 unit, 15 rear-building browser and 28 entrance regression checks. Next: user traversal feedback.

## M1.DO1 — Walk-through entrances

**Implemented, tested, pushed and published; traversal feedback pending.** All usable doors and gates must work by walking without A or selection. Fix both yard boundary exceptions and show walking cues; preserve solid surroundings, story and saves. [Deliverable](reviews/M1-DO1/README.md). Source `5ba17b5` is published after 101 unit checks and 28 browser scenarios. Next: user traversal feedback.

## M1.ST1 — Stair traversal correction

**Implementation/checks/publication complete; traversal feedback pending.** The user requests Emerald-style stairs. Apply the inspected single entrance/solid surround to the two home staircases, preserve story/saves, and verify directional entry, safe arrivals and old-position recovery. [Deliverable](reviews/M1-ST1/README.md). Source `8d0b57b` is live at the existing phone URL after 98 unit, six stair-browser and 17 chapter-browser checks. Next: user traversal feedback; no broader movement milestone is self-approved.

## M1.UI1 — Menus, fast speech and NPC life

**Implementation/checks/publication complete; user feedback pending.** The user authorizes this focused Gen 3 UI/acting pass, including fast-only typing, simple menus/options, reactions and small NPC routines. Preserve the existing ecosystem/story and selected living art. [Deliverable and source research](reviews/M1-UI1/README.md) records original Critz decisions and actual checks. Source `56874e4` is published at the existing phone URL after 91 unit, 8 UI-browser and 17 chapter-browser checks. Collect user UI/feel feedback next; full pixel UI and broader movement approval remain separate.


## MUSIC.02 — Thirty independently rewritten MIDI pieces

The user rejected MUSIC.01 for sameness and excessive glides. The latest request supersedes its bending-synth direction: rewrite all thirty from the first note, with distinct musical premises, tempos, keys, meters, instrumentation and restrained arrangements informed by Minecraft/Pokémon/Terraria research. **Composition/export/player work complete, tested, pushed and published; listening approval pending.** [MUSIC.02](reviews/MUSIC-02/README.md) presents all thirty new scores and previews. No gameplay soundtrack integration is authorized by delivery. Exact next action: use the user's listening response to the published collection for refinement/selection.

## M1.I4 — Selected living collection in gameplay

**Implementation, checks and publication complete; user feedback pending.** User authorizes C7 cast/walks, animals and tanks in runtime plus indoor mats/open-entrance daylight and clock-based night. Keep 25-gallon care/earnings/save systems. Rival parents remain legacy placeholders with an idle-only agent brief; do not animate replacements before user review. [Deliverable and checks](reviews/M1-I4/README.md). Source `ce14c52` is live at the existing phone URL after 83 unit, 17 chapter and 10 integration browser checks. Collect appearance/motion feedback next; then review the two parent idles before authorizing their animations.


## M1.W1 — Playable northern overworld

**Implementation/checks/publication complete; awaiting user visual/motion feedback.** User-selected M1.E2 is integrated into Rootport → Mossway → Liarsville, with tile-built architecture, water/cliffs, gardens/fences/fountains, hollow logs and living vegetation. Existing story/save systems are preserved. Source `787d0ea` passes 78 unit tests, original chapter regression and 12 release-browser checks; its exact tested build is live at the existing phone URL. [Receipt and next action](PROJECT_STATUS.md#m1w1--rootport-to-liarsville). Refine user feedback next; do not infer approval of unrelated character work or self-approve the new world/motion.


## M1.C7 — Walks and living habitat review

**Deliverable/checks complete; awaiting visual and motion review.** User explicitly authorizes animation of the M1.C6 appearances and three habitat types. [Collection](reviews/M1-C7/README.md): twelve characters in four directions, ten animated critters, aquarium/terrarium/paludarium close-ups and world props. Frozen source idles and Boy V1 front walk remain exact. Native GIF/PNG/editor/RLE checks pass. No gameplay integration or simulation is added; new directional anatomy and habitat layouts remain original review proposals. User feedback is the next action.

## MUSIC.01 — Original 30-track soundtrack collection

**Rejected and superseded by MUSIC.02.** Historical plan follows.

Latest user request authorizes a separate music-review extension: research Pokémon composition, write 30 distinct original Critz MIDI tracks with expressive synths and every requested emotion, and present all of them without questions. **Composition/export/player work complete; awaiting user listening review.** [MUSIC.01](reviews/MUSIC-01/README.md) contains all 30 tracks, matching audio, editable sources and actual validation. Musical future-place/battle cues are proposals, not new canon or gameplay. Keep the collection separate until the user chooses integration; no visual/movement review gate is self-approved. Exact next action: user listens and selects/refines tracks. Publication evidence belongs in PROJECT_STATUS.

## M1.E2 — Full overworld tile kit at Emerald 2×

Latest user request authorizes the complete original terrain/building/garden kit as a review deliverable, superseding the older house/tree-only restriction. **Asset/checks delivered; awaiting user visual review.** [M1.E2 packet](reviews/M1-E2/README.md) includes one native master PNG, 385 named tile entries, full terrain/fence/hedge connections, genuinely modular building parts, editable source, Tiled metadata, assembly proofs and an interactive review. Source and native export checks pass; publication evidence is in PROJECT_STATUS. This does not approve the artwork, animate the kit, replace Rootport's layout, alter saves or silently integrate replacement gameplay art. Exact next action: user reviews this native revision; refine it before runtime integration or animation. Art direction belongs in ART_BIBLE.

## M1.C6 — Expanded native idle collection

**Deliverable/checks complete; awaiting native-art visual review.** The 2026-10-06 request explicitly selects the R11 girl concept and authorizes an expanded idle cast plus animals. [Nineteen new native stills](reviews/M1-C6/README.md): Girl Hero, Nugget, Mom, Kaid, both rival options, five existing Rootport support characters, four existing rescue animals and four future-species proposals. Approved Hero Boy V1 remains unchanged. Actual 32×64 character and 32×32 animal exports, editor sources, masks, native/clean/grid plates and validation are delivered. Animation and accepted runtime integration remain separate; review output does not self-approve new art.

## M1.C4 revision 11 — Girl Hero concept review

Concept delivered, awaiting user visual review. Use the newly supplied boy RLE and editor skeleton for unchanged body construction; hair adds separate volume above the skull. [R11 preview](reviews/M1-C4/revision-11/README.md) includes source data and measurement evidence. The generated enlarged concept is not a verified native 32×64 asset. Review the design before subsequent production-pixel work or animation. No accepted gameplay art is replaced.


## M1.C5 — Hero Boy V1 approved; front walk delivered

The user's exact corrected export is officially registered as Hero Boy V1 and must remain unchanged. Two original front-walk strides now surround that exact passing pose, following pinned Emerald3/0/4/0 cadence and two-target-pixel stride bob. [GIFs, sources and verification](reviews/HERO-V1-WALK/README.md). Deliverable/checks complete; animation acceptance awaits the user. Native and6× GIFs are provided with documented centisecond rounding. No side/back/run poses or runtime integration are included; prior M1.C4 assistant stills are superseded by the user-approved V1.

## TOOLS.SE8 — Reference-to-artwork and flexible colors

Complete, tested, pushed and published in revision 08. Full-opacity exact-color reference copy, artwork/reference eyedropper, 14 palettes/custom RGB, skeleton reference preset, two-finger pan/pinch zoom and color/reference-first panels are available. All 71 unit tests and 70 browser scenarios pass; exact tested archive deployed successfully. Latest user instruction relaxes editor color restrictions while preserving Wildlife values and gameplay/art review gates. [Evidence](reviews/TOOLS-SE8/README.md).

## M1.C4 revision 10 — Current selected Hero review

Local cleanup complete; visual acceptance pending. Preserve the selected layered-twists/orange-stripes native target, 32×64 frame, symmetric body, two bottom padding rows and unrestricted source colors. Apply a one-pixel pure-black outline without reauthoring the hair or copying R9 proportions. [R10](reviews/M1-C4/revision-10/README.md) supplies the native asset, countable proof and exact edit log. No animation or runtime replacement.

## TOOLS.SE7 — Construction-aware Sprite Editor

Complete, tested, pushed and published. Exact user skeleton and anatomy/shading map, fixed region masks, outline/alpha locks, palette-ramp Shade/Lighten, scoped recolor, clean view, symmetry diagnostics and lossless RLE paste/open are available in revision 07. All 67 unit tests and 60 browser scenarios passed. This authoring-tool update preserves prior reference/zoom/animation workflows and does not approve or replace gameplay artwork. [Release evidence](reviews/TOOLS-SE7/README.md).

## M1.C4 revision 9 — Current user-template idle review

Deliverable/checks complete; visual acceptance pending. Use the user's exact editor RLE skeleton, maintain X-mirrored anatomy, paint the four supplied hairstyle/outfit variants at native 32×64 with one-pixel outlines and no forced 2×2 block construction. [R9 asset packet](reviews/M1-C4/revision-9/README.md) includes PNGs, editor projects, exact RLE, metadata and native/grid comparisons with external Brendan. Keep assets review-only until visual acceptance; no animation or runtime replacement in this task. ART_BIBLE supersedes older outline-weight advice.

## TOOLS.SE6 — Pointer-anchored zoom

Complete, tested, pushed and published. Anchors wheel zoom to the chosen canvas point, buttons to the view center, and preserve integer pixel rendering. Permit panning around all edges and keep Fit as an explicit recenter action. All 60 unit tests and 49 browser scenarios passed, including repeated zoom, panning, draw coordinates, mobile layouts and existing reference/crop workflows. [Release/deployment evidence](reviews/TOOLS-SE6/README.md). Preserve palette, artwork, saves and review gates.

## TOOLS.SE5 — Visible column correction and reference crop

Complete, tested, pushed and published. Prevents reference reduction from erasing center-column edits by editing the displayed grid and retaining 1:1 corrected pixels. Add reference-only drag/numeric cropping with Apply/Cancel and full-source restoration. Preserve artwork, animation, palette, saves and review gates. All 60 unit tests and 42 browser scenarios passed. [Release/deployment evidence](reviews/TOOLS-SE5/README.md).

## TOOLS.SE4 — Side-of-center reference correction

Complete, tested, pushed and published. Replaces the old even-grid no-op with four explicit left/right add/remove treatments. Highlight the selected column, replace the viewport reference immediately on Center this image, and preserve exact original-reference restoration. Verify actual rendered pixels, odd/even inputs and hidden/mobile overlays. No game/art acceptance changes. All 60 unit tests and 36 isolated browser scenarios passed. [Release and deployment evidence](reviews/TOOLS-SE4/README.md).

## M1.C4 revision 8 — Current native pixel-art review

Deliverable/checks complete; visual acceptance awaits the user. Retain all four supplied designs and hairstyles in directly authored 32×64 pixel sprites, with intentional clusters and short color ramps. Present an unscaled 160×64 lineup with Brendan first; the user's latest native-size request overrides enlarged grids for this revision. [R8 packet](reviews/M1-C4/revision-8/README.md). R7 is alignment evidence only, and ART_BIBLE now distinguishes reference transfers from finished pixel art. Front idle only; no animation or accepted runtime artwork replacement.

## TOOLS.SE3 — Canvas-first workspace and symmetry correction

Complete, tested, pushed and published. Provides window-bounded layout, draggable dock widths/animation height, collapsible sections and animation, Focus/reset, and separate layout persistence. Includes a reversible reference-only odd→even workshop with exact center-column duplication/removal, native-grid input, before/after previews and even-center placement. Preserve artwork, exports, saves, palette, animation behavior and art-review gates. [Guide](../sprite-editor/README.md). Clean release passed 60 unit tests and 30 browser scenarios. [Deployment and validation](reviews/TOOLS-SE3/README.md).

## M1.C4 revision 7 — Current five-grid reference-led review

Deliverable complete, artwork awaiting user review. Use the actual supplied four designs at one uniform whole-figure scale, aligned to Brendan's eyes and feet, on five full 32×64 grids with Brendan first, x=16 centerlines and Y=0 at bottom. Preserve rounded cranium/hair volume and each supplied outfit. R6's shorter-head directive and forced hat-bottom hairline are revoked. [R7](reviews/M1-C4/revision-7/README.md) records actual source registration, measured bounds, native transfers and visual/check evidence. ART_BIBLE remains the only art-direction authority; AGENTS already points there. Idle only; no animation or gameplay integration. Earlier revision sections below are history, not current construction instructions.

## M1.C4 revision 6 — Current four-character review

Deliver four corrected front-idle candidates retaining the user's supplied designs, with original shorter hair/skull construction and face/body landmarks aligned to the supplied Brendan reference. Use all 32×64 grid space, Y=0 bottom/Y=64 top, x=16 symmetry, native-pixel cells and ten-height guides. [Revision 6](reviews/M1-C4/revision-6/README.md) records actual extents and source/design distinctions. ART_BIBLE is the sole art direction; AGENTS and the reusable prompt point to it. Final art acceptance awaits the user; no walking or accepted gameplay replacement is included.

## TOOLS.SE2 — Free reference transform and user palette

Completed and published editor update: 1× / 2× / Free reference scaling, automatic fit, direct move/resize/stretch, source cropping, alpha-aware area averaging plus nearest sampling, and the user's exact 32-slot Wildlife palette. Preserve old project colors and game saves. This tooling task does not create or approve game artwork. [Editor guide](../sprite-editor/README.md). Clean release passed 56 unit tests and 20 browser scenarios; deployment succeeded. See PROJECT_STATUS for receipt and limitations.

## TOOLS.SE1 — User-requested sprite authoring tool

Completed and published tool deliverable: **Free Market Wildlife Sprite Editor**, a standalone `/sprite-editor/` tool with the user's Emerald 2× canvas budgets, existing original Critz palette banks, pixel drawing/zoom, local reference overlays, exact pixel copy, project persistence and animation exports. [Editor guide](../sprite-editor/README.md). No new artwork, roster expansion, renderer migration or milestone acceptance is implied. Existing unfinished M1.I3 changes stay excluded. The new tool is usable before final art approval; it must label palette/proportion limits honestly and preserve game saves. After editor release, M1.C4 revision-3 visual review remains pending.

## M1.C4 revision 4 — Four gridded 2× Hero candidates

Current review follows the latest user request: four front-idle 32×64 options corresponding to afro/teal, flat-top/gold, twists/red stripes and cornrows/blue references. Present every option on native-pixel grids with x=16 symmetry and numbered ten-row Y guides. [Revision 4](reviews/M1-C4/revision-4/README.md) records compact-human-ear corrections and explicit proportion deviations. The requested four 2× variants supersede the earlier paired-budget layout for this review only. Await user selection/refinement; no animation, accepted art replacement or game integration.

## M1.C4 revision 3 — Target-grid contour and depth correction

Current delivered review: original 2× boy Hero idle with actual one-target-pixel contour refinement, selective colored outlines and clustered form shading, retaining measured envelopes, eye positions and mirrored anatomy. Preserve the 1× baseline, required centerline/ten-row grid and a clean before/after. [Revision 3](reviews/M1-C4/revision-3/README.md) records why exact doubled occupancy was an incorrect final-art constraint. The user must review the style before animation; no runtime migration or unrelated M1.I3 work is included.

## M1.C4 revision 2 — Measured, symmetric idle review

Delivered for user review: original boy Hero front idle at Emerald 1× and 2×, measured from pinned Brendan frame 0 before drawing, with one-pixel cells, vertical centerline and numbered ten-row horizontal guides. [Revision 2](reviews/M1-C4/revision-2/README.md) fixes material/anatomy symmetry and eye placement. ART_BIBLE now requires default bilateral front/back idle anatomy and 2× grid presentation for new characters, preserving hair/color and explicit unusual-character exceptions. Keep both Hero budgets until the user accepts the style. No walking, back-frame authoring or runtime migration is included; existing M1.I3 work is preserved.

## ART.2X — Standing Emerald proportion and resolution contract

Documentation task authorized 2026-10-02: record exact Emerald proportions/framing at 2× linear resolution in AGENTS and ART_BIBLE, align entry-point docs and supply a reusable prompt. No sprite generation, runtime migration or deployment is part of this task. The [2× contract](ART_BIBLE.md#emerald-2-visual-contract--authoritative-2026-10-02) supersedes conflicting pixel budgets and invented chibi ratios in historical task descriptions below, including M1.I3. Preserve unfinished implementation changes; do not treat them as delivered or accepted.

Next asset work must first annotate reference anatomy and pose measurements for the authorized sample, then author against exact doubled targets and present comparison evidence. The 480×320 renderer/32px map presentation migration remains planned, not implemented by updating the docs. Existing milestone scope and user visual/feel approval requirements remain in force.

## M1.C4 — Idle resolution and chibi construction review

Current review task: boy Hero only, one south idle at 16×32 and 32×64. The user requests a countable native-pixel grid, marks every ten pixels and the supplied reference’s compact body construction. Deliver original native PNGs, editable pixels, exact enlarged grids and a separate construction plate. Refine idle first; no new walking or playable integration is part of this task. [Review packet](reviews/M1-C4/README.md) is delivered and awaits user visual feedback. Preserve unfinished M1.I3 work. The ideas notebook’s separate one-tile body proposal is not adopted or resolved by these taller storage frames.

## M1.C3 — Walking animations for the current cast

The user authorizes animation of every delivered M1.C2 character. Produce original front/back/both-side walks, preserve the chibi framework and existing front idle pixels, and provide individual/full-cast GIFs plus a controllable review. Three poses per direction use source-derived 8-tick walk holds. This is an animation-review deliverable, not a gameplay replacement or new roster. Final visual acceptance remains the user’s.

## M1.C2 — User-selected 20×26 chibi still cast

Current authorized task: establish an implementable chibi drawing framework and create one south/front idle still per requested character. Use large rounded heads, compact connected bodies, distinct body shapes and original character-specific silhouettes. No new animation or game integration is requested. Export shared/individual transparent native PNGs, palettes/editable sources, labeled native/enlarged lineups, annotations and measured validation. Final review remains the user's.

The requested 102 roster is not present in the repository/history audit; clarification is pending. Continue framework and confirmed-cast drawings without inventing additional canon. See [CHARACTER_FRAMEWORK](CHARACTER_FRAMEWORK.md) and current [PROJECT_STATUS](PROJECT_STATUS.md).

Established 2026-09-24. Scope: original Critz artwork and exploration conforming to measured Emerald-era conventions while retaining the playable game. [GAME_VISION.md](GAME_VISION.md) owns canon; [PROJECT_STATUS.md](PROJECT_STATUS.md) owns current state. No artwork or gameplay rewrite is authorized by M0.

## Execution and gates

**2026-09-27 scope update: M1.I2 is authorized.** The user explicitly requests missing-art completion, main-game visual integration and tile movement together as one playable visual-review build. Implement and validate these components without intermediate gate pauses. G1/G2 final acceptance still belongs to the user after delivery; no self-approval. Existing world/story/economy preservation, isolated synthetic save testing and publication requirements remain in force. The staged milestone definitions below remain quality requirements/backlog context, not a reason to stop this authorized combined implementation.

Use `planned → in progress → awaiting review → complete`, or `blocked` with a named dependency. Only one implementation task is active. A check failure keeps that task in progress; required user approval keeps it awaiting review. Completing M0 does not start M1. Start the next milestone when the user authorizes it. User approval must cite the delivered artifact/revision and be recorded in [DECISIONS.md](DECISIONS.md); an agent cannot approve its own art.

All work stays on `main`. Existing feature history is audit evidence, not a request to create branches. Publish/deployment is separate from milestone completion. Reference artwork is for inspection only; deliver original Critz assets.

## M0 — Audit and production plan

Dependency: locate existing playable implementation and read vision/system/QA documents.

| ID | Deliverable | Acceptance and validation |
| --- | --- | --- |
| M0.1 | Repository and gameplay audit | Record remote main, existing branches/PRs, playable SHA, architecture, scene/story/control contracts, save keys/schema, test results, visual discrepancies and test gaps. Inspect actual code and rerun available baseline checks. |
| M0.2 | Reference ledger | Pin source revision; distinguish source verification from observation; record tile/palette/frame-canvas facts, measured child/adult bounds, per-animation holds, movement and camera evidence. Give each unknown a verification task; do not invent exact values. |
| M0.3 | Production documents and resume workflow | Deliver plan/status/art bible/reference ledger/decision log/AGENTS; define M1 sample precisely; confirm no runtime or vision changes. Check links, Git diff and all required sections. |

Gate G0: report M0 and exact M1 sample; await instruction to begin M1. No visual approval is claimed in M0. Exclusions: redraws, sprite production, gameplay edits, schema migration implementation, deployment, new features.

## M1 — Visual style proof

Dependency: M0 delivered; user authorizes M1.

| ID | Deliverable | Acceptance and validation |
| --- | --- | --- |
| M1.1 | Original seven-character lineup | Boy Hero, girl Hero, boy rival, girl rival, Kaid, Mom, Professor Nugget. One front pose and one side pose each, plus Kaid's opposite side to inspect his asymmetric handle/spout; shared native baseline, frame/bounding-box/eye/head guides on a separate overlay. Hero reads as a ten-year-old Black child; children/adults differ without doubled canvases. Kaid is an original pitcher child. Export 1× and exact 4× nearest-neighbor sheets. |
| M1.2 | One bedroom composition and initial tile sheet | One 240×160 composition (15×10 metatile view), original 8×8 tiles/16×16 metatiles, bed/desk/chair/window/shelf/door or stairs/25-gallon tank/plant/rug/walls/floor. Show Hero and Mom together; 1×/4× exports. Include pixel ruler and a separate ground/occlusion overlay. Reuse the actual draft tiles, not a flattened illustration presented as a tileset. |
| M1.3 | Review packet G1 | Bundle PNGs, editable sources where practical, provisional asset IDs and palettes, measured dimensions, and a short deviations list. Inspect at 1× and 4×: hard pixel edges, no stray alpha/AA, tile seams, visible silhouettes, foot consistency. User explicitly approves or requests revisions to palette, scale, silhouettes and room composition. |

Gate G1: user visual approval recorded before M2 or roster/world expansion. Exclusions: full roster, town redraw, playable movement rewrite, new canon, full production pipeline. If G1 requests changes, revise M1; do not proceed while waiting.

## M1.E1 — User-requested environment review extension

Authorized 2026-09-25: start original indoor/outdoor tiles, placeable trees and houses, research missing Emerald construction details, and present proposed Rootport, Liarsville and their short connecting forest route. This later instruction extends the earlier bedroom-only art scope **for review artifacts**, without approving gameplay integration or G1/G2.

The 2026-09-26 inventory/contact-sheet and animation gallery using existing artwork is complete and successfully published alongside the playable game; see PROJECT_STATUS for source/deployment and checks. This does not approve art, invent new animations, or begin M2. Only this implementation task is active. Revision 1 produced a draft kit and map proposals but was rejected by the user for visual mismatch. **State: awaiting review of revision 2**, a focused native house/tree proof. The broader kit and town revisions remain planned until this direction is accepted; M1.1/M1.2/M1.3 are not complete. Deliver PNGs and sources as review assets, preserve the rejected version as clearly labeled history, and record the user's response before expanding the revised artwork. Research evidence is in the [environment report](reference-data/EMERALD_ENVIRONMENT_RESEARCH.md).

## M1.I1 — Recovered-art integration review

Requested 2026-09-26: update the game using the new Emerald-style artwork, prefer one shared PNG, and retain the target of Emerald tile movement. Discovery found ten finished south-idle candidate PNGs outside this checkout; it did not find directional/animated character sheets, Mom/Kaid/Nugget sheets, or a revised indoor kit. No recorded G1 approval exists. The user has been asked whether to authorize a combined art/movement playable review or keep the staged gates; no response is recorded yet.

**Active deliverable: awaiting review; artifact and checks complete.** Recovered the original candidates and editable source, losslessly packed them with environment revision 2 into one 256×160 atlas (23 stable IDs), and provided a static 240×160 assembly review with candidate selection and foreground placement. Rejected environment revision 1 and reference-game art are excluded. This is useful preparation for the requested integration, not completion of the full reskin or M2. The preview never accesses saved game storage. New runtime integration and movement remain dependent on the user's scope/gate response. Delivery evidence is in PROJECT_STATUS.

## M2 — Movement and camera proof

Dependency: G1 approved art; unresolved critical motion details measured or explicitly labeled approximation in the demo.

| ID | Deliverable | Acceptance and validation |
| --- | --- | --- |
| M2.1 | Isolated movement harness | Approved sprites; 240×160 buffer; fixed simulation clock; cardinal 16px steps; explicit directional/frame-hold tables. An input trace covers idle, tap turn, held walk, held run, release mid-step, direction change mid-step, blocked step, input on pause/background/resume. Native coordinates are integers at render. |
| M2.2 | Two-map playable proof | Small bedroom-like room and scrolling outdoor area at least 30×20 metatiles. Include a door, corner obstacle, foreground tree/object and labeled border test. Demonstrate screen anchor, direct scroll, padding, warps and occlusion. Preserve keyboard and touch bindings. Isolate from production saves; do not activate a new movement model on the existing story yet. |
| M2.3 | Timing evidence and review G2 | Log expected/actual positions and frame indices for identical tick-stamped input traces at 30/60/90/120 Hz render schedules; outputs at equal processed simulation ticks must match. Separately test one long-frame case against the declared catch-up/dropped-time policy and show any wall-time divergence. Validate 16 updates per walk step and 8 per run step if adopted, plus documented turn/block/door rules. Provide native capture, input/tick overlay and browser play link/launch command; user approves feel. |

Gate G2: user approves movement/camera/transition feel and any deviations. Exclusions: world-wide migration, ecosystem rebalance, finalized full map pipeline, auto-approval based on tests. M2 changes the prototype's deliberate diagonal behavior in the harness only; eventual regression expectations must change explicitly.

## M3 — Reusable asset and map pipeline

Dependency: G1 and G2 approved.

| ID | Deliverable | Acceptance and validation |
| --- | --- | --- |
| M3.1 | Versioned asset/map contract | Finalize PNG sheets, animation holds, anchors, palette IDs and Tiled JSON export rules proposed in ART_BIBLE. Validate every referenced asset, rectangle, frame and map ID; reject duplicate or missing IDs. |
| M3.2 | Shared renderer and map loader | Ground, sortable objects and foreground layers; collision/interaction/warp data separate. Add a second test room solely through map/asset data, with no scene-specific renderer branch. Verify seams, foreground coverage and both directions of each warp. Include assets in build and PNG/JSON server content types. |
| M3.3 | Save migration boundary | Establish synthetic v1 fixtures for both loan paths, partial opening, all scene IDs, rescues, notebook, purchases and paid posts. If coordinates/schema change, explicit deterministic safe-anchor mapping preserves all nonposition progress and backup bytes; failures retain a recoverable old save. Repeated migration has no extra money or quest effects. |

Gate G3: checkable technical acceptance; user review only for a material departure from G1/G2. Exclusions: elaborate custom editor, mass world art, content expansion, deleting v1 compatibility. No migration is needed solely because tile pixel size changes while coordinates/geometry retain their meaning.

## M4 — Home and opening integration

Dependency: M3 validated formats, save conversion and approved movement.

| ID | Deliverable | Acceptance and validation |
| --- | --- | --- |
| M4.1 | Bedroom/house/yard maps | Integrate approved assets and map data in the existing three scene IDs; every original interaction has a reachable approach, every entrance/exit a safe spawn. Check native/4× views, collisions and occlusion. |
| M4.2 | Opening and rescue reconnection | Browser walkthrough with both Hero genders and both loan choices: named rival, compassionate Mom dialogue, all four surviving rescue groups, gift always 25 gallons, optional $100 applied once, first morning and tank menu. Preserve saved partial-opening semantics. |
| M4.3 | Compatibility validation | Load pre-migration saves in each integrated scene, continue to town and back, save/reload again; compare inventory, money, flags, tank and Critter balances. User can play the full opening before expanding town. |

Gate G4: integration review with actual opening preview and passed story/save checks. Exclusions: recurring medication setback, new rescues/species, new tanks or rewritten story.

## M5 — Rootport integration

Dependency: M4 complete.

| ID | Deliverable | Acceptance and validation |
| --- | --- | --- |
| M5.1 | Connected town and neighboring homes | Preserve `town`, `kaidHome`, `rivalHome`, three neighboring homes, entrances and return spawns; all walkable links form one reachable network. |
| M5.2 | Five businesses and NPCs | Critz, Vet, Drug Store, Bike Shop, Glow n’ Blow stay named and enterable. Professor Nugget notebook/$15 reward, free kit/foraging, prescription delivery, purchases, repayment and outdoor skateboard remain functional. |
| M5.3 | Town review | Walk every door both ways; audit all entity IDs and interaction approach cells, tree/building occlusion, map borders, shop thresholds, native readability and old-save restoration. Present town overview and a playable route. |

Gate G5: integration review; any new art family gets user review before wider use. Exclusions: Liarsville/forest access, new shops, new transport types, new quests.

## M6 — Tank and interface art pass

Dependency: M5 complete; keep domain simulation untouched unless separately authorized.

| ID | Deliverable | Acceptance and validation |
| --- | --- | --- |
| M6.1 | Tank/creature visual pass | Original reusable artwork; preserve care variables, visible causal events, births/nonlethal behavior, pan/zoom, photos and six-second simulated videos. Compare identical-state simulation/scoring before/after. |
| M6.2 | Dialogue/menus/notebook/Critter | Consistent palette/borders/icons and readable text. Tank first menu remains exactly Manage/Stats/View. Keyboard focus, full player names, scrollable content and touch targets ≥44 CSS px for primary controls; no controller/world overlap. |
| M6.3 | Interface review | Test posting/reach/exactly-once revenue, cancel/reframe, save/reload, menu time-freeze rules and every care/shop action. Screens at 320×568, 390×844, 844×390, 1280×900 with no clipped actionable controls. User reviews readability and touch use. |

Gate G6: UI/tank review; DOM readability may differ from native bitmap text if documented and approved. Exclusions: real video export, external services, altered economic balance, expanded simulation scope.

## M7 — Consistency and regression pass

Dependency: M4–M6 complete.

| ID | Deliverable | Acceptance and validation |
| --- | --- | --- |
| M7.1 | Asset/geometry/timing audit | No missing assets or unresolved blocking IDs; inspect every scene at 1×/4×, tile seams, actor dimensions, sprite holds, foot anchors, foreground order, native camera offsets and border padding. Re-run fixed-clock trace comparisons. |
| M7.2 | End-to-end regression | Both naming/loan paths, every rescue/shop/neighbor, all tank modes, earning once, old/current/corrupt-primary saves, backgrounding and touch cancellation. Chromium plus physical iPhone Safari portrait/landscape; record device/browser versions and untested cases. |
| M7.3 | Final acceptance packet | Complete playable opening, comparison captures, test report, remaining nonblocking limitations and exact launch instructions. User accepts visual/feel consistency. Status and decision log reference accepted asset/code revisions. |

Gate G7: user final consistency review; zero open save-loss, unreachable required interaction, blank-asset, stuck-input, or duplicated-payment defects. Exclusions: deferred game expansion, silent release/deployment, treating emulated mobile viewports as physical-device testing.

## Preservation and risk controls

- Reuse pure state/economy functions; new renderers consume state without changing balances or quest flags. Read [AUDIT_M0.md](AUDIT_M0.md) for concrete boundaries.
- Keep the existing story playable while M1/M2 artifacts are evaluated separately. Incremental map conversion must support old and converted scenes during M4/M5.
- Before a destructive map/save change, use synthetic legacy fixtures and a backup-preserving migration; coordinate systems must be explicit. Never delete localStorage to make a test pass.
- Test criteria apply to delivered behavior, not amount of code. Critical unresolved reference behavior must either be verified or receive a clearly stated approximation approval before G2.
- Future habitat upgrades, commissions and multiple tanks from GAME_VISION §10 remain separate backlog work.

### M1.I2 delivery acceptance

Combined playable review includes the existing 11 scenes, native shared atlas, missing directional/supporting-character/environment assets, cardinal fixed-tick motion, v1 coordinate recovery and full story regression. Final user art/feel review follows delivery at the normal play URL; G1/G2 are awaiting review, not self-approved. Existing later world/roster expansion and Tiled migration remain deferred. Implementation uses the current map module with explicit appearance/collision/warp data; introducing a new map editor pipeline is not required to play this build.

## M1.C1 — Two-budget animated character study

Authorized 2026-09-27 after the user liked the concept characters: compare three representative designs at 16×32 and 24×32 with walking animations. Independently author each budget at native resolution, preserve identity/palette, show matched timing/scale and room context, and publish a separate review. The game retains its current artwork and saves. Final budget selection and final-art acceptance await the user's comparison; this task does not authorize applying the larger standard to the full roster.

M1.C1 comparison delivery is complete. The user selected the larger 20×26 painted budget for the M1.C2 still-character pass. Final designs remain awaiting review; the existing game retains its current artwork during that design work.
