// Affiche le texte exact des licences Mixkit (fenêtres ouvertes par des boutons sur https://mixkit.co/license/).
// Usage : node data/mixkit_license.cjs   (Chromium headless de l'environnement)
const { chromium } = require("playwright-core");
(async () => {
  const b = await chromium.launch({
    executablePath: "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
    proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined,
  });
  const p = await b.newPage();
  await p.goto("https://mixkit.co/license/", { waitUntil: "networkidle", timeout: 60000 });
  for (const k of ["sfxFree", "musicFree"]) {
    await p.click(`[data-license="${k}"]`);
    await p.waitForTimeout(2500);
    const txt = await p.evaluate(() => {
      const m = [...document.querySelectorAll("dialog, [role=dialog], [class*=modal]")].map((e) => e.innerText).filter((t) => t && t.length > 200);
      return m[0] || "";
    });
    console.log(`===== ${k} =====\n${txt.replace(/\n\s*\n+/g, "\n").trim()}\n`);
    await p.keyboard.press("Escape");
    await p.waitForTimeout(800);
  }
  await b.close();
})().catch((e) => { console.error(e.message); process.exit(1); });
