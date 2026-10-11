# Critz: Tycoon — art bible

## M1.WA7 — Complete corrected coastal set

User requests all water/sand/grass combinations for verification. Registered inward returns curve through the connected-row overlap, joining the16px side contact and shore cap. The assembled shoreline is the union of registered water pixels; bank art and wash fronts must be clipped to this shared boundary to remove false internal tails from overlapping sprites. Use `src/coastal-composition.js` for registered tile assemblies. This supplements WA6; no change to collision, B straight contacts, mixed-depth enclosure, bank-vs-beach direction or rock placement. The complete review presents16 water/grass/sand pairs,2 sand/grass directions and56 ordered unequal water pairs, all47 shapes each, plus four rotations/mirrors, tile grid and pause. Original pixels and3.2-second loops; review-only, awaiting user visual verification.


## M1.WA6 — Raised shores, flat beaches and curved water depth edges

User correction2026-10-10 supersedes **WA5's raised shallow/deep bank artwork**. A **transition tile** contains the boundary between materials and/or traversal regions in one map cell. **Water-to-water transition:** shallow/deep edges are rounded color contours, with no earth cap, rock face, cliff or jumpable ledge. **Water-to-raised-land transition:** deep water can directly meet grass, dirt/path, soil, paving or cliff, and shows a clear cap, recessed face and dark toe. Here the user's informal “ledge” means visible shore/cliff art; it does not authorize jumping into blocked deep water. **Water-to-sand transition:** low flat shore, pale foam and wet sand, with waves advancing/receding in a3.2-second native loop. No stone bank on sand. Still puddles on sand do not receive ocean-style wave wash.

**Map rule:** all-deep water directly beside land or sand is allowed and will be common. The earlier complete shallow enclosure rule remains only for a connected water body that actually mixes shallow and deep cells: shallow surrounds the deep region, including diagonal corners. It does not require shallows in deep-only bodies. The distinction is enclosure/layout versus artwork—an enclosure's shallow/deep boundary has only a curved water-to-water transition.

**Rock placement:** no rock may occupy any transition tile. Require its cell and all8 neighboring cells to have the same identity, motion and depth. This excludes land shores, shallow/deep contours, still/moving joins and freshwater/ocean joins, including diagonal contacts. Use3 original faceted cool-gray rock variants with distinct light top planes and darker material faces. Larger stepped underwater/contact halos are separate sprites on the saved Shadows layer, never baked cast shadows. Rocks block their cells; texture and material shading remain when shadows are off. Earlier pool study moves its two rocks into full deep interiors and removes the rejected depth-bank draw. Its188-piece sheet is historical, superseded evidence.

New coastal extension supplies6,496 base32px assets plus6,016 registered shore sprites (12,512 total). Registered shore art imports the shared approved B geometry:16px structure/16px ground at straight boundaries, on a32px collision grid with64px art projection; bed and rocks use the shared contact renderer. The base bank includes:4 sand variants,48 water/ground pairs×47 join/overlay shapes,10 sand/ground directions×47 shapes,47 beach overlays×32 frames and3 rock/3 shadow variants. Existing curved water-to-water atlas and all surface loops remain. Tiled exports47 explicit3.2-second wash animations. Wash-front noise follows the same periodic tide phase; verify the wrap is no larger than ordinary adjacent-frame changes (an earlier counter-based pattern failed this check and was corrected). Full avatar, minute clock, freshwater reflections, ocean exclusion, still-shallow-only rings, Sunny10am–3pm clouds, night stars, turtles/fish and no-fee6am–2am sleep remain. This is a separately labeled M1 visual review, not accepted-map integration; the concurrent approved CT4 contact integration is preserved. [Review and evidence](reviews/M1-WA6/README.md).

## M1.WA5 — Enclosed deep water and submerged depth banks

**Mixed-depth enclosure rule:** If a connected water body contains shallow and deep water, every deep area must be completely surrounded by at least one full tile of shallow water. Deep water cannot touch grass, dirt, paving, cliffs or any other land, even diagonally. The shallow border continues around every corner; it cannot be a partial strip. Separate shallow-only puddles and separate entirely-deep water bodies are allowed. Connectivity includes diagonal contact. This supersedes the striped mixed-depth demo layout.

The depth edge is a **collision transition / submerged depth bank**, drawn with a bright cap, recessed rock face, cracks and dark toe. It has ledge-like artwork but is not a jumpable **ledge**: whole deep cells remain blocked, including their drawn transition pixels. A shallow surface transition remains walkable. Each of the four deep identity/motion combinations has all47 canonical neighbor masks in a separate188-piece native32px extension. Surface loops remain3.2 seconds. Freshwater character reflections, ocean exclusion and shallow-still-only rings remain unchanged. Left demo pool is Still Water with a Shallow Still Water border; right is Moving Water with a Shallow Moving Water border. New layout validation rejects direct and diagonal land/deep contact in mixed bodies. These are review visuals, awaiting the user; no wider visual/movement gate or accepted-map integration is approved.

## M1.WA4 — Corrected corner geometry and sunny cloud reflections

User correction2026-10-10: fix the corner pieces visible in the water demo and replace ellipse-based clouds with convincing upside-down reflected clouds. Match inward-corner cutouts to the five-pixel straight shoreline inset in both authored PNGs and runtime masks; the old eight-pixel notch caused a three-pixel mismatch at shared edges. Preserve all6,648 tile IDs/coordinates and all256 existing water-animation frames. Verify every shared edge across all65,536 four-by-four neighbor layouts. Original clouds use hand-drawn stepped silhouettes, **three opaque colors plus transparency**,96×64 native frames and explicit vertical inversion. Broad connected highlight/body/shadow clusters replace stacked ellipses. Three variants; minute-by-minute lighting studies10am–3pm shift sunlight from **east/right** through overhead at noon toward **west/left**. This is a proposed Critz solar arc, not verified Emerald lighting. Show clouds only in Sunny review weather, from10:00am inclusive until3:00pm exclusive; Overcast/Rain selector demonstrates suppression without adding adventure weather/save rules. Night stars and existing reflections/footsteps/Calm/shadow controls remain. Pinned Emerald cloud sprite has64×64 allocated source pixels, uses blended-object mode, priority3 and five nonzero palette indices; three colors is the user's stricter Critz budget. Source image/code inspection is not our own emulator capture. [Evidence and review](reviews/M1-WA4/README.md). New cloud/corner visuals await user review; praise does not self-approve them or wider gates.

## M1.WA3 — Water identity, shallow traversal and reflected skies

User correction2026-10-10: name the four surfaces **Still Water, Shallow Still Water, Moving Water, Shallow Moving Water**. Keep freshwater/ocean identity independent: freshwater always permits character reflection at either depth; ocean never reflects characters. Only shallow still footsteps make circular ripples. Shallow cells are walkable surface transitions; this latest request supersedes the earlier wholly-blocked-water rule for these new review shallows only. Deep water/raised banks and rock footprints remain solid. Original 32px water extension includes every ordered water pair and five ground families, each with all47 canonical corners/edges; append a separate stable-ID Tiled bank without changing earlier atlases. Deep shoreline has a recessed earth cap/face/toe; shallow rims stay low and traversable. Surface animation loops3.2 seconds. Actor reflection uses current pose, vertical inversion, palette tint, water clipping and doubled four-pixel foot offset; moving reflection uses restrained hard-pixel distortion. Ring cadence follows pinned Emerald's79-tick ripple table, with original pixels. Daytime drifting cloud reflections and night stars remain original Critz artwork; stars are a Critz extension, not a verified Emerald nighttime feature. Sky reflections can appear on ocean, while ocean character reflections stay prohibited. Calm and independent shadows remain available. [Source evidence, screenshot interpretations and review](reviews/M1-WA3/README.md). User praise authorizes this next review deliverable; it does not self-approve the new visuals or integrate them into accepted maps.


## M1.WA2 — User-liked water study refinement

On 2026-10-10 the user says “I love it!!!!” about the published WA1 study and requests minute-by-minute clock text, the main game's tile-based walking in the test, and smooth water loops no longer than ten seconds. Preserve the liked water palette and all twelve rock/turtle/fish/splash sprites pixel-exact. Replace the eight-frame partial translation (which jumped back at its wrap) with a complete 32-position toroidal translation, one native pixel per 100ms frame: **3.2 seconds**, including the final-to-first step. Keep native hard pixels and nearest-neighbor rendering; smooth motion does not mean softened artwork. Calm still freezes water. Reuse `src/movement.js` for committed steps, turn/blocked behavior and walking poses; whole water and bed cells remain solid. Clock display derives individual minutes from the existing fractional saved clock, retaining the same 28-minute day and v1 representation. Praise records the liked WA1 direction; the new animation refinement awaits user feedback and does not approve wider M1/M2 or authorize unrelated world integration.

## M1.WA1 — Water/wildlife and Stardew-inspired daylight

User direction2026-10-10: animate water, turtles sliding from rocks on approach, and fish breaching around sunrise/sunset. Original32px native cells, eight-frame moving ripple clusters with wrapped joins; restrained cyan/teal ramps, compact segmented olive shells, cool-gray rocks and silver/teal fish. Source and exported review bank are `art/source/water-wildlife/` and `assets/review/water-wildlife/`. No source-game pixels, blur or filtered resampling. Cast shadows stay on the independently toggleable render layer; material shading is retained. Calm freezes ripples and removes jump/slide motion.

The requested permanent clock supersedes M1.UI2's former time-in-menu-only instruction for this one compact display. Use the upper-right wood/paper date/time/dial/money grouping as reference, with original readable Critz text/icons. Current deliverable uses day numbering and sky phase; do not claim a pixel-exact Stardew HUD, measured native font or existing weather/season simulation. Spring/summer8pm onset and gradually deepening outdoor darkness are reference-documented; warm dusk,6–8am dawn,8–10pm ramp, continuous indoor tint and stepped local lamp pools are proposed Critz treatment. Clock/sleep rules are authorized gameplay, while new wildlife pixels/preview local light remain an explicitly labeled review deliverable. The user alone accepts the new visual/motion result. [Evidence and limits](reviews/M1-WA1/README.md).


## M1.LG2 — compact greenhouse, effect layers and rare fish

User feedback on 2026-10-09 explicitly likes LG1 and asks for this refinement; new LG2 art/motion remains a review deliverable. Use a 13×17 native-cell room (416×544), centered door cell(6,16), three-cell central aisle, four96×64 tubs at x2 and four at x8, rows4/7/10/13. Mirror paired tub planting and pump/airline art. Equipment occupies the outer1×2 cells alongside each tub; crossing rows remain clear. Three display aquariums balance the back wall. Original character/fish assets stay intact.

**Standing shadow rule from the user:** all future cast/contact shadows belong to a separate render layer controlled by the saved **Settings → Shadows: On/Off** preference. Do not bake cast shadows into new sprites. Greenhouse uses a disposable native-pixel mask with restrained teal opacity, stepped moving roof/leaf shadows and actor contact shadows; off clears the mask entirely. Calm/reduced-motion makes atmospheric shadows static. Material shading, dark tub interiors and intentionally concealed fish silhouettes are not cast shadows and remain visible. Shared preference key `critz.render-settings.v1` is independent of progress; legacy world renderer migration is outside this focused review.

Dorothy is an original ordinary orange common goldfish with no special decoration, kind16, coded legendary rarity; a separate golden mascot hops around all eight tubs on a loop. Existing sixteen fancy designs are retained. Each fish supports twelve temporary exuberant shiny palettes, keeping face/outline contrast, with small native-pixel sparkle crosses at reveal. Never show hidden odds or eligibility hints in player dialogue. Neither sparkling fish nor shadow animation uses blur or smoothed scaling. [LG2 art/evidence](reviews/M1-LG2/README.md).


## Transition-tile contact study — M1.CT1, user correction

**Terminology:** a **transition tile** joins materials and/or traversal regions inside one map cell. A **surface transition** joins walkable surfaces (grass/dirt/path) and can remain walkable. A **collision transition** contains solid structure plus ground (building/grass, indoor wall/floor, cliff/ground); its **entire cell stays blocked**, including visible ground. Doors are separate explicit entrance cells, not an excuse to make structural boundary cells walkable. A **cliff** is a mountain/raised-terrain edge or wall. A **ledge** is the short directional obstacle crossed by a one-way jump. **Ground footprint** is the actual blocking region; **overhead projection** is roof/canopy art that can cover a character standing on clear ground behind it.

**Approved by the user, 2026-10-10 — B, 50% structure / 50% ground.** The user explicitly says “B is perfect for us” after the one-full-tile-south CT3 correction, and authorizes integrating this contact rule into every building and static collidable. This supersedes the earlier unselected A–D study and four-pixel-ground baseline. B is a Critz design decision, not a universal Emerald measurement. Historical alternatives remain labeled comparison history.

Use a16-native-pixel structure/ground split at every straight exposed boundary, vertically and horizontally. Preserve the approved bottom-center actor anchoring and whole-cell collision; do not change movement or saved cells to fix art spacing. North/south contact planes are registered around ground foot anchors, placing the front visible base16 pixels beyond the last solid row’s grid edge; Hero’s front idle foot baseline is14 pixels farther south. Side contact trims leave16 pixels of surrounding ground at exposed multi-cell edges. Corners, connected runs and single-cell caps join those half-cell edges; the percentage describes the straight boundary, not the occupied area of every irregular corner/canopy tile. A one-cell cap keeps a16-pixel-wide structure centered between ground strips. Connected fences/hedges/cliffs must retain joining center segments; never trim each piece into disconnected posts.

Apply this contract to all current houses/storefronts/greenhouse facades, indoor/outer walls, cliff faces, solid water/depth banks, fences/gates, tree roots, bushes/hedges, rocks/boulders, planters, benches/logs/fountains, furniture, counters, aquariums, tubs/equipment and stair rails. Ground transitions need north/south/east/west edges, corner/cap/junction compositions and the actual grass/path/paving/soil/floor beneath them. Preserve existing explicit doors, passages, stairs, one-way ledges and walkable shallows. Decorative vegetation and moving characters do not gain collision merely because they share this art family.

Keep ground footprint distinct from overhead projection. Roofs and canopies can cover a character on clear rear ground, while lower-body contact stays on ground. Translate/crop native structure pixels and reattach native edge trim; do not rescale buildings or alter Hero anatomy. The named approved contact bank in `assets/playable/contact/` is the runtime tile/assembly source; previous source/review PNGs remain historical inputs, not alternative accepted rules. Independent indoor/greenhouse/water renderers must use `src/contact-rules.js` too. Optional haptics remain feature-detected; physical support is never inferred from an API return value. [Implementation and coverage](reviews/M1-CT4/README.md).

## Map authoring review — M1.ME1

The user commissions a terrain-aware map editor, whole-building stamps, explicit collision, cliff openings, directed ledges and Hero testing. Keep this as a separate review tool; it does not replace accepted maps or approve new art. Reuse the exact existing native 32px environment and selected living Hero. Add an editor extension sheet with stable named terrain-pair corner banks, fence/ground compositions, mountain walls, cave mouths, stairs and directed ledges. Author hard native pixels with the existing grass/stone/wood/water ramps; no reference-game pixels ship. Terrain, fence and cliff pieces compile to one ground metatile per cell; planters and pushable boulders retain explicit object semantics. Roof/canopy projection is independent of solid footprints.

Water edge cells, including their grass strip, are wholly blocked per this request. Mountain walls are solid; stairs/openings carry explicit walking behavior; short ledges permit a directional two-cell hop only to a clear landing. These are editor rules, not artwork-derived collision. Original Emerald data informs map sizes, connections and behavior; automatic neighbor selection is our authoring feature, not a claim about Game Freak’s original editor. All new extension art and testing feel await user review. Keep specifications here and source evidence in the M1-ME1 review record.

## Luke’s Greenhouse — M1.LG1, user direction 2026-10-08

The user commissions Luke (brown hair, full beard, bright blue eyes), his greenhouse and a paid silhouette-scoop encounter. **Luke’s Greenhouse supersedes the old Nuggets sign. Luke is the sole goldfish seller in the entire game.** This authorizes a concrete playable review of this new character/location/interaction; it does not self-approve the art or the broader M1/M2 gates. Other IDEA-003 creators stay planned while this implementation task is reviewed.

Use the authoritative Emerald 2× standard: original native 32×64 Luke, 32px environment cells, bottom-center anchor (16,64), one-native-pixel contours and compact adult anatomy. Reuse the C7 adult scaffold rather than inventing a larger frame-filling adult. The reference dimensions, original adult adaptations, exact actual extents, photo context and unresolved hidden anatomy are recorded in [the art evidence](reviews/M1-LG1/art-notes.md). Luke’s maroon shirt and blue eyes distinguish him without logos. The real creator’s identity supplies visual inspiration; the dialogue, admission and scooping behavior are fictional user-directed game choices.

Compose an airy glass-and-green-frame greenhouse with eight large black planted tubs, wall aquariums, warm brick paving, accessible approaches and a clear exit. Tub water, planted rims and contact shadows belong in separate native sprites, with explicit solid footprints. Use native 96×64 world tubs/tanks, four planting variants and a separately authored 240×160 top-down tub closeup. These are Critz proposals, not claimed Emerald prop measurements. Show fish swimming visibly in the room; during selection conceal colors while retaining individual body/head/tail silhouettes. Ranchu lack a dorsal fin; oranda retain one. Sixteen original named individuals have soft chubby cheeks, rounded head growth, tiny eyes and puckered mouths; front portraits support a celebratory reveal. Do not imply these invented names/patterns are Luke’s actual merchandise.

The closeup displays at uniform nearest-neighbor 2×; reveal portraits can enlarge the same authored pixels for inspection. No blur or arbitrary resampling may supply native art. Keep controls at least44 CSS pixels, include keyboard aim/scoop and a Calm option. The short net travel delay makes timing matter; missed scoops retry without another charge. Show one actual captured fish, then permit free browsing until exit. The review uses its own wallet/collection and never reads the adventure’s v1 save. Full aquarium care/stocking and world placement remain subsequent integration work after feedback.


## Music accepted for gameplay — MUSIC.03

On 2026-10-08 the user said the MIDI rewrite was “much better,” requested the approved tracks be saved for future use, asked to delete the rejected ones and explicitly authorized in-game placement. This supersedes MUSIC.02's former listening-review-only restriction. Keep the thirty approved note files unchanged when moving them into canonical assets. Use the original stable-pitch timbre families, modest background volume and gentle transitions; home/care cues remain warm, and the opening distress uses sadness rather than treating Mom as a horror character. Future battle/place tracks may remain saved without inventing new gameplay. Keep Music and a touch-friendly volume slider in Options, with preferences separate from progress. [Runtime architecture and chosen placements](AUDIO_ARCHITECTURE.md). This music approval does not approve unrelated artwork or movement.

## Lived-in terrain and clear paths — user correction, M1.E3

The user rejects the flat grass/dirt and misplaced flowers/fences, and explicitly requests richer terrain in the current world. Preserve the liked rooted flower animation. Author clustered turf, connected darker grass patches and warm worn trails with restrained stone/scuff variation. Use named native palette ramps, hard pixels and complete inner/outer corner banks; avoid an evenly repeated noise pattern. Keep characters, doorways and road direction more prominent than ground detail. Append revised terrain under stable IDs in the master PNG; retain every preceding tile and animation cell unchanged.

Road, paved-lane and bridge cells must never contain a fence. Fence end tiles must match the rails actually remaining after a gate or road opening. Flower roots belong on grass or planted soil, never the road or a solid prop footprint. Place turf islands only on grass and retain the tall-grass route crossing. Clear misplaced obstacles without adding new blocked cells or invalidating old save positions. Existing forest assemblies may fill the non-playable backdrop exposed by an expanded viewport; they are scenery, not new map space. The current refinement is authorized for gameplay, with its visual result awaiting user feedback; no broader art gate is self-approved.


## Uninterrupted play area — user correction, M1.UI2

Remove all floating tips, proximity prompts, location banners and reward toasts. Remove the title/status/quest chrome around the world; put money, location/time, objectives, help and studio links inside player-opened menus. Preserve actual story dialogue, choices and character reactions. Action/validation/save feedback belongs inline in the open menu; retain nonvisual accessible announcements. Failed background saves remain reported when the next menu opens.

The world fills the top edge and the entire area above the touch controls; short landscape layouts reserve a right-hand control column. Expand the framebuffer field of view to fill the available space with uniform nearest-neighbor pixel scale, rather than stretching or cropping a fixed 480×320 view. Retain integer upscaling where space permits and uniform downscaling on narrow phones. All terrain culling, camera bounds and day/night overlays use the actual framebuffer. Conversation must never change its size or camera target. Keep touch controls safe-area aware and at least 44px. This latest direction supersedes earlier fixed-frame presentation and automatic doorway-cue requirements; it is a Critz layout decision, not a newly measured Emerald fact.


## Shakeable fruit trees — user update, M1.FR1

The user authorizes fruit-bearing trees and shaking them in gameplay. Place four apple trees in the existing yard, Rootport, Mossway and Liarsville by reusing the selected broadleaf footprint; do not block another walking cell. Append the ripe crown and apple pickup pixels to the master PNG, retain the bare rooted tree and all previous tile pixels/IDs, and show three clearly readable red apples against the foliage. Fruit is a new original Critz design, not copied reference artwork.

Shake the crown by a few integer native pixels while roots and camera stay fixed. Falling apples briefly bounce at the tree base before collection feedback; Calm removes the shake/fall motion while preserving harvest and accessible feedback. Ripe and harvested art must agree with saved per-tree regrowth, and both occupied root cells must be interactable from an adjacent clear cell. The current gameplay choice is three bag apples per tree with regrowth after 24 saved habitat hours. No feeding, selling or new animal rules are implied. [Deliverable](reviews/M1-FR1/README.md). Visual/motion feedback remains the user's decision.

## Stable dialogue and readable contact — user correction, M1.CF1

Conversation must not move the camera or resize the world. Use a compact two-line overlay with a 44px confirmation target; show the scene from the same camera target before, during and after speech. Actor reactions may move an actor, never the whole scene.

Use the same bottom-center ground-cell anchor indoors and outdoors. At the current 32px map scale, saved cell `(x,y)` renders the frame anchor at `(32x+16,32y+32)`; the 16px movement units remain internal transport coordinates. Props keep their authored ground footprints. Check visible contact from all four directions instead of compensating for an anchor mismatch by arbitrarily shrinking collision. Visible room borders, stair lips and threshold decoration must align to the occupied cells. A released blocked attempt returns to idle immediately, with no displacement or camera bump; committed walking steps still finish normally. This release policy is a Critz responsiveness choice, not a new Emerald timing measurement.

Use explicit foundation/ground metatiles: the M1.CF1 additions have a stone contact edge and four rows of surrounding grass, path or paving inside the blocked base cell. Trees use spreading roots to make their two-cell trunk footprint visible; canopy projection remains separate. Preserve source tiles under their existing IDs and append revised pieces under new stable IDs. Current additions: 42 foundation variants, four tree-root pieces and five indoor boundary pieces in the master PNG. Check native pixels, clear neighboring cells, all doorway/stair approaches and saves alongside phone views. [Deliverable and evidence](reviews/M1-CF1/README.md). Visual/feel acceptance still comes from the user.

## Walking behind buildings — user correction, M1.BH1

Freestanding buildings must allow at least one walkable map row beneath their rear roof projection. Author deeper overlap for larger or taller buildings where the assembly supports it; the Old Waterworks uses two rows. Store this as explicit per-building rear depth, separate from the full visual rectangle. Preserve the solid walls and wall-base/ground boundary cells. Roofs and attached chimneys cover the actor behind them; actors on the front side draw in front. Connect the rear strip to reachable clear ground and check the entire strip for accidental tree or prop blockers. Cropped boundary facades whose rear lies outside the map are an explicit exception, not an excuse to block freestanding houses.

Verify actual movement, blocked wall contact, native renderer occlusion and save/reload on the newly walkable cells. These depths are original Critz choices following the user's direction, not newly measured Emerald facts. [Implementation and checks](reviews/M1-BH1/README.md).

## Walk-through entrances — user correction, M1.DO1

Every usable doorway, gate, stair entrance and route connection must work through directional movement alone. No option selection or A press is required. Keep the approach and threshold walkable, trigger travel when the entrance step completes, and leave the player on a clear destination landing. Sideways movement across a storefront must not enter it. Entrances need no popup cue; their authored openings and in-world signs communicate the route (M1.UI2). Any optional compatibility shortcut must never substitute for a tested walking path. Explicit portal cells may cross a map’s ordinary walking boundary; adjacent walls/fences remain solid. [Implementation and checks](reviews/M1-DO1/README.md).

## Stair construction and traversal — user correction, M1.ST1

Treat indoor stairs as a solid stairwell with **one clearly readable entrance and landing**, following the inspected Emerald house-map pattern. Rail, side and back cells block movement. The player enters from the opening and travels when the entrance step completes; they cannot roam over the entire stair graphic or activate it through a side wall. A shortcut, when offered, must use the same landing and facing. Match the visible stair mouth to its entrance and keep the arrival landing clear, facing away from the stairwell. Overlapping art never substitutes for explicit collision/warp metadata. Existing saves inside a corrected footprint must recover safely without losing progress.

[Reference evidence and Critz implementation](reviews/M1-ST1/README.md) separate the pinned map/collision facts from our footprint, layout and transition choices. This does not impose indoor warp behavior on outdoor steps: an outdoor stair flight needs its own authored traversable lane, blocked edges and connected landings. Check actual movement from all sides and both ends before integrating either kind.

## Object-to-ground boundary tiles — user correction, DOC.EDGE1

**Mandatory construction rule:** author deliberate boundary tiles wherever a solid object meets the ground. A building's bottom wall/foundation and the adjoining grass belong together in a reusable boundary metatile. The object may end partway through that cell; the remaining pixels show the surrounding ground and a deliberate contact edge. Do not require the wall to fill the entire cell or end exactly on a grid line. This is the user's requested Emerald-inspired construction principle, recorded as Critz direction rather than a newly verified reference measurement.

For our current 32×32 map cells, provide repeating wall-base/ground centers, left/right ends and corners, plus doorway/threshold transitions. Supply grass, dirt or paving variants where those surfaces actually meet the object; adjacent ground texture, palette and contact shadows must join cleanly. Apply the same principle to fence and garden bases, tree roots, rocks, cliff feet and fountain rims. Keep these parts organized under stable IDs in the master tileset, with explicit assembly metadata. Layered source art is allowed, but the reusable boundary composition must be intentional and inspectable.

**Grass visible inside a solid boundary cell does not make it walkable.** A wall-base-plus-grass cell is blocked as a whole because it contains the building's ground footprint. Store that collision explicitly alongside the map assembly; never infer it from alpha or the proportion of grass pixels. The neighboring clear ground cell remains walkable. Doorway/threshold cells have their own explicit entrance/warp behavior and reachable approaches. Distinguish solid contact from overhead art: a roof overhang, canopy or cast shadow alone does not make the ground below solid.

Before integrating or revising an environment assembly, inspect its repeating edges and corners at native size, then inspect an overlay of the actual collision cells with the Hero standing on the adjacent walkable row. Confirm the Hero cannot step into the wall-base boundary, doors remain reachable, and ground joins have no gaps, abrupt material seams or accidental extra blocked rows. Existing assemblies must be audited against this rule during their next environment correction; this documentation update does not certify or repair their current pixels/collision.

## Menus and acting — M1.UI1, user update

The user explicitly requests Gen 3-inspired menu/dialogue simplification, always-fast typed text, punctuation reactions, short cutscene hops/looks and NPC walking paths. Full pixel-art UI is deferred. Use quiet warm-paper windows, clear dark borders and a single visible selection cursor; keep original Critz labels and accessible DOM text/touch targets. Maintain Manage/Stats/View and every existing care/story option. Color frames may vary between Leaf/Ocean/Sunset without changing layouts. [Research, implementation and review](reviews/M1-UI1/README.md).

Speech is paged into two readable lines, types ordinary graphemes at the source-derived Fast cadence, and offers immediate page completion on A/B before advancing. No Slow option or extra punctuation wait. Keep people and reactions visible above the window on narrow phones. Use original native-grid exclamation/question balloons, brief 8px hops for cheerful beats and restrained surprise for distress. Calm suppresses hop/look/bob flourishes; existing character sources remain untouched. NPCs use short clear-ground paths and glance/face poses; reserve moving cells and keep doorway approaches connected. Acting is transient and must never change story saves or imply approval of the full movement milestone.


## Living collection integration — M1.I4, user update

The user now explicitly selects existing M1.C7 living-collection-v1 assets for gameplay, including walking characters, animals and tanks. This supersedes the preceding C7 no-integration restriction for that collection. Preserve exact source pixels: native 32×64 characters, 32×32 animal studies, 192×144 layered close-ups and separately authored 96×96 world props. The world framebuffer stays 480×320; do not enlarge the new character sprites a second time. The close-up UI presents its authored image at nearest-neighbor 2× in a 384×288 canvas, fitting uniformly on smaller phones. Retain accessible DOM controls and Manage/Stats/View; display scale does not increase the art’s native budget.

The rival’s mother and father lack selected C7 sets. Keep their legacy placeholders until the user reviews one south-facing idle each; no parent animation is authorized before that review. [Integration, limitations and idle-only prompt](reviews/M1-I4/README.md). Existing furniture and broken-tank story art remain until corresponding replacements exist.

Closed exterior doors map to horizontal indoor floor mats; open exterior entrances map to a readable threshold and stepped daylight cast inward during daylight. Glow n’ Blow and Waterworks use the open treatment. Original dawn/day/dusk/night tint follows the saved simulation clock, with the opening’s night overridden explicitly; do not claim Emerald had this lighting system. Native art pixels remain unchanged beneath scene lighting. Animals shown in display habitats/field-guide studies do not imply ownership, compatibility or new simulation species. Keep the 25-gallon gift and all care/earnings/save behavior.


## Playable overworld — user update, M1.W1

The user explicitly selected the M1.E2 tileset for world integration and authorized Rootport, a short northern wooded route through tall grass to Liarsville, hollow logs and environmental animation. This supersedes the preceding static-review and old world-expansion limits for this task. New composition/motion awaits feedback; unrelated character reviews remain separate.

[World deliverable and research](reviews/M1-W1/README.md). Keep the selected 385 original cells unchanged and append to reserved master slots. The active atlas has 588 named cells in the same 1024×1024 sheet. Rootport uses warm cottage lanes and a communal spring; Liarsville uses broader stone waterworks, a clock plaque, timber millhouse and waterwheel. Mossway connects their watercourse history through trees, a grass meadow, logs and a spillway. History must appear in materials, shared structures and inspectable details, not only exposition.

Use native 480×320 outdoor rendering, 32-pixel cells, quiet ground, rooted flower sway and local contacted-grass motion. Shared terrain animation stays on fixed banks. Tree footprint and depth ordering are independent of canopy alpha. Preserve logical save/movement units; display doubles spatial pixels without changing cadence. Retain existing character/interior artwork until its own authorized integration. Phones below 480 CSS pixels fit the whole frame uniformly; document that physical pixel scaling is fractional there. Visual and movement approval still comes from the user.


## Current motion and habitats — M1.C7

The user explicitly requested walks for the M1.C6 cast and critters plus an aquarium, terrarium and paludarium, with more critters where useful. **Animation and habitat artwork are now authorized**; older idle-only limits are historical. Use the native stills as frozen source appearances. Keep approved Boy V1 and its existing front walk untouched. New back/profile views, strides, critter movement and habitats remain review proposals until accepted. [M1.C7 GIFs, grids, sources and actual checks](reviews/M1-C7/README.md).

Character sets retain 32×64 canvases, anchor (16,64), four directions and stride/passing/stride/passing holds 8/8/8/8 source ticks. Passing feet end on row 61; strides may reach 63. Original front-idle RGBA remains exact in passing poses. Side bodies retain compact torso mass and an attached neck: never reduce them to a thin column beneath a floating head. Outer garments remain recognizable on back/profile views. Draw Kaid's handle/spout relationship explicitly; a blindly mirrored profile is insufficient. Source cadence and 2px bob reuse pinned evidence; new side/back anatomy is original Critz construction, not new Emerald measurement.

Critters use species-specific crawl, scuttle, glide, hop, swim and paddle movements in 32×32 frames. Do not impose a human gait on every organism. Keep moved appendages connected: tail fans, frog hips, gecko joints and insect feet need explicit transition cells, not merely translated boxes. Verify every pose and GIF loop independently, and inspect native/enlarged frames. Tiny organisms remain observation-scale art, not biological-size comparisons. Crab/catfish are visual proposals, not new care or stocking rules.

Habitat close-ups use 192×144 native cells, separate back/foreground layers, and animated inhabitants/effects. Separately authored 96×96 world props preserve native density; they are not downsampled screenshots. These are original proposed art dimensions, not Emerald measurements or gallon ratings. Aquarium: submerged plants, filter and sand. Terrarium: dry substrate, hide, dish and ventilation. Paludarium: retained land, shore, water and planting. Feature one species per demonstration; artwork does not authorize mixing animals, changing the 25-gallon gift, or adding ecosystem/world functionality.

Native PNG/indexed/RLE and native GIF palettes are authoritative. Labeled composite GIF galleries may normalize timing or reduce their display palette; never feed them back into production sprites. Preserve source ticks in editor files, document GIF centisecond rounding, and keep guides out of native sprites. Art direction stays here; AGENTS.md remains a pointer.

## Music review direction — MUSIC.02 supersedes MUSIC.01

The user rejected the first collection for similarity and excessive, unstable-sounding glides. Rebuild each song from a fresh musical idea; changing tempo/key alone is insufficient. Favor minimal arrangements with individual phrase shapes, forms, harmonic rhythms and instrument roles. Draw broad genre lessons from Minecraft/Pokémon/Terraria without copying tunes or sound banks. The replacement edition uses fixed A440 pitches: no melodic pitch wheels, portamento, detuned unison, pitch vibrato, chorus or tape wow. Sine, triangle, square, pulse, saw and acoustic-inspired sounds must have distinct timbres; full drums belong only where the individual piece benefits. Silence is part of the arrangement. MIDI does not embed these waveforms; provide editable MIDI plus honest custom-synth previews. Preserve the compassionate story and leave musical/future-battle proposals outside gameplay until selected. Technical diversity/tuning checks do not replace the user's listening approval. [MUSIC.02 research and decisions](reviews/MUSIC-02/RESEARCH.md) · [All thirty new pieces](reviews/MUSIC-02/README.md).

## Music review direction — MUSIC.01

The user explicitly requests 30 original MIDI tracks with creative bending synths, strong emotional storytelling, Pokémon-informed research, wholesome nostalgia and optional lo-fi. The review collection uses memorable question/answer melodies, independent responding voices, varied meters/grooves, expressive pitch scoops, warm keys, glass/bubble tones and restrained ambience. Preserve the compassionate story: Mom's music is tender, animals survive, and battle/future-place cues remain labeled musical proposals. Never ship reference-game melodies, recordings or sound banks. MIDI performance data and the custom-synth audio are distinct deliverables; arbitrary MIDI playback will use different instruments. Technical checks do not replace the user's listening approval. [Research, original composition decisions and measured limits](reviews/MUSIC-01/RESEARCH.md) · [All 30 tracks](reviews/MUSIC-01/README.md). No gameplay soundtrack integration is authorized by delivery alone.

## Overworld master tileset — user update, M1.E2

The user authorizes a full original overworld kit evoking Emerald's Littleroot/Oldale garden-town feeling: **water, cliffs, buildings made from tiles, fences, gardens and fountains**, at the established 2× linear budget. This supersedes the older house/tree-only restriction for this review task. It does not approve finished art or replace accepted gameplay artwork. [Review 01](reviews/M1-E2/README.md) awaits the user's visual response.

Use one master PNG plus stable metadata. Review 01 uses a **1024×1024 sheet, 32×32 map cells, four 16×16 base tiles per cell**. Reserved transparent slots are not finished tiles. Keep grids, labels and reference art out of the master. Sample at integer coordinates with nearest-neighbor filtering; generate padded runtime exports if filtering/mipmaps are later enabled.

The pinned ledger's selected 80×80 house, 32×32 tree assembly and 16×32 door redraw become **160×160, 64×64 and 32×64**. The 224×160 shop, 64×96 cypress, 96×96 / 160×96 fountain basins and footprints are **Critz proposals**, not Emerald measurements. Show the unchanged approved Hero in native 480×320 context. Roof, wall, window, door, eave and foundation parts must really repeat; prove a second building width using shared center modules.

Material direction: ivory walls, terracotta and lagoon-teal roofs, yellow-green upper foliage over connected darker bases, warm stone, golden paths and blue-teal water. Keep ground quiet and entrances readable. Use single target pixels for roof curvature, leaves and stair-step edges; shingles must show overlap and plane direction rather than read as wall bricks. Retain short wall fronts and mostly hidden trunks. The review's 59 used opaque colors are an actual inventory, not a universal cap or a fourfold palette allowance.

Supply inner/outer terrain corners, narrow connections and islands. Review 01 has all 47 normalized eight-neighbor shapes for path, water bank, paving and soil, plus sixteen cardinal fence/hedge connections. Inspect assemblies and test joins: the first implementation's inner-corner mismatch was caught by edge comparison and corrected. Supply cliff returns, repeated faces/feet, corners, stairs, bridge decks and rails. Connect both bridge ends to dry ground and south-facing doors to approaches.

This review is static; animation follows visual review. Keep ground, decals, objects and foreground separate, and never derive collision from alpha. Tree ordering and footprints need deliberate runtime integration later. Asset validity does not establish visual acceptance.

The generated design study had irregular spacing and raster artifacts. Retain it as provenance; author and verify the native kit independently. Do not promote a generated contact sheet to a working atlas merely because it resembles modular art. Deliver editable pixels, IDs, assembly recipes, native crops, exact enlargements, hashes and actual checks.

## Current cast and animal direction — M1.C6, 2026-10-06

The user explicitly requested native idle sprites for Girl Hero, Professor Nugget, Mom, Kaid, additional characters and animals, and praised the R11 girl design. **Roster expansion for this idle review is authorized.** The selected girl concept supplies approved design direction; its generated raster is not itself an approved native sprite. [M1.C6 collection and grids](reviews/M1-C6/README.md) contain eleven new character stills and eight animal studies. The subsequent M1.C7 request authorizes animating these appearances. Do not silently substitute review outputs into gameplay.

Use the **exact approved Hero Boy V1** as the current style/anatomy baseline, not a discarded assistant draft. Its user-edited pixels take precedence over older generic outline/palette/ratio advice. Preserve V1 unchanged. Girl Hero retains its body occupancy from native row45 down, including both hand/hip gaps, feet, stance and two empty bottom rows. Her separate twin puffs, coral ties, coral/cream top, blue shorts and burgundy/cream shoes follow the selected concept. Do not make her thinner or taller through gender stereotypes.

The baseline is 32×64, with 2×4 eyes at x12–13 and x18–19, native rows38–41. Full painted bounds are `[3,25,29,62]`; this includes hair, not a measured bare skull. New hair can extend above that envelope. Adult studies keep the same canvas/foot anchor, shift the face/eyes upward two pixels and extend the torso upward by two pixels; this is an **original Critz adaptation**, not a new measurement of Emerald anatomy. Adult identity also comes from clothing, hair and posture, rather than large frames or elongated shins.

Retain established supporting identities: Mom's rounded natural hair, earrings and rose cardigan; Nugget's field hat, silver hair, glasses, cream field coat and green shirt; Kaid's teal pitcher, amber contents, left spout and right hollow handle. His vessel is the specific anatomical exception; paired limbs and eye positions still mirror. Use the existing Rootport cast (Aunt Ember, Dr. Fern, Juniper, Mina and Ollie) before inventing towns or renaming characters. Rival options remain player-named children. Their costumes are proposals, not new story canon.

Animal studies use original species-specific silhouettes in 32×32 transparent frames. Pebble, Button, isopods and springtails belong to the current rescue story. Tree frog, cherry shrimp, guppy and stag beetle are optional future-species **visual proposals**, not implemented stock, new rescues or habitat compatibility claims. Observation-scale depictions of small organisms are not their world-scale dimensions. Human bilateral idle rules do not force a side-view snail, swimming fish or curled gecko tail to mirror.

**Production lessons:** preserve the selected design while authoring explicit native cells; a screenshot overlay or resized concept does not establish a native sprite. Keep one-cell contour refinements, coherent material clusters, no antialiasing, no forced 2×2 construction, and no arbitrary palette cap. Dark hair fill is not an outline. Verify the *visible* paired eyes after adding fringe or accessories: a symmetric hidden eye mask is insufficient if one bang erases an eye. Keep authored geometry masks separate from hair, shading and accessories. Record actual dimensions/deviations, inspect both native and clean enlarged artwork, then inspect the countable grid. Passing checks is not user visual approval.

For review, show the full 32×64 character canvas with one native pixel per square, the vertical x16 line and Y0 at the bottom, major horizontal guides every ten pixels. Include a clean view and exact native exports. Animal grids use the same rule on 32×32 canvases. All review overlays stay out of sprite PNGs.

## Girl Hero concept — user update, M1.C4 revision 11

The user supplied their newly edited boy as exact editor RLE and requested a girl concept using that boy and the editor's basic skeleton, **keeping the body proportions the same**. This initially authorized one front-idle concept; the current M1.C6 request above authorizes native production and additional idle cast. Preserve the source at [R11 boy RLE](reviews/M1-C4/revision-11/user-boy.rle.json). Its body construction is the current comparison target for this girl, superseding older boy revisions wherever they differ.

Use the skeleton's rounded bare cranium and fixed eye landmarks; hair is a separate volume extending above the skull. Do not enlarge or stretch the skull to reach the top of the hairstyle. Retain the boy's shoulders, torso, arms/hands, pelvis, short legs, shoes and stance; do not narrow or lengthen the girl to communicate gender. The attached girl screenshot supplies the twin-puff/short-lock hairstyle and coral/blue/burgundy outfit direction, not replacement anatomy. Her identity remains a ten-year-old Black child.

Measured inputs: both sources use 32×64 frames; the boy's full bounds are `[3,25,29,62]`, and the skeleton's are `[3,26,29,62]`. Body/chin outer row envelopes match from row44 down, but the boy has two empty hand/hip gap cells at `(7,54)` and `(24,54)` where the skeleton is occupied. Preserve the boy as instructed rather than silently filling them. Source eyes retain the 2×4 landmarks and source feet end on row61. All coordinates here are top-down native; these source measurements do not certify a generated concept's pixel positions.

[R11](reviews/M1-C4/revision-11/README.md) is a generated enlarged design preview, selected by the user on 2026-10-06. Its 32×64 budget is a construction target, not a claim that the high-resolution output is a native sprite. Generated grid labels cannot establish exact proportions: reject unreliable grids, preserve actual source evidence, and require a separately verified native/grid deliverable before calling later artwork production-ready. Selection of that design does not approve a later native rendition.

## Editor color freedom — user update, TOOLS.SE8

The latest user request expands the Sprite Editor beyond a single Wildlife palette: **selectable palettes, arbitrary exact RGB picked from references/artwork, custom colors and full-opacity reference copying are authorized.** This supersedes the Wildlife-only selectable bank and 31-opaque-color editor validation restrictions below. The original Wildlife slot order/values stay intact as one choice; existing artwork is not recolored when switching banks. Fourteen editor palette collections include existing Critz character/environment banks, a new portrait/skin/hair selection and grayscale. These are authoring choices, not approval or recoloring of gameplay assets.

Copied references preserve their current crop, position, sampling and exact colors. Fully transparent cells stay unpainted; nonzero alpha becomes fully opaque because artwork remains true binary-alpha pixels. Guide opacity does not affect copied or eyedropped RGB. References remain separate until the user explicitly clicks Copy reference. PNG/project/exact-data exports keep all colors; GIF exports may reduce their own color table above 255 opaque colors, without changing the project. Preset references contain only the user's original skeleton; no reference-game artwork is bundled.

## Current Wildlife palette — 32 slots, 2026-10-03

The user supplied the following exact palette for the Sprite Editor. **Slot 00 is transparent; slots 01–31 are fully opaque.** Wildlife remains one selectable bank alongside other banks and exact custom RGB. It does not replace or restrict them. The older proposed 15-color restriction below is historical. Palette selection is not artwork approval, a reference-game palette claim or authorization to recolor existing gameplay assets.

Editable source: [sprite-editor/palettes.json](../sprite-editor/palettes.json). Preserve the slot order, exact RGB values and names. Existing project pixels retain their colors on open/restore; do not silently quantize old artwork. New drawing/imports may use any selected bank or custom RGB. Reference copying is an explicit editor action; overlays remain separate until copied. A copied reference still needs native-pixel inspection and the appropriate originality/approval checks.

| Slot | Exact value | Color | Family |
| --- | --- | --- | --- |
| 00 | `#00000000` | Transparent | Transparency |
| 01 | `#E84038` | Saturated Ruby Red | Tropical vibrant creatures |
| 02 | `#FC7858` | Coral Salmon | Tropical vibrant creatures |
| 03 | `#FCD080` | Warm Belly Yellow | Tropical vibrant creatures |
| 04 | `#289870` | Tropical Teal Green | Tropical vibrant creatures |
| 05 | `#48D098` | Saturated Mint | Tropical vibrant creatures |
| 06 | `#A0F8D0` | Seafoam Cream | Tropical vibrant creatures |
| 07 | `#F85888` | Bioluminescent Pink | Tropical vibrant creatures |
| 08 | `#082048` | Midnight Trench Blue | Reef & deep water |
| 09 | `#184080` | Sunken Sapphire | Reef & deep water |
| 10 | `#3878B8` | Classic Surf Aqua | Reef & deep water |
| 11 | `#68B0E0` | Shallow Lagoon Teal | Reef & deep water |
| 12 | `#98E0F8` | Crisp Glass Ice | Reef & deep water |
| 13 | `#F8F8F8` | Pure Bubble White | Reef & deep water |
| 14 | `#201008` | Damp Humus Black | Substrate, wood & roots |
| 15 | `#482810` | Bogwood Brown | Substrate, wood & roots |
| 16 | `#784820` | Mangrove Bark | Substrate, wood & roots |
| 17 | `#A87038` | Golden Tan Oak | Substrate, wood & roots |
| 18 | `#D0A068` | Desert Clay/Sand | Substrate, wood & roots |
| 19 | `#F8D8B0` | Soft Silicate Sand | Substrate, wood & roots |
| 20 | `#083018` | Overgrown Shadow Green | Forestry & rainforest canopy |
| 21 | `#185828` | Monstera Leaf Base | Forestry & rainforest canopy |
| 22 | `#388840` | Vibrant Emerald | Forestry & rainforest canopy |
| 23 | `#68B858` | Chartreuse Sprout | Forestry & rainforest canopy |
| 24 | `#A0E068` | Vivid Lime | Forestry & rainforest canopy |
| 25 | `#D8F880` | Acidic Shoot Yellow | Forestry & rainforest canopy |
| 26 | `#282830` | Obsidian Iron | Hardscape & hardware |
| 27 | `#484850` | Weathered Basalt | Hardscape & hardware |
| 28 | `#707078` | River Slate | Hardscape & hardware |
| 29 | `#9898A0` | Pumice Ash | Hardscape & hardware |
| 30 | `#C0C0C8` | Polished Chrome Filter | Hardscape & hardware |
| 31 | `#E0E0E8` | Anodized Aluminum | Hardscape & hardware |

## Emerald 2× visual contract — authoritative, 2026-10-02

**User-confirmed direction:** Critz uses Pokémon Emerald's art style, camera framing and character proportions at **twice the linear pixel resolution**. Use the selected reference's face/body landmarks, pose, overlapping forms and pixel rendering to construct original characters. Separate the skull, exposed face, hairstyle and headwear. Matching the highest hat/hair pixel or full opaque bounding box is not anatomical fidelity; original hairstyles do not have to reach a reference hat's tip.

This contract supersedes conflicting production dimensions, generic chibi formulas and 20×26/24×32 constraints below and in CHARACTER_FRAMEWORK, PROJECT_PLAN and older prompts. Those passages remain historical records. It does not retroactively certify existing assets, implement a renderer migration, approve finished art or expand the authorized roster/world. GAME_VISION remains story canon.

### Official Hero Boy V1 — approved still; walking review (M1.C5)

The user declared their editor-corrected Hero Boy still perfect and requested official V1, then supplied the exact RLE. **That supplied sprite is now the approved still**, superseding earlier assistant drafts. Preserve its pixels without cleanup, palette replacement, outline normalization or automatic mirroring. [Official PNG](../assets/characters/hero-boy-v1/idle-south.png) · [Approval/hash manifest](../assets/characters/hero-boy-v1/manifest.json) · [Exact original export](../art/source/hero-boy-v1/user-approved.rle.json). Source SHA-256 `bef3289d8d62801ea2f223ae9359beb305856764a54afed8fe9990f42676fb3a`. Measured 32×64, bounds `[3,25,29,62]`, 757 occupied cells, 14 used colors, anchor `[16,64]`. Later user edits require a new version; V1 stays intact.

Walking is now explicitly authorized for this Hero. The current deliverable is a front-facing walk in place using the exact approved still as both passing poses. Study pinned Emerald frames3/0/4/0 at eight ticks each; translate this Hero's head/hair down two target pixels for strides, maintain its asymmetric hair/color identity, and alternate opposing arms/legs with a tucked rear foot. Never mirror the entire sprite to switch leading legs. Idle feet end at row61; stride feet may reach63. The 32×64 frame stays fixed. The still's approval does not self-approve the new strides or authorize silent runtime replacement. [Walk GIF/evidence](reviews/HERO-V1-WALK/README.md).

GIF uses 10ms timing units. Preserve exact source ticks in editable data and state export rounding honestly: this four-pose preview holds130/140/130/140ms, a540ms loop versus535.7666ms source cadence. Preserve palette and per-frame transparency; check decoded animation frames for trails, recoloring, clipping and exact return to the approved still.

### Prior Hero target — preserve the twists reference; local cleanup only (revision 10)

The user selected the orange-and-cream striped Hero with layered twists shown in the R7-derived screenshot. It already fits the native 32×64 budget; use its saved native pixels as the visual target. Preserve the good irregular hair clusters, proportions, clothing and color relationships. The supplied skeleton is an anatomy/landmark guide, not authorization to replace the chosen silhouette with the differently shaped R9 body. Keep two transparent bottom rows, mirrored anatomy/eye positions, separate hair/lighting variation, and a one-native-pixel **black** exterior outline.

**No color-budget restriction for this request.** Do not quantize to the editor's Wildlife bank or simplify the palette merely to match a previous revision's count. R10 has 28 deliberate retained/cleanup colors; that is an actual result, not a new cap. Being derived from an earlier reference transfer is not itself a reason to discard valid native pixels or redesign the character. The failure in R8/R9 was losing the selected appearance while changing methods. Make small recorded edits to the target instead. A reference image overlay is not an export, but a correctly decoded native raster is real pixel data; evaluate its pixels and appearance rather than assigning quality from its origin.

The R10 operation preserves all occupied cells and all non-outline hair-region colors, changes the exterior to one black boundary layer, and repaints adjacent overly dark body bands as material shadows. No 2×2 solid pure-black outline blocks remain. Anatomy is mirrored; the selected hair/lighting variation stays intact under the standing hair exception. Only the user approves the resulting appearance. Front idle only; animation and gameplay integration remain separate. The earlier R9 strict-template/Wildlife directions below describe that revision and do not override this chosen target.

### Prior asset direction — user-authored skeleton and one-pixel outlines (revision 9)

The user supplied an exact `fmw-sprite-exact-rle` editor export as the construction source. Decode its native pixels; do not infer geometry from screenshot grid lines. This input is one symmetric color-blocked template, not four finished sprites. Preserve its head/body construction, eye positions and two-row idle foot padding; apply the four supplied hairstyles/outfits separately. Mirror anatomy with `x ↔ 31-x`, the same operation as the editor's X-symmetry tool. Preserve original input before editing. Hair and lighting remain separate from anatomical symmetry.

**Latest explicit outline rule: one native pixel thick.** This supersedes earlier suggestions of 2px outline weight for these character assets. Use one boundary layer without stroke dilation, and single-pixel internal separation lines. Refine contours and shading at individual target pixels; do not lock forms to a repeated 2×2 block grid. Solid material areas and the established 2×4 eyes are not forbidden merely because they contain adjacent pixels; avoid forced block construction, not coherent color clusters. Dark hair fills are material, not automatically a thick outline.

Grid alignment alone does not establish finished pixel quality. Check actual dimensions, exact export pixels, paired anatomy, outline masks, palette, anchor and native-size readability. R9 retains the input Wildlife palette and exports native transparent PNGs, reopenable editor projects, exact RLE and stable asset metadata. These are technically ready front-idle asset files awaiting visual review, not a complete animated/multidirectional character. Animation and runtime replacement are separate next steps. Brendan stays external to the build. Native and gridded comparison views may both accompany this revision; grids are never baked into sprites.

### Basic character skeleton — exact user intent, TOOLS.SE7

The user's pasted sprite is the **basic anatomical construction model**. Blue is head volume, gray is torso, pink marks arms/hands, green the pelvis/upper-leg connection, and coral the lower legs/feet. These colors distinguish body sections; they are not an alien, costume, skin-color assignment or finished outfit. Preserve this structural reading when designing original characters. The exact source is retained in [user-skeleton.pixels.json](reviews/TOOLS-SE7/user-skeleton.pixels.json); the editor's [starter](../sprite-editor/templates/basic-character.json) contains identical pixels and palette.

| Section | Exact source colors | Construction / shading |
| --- | --- | --- |
| Head | `#68B0E0`, `#3878B8`, `#184080` | Main blue cranium/face plane; medium-blue lower-face/side shadow; deepest blue recessed side areas |
| Eyes | `#F8F8F8` | Two 2×4 landmark blocks at x12–13 and x18–19, source rows38–41 |
| Body / torso | `#9898A0`, `#707078` | Gray torso plane; darker neck/shoulder shading below the head |
| Arms / hands | `#F85888` | Paired side volumes; no separate arm shadow ramp in this template |
| Pelvis / upper legs | `#388840` | Structural connection between torso and two legs |
| Lower legs / feet | `#FC7858` | Paired lower-limb volumes; no separate leg shadow ramp in this template |
| Outline / separations | `#201008` | Dark-brown outer contour and internal form divisions; distinguish these pixels from shadows |

Measured user pixels: 32×64 canvas, 720 occupied cells, 10 opaque colors, half-open bounds `[3,26,29,62]` (26×36). All colors and occupied cells mirror exactly about x16. Feet finish on source row61 with two transparent rows below (review cell Y2). Source rows count downward; review guides count upward. These measurements describe the supplied template, not mandatory bounding heights for hair or headwear.

The saved supplied Brendan **screenshot reconstruction** matches all 832 occupied/empty cells across rows36–61 (zero silhouette differences), eye positions and the foot row. This comparison is evidence for the supplied alignment, not raw-ROM pixel identity or a measurement of the skull hidden under Brendan's hat. The rounded bare head above row36 belongs to the user's construction. Do not stretch it to the hat peak or flatten it to the hat brim. [Measurement evidence](reviews/TOOLS-SE7/measurements.json) pins source hashes and the comparison's scope. Reference-game pixels stay outside the shipped project.

The editor uses fixed semantic masks derived from this template, so recoloring does not reclassify anatomy. A selected region, outline protection and alpha lock constrain drawing; guide pixels remain separate from artwork. General silhouette/RGB mirror counts are diagnostic only and do not replace anatomical-mask validation or user approval. This request authorizes a reusable editor guide and starter; it does not approve new character art, animation or gameplay replacements.

### Prior correction — author native pixel clusters; reference overlays are guides (revision 8)

**User instruction:** retain all four supplied boy designs and hairstyles, turn them into real native pixel art within the 32×64 budget, and put Brendan beside them. **Show this revision at actual 1× size, without enlarging it.** This specific request overrides the default gridded review presentation for R8. Front idle only; no animation or accepted gameplay replacement.

R7 brought the designs closer to the references, but transferring/quantizing the screenshots was not the requested finished pixel art. A 32×64 file and binary alpha are necessary technical properties, not proof of deliberate pixel craft. Do not promote a reference overlay, averaged screenshot, automatic quantization or noisy sampled colors into final artwork merely because it passes dimension checks. Use references to establish proportions, then author clean silhouette steps, locks/braids, facial planes, garment edges, contact shadows and highlights directly on the native pixel grid. Use short intentional color ramps and connected clusters. Inspect at native size before delivery. Do not add detail just to fill a color or pixel quota.

**Keep the lessons that are valid:** skull, exposed face, hair and headwear are separate. R4 stretched heads toward Brendan's hat peak; R6 then flattened them by forcing bare heads to the hat's lower edge. Both constructions were wrong. Native row 36 in the supplied Brendan is a hat-to-visible-face boundary, not a universal bare-head hairline or a measured skull crown. His covered forehead cannot determine the hairline of an uncovered head. Cornrows must follow a rounded cranium; twists hang over it, and an afro or flat-top adds its own volume.

Align reference concepts as whole figures at uniform scale when checking proportions. Preserve their identities and head/body relationships while deliberately redrawing native clusters. Do not independently squash hair/skull or stretch limbs to satisfy a bounding rectangle. The 32×64 canvas is capacity, not required figure height. The former 33–35px figures, the miscounted 36 and Brendan's 42px headwear-inclusive bound are not mandatory heights. Record actual bounds and deviations, and label hidden cranium construction as inferred rather than measured.

R8 uses authored indexed pixels and explicit anatomical masks, with 15–16 intentionally chosen opaque colors per candidate. These preserve the supplied teal/cream, gold/cream, red/cream and blue/olive designs; they do not revise the editor's separate Wildlife palette or establish a universal production color count. [R8 source and evidence](reviews/M1-C4/revision-8/README.md). R7 remains reference-alignment history, not an accepted production rendering method. Only the user accepts visual quality; neither code, tests nor this document can self-approve it.

### Resolution and framing

| Quantity | Reference basis | Critz target |
| --- | --- | --- |
| Exploration raster | 240×160 | **480×320**, same 3:2 view |
| Total raster pixels | 38,400 | **153,600** (4× area) |
| Standard human overworld frame | 16×32 | **32×64** transparent canvas |
| Small NPC/item frame family | 16×16 | **32×32**, where that reference family applies |
| Map metatile | 16×16 | **32×32** |
| Base art tile | 8×8 | **16×16** |
| Battle/intro front/back frame budget | User-supplied 64×64 basis | **128×128** when such assets are authorized |

Battle/intro dimensions are a user-selected production budget, not a newly verified universal fact about Emerald portraits or an instruction to implement battles. Do not substitute Platinum, HeartGold, remakes or other generations for the Emerald reference.

Scale viewport, artwork, rendered distances and camera offsets together. The view remains 15×10 metatiles, not a zoom-out showing more world. Keep the controller outside it. At 2×, a standard bottom-center frame anchor `(8,32)` becomes `(16,64)`; the 16×16 family anchor `(8,16)` becomes `(16,32)`. Edge coordinates double; an inclusive pixel row `r` maps to rows `2r` and `2r+1`: reference idle foot row 30 becomes rows 60–61, stride row 31 becomes 62–63. Do not mistake transparent frame padding for body height.

The existing ledger's south-idle bounds imply these **derived, not newly measured full-silhouette examples (including hair/headwear), not required anatomy or mandatory heights for original hairstyles**: Brendan 14×21 → 28×42; May 14×20 → 28×40; Wally 16×19 → 32×38; Mom/Birch 16×20 → 32×40. These examples show why a 32×64 frame must not be filled by a 64px-tall person. Select a specific measured reference family for each Critz design; there is no single universal Gen 3 head/body ratio.

### Mandatory measured construction

1. For a new reference family, inspect actual native Emerald overworld frames from pinned revision `5eff78649e7170a877b961ef0b3da13b81a16038`, using the ledger's transparency rules. Record source path, frame index, direction, revision and method. For the current cast, reuse the approved Hero V1 and the existing pinned measurements instead of restarting from another inferred Brendan skull. Use gameplay captures for camera/motion claims; label source-only evidence accurately.
2. Before production, create an annotated measurement table per representative body/pose family: full opaque bounds; head width/height; face/eye/chin landmarks; hair and hat envelopes separately from face/head; shoulder and torso widths/heights; arm/hand bounds and attachment points; leg/shoe bounds, stance and contact points; ground anchor; all pose offsets. Each row must contain reference coordinates or dimensions, exact 2× target where that same feature applies, actual Critz value and deviation. Label headwear-only extents and hidden anatomy explicitly; do not turn an inapplicable hat height into a skull target. Head/eye/limb segmentation remains unresolved in the old ledger: inspect and annotate it instead of inventing values.
3. Use the measured structure as the drawing scaffold in front, back and both profiles. Preserve face/body relative size, placement, overlap and foreshortening. Compare silhouette mass by anatomical region; the highest hair/hat pixel is not a universal head-height target. No improvised taller torsos, long shins, narrow waists, oversized hands/shoes or enlarged hair/hats merely because the canvas has room. Distinct body types use corresponding measured reference families. Kaid's nonhuman vessel/spout/handle require a labeled original adaptation while limb scale, ground contact and gait stay coherent; do not pretend Emerald contains an exact Kaid template.
4. Author original Critz PNGs and editable pixel sources against that scaffold. Reference sprites remain inspection material, never shipped game assets. Preserve the Black child Hero, child rival/Kaid and adult Mom/Nugget. Do not recolor reference characters and call them original designs.

### Idle front/back symmetry — mandatory character rule, 2026-10-03

**User-confirmed:** we are committed to the measured **Emerald 2× style and pixel budget**. New standard-human character reviews use 32×64 frames. Derive face/body landmarks from the selected reference; measure actual painted bounds separately after original hair/headwear construction. Do not force those bounds to match a hat-bearing reference. Older approximate chibi budgets are not alternate defaults. Show the user the measured reference proportions and their doubled targets **before drawing**, with the reference revision, frame/pose, annotation definitions and unresolved hidden anatomy clearly identified.

For **front idle and back idle**, the underlying skull/cranium, face construction, eye positions, torso/body, shoulders, arms, hands, hips, legs and feet must be bilaterally symmetric by default. Corresponding parts have mirrored contours, equal dimensions and area, equal attachment heights and equal offsets from the centerline. The eye positions and shape must mirror; matching outer alpha alone is insufficient. A larger hand, a lower shoulder or displaced eye is a defect unless the user explicitly requests that structural exception.

- Mirror geometry across the vertical line halfway across the X extent: `x = frameWidth / 2`. For native pixel indices the partner is `frameWidth - 1 - x`. A 32×64 frame has its centerline at edge coordinate **x=16**, between columns 15 and 16; the 16×32 comparison has x=8, between columns 7 and 8.
- **Hair is separate.** Hairstyles, bangs, parts and uneven hair volume may be asymmetric. Keep the underlying skull construction symmetric; do not let hair asymmetry silently distort the cranium or eye placement. Hair follows the supplied character design and its recorded construction; it need not fill a reference hat envelope.
- **Color is separate.** Lighting, shadows, highlights, fabric colors and decorative color patterns may be asymmetric. Do not RGB-mirror the whole character. Conversely, do not excuse different anatomical or sleeve/hand boundaries as mere shading; inspect the actual part masks and visible shape.
- **Explicit exceptions:** unusual/nonhuman designs such as Kaid may have documented asymmetric features (for example, a pitcher spout and handle), or the user may explicitly request another exception. Record the specific exempt feature; an unusual character does not automatically exempt every limb or eye.
- This bilateral idle rule applies to front/back rest poses. It does not force profile views, walking strides, running or expressive action poses to be symmetric. Those still follow measured reference construction and pose-specific checks.

Author or annotate separate anatomical masks for skull/face, eyes, torso, arms, hands and legs/feet. Validate each reflected pair, its bounds/attachments and occupied area, independently of RGB shading and hair. Where a hat or garment hides anatomy, label the hidden construction as a symmetric Critz scaffold, not a measured Emerald bone shape. Inspect the visible result as well as the automated mask comparison.

### Character review grid — default presentation; honor explicit overrides

**User correction: Y increases upward.** Display **0 at the bottom and 64 at the top** of a standard 32×64 grid, with major horizontal lines labeled 0/10/20/30/40/50/60 and the top boundary 64. X increases left to right, with the vertical symmetry line at x=16. Preserve all 64 rows of available space in each requested review panel. Changing labels does not flip the artwork.

Native PNG/source indices still run from top row 0 downward. Convert an edge at native row `r` to displayed height `Y = 64 - r`; cell row `r` occupies heights `[63-r, 64-r]`. Label coordinate systems explicitly in measurements. Earlier review references to “row 36” use top-down native coordinates and therefore mean the face edge at displayed Y=28, not a 36px skull height. The user explained that the earlier 36 estimate came from counting upward on a downward-labeled grid; **do not impose 36px as a required skull or figure height**.

Unless the user explicitly requests another presentation, present new characters in their **Emerald 2× native budget** with a countable grid: **one square equals one native pixel**, even when enlarged. Always show a distinct **vertical symmetry line through the horizontal midpoint** (x=16 for a standard 32×64 human frame). Draw and number **horizontal major guides every 10 pixels up the Y axis**, with frame boundaries labeled too. Keep the ordinary one-pixel cell lines visible and clearly distinguish the centerline from the ten-row guides. Use integer enlargement and report the native frame, painted bounds and display scale. Blank padding is not anatomy.

For **boy Hero**, the earlier 1×/2× paired comparison remains available on request; the latest explicit review request controls the layout. R8 explicitly requests an unscaled native lineup: Brendan first, followed by the four 32×64 candidates, with no enlarged grid. The five-grid layout belongs to R7 history. Other characters normally need only the 2× presentation unless a comparison is requested. Include a part/silhouette proof when checking symmetry. Grids are review overlays, never baked into the native character PNG. Present idle revisions first; this rule does not authorize animation or game integration.

### Lessons from prior rejected revisions (history, subject to the current correction)

#### Human ear/face correction and review priority — revision 4

The user rejected the previous Hero as elf-like and supplied four human-boy concepts. Human Hero ears must be small, blunt lobes close to the head; do not stretch or taper them sideways to satisfy an overall bounding width. Preserve a full, rounded cheek/jaw mass. The anatomy includes mirrored ears; hairstyle volume and costume shading remain independent. Measure candidate deviations explicitly instead of compensating for smaller hair with oversized ears. Revision 4’s narrower face/ear shapes are proposed adaptations to those concepts, not approval of a changed global proportion standard.

When the user explicitly requests multiple 2× candidates, that request determines the current comparison layout: revision 4 presents four 2× idles, without an added 1× panel. **Lead with the user’s currently requested presentation.** When grids are requested, show them directly with one native pixel per cell, x=16 symmetry and ten-row Y guides; do not hide them behind a link. When the user requests native size, as in R8, show the native sprites directly instead. Technical symmetry/bounds checks never substitute for whether the character visibly matches the user’s reference.

#### Aligned-reference diagnosis — revision 5 (incomplete; corrected by revision 7)

The user requested their refined Brendan screenshot beside all four unchanged R4 Heroes. The comparison reveals that equal frame/painted height and mirrored anatomy do not ensure the same proportions or character read. In the supplied reference, the continuous central exposed face begins at row 36; A/B/D begin around rows 30–31 while retaining eyes at rows 38–41. This changed the face, but treating it as automatically wrong was an incomplete diagnosis: Brendan’s hat hides forehead that a bare head exposes. Do not copy its occlusion boundary as a mandatory hairline. C’s locks partly cover the underlying scaffold. A pointed hat peak and a broad afro/flat-top cannot be equated solely by their topmost pixel; compare occupied row widths and distinguish hat, hair, exposed face and hidden skull.

Before the next correction, compare the exposed hairline-to-eye and eye-to-chin distances, face width profile, neck overlap, shoulder/arm attachment, torso width profile and dark separation between body parts. The prior broad shirt rectangles and weak arm/torso separation flatten the image. Preserve the reference’s structural readability without changing Hero’s identity/skin tone. This is a diagnosis of the supplied comparison, not new ROM-source measurement or approval of a revised anatomy standard. Keep all reference-colored review images outside the shipped build; screenshot interpolation is not additional native colors.

### Asset integration boundary

Keep appearance separate from collision, interaction, warp and gameplay data. Ship original reusable PNG assets with stable IDs and metadata; do not ship reference-game sprites or reference-colored comparison plates. Reference-only files remain outside the repository because the build copies documentation. Keep art workflow details here rather than duplicating them in AGENTS.md.

### What the extra pixels are for

Each reference pixel occupies a 2×2 area in the structural comparison. Start comparison guides with exact nearest-neighbor doubling. Final original assets may subdivide those blocks into finer **1px target-grid** clusters for cleaner linework, texture, expressive faces and material detail while retaining the measured envelopes and landmarks. Literal upscaling alone adds no detail; a freely redesigned 32×64 figure also does not satisfy this contract.

Aim for the user's richer texture and cleaner linework within Emerald's restrained contrast, palette relationships and readable shapes. Detail must survive inspection at intended screen size. Avoid noise, pillow shading, antialiasing, blur, fractional pixel placement or mixed asset densities. A reference 1px outline initially occupies 2 target pixels; selective 1px refinements must not change silhouette mass or make the whole character look thin. Do not silently turn the 4× pixel count into a 4× color budget.

### Target-grid contours, outlines and depth — revision-3 correction

**User-confirmed correction, 2026-10-03:** Emerald 2× means authoring with individual target pixels. Preserve measured dimensions, proportions, landmarks, anchor and pose; do **not** freeze the final silhouette to an exact nearest-neighbor doubling of every occupied source pixel. The source's 2×2 blocks are a comparison scaffold. Redraw stair-step corners, curves, diagonals, overlap boundaries and material edges at **one target pixel** where it improves the form. Add/remove individual opaque edge pixels within the measured envelope and mirror corresponding anatomical changes in front/back idle. Document meaningful envelope/landmark deviations instead of disguising them as refinement.

The rejected M1.C4 revision 2 illustrates the failure: its high-resolution mask and part labels were duplicated from the low-resolution source, and its pixel-edit helper prohibited editing empty cells. It therefore had **zero partially occupied 2×2 silhouette blocks**. A few internal color changes did not correct its doubled corners or heavy bands. The validation of exact doubled row occupancy reinforced the error. Future checks must preserve the measured envelopes, landmarks and paired anatomical masks **without requiring the old block pattern**. Mixed-block counts can diagnose a locked enlargement; they are not a beauty score or a required texture quota.

**Selective outline treatment:** study the selected native reference, then use dark colors appropriate to the material and lighting. In the inspected Brendan south-idle frame, the four-neighbor exterior boundary contains black, dark blue, blue-violet and brown; it is not one uniform black stroke. This is evidence for that frame, not a universal claim about every Emerald sprite or Game Freak's drawing process. Keep strong dark accents at useful overlaps and contacts (under the hair, between arm and torso, under feet). Use lighter/colored edge pixels on lit faces or materials where readable. For current character production, the user’s R9 instruction requires a one-pixel outline. Interior shadow clusters may describe form, but must not act as a second outline layer. The older mixed 1px/2px outline suggestion is superseded.

**Depth through clustered shading:** establish a consistent light direction for the asset; make highlights, midtones and shadows describe rounded skull/cheeks, sleeve volume, hair masses, cloth turns and shoes. Use short material-specific hue/value ramps and connected clusters. Separate a cast/contact shadow from the object's outline. Avoid broad rectangular color patches that ignore form, long accidental nose stripes, randomly scattered bright pixels and texture added solely to appear more detailed. Symmetry constrains anatomy; it does not require symmetric light and shadow. Remain within the declared palette and native opaque pixels—no blur, antialiasing, interpolated gradients or fractional coordinates.

Review at native size and an exact enlargement **both with and without the grid**. Keep the required centerline/ten-row grid, but add a clean view when evaluating edge weight, material contrast and volume. Inspect a before/after when fixing a style error. Technical checks must not be described as proof of visual success; final acceptance is the user's. See [revision-3 diagnosis and evidence](reviews/M1-C4/revision-3/README.md).

### Animation fidelity

Map each authorized Critz key pose to a named reference pose and measure limb travel, foot contacts, arm opposition, body bob, head stability and accessory motion. Double spatial offsets, preserve timing and phase continuity. Do not animate disconnected feet beneath a static invented body or reset the gait every tile. Author both profiles for asymmetric designs.

The existing source-derived baseline remains walk `stride A → idle/passing → stride B → idle/passing`, holds `8/8/8/8` ticks, and run holds `5/3/5/3`, at `280896/16777216` seconds per tick. Scaling changes walk displacement from 1 to 2 rendered pixels/tick and run from 2 to 4; a 32px cell still takes 16 walk ticks or 8 run ticks. These are source-derived targets, not a claim of emulator-observed equivalence. Finer spatial resolution alone does not add animation frames or temporal smoothness. When smoother animation is in scope, add measured in-between poses within the same cycle duration and preserve key-pose/contact timing; present the refinement beside the reference-cadence version for user review.

### Required evidence and acceptance

For the currently authorized sample, deliver a measured overlay/comparison at matched apparent scale (reference 2× beside Critz 1×), native 480×320 room context when environment/framing is in scope, enlarged nearest-neighbor sheets, and synchronized loops plus frame stepping when animation is in scope. Include a table of targets/actual values/deviations, original asset IDs, source/PNG hashes and unresolved measurements. Keep reference imagery separate from production atlases and build output.

Check PNG dimensions, binary alpha, palette counts, opaque bounds, landmarks, anchors, pose continuity, tile seams and exact enlargement. Inspect actual pixels as well as automated results. Do not declare compliance from dimensions or bounding boxes alone. No unmeasured “close enough” substitutions: document the gap and resolve it before calling that requirement complete. The user retains visual/feel approval; documentation acceptance approves the specification only.

For a future renderer migration, keep appearance units separate from gameplay cells, collision, interactions, warps and v1 save coordinates. Re-evaluate phone presentation explicitly: 480px cannot fit a 320px-wide screen at 1×. Present and test any nearest-neighbor downsampling or orientation/layout solution with its detail-loss tradeoff; never silently crop, blur or stretch. This documentation task changes no runtime or saves.

---

## Historical art direction and implementation records

The following specifications predate the authoritative 2× contract. Read conflicting dimensions and construction rules as history, not current authoring instructions.

**M1.C3 animation extension:** The user now requests walking cycles and GIFs for every current M1.C2 design. The [walking extension](CHARACTER_FRAMEWORK.md#m1c3-walking-extension) retains the 20×26 painted ceiling, compact anatomy, exact front-idle art and four explicit directions. This supersedes still-only scope for animation review; finished artwork remains awaiting user acceptance.

**M1.C2 current character direction:** The user selected a 20×26 maximum visible budget and requested a new compact chibi framework, distinct body types and one still frame per character. [CHARACTER_FRAMEWORK.md](CHARACTER_FRAMEWORK.md) now governs this still-character design pass, superseding the earlier 16×32 character-production proposal for these new assets. Storage remains 24×32 with explicit anchors; the map grid stays 16×16. Final artwork acceptance is pending; budget selection alone does not approve the drawings.

**2026-09-27 scope amendment:** The user explicitly authorized M1.I2 to complete the existing roster/environment art, directional walk/run sheets, playable integration and tile movement together without intermediate art approvals. Earlier staged restrictions below are historical and superseded for this deliverable. Technical/visual proposals remain provisional; final user acceptance is pending. The [playable-review record](reviews/M1-I2/README.md) documents actual asset extents, native rendering, limitations and checks. No world expansion is authorized.

M1 environment review edition, 2026-09-25. **No example artwork, character proportions, palette swatches or motion proof has user approval yet.** “Approved direction” below means the user's supplied technical brief, not a finished art asset. [REFERENCE_MEASUREMENTS.md](REFERENCE_MEASUREMENTS.md) separates measured evidence from proposals. [GAME_VISION.md](GAME_VISION.md) remains canon.

## Approved direction

- Exploration is rendered first into a **240×160 native raster (3:2)**. Construct artwork from **8×8 base tiles** and **16×16 map metatiles**. Final world/sprite/camera positions align to integer native pixels; nearest-neighbor presentation, no bilinear resampling.
- Overhead three-quarter orthographic tile conventions: roofs, building fronts and furniture tops are visible together; ground-plane contact is consistent. This is an authored drawing convention, not a numerical camera angle or a perspective-projected 3D scene.
- Original Critz characters, environments, tiles and interface. Emerald is a measurement/reference source, not a source of shipped artwork or copied characters.
- Hero is a ten-year-old Black child; Hero and opposite-gender rival are player-named. Kaid and rival are children; Mom and Professor Nugget adults. Kaid remains an original whimsical pitcher child. Do not make adults twice the frame size.
- Controller stays **outside** the 240×160 exploration image. Preserve keyboard and touch access and readable menus.

## Presentation proposal — validate in M2 and M6

Default to the largest integer CSS scale fitting the space reserved for the world after HUD/controller layout: `floor(min(availableWidth/240, availableHeight/160))`, minimum 1 when it fits. Center/letterbox unused space; keep browser zoom/device-pixel-ratio in QA because integer CSS scale does not guarantee integer physical pixels on every screen. For example, a 320px-wide phone fits 240px at 1×, leaving lateral space; 2× requires 480px. Never stretch x/y independently or move controls onto the image to fill the phone.

If portrait readability makes 1× too small, offer a documented optional nearest-neighbor fractional presentation (e.g. 1.25× = 300×200). It preserves hard edges but produces uneven physical pixel widths and loses a perfect uniform pixel grid. This is a **proposed tradeoff requiring review**, not the approved default. If the available space is under 240×160, present a documented orientation/layout fallback; do not silently crop or downsample the game. DOM menu text/touch targets can use display-scale sizing independent of native exploration artwork.

## Character production specification — proposed for Critz

All values in this section are **proposed for Critz**, not user-approved or claimed Emerald anatomy. Reference frame/bounds tables live in the measurement ledger; exact Emerald head/eye segmentation remains unresolved.

| Character | Frame | Visible front idle W×H | Head silhouette / body guide | Eye rows (zero-based frame) |
| --- | --- | --- | --- | --- |
| Boy Hero | 16×32 | 14×20 | 12px / 8px | 19–20 |
| Girl Hero | 16×32 | 14×20 | 12px / 8px | 19–20 |
| Boy rival | 16×32 | 14×20 | 12px / 8px | 19–20 |
| Girl rival | 16×32 | 14×20 | 12px / 8px | 19–20 |
| Kaid | 16×32 | 14–16×19–20 including handle | 11–12px vessel/face + ~8px short body/legs; exact split unresolved | 19–20, face placement to review |
| Mom | 16×32 | 14–16×21 | 11px / 10px | 18–19 |
| Professor Nugget | 16×32 | 16×21 | 11px / 10px | 18–19 |

The guides describe silhouette regions rather than anatomical cuts through hair/clothes. Adults read through posture, torso/shoulders and clothing, with only a small height difference. Show Hero's dark skin ramp clearly in light and shadow; highlights must not erase identity. Kaid uses a small rounded vessel, expressive face, short limbs and distinctive spout/handle, with the teal glass/amber contents slice direction from the vision. Do not copy a branded mascot.

| Shared property | Proposed production rule |
| --- | --- |
| Frame origin | Top-left `(0,0)`; never independently trim frames. |
| Ground anchor | Frame edge coordinate `(8,32)`; frame extends 16px above its 16px ground cell. Anchor is not the final painted foot pixel. |
| Foot baseline | Idle last painted row 30 (edge below it y31); stride last row 31 (edge y32), matching observed source-asset vertical offsets. Foot guide and anchor must both appear on review overlay. |
| Collision footprint | One 16×16 ground cell and explicit current/destination reservation during a step; not the 16×32 image rectangle or silhouette. Final behavior validated in M2. |
| Directional poses | Four logical directions × idle plus two alternating stride poses. Store 12 images where needed; allow mirrored east only for genuinely symmetric art. Kaid handle/spout needs explicit east/west inspection. |
| Run poses | Separate four-direction run set where silhouette demands it; cadence from reference ledger. Do not generate the full run sheet in M1. |
| Gait metadata | Integer update holds and phase continuity; no generic “12 FPS” label. M1 static lineup only; M2 approves motion. |

## Environment scale — proposed for Critz

These are original composition targets to test, **not verified Emerald prop measurements**. Art extent may project above or beside the ground footprint; both must be explicit.

| Element | Draft artwork extent | Ground/collision and interaction |
| --- | --- | --- |
| Door | 16×32 | One-cell threshold; adjacent approach cell and explicit warp target/arrival direction. |
| Bed | 32×32 | 2×2 blocked cells; reachable side/foot interaction. |
| Chair | 16×16 or 16×24 | One-cell contact/occupancy; upper back can occlude. |
| Desk | 32×32 | 2×1 occupied ground cells plus upper projection; interaction at front. |
| Shelf | 32×32 | 2×1 occupied ground cells; upper shelving above contact line. |
| Fence | Modular 16×16 segments | One blocked cell per segment, explicit gate opening. |
| Tree | 32×48 | 1×1 or 2×1 trunk footprint per asset; canopy foreground separate. |
| Compact house | Initial 96×80 silhouette | Grid-composed roof/front; explicit building footprint and one-cell entrance. Not a size rule for every building. |
| Starter tank fixture | 32×32 | 2×1 supporting cabinet/contact footprint; reachable front interaction, identified as 25 gallons in UI. Artwork alone is not a gallon measurement. |

The user authorized M1.E1 environment review artwork on 2026-09-25, including original indoor/outdoor pieces and proposed Rootport, forest-route and Liarsville views. This is a review-only scope extension; it does not authorize gameplay expansion or approve G1/G2. Revision 1 was rejected for missing the intended Emerald style; revision 2 returns to a small house/tree proof before more map work. Leave floor and wall areas visually quiet enough that silhouettes, doors and interactions remain readable.

## Palette, outlines and light — proposals for G1

Emerald's 4bpp art uses multiple 16-entry palette banks; **the whole game is not limited to sixteen colors**. Background and object memory are separate; map tileset allocation is not a global character/UI budget. See reference sources for bank counts.

For Critz, propose named reusable families: warm wood/plaster interiors; leaf green ground/canopy ramps; cool teal water/glass; terracotta roofs; warm brown skin ramps; distinct clothing accents; dark blue-green UI ink and warm light text. Start with at most 15 opaque colors plus transparency per character palette, and multiple explicit 16-entry environment banks where needed. These are practical discipline targets, not a claim the browser emulates every GBA hardware limit. Exact RGB swatches await M1 and must be stored in editable palette files.

Use selective dark colored 1px silhouette outlines; reserve darkest values for faces/contact edges. Light comes from upper-left on the image plane as a **Critz proposal**; keep roof/top surfaces lighter, building fronts quieter, and short ground/contact shadows consistent. Use 2–4 deliberately chosen tones per material, hue-shifted shadows, clustered pixels rather than gradients. No antialiased ellipses, translucent blur, painterly noise or per-frame subpixel shading in exploration assets. Sparse texture in floors/grass; stronger contrast on actor edges, doors and key objects. Confirm exact ramps, texture density and outline breaks together in the bedroom sample, not through text approval alone.

## Draw order, collision and interactions

Proposed rendering order: ground and floor detail → anchored objects/characters sorted by ground-contact y with stable tie-breaker → explicit foreground/canopy/roof segments → native effects/interface. Split tall objects where necessary; an entire tree/building must not always draw behind every actor as it does in the prototype. Each sortable asset records a `sortAnchor`; each foreground tile records its intended cover behavior. No collision is inferred from alpha pixels.

Map collision, warp, interaction and spawn data remain distinct from appearances. Door opening/closing state chooses art without changing quest rules. Interaction metadata records reachable cells, facing requirements if adopted, action ID and prompt; keep generous touch interaction while preserving all current actions. Reference tile/elevation rules guide M2; any simplified Critz footprint is labeled as a choice.

## Reusable asset and map workflow — technical proposal

Use **Tiled finite orthogonal maps with JSON export**, a 16×16 placement grid, and PNG tilesets assembled from editable 8×8 source tiles. Tiled supplies tile/object layers and custom properties, so this avoids building a custom editor. Keep source `.tmx`/`.tsx` and exported JSON together; finalize a small supported subset and version in M3. See the official [layer guide](https://doc.mapeditor.org/en/stable/manual/layers/) and [JSON format](https://doc.mapeditor.org/en/stable/reference/json-map-format/), consulted 2026-09-24 (displayed version 1.12.2).

Proposed layers: `ground`, `detail`, `foreground` for appearance; `collision`, `interactions`, `warps`, `spawns`, `actors` for nonvisual data/placements. Sortable prop objects reference stable artwork IDs. Named actions dispatch into existing game logic; map files contain no story scripts/economy formulas. Treat map object coordinates as native pixels at export boundaries, map gameplay cells as explicitly converted units. Preserve existing scene and map-local entity IDs; use `<sceneId>:<entityId>` for globally unique lookup. Never persist Tiled GIDs as gameplay identity; resolve GIDs through export metadata into stable asset IDs.

Proposed paths/IDs (not files promised as implemented):

- `assets/characters/hero-boy.png`, ID `char.hero.boy`; analogues for girl, rival variants, Kaid, Mom, Nugget.
- `assets/tilesets/home.png`, ID `tiles.home.v1`; shared environmental bank plus area-specific additions in later milestones.
- `assets/metadata/characters.json` and tileset metadata: schemaVersion, assetId, PNG path, paletteId, frame dimensions/rectangles, origin, ground/sort anchor, opaque bbox, logical direction, mirrored flag, animation sequences/holds, source path and approval revision.
- `maps/home/bedroom.tmx` + exported map JSON with stable scene ID `bedroom`; sprite/collision/interaction metadata never hidden in renderer switch statements.
- `art/source/` for `.aseprite`/`.ora`, editable indexed PNG/palette data, or deterministic authoring sources plus manual correction layers. A procedural generator may author art; approved PNG outputs remain checked-in and inspectable.
- `docs/reviews/M1/` for `lineup-native.png`, `lineup-4x.png`, `bedroom-native.png` (240×160), `bedroom-4x.png` (960×640), guides and review notes. Export actual assets separately from labeled review sheets.

Export PNG at 1× with hard pixels and binary transparency for exploration sprites. Keep source palette/index data where practical, no JPEG, no blurred resizing, no outlines baked into blank margins. A 4× export must map every native pixel to exactly 4×4 identical pixels. Metadata must survive atlas reorder; validators in M3 check bounds/IDs/anchors/references. Build currently copies only HTML/CSS/src/icon, so M3 must explicitly add asset/map export paths and server MIME types.

## Interface standard and approval registry

Preserve accessible DOM menus/control semantics while native borders/icons/fonts are evaluated in M6. Never shrink touch hit areas to sprite dimensions. Primary touch targets proposed at ≥44 CSS px; preserve scroll and keyboard focus, player-entered names and live causal tank data. Manage/Stats/View remain the first tank choices. Whether dialogue/menu text is native bitmap or display-scale DOM is unresolved pending readability review.

Current approvals are recorded in the authoritative sections above: **Hero Boy V1's exact still is approved**, and the R11 girl concept is user-selected design direction. New native cast/animal outputs remain review proposals. Existing `docs/screenshots/` and M0 test captures document the prototype only. The earlier seven-character gate described the original plan; the user has now explicitly authorized the M1.C6 idle collection. This does not self-approve new sprites, world changes or animation.

Recovered character proposals: the separate art task delivered ten shared Hero/rival candidates B1–B5/G1–G5, one south-idle pose each. They are now in `assets/review/characters-v1/`, with editable indexed rows/palettes in `art/source/characters-v1/`. The combined [M1.I1 atlas](../assets/review/integration-v1/atlas.png) contains those ten and environment revision 2, using [stable IDs](../assets/review/integration-v1/atlas.json). It is a lossless review package, not a complete production sheet. No directional/animated character or revised indoor assets are implied. Inspect them together at [the static assembly review](../art-review/integration.html).


## Environment construction research and the rejected first draft — 2026-09-25

Read the [pinned environment research](reference-data/EMERALD_ENVIRONMENT_RESEARCH.md) for source links, assembly measurements and limits. Emerald uses shared primary and area-specific secondary tilesets, reusable 8×8 references inside 16×16 metatiles, and explicit layering. Selected measured examples are a **32×32 tree assembly** and **80×80 house assembly**; these are not universal silhouette dimensions. The earlier 32×48 tree and 96×80 house remain Critz proposals. Original Game Freak drawing software, brush/layer workflow and art review process were not verified; the decompilation's modern file organization does not establish those historical facts. No emulator observations were made.

The first Critz environment draft passed elementary grid constraints but the user rejected its visual style: “What I see you making does not look like Pokémon emerald.” Treat **all revision-1 environment PNGs/maps as rejected review history**. Technical validity is not visual approval. Do not integrate them, call them accepted, or use them as a new style reference.

### Revised drawing guidance — proposed, awaiting review

- **Draw volume before texture.** Roofs should show distinct planes, narrow side returns and layered eaves above a short front wall. Avoid a flat rectangle with a brick pattern and a front-facing triangular porch pasted onto it. Not every building needs the same silhouette.
- **Use material-specific pixel clusters.** Roof highlights describe the direction and overlap of tiles. Avoid a uniform decorative dash pattern. Windows need a simple cyan glass ramp and structural framing; walls should be calmer than roof edges.
- **Separate warm/cool material families.** Explore warm ochre/terracotta roof surfaces against pale cream plaster, cool gray-violet structural shadows and cyan window glass. Ground can be lighter mint green than deep foliage. These color relationships are observations/proposals, not a copied reference palette or exact final RGB specification.
- **Trees are compact foliage masses.** Prefer a 32×32 specimen for the next comparison, with jagged interlocking leaf clusters, bright yellow-green upper planes, dark connected lower canopy, and a mostly concealed trunk. Avoid smooth pear silhouettes, isolated circular highlight spots, long lollipop trunks and detached oval shadows. Taller variants remain possible after the small reference-scale specimen works.
- **Judge at native size.** A 240×160 proof and exact nearest-neighbor enlargement must both be shown. Generative mood studies may guide a direction but cannot establish native dimensions, palette membership or tile reusability. Exported native proofs require independent pixel checks.
- **Keep originality explicit.** Source assemblies can be studied outside the repository. New Critz palettes, pixels and assemblies must be authored separately; never ship source-game sprites. The checked-in generators read no reference artwork.
- **Build connected compositions.** Keep paths clear of border trees, bridge the full stream width, connect each doorstep to a lane, and leave room below south-facing doors. These static layout checks do not prove collision or movement.

Current review: [M1.E1 packet](reviews/M1-E1/README.md), [revision-2 native proof](../assets/review/environment-v2/house-tree-native.png), [exact 4× proof](reviews/M1-E1/revision-2/house-tree-4x.png). The revised proof is **awaiting user feedback**, not an accepted art example. Indoor furniture, all town maps and the production tileset must be revised after the direction is settled. The planned Hero/Mom scale test and G1/G2 gates remain outstanding.

## M1.C1 character-budget comparison (2026-09-27)

The user likes the supporting-character concept designs and requested animated 16×32 versus 24×32 samples. [The comparison](reviews/M1-C1/README.md) uses Mom, Kaid and Nugget at equal pixel zoom with the same 16px tile movement. This is a proposed character-only budget comparison, not a change to the 240×160 viewport, map grid, or approved production standard. Final budget and native-sheet acceptance await the user.
