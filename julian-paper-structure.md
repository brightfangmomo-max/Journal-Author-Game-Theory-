# Julian Garcia -- Paper Structure Template

> Section-by-section patterns extracted from published papers (2024--2025).
> Use alongside `julian-style-guide.md` for full writing instructions.

---

## Abstract

**Length:** 150--220 words, single paragraph.

**Arc:** Context -> Gap -> Method -> Key Result -> Implication

**Rules:**
- Do NOT open with a generic platitude ("Cooperation is important to society..."). Jump into the specific mechanism or problem.
- The first sentence should name the specific phenomenon or mechanism the paper addresses.
- Em-dash parenthetical definitions are welcome for accessibility: "Age-polyethism -- the age-based allocation of tasks in social insect colonies -- is a key feature..."
- State quantitative results when available, but foreground the conceptual finding.
- The final sentence should convey a broader implication, not just restate the result.

**Example arc (from "Repeated games with partner choice"):**
1. Context: "Repetition is a classic mechanism for the evolution of cooperation."
2. Gap: Who individuals interact with "can however also be under their control."
3. Method: "If we change the standard model so that it allows for individuals to terminate the interaction..."
4. Result: "We find that the net effect of introducing the option to leave on cooperation is positive."
5. Implication: "This phenotypic assortment... may be a better match with the long-lasting cooperation we observe in humans."

---

## Introduction

**Structure:** Funnel from broad to specific.

**Typical flow across paragraphs:**

1. **Open with the specific mechanism or phenomenon** -- not a broad platitude. Start where the action is.
   - Good: "In the prisoner's dilemma, repetition can stabilize cooperation."
   - Bad: "Cooperation is fundamental to human societies."

2. **Identify the standard assumption or existing approach.** Describe how the field currently handles the problem.
   - "The standard setup in models for the co-evolution of reciprocity and cooperation assumes that randomly matched individuals are tied to their partner."

3. **Introduce the deviation or gap.** Use contrastive framing ("While... remains poorly understood"; "However, little progress has been made on..."). Do NOT use formulaic "To the best of our knowledge, no study has..."

4. **Flowing literature review.** Group references thematically, not as a list. Weave citations into the narrative.
   - "While most of these papers do not combine a full game-theoretical analysis with studying the evolutionary dynamics, this literature does contain findings that are relevant."

5. **State your contribution.** Options depending on venue:
   - **Narrative style (preferred):** Weave contributions into the text with forward references to sections: "In Section X, we will see that..."
   - **Enumerated style (when venue requires):** "(1) We provide... (2) We show..." -- use inline numbering, not bullet points.
   - **Declarative style:** "In this paper, we introduce best response guided agents (BRG), which..."

6. **Optional roadmap paragraph.** Brief, one paragraph: "The rest of this paper is organized as follows. In Sect. 2, we review..."

**Anti-patterns:**
- Do not open with a sentence about the importance of cooperation in general.
- Do not use "To the best of our knowledge" or "In recent years, there has been growing interest."
- Do not present the literature review as a disconnected list of papers.

---

## Model / Methods

**Placement:** Before Results (PLOS, Springer) or after Discussion (Science/Nature/Sci Reports style). Follow venue convention.

**Principles:**
- **Conceptual clarity over formalism.** The main text builds intuition through verbal argument. Formal proofs go to the supplement.
- Introduce equations with **natural language lead-ins** that flow into the math:
  - "...is modeled as a sigmoid function, for example:" [equation]
  - "That means that we can use the standard replicator dynamics" [equation] "where..." [define terms]
- Define all variables immediately after their first equation appearance using a "where" clause.
- Use **algorithm blocks** (formal pseudocode with line numbers) when describing computational procedures.
- Payoff matrices use standard format with row/column labels placed outside brackets.

**Equation referencing:**
- "Eq 1", "Eq (3)", or "equation [1]" depending on venue.
- Introduce before the display: "...as shown in Eq 3:" followed by the equation.

---

## Results

**Structure:** Organized by **comparison axis or experimental domain**, not as a monolithic block. Each subsection addresses a distinct question.

**Subsection headings should state findings, not just topics:**
- Good: "Collective accuracy does not increase monotonically with accuracy motives of the debaters"
- Good: "When punishing with leaving is better than punishing with defecting"
- Bad: "Accuracy analysis"
- Bad: "Punishment comparison"

**Figure integration:**
- Figures are **tightly woven into analytical prose**, not just pointed at.
- Describe what the reader should observe: "A close examination of the figure reveals that BRG agents do not consistently commence with cooperation."
- Use phrases like: "As is illustrated in Fig 10, the average time it takes..."

**Qualifying numerical results:**
- State the number, then qualify: "We should obviously not attach deeper meaning to this exact number, because it is the result of a somewhat arbitrary choice."
- Use "As expected,..." when results confirm predictions.

---

## Discussion

**The Discussion IS the Conclusion.** There is typically no separate Conclusion section. (Exception: applied ML papers where "Conclusions and future work" is a combined heading.)

**Structure:**

1. **Open by zooming out.** Restate the contribution in broader context, not by repeating the abstract.
   - "The two mechanisms that received the lion share of the attention in the literature on the evolution of cooperation are kin selection and repetition."

2. **Make strong interpretive claims** with appropriate hedging:
   - "Partner choice therefore seems to be at least as powerful a mechanism for the evolution of cooperation as reciprocity is."

3. **Engage with limitations** honestly but briefly. One paragraph is usually sufficient.
   - "There are many ways in which our model is stylized."

4. **Forward-looking statements are substantive, not a laundry list.** Connect future directions to specific open questions or empirical puzzles.
   - Good: "This phenotypic assortment... may be a better match with the long-lasting cooperation we observe in humans, who tend to exert some influence over who they cooperate with."
   - Bad: "Future work could extend this to larger populations, different game structures, and heterogeneous agents."

5. **End on a memorable note.** The final sentence should be a broader implication or a conceptual insight, not a mechanical summary.

**Anti-patterns:**
- Do not begin the Discussion by restating the abstract.
- Do not end with "In conclusion, we have shown that..." followed by a bullet list of results.
- Do not include a lengthy, disconnected list of future work directions.

---

## Supporting Information / Appendix

- Formal proofs, theorems, and lemmas go here, not in the main text.
- Reference from the main text: "(see Theorems 1 and 2 in S1 Text for a formal proof...)"
- Parameter tables can be placed here rather than cluttering the main text.
- Extended simulation details and sensitivity analyses belong here.

---

## Author Summary (PLOS-specific)

- Written in a more accessible, less technical register than the abstract.
- Avoids equations entirely.
- Uses concrete, vivid language: "safe tasks inside the nest", "dangerous foraging tasks."
- Ends with real-world relevance.
