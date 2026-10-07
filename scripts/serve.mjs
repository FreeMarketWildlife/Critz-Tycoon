import http from "node:http";
import { readFile, stat } from "node:fs/promises";
import { resolve, extname, sep } from "node:path";
const root = resolve(process.argv.includes("--dist") ? "dist" : ".");
const port = Number(process.env.PORT || 5173);
const types = {
  ".html": "text/html",
  ".js": "text/javascript",
  ".css": "text/css",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".gif": "image/gif",
  ".mp3": "audio/mpeg",
  ".mid": "audio/midi",
  ".zip": "application/zip",
  ".json": "application/json",
  ".md": "text/plain; charset=utf-8",
};
http
  .createServer(async (req, res) => {
    try {
      const pathname = decodeURIComponent(
        new URL(req.url, "http://localhost").pathname,
      );
      let file = resolve(root, "." + pathname);
      if (file !== root && !file.startsWith(root + sep))
        throw new Error("Invalid path");
      if ((await stat(file)).isDirectory()) file = resolve(file, "index.html");
      const data = await readFile(file);
      const headers = {
        "Content-Type": types[extname(file)] || "application/octet-stream",
        "Cache-Control": "no-cache",
        "Content-Length": data.length,
      };
      // Browser audio seeking needs byte ranges, including on the local phone preview.
      if (extname(file) === ".mp3") {
        headers["Accept-Ranges"] = "bytes";
        if (req.headers.range) {
          const match = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range);
          let start = 0, end = data.length - 1;
          if (match && (match[1] || match[2])) {
            if (match[1]) {
              start = Number(match[1]);
              if (match[2]) end = Math.min(end, Number(match[2]));
            } else start = Math.max(0, data.length - Number(match[2]));
          }
          if (!match || !(match[1] || match[2]) || start > end || start >= data.length) {
            res.writeHead(416, { "Content-Range": `bytes */${data.length}` });
            res.end();
            return;
          }
          res.writeHead(206, { ...headers, "Content-Range": `bytes ${start}-${end}/${data.length}`, "Content-Length": end - start + 1 });
          res.end(req.method === "HEAD" ? undefined : data.subarray(start, end + 1));
          return;
        }
      }
      res.writeHead(200, headers);
      res.end(req.method === "HEAD" ? undefined : data);
    } catch {
      res.writeHead(404);
      res.end("Not found");
    }
  })
  .listen(port, "0.0.0.0", () =>
    console.log(`Critz: Tycoon → http://localhost:${port}`),
  );
