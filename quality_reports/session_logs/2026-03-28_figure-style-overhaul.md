# Session Log: Figure Style Overhaul

**Date:** 2026-03-28
**Goal:** Remove visual clutter from figures and add consistent seaborn paper style across all six publication figures (fig3–fig8).

## Context

- Figures had oversized star markers, intrusive arrows, and floating regime-name text inside heatmaps
- Fig4 and fig5 were already clean; fig3, fig6, fig7, fig8 needed major/moderate rework
- Plan approved to create shared style module and standardise all six scripts

## Key Decisions

- Created `scr/fig_style.py` as shared style module (seaborn paper context, regime palette, `mark_point()`, `regime_legend()`)
- Replaced star markers with small open circles (white fill, black edge, ms=5)
- Replaced floating regime text labels with discrete colour legend below panels
- Added `ax.contour()` at half-integer levels for crisp regime boundaries on heatmaps
- Fig6 hysteresis arrows shortened to span tipping-branch-to-stable-branch only
- Fig8 thick intervention arrows replaced with thin dashed lines + triangle endpoint markers

## Status

- All 6 scripts modified and running successfully
- All PDFs generated and visually verified
- Paper compiles (21 pages, no broken references)
- CLAUDE.md updated with `fig_style.py` entry
- **COMPLETE** — ready for user review

## Open Questions

- None
