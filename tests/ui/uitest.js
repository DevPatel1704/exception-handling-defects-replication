// Real-browser UI test of the ExceptionLab dashboard (headless Edge/Chrome via puppeteer-core).
// Setup:  cd tests/ui && npm install          (puppeteer-core only; it uses your installed browser)
// Run:    ./envrun.sh python dashboard/app.py   (in another terminal), then
//         node tests/ui/uitest.js pages        # visits every page, exercises interactions, writes shots/*.png
//         node tests/ui/uitest.js cancel       # submits a REAL job through the form, then cancels it from the UI
// Env:    BROWSER=<path to msedge.exe or chrome.exe>   DASHBOARD=http://127.0.0.1:8000
const puppeteer = require("puppeteer-core");
const path = require("path");
const BASE = (process.env.DASHBOARD || "http://127.0.0.1:8000") + "/dashboard/index.html";
const BROWSER = process.env.BROWSER || ["C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe", "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "/usr/bin/google-chrome", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"].find(p => require("fs").existsSync(p));
const OUT = path.join(__dirname, "shots");   // gitignored
require("fs").mkdirSync(OUT, { recursive: true });
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const mode = process.argv[2] || "pages";

(async () => {
  const browser = await puppeteer.launch({ executablePath: BROWSER,
    headless: "new", args: ["--no-first-run", "--disable-extensions"] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 1000 });
  const errors = [];
  page.on("pageerror", e => errors.push("pageerror: " + e.message));
  page.on("console", m => { if (m.type() === "error") errors.push("console: " + m.text()); });
  page.on("requestfailed", r => errors.push("requestfailed: " + r.url()));
  page.on("response", r => { if (r.status() >= 400) errors.push(`HTTP ${r.status()}: ${r.url()}`); });
  await page.evaluateOnNewDocument(() => { try { localStorage.setItem("theme", "light"); } catch (e) {} });
  const go = async (hash, wait = 1800) => { await page.goto(BASE + hash, { waitUntil: "networkidle0" }); await sleep(wait); };
  const shot = async (name, full = true) => { await page.screenshot({ path: path.join(OUT, name + ".png"), fullPage: full }); console.log("shot", name); };
  const text = (sel) => page.$eval(sel, e => e.innerText).catch(() => "(missing)");

  if (mode === "pages") {
    await go("#/overview"); await shot("01-overview");
    console.log("overview repro:", (await text("#ovRepro")).split("\n")[0], "| jobs:", (await page.$$("#ovJobs .job-item")).length);

    await go("#/analyze");
    await page.type("#repoUrl", "https://github.com/apache/zookeeper");
    await page.click("#loadTags");
    await page.waitForFunction(() => !document.querySelector("#cfgFields").disabled, { timeout: 60000 });
    await sleep(500);
    console.log("analyze help:", await text("#repoHelp"), "| rel:", await page.$eval("#rel", e => e.value), "| post:", await page.$eval("#post", e => e.value),
      "| prev:", await page.$eval("#prev", e => e.value), "| tracker:", await page.$eval("#tracker", e => e.value));
    await page.select("#rel", "release-3.7.0"); await sleep(2500);
    console.log("after release change -> post:", await page.$eval("#post", e => e.value), "| prev:", await page.$eval("#prev", e => e.value));
    await page.click("#adv summary"); await sleep(300);
    await shot("02-analyze");
    await page.click("#run"); await sleep(700);
    console.log("dialog:", (await text(".dialog")).split("\n").slice(0, 3).join(" | "));
    await shot("03-run-dialog", false);
    await page.keyboard.press("Escape"); await sleep(500);
    console.log("dialog closed:", !(await page.$(".dialog")));

    await go("#/results/hibernate-5.1", 2500); await shot("04-results");
    const sections = await page.$$eval("#resBody h2", hs => hs.map(h => h.innerText.trim()));
    console.log("results sections:", sections.join(" | "));
    const chip = await page.$(".pchip.eh"); if (chip) { await chip.click(); await sleep(600); await shot("05-predictor-drawer", false);
      console.log("drawer:", (await text(".drawer")).split("\n").slice(0, 2).join(" | ")); await page.keyboard.press("Escape"); await sleep(400); }
    await page.click('#secML [data-l="LR"]'); await sleep(400);
    console.log("ML table rows after hiding LR:", (await page.$$("#secML tbody tr")).length);
    await page.click('#secML [data-m="roc_auc"]'); await sleep(400);
    console.log("ML header after ROC switch:", await page.$eval("#secML thead", e => e.innerText.replace(/\s+/g, " ")));
    const pf = await page.$("#perFile"); if (pf) { await pf.click(); await sleep(2500); await shot("06-perfile", false);
      console.log("per-file info:", (await text("#pfInfo")).slice(0, 140)); await page.keyboard.press("Escape"); await sleep(400); }
    await page.type("#apSearch", "catch"); await sleep(300);
    console.log("AP rows filtered 'catch':", (await page.$$("#apTable tbody tr")).length);

    await go("#/results/zookeeper-release-3.6.0", 2500);
    console.log("zk 3.6 warning badge:", !!(await page.$("#secModels .badge.b-warn")), "| caveats:", (await page.$$(".caveat")).length);
    await go("#/original", 3500); await shot("07-original");
    console.log("original metric:", (await text("#oTable4 .metric .m-val")), "| t4 rows:", (await page.$$("#t4 tbody tr")).length, "| shap charts:", (await page.$$("#oSHAPGrid svg")).length);
    await go("#/downloads/hibernate-5.1", 2000); await shot("08-downloads");
    console.log("downloads categories:", (await page.$$(".art-cat")).length, "| zip href:", await page.$eval("#dlAll", e => e.getAttribute("href")));
    await go("#/jobs", 2500); await shot("09-jobs");
    const logBtn = await page.$('[data-log="models"]'); if (logBtn) { await logBtn.click(); await sleep(1500); await shot("10-log-drawer", false);
      console.log("log lines:", (await page.$$(".drawer .ln")).length); await page.keyboard.press("Escape"); await sleep(300); }
    await page.click("#themeBtn"); await sleep(500); await go("#/results/hibernate-5.1", 2500); await shot("11-results-dark", false);
    await page.click("#themeBtn"); await sleep(300);
    await page.setViewport({ width: 390, height: 844, isMobile: true }); await go("#/overview", 1500); await shot("12-mobile", false);
    await page.click("#menuBtn"); await sleep(500); await shot("13-mobile-drawer", false);
  }
  if (mode === "cancel") {
    await go("#/analyze");
    await page.type("#repoUrl", "https://github.com/apache/zookeeper"); await page.click("#loadTags");
    await page.waitForFunction(() => !document.querySelector("#cfgFields").disabled, { timeout: 60000 });
    await page.select("#rel", "release-3.7.0"); await sleep(2500);
    await page.click("#run"); await sleep(700);
    await page.$$eval(".dialog-foot button", bs => bs.find(b => b.textContent.includes("Start")).click());
    await page.waitForFunction(() => location.hash.startsWith("#/jobs/"), { timeout: 30000 });
    const jobId = decodeURIComponent(await page.evaluate(() => location.hash.slice(7)));
    console.log("job created:", jobId);
    await page.waitForSelector("#cancelJob", { timeout: 30000 }); await sleep(2500);
    await page.click("#cancelJob"); await sleep(600);
    console.log("confirm dialog:", (await text(".dialog")).split("\n")[0]);
    await page.$$eval(".dialog-foot button", bs => bs.find(b => b.textContent.trim() === "Cancel job").click());
    await page.waitForFunction(() => /Cancelled/.test(document.querySelector("#jobDetail")?.innerText || ""), { timeout: 60000 });
    console.log("job status after cancel:", await page.$eval("#jobDetail .card-head .badge", e => e.innerText));
    console.log("steps:", (await page.$$eval("#jobDetail .stepper li", ls => ls.map(l => l.className.replace("s-", "")))).join(","));
  }
  console.log(errors.length ? "ERRORS:\n" + [...new Set(errors)].join("\n") : "no browser errors");
  await browser.close();
})().catch(e => { console.error("TEST CRASH:", e); process.exit(1); });
