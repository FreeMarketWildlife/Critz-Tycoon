import './build-soundtrack.mjs';
import {prepareAssetDelivery,compactJsonDelivery} from './asset-delivery.mjs';
import { basename } from "node:path";
import { mkdir, cp, rm, stat, writeFile } from "node:fs/promises";
await rm("dist", { recursive: true, force: true });
await mkdir("dist");
for (const path of ["index.html", "style.css", "src", "icon.svg", "sprite-editor", "map-editor", "music", "art-review", "assets", "docs", "art"])
  await cp(path, `dist/${path}`, { recursive: true, filter: source => {const name=basename(source);return !["__pycache__","node_modules",".DS_Store"].includes(name)&&!name.startsWith("._")&&!/\.py[cod]$/.test(name);} });
const deliveries=[await prepareAssetDelivery('dist/assets'),await compactJsonDelivery('dist/docs'),await compactJsonDelivery('dist/art')];
const delivery={files:deliveries.reduce((n,d)=>n+d.files,0)};
await writeFile('dist/src/asset-urls.js',"// Generated production asset URLs.\nexport const CONTACT_MANIFEST='../assets/playable/contact/runtime.json';\n");
console.log(`Compacted ${delivery.files} delivery JSON files without changing their data; contact catalogue loads only in authoring tools.`);
console.log(
  `Built Critz: Tycoon. Entry: ${(await stat("dist/index.html")).size} bytes. No runtime dependencies.`,
);
