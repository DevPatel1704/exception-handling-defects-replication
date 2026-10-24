// Downloads: artifacts of one analysed release (or of the original-study reproduction), grouped by category.
import * as api from "../api.js";
import { icon } from "../icons.js";
import { $, emptyState, errorBox, esc, fmtBytes, repoName, skeleton } from "../ui.js";

let el, ctx;
const ORIGINAL = "_original";

export default {
  mount(root, c) {
    el = root; ctx = c;
    el.innerHTML = `<div class="page-head"><div><h1>Downloads</h1><p>Every file the pipeline produced, served directly from the repository's <code>data/</code> and <code>results/</code> folders.</p></div>
      <div class="row"><label class="sr-only" for="dlPick">Artifact set</label><select class="input" id="dlPick" style="min-width:300px"></select>
      <a class="btn btn-primary" id="dlAll" href="#">${icon("archive", 15)} Download all (.zip)</a></div></div>
      <div class="card"><div class="card-body" id="dlBody">${skeleton(6)}</div></div>`;
    $("#dlPick", el).onchange = (e) => ctx.navigate(`#/downloads/${encodeURIComponent(e.target.value)}`);
  },
  async show(param) {
    let idx = [];
    try { idx = await api.listResults(); } catch (e) { $("#dlBody", el).innerHTML = errorBox(e.message); return; }
    const t = param || (idx[0] ? idx[0].target : ORIGINAL);
    $("#dlPick", el).innerHTML = idx.map(i => `<option value="${esc(i.target)}" ${i.target === t ? "selected" : ""}>${esc(repoName(i.repo))} · ${esc(i.release)}</option>`).join("")
      + `<option value="${ORIGINAL}" ${t === ORIGINAL ? "selected" : ""}>Original study (reproduction files)</option>`;
    $("#dlBody", el).innerHTML = skeleton(6);
    let cats;
    try { cats = await api.getArtifacts(t); } catch (e) { $("#dlBody", el).innerHTML = errorBox(e.message); return; }
    const all = $("#dlAll", el);
    if (!cats.length) { all.classList.add("hidden"); $("#dlBody", el).innerHTML = emptyState("downloads", "No artifacts yet", "Files appear here as the pipeline steps finish."); return; }
    all.classList.remove("hidden"); all.href = api.archiveUrl(t);
    const total = cats.reduce((n, c) => n + c.files.reduce((m, f) => m + f.bytes, 0), 0), count = cats.reduce((n, c) => n + c.files.length, 0);
    all.setAttribute("download", ""); all.setAttribute("data-tip", `${count} files, ${fmtBytes(total)} before compression; the zip is built on request`);
    $("#dlBody", el).innerHTML = `<p class="small muted" style="margin-top:0">${count} files · ${fmtBytes(total)}</p>` + cats.map(c => `
      <div class="art-cat"><h3>${icon(catIcon(c.category), 15)} ${esc(c.category)} <span class="badge b-mute">${c.files.length}</span></h3>
        <div class="table-wrap"><table class="t"><thead><tr><th>File</th><th>Type</th><th class="r">Size</th><th>Folder</th><th class="r"><span class="sr-only">Download</span></th></tr></thead><tbody>
        ${c.files.map(f => `<tr><td><span class="row" style="gap:7px;flex-wrap:nowrap">${icon("file", 14)}<span class="mono">${esc(f.name)}</span></span></td>
          <td><span class="badge b-mute">${esc(f.type)}</span></td><td class="r">${fmtBytes(f.bytes)}</td><td class="mono small muted">${esc(f.folder)}</td>
          <td class="r"><a class="btn btn-ghost btn-sm" href="${esc(f.path)}" download="${esc(f.name)}" aria-label="Download ${esc(f.name)}">${icon("downloads", 13)} Download</a></td></tr>`).join("")}
        </tbody></table></div></div>`).join("");
  },
};

function catIcon(c) {
  if (/dataset/i.test(c)) return "database"; if (/defect|bug/i.test(c)) return "bug"; if (/model|reproduction|Table/i.test(c)) return "flask";
  if (/ML/i.test(c)) return "target"; if (/SHAP/i.test(c)) return "zap"; if (/log/i.test(c)) return "terminal"; if (/validation|sample/i.test(c)) return "shield";
  return "file";
}
