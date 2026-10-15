# PS1 editable native-grid side/back trial

Separate review candidate; front exact. [Source finding, changes, proofs and review limits](../../../docs/reviews/M1-PS1/README.md).

`build.py` reads frozen original HR14 art, applies native body contour/material decisions to NWE only and preserves head/hair/hands/contacts/rigid pack inputs. `changes.json` records exact final changed RGBA cells. Five `.sprite.json` projects retain original frame/tick order. Run the paired NB3 builder, then `proof.py` to verify actual saved layers and create normal/slow/native/4x comparisons. No original sprite bank or gameplay code is overwritten.
