// Service layer: the only module that talks to dashboard/app.py. Types are JSDoc typedefs (no build step).

/**
 * @typedef {{git:?string, Rscript:?string, java8:?string, understand:?string, python:string,
 *            authors_package:boolean, jtratch_source:boolean}} Health
 * @typedef {{release:?string, post_release:?string, prev_release:?string, notes:string[]}} TagSuggestion
 * @typedef {{repo:string, tags:string[], suggested:TagSuggestion, github:boolean}} RepoTags
 * @typedef {{type:'jira'|'github'|'none', base?:string, project_keys?:string, bug_label_regex?:string}} TrackerInput
 * @typedef {{repo:string, release_tag:string, post_release_tag:string, prev_release_tag:string,
 *            language:'auto'|'java'|'csharp', tracker:TrackerInput, include_regex:string, exclude_regex:string,
 *            repeats:number, reuse:boolean}} JobRequest
 * @typedef {'pending'|'running'|'done'|'reused'|'skipped'|'failed'|'blocked'|'cancelled'} StepStatus
 * @typedef {{name:string, title:string, deps:string[], status:StepStatus, message:string,
 *            started:?string, ended:?string, seconds:?number}} PipelineStep
 * @typedef {'queued'|'running'|'finished'|'finished with problems'|'cancelled'|'interrupted'|'error'} JobStatus
 * @typedef {{id:string, target:string, status:JobStatus, created:string, started:?string, ended:?string,
 *            repo:string, release:?string, post_release:?string, progress:{finished:number,total:number},
 *            current_step:?string}} JobBrief
 * @typedef {JobBrief & {steps:PipelineStep[], log_tail?:string, error?:string, queue_position:number,
 *            reused_target:boolean, repeats:number, reuse:boolean}} Job
 * @typedef {{metric:string, name:string, group:'traditional'|'flow'|'anti-pattern', wald_chi2:number,
 *            p_value:number, direction:'+'|'-', effect_pct:number}} Predictor
 * @typedef {{model:'BASE'|'BSFC'|'BSAP', r2_optimism_reduced:?number, r2_apparent:?number, files:number,
 *            budget:number, potential_predictors:number, cutoff:number, predictors:Predictor[],
 *            dropped_base_significant?:string[]}} ModelResult
 * @typedef {{project:string, learner:string, feature_set:string, n_features:number, prevalence:number,
 *            pr_auc_mean:number, pr_auc_std:number, roc_auc_mean:number, roc_auc_std:number, f1_mean:number,
 *            f1_std:number}} MlResult
 * @typedef {{project:string, learner:string, feature_set:string, metric:string, trad_mean:number, ext_mean:number,
 *            delta_mean:number, delta_std:number, folds_improved:string, p_corrected_ttest:number}} MlUplift
 * @typedef {{target:string, repo:string, language:string, tags:Object, provenance:Object, tracker:Object,
 *            defect_mining:?Object, dataset:?Object, product_metrics_backend:?string, eh_profile:?Object,
 *            models:?{presented:ModelResult[], preliminary_all_files:Object[]}, ml:?{results:MlResult[], uplift:MlUplift[]},
 *            shap:?Object, paper_reference:?Object, files:Object<string,string>, caveats:string[]}} Summary
 * @typedef {{target:string, repo:string, release:string, language:string, tracker:string, generated:string,
 *            has_models:boolean, has_ml:boolean}} ResultIndexItem
 * @typedef {{name:string, path:string, type:string, bytes:number, folder:string}} ArtifactFile
 * @typedef {{category:string, files:ArtifactFile[]}} ArtifactCategory
 */

export const NO_SERVER_MSG = "The dashboard server is not reachable. Start it with ./envrun.sh python dashboard/app.py and open http://localhost:8000/";

export class ApiError extends Error {
  constructor(message, status = 0, noServer = false) { super(message); this.status = status; this.noServer = noServer; }
}

async function request(path, opts = {}) {
  let r;
  try { r = await fetch(path, { headers: { Accept: "application/json" }, ...opts }); }
  catch { throw new ApiError(NO_SERVER_MSG, 0, true); }
  const text = await r.text();
  let body = null; try { body = JSON.parse(text); } catch { /* not JSON */ }
  if (body === null) {
    if (!r.ok) throw new ApiError(`${NO_SERVER_MSG} (HTTP ${r.status} from ${location.host})`, r.status, true);
    throw new ApiError("Unexpected non-JSON answer from the server.", r.status);
  }
  if (!r.ok) throw new ApiError(body.error || r.statusText, r.status);
  return body;
}

/** @returns {Promise<Health>} */ export const getHealth = () => request("/api/health");
/** @returns {Promise<RepoTags>} */
export const getTags = (repo, release) =>
  request(`/api/tags?repo=${encodeURIComponent(repo)}${release ? `&release=${encodeURIComponent(release)}` : ""}`);
/** @param {JobRequest} body @returns {Promise<{job_id:string, target:string, reused:boolean}>} */
export const createJob = (body) => request("/api/jobs", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
/** @returns {Promise<JobBrief[]>} */ export const listJobs = () => request("/api/jobs");
/** @returns {Promise<Job>} */ export const getJob = (id) => request(`/api/jobs/${encodeURIComponent(id)}`);
/** @returns {Promise<Job>} */ export const cancelJob = (id) => request(`/api/jobs/${encodeURIComponent(id)}/cancel`, { method: "POST" });
/** @returns {Promise<ResultIndexItem[]>} */ export const listResults = () => request("/api/results");
/** @returns {Promise<Summary>} */ export const getSummary = (target) => request(`/api/results/${encodeURIComponent(target)}`);
/** @returns {Promise<ArtifactCategory[]>} */ export const getArtifacts = (target) => request(`/api/artifacts/${encodeURIComponent(target)}`);
/** @returns {Promise<Object<string,string>>} R column name -> readable metric name */ export const getMetricNames = () => request("/api/metric-names");
export const archiveUrl = (target) => `/api/archive/${encodeURIComponent(target)}.zip`;
export const logUrl = (jobId, step) => `/api/jobs/${encodeURIComponent(jobId)}/log/${encodeURIComponent(step)}`;

/** Step log as text (lines are "2026-10-24T13:06:36Z | message" for runs since the timestamped runner). */
export async function getLog(jobId, step) {
  let r; try { r = await fetch(logUrl(jobId, step)); } catch { throw new ApiError(NO_SERVER_MSG, 0, true); }
  if (!r.ok) throw new ApiError(`log not available (HTTP ${r.status})`, r.status);
  return r.text();
}

/** Fetch a CSV result file (served from results/ or data/new/) and parse it into objects. */
export async function getCsv(path) {
  let r; try { r = await fetch(path); } catch { throw new ApiError(NO_SERVER_MSG, 0, true); }
  if (!r.ok) throw new ApiError(`${path} not available (HTTP ${r.status})`, r.status);
  return parseCsv(await r.text());
}

export function parseCsv(text) {
  const rows = []; let row = [], cur = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"' && text[i + 1] === '"') { cur += '"'; i++; } else if (c === '"') q = false; else cur += c; }
    else if (c === '"') q = true;
    else if (c === ",") { row.push(cur); cur = ""; }
    else if (c === "\n") { row.push(cur.replace(/\r$/, "")); rows.push(row); row = []; cur = ""; }
    else cur += c;
  }
  if (cur || row.length) { row.push(cur.replace(/\r$/, "")); rows.push(row); }
  const head = rows.shift() || [];
  return rows.filter(r => r.length === head.length).map(r => Object.fromEntries(head.map((h, i) => [h, r[i]])));
}

/** Poll fn every `ms` while `keepGoing(result)` is true. Returns a stop() function. Swap for SSE/WebSocket later. */
export function poll(fn, ms, keepGoing, onResult, onError) {
  let stopped = false, timer = null;
  const tick = async () => {
    if (stopped) return;
    try { const r = await fn(); if (stopped) return; onResult(r); if (keepGoing(r)) timer = setTimeout(tick, ms); }
    catch (e) { if (!stopped) { onError && onError(e); timer = setTimeout(tick, ms * 3); } }
  };
  tick();
  return () => { stopped = true; clearTimeout(timer); };
}
