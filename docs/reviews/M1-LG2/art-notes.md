# M1.LG2 native equipment and Dorothy art

The user likes the prior greenhouse artwork and requests a smaller symmetrical layout, pumps/cords/hoses, optional shadows, Dorothy and shiny fish. These new assets preserve the previous collection byte-for-byte and remain pending review. Parent implementation owns the room, collision, bubbles, shiny recoloring, sparkles, mascot movement and optional shadow layer.

## Equipment and architecture

The room proposal is13×17 native32px cells (416×544), symmetry axis x208, centered door cell(6,16). Tubs retain96×64 original art at x2 and8, rows4/7/10/13. New hardware is intentionally small beside those tubs: a green-gray vented air pump on a low stand, fixed black electrical loop, protected green wall channel and pale teal airline.

| PNG | Native size | Placement / meaning |
|---|---|---|
| equipment-left / equipment-right | 32×64 each | Columns1/11 at each tub row;1×2 blocked ground footprint, parent records it explicitly |
| inlet-left / inlet-right | 16×32 each | Over tub at offsets(0,0)/(80,0); nozzle ends(12,25)/(3,25), ready for parent-rendered bubbles |
| wall-riser-left / wall-riser-right | 32×32 each | Optional visual wall-channel continuation; does not imply blocked walkway cells |
| header | 416×96 | Behind three existing aquarium props at x32/160/288,y32; equal ceiling lamps and exact mirrored window structure |
| greenhouse | 320×192 | Optional original facade refinement, center x160; regular mirrored roof bays and continuous centered threshold |

Left and right hardware are exact pixel mirrors. Header RGB is exactly symmetric. Facade geometry/alpha is exactly symmetric; architectural RGB is symmetric except the preserved original fish sign and practical single-sided door latch. The facade uses the same selected pixels/material ramps, with its roof ribs redrawn on the same trapezoid and foundation gaps closed. No cast-shadow pixels, glow gradient or moving cable animation are baked into new art. Material shading inside the pump remains part of the prop. Parent may animate a separate shadow layer without rewriting any artwork.

The equipment's last painted contact row is55 within its64px extent. Remaining bottom padding displays parent floor. Its whole assigned1×2-cell footprint stays blocked: this does not select a contact-lab transition ratio or import the concurrent M1.CT1 fine-approach proposal. Source dimensions and equipment scale are original Critz decisions, not new Emerald measurements. Character artwork and body measurements are untouched.

## Dorothy and golden hopper

Dorothy is an original plain common goldfish, kind16 after the original sixteen fancy individuals. Her more streamlined body, ordinary forehead without wen, dorsal fin and single forked tail distinguish her from the ranchu/oranda collection. She has a soft orange/cream palette, little dark eyes and a round mouth. Rarity and outcomes are parent-owned game rules.

| PNG | Native size | Columns |
|---|---|---|
| dorothy | 128×32 |32px side0,side1,top0,top1 |
| dorothy-front |64×32 |32px front0,front1 |
| dorothy-silhouettes |64×32 |32px top0,top1 |
| dorothy-world |64×16 |16px top0,top1,side0,side1 |
| gold-hopper |32×16 |16px side0,side1 |

Top views face north; side views face west. World views are independently authored16px clusters, never downsized observation sprites. Gold hopper is a separate golden fish mascot using brighter gold/cream materials. It has no human limbs; the parent supplies the hopping path. Both fish poses keep fins/tails attached. Shiny versions and sparkles are runtime effects; original indexed source palettes stay unchanged.

## Source and evidence

[Native context at3×](art-contact-3x.png), [facade at3×](art-facade-3x.png) and [Dorothy plus hopper at4×](art-dorothy-4x.png) were visually inspected. The context image displays two representative tub rows only, not the final complete gameplay room. Native assets and precise placement metadata live in `assets/review/luke-greenhouse-r2/manifest.json`.

Deterministic builder: `node art/source/luke-greenhouse-r2/build.mjs`. It authors integer pixels, reads existing indexed Critz art and creates native PNG plus editable palette-index source; it does not access reference images or modify the old collection. Independent Pillow validation: `python3 art/source/luke-greenhouse-r2/validate.py`. [Actual validation results](art-validation.json) prove all13 PNGs decode exactly to source, all dimensions and hashes match, alpha is binary, three equipment pairs mirror, header mirrors, facade alpha/architecture mirror, context is exact3× and all16 files in the previous asset directory retain their recorded hashes.

Technical validity does not replace the user's visual acceptance or parent gameplay/collision checks.
