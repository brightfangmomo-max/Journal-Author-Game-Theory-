# Session Log: Integrate AI into Core Model + Figure Improvement Plan

**Date:** 2026-03-28
**Goal:** Eliminate the "Baseline Model" / "AI Extension" two-section structure by merging into a single unified "The Model" section (Option A from plan). Then develop a figure improvement plan.

## Key Context

- Paper: "Flooding the filter" — game-theoretic model of AI, submission pressure, and quality collapse
- The introduction already frames AI as central, but the model presentation contradicted this by treating AI as a bolt-on extension
- User requested terminology changes: "bottleneck" → "capacity constraint", "spam" → "indiscriminate submission" / "universal submission"

## Completed

1. **Merged Sections 2 and 3** into a single "The Model" section
   - Introduced AI parameter `a` and four channels immediately after "Players and strategies"
   - Rewrote "Two bottlenecks" → "Two capacity constraints" with AI-parameterised equations from the start
   - Rewrote "Screening errors and the spam payoff" → "Screening errors and the payoff from indiscriminate submission"
   - Kept dynamics and four long-run outcomes, adapted for `a`-parameterised versions
   - Moved boundary analysis, special cases, and testable predictions from old Section 3
   - Removed `\section{The AI Extension}` and `\label{sec:ai_extension}` entirely
   - Updated all cross-references (roadmap paragraph, Section 4 references)
2. **Terminology cleanup throughout entire main.tex**
   - "bottleneck" → "capacity constraint" (zero occurrences of "bottleneck" remain)
   - "spam" / "spammer" / "spamming" → "indiscriminate submission" / "universal submission" / "flooding" (zero occurrences of "spam" remain)
3. **Compiled successfully** — 23 pages, zero errors, zero undefined references
4. **Figure improvement plan** — GAN-style critique of all 9 figures, with concrete proposals

## Figure Plan Summary

- Promote fig7 (tipping timeseries) from supplement to main paper
- Demote fig2 (phase portrait) to supplement
- Fix hysteresis loop bug (panel b `a_rec` logic)
- Fix TikZ "spam profitability" text
- Reduce fig5 to 2 panels, fig6 to 1 panel
- Create shared palette module, add rcParams to all scripts
- All scripts need Paul Tol colours, proper figsize, no suptitles

## Figure Execution Progress

- [x] Fig 1 (TikZ channels): already clean from restructuring
- [x] Fig 2 (phase portrait): demoted to supplement, script rebuilt (Paul Tol, rcParams, terminology)
- [x] Fig 3 (phase diagram): rebuilt, renamed fig4→fig3, Paul Tol, proper figsize
- [x] Fig 4 (equilibrium vs a): reduced to 2 panels, renamed fig5→fig4
- [x] Fig 5 (tipping timeseries): PROMOTED from supplement to main, renamed fig7→fig5
- [x] Fig 6 (hysteresis loop): FIXED panel b bug, rebuilt, renamed
- [x] Fig 7 (regime map N,a): simplified to 1 panel, renamed fig6→fig7
- [x] Fig 8 (interventions): decluttered, renamed fig10→fig8
- [ ] Global: shared palette module (deferred — each script has Paul Tol colours inline)

## Open Questions

- Supplement still contains "spam" and "baseline model" terminology (not yet addressed)
