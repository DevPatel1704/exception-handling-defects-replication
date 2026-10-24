// Analyze a Repository: repository -> tags -> release window + tracker -> advanced -> Run Analysis (real backend job).
import * as api from "../api.js";
import { icon } from "../icons.js";
import { $, $$, dialog, esc, infoTip, toast } from "../ui.js";

const EXAMPLES = [
  ["Apache ZooKeeper", "https://github.com/apache/zookeeper", "Jira"],
  ["Hibernate ORM", "https://github.com/hibernate/hibernate-orm", "Jira"],
  ["Apache Hadoop", "https://github.com/apache/hadoop", "Jira"],
  ["Apache Commons Lang", "https://github.com/apache/commons-lang", "Jira"],
  ["Google Gson", "https://github.com/google/gson", "GitHub Issues"],
];
const URL_RE = /^https:\/\/[A-Za-z0-9.-]+(?::\d+)?(\/[A-Za-z0-9._~-]+)+\/?$/;
const TEST_EXCLUDE_OFF = "^$";   // exclude regex that never matches a path ("include test files")

let el, ctx, tags = [], loadedRepo = null;

export default {
  mount(root, c) {
    el = root; ctx = c;
    el.innerHTML = `
    <div class="stack-lg">
      <div class="card">
        <div class="card-head"><div><h2><span class="step-num">A</span> Repository</h2>
          <p>A public Git repository over https. Tags are read remotely with <code>git ls-remote</code>; nothing is cloned yet.</p></div></div>
        <div class="card-body">
          <label class="lbl" for="repoUrl">Repository URL ${infoTip("Any public https Git URL. GitHub, GitLab and Apache's GitHub mirrors work. Java projects are supported end to end.")}</label>
          <div class="row" style="flex-wrap:nowrap;align-items:flex-start">
            <div class="input-wrap" style="flex:1"><span class="lead">${icon("github", 16)}</span>
              <input class="input" id="repoUrl" type="url" placeholder="https://github.com/apache/zookeeper" autocomplete="off" spellcheck="false" aria-describedby="repoHelp"></div>
            <button class="btn btn-secondary" id="loadTags">${icon("refresh", 15)} Load tags</button>
          </div>
          <div class="help" id="repoHelp">Paste a repository link, or pick an example below.</div>
          <div class="row" style="margin-top:12px"><span class="small muted">Examples</span>
            ${EXAMPLES.map(([n, u, t]) => `<button class="chip" data-url="${u}" data-tip="${esc(u)}">${esc(n)} <span class="sub">· ${t}</span></button>`).join("")}</div>
        </div>
      </div>

      <div class="card" id="cfgCard">
        <div class="card-head"><div><h2><span class="step-num">B</span> Release window and issue tracker</h2>
          <p>Which snapshot to study, when defects are counted, and where bug reports live.</p></div>
          <span class="badge b-mute" id="tagCount">no tags loaded</span></div>
        <div class="card-body">
          <div id="cfgLocked" class="banner info"><span class="b-ic">${icon("info", 18)}</span><div class="small">Load the repository's tags in step A to configure the release window.</div></div>
          <fieldset id="cfgFields" disabled style="border:0;padding:0;margin:0" class="stack">
            <div class="grid-2">
              <div><label class="lbl" for="rel">Release ${infoTip("The source snapshot to analyse. All product metrics and exception-handling metrics are measured on this commit.")}</label><select class="input" id="rel"></select></div>
              <div><label class="lbl" for="post">Latest post-release tag ${infoTip("End of the defect observation window. Bugs reported after the release and fixed before this tag count as post-release defects.")}</label><select class="input" id="post"></select></div>
              <div><label class="lbl" for="prev">Previous release ${infoTip("Start of the pre-release window for process metrics (changes, churn, authors, pre-release bugs). Leave empty to use the whole history.")}</label><select class="input" id="prev"></select></div>
              <div><label class="lbl" for="lang">Language ${infoTip("Java runs end to end. C# is experimental: metrics without exception-flow analysis.")}</label>
                <select class="input" id="lang"><option value="auto">Auto-detect</option><option value="java">Java</option><option value="csharp">C# (experimental)</option></select></div>
            </div>
            <div class="timeline" aria-label="Release window timeline"><svg id="tl" height="86"></svg></div>
            <div class="help" id="tagNotes"></div>
            <div class="grid-2">
              <div><label class="lbl" for="tracker">Issue tracker ${infoTip("Where bug reports live. Jira follows the paper's definition (type Bug, resolution Fixed). GitHub Issues uses bug-labelled issues: a documented deviation. None: metrics only, no models.")}</label>
                <select class="input" id="tracker"><option value="jira">Jira</option><option value="github">GitHub Issues</option><option value="none">None (metrics only)</option></select></div>
              <div class="tr-jira"><label class="lbl" for="jiraBase">Jira base URL ${infoTip("e.g. https://issues.apache.org/jira or https://hibernate.atlassian.net. Cloud vs. Server API is detected automatically.")}</label>
                <input class="input" id="jiraBase" placeholder="https://issues.apache.org/jira"></div>
              <div class="tr-jira"><label class="lbl" for="jiraKeys">Jira project keys ${infoTip("Comma-separated, e.g. ZOOKEEPER or HADOOP, HDFS. Leave blank to detect them from commit messages; each detected key is verified against the Jira instance.")}</label>
                <input class="input" id="jiraKeys" placeholder="blank = detect automatically"></div>
              <div class="tr-github hidden"><label class="lbl" for="ghLabel">Bug-label pattern ${infoTip("Regular expression for labels that mark bugs on GitHub. Closed issues/PRs with such a label, referenced as #123 in a commit, count as defects.")}</label>
                <input class="input mono" id="ghLabel" value="(?i)\\b(bug|defect|regression)\\b"></div>
            </div>
            <details class="acc" id="adv"><summary>${icon("filter", 15)} Advanced settings <span class="muted small" style="font-weight:400">filters, cross-validation, reuse</span><span class="chev">${icon("chevDown", 16)}</span></summary>
              <div class="acc-body stack" style="padding-top:14px">
                <div class="grid-2">
                  <div><label class="lbl" for="inc">Source include pattern ${infoTip("Regex on the path. 'auto' uses Maven's src/main/java layout when most files follow it, else all .java files.")}</label><input class="input mono" id="inc" value="auto"></div>
                  <div><label class="lbl" for="exc">Exclude pattern ${infoTip("Regex on the path. Blank uses the default test/example/benchmark filter.")}</label><input class="input mono" id="exc" placeholder="default: tests, examples, benchmarks"></div>
                  <div><label class="lbl" for="reps">ML cross-validation repeats ${infoTip("Repeated stratified 5-fold CV. 5 repeats = 25 folds per learner and feature set.")}</label>
                    <select class="input" id="reps"><option>2</option><option>3</option><option selected>5</option><option>10</option></select></div>
                  <div class="stack" style="gap:10px;align-self:end">
                    <label class="check"><input type="checkbox" id="exTests" checked> <span>Exclude test files <span class="muted">(as in the paper)</span></span></label>
                    <label class="check"><input type="checkbox" id="reuse" checked> <span>Reuse unchanged results <span class="muted">(skip steps whose inputs did not change)</span></span></label>
                  </div>
                </div>
              </div></details>
            <div class="row" style="justify-content:space-between;margin-top:4px">
              <div class="small muted" style="max-width:640px">Runs in the background: ~5–10 min for a small project, up to ~1 h for a Hibernate-sized one (JTratch ~35 min, R ~15 min).
                One job runs at a time; later jobs wait in the queue.</div>
              <button class="btn btn-primary" id="run">${icon("play", 14)} Run Analysis</button>
            </div>
            <div class="help" id="runMsg" role="status"></div>
          </fieldset>
        </div>
      </div>
    </div>`;

    const url = $("#repoUrl", el);
    url.addEventListener("input", () => validateUrl(false));
    url.addEventListener("keydown", (e) => { if (e.key === "Enter") loadTags(); });
    $("#loadTags", el).onclick = loadTags;
    $$(".chip[data-url]", el).forEach(ch => ch.onclick = () => { url.value = ch.dataset.url; validateUrl(false); loadTags(); });
    $("#rel", el).onchange = onRelease;
    ["post", "prev"].forEach(id => $(`#${id}`, el).onchange = drawTimeline);
    $("#tracker", el).onchange = trackerUI;
    $("#run", el).onclick = run;
    ctx.onHealth.push(() => { const off = ctx.noServer; $("#loadTags", el).disabled = off; $("#run", el).disabled = off; });
    drawTimeline();
    new ResizeObserver(() => drawTimeline()).observe($(".timeline", el));
  },
};

function validateUrl(strict) {
  const v = $("#repoUrl", el).value.trim(), help = $("#repoHelp", el), input = $("#repoUrl", el);
  if (!v) { input.classList.toggle("invalid", strict); help.className = `help ${strict ? "err" : ""}`;
    help.textContent = strict ? "Type or paste a repository URL first (the grey text is only an example)." : "Paste a repository link, or pick an example below."; return false; }
  const ok = URL_RE.test(v) && !v.includes(".."); input.classList.toggle("invalid", !ok);
  help.className = `help ${ok ? "" : "err"}`;
  help.textContent = ok ? (v.includes("github.com") ? "GitHub repository: Jira or GitHub Issues can be used for defect labels." : "Git repository over https.")
    : "Use a public https URL like https://github.com/owner/repo (no ssh, no spaces).";
  return ok;
}

async function loadTags() {
  if (!validateUrl(true)) return;
  const btn = $("#loadTags", el), help = $("#repoHelp", el), repo = $("#repoUrl", el).value.trim();
  btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Loading tags…';
  help.className = "help"; help.textContent = "Reading tags with git ls-remote…";
  try {
    const r = await api.getTags(repo); tags = r.tags; loadedRepo = r.repo;
    const stable = tags.filter(t => !/(alpha|beta|rc\d*|cr\d*|snapshot|preview|milestone|-\d+$)/i.test(t)).length;
    help.className = "help ok"; help.innerHTML = `${icon("check", 13)} ${tags.length} tags found in <b>${esc(r.repo)}</b>.`;
    $("#tagCount", el).className = "badge b-acc"; $("#tagCount", el).textContent = `${tags.length} tags · ~${stable} stable`;
    fill("rel", r.suggested.release); fill("post", r.suggested.post_release); fill("prev", r.suggested.prev_release, true);
    notes(r.suggested.notes);
    const u = r.repo.toLowerCase();
    $("#tracker", el).value = u.includes("github.com/apache/") || u.includes("github.com/hibernate/") ? "jira" : u.includes("github.com/") ? "github" : "none";
    $("#jiraBase", el).value = u.includes("github.com/apache/") ? "https://issues.apache.org/jira" : u.includes("github.com/hibernate/") ? "https://hibernate.atlassian.net" : "";
    $("#jiraKeys", el).value = ""; trackerUI();
    $("#cfgFields", el).disabled = false; $("#cfgLocked", el).classList.add("hidden"); drawTimeline();
  } catch (e) {
    help.className = "help err"; help.textContent = e.message; $("#repoUrl", el).classList.add("invalid");
  } finally { btn.disabled = ctx.noServer; btn.innerHTML = `${icon("refresh", 15)} Load tags`; }
}

function fill(id, value, allowEmpty = false) {
  $(`#${id}`, el).innerHTML = (allowEmpty ? '<option value="">(none: whole history)</option>' : "") +
    tags.map(t => `<option ${t === value ? "selected" : ""}>${esc(t)}</option>`).join("");
}
const notes = (n) => { $("#tagNotes", el).textContent = (n || []).length ? `Suggestion: ${(n || []).join(" ")}` : "Tags pre-selected with the paper's convention: the latest patch of the same line ends the defect window."; };

async function onRelease() {
  drawTimeline();
  try { const r = await api.getTags(loadedRepo, $("#rel", el).value); fill("post", r.suggested.post_release); fill("prev", r.suggested.prev_release, true); notes(r.suggested.notes); drawTimeline(); }
  catch (e) { $("#tagNotes", el).innerHTML = `<span style="color:var(--bad)">${esc(e.message)}</span>`; }
}

function trackerUI() {
  const t = $("#tracker", el).value;
  $$(".tr-jira", el).forEach(x => x.classList.toggle("hidden", t !== "jira"));
  $$(".tr-github", el).forEach(x => x.classList.toggle("hidden", t !== "github"));
}

function drawTimeline() {
  const prev = $("#prev", el)?.value || "", rel = $("#rel", el)?.value || "release", post = $("#post", el)?.value || "post-release";
  const accent = "var(--accent)", mut = "var(--muted)", warn = "var(--warn-strong)";
  const svgEl = $("#tl", el), W = Math.max(svgEl.clientWidth || 800, 420), L = 70, M = W / 2, R = W - 70;
  svgEl.setAttribute("viewBox", `0 0 ${W} 86`);
  const pt = (x, label, sub, color) => `<circle cx="${x}" cy="40" r="7" fill="var(--surface)" stroke="${color}" stroke-width="3"/>
    <text x="${x}" y="22" text-anchor="middle" style="font:600 12px var(--font);fill:var(--text)">${esc(label.length > 26 ? label.slice(0, 25) + "…" : label)}</text>
    <text x="${x}" y="64" text-anchor="middle" style="font:11px var(--font);fill:${mut}">${sub}</text>`;
  $("#tl", el).innerHTML = `
    <line x1="${L}" y1="40" x2="${M}" y2="40" stroke="${mut}" stroke-width="3" stroke-linecap="round" opacity=".55"/>
    <line x1="${M}" y1="40" x2="${R}" y2="40" stroke="${warn}" stroke-width="3" stroke-linecap="round" opacity=".8"/>
    <text x="${(L + M) / 2}" y="82" text-anchor="middle" style="font:11.5px var(--font);fill:${mut}">${W < 760 ? "pre-release window" : "pre-release window · changes, churn, authors, pre-release bugs"}</text>
    <text x="${(M + R) / 2}" y="82" text-anchor="middle" style="font:11.5px var(--font);fill:${warn}">${W < 760 ? "post-release window" : "post-release window · defects reported after the release"}</text>
    ${pt(L, prev || "start of history", "previous release", mut)}${pt(M, rel, "release (studied snapshot)", accent)}${pt(R, post, "latest post-release", warn)}`;
}

function collect() {
  const ex = $("#exc", el).value.trim();
  return {
    repo: $("#repoUrl", el).value.trim(), release_tag: $("#rel", el).value, post_release_tag: $("#post", el).value, prev_release_tag: $("#prev", el).value,
    language: $("#lang", el).value,
    tracker: { type: $("#tracker", el).value, base: $("#jiraBase", el).value.trim(), project_keys: $("#jiraKeys", el).value.trim(), bug_label_regex: $("#ghLabel", el).value.trim() },
    include_regex: $("#inc", el).value.trim() || "auto", exclude_regex: $("#exTests", el).checked ? ex : TEST_EXCLUDE_OFF,
    repeats: parseInt($("#reps", el).value, 10), reuse: $("#reuse", el).checked,
  };
}

async function run() {
  const msg = $("#runMsg", el);
  if (!validateUrl(true)) return;
  if (!loadedRepo || !tags.length) { msg.className = "help err"; msg.textContent = "Load the tags first."; return; }
  const b = collect();
  if (b.release_tag === b.post_release_tag) { msg.className = "help err"; msg.textContent = "The post-release tag must differ from the release."; return; }
  if (b.tracker.type === "jira" && !/^https:\/\//.test(b.tracker.base)) { msg.className = "help err"; msg.textContent = "Enter the Jira base URL (https://…), or choose another tracker."; $("#jiraBase", el).focus(); return; }
  const tr = b.tracker.type === "jira" ? `Jira at ${b.tracker.base} (${b.tracker.project_keys || "keys auto-detected"})` : b.tracker.type === "github" ? "GitHub Issues (bug labels)" : "none: metrics only, no models";
  const ok = await dialog({
    title: "Start analysis?",
    body: `<dl class="kv"><dt>Repository</dt><dd class="mono">${esc(b.repo)}</dd><dt>Release</dt><dd class="mono">${esc(b.release_tag)}</dd>
      <dt>Defect window ends</dt><dd class="mono">${esc(b.post_release_tag)}</dd><dt>Pre-release from</dt><dd class="mono">${esc(b.prev_release_tag || "start of history")}</dd>
      <dt>Issue tracker</dt><dd>${esc(tr)}</dd><dt>Language</dt><dd>${esc(b.language)}</dd><dt>ML repeats</dt><dd>${b.repeats} × 5-fold</dd>
      <dt>Reuse</dt><dd>${b.reuse ? "yes, unchanged steps are skipped" : "no, everything re-runs"}</dd></dl>
      <p class="small muted" style="margin-top:12px">The job clones the repository, runs JTratch (needs ~6 GB of memory) and the authors' R models. You can follow it on the Analysis Jobs page and cancel it at any time.</p>`,
    actions: [{ label: "Cancel", value: null }, { label: "Start analysis", value: "go", kind: "btn-primary", autofocus: true }],
  });
  if (ok !== "go") return;
  const btn = $("#run", el); btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Creating job…'; msg.className = "help"; msg.textContent = "";
  try {
    const r = await api.createJob(b);
    toast(r.reused ? `Job queued (existing target ${r.target}; cached results reused where inputs are unchanged)` : `Job queued for ${r.target}`);
    ctx.navigate(`#/jobs/${encodeURIComponent(r.job_id)}`);
  } catch (e) { msg.className = "help err"; msg.textContent = e.message; }
  finally { btn.disabled = ctx.noServer; btn.innerHTML = `${icon("play", 14)} Run Analysis`; }
}
