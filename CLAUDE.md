# CLAUDE.md

## Project Overview

Academic research project modeling the impact of AI on academic publishing systems using game theory and agent-based simulations. The paper ("Big Science and Peer Review") shows that if AI asymmetrically increases submission volume faster than review capacity, creating tipping points and quality collapse.

**Author:** Yuhui Fang

## Architecture

- **`scr/`** — Python simulation scripts that generate PDF figures
- **`doc/tex/`** — LaTeX paper manuscript, bibliography, and output figures
- **`julian-*.md`** — Writing style guides for academic papers

### Python Scripts (`scr/`)

| Script | Purpose | Output |
|--------|---------|--------|
| `ABM_authors.py` | 4-strategy agent-based model (OG/AS/OB/NS) | — |
| `ABM_batch_matching.py` | Local batch-matching ABM with global social learning; compares ODE vs stochastic dynamics | `Plot1-4*.pdf` |
| `ABM_journal.py` | Empty placeholder | — |
| `Boundaries_regimes.py` | Phase diagram across K_rev vs K_store | `regime_map_final.pdf` |
| `Hysteresis_Loop_and_Quality_Collapse.py` | Evolutionary dynamics curves showing convergence regions | `polynomial_graph_1-4.pdf` |
| `regimes_distribution.py` | Parameter space regime classification | `regime_map_final.pdf` |
| `data_io.py` | Data I/O utilities | — |
| `fig_hysteresis_loop.py` | Hysteresis loop figure | `fig_hysteresis_loop.pdf` |
| `fig2_phase_portrait.py` | Phase portrait | `fig2_phase_portrait.pdf` |
| `fig4_ai_phase_diagram.py` | AI phase diagram | `fig4_ai_phase_diagram.pdf` |
| `fig5_equilibrium_vs_a.py` | Equilibrium vs AI parameter | `fig5_equilibrium_vs_a.pdf` |
| `fig6_hysteresis_widening.py` | Hysteresis widening | `fig6_hysteresis_widening.pdf` |
| `fig7_tipping_timeseries.py` | Tipping point time series | `fig7_tipping_timeseries.pdf` |
| `fig8_heatmap_outcomes.py` | Outcome heatmap | `fig8_heatmap_outcomes.pdf` |
| `fig9_abm_validation.py` | ABM validation | `fig9_abm_validation.pdf` |
| `fig10_interventions.py` | Intervention analysis | `fig10_interventions.pdf` |

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
- Writing style: short sentences, define symbols once, minimize jargon (see `julian-style-guide.md` for full guidelines)


---

<!-- Added by claude-code academic workflow setup -->

## Core Principles

- **Plan first** -- enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** -- compile and confirm output at the end of every task
- **Style guide compliance** -- follow Julian's writing conventions (see `paper-writing-protocol` rule and `julian-*.md` files)
- **Quality gates** -- nothing ships below 80/100
- **[LEARN] tags** -- when corrected, save `[LEARN:category] wrong -> right` to MEMORY.md

---

## Folder Structure

```
simple_journals/
├── CLAUDE.md                    # This file
├── .claude/                     # Rules, skills, agents, hooks
├── scr/                         # Python simulation scripts
├── doc/tex/                     # LaTeX paper, bibliography, and generated figures
│   ├── main.tex                 # Paper manuscript
│   └── references.bib           # Bibliography
├── julian-*.md                  # Writing style guides
├── quality_reports/             # Plans, session logs, reviews
│   ├── plans/
│   ├── session_logs/
│   ├── specs/
│   └── merges/
├── templates/                   # Templates for session logs, reports, etc.
├── explorations/                # Research sandbox
└── master_supporting_docs/      # Reference papers and materials
```

---

## Quality Thresholds

| Score | Gate | Meaning |
|-------|------|---------|
| 80 | Commit | Good enough to save |
| 90 | PR | Ready for submission |
| 95 | Excellence | Aspirational |

---

## Skills Quick Reference

| Command | What It Does |
|---------|-------------|
| `/compile-paper [file]` | 3-pass XeLaTeX + bibtex for papers |
| `/proofread [file]` | Grammar/typo/consistency review |
| `/review-paper [file]` | Full manuscript review (referee-style) |
| `/review-python [file]` | Python code quality review |
| `/review-julia [file]` | Julia code quality review |
| `/review-figure [path]` | Figure publication quality review |
| `/draft-section [section]` | Draft paper section using style guide |
| `/run-simulation [script]` | Run Monte Carlo / computational experiments |
| `/data-analysis [dataset]` | End-to-end Python analysis |
| `/validate-bib` | Cross-reference citations |
| `/devils-advocate [file]` | Challenge paper argument/structure |
| `/commit [msg]` | Stage, commit, PR, merge |
| `/lit-review [topic]` | Literature search + synthesis |
| `/research-ideation [topic]` | Research questions + strategies |
| `/interview-me [topic]` | Interactive research interview |
| `/learn [skill-name]` | Extract discovery into persistent skill |
| `/context-status` | Show session health + context usage |
| `/deep-audit` | Repository-wide consistency audit |
| `/check-upstream` | Check upstream repo for new features to adopt |

---

## Writing Style Reference

Julian's writing conventions are documented in these files (kept in repo root):
- `julian-style-guide.md` -- Voice, tone, sentence style, hedging
- `julian-paper-structure.md` -- Section-by-section template
- `julian-notation-formatting.md` -- Math, figures, tables, citations
- `julian-rhetoric-playbook.md` -- Argumentation patterns
- `julian-deeper-suggestions.md` -- Venue adaptation, advanced patterns
- `julian-figure-standards.md` -- Composition, colour, typography, technical specs

These are consolidated into the rule `.claude/rules/paper-writing-protocol.md` which is automatically loaded when editing `doc/tex/**/*.tex`.

---

## Current Project State

| Paper | File | Status | Target Venue |
|-------|------|--------|-------------|
| | | | |
