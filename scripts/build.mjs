import { mkdir, cp, rm, stat } from "node:fs/promises";
await rm("dist", { recursive: true, force: true });
await mkdir("dist");
for (const path of ["index.html", "style.css", "src", "icon.svg", "art-review", "assets", "docs", "art"])
  await cp(path, `dist/${path}`, { recursive: true });
console.log(
  `Built Critz: Tycoon. Entry: ${(await stat("dist/index.html")).size} bytes. No runtime dependencies.`,
);
