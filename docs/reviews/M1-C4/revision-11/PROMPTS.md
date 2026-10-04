# Image generation prompts

Tool: built-in image_gen. Reference order: decoded user boy, exact editor skeleton, attached girl design screenshot. These prompts specify targets, not proof of generated pixel geometry.

## Initial concept (not selected)

Use case: stylized-concept.
Create a carefully proportioned PIXEL ART CONCEPT REVIEW of the girl Hero for Critz: Tycoon. This is one front-facing idle Black girl, age ten, using the SAME body anatomy and proportions as the supplied boy and basic skeleton.

REFERENCES in order:
1. boy-16x.png: authoritative user-created boy sprite, an exact 16x nearest-neighbor display of 32x64 pixels. Preserve underlying face/head size, eye locations, shoulder/torso dimensions, hands, pelvis, short legs, shoe size, stance and all body proportions.
2. skeleton-16x.png: authoritative bare-head/anatomy scaffold in the SAME 32x64 canvas. Blue is the bare skull/face, gray torso, pink arms/hands, green pelvis, coral legs. It is NOT clothing or skin coloring. Hair must extend above and wrap around this head; don't stretch the skull to the hair top.
3. attached small girl screenshot: reference for GIRL DESIGN ONLY: two dark brown/black afro puffs high on the sides, small coral-pink ties, short framing locks, coral rose shirt, blue shorts, burgundy shoes. Rebuild that appearance on references 1 and 2's larger exact anatomy. Do NOT copy screenshot's smaller/narrower body.

PRESENTATION: a polished but restrained landscape concept plate on plain warm off-white background with TWO equal-size panels. LEFT is a large clean pixelated full girl, labeled "GIRL HERO · CONCEPT". RIGHT repeats EXACTLY THE SAME girl, same scale and position within its frame, with a 32-column by 64-row faint square pixel grid and thin cyan dashed skull scaffold over the hair to show the rounded original bare head, labeled "SAME BODY · HAIR ABOVE SKULL". Preserve full 64-row frame space, with empty space above head; magnification exactly 12 screen pixels per native pixel in each panel. Panels are 384x768 logical screen pixels, side by side. Grid labels Y increase UP: 0 bottom, 10,20,30,40,50,60,64 top, X center at 16 marked by distinct fine muted rose line. One grid square is one native pixel. No giant fancy typography. Tiny clear callout "Hair volume" at puffs, "Skull guide" pointing to cyan outline. Footer "32 × 64 target • Front idle • Awaiting review".

CRITICAL PIXEL GEOMETRY, native indices measured TOP-DOWN:
Canvas 32x64, symmetry axis between x15 and x16. Underlying skull crown at row26, rounded bare cranium x4..27 broadening toward face; it does NOT begin at the highest puff.
Eye rectangles EXACTLY x12..13 and x18..19, y38..41, each 2x4, dark, retaining tiny upper glint treatment of supplied boy if useful.
Face/ear envelope x3..28; chin narrows to x8..23 at row44; no little pointed chin or adult face.
Body opaque row envelopes [left,right EXCLUSIVE]: row45 [7,25],46 [6,26],47 [5,27],48 [5,27],49 [4,28],50..52 [3,29],53 [4,28],54 [5,27] with original hand/torso separation,55..59 [7,25],60 [8,24],61 [9,23]. Preserve original gap between feet. Foot last occupied row61, rows62-63 empty. SAME broad stubby hands and same squat short legs as boy; no narrowing waist, no hourglass, no taller torso, no slim arms, no lengthened legs. Boy arms/skin extend beside shirt rows48..53, preserve those attachment points.
Design hair as two compact rounded curly puffs rooted just above skull, top around row20 or21, staying inside x2..29, with rounded stepped clusters and a few large highlights rather than noisy dots. Smoothly fitted dark hair cap follows skeleton cranium with forehead readable, puffs above crown. Girl overall ~28x42 including hair. No hair below shoulders that hides body contours. Short framing locks can end near chin.
Skin preserve boy's warm medium-deep brown skin family, dark outline, deliberate connected shadow/highlight clusters. Rose shirt, blue shorts, burgundy sneakers; clothing changes COLOR and decoration, NEVER body geometry. Pixel silhouettes and shading authored in individual native pixels: no enforced 2x2 chunky construction, no antialiasing inside sprite, no blurry edges, no subpixel detail, no gradients, no 3D.
A one-native-pixel dark exterior contour; interior hair fill is hair, not a thick outline. Front idle anatomy symmetric; light from upper left may make shading asymmetric. One single design, repeated for overlay only. Focus on cute grounded confident young child with proportionally LARGE rounded head and compact broad short body exactly like input boy.

## Clean concept refinement

Use case: identity-preserve. Pixel-art character concept.
EDIT reference 1 (the exact user-created BOY) into a GIRL. Reference 2 is its exact bare-head skeleton; reference 3 is the girl's visual design inspiration. Do NOT make a diagram or presentation board. Output ONLY ONE front-idle girl sprite on a completely UNIFORM OPAQUE light warm gray #e9e9e1 background. No transparency, no vignette, no shadows outside sprite, no glow, no blur, no labels, no grid.

Most important: keep boy body's existing silhouette and all anatomical proportions EXACTLY unchanged. Keep same rounded head and face width, same eyes and eye positions, same shoulders, wide compact torso, large stubby hands, short compact legs, same shoes and stance. Never feminize by narrowing body, reducing hands, reducing skull or lengthening legs. The girl is the same ten-year-old Black child body template. Girlhood reads through hairstyle and clothing colors. Only change HAIR and CLOTHING COLORS. Skin remains same warm deep brown as boy.

Hair: replace the boy's twists with two compact rounded natural afro puffs with coral pink ties, drawing from reference 3. Tight fitted hair cap over original bare-head dome. A simple center part and short temple locks. Puffs sit ABOVE and outside skull crown; skull stays fixed. Use restrained clean connected dark-brown/charcoal clusters, just two shades and sparse brown highlights; NOT many isolated dots. Puff tops extend 5 pixels above original skull crown, stay within total 28px width. Underlying skull starts native row26, puff tops around row21. No huge ears. No hair covering hands or shoulders.
Outfit: retain exact boy shirt silhouette, coral-rose shirt with cream sleeve trim; exact boy blue shorts shape; same footwear silhouette now burgundy with cream soles. No new details, backpack, skirt or props.
Render in the SAME 32x64 native logical pixel budget as boy source, with each native pixel a clean uniform large square. Keep entire canvas padding; do not zoom/crop to fit. Source eye rectangles at x12..13 and18..19, y38..41. Chin at row44, body rows45..61, feet last row61, two empty rows62..63. Head and body's on-canvas placement must not shift. Canvas top rows0..20 blank. Centerline x16. All new marks match the existing native cell size. One-pixel dark contour.
REPEAT: body unchanged, skull unchanged, hair adds volume ABOVE skull. Simpler clean native-scale design, not a detailed high-resolution illustration. Opaque LIGHT background across the entire image.
