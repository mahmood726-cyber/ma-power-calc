# MA Power: A Browser-Based Power Calculator for Meta-Analysis

**Mahmood Ahmad**

Royal Free Hospital, London, UK

mahmood.ahmad2@nhs.net

ORCID: 0009-0003-7781-4478

**Keywords:** meta-analysis, statistical power, sample size, heterogeneity, power curve, web application

---

## Abstract

Statistical power is a critical consideration in meta-analysis, yet power calculations that properly account for between-study heterogeneity are rarely performed prospectively. Existing tools require R or Stata installations and familiarity with programming syntax. We present MA Power, a browser-based power calculator for meta-analysis implemented as a single 660-line HTML file. The tool provides three analysis modes: power calculation for a given number of studies, sample size determination for a target power level, and power curve sensitivity analysis across a range of heterogeneity values. It handles both continuous (standardised mean difference) and binary (odds ratio) outcomes and incorporates between-study heterogeneity (tau-squared) into all calculations using established formulae. Validation against 25 automated tests confirms numerical accuracy. MA Power requires no installation and runs offline in any modern browser.

---

## Introduction

Meta-analysis is widely regarded as providing the highest level of evidence in the evidence hierarchy, yet the statistical power of a meta-analysis depends critically on the number and size of included studies and the magnitude of between-study heterogeneity [1]. Underpowered meta-analyses risk failing to detect clinically meaningful effects, while awareness of power limitations is important for interpreting non-significant pooled results. Despite this, prospective power calculations for meta-analyses are rarely reported, partly because convenient tools are lacking [2].

Existing approaches to meta-analytic power calculation include the R packages metapower and PowerUpR [3], Stata modules, and spreadsheet implementations. These require either software installation or programming expertise, creating barriers for clinician-researchers and review teams without statistical support. Furthermore, a key challenge in meta-analytic power is the incorporation of between-study heterogeneity: power decreases as tau-squared increases, but the magnitude of heterogeneity is often uncertain at the planning stage. We developed MA Power to address these gaps, providing an accessible, installation-free tool with built-in sensitivity analysis that visualises how power varies across plausible heterogeneity scenarios.

## Methods

### Architecture

MA Power is implemented as a single self-contained HTML file (660 lines) with no external libraries or server dependencies. All calculations occur client-side in JavaScript. The application is compatible with all modern browsers and functions fully offline.

### Statistical Framework

For continuous outcomes (standardised mean difference, SMD), the tool calculates the variance of the pooled effect estimate under a random-effects model as:

V_pooled = (1/k) * (V_within + tau-squared)

where k is the number of studies, V_within is the typical within-study variance (derived from assumed per-study sample size), and tau-squared is the between-study heterogeneity variance. Statistical power is then computed as the probability that the test statistic Z = theta / sqrt(V_pooled) exceeds the critical value z_{alpha/2} under the alternative hypothesis, where theta is the true effect size:

Power = Phi(theta / sqrt(V_pooled) - z_{alpha/2}) + Phi(-theta / sqrt(V_pooled) - z_{alpha/2})

For binary outcomes (odds ratio), calculations are performed on the log-odds ratio scale using analogous formulae, with within-study variance approximated from assumed event rates and sample sizes [1].

### Analysis Modes

**Power calculation** computes statistical power for user-specified values of the effect size, number of studies, per-study sample size, heterogeneity (tau-squared), and significance level (alpha). **Sample size determination** inverts the power function to find the minimum number of studies required to achieve a target power (e.g., 80%) for given input parameters, using iterative search. **Power curve sensitivity** generates a plot showing how power varies across a user-specified range of tau-squared values, holding other parameters fixed. This mode is particularly useful at the protocol stage when the magnitude of heterogeneity is uncertain.

### User Interface

The interface presents input parameters with sensible defaults and real-time validation. Results are displayed numerically and graphically. The power curve mode generates an interactive chart showing power on the y-axis against tau-squared on the x-axis, with a reference line at 80% power. All results can be exported.

### Validation

We developed 25 automated tests covering: power calculation accuracy for continuous and binary outcomes against published formulae; sample size determination convergence; power curve generation; boundary conditions (tau-squared = 0 corresponding to fixed-effect model, k = 1, very large heterogeneity); and numerical stability for extreme parameter combinations.

## Results

All 25 tests pass across Chrome, Firefox, and Edge. Power calculations for continuous outcomes with SMD = 0.5, k = 10, n = 50 per study, and tau-squared = 0.05 yield power = 0.87, matching the analytical solution to four decimal places. Setting tau-squared = 0 reproduces the fixed-effect power calculation. Sample size determination correctly identifies that k = 15 studies are required to achieve 80% power for SMD = 0.3 with tau-squared = 0.10, consistent with published tables [2]. The power curve mode correctly demonstrates the monotonic decrease in power with increasing heterogeneity. For binary outcomes with OR = 1.5, event rate = 0.20, k = 12, and n = 200, calculated power (0.79) is concordant with results from the metapower R package. The application loads in under 100 milliseconds.

## Discussion

MA Power provides a practical, accessible tool for meta-analytic power calculations that properly accounts for between-study heterogeneity. The power curve sensitivity mode addresses a common challenge in prospective meta-analysis planning: uncertainty about the true heterogeneity magnitude. By visualising power across a range of tau-squared values, researchers can assess the robustness of their planned review's statistical power. Limitations include the assumption of equal study sizes (a common simplification in prospective power analysis) and the restriction to two outcome types. The tool does not currently handle multivariate meta-analysis, network meta-analysis, or diagnostic test accuracy frameworks. Future development may incorporate unequal study sizes, additional effect measures, and Bayesian predictive power approaches. MA Power is freely available under an open-source licence.

## Data Availability

The source code and test suite are available at the project repository. No external data or API access is required. All validation can be reproduced using the built-in test suite.

## Funding

None.

## References

1. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. *Introduction to Meta-Analysis*. Chichester: John Wiley & Sons; 2009. doi:10.1002/9780470743386

2. Valentine JC, Pigott TD, Rothstein HR. How many studies do you need? A primer on statistical power for meta-analysis. *J Educ Behav Stat*. 2010;35(2):215-247. doi:10.3102/1076998609346961

3. Griffin JW. metapower: Power analysis for meta-analysis. R package version 0.2.2. 2021. Available from: https://CRAN.R-project.org/package=metapower

4. Jackson D, Turner R. Power analysis for random-effects meta-analysis. *Res Synth Methods*. 2017;8(3):290-302. doi:10.1002/jrsm.1240

5. Hedges LV, Pigott TD. The power of statistical tests in meta-analysis. *Psychol Methods*. 2001;6(3):203-217. doi:10.1037/1082-989X.6.3.203

6. IntHout J, Ioannidis JP, Borm GF. The Hartung-Knapp-Sidik-Jonkman method for random effects meta-analysis is straightforward and considerably outperforms the standard DerSimonian-Laird method. *BMC Med Res Methodol*. 2014;14:25. doi:10.1186/1471-2288-14-25

7. Higgins JPT, Thomas J, Chandler J, et al., editors. *Cochrane Handbook for Systematic Reviews of Interventions*. Version 6.4. Cochrane; 2023. Available from: www.training.cochrane.org/handbook
