Mahmood Ahmad
Tahir Heart Institute
mahmood.ahmad2@nhs.net

MA Power: A Browser-Based Power and Sample Size Calculator for Random-Effects Meta-Analysis

How many studies does a planned random-effects meta-analysis need to achieve adequate statistical power, and how does between-study heterogeneity affect this requirement? The calculator implements the Valentine-Pigott-Rothstein power framework for binary outcomes on the log-odds-ratio scale and continuous outcomes using standardized mean differences. Power is computed from the true effect size, pooled standard error, between-study tau-squared derived from expected I-squared, and a user-specified alpha level. A worked example shows that 10 studies of 100 participants expecting an SMD of 0.3 with I-squared 50% achieve only 68% power (95% CI for power: 58 to 77% at this heterogeneity). Interactive power curves at four heterogeneity levels and a sensitivity table showing required study counts complement the primary calculation result. The tool generates manuscript-ready methods text and equivalent R code for the metapower package, supporting protocol registration. Power estimates are limited to the overall summary effect test and cannot address power for heterogeneity tests, moderator analyses, or subgroup comparisons.

Outside Notes

Type: methods
Primary estimand: Statistical power for planned meta-analysis
App: MA Power v1.0
Data: Worked examples based on Valentine et al. (2010) reference scenarios
Code: https://github.com/mahmood726-cyber/ma-power-calc
Version: 1.0
Certainty: moderate
Validation: DRAFT

References

1. Valentine JC, Pigott TD, Rothstein HR. How many studies do you need? A primer on statistical power for meta-analysis. J Educ Behav Stat. 2010;35(2):215-247.
2. Jackson D, Turner R. Power analysis for random-effects meta-analysis. Res Synth Methods. 2017;8(3):290-302.
3. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.

AI Disclosure

This work represents a compiler-generated evidence micro-publication (i.e., a structured, pipeline-based synthesis output). AI is used as a constrained synthesis engine operating on structured inputs and predefined rules, rather than as an autonomous author. Deterministic components of the pipeline, together with versioned, reproducible evidence capsules (TruthCert), are designed to support transparent and auditable outputs. All results and text were reviewed and verified by the author, who takes full responsibility for the content. The workflow operationalises key transparency and reporting principles consistent with CONSORT-AI/SPIRIT-AI, including explicit input specification, predefined schemas, logged human-AI interaction, and reproducible outputs.
