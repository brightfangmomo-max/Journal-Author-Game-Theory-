# Plan: Figure Style Overhaul — Remove Clutter, Add Seaborn Paper Style

**Status:** DRAFT
**Date:** 2026-03-28

## Context

The user finds the figures visually cluttered: large star markers, intrusive arrows, and cryptic regime-name text floating inside heatmaps. The two cleanest figures (fig4, fig5) use algorithmic label placement and data-driven annotations. The four problematic figures (fig3, fig6, fig7, fig8) rely on hardcoded positions, oversized markers, and floating text. The goal is to bring all six figures to a consistent, publication-quality style using seaborn's paper context.

## What Changes

### Step 0: Create `scr/fig_style.py` (shared style module)

All six scripts currently copy-paste the same 13-line rcParams block. Replace with a single import.

Contents:
- **`apply_style()`** — calls `sns.set_context("paper", font_scale=1.0)` + `sns.set_style("ticks", {"font.family": "serif"})`, then overlays project-specific rcParams (`text.usetex`, `pdf.fonttype: 42`, `savefig.dpi: 300`, linewidths)
- **Palette constants** — `REGIME_COLORS`, `REGIME_NAMES`, `REGIME_CMAP` (ListedColormap for heatmaps)
- **`regime_legend(present_codes)`** — returns `Patch` handles mapping colours to full regime names (e.g., "GH (Global Honesty)"). Replaces all floating text labels in heatmaps.
- **`mark_point(ax, x, y, label, offset)`** — small open circle (`'o'`, markersize=5, white fill, black edge) with offset text label, no arrow. Replaces star markers.

### Step 1: `fig3_ai_phase_diagram.py` — major rework

| Remove | Replace with |
|--------|-------------|
| rcParams block | `apply_style()` |
| Black star markers (`marker='*'`, ms=10) | `mark_point(ax, 300, 400)` — small open circle |
| Arrow annotations to "Set A" labels | Text offset in `mark_point()`, no arrow |
| 6 floating regime text labels (hardcoded transAxes) | Shared discrete legend below panels via `regime_legend()` |
| — | Add `ax.contour()` at half-integer levels on the regime grid for crisp boundaries |

### Step 2: `fig7_hysteresis_widening.py` — major rework

| Remove | Replace with |
|--------|-------------|
| rcParams block | `apply_style()` |
| 4 floating text labels at hardcoded data coords | Discrete regime legend via `regime_legend()` |
| — | Optional contour lines for boundary crispness |

Existing boundary curves (red solid collapse, blue dashed BS) stay — they're informative.

### Step 3: `fig8_interventions.py` — major rework

| Remove | Replace with |
|--------|-------------|
| rcParams block | `apply_style()` |
| Star markers (ms=12) | `mark_point()` — small open circle |
| Arrow annotations to "Set A" | Text offset in `mark_point()`, no arrow |
| Thick horizontal intervention arrows | Thin dashed line + small triangle endpoint marker |
| Floating regime text labels | Shared discrete legend below panels |
| — | Contour lines on regime boundaries |

### Step 4: `fig6_hysteresis_loop.py` — moderate rework

| Remove | Replace with |
|--------|-------------|
| rcParams block | `apply_style()` |
| Massive vertical arrows (spanning 88% of y-axis) | Shortened thin arrows (`lw=0.8`, `mutation_scale=8`) from upper-branch value to lower-branch value at fold points |

Regime shading strips at top with computed midpoint labels stay — already clean.

### Step 5: `fig4_equilibrium_vs_a.py` — style refresh only

Replace rcParams block with `apply_style()`. No other changes.

### Step 6: `fig5_tipping_timeseries.py` — style refresh only

Replace rcParams block with `apply_style()`. No other changes.

## Files to Modify

| File | Change Level |
|------|-------------|
| `scr/fig_style.py` | **New** — shared style module |
| `scr/fig3_ai_phase_diagram.py` | Major — stars, arrows, labels, boundaries |
| `scr/fig7_hysteresis_widening.py` | Major — floating labels, legend |
| `scr/fig8_interventions.py` | Major — stars, arrows, labels, intervention path |
| `scr/fig6_hysteresis_loop.py` | Moderate — replace oversized arrows |
| `scr/fig4_equilibrium_vs_a.py` | Minor — style import only |
| `scr/fig5_tipping_timeseries.py` | Minor — style import only |
| `CLAUDE.md` | Add `fig_style.py` to architecture table |

## Sequencing

1. Create `scr/fig_style.py` (dependency for all others)
2. Modify all 6 scripts (independent — can be parallelised)
3. Run all scripts, inspect output PDFs
4. Compile paper
5. Update `CLAUDE.md`

## Verification

1. `python -c "import seaborn"` — confirm dependency available
2. Run each script: `python scr/fig3_ai_phase_diagram.py` (etc.)
3. Visual check of each PDF:
   - No star markers remain
   - No oversized arrows
   - No floating regime text inside heatmaps — replaced by legend
   - Regime boundaries visually crisp (contour lines)
   - Set A marker is a clean small circle
   - Font sizes match julian-figure-standards (axis 11pt, ticks 10pt, panel labels 12pt bold)
4. Compile: `cd doc/tex && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
5. No broken figure references
