# M1.BH1 — Walking behind buildings

All twelve freestanding buildings now have reachable ground under their rear roof projection. Eleven allow one row; Old Waterworks allows two. Explicit rear-depth metadata separates roof extent from the solid footprint. The bottom walls remain blocked, and roofs plus chimneys draw over characters passing behind them. One cypress moves two cells east to clear the gardener cottage's rear corner. The cropped yard facade has its rear outside the map and remains an explicit boundary exception; the full home in Rootport has a walkable rear row.

The existing native art is unchanged. Doors, stairs, player names, story, economy, animal care and save keys are preserved. This is an original Critz implementation of the user's requested depth, not a new Emerald measurement.

## Verification

[104 unit checks](unit-results.txt) pass, including exact footprints, connected rear cells, solid remaining rows, attached chimney sorting and preservation of existing saved positions. [15 isolated browser checks](report.json) walk every rear strip with real movement input, verify blocked wall contact, compare [actual renderer occlusion pixels](occlusion.json), save/reload behind Waterworks and check runtime/assets. Synthetic saves use fresh isolated browser storage. Phone screenshots inspected; no physical Safari claim. The exact clean release repeats all 104 unit checks and 15 rear-building scenarios, plus [28 entrance regression checks](doors-report.json) covering all 26 doors, stairs and route connections, sideways entry prevention and runtime/asset errors. Existing unfinished character work is excluded.

![Behind the Rootport home](town-behind.png)
![Two rows behind Old Waterworks](liarsville-behind.png)

## Publication

[Play on your phone](https://critz-tycoon.freemarketwildlife.chatgpt.site). Source `86c310e42656024a041e0ac1954eddd42ba5a09b` is pushed to GitHub main and the Sites source repository. All **1,610 tested content files** match the archive exactly; only the hosting manifest is additional. [Archive verification](archive-check.json) · [Content hashes](tested-build-sha256.json). [Native deployment](deployment.json) succeeded at **2026-10-08 08:13:57 UTC**, preserving owner-private access. This final documentation receipt does not change the playable build or require another deployment. User traversal feedback remains pending; no full visual/movement approval is inferred.
