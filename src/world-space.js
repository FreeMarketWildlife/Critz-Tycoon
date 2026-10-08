// A saved (x,y) is the occupied ground cell. All actors use its bottom center,
// indoors and outdoors. Motion coordinates retain the original 16px units.
export const CAMERA_FOCUS_Y = 176;
export const worldFoot = (x, y) => ({x:x*2+16, y:y*2+32});
export const cellFoot = (x, y) => worldFoot(x*16,y*16);
