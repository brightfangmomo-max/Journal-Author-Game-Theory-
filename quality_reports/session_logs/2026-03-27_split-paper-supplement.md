# Session Log: Split Paper into Main Text + Supplementary Material

**Date:** 2026-03-27
**Goal:** Split the ~20,900-word single-document paper into a concise main text (~12,000 words) and a supplementary material document, following the approved plan.

## Key Context

- Paper: "Flooding the filter: a game-theoretic model of AI, submission pressure, and quality collapse" by Yuhui Fang
- Plan approved at: `quality_reports/plans/` (split plan)
- Target: main text 12,000-13,000 words; secondary results and formal derivations in supplement

## Progress

### Completed

1. **Created `doc/tex/supplement.tex`** with matching preamble, S-prefixed numbering (Figure S1, Table S1, etc.), and shared bibliography.

2. **Moved content to supplement:**
   - Appendix A: Proofs of Propositions 1-4 (formerly main.tex appendix, lines 1787-2122)
   - Appendix B: ABM Tipping Dynamics (formerly Section "Agent-Based Modeling", subsections Why Simulate, Model Design, Results)
   - Appendix C: Robustness and Stochastic Validation (formerly ABM subsections on heatmap robustness and stochastic ABM)
   - Appendix D: Welfare Analysis and Normative Policy Design (full section including welfare function, externalities, regime ranking, Corollaries W1-W4, Box S1)
   - Appendix E: Extended Empirical Predictions (Predictions 3-6: proxies, data sources, identification strategy, falsification)
   - Appendix F: Model Extensions (heterogeneity, multi-journal cascades, endogenous rewards)

3. **Updated main.tex:**
   - Introduction roadmap updated to reference supplement
   - ABM section replaced with ~150-word condensed summary citing Appendices B-C
   - Welfare section replaced with ~200-word condensed summary citing Appendix D
   - Predictions 3-6 replaced with brief forward reference to Appendix E
   - Discussion: kept "Scope" and "Institutional mismatch" paragraphs; moved three extension paragraphs to Appendix F
   - Proofs appendix removed entirely (now Appendix A of supplement)
   - All cross-references updated (no dangling refs)

4. **Verified:**
   - Both documents compile cleanly (3-pass pdflatex + bibtex)
   - Zero undefined references in both logs
   - Main text: ~11,543 words (29 pages) — slightly below 12k target
   - Supplement: ~6,496 words (17 pages)

## Decisions

- Kept "Scope and simplifying assumptions" and "Institutional mismatch" paragraphs in Discussion (core narrative, not extensions)
- Used explicit text references ("Appendix X of the Supplementary Material") rather than cross-document \ref commands
- Supplement internal references to main text use descriptive text ("the main text", "the Analysis section of the main text")

### Second pass: Tables and Boxes to Supplement

5. **Moved all tables and boxes out of main.tex:**
   - Table 1 (AI channels) → Appendix G of supplement
   - Table 2 (regime classification) → embedded as inline definitions in prose
   - Table 3 (scenario matrix) → Appendix G of supplement
   - Table 4 (calibration) → Appendix G of supplement
   - Table 5 (institutions) → Appendix G of supplement
   - Box 1 (Baseline Model) → Box S2 in Appendix G
   - Box 2 (AI Changes) → Box S3 in Appendix G
   - Box 3 (Policy Menu) → Box S4 in Appendix G
   - Removed tcolorbox package from main.tex preamble (no longer needed)

6. **Updated all cross-references** — zero dangling refs in both docs.

7. **Final state:**
   - Main text: ~11,160 words, 25 pages, zero tables, zero boxes
   - Supplement: ~7,038 words, 21 pages
   - Both compile cleanly (3-pass pdflatex + bibtex), zero undefined references

## Open Questions

- Main text word count ~11,160 vs target 12,000-13,000. Slightly under but within range.
- Figure numbering in main text now skips 7-9 (those moved to supplement as S1-S3). LaTeX auto-renumbers, so what was Fig 10 is now Fig 7.
