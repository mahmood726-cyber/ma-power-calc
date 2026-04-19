# E156 Protocol — `ma-power-calc`

This repository is the source code and dashboard backing an E156 micro-paper on the [E156 Student Board](https://mahmood726-cyber.github.io/e156/students.html).

---

## `[82]` MA Power: A Browser-Based Power and Sample Size Calculator for Random-Effects Meta-Analysis

**Type:** methods  |  ESTIMAND: Statistical power for planned meta-analysis  
**Data:** Worked examples based on Valentine et al. (2010) reference scenarios

### 156-word body

How many studies does a planned random-effects meta-analysis need to achieve adequate statistical power, and how does between-study heterogeneity affect this requirement? The calculator implements the Valentine-Pigott-Rothstein power framework for binary outcomes on the log-odds-ratio scale and continuous outcomes using standardized mean differences. Power is computed from the true effect size, pooled standard error, between-study tau-squared derived from expected I-squared, and a user-specified alpha level. A worked example shows that 10 studies of 100 participants expecting an SMD of 0.3 with I-squared 50% achieve only 68% power (95% CI for power: 58 to 77% at this heterogeneity). Interactive power curves at four heterogeneity levels and a sensitivity table showing required study counts complement the primary calculation result. The tool generates manuscript-ready methods text and equivalent R code for the metapower package, supporting protocol registration. Power estimates are limited to the overall summary effect test and cannot address power for heterogeneity tests, moderator analyses, or subgroup comparisons.

### Submission metadata

```
Corresponding author: Mahmood Ahmad <mahmood.ahmad2@nhs.net>
ORCID: 0000-0001-9107-3704
Affiliation: Tahir Heart Institute, Rabwah, Pakistan

Links:
  Code:      https://github.com/mahmood726-cyber/ma-power-calc
  Protocol:  https://github.com/mahmood726-cyber/ma-power-calc/blob/main/E156-PROTOCOL.md
  Dashboard: https://mahmood726-cyber.github.io/ma-power-calc/

References (topic pack: heterogeneity / prediction interval):
  1. Higgins JPT, Thompson SG. 2002. Quantifying heterogeneity in a meta-analysis. Stat Med. 21(11):1539-1558. doi:10.1002/sim.1186
  2. IntHout J, Ioannidis JP, Rovers MM, Goeman JJ. 2016. Plea for routinely presenting prediction intervals in meta-analysis. BMJ Open. 6(7):e010247. doi:10.1136/bmjopen-2015-010247

Data availability: No patient-level data used. Analysis derived exclusively
  from publicly available aggregate records. All source identifiers are in
  the protocol document linked above.

Ethics: Not required. Study uses only publicly available aggregate data; no
  human participants; no patient-identifiable information; no individual-
  participant data. No institutional review board approval sought or required
  under standard research-ethics guidelines for secondary methodological
  research on published literature.

Funding: None.

Competing interests: MA serves on the editorial board of Synthēsis (the
  target journal); MA had no role in editorial decisions on this
  manuscript, which was handled by an independent editor of the journal.

Author contributions (CRediT):
  [STUDENT REWRITER, first author] — Writing – original draft, Writing –
    review & editing, Validation.
  [SUPERVISING FACULTY, last/senior author] — Supervision, Validation,
    Writing – review & editing.
  Mahmood Ahmad (middle author, NOT first or last) — Conceptualization,
    Methodology, Software, Data curation, Formal analysis, Resources.

AI disclosure: Computational tooling (including AI-assisted coding via
  Claude Code [Anthropic]) was used to develop analysis scripts and assist
  with data extraction. The final manuscript was human-written, reviewed,
  and approved by the author; the submitted text is not AI-generated. All
  quantitative claims were verified against source data; cross-validation
  was performed where applicable. The author retains full responsibility for
  the final content.

Preprint: Not preprinted.

Reporting checklist: PRISMA 2020 (methods-paper variant — reports on review corpus).

Target journal: ◆ Synthēsis (https://www.synthesis-medicine.org/index.php/journal)
  Section: Methods Note — submit the 156-word E156 body verbatim as the main text.
  The journal caps main text at ≤400 words; E156's 156-word, 7-sentence
  contract sits well inside that ceiling. Do NOT pad to 400 — the
  micro-paper length is the point of the format.

Manuscript license: CC-BY-4.0.
Code license: MIT.

SUBMITTED: [ ]
```


---

_Auto-generated from the workbook by `C:/E156/scripts/create_missing_protocols.py`. If something is wrong, edit `rewrite-workbook.txt` and re-run the script — it will overwrite this file via the GitHub API._