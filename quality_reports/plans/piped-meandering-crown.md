# Plan: PNAS-Style Restructuring — General Audience, Single Clear Message

**Status:** DRAFT
**Date:** 2026-03-28

## Context

The paper is currently structured as a specialist game-theory article: 14 numbered equations in main text, a 197-line Model section that dominates the narrative, and a 44-line Discussion that is too thin. For PNAS, the ratio should be inverted: prose-driven narrative with formalism in SI/Materials and Methods, and a Discussion that carries interpretive weight. The mechanism diagram — the most accessible visual — is hidden in the supplement.

**The single message:**
> AI makes it dramatically easier to produce manuscripts but not to verify them. This asymmetry can silently erode peer review until the system tips past a point of no return — and recovery requires far more effort than prevention.

Every structural decision below serves this message.

## New Section Structure

```
Significance Statement  (~120 words, NEW)
Abstract               (~150 words, REWRITTEN for general audience)
Introduction           (~60 lines, SHORTENED — cut roadmap, condense EGT justification)
Results
  1. AI as an Asymmetric Shock        (prose model summary + Fig 1 mechanism diagram)
  2. AI Shifts Regime Boundaries      (Fig 2 = current Fig 3, phase diagram)
  3. Tipping and Hysteresis           (Fig 3 = current Fig 6, hysteresis loop)
  4. Silent Erosion of Stability      (Fig 4 = current Fig 5, tipping timeseries)
  5. Intervention Must Target Verification  (Fig 5 = current Fig 8, interventions)
Discussion             (~100-120 lines, EXPANDED — absorbs Institutional Responses)
Materials and Methods  (~80-100 lines, NEW — absorbs formal model setup)
```

**Target:** ~4,500 words main text (current: ~9,300).

## What Changes

### 1. Add Significance Statement (NEW)

~120 words, plain language, no symbols, no citations. Conveys the tipping + hysteresis + verification message for a reader who reads nothing else.

### 2. Rewrite Abstract

Remove specialist language ("game-theoretic framework", "screening"). Focus on: asymmetry → tipping → hysteresis → slot expansion paradox → policy. Written so a biologist or physicist grasps the contribution.

### 3. Shorten Introduction (from ~76 to ~60 lines)

| Cut | Why |
|-----|-----|
| Roadmap paragraph (lines 123–128) | PNAS papers don't have roadmaps |
| EGT justification paragraph (lines 83–86) | Condense to 1 sentence; audience doesn't need selling on the method |
| Four-channel preview (lines 88–101) | This now appears in Results with the mechanism diagram |
| "Three results" preview (lines 104–111) | Shorten to 2–3 sentences |

### 4. Replace Model Section with Prose-Driven "Results" Subsection

The current 197-line Model section (12 equations) becomes a ~60-70 line prose narrative called "AI as an Asymmetric Shock."

**Keep 3 equations in main text:**
1. **Spam payoff** (current eq:pibad): `Π_bad = r·ρ̄·π₀ − c(a)` — the central object
2. **Replicator dynamics** (current eq:replicator): `ẋ = −x(1−x)(1−α)Π_bad` — tells the whole story
3. **Tipping threshold** (current closed-form a*): the punchline formula

**Move 11 equations to Materials and Methods / SI:**
All four channel functional forms (V, c, λ, K_rev), the asymmetry condition, η and ρ̄ definitions, pass rates π₀/π₁, peer-accepted pool M, boundary Pi_bad, quality Q(x). Describe each verbally in main text, e.g.: "When submissions exceed review capacity, scrutiny per paper falls."

### 5. Move Mechanism Diagram from SI to Main Text as Figure 1

The TikZ flow diagram (supplement lines 51–170, current Figure S1) showing AI → 4 channels → Π_bad → tipping/hysteresis is the most accessible visual. A biologist or physicist can grasp the entire argument from this single figure. It becomes **Figure 1**.

### 6. Move Current Fig 4 (equilibrium vs a) to SI

Its content (x* trajectory under two parameter sets) overlaps with Fig 6 (hysteresis loop), which tells the same story more dramatically. This keeps main text at 6 figures (within PNAS limits).

### 7. Figure Renumbering

| New # | Current # | Content |
|-------|-----------|---------|
| Fig 1 | Fig S1 (supplement) | Mechanism diagram (TikZ) — MOVES to main |
| Fig 2 | Fig 3 | AI phase diagram (K_rev, K space) |
| Fig 3 | Fig 6 | Hysteresis loop |
| Fig 4 | Fig 5 | Tipping timeseries |
| Fig 5 | Fig 7 | Hysteresis widening (N, a plane) |
| Fig 6 | Fig 8 | Interventions |
| Fig S1 | Fig S2 (current) | Phase portrait |
| Fig S2 | Fig 4 (current) | Equilibrium vs a — MOVES to SI |

### 8. Rewrite All Figure Captions

Current captions use parameter-set labels and Greek symbols. Rewrite so a reader can understand each figure without reading any equation. Use descriptive language: "a typical journal prone to tipping" instead of "Set A (K_rev=300, K=400)". Move parameter values to parenthetical at end of caption.

### 9. Expand Discussion (from ~44 to ~100-120 lines)

Absorb current Institutional Responses section. New structure:

1. **Implications for institutional design** (~40 lines) — the five principles, rewritten as narrative prose (not a numbered list). This is the policy crescendo.
2. **Opening zoom-out** (~15 lines) — the production-verification asymmetry as a recurring historical pattern, not unique to AI.
3. **Testable predictions** (~25 lines) — merge and expand the current predictions. Name specific data sources (arXiv submission records, reviewer acceptance rates, retraction databases). Ground in the November 2022 natural experiment.
4. **Model boundaries** (~15 lines) — reframe limitations as scope conditions, not apologies. Binary strategies, single journal, no heterogeneity.
5. **Closing** (~10 lines) — memorable conceptual note about institutions designed for an era when producing a credible manuscript was difficult.

### 10. Create Materials and Methods Section (NEW, ~80-100 lines)

Goes at end of paper (PNAS format). Absorbs formal setup from current Model section:
- Population of N authors, binary quality, two strategies, replicator dynamics — define all symbols
- Four AI channel functional forms (V, c, λ, K_rev) — state compactly
- Two capacity constraints (η, ρ̄)
- Pass rates and peer-accepted pool
- Parameter calibration (Set A, Set B values; point to SI table)
- Brief note on ABM validation (in SI)

### 11. Reorganise Supplement

New content to add:
- New **Appendix A: Model Details and Functional Forms** — absorbs moved equations and derivations
- **Figure S2** (current main text Fig 4) moves to SI

Existing appendices B–G renumber to C–H.

## Files to Modify

| File | Change Level |
|------|-------------|
| `doc/tex/main.tex` | **Major** — restructure sections, migrate equations, new Significance Statement and M&M |
| `doc/tex/supplement.tex` | **Moderate** — donate Fig S1 to main, absorb Fig 4 and model details, renumber |
| `scr/fig4_equilibrium_vs_a.py` | **Minor** — update output path to reflect SI placement |

## Sequencing

1. Restructure `main.tex`: add Significance Statement, rewrite abstract, shorten intro
2. Create Materials and Methods section by extracting formal content from Model
3. Rewrite Model section as prose-driven Results subsection
4. Move mechanism diagram from supplement to main text (Fig 1)
5. Move Fig 4 to SI, renumber all figures
6. Merge Institutional Responses into expanded Discussion
7. Rewrite all figure captions for general audience
8. Update supplement (new Appendix A, figure renumbering)
9. Update all cross-references
10. Compile and verify

## Verification

1. Compile: `cd doc/tex && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
2. No broken figure or equation references
3. No broken citations
4. Word count check: ~4,500 words main text (excluding abstract, M&M, references)
5. Equation count: exactly 3 in main text
6. Figure count: 6 in main text, mechanism diagram is Figure 1
7. Proofread for general-audience accessibility: no unexplained jargon, no assumed specialist knowledge
