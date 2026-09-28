# M 1.C 3 core cardinal walks — review candidates

Four characters × four cardinal directions × idle/stride A/stride B = 48 native poses. The south idle and complete palette of each character are identical to the current M 1.C 2 source.

The new views preserve canonical outfit, hair, skin and compact body family. Back views remove the face rather than recoloring facial pixels. West profiles are authored individually; east uses the corresponding symmetric silhouette with separately placed upper-left highlights. Girl/Mom profiles show overlapping puff volumes, the boy has an afro mass, and Nugget keeps grey hair, the broad brim and a readable side lens.

A stride uses one downward pixel of whole-head bob and a redrawn body/foot pose. Front/back arms alternate opposite the advanced foot; side near arms counter the near leg. Children retain short cream shoes; adult feet remain compact under trousers/coat. Every pose is one four-neighbor connected component, with no blank row through the figure.

Proof rows: south, north, west, east. Columns: idle, stride A, stride B. Proofs were inspected at 1×/4×/8×. Palette, bbox, connected components, baseline, head invariance and exact enlargement checks are in validation.json.

Assumptions: these human costumes/hair permit symmetric profile geometry; east is stored explicitly and re-lit. Relative feet and arms are art proposals for user review, not captured emulator observations. The 32-tick sequence stride A/idle/stride B/idle uses 8 ticks each, from the pinned source-derived walk table. No run poses, movement integration, collision changes or save changes are included.

Built-in imagegen produced one guide per character after current still inspection. Exact prompts, original generated paths and staged guide PNGs are in guides/. Generated pixels were not resampled into native artwork. Final visual acceptance remains with the user.
