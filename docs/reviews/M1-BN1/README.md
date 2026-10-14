# Bench, vertical fence and water-edge review

M1.BN1 seating, then M1.ME8 vertical fences, then M1.WA9 water edges, implemented sequentially under the user's three requests. New native appearances and seating feel await their response; no wider M1/M2 gate is accepted by automated checks.

## Benches

Four native transparent bench orientations show backrest, planks, arms and legs. Four new seated Hero poses retain existing upper-body pixels and adapt the lower body; original gameplay Hero files stay unchanged. Walk into a seat through its front for a280ms hop. Release, then move outward through that same front to exit. Facing locks while seated; sides/rear and walking between seat lanes remain blocked. Exit checks the actual clear lane and fences again. Reduced motion suppresses the visual hop. Playtest seating is transient and never writes adventure saves or the editable project.

Existing `bench` v1 stamps mean south-facing benches. New `bench-up`, `bench-left`, `bench-right` stamps appear in search. Collision remains an explicit footprint; seating is a special transition into that otherwise blocked footprint. Reachability does not treat seating as a route through the bench. [Bench review](https://critz-tycoon.freemarketwildlife.chatgpt.site/map-editor/?review=bench).

## Fence and water corrections

Vertical wood, picket and barbed-wire sprites use narrow continuous side planes without wide ladder-like rungs. Horizontal-only frames and crossing rules are unchanged. Native32×64 registration and binary alpha remain exact;432 exhaustive native joining/band checks pass.

Raised water's straight north/left/right transitions have24 clear water pixels and8 combined ground/bank pixels. The straight south boundary remains exact. Corner shape changes join those revised side boundaries. Collision cells, surface identities, mixed-depth rules, still/moving loops, reflections, separate shadows and saves stay unchanged. Surface/depth transitions and sand do not gain raised cliffs. The entire shared field, native alias bank and all4,070 colored references use the revised geometry. Original256 water texture/animation frames and ten prop frames remain exact. [Water review](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/coast.html).

## Verification and publication

Main workspace:311 unit tests pass. Bench-only publication checkout started from actual Sites/live source `6f8198856ebde6b9e31724d97eb83d81c31be232`, then received these three corrections; pending TN2/TN3 changes are excluded. Publication checkout:303 units, standard syntax/build checks pass. Browser groups:6 bench,8 fence,17 doorway/ledge/fence regressions,14 coastal play and8 complete coast groups pass in isolated synthetic contexts; four orientations, entry/exit/facing lock, original draft sentinel, phone search/layout and no runtime errors are covered. Independent native/source/binary-alpha checks pass; all4,070 colored references match actual browser pixels. Native and actual desktop/phone captures inspected. Physical Safari remains unverified. Final production/package and deployment receipts are recorded alongside this file.

Useful beach-return previews/unique packed counts changed with the new geometry:446 native pieces,346 unique frames,100 wash sequences,1,918 colored tiles;15 supported masks,55 raw contexts,74 pairs and4,070 aliases remain. Every wave sequence still totals3.2 seconds. Earlier expected packed counts were updated only after regenerated exports and native/browser evidence established the new inventory.

Exact next action: user tests the bench's four seating directions and judges the revised vertical profiles and shoreline contact. Original Grove draft tab is preserved; a separate bench review is the handoff. Remaining unrelated TN3 edits remain outside these commits and publication.
