# Session Log: Style Rewrite and Introduction Restructure

**Date:** 2026-03-28
**Goal:** Rewrite main text prose to Julian's voice, then restructure introduction per author feedback.

## Key Context

- Paper: "Flooding the filter" — game-theoretic model of AI, submission pressure, and quality collapse in academic publishing
- Authors: Yuhui Fang, Toby Handfield, Julian Garcia (Toby and Julian added this session)
- Main file: `doc/tex/main.tex`, supplement: `doc/tex/supplement.tex`

## Completed

### Phase 1: Style rewrite (committed as eeafa7b)
- Applied five systematic transformations across all prose sections:
  - Deflated jargon (elasticity→sensitivity, Pigouvian→corrective levy, etc.)
  - Added contrastive framing ("While X..., Y...") throughout
  - Fixed hedging asymmetry (direct on model results, hedged on interpretations)
  - Active voice for own contributions
  - Strengthened topic sentences
- British spelling enforced throughout
- Section 2 rewritten from disconnected \paragraph blocks to flowing narrative
- Roadmap compressed from 11 to 6 lines
- Proofreader agent run; fixed towardss typo, subject-verb agreement, redundant phrasing
- Generated latexdiff PDF at `doc/tex/main_style_diff.pdf`

### Phase 2: Introduction restructure and author additions (in progress, not yet committed)
- Added Toby Handfield and Julian Garcia to author list
- Restructured intro: evidence first, then broader context (social dynamics, institutions, culture around technology), then the question
- New citations: Walker (2026), Zhong et al. (2026), Mokyr (2002), Hao et al. (2026), March (1991)
- New paragraph motivating evolutionary dynamics as social/group phenomenon
- Softened "concrete policy agenda" → "suggest institutional reform should prioritise verification"
- Moved Figure 1 (mechanism diagram) to supplement
- Relaxed bib hook: references.bib now uses normal approval instead of hard block

## Decisions
- User wants intro to warm up to the publishing question rather than jumping straight in
- User wants evolutionary dynamics motivated as social dynamics, not just game theory
- User finds "concrete policy agenda" too strong — softer framing preferred
- User prefers bib edits go through normal approval, not hard block
- Coordination protocol: always re-read files before editing (user edits manually between turns)

### Phase 3: Merge Sections 1–3 into unified Introduction (not yet committed)
- Merged Stylized Facts and Related Literature into Introduction
- Essential lit review citations woven into argument paragraphs
- "What we contribute" paragraph moved into intro before results summary
- Equation 1 (asymmetry assumption) moved to AI Extension section (Channel 4)
- Removed standalone Sections 2 and 3; paper now goes Intro → Baseline Model
- Model-parameter mapping sentences removed from intro (belong in Model section)
- Updated roadmap and all cross-references (sec:stylized_facts, sec:literature)
- Paper reduced from 25 to 23 pages
- Added Ginsparg dissemination/certification distinction to bottlenecks paragraph

## Open Questions
- Supplement compile not yet verified after mechanism figure addition
- Should detailed empirical evidence (Kovanis hours, Kobak vocabulary analysis) be added to supplement?
