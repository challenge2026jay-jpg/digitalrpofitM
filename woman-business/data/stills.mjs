// Rend des images de contrôle à des instants donnés (s) : node data/stills.mjs 1.5 7 12 ...
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";

const times = process.argv.slice(2).map(Number);
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const browserExecutable = "/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell";
const composition = await selectComposition({ serveUrl, id: "WomanBusiness", browserExecutable });
for (const t of times) {
  const frame = Math.round(t * 30);
  await renderStill({ composition, serveUrl, frame, output: `out/still_${String(t).padStart(5, "0")}.png`, browserExecutable, scale: 0.5 });
  console.log("ok", t);
}
