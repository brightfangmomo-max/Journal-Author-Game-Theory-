# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Academic research project modeling the impact of AI on academic publishing systems using game theory and agent-based simulations. The paper ("Big Science and Peer Review") shows that if AI asymmetrically increases submission volume faster than review capacity, creating tipping points and quality collapse.

**Author:** Yuhui Fang

## Architecture

- **`scr/`** — Python simulation scripts that generate PDF figures
- **`doc/tex/`** — LaTeX paper manuscript, bibliography, and output figures
- **`AI_paper_rewrite_guide.md`** — Detailed guide for extending the model with AI adoption parameter

### Python Scripts (`scr/`)

| Script | Purpose | Output |
|--------|---------|--------|
| `ABM_authors.py` | 4-strategy agent-based model (OG/AS/OB/NS) | — |
| `ABM_batch_matching.py` | Local batch-matching ABM with global social learning; compares ODE vs stochastic dynamics | `Plot1-4*.pdf` |
| `Boundaries_regimes.py` | Phase diagram across K_rev vs K_store | `regime_map_final.pdf` |
| `Hysteresis_Loop_and_Quality_Collapse.py` | Evolutionary dynamics curves showing convergence regions | `polynomial_graph_1-4.pdf` |
| `regimes_distribution.py` | Parameter space regime classification | `regime_map_final.pdf` |
| `ABM_journal.py` | Empty placeholder | — |

### Key Model Parameters

- **N** = population size, **x** = proportion of honest authors
- **K_rev** = review capacity, **K** (K_store) = publication slots
- **r** = publication reward, **c** = submission cost
- **λ** = screening accuracy (bad papers), **ε** = false rejection rate (good papers)
- **η** = review bottleneck = min(1, K_rev/V), **ρ** = publication bottleneck = min(1, K/M)
- Spam profitability: **Π_bad = r·ρ·π₀ − c**

### Regime Types

- **GH** (Green): Global Honesty — **GC** (Red): Global Corruption — **BS** (Yellow): Bistability — **SC** (Blue): Stable Coexistence — **NS** (Gray): No Submission

## Commands

### Run simulations (generate figures)

```bash
python scr/ABM_batch_matching.py
python scr/Boundaries_regimes.py
python scr/Hysteresis_Loop_and_Quality_Collapse.py
python scr/regimes_distribution.py
```

### Compile LaTeX paper

```bash
cd doc/tex && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

Or with latexmk: `latexmk -pdf doc/tex/main.tex`

### Python dependencies

```bash
pip install numpy matplotlib pandas
```

## Conventions

- **One sentence per line in LaTeX.** In `doc/tex/main.tex`, each sentence must start on its own line. This makes git diffs readable. Do not join sentences onto one line; do not break a single sentence across lines. This rule applies to prose paragraphs only — not to equations, TikZ code, tables, or `\caption{}` blocks.
- Scripts use a custom `soft_min(a, b, k)` function for smooth differentiable approximation of `min()` in dynamics equations
- Generated figures are PDF (vector format) and placed in `doc/tex/` for LaTeX inclusion
- The paper uses `natbib` for bibliography management
- Writing style: short sentences, define symbols once, minimize jargon (see `AI_paper_rewrite_guide.md` Section 4 for full guidelines)
