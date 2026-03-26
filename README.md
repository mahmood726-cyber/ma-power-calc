# MA Power

Meta-analysis power and sample size calculator for planning systematic reviews.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Overview

MA Power computes statistical power for planned random-effects meta-analyses and determines the number of studies needed to achieve a target power level. Based on the methods of Valentine et al. (2010) and Jackson and Turner (2017), it accounts for between-study heterogeneity (tau-squared derived from the expected I-squared) and supports both binary (OR/RR) and continuous (SMD/MD) outcomes. Interactive power curves visualize how power changes across different numbers of studies and heterogeneity levels.

## Features

- Power calculation for random-effects meta-analyses given k, N, effect size, and I-squared
- Sample size determination: minimum number of studies (k) needed for a target power
- Support for binary outcomes (odds ratio, risk ratio) and continuous outcomes (SMD, mean difference)
- Within-study variance formulae appropriate to each effect measure
- Between-study variance (tau-squared) derived from expected I-squared and average within-study variance
- Sensitivity table showing required k across multiple I-squared levels (0%, 25%, 50%, 75%)
- Interactive power curve plots at four heterogeneity levels
- Tabulated power at key study counts (k = 5, 10, 15, 20, 30, 50)
- Colour-coded power result (green >= 80%, amber 50-79%, red < 50%)
- Auto-generated methods text for manuscripts
- Equivalent R code generation
- Dark mode and print-optimized layout

## Quick Start

1. Download `ma-power.html`
2. Open in any modern browser
3. No installation, no dependencies, works offline

## Built-in Examples

No built-in datasets. Enter parameters directly: number of studies (k), average sample size per study (N), expected effect size, expected I-squared (%), and alpha level.

## Methods

- Random-effects power: Power = Phi(|delta| / SE_pooled - z_{alpha/2})
- Pooled SE under random effects: SE = sqrt(1 / sum(1 / (v_i + tau-squared)))
- Binary outcomes: v_i approximated from log-OR/log-RR variance formulae
- Continuous outcomes: v_i = 4/N + d-squared/(2N) (Hedges approximation)
- Tau-squared from I-squared: tau-squared = I-squared * v_bar / (1 - I-squared)
- References: Valentine et al. (2010), Jackson and Turner (2017), Hedges and Pigott (2004)

## Screenshots

> Screenshots can be added by opening the tool and using browser screenshot.

## Validation

- 25/25 Selenium tests pass
- Cross-validated against power calculations from Valentine et al. (2010) reference examples

## Export

- Methods text (clipboard, manuscript-ready)
- R code equivalent
- Print-optimized report

## Citation

If you use this tool, please cite:

> Ahmad M. MA Power: A browser-based power and sample size calculator for meta-analysis. 2026. Available at: https://github.com/mahmood726-cyber/ma-power

## Author

**Mahmood Ahmad**
Royal Free Hospital, London, United Kingdom
ORCID: [0009-0003-7781-4478](https://orcid.org/0009-0003-7781-4478)

## License

MIT
