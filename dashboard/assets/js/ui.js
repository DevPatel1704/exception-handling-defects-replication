// Reusable UI building blocks: formatting, tooltips, toasts, dialogs, drawers, badges, sortable tables, states.
import { icon } from "./icons.js";

export const $ = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
export const esc = (s) => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
export function html(str) { const t = document.createElement("template"); t.innerHTML = str.trim(); return t.content.firstElementChild; }

export const isNum = (x) => x !== null && x !== undefined && x !== "" && !Number.isNaN(+x);
export const fmt = (x, d = 3) => (isNum(x) ? (+x).toFixed(d) : "—");
export const fmtInt = (x) => (isNum(x) ? Math.round(+x).toLocaleString("en-US") : "—");
export const fmtPct = (x, d = 1) => (isNum(x) ? `${(+x).toFixed(d)}%` : "—");
export const fmtSigned = (x, d = 3) => (isNum(x) ? `${+x > 0 ? "+" : ""}${(+x).toFixed(d)}` : "—");
export const fmtP = (p) => (!isNum(p) ? "—" : +p < 0.001 ? "< 0.001" : (+p).toFixed(3));
export function fmtBytes(b) {
  if (!isNum(b)) return "—"; const u = ["B", "KB", "MB", "GB"]; let i = 0, v = +b;
  while (v >= 1024 && i < u.length - 1) { v /= 1024; i++; }
  return `${v < 10 && i ? v.toFixed(1) : Math.round(v)} ${u[i]}`;
}
export function fmtDur(s) {
  if (!isNum(s)) return ""; s = +s;
  if (s < 60) return `${s < 10 ? s.toFixed(1) : Math.round(s)} s`;
  if (s < 3600) return `${Math.floor(s / 60)} min ${Math.round(s % 60)} s`;
  return `${Math.floor(s / 3600)} h ${Math.round((s % 3600) / 60)} min`;
}
export function relTime(iso) {
  if (!iso) return ""; const d = (Date.now() - new Date(iso).getTime()) / 1000;
  if (d < 60) return "just now"; if (d < 3600) return `${Math.round(d / 60)} min ago`;
  if (d < 86400) return `${Math.round(d / 3600)} h ago`; return new Date(iso).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}
export const fmtDate = (iso) => (iso ? new Date(iso).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" }) : "—");
export const shortSha = (s) => (s || "").slice(0, 10);
export const repoName = (url) => (url || "").replace(/\.git$/, "").split("/").slice(-2).join("/");

// ---------- tooltip (hover + keyboard focus on any [data-tip]) ----------
let tipEl;
export function initTooltips() {
  tipEl = html('<div class="tip" role="tooltip" id="tip"></div>'); document.body.appendChild(tipEl);
  const show = (e) => {
    const t = e.target.closest?.("[data-tip]"); if (!t) return;
    tipEl.textContent = t.getAttribute("data-tip"); tipEl.classList.add("show");
    const r = t.getBoundingClientRect(), w = tipEl.offsetWidth, hgt = tipEl.offsetHeight;
    let x = r.left + r.width / 2 - w / 2, y = r.top - hgt - 8;
    if (y < 6) y = r.bottom + 8; x = Math.max(6, Math.min(x, innerWidth - w - 6));
    tipEl.style.left = `${x}px`; tipEl.style.top = `${y}px`; t.setAttribute("aria-describedby", "tip");
  };
  const hide = (e) => { const t = e.target.closest?.("[data-tip]"); if (t) { tipEl.classList.remove("show"); t.removeAttribute("aria-describedby"); } };
  document.addEventListener("mouseover", show); document.addEventListener("mouseout", hide);
  document.addEventListener("focusin", show); document.addEventListener("focusout", hide);
}
/** Free-positioned tooltip used by charts. */
export function chartTip(text, x, y) {
  if (!tipEl) return; if (text === null) { tipEl.classList.remove("show"); return; }
  tipEl.innerHTML = text; tipEl.classList.add("show");
  const w = tipEl.offsetWidth, hgt = tipEl.offsetHeight;
  tipEl.style.left = `${Math.max(6, Math.min(x - w / 2, innerWidth - w - 6))}px`;
  tipEl.style.top = `${y - hgt - 12 < 6 ? y + 16 : y - hgt - 12}px`;
}
export const infoTip = (text) => `<span class="info-ic" tabindex="0" role="img" aria-label="More information" data-tip="${esc(text)}">${icon("info", 14)}</span>`;

// ---------- toast ----------
export function toast(msg, kind = "") {
  let box = $(".toasts"); if (!box) { box = html('<div class="toasts" aria-live="polite"></div>'); document.body.appendChild(box); }
  const t = html(`<div class="toast ${kind}">${icon(kind === "bad" ? "alert" : "check", 15)}<span>${esc(msg)}</span></div>`);
  box.appendChild(t); setTimeout(() => t.remove(), 3200);
}
export async function copyText(text, what = "Copied") {
  try { await navigator.clipboard.writeText(text); toast(`${what} to clipboard`); }
  catch { const ta = html("<textarea></textarea>"); ta.value = text; document.body.appendChild(ta); ta.select();
          try { document.execCommand("copy"); toast(`${what} to clipboard`); } catch { toast("Copy failed", "bad"); } ta.remove(); }
}

// ---------- overlay, dialog, drawer (Esc closes, focus returns to the opener) ----------
function trapFocus(container, e) {
  if (e.key !== "Tab") return;
  const f = $$('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])', container).filter(x => !x.disabled && x.offsetParent !== null);
  if (!f.length) return; const first = f[0], last = f[f.length - 1];
  if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
  else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
}
function openLayer(panel, onClosed) {
  const opener = document.activeElement; const ov = html('<div class="overlay"></div>');
  document.body.append(ov, panel); requestAnimationFrame(() => { ov.classList.add("show"); panel.classList.add("show"); });
  let closed = false;
  const close = () => {
    if (closed) return; closed = true; ov.classList.remove("show"); panel.classList.remove("show");
    document.removeEventListener("keydown", onKey); setTimeout(() => { ov.remove(); panel.remove(); onClosed && onClosed(); }, 230); opener?.focus?.();
  };
  const onKey = (e) => { if (e.key === "Escape") close(); else trapFocus(panel, e); };
  document.addEventListener("keydown", onKey); ov.addEventListener("click", close);
  setTimeout(() => ($('[autofocus]', panel) || $("button, [href], input, select", panel))?.focus(), 30);
  return close;
}
/** @returns {Promise<string|null>} the clicked action's value, or null if dismissed */
export function dialog({ title, body, actions = [{ label: "Close", value: null }], wide = false }) {
  return new Promise((resolve) => {
    const d = html(`<div class="dialog ${wide ? "wide" : ""}" role="dialog" aria-modal="true" aria-labelledby="dlg-t">
      <div class="dialog-head"><h3 id="dlg-t">${esc(title)}</h3></div><div class="dialog-body"></div><div class="dialog-foot"></div></div>`);
    const b = $(".dialog-body", d); typeof body === "string" ? (b.innerHTML = body) : b.appendChild(body);
    let result = null; const close = openLayer(d, () => resolve(result));
    const done = (v) => { result = v; close(); };
    actions.forEach(a => {
      const btn = html(`<button class="btn btn-sm ${a.kind || "btn-secondary"}">${esc(a.label)}</button>`);
      if (a.autofocus) btn.setAttribute("autofocus", ""); btn.onclick = () => done(a.value); $(".dialog-foot", d).appendChild(btn);
    });
  });
}
export function drawer({ title, body, narrow = false, actions = "" }) {
  const d = html(`<aside class="drawer ${narrow ? "narrow" : ""}" role="dialog" aria-modal="true" aria-labelledby="drw-t">
    <div class="drawer-head"><h3 id="drw-t">${title}</h3>${actions}<button class="icon-btn" aria-label="Close panel">${icon("x")}</button></div>
    <div class="drawer-body"></div></aside>`);
  const b = $(".drawer-body", d); typeof body === "string" ? (b.innerHTML = body) : b.appendChild(body);
  const close = openLayer(d); $(".drawer-head .icon-btn:last-child", d).onclick = close;
  return { el: d, body: b, close };
}

// ---------- status ----------
const JOB_BADGE = { queued: ["b-mute", "Queued"], running: ["b-run", "Running"], finished: ["b-ok", "Finished"],
  "finished with problems": ["b-warn", "Finished with problems"], cancelled: ["b-mute", "Cancelled"],
  interrupted: ["b-warn", "Interrupted"], error: ["b-bad", "Error"] };
export function jobBadge(status) {
  const [c, l] = JOB_BADGE[status] || ["b-mute", status];
  return `<span class="badge ${c}">${status === "running" ? '<span class="spinner" style="width:10px;height:10px;border-width:1.5px"></span>' : ""}${esc(l)}</span>`;
}
const STEP_BADGE = { done: ["b-ok", "Done"], reused: ["b-ok", "Reused"], running: ["b-run", "Running"], skipped: ["b-mute", "Skipped"],
  failed: ["b-bad", "Failed"], blocked: ["b-bad", "Blocked"], cancelled: ["b-mute", "Cancelled"], pending: ["b-mute", "Pending"] };
export const stepBadge = (s) => { const [c, l] = STEP_BADGE[s] || ["b-mute", s]; return `<span class="badge ${c}">${l}</span>`; };
export function stepIcon(s) {
  if (s === "running") return '<span class="spinner"></span>';
  if (s === "done") return icon("check", 15); if (s === "reused") return icon("refresh", 14);
  if (s === "failed") return icon("x", 15); if (s === "blocked") return icon("alert", 14);
  if (s === "skipped") return icon("chevRight", 14); if (s === "cancelled") return icon("stop", 12);
  return `<span class="tiny">·</span>`;
}

// ---------- states ----------
export const skeleton = (lines = 3, h = 14) => Array.from({ length: lines }, (_, i) =>
  `<div class="skel" style="height:${h}px;width:${92 - i * 13}%;margin:8px 0"></div>`).join("");
export const emptyState = (ic, title, text, actionHtml = "") =>
  `<div class="empty"><div class="e-ic">${icon(ic, 22)}</div><h3>${esc(title)}</h3><p class="small">${text}</p>${actionHtml}</div>`;
export const errorBox = (msg) => `<div class="banner bad"><span class="b-ic">${icon("alert", 18)}</span><div class="small">${esc(msg)}</div></div>`;

// ---------- sortable, filterable table ----------
/**
 * @param {HTMLElement} el container
 * @param {{key:string,label:string,num?:boolean,render?:(row)=>string,sort?:(row)=>any,tip?:string}[]} cols
 * @param {Object[]} rows
 * @param {{sortKey?:string, desc?:boolean, filter?:string, filterKeys?:string[], rowClass?:(row)=>string, empty?:string}} opts
 */
export function sortableTable(el, cols, rows, opts = {}) {
  const state = { key: opts.sortKey || null, desc: opts.desc ?? true, filter: "" };
  const render = () => {
    const q = state.filter.toLowerCase();
    let rs = q ? rows.filter(r => (opts.filterKeys || cols.map(c => c.key)).some(k => String(r[k] ?? "").toLowerCase().includes(q))) : rows.slice();
    if (state.key) {
      const c = cols.find(x => x.key === state.key); const g = c.sort || (r => r[c.key]);
      rs.sort((a, b) => { const x = g(a), y = g(b); const cmp = isNum(x) && isNum(y) ? x - y : String(x).localeCompare(String(y)); return state.desc ? -cmp : cmp; });
    }
    el.innerHTML = `<div class="table-wrap"><table class="t"><thead><tr>${cols.map(c => `<th class="sortable ${c.num ? "r" : ""}" data-k="${c.key}" tabindex="0"
      ${state.key === c.key ? `aria-sort="${state.desc ? "descending" : "ascending"}"` : ""} scope="col">${esc(c.label)}${c.tip ? " " + infoTip(c.tip) : ""}<span class="arrow">${state.key === c.key ? (state.desc ? "↓" : "↑") : "↕"}</span></th>`).join("")}</tr></thead>
      <tbody>${rs.length ? rs.map(r => `<tr class="${opts.rowClass ? opts.rowClass(r) : ""}">${cols.map(c => `<td class="${c.num ? "r" : ""}">${c.render ? c.render(r) : esc(r[c.key])}</td>`).join("")}</tr>`).join("")
        : `<tr><td colspan="${cols.length}" class="muted small" style="text-align:center;padding:18px">${esc(opts.empty || "No matching rows.")}</td></tr>`}</tbody></table></div>`;
    $$("th.sortable", el).forEach(th => {
      const go = () => { const k = th.dataset.k; state.desc = state.key === k ? !state.desc : true; state.key = k; render(); };
      th.onclick = go; th.onkeydown = (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } };
    });
  };
  render();
  return { setFilter: (q) => { state.filter = q; render(); }, setRows: (r) => { rows = r; render(); } };
}
