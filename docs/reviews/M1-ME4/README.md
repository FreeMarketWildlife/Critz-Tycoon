# M1.ME4 — Buildings, exits, fences and landings

User requested a consistent revision3 building treatment, indoor exit mats, always-open entrances, walk-behind fence rails and reliable ledge hops with landing dust. The playable revision is [Map Studio revision4](https://critz-tycoon.freemarketwildlife.chatgpt.site/map-editor/?review=me4); the adventure uses the same standard facade renderer. The custom greenhouse stays intact. No roster/world expansion or wider visual/feel approval is inferred.

The shared native renderer uses the original revision3 bank. Three closed-door and three always-open editor stamps retain semantic footprints and v1 imports. Reciprocal room links derive indoor-only mats/light cues, including legacy v1 projects. Standard adventure buildings now share this facade treatment; wide waterworks repeats native modules. All existing movement-only travel remains available.

Fence collision is an edge-crossing rule shared between the editor and adventure player/NPC movement. Same-row actors draw behind the raised rail, below-row actors in front. Other blockers and map guards remain explicit. Editor overlays show barrier edges. Save-position recovery traverses the same fence edges.

The reported intermittent ledge bug was a direction-change handoff: a jump destination could be accepted by the one-cell walking controller. A separate tested controller accepts every jump at the appropriate action boundary and prohibits jump targets in ordinary walking. Landing dust starts once, with five native poses and a reduced-motion first pose. A ledge landing on a passage finishes its hop and dust before travelling.

## Validation

236 unit tests,505 independent native checks and86 relevant release-browser scenarios pass:22 editor,17 revision4,8 revision3 regression,30 adventure doorway and9 full integration checks. Native pixel proof verifies that the rail covers Hero on its row and the five dust poses are distinct with binary alpha. All six variants enter and return. Screenshots were inspected for indoor-only mats, inward open-exit daylight, fence depth and landing dust. Browser reports are saved beside this record. One intermediate door run hit a temporarily unavailable atlas during a rebuild; the stable-release rerun passes all30 checks. Runtime files are frozen for packaging and checked byte-for-byte against the tested build.

Use `node --test tests/*.test.mjs`, the original native checker `art/source/map-studio-r3/check.py`, and the five corresponding browser scripts against the built release. See [revision4 checks](revision4-checks.json), [door checks](doors-checks.json), [integration checks](integration-checks.json) and [native proof](native-check.json). All browser contexts are isolated with synthetic fixtures; no user browser save storage is tested. Original atlas pixels and save keys remain unchanged. Physical Safari is unverified. New appearance/feel remains for the user to judge.

## Publication

Runtime source `0e6d29fc834baeae673c793b2976740e14d459cd` is pushed to GitHub main with remote SHA verified, and published as owner-private version47. [Successful deployment receipt](deployment.json) and [archive proof](archive-check.json) verify the tested1,337 runtime files and all2,684 build files against the2,685-file archive. The exact hosting manifest is the sole archive addition; no resource forks or caches. Browser handoff is queued in this chat. Final evidence is documentation only. Exact next action: user tests the revision4 link above; final appearance/feel acceptance is still pending.
