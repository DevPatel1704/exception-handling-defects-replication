# Manual validation of defect links: rating guide

**Why.** The outcome variable (post-release defective file) comes from linking Jira issue keys in commit messages to
the release files those commits change (docs/DATA.md §2). Key-based linking is known to be biased and noisy
(Bird et al., FSE 2009). Two raters check a seeded random sample of links (seed 2018, 40 per target or all links
if fewer) to estimate the **precision** of the labels and their **inter-rater agreement**.

**Material.** For each target, `data/new/<target>/validation/`:

* `packet.md`: one section per link with the Jira issue (type, status, resolution, dates, fix versions,
  summary), the full commit message, the files the commit changes (lines added/removed, ✔ = a linked release
  file), and automatic pre-checks. Open the issue and commit URLs when the packet is not enough.
* `rating_<Rater>.csv`: your sheet. **Rate independently**: do not open the other rater's sheet or discuss
  individual links until both sheets are complete.

Generate or refresh them with `./envrun.sh python src/collect/validation_packet.py` (it never overwrites a sheet).

## Questions and answer codes

Answer each question with `yes`, `no` or `unsure`. Put a one-line reason in `notes` for every `no` or `unsure`.

| Column | Question | `yes` when | `no` when (examples) |
|---|---|---|---|
| `q1_real_bug` | Does the issue describe a real defect in the system's behaviour? | Wrong behaviour, crash, leak, deadlock, data loss, wrong error handling, security flaw in production code | Feature request, improvement, refactoring, dependency/build/CI change, test-only or documentation-only issue filed as "Bug" |
| `q2_commit_fixes_issue` | Does this commit implement (part of) the fix for this issue? | The diff addresses the issue (also a cherry-pick/backport of the fix, or one of several fix commits) | Revert of the fix, unrelated commit that only mentions the key, pure formatting, merge commit |
| `q3_files_part_of_fix` | Are the linked release files (✔) changed as part of the fix? | At least one ✔ file contains a substantive part of the fix; for several ✔ files, most are | ✔ files only have incidental edits (imports, renames, whitespace, logging) while the fix is elsewhere |

A link is **valid** when all three answers are `yes`. `unsure` counts as not valid for precision and as its own
category for agreement.

## Procedure

1. Each rater fills in their own sheet for all targets (about 30–40 s per link, ~1.5 h in total).
2. Run `./envrun.sh python src/collect/validation_agreement.py`. It writes Cohen's κ and percent agreement per
   question, each rater's precision and the list of disagreements (`results/defect_link_validation.{csv,md}`).
3. Both raters discuss each disagreement and write the agreed answers into
   `data/new/<target>/validation/adjudicated.csv` (same columns as the sheets; only the disagreeing links are
   needed). Rerun the script: it reports the final precision with a 95% Wilson interval.

Interpretation (Landis & Koch): κ 0.41–0.60 moderate, 0.61–0.80 substantial, > 0.80 almost perfect.
