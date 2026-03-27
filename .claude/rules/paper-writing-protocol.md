---
paths:
  - "doc/tex/**/*.tex"
---

# Paper Writing Protocol

**Consolidated writing rules from Julian Garcia's style guides.**
Full reference files: `julian-style-guide.md`, `julian-paper-structure.md`, `julian-notation-formatting.md`, `julian-rhetoric-playbook.md`, `julian-deeper-suggestions.md`.

## Voice and Person

- **Always use first person plural ("we").** Never "I", never "one argues."
- **Active voice** for own contributions: "We introduce...", "We find...", "We show..."
- **Passive voice** only for established background: "It has been shown that..."

## Tone

- **Formal but accessible.** Explain concepts; guide the reader.
- No emojis. No exclamation marks. No informal register.
- No bullet lists in main text prose.

## Core Rhetorical Device: Contrastive Framing

- **"While X..., Y..."** is the workhorse. Use it for gaps, nuances, tradeoffs.
- **"However,"** as a pivot from prior work to the gap.
- **Dialectical structures:** present two sides, then resolve.
- Shape: set up expectation -> reveal complication -> resolve.

## Hedging (Asymmetric)

- **Direct on results:** "We find that...", "Our models demonstrate that..."
- **Hedge interpretations:** "seems to be", "may be", "suggests that"
- Never over-hedge. Be strong when evidence supports it.

## Formatting

- **One sentence per line** in LaTeX source. Never join multiple sentences on a single line. This makes git diffs clean and reviewable.
- **British spelling everywhere.** Use "behaviour", "modelling", "organisation", "analyse", "colour", "favour", "generalise", etc. Never American variants.

## Sentence and Paragraph Style

- Medium-to-long sentences (25-40 words) as backbone.
- Short sentences reserved for emphasis on key findings.
- Medium-to-long paragraphs (5-12 sentences).
- Strong topic sentences that signal purpose.
- "This [noun]..." backward links between paragraphs.

## Section Structure

### Abstract (150-220 words)
Arc: Context -> Gap -> Method -> Key Result -> Implication.
Do NOT open with a generic platitude.

### Introduction (Funnel)
1. Open with specific mechanism/phenomenon (not broad platitude)
2. Identify standard assumption or approach
3. Introduce gap using contrastive framing
4. Flowing literature review (thematic, not a list)
5. State contribution (narrative preferred, enumerated if venue requires)
6. Optional roadmap paragraph

### Model/Methods
- Conceptual clarity over formalism
- Introduce equations with natural language lead-ins
- Define all variables with "where" clauses after equations
- Formal proofs go to supplement (unless economics/theory venue)

### Results
- Organized by comparison axis, not monolithic
- Subsection headings state findings, not just topics
- Figures woven into analytical prose

### Discussion (IS the Conclusion)
- Open by zooming out
- Strong interpretive claims with appropriate hedging
- Brief limitations (one paragraph)
- End on a memorable conceptual note

## Equation Handling

- Introduce with verbal lead-in: "...is modeled as:" [equation]
- Define variables immediately with "where" clause
- Heavy derivations go to supplement
- Reference format depends on venue (see notation guide)

## Figure Integration

- Woven into analytical prose, not just pointed at
- Describe what the reader should observe
- Caption format: bold lead sentence + detailed explanation
- Full figure standards: `julian-figure-standards.md`. Use `/review-figure` to check quality.

## Citation Style

- Venue-dependent (check `julian-notation-formatting.md`)
- Default to numbered square brackets [1]
- Dense in Introduction and Discussion, sparse in Methods/Results
- Name authors only for specific attributions

## Venue Adaptation

When no target venue specified, default to biology/general-science register.
See `julian-deeper-suggestions.md` for the full venue adaptation table.

| Feature | Bio/Comp Bio | Economics | CS Conference | Philosophy |
|---------|-------------|-----------|---------------|------------|
| Proofs in text | No | Yes | Rarely | No |
| Tone | Accessible | Specialist | Compressed | Discursive |
| Bullet lists | Never | Never | Occasionally | Never |
| Footnotes | Rare | Occasional | Rare | Heavy |

## Things to Avoid

- No first person singular
- No generic openings ("Since the dawn of time...")
- No "To the best of our knowledge"
- No gratuitous future work laundry lists
- No "our contributions are as follows" (unless venue demands it)
- No over-engineering of hedging
- No unnecessary formalism
- No commenting on what was removed or renamed
