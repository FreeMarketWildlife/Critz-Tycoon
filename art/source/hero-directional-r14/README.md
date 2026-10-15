# HR14 review source

Original Critz assets only; reference-colored comparison files stay external. No game/editor runtime import points at these files. Lower coordinate rows describe observed costume planes, not bones or visible bare legs.

Repeatable author/review order, from repository root with Pillow-capable Python (`/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` on this host):

1. `build.py` rebuilds original Hero/dummy poses and ten editable projects. No reference image is read by this authoring script.
2. `reference.py EXTERNAL_DIR` rechecks pinned source PNG/table and emits only numeric observations to the repo. It expects the pinned table in the external directory and uses the previously verified source PNG path.
3. `checkpoint.py EXTERNAL_DIR` freshly decodes all8 supplied front frames and compares lower masks and rigid canonical pack/strap/composite registration.
4. `package.py EXTERNAL_DIR` prepares source/Hero/dummy proofs, true grids, all8 sheets and the featured dummy sheet. It creates `gif-jobs.json` externally.
5. `node art/source/hero-directional-r14/encode-review.mjs EXTERNAL_DIR/gif-jobs.json` uses the actual Sprite Editor model validator/exporter and declared GIF timing arrays.
6. `feature-guide.py` supplements `construction.json` with visible common features/contact spans and explicit null hidden joints, then emits the labelled separate guide. It changes no sprite pixels.
7. `interface-proof.py EXTERNAL_DIR` checks rows48–53 source envelopes, passing taper and idle50–55=P+2 silhouette registration; protects heads/lower contacts/canonical bag/strap pixels and exact original hand sites. It writes current interface/idle proofs. `seam-proof.py` and old row53-only plates are historical snapshots, superseded by this pass.
8. `verify.py EXTERNAL_DIR` independently checks native/source equality, observed lower alpha/material planes, pack registration, all28 decoded GIFs, normal/slow pixels and common-feature/contact metadata. Checks cannot approve art.

EXTERNAL_DIR for this review is `/Users/tanoshi/.codex/visualizations/2026/10/15/hero-hr14-review/`. Source GIF and PNG hashes/provenance, timing quantization, exact deliverables and interpretation limits are in `docs/reviews/M1-HR14/README.md`. Keep source rasters/palettes outside repo/build. Library export requires Eutychus/read-only final review; all art remains UNAPPROVED until the user responds.
