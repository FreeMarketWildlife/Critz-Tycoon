# M1.ME9 — Named Rootport starting base

The user supplies a full v1 RLE map export and asks to name it Rootport, load it as an area, and send future replacement exports. Authoring only: this does not replace the adventure town or its saved progress.

Open [Rootport in Map Studio](https://critz-tycoon.freemarketwildlife.chatgpt.site/map-editor/?area=rootport). Alternatively use **Project → Load an area → Rootport → Open area**. The Map selector switches between Rootport and the cottage interior.

[Rootport source](../../../map-editor/areas/rootport.json) retains every submitted terrain/feature run, raw override, object ID, spawn, room, reciprocal warp, connection and note. Only the project name and outdoor map name change to Rootport. Stable internal map IDs are retained so the cottage return continues to work. Check map reports three supplied water cells lacking the existing2×2 minimum; they were not silently modified.

Named areas are catalogued in [areas.js](../../../map-editor/areas.js). Rootport revision1 uses `critz.map-editor.area.rootport.r1.v1`; generic `critz.map-editor.v1` and adventure keys remain unchanged. Opening a base first seeds the project from the shipped JSON, then restores that revision's draft if one exists. Edits autosave only in that area/revision slot. Corrupt drafts remain unchanged and failed/unknown area loads never enable writes to a fallback clearing. Normal and review editor routes keep their existing behavior.

For a future update, edit Rootport, choose **Copy for chat**, send the complete export and ask to make it the new Rootport base. Replace only this area JSON and increment the catalogue revision after checking it. The next revision gets its own fresh draft; old revision keys remain untouched. Do not delete old drafts, renumber linked IDs, invent terrain fixes or silently integrate the area into adventure maps.

Verification:313 main/current-publication-source unit tests pass; the earlier version52-based rehearsal passed305. Seven browser groups in isolated synthetic contexts cover the actual Open area control, exact base equality, separate-draft persistence/reload, generic-draft sentinel, Copy for chat,390px fit, corrupt-draft retention and unknown-area failure. Source syntax/build checks pass. No user browser storage was used for tests. Desktop and phone captures inspected; physical Safari remains unverified. While preparing publication, the independently accepted TN2/TN3 version53 went live. The older isolated release push was safely rejected. Final publication uses current main descended from the reconciled version53 source, preserving all accepted character, bench, fence and shore updates.

The unrelated screenshot question was traced to `art/source/overworld-live/terrain.mjs`'s connected `sward` ground patches, selected by `src/overworld.js`'s `turf` regions. The dark marks are decorative grass texture, not actual cast shadows or extra collision. No grass-art change was requested or included.

Next action: user opens the named Rootport draft, edits it, and sends a new complete export when ready to replace the published starting base.
