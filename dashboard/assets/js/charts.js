// Small dependency-free SVG charts. Every chart re-renders on container resize, exposes hover/focus tooltips,
// and gets an aria-label summary so the data is also available to screen readers.
import { chartTip, esc } from "./ui.js";

const NS = "http://www.w3.org/2000/svg";
let measureCtx;
function textWidth(s, font = "11.5px Inter, system-ui, sans-serif") {
  measureCtx = measureCtx || document.createElement("canvas").getContext("2d");
  measureCtx.font = font; return measureCtx.measureText(s).width;
}
function niceMax(v) {
  if (!(v > 0)) return 1; const e = 10 ** Math.floor(Math.log10(v)), m = v / e;
  return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * e;
}
// tick count chosen so the step is a round number (1, 2, 2.5 or 5 x 10^k) for the given nice maximum
function ticks(max, prefer = 5) {
  const round = (st) => { const m = st / 10 ** Math.floor(Math.log10(st)); return [1, 2, 2.5, 5, 10].some(v => Math.abs(m - v) < 1e-9); };
  const n = [prefer, 5, 4, 2, 6, 3].find(k => round(max / k)) || prefer;
  return Array.from({ length: n + 1 }, (_, i) => +(i * max / n).toPrecision(6));
}
const cssVar = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
// SVG presentation attributes do not reliably accept var(): resolve "var(--x)" to the computed colour
const resolve = (c) => { const m = /^var\((--[\w-]+)\)$/.exec(c || ""); return m ? cssVar(m[1]) : c; };

function mount(el, draw) {
  const run = () => { const w = el.clientWidth || 600; el.innerHTML = ""; draw(w); };
  run();
  if (el._ro) el._ro.disconnect();
  let last = el.clientWidth;
  el._ro = new ResizeObserver(() => { if (Math.abs(el.clientWidth - last) > 4) { last = el.clientWidth; run(); } });
  el._ro.observe(el);
}
function svg(w, h, label) {
  const s = document.createElementNS(NS, "svg");
  s.setAttribute("viewBox", `0 0 ${w} ${h}`); s.setAttribute("width", w); s.setAttribute("height", h);
  s.setAttribute("role", "img"); s.setAttribute("aria-label", label); return s;
}
function node(tag, attrs, parent, text) {
  const n = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
  if (text !== undefined) n.textContent = text; parent && parent.appendChild(n); return n;
}
function hatchDef(s, id, color) {
  const defs = node("defs", {}, s);
  const p = node("pattern", { id, width: 6, height: 6, patternUnits: "userSpaceOnUse", patternTransform: "rotate(45)" }, defs);
  node("rect", { width: 6, height: 6, fill: color }, p);
  node("line", { x1: 0, y1: 0, x2: 0, y2: 6, stroke: "rgba(255,255,255,.55)", "stroke-width": 2 }, p);
}
function bindTip(elm, html) {
  elm.setAttribute("tabindex", "0");
  const show = (e) => { const r = elm.getBoundingClientRect(); chartTip(html, e?.clientX ?? r.left + r.width / 2, e?.clientY ?? r.top); elm.classList.add("hover"); };
  const hide = () => { chartTip(null); elm.classList.remove("hover"); };
  elm.addEventListener("mousemove", show); elm.addEventListener("mouseleave", hide);
  elm.addEventListener("focus", () => show()); elm.addEventListener("blur", hide);
}

/**
 * Horizontal bar chart.
 * @param {HTMLElement} el
 * @param {{label:string, value:number, hatch?:boolean, color?:string, tip?:string}[]} items
 * @param {{valueFmt?:(v)=>string, color?:string, unit?:string, title:string, max?:number, barH?:number}} o
 */
export function hbar(el, items, o) {
  mount(el, (W) => {
    const barH = o.barH || 18, gap = 8, top = 6, bottom = 26, fmtv = o.valueFmt || (v => v.toFixed(3));
    const labelW = Math.min(Math.max(...items.map(i => textWidth(i.label)), 40) + 12, W * 0.45);
    const valW = Math.max(...items.map(i => textWidth(fmtv(i.value)))) + 10;
    const H = top + items.length * (barH + gap) + bottom, x0 = labelW, x1 = W - valW;
    const max = o.max || niceMax(Math.max(...items.map(i => i.value), 0));
    const s = svg(W, H, `${o.title}: ` + items.map(i => `${i.label} ${fmtv(i.value)}`).join("; "));
    const base = resolve(o.color) || cssVar("--accent");
    hatchDef(s, `h-${el.id || "c"}`, cssVar("--eh"));
    const g = node("g", { class: "grid" }, s);
    ticks(max, 4).forEach(t => {
      const x = x0 + (x1 - x0) * (t / max);
      node("line", { x1: x, x2: x, y1: top, y2: H - bottom + 4 }, g);
      node("text", { x, y: H - 8, "text-anchor": "middle" }, s, fmtv(t));
    });
    items.forEach((it, i) => {
      const y = top + i * (barH + gap), w = Math.max(1, (x1 - x0) * (it.value / max));
      const lab = it.label.length > 48 ? it.label.slice(0, 46) + "…" : it.label;
      node("text", { x: x0 - 8, y: y + barH / 2 + 4, "text-anchor": "end", class: "lbl-strong" }, s, lab);
      const r = node("rect", { x: x0, y, width: w, height: barH, rx: 3, class: "bar",
        fill: it.hatch ? `url(#h-${el.id || "c"})` : (resolve(it.color) || base) }, s);
      node("text", { x: x0 + w + 6, y: y + barH / 2 + 4 }, s, fmtv(it.value));
      bindTip(r, it.tip || `<b>${esc(it.label)}</b><br>${esc(fmtv(it.value))}${o.unit ? " " + esc(o.unit) : ""}`);
    });
    el.appendChild(s);
  });
}

/**
 * Grouped vertical bars with optional error bars (mean ± sd) and a dashed-free baseline reference line.
 * @param {{label:string, bars:{key:string,label:string,value:number,err?:number,color:string,tip?:string}[]}[]} groups
 * @param {{title:string, yLabel?:string, baseline?:{value:number,label:string}, valueFmt?:(v)=>string, height?:number}} o
 */
export function grouped(el, groups, o) {
  mount(el, (W) => {
    const fmtv = o.valueFmt || (v => v.toFixed(2));
    const H = o.height || 280, left = 46, top = 14, bottom = 40;
    const right = o.baseline ? Math.max(12, textWidth(`${o.baseline.label} ${fmtv(o.baseline.value)}`) * 0.62 + 14) : 12;   // label column for the baseline
    const vals = groups.flatMap(g => g.bars.map(b => b.value + (b.err || 0))).concat(o.baseline ? [o.baseline.value] : []);
    const max = niceMax(Math.max(...vals, 0.01));
    const s = svg(W, H, `${o.title}: ` + groups.map(g => `${g.label} ${g.bars.map(b => `${b.label} ${fmtv(b.value)}`).join(", ")}`).join("; "));
    const y = (v) => top + (H - top - bottom) * (1 - v / max);
    const gg = node("g", { class: "grid" }, s);
    ticks(max, 5).forEach(t => { node("line", { x1: left, x2: W - right, y1: y(t), y2: y(t) }, gg); node("text", { x: left - 6, y: y(t) + 4, "text-anchor": "end" }, s, fmtv(t)); });
    if (o.yLabel) node("text", { x: 12, y: top + (H - top - bottom) / 2, transform: `rotate(-90 12 ${top + (H - top - bottom) / 2})`, "text-anchor": "middle" }, s, o.yLabel);
    const gw = (W - left - right) / Math.max(groups.length, 1), inner = Math.min(gw * 0.78, 46 * Math.max(...groups.map(g => g.bars.length), 1));
    groups.forEach((g, gi) => {
      const n = g.bars.length || 1, bw = Math.min(40, inner / n - 4), gx = left + gi * gw + (gw - (bw + 4) * n) / 2;
      node("text", { x: left + gi * gw + gw / 2, y: H - bottom + 18, "text-anchor": "middle", class: "lbl-strong" }, s, g.label);
      g.bars.forEach((b, bi) => {
        const x = gx + bi * (bw + 4);
        const r = node("rect", { x, y: y(b.value), width: bw, height: Math.max(1, y(0) - y(b.value)), rx: 3, fill: resolve(b.color), class: "bar" }, s);
        if (b.err) {
          const cx = x + bw / 2, lo = y(Math.max(0, b.value - b.err)), hi = y(b.value + b.err), ink = cssVar("--text-2");
          node("line", { x1: cx, x2: cx, y1: lo, y2: hi, stroke: ink, "stroke-width": 1.2 }, s);
          node("line", { x1: cx - 4, x2: cx + 4, y1: hi, y2: hi, stroke: ink, "stroke-width": 1.2 }, s);
          node("line", { x1: cx - 4, x2: cx + 4, y1: lo, y2: lo, stroke: ink, "stroke-width": 1.2 }, s);
        }
        bindTip(r, b.tip || `<b>${esc(g.label)} · ${esc(b.label)}</b><br>${fmtv(b.value)}${b.err ? ` ± ${fmtv(b.err)}` : ""}`);
      });
    });
    if (o.baseline) {
      const by = y(o.baseline.value);
      node("line", { x1: left, x2: W - right, y1: by, y2: by, stroke: cssVar("--warn-strong"), "stroke-width": 1.5 }, s);
      const [l1, l2] = [o.baseline.label.replace(/ \(.*$/, ""), (o.baseline.label.match(/\((.*)\)/) || [, ""])[1]];
      node("text", { x: W - right + 6, y: by - 2, style: `fill:${cssVar("--warn")};font-weight:600` }, s, `${l1} ${fmtv(o.baseline.value)}`);
      if (l2) node("text", { x: W - right + 6, y: by + 12, style: `fill:${cssVar("--warn")}` }, s, l2);
    }
    node("line", { x1: left, x2: W - right, y1: y(0), y2: y(0), stroke: cssVar("--border-2") }, s);
    el.appendChild(s);
  });
}

/**
 * Diverging bars around zero (per-file SHAP contributions): right = raises defect probability.
 * @param {{label:string, value:number, tip?:string}[]} items
 */
export function diverging(el, items, o) {
  mount(el, (W) => {
    const barH = 16, gap = 7, top = 22, bottom = 22, fmtv = o.valueFmt || (v => (v > 0 ? "+" : "") + v.toFixed(3));
    const labelW = Math.min(Math.max(...items.map(i => textWidth(i.label)), 40) + 12, W * 0.42);
    const H = top + items.length * (barH + gap) + bottom, x0 = labelW + 8, x1 = W - 52, mid = (x0 + x1) / 2;
    const m = niceMax(Math.max(...items.map(i => Math.abs(i.value)), 1e-6));
    const s = svg(W, H, `${o.title}: ` + items.map(i => `${i.label} ${fmtv(i.value)}`).join("; "));
    const pos = "#C2410C", neg = "#2563EB";
    node("text", { x: mid + 6, y: 12 }, s, "raises defect risk →");
    node("text", { x: mid - 6, y: 12, "text-anchor": "end" }, s, "← lowers defect risk");
    items.forEach((it, i) => {
      const yv = top + i * (barH + gap), w = (x1 - mid) * Math.abs(it.value) / m;
      node("text", { x: x0 - 8, y: yv + barH / 2 + 4, "text-anchor": "end", class: "lbl-strong" }, s, it.label.length > 44 ? it.label.slice(0, 42) + "…" : it.label);
      const r = node("rect", { x: it.value >= 0 ? mid : mid - w, y: yv, width: Math.max(1, w), height: barH, rx: 3, fill: it.value >= 0 ? pos : neg, class: "bar" }, s);
      node("text", { x: it.value >= 0 ? mid + w + 5 : mid - w - 5, y: yv + barH / 2 + 4, "text-anchor": it.value >= 0 ? "start" : "end" }, s, fmtv(it.value));
      bindTip(r, it.tip || `<b>${esc(it.label)}</b><br>${fmtv(it.value)}`);
    });
    node("line", { x1: mid, x2: mid, y1: top - 4, y2: H - bottom + 4, stroke: cssVar("--border-2") }, s);
    el.appendChild(s);
  });
}

export const FEATURE_SET_COLORS = () => ({ TRAD: cssVar("--fs-trad"), "TRAD+FLOW": cssVar("--fs-flow"), "TRAD+AP": cssVar("--fs-ap"), "TRAD+EH": cssVar("--fs-eh") });
export const FEATURE_SET_LABEL = { TRAD: "TRAD", "TRAD+FLOW": "+FLOW", "TRAD+AP": "+AP", "TRAD+EH": "+EH" };
