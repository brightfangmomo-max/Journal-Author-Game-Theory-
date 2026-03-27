---
name: draft-section
description: Draft a paper section following Julian's writing style guide. Takes section name and notes as input, produces LaTeX output following all conventions.
argument-hint: "[section name] [optional: brief notes or key points]"
allowed-tools: ["Read", "Grep", "Glob", "Write"]
---

# Draft Paper Section

Draft a section of a research paper following Julian Garcia's writing style conventions.

**Input:** `$ARGUMENTS` -- section name (e.g., "introduction", "model", "results", "discussion") and optional notes about key points to cover.

---

## Steps

1. **Read the style guides:**
   - `julian-style-guide.md` -- voice, tone, hedging
   - `julian-paper-structure.md` -- section-specific template
   - `julian-rhetoric-playbook.md` -- argumentation patterns
   - `julian-notation-formatting.md` -- equations, figures, citations
   - `.claude/rules/paper-writing-protocol.md` -- consolidated rules

2. **Read existing paper content** (if any) in `Papers/` to understand:
   - Target venue (determines citation style, formalism level, etc.)
   - Notation already in use
   - Narrative arc established in earlier sections

3. **Draft the section** following these conventions:
   - First person plural "we"
   - Active voice for contributions, passive for background
   - Contrastive framing ("While..., ..." / "However,")
   - Strong topic sentences in every paragraph
   - Equations introduced with verbal lead-ins + "where" definitions
   - No bullet lists in prose
   - Asymmetric hedging (direct on results, cautious on interpretations)

4. **Section-specific guidance:**

   **Abstract:** 150-220 words. Arc: Context -> Gap -> Method -> Result -> Implication. No generic opening.

   **Introduction:** Funnel structure. Open with specific mechanism. Gap via contrastive framing. Flowing literature review. Contribution statement. Optional roadmap.

   **Model/Methods:** Conceptual clarity over formalism. Verbal before math. Natural lead-ins to equations. Proofs to supplement.

   **Results:** Organized by comparison axis. Descriptive subsection headings. Figures woven into prose.

   **Discussion:** Zoom out. Strong interpretive claims. Brief limitations. End on memorable conceptual note. No separate Conclusion unless venue requires.

5. **Output as LaTeX** in `Papers/` directory. Include:
   - Proper `\section{}` or `\subsection{}` headings
   - `\cite{}` keys matching `Bibliography.bib`
   - `\label{}` for cross-references
   - Equation environments with numbering

6. **Self-check** against the style guide checklist from `julian-deeper-suggestions.md`:
   - [ ] Every paragraph has a clear topic sentence
   - [ ] "We" and active voice for own contributions
   - [ ] Contrastive structure present
   - [ ] Results direct, interpretations hedged
   - [ ] Equations with lead-ins and "where" definitions
   - [ ] Figures woven into prose
   - [ ] No unnecessary formalism
