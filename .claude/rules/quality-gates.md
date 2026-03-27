---
paths:
  - "doc/tex/**/*.tex"
  - "scr/**/*.py"
---

# Quality Gates & Scoring Rubrics

## Thresholds

- **80/100 = Commit** -- good enough to save
- **90/100 = PR** -- ready for submission
- **95/100 = Excellence** -- aspirational

## LaTeX Papers (.tex)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | XeLaTeX compilation failure | -100 |
| Critical | Undefined citation | -15 |
| Critical | Overfull hbox > 10pt | -10 |
| Critical | Typo in equation | -10 |
| Major | Notation inconsistency | -5 |
| Major | Missing variable definition after equation | -5 |
| Major | Style guide violation (voice, hedging, structure) | -3 |
| Minor | Overfull hbox < 10pt | -1 |
| Minor | Long lines (>100 chars) | -1 (EXCEPT math formulas) |

## Python Scripts (.py)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Syntax/runtime errors | -100 |
| Critical | Missing random seed (stochastic code) | -20 |
| Critical | Hardcoded absolute paths | -20 |
| Major | Missing figure generation | -10 |
| Major | No type hints on functions | -5 |
| Major | PEP 8 violations | -3 |
| Minor | Missing docstrings | -1 |

## Julia Scripts (.jl)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Errors on execution | -100 |
| Critical | Missing random seed (stochastic code) | -20 |
| Critical | Type instability in hot loops | -15 |
| Major | Missing Project.toml | -10 |
| Major | Unnecessary allocations in loops | -5 |
| Minor | Missing docstrings | -1 |

## Figures

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Non-colourblind-safe palette (rainbow/jet) | -20 |
| Critical | Raster-only output (no PDF vector) | -15 |
| Major | Font size below minimum (< 9pt) | -10 |
| Major | Missing axis labels or units | -10 |
| Major | Colour-only encoding (no shape/line differentiation) | -10 |
| Major | No uncertainty shown (missing error bars/bands) | -5 |
| Major | 3D effects on 2D data | -5 |
| Minor | Caption missing bold lead sentence | -3 |
| Minor | Inconsistent colour mapping across panels | -3 |
| Minor | Default matplotlib/Plots.jl styling | -2 |
| Minor | JPEG format used | -2 |

## Enforcement

- **Score < 80:** Block commit. List blocking issues.
- **Score < 90:** Allow commit, warn. List recommendations.
- User can override with justification.

## Quality Reports

Generated **only at merge time**. Use `templates/quality-report.md` for format.
Save to `quality_reports/merges/YYYY-MM-DD_[branch-name].md`.

## Tolerance Thresholds (Research)

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| Simulation means | 1e-3 | MC variability |
| Equilibrium values | 1e-6 | Numerical precision |
| Coverage rates | +/- 0.01 | MC with B reps |
