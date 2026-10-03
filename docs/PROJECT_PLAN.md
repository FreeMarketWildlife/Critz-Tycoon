# Visual foundation production plan

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
