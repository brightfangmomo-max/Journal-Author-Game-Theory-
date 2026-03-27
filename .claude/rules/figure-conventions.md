---
paths:
  - "doc/tex/**/*.pdf"
  - "scr/fig_*"
---

# Figure Conventions (Quick Reference)

**Full standards:** `julian-figure-standards.md` (repo root).
**Review command:** `/review-figure [path or 'all']`.

## Essentials

- **Palette:** Paul Tol (primary), ColorBrewer (secondary). Never rainbow/jet.
- **Format:** PDF vector (primary), PNG 300 DPI (backup). Never JPEG.
- **Font sizes:** 10-12pt labels, 9-11pt ticks, LaTeX-rendered math.
- **Accessibility:** no colour-only encoding; combine colour with shape/line style.
- **Captions:** bold lead sentence, self-contained, panel descriptions.
- **Data-ink:** maximise. No chartjunk, no 3D effects, no unnecessary gridlines.
- **Uncertainty:** always show error bars, confidence bands, or distributions.

## Python Figures

Apply the publication rcParams block from `julian-figure-standards.md` at the top of every figure script. Use `pathlib.Path` for output paths. Save to `doc/tex/` as PDF.

## Quality Gate

Figures are scored by the figure-critic agent across 6 dimensions (see `julian-figure-standards.md`). Score >= 80 to commit.
