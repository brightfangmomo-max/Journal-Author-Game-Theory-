---
name: review-figure
description: |
  Review figures for publication quality across composition, colour,
  accessibility, typography, data representation, and technical specs.
  Use when: after creating figures, before submission, or when user says
  "review figure", "check figure quality", or "review-figure".
allowed-tools: ["Read", "Glob", "Grep", "Agent"]
---

# /review-figure -- Figure Quality Review

Review one or more figures for publication quality using the figure-critic agent.

## Usage

```
/review-figure [path]       # Review a specific figure
/review-figure all           # Review all figures in Figures/
```

## Workflow

1. **Identify targets:**
   - If a specific path is given, review that figure.
   - If `all` is given, glob `Figures/**/*.{pdf,png,svg}` and review each.
   - For each figure, also look for the generating script (`scripts/python/fig_*.py` or `scripts/julia/fig_*.jl`) and any LaTeX caption.

2. **Launch figure-critic agent** for each target (or batch if reviewing all).

3. **Present results:**
   - Show the summary score table.
   - List critical and major issues.
   - If score < 80, flag as blocking.

## Output

```
## Figure Review Summary

| Figure | Score | Rating | Issues |
|--------|-------|--------|--------|
| name.pdf | 85/100 | GOOD | 1 major, 2 minor |

### Critical/Major Issues
[List with file references and suggested fixes]
```
