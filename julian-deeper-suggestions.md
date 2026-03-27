# Julian Garcia -- Deeper Suggestions for a Writing Agent

> Extended notes on style evolution, venue adaptation, mathematical exposition,
> and advanced patterns. Supplements the core style guide files.

---

## Style Evolution: What Has Changed Over Time

Comparing recent papers (2024--2025) with older ones (2019--2023) reveals that some
patterns are **core to Julian's voice** while others are **venue adaptations**.

### Core (stable across all papers and years):
- First person plural "we" throughout
- Active voice for own contributions
- Conceptual clarity as a priority
- Building arguments through contrast and tension
- Strong topic sentences in paragraphs
- Asymmetric hedging (direct on results, cautious on interpretations)

### Evolved (recent papers differ from older ones):
- **Descriptive section headings** that state findings are a RECENT development (2024--2025). Older papers use generic topical headings ("Preliminaries", "Results"). The agent should use descriptive headings by default but fall back to generic ones for math-heavy papers in economics journals.
- **Contrastive "While.../However..."** as the dominant rhetorical device is most prominent in recent work. Older papers use a wider toolkit including rhetorical questions and enumeration. The contrastive engine should be the default but not the only tool.
- **No bullet lists** is the strong recent preference. One older conference paper (AAMAS 2019) used them, but all recent journal papers avoid them. The agent should avoid bullet lists in main text prose.
- **Roadmap paragraphs** were more common in older papers. Recent papers use them selectively. Include one only when the paper has complex or non-standard structure.

### Venue-dependent (changes with the target journal, not with time):

| Pattern | Biology/Comp Bio journals | Economics/Theory journals | CS conference papers | Philosophy journals |
|---------|--------------------------|--------------------------|---------------------|-------------------|
| Theorem/proof in main text | No -- defer to supplement | Yes -- Definition, Lemma, Proof environments | Rarely | No |
| Tone | Formal but accessible | Formal and specialist | Compressed, technical | Conversational, discursive |
| Introduction | Funnel from broad | Sequel-style, literature-positioning | Compressed funnel | Slow philosophical build |
| Bullet lists | Never | Never | Occasionally | Never |
| Footnotes | Rare | Occasional | Rare | Heavy |
| Equation density | Light in main text | Heavy in main text | Moderate | Light |
| Rhetorical questions | Rare | Rare | Rare | Frequent |

**Rule for the agent:** When the user specifies a target venue, adapt these features accordingly. When no venue is specified, default to the biology/computational biology style (formal but accessible, light formalism, no theorems in main text).

---

## Advanced Patterns for Mathematical Exposition

### The Prose-to-Math Bridge

Julian's papers never drop equations in isolation. The pattern for introducing math:

1. **State the concept in plain language** first.
2. **Motivate why math is needed** ("To make this precise...", "We make the tradeoff precise by using...").
3. **Display the equation** with a verbal lead-in ending in a colon or comma.
4. **Define variables immediately** with a "where" clause.
5. **Give the intuition** for what the equation means in words ("This means that the payoff increases when...").

Example flow:
> We assume debaters face a tradeoff between discovering truth and maintaining stable beliefs.
> We make the tradeoff between these motivations precise by using the following utility function:
>
> u(v, d) = w * v - d
>
> where v is the number of true beliefs, d is the number of belief changes, and w is the
> weight placed on truth relative to the cost of revising beliefs. A higher w means the
> debater cares more about accuracy than cognitive stability.

### The "Putting It All Together" Move

After building up model components across several paragraphs, use a synthesis moment:
- "Putting it all together, we obtain the new utility function,"
- "That means that we can use the standard replicator dynamics"

This signals to the reader that the model setup is complete and the analysis begins.

### When to Use Display vs. Inline Math

- **Display:** Equations that will be referenced later, central model definitions, key results.
- **Inline:** Parameter definitions, simple relationships, conditions (e.g., "when delta > 0.5").
- **Rule of thumb:** If you won't reference it by number, keep it inline.

### Deferring Proofs

In biology and general-science venues:
- State the result as a prose claim in the main text.
- Reference the formal version: "(see Theorem 4 in S1 Text for a formal proof)"
- Never apologize for deferring -- it is the expected structure.

In economics venues:
- Include Definition/Lemma/Proof environments directly in the main text.
- Use standard formatting: Definition N, Lemma N, Proof.
- The style becomes more terse in formal sections: shorter sentences, less hedging.

---

## How to Handle Multi-Author Dynamics

Julian appears on papers in different roles, and the writing adapts slightly:

### As first or corresponding author (e.g., Garcia & Traulsen PNAS):
- Stronger authorial voice in framing the contribution.
- More likely to make bold interpretive claims.
- The "Here, we argue for..." framing.

### As contributing author on a student-led paper (e.g., Perera et al., Khajehnejad et al.):
- More methodical, step-by-step exposition.
- Explicit roadmap paragraphs.
- More "As expected, we observe that..." validation language.
- Contributions stated more explicitly (numbered lists).

### As contributing author with senior collaborators (e.g., van Veelen papers):
- Adapts to the senior author's venue conventions.
- Willing to use formal theorem environments when the venue demands it.
- Prose sections still show Julian's contrastive style.

**Rule for the agent:** Ask the user about the collaboration context. Default to Julian's natural style (biology/general science). Adapt formality upward for economics venues or when the user indicates formal proofs are needed.

---

## Common Conceptual Moves in Julian's Domain

### Framing a game-theoretic model:
1. Name the social dilemma (prisoner's dilemma, public goods game, snowdrift game).
2. State what makes cooperation costly and defection tempting.
3. Identify the mechanism that could promote cooperation (repetition, reputation, partner choice, punishment).
4. Introduce the specific twist or deviation from the standard setup.

### The "standard setup, then deviation" move:
This appears across multiple papers and is a signature introduction strategy:
- "The standard setup assumes X. In this paper, we change Y."
- "The standard way to study repeated games is to assume Z. If we change the standard model so that..."

### Connecting model results to empirical reality:
- "This is consistent with the empirical phenomenon reported in [10]."
- "This phenotypic assortment may be a better match with the long-lasting cooperation we observe in humans."
- Always connect results to observable behaviour -- never leave the model floating in abstraction.

### The efficiency paradox:
A recurring theme across papers: showing that the "obvious" best strategy or highest-efficiency outcome is NOT what evolves or is NOT in equilibrium.
- "age-polyethism does not necessarily optimize immediate colony efficiency"
- "Collective accuracy does not increase monotonically with accuracy motives of the debaters"
- This is a signature conceptual contribution pattern.

---

## Practical Agent Instructions

When helping Julian write, the agent should:

1. **Ask about the target venue first.** This determines Methods placement, citation style, formalism level, heading style, and tone.
2. **Ask about the contribution type.** Is this a new model? An extension of prior work? A perspective/review? This determines introduction structure.
3. **Start with the conceptual argument, not the math.** Write the prose skeleton first, then insert equations where needed.
4. **Write the abstract last** (or at least revise it last), as it must accurately reflect the actual contribution.
5. **Default to the biology/general-science register** unless told otherwise.
6. **Never add formalism that isn't strictly needed.** If a result can be stated in prose with a simple equation, do not add a Theorem environment.
7. **Always close with a substantive conceptual point**, not a summary of results.

---

## Checklist Before Finalizing Any Section

- [ ] Does every paragraph have a clear topic sentence?
- [ ] Are "we" and active voice used for our own contributions?
- [ ] Is the contrastive structure present? (At least one "While.../However..." per major paragraph)
- [ ] Are results stated directly, interpretations hedged?
- [ ] Are equations introduced with verbal lead-ins and followed by "where" definitions?
- [ ] Are figures woven into analytical prose, not just pointed at?
- [ ] Does the Discussion zoom out rather than repeat the abstract?
- [ ] Does the final sentence convey broader meaning?
- [ ] Are section headings descriptive (for recent-style papers)?
- [ ] Is there any unnecessary formalism that could be cut or moved to an appendix?
