# M1.ME5 — Two-tile fences

The user confirms the collision and corrects the visual registration. All fence sprites use32×64 native frames with paint only in rows16–47 and transparent outer half tiles. The new shared bank replaces ME4’s upward draw offset in the adventure and editor. Wood was checked before adding white picket and barbed-wire variants. Vertical runs have continuous rails and attached crosspieces. No collision policy, save keys, authored layout, buildings, characters or economy changes.

[Playable fence review](https://critz-tycoon.freemarketwildlife.chatgpt.site/map-editor/?review=me5) demonstrates all three styles, horizontal/vertical runs, corners, junctions and gaps. The new styles are searchable semantic editor brushes and survive v1 export/import. Existing adventure fences use revised wood. Main branch; user appearance feedback remains pending.

245 unit tests,432 independent native fence checks and56 release-browser scenarios pass (8 fence,22 editor,17 ME4 regression,9 adventure integration). Native/grid/phone and front/behind views inspected. Every style paints only rows16–47, all horizontal/vertical edge pairs join exactly, and projected lower halves remain visible when their anchor is above the viewport. Wood144-check proof preceded adding variants. The adventure integration harness now observes actual committed tile steps instead of assuming wall-clock holds yield fixed tile counts; its stable rerun passes. Tests use isolated synthetic storage; physical Safari is unverified.

Publication pending. Exact next action: commit/push and publish the matching checked build, then user reviews the three fence styles.
