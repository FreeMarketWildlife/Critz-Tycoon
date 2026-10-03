// Reference-only geometry and sampling. No artwork or palette mutation.
export function fitReference(cropWidth, cropHeight, width, height) {
  const scale = Math.min(width / cropWidth, height / cropHeight);
  const w = Math.max(1, Math.round(cropWidth * scale));
  const h = Math.max(1, Math.round(cropHeight * scale));
  return { x: Math.round((width - w) / 2), y: Math.round((height - h) / 2), w, h };
}

export function resizeReference(box, handle, dx, dy, locked, maximum = 2048) {
  let w = box.w, h = box.h;
  if (handle.includes('e')) w += dx;
  if (handle.includes('w')) w -= dx;
  if (handle.includes('s')) h += dy;
  if (handle.includes('n')) h -= dy;
  if (locked) {
    const ratio = box.w / box.h;
    const horizontal = /[ew]/.test(handle), vertical = /[ns]/.test(handle);
    if (horizontal && (!vertical || Math.abs(w / box.w - 1) >= Math.abs(h / box.h - 1))) h = w / ratio;
    else w = h * ratio;
    const scale = Math.max(1 / Math.min(box.w, box.h), Math.min(maximum / Math.max(box.w, box.h), w / box.w));
    w = box.w * scale; h = box.h * scale;
  }
  w = Math.max(1, Math.min(maximum, Math.round(w)));
  h = Math.max(1, Math.min(maximum, Math.round(h)));
  const x = handle.includes('w') ? box.x + box.w - w : handle.includes('e') ? box.x : box.x + (box.w - w) / 2;
  const y = handle.includes('n') ? box.y + box.h - h : handle.includes('s') ? box.y : box.y + (box.h - h) / 2;
  return { x: Math.round(x), y: Math.round(y), w, h };
}

// Box-area average in source sRGB space, with alpha-weighted RGB. Transparent
// RGB cannot darken the result. Each output cell integrates the source area it
// covers. Nearest mode samples its center. A crop excludes all exterior pixels.
export function sampleReference(source, sourceWidth, crop, width, height, method = 'average', background = null) {
  const out = new Uint8ClampedArray(width * height * 4);
  const sx = crop.w / width, sy = crop.h / height;
  const alpha = i => background && source[i] === background[0] && source[i + 1] === background[1] && source[i + 2] === background[2] ? 0 : source[i + 3] / 255;
  for (let y = 0; y < height; y++) {
    const top = crop.y + y * sy, bottom = crop.y + (y + 1) * sy;
    for (let x = 0; x < width; x++) {
      const dest = (y * width + x) * 4;
      if (method === 'nearest') {
        const px = Math.min(crop.x + crop.w - 1, Math.floor(crop.x + (x + .5) * sx));
        const py = Math.min(crop.y + crop.h - 1, Math.floor(crop.y + (y + .5) * sy));
        const i = (py * sourceWidth + px) * 4;
        out[dest + 3] = Math.round(alpha(i) * 255);
        if (out[dest + 3]) out.set(source.subarray(i, i + 3), dest);
        continue;
      }
      const left = crop.x + x * sx, right = crop.x + (x + 1) * sx;
      let r = 0, g = 0, b = 0, a = 0;
      for (let py = Math.floor(top); py < Math.min(crop.y + crop.h, Math.ceil(bottom)); py++) {
        const wy = Math.min(bottom, py + 1) - Math.max(top, py);
        for (let px = Math.floor(left); px < Math.min(crop.x + crop.w, Math.ceil(right)); px++) {
          const i = (py * sourceWidth + px) * 4;
          const weight = (Math.min(right, px + 1) - Math.max(left, px)) * wy * alpha(i);
          a += weight; r += source[i] * weight; g += source[i + 1] * weight; b += source[i + 2] * weight;
        }
      }
      if (a > 0) {
        out[dest] = Math.round(r / a); out[dest + 1] = Math.round(g / a); out[dest + 2] = Math.round(b / a);
        out[dest + 3] = Math.round(255 * a / (sx * sy));
      }
    }
  }
  return out;
}
