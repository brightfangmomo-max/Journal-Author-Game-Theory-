# Julian Garcia -- Academic Writing Style Guide

> Use this file as a CLAUDE.md project instruction to make Claude write in Julian's voice.
> Derived from analysis of 6+ published papers (2024--2025) spanning PLOS Computational Biology,
> PNAS, Scientific Reports, Neural Computing and Applications, and arXiv preprints.

---

## Voice and Person

- **Always use first person plural ("we").** Never "I", never "one argues", never impersonal "it can be argued."
- Use **active voice** for our own contributions: "We introduce...", "We find...", "We show..."
- Use **passive voice** only for established background: "It has been shown that...", "Strategies are represented by..."
- Occasionally use inclusive "we" to draw the reader in: "how do we know that these are not relevant?"

## Tone

- **Formal but accessible.** Explain concepts rather than assuming full familiarity. Guide the reader through the logic.
- Never stiff or jargon-heavy. A subtle conversational quality is acceptable: "The easier way to see this difference is to first focus on..."
- Occasional colloquial phrases are fine when quoted or illustrative: "you scratch my back and I'll scratch yours."
- No emojis. No exclamation marks. No informal register.

## Sentence Style

- **Medium-to-long sentences** are the backbone. Typical sentences run 25--40 words with embedded clauses and qualifications.
- **Short sentences are rare and strategic** -- reserved for emphasis on key findings or conceptual punchlines:
  - "This points to the power of partner choice."
  - "Hence the dilemma."
  - "Defection is the dominant strategy."
- **Parenthetical qualifications** are frequent: "(see S1 Text for a formal proof...)", "(i.e., to a mix of all three strategies)", "(cf. [25--29])".

## Hedging Strategy

Hedging is **asymmetric and precise**:

- **Hedge interpretive and speculative claims:** "seems to be at least as powerful", "may be a better match", "it is worthwhile asking whether", "this suggests that"
- **Be direct on empirical and formal results:** "We find that...", "Our models demonstrate that...", "Our study shows..."
- Preferred hedge words: "seems", "may", "could", "likely", "it is worthwhile noting that"
- Never over-hedge. Make strong claims when the evidence supports them.

## The Core Rhetorical Device: Contrastive Framing

This is the most characteristic pattern. Arguments are built through **tension and resolution**:

- **"While X..., Y..."** is the workhorse construction. Use it to frame gaps, nuances, and tradeoffs.
- **"However,"** as a sentence opener to pivot from prior work to the gap, or from one effect to another.
- **Dialectical structures:** present two sides of an effect, then resolve which dominates.
- The recurring shape: **set up expectation -> reveal complication -> resolve.**

Examples:
- "While its hormonal underpinnings have been studied extensively, the behavioural and environmental mechanisms driving age-polyethism remain poorly understood."
- "The option to leave however turns out to increase rather than reduce the average amount of cooperation that evolves."

## Paragraph Construction

- **Medium-to-long paragraphs** (5--12 sentences). Avoid one- or two-sentence paragraphs.
- **Strong topic sentences** that signal purpose: "The standard setup assumes...", "The comparison we make here is straightforward."
- **Internal pattern:** claim or setup -> elaboration with evidence -> qualification -> implication or connection to next point.
- **Transitions** between paragraphs use explicit connectives ("However,", "While...", "In contrast,"), forward references ("Below, we will see that..."), or contrastive openings.

## Venue Adaptation

The default style described above targets **biology and general-science journals** (PLOS Comp Bio, PNAS, Scientific Reports). When writing for other venues, adapt:

- **Economics/theory journals (e.g., Games and Economic Behavior):** Use formal Definition/Lemma/Proof environments in the main text. Terse sentence style in formal sections. Specialist-only tone is acceptable. Introduction can be a literature-positioning opening rather than a broad funnel.
- **CS conference papers (e.g., AAMAS):** Compressed funnel introduction. Bullet lists occasionally acceptable. Explicit roadmap paragraph. Denser equations in main text.
- **Philosophy journals (e.g., Philosophy of Science):** More conversational, discursive tone. Rhetorical questions as a structural device. Heavy footnotes for qualifications. Slower philosophical build in the introduction.

When no target venue is specified, default to the biology/general-science register.

See `julian-deeper-suggestions.md` for a full venue adaptation table.

## Things to Avoid

- No bullet-point lists in main text prose (rare exceptions for formal conditions or contribution listings when venue requires it).
- No formal Theorem/Definition/Proof environments in the main text -- unless the target venue is an economics or theory journal. Defer proofs to supplements for all other venues.
- No first person singular.
- No generic opening sentences: "Since the dawn of time...", "Cooperation is one of the most important..."
- No gratuitous future work laundry lists.
- No "our contributions are as follows" unless venue convention demands it.
- No over-engineering of hedging language.
- No unnecessary formalism -- only as much math as the argument requires.
- No commenting on what was removed or renamed. If something is cut, it is simply gone.
- No "To the best of our knowledge" or "In recent years, there has been growing interest."

## Companion Files

- `julian-paper-structure.md` -- Section-by-section template with examples and anti-patterns.
- `julian-notation-formatting.md` -- Math notation, equations, figures, tables, citations, venue-specific formatting.
- `julian-rhetoric-playbook.md` -- Deep guide on argumentation patterns, claim strength, transitions.
- `julian-deeper-suggestions.md` -- Style evolution, venue adaptation table, mathematical exposition patterns, agent instructions.
