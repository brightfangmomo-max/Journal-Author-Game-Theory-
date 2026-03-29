# Session Log: PNAS-Style Restructure

**Date:** 2026-03-28
**Goal:** Restructure the paper from a specialist game-theory article to a PNAS-style general-audience narrative.

## Key Decisions (resolved via user feedback)

1. **Equations:** 4 in main text (Pi_bad, replicator, a* threshold, gamma > delta asymmetry). Four channel functional forms described verbally; formal versions in M&M.
2. **Fig 4 (equilibrium vs a):** Moved to SI as Fig S2. Main text keeps 5 figures.
3. **Propositions 1-4:** Moved to SI (Appendix A). Main text states results as inline prose claims.
4. **Word count target:** ~5,500-6,000 (not aggressive 4,500). Final: ~5,100 text + 500 captions.
5. **Mechanism diagram:** Removed entirely. Prose in Section 2.1 carries the mechanism story.
6. **Terminology:**
   - "tipping point" → "critical transition"
   - "tipping threshold" → "collapse threshold"
   - "hysteresis" → "asymmetric recovery"
   - "hysteresis gap" → "recovery gap"
   - "spam payoff" → removed; use Pi_bad or "net payoff from weak submissions"
   - "bottleneck" → already absent

## What Changed

### main.tex (major rewrite)
- Added Significance Statement (~120 words)
- Rewrote Abstract for general audience
- Shortened Introduction (cut roadmap, condensed EGT justification)
- Created 5 Results subsections (prose model summary, regime boundaries, critical transitions, silent erosion, interventions)
- Expanded Discussion (~1,150 words, absorbed Institutional Responses)
- Created Materials and Methods section
- 14 equations → 4; 6 figures → 5

### supplement.tex (moderate)
- Removed mechanism diagram (moved to prose in main)
- Added Fig S2 (equilibrium vs a, from main)
- Updated captions for general-audience terms
- Updated cross-references to new main-text figure numbers

## Open Items
- SI figures (S1 phase portrait, S2 equilibrium vs a, S3 channels) still have old plot-level labels (OG/AS, BS→GC). Need script regeneration pass.
- Supplement formal proofs still use "spam payoff" — acceptable for specialist material.
- Proofread and domain review agents were launched but results not yet incorporated.

## Compile Status
- main.tex: 14 pages, clean compile, no warnings
- supplement.tex: 22 pages, clean compile, no warnings
