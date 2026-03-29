# Session Log: Review Issue Resolution

**Date:** 2026-03-29
**Goal:** Walk through all issues found by domain-review and proofreading agents, resolve each with user input.

## Context
- Paper was restructured to PNAS-style in previous session (2026-03-28)
- Domain reviewer found 9 issues (1 major, 8 minor)
- Proofreader found 15 issues (1 high — already fixed, 5 medium, 9 low)
- Line numbers added to PDF for review discussion

## All Issues Resolved

### Issue: Binary strategy reduction (PDF lines 88-90)
- **Decision:** Reframe as modelling assumption justified by continuous-strategy ABM simulations (SI Appendix B). Student will run the ABM. Circular reference broken.

### Issue: "cheapest to verify" (PDF line 41)
- **Decision:** Restructured contrast + new Table S6 in supplement (stage-by-stage AI impact vs verification intensity). New bib entries: Si2024, Lu2024, Dahl2024, HalluCitations2026.

### Issue: λ vs π₀ conflation (PDF line 101)
- **Decision:** Changed to "false-positive rate λ"

### Issue: Moher2009 for CONSORT (PDF line 264)
- **Decision:** Added Schulz2010 for CONSORT, kept Moher for PRISMA

### Issue: Moher2009 for ClinicalTrials.gov (PDF line 295)
- **Decision:** Replaced with DeAngelis2004

### Issue: Gross2019 loose cite (PDF line 55)
- **Decision:** Replaced with Bianchi2018

### Issue: Prop 1 Case III qualifier
- **Decision:** Added qualifier + red student note [YF: verify sufficient condition across full parameter grid]

### Issue: Filter condition
- **Decision:** Added λ + ε < 1 to Materials and Methods

### Issue: OG/AS orphaned in M&M
- **Decision:** Dropped; use "selective"/"universal" throughout

### Issue: Supplement authors
- **Decision:** Synced to three authors

### Issue: Title
- **Decision:** Changed to "More papers, worse science? Why AI-driven publishing needs peer review reform"

### Low-priority style fixes (all applied)
- Non-breaking spaces before citations, Figure→Fig., nonlinear→non-linear, Set A caption clarity, collapsed blank lines, abstract expanded with prediction sentence (~160 words)

## Remaining Issues (in priority order)

### Medium
1. "cheapest to verify" phrasing (PDF line 41) — conflates production and verification
2. λ vs π₀ conflation (PDF line 101) — same phrase for distinct quantities
3. Moher2009 cited for CONSORT (PDF ~line 324) — actually the PRISMA paper
4. Moher2009 cited for ClinicalTrials.gov mandate (PDF ~line 349) — should be De Angelis 2004
5. Proposition 1 Case III needs qualifier — result is numerical, not fully analytical
6. Discriminatory filter condition (λ + ε < 1) not stated in main text
7. Gross2019 citation loose for peer review congestion (PDF line 55)
8. Discussion CONSORT/Registered Reports loosely connected to model parameter λ

### Low
9. Figure vs Fig. (PNAS style)
10. "Supplementary Material" vs "SI Appendix" (PNAS style)
11. OG/AS abbreviations orphaned in M&M
12. Missing non-breaking spaces before citations
13. Equation labels defined but never referenced
14. Bib key casing inconsistent
15. "nonlinear" vs "non-linear"
16. Set A parameter override in hysteresis caption unclear
17. Abstract slightly below PNAS word count
18. Supplement author list mismatch (1 vs 3 authors)
19. No random seed in fig5_tipping_timeseries.py

## Key Context
- User wants to discuss each issue via the feedback interface, with PDF line numbers
- lineno package added temporarily for review (will remove before submission)
