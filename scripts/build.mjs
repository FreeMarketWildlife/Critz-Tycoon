import './build-soundtrack.mjs';
import { basename } from "node:path";
import { mkdir, cp, rm, stat } from "node:fs/promises";
await rm("dist", { recursive: true, force: true });
await mkdir("dist");
for (const path of ["index.html", "style.css", "src", "icon.svg", "sprite-editor", "map-editor", "music", "art-review", "assets", "docs", "art"])
  await cp(path, `dist/${path}`, { recursive: true, filter: source => {const name=basename(source);return !["__pycache__","node_modules",".DS_Store"].includes(name)&&!name.startsWith("._")&&!/\.py[cod]$/.test(name);} });
console.log(
  `Built Critz: Tycoon. Entry: ${(await stat("dist/index.html")).size} bytes. No runtime dependencies.`,
);
