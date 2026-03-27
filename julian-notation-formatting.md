# Julian Garcia -- Notation and Formatting Reference

> Mathematical conventions, equation handling, figure/table patterns, citation integration,
> and venue-specific adaptations. Use alongside `julian-style-guide.md`.

---

## Mathematical Notation

### Variable Naming Conventions

| Category | Convention | Examples |
|----------|-----------|----------|
| Scalar quantities | Lowercase Latin italic | *b* (benefit), *c* (cost), *n* (rounds), *t* (time), *N* (population size), *x* (abundance/trait) |
| Parameters | Lowercase Greek italic | *delta* (continuation prob.), *beta* (selection intensity), *mu* (mutation), *gamma* (cost), *theta* (threshold) |
| Payoffs | *pi* (Greek) | *pi_{AllD,AllD}*, average payoff as pi-bar (overbar) |
| Strategy names | Italic abbreviations | *AllD*, *AllC*, *TFT*, *STFT*, *CTFT* |
| Sets | Calligraphic/script | Script-X for trait sets, script-S for state space, script-A for action space |
| Functions/values | Uppercase Latin | *Q* (Q-values), *V(s)* (state value), *E(C,C)* (expected payoff) |
| Vectors | **Not bolded** -- context and subscripts distinguish | Use subscripts: *x_i*, *x_j* |
| Time derivatives | Dot notation | x-dot for replicator dynamics |
| Averages | Overbar or angle brackets | pi-bar or <f> |

### Game-Theoretic Conventions

- **Payoff matrix format:** Standard matrix with row/column labels (C, D) placed outside brackets:
  ```
       C      D
  C  b-c    -c
  D   b      0
  ```
- **Payoff ordering** for the Prisoner's Dilemma: *T > R > P > S* (temptation, reward, punishment, sucker).
- **Game tuple:** Angle-bracket notation: G = <S, A, T, R, gamma>.
- **Strategy labels:** Use consistent italic abbreviations. For named strategies, define on first use: "Tit-for-Tat (*TFT*)", then use the abbreviation throughout.

### RL/ML Notation (when applicable)

- Standard RL conventions: *pi* for policy (with subscripts), *theta* for parameters, *gamma* for discount factor.
- Metrics in standard form: *F_1*, *TP*, *TN*, *FP*, *FN*.
- Feature vectors may use *phi(s,a)*.

---

## Equation Handling

### Introducing Equations

Equations are introduced with **natural language lead-ins**, not dropped in isolation:

**Good:**
- "...is modeled as a sigmoid function, for example:" [display equation]
- "That means that we can use the standard replicator dynamics" [display equation] "where *x_i* denotes the abundance of strategy *i*..."
- "...be given as:" [display equation]
- "Putting it all together, we obtain the new utility function," [display equation]

**Bad:**
- [Display equation with no verbal introduction]
- "We have:" [display equation] -- too terse

### After the Equation

- **Always define variables** immediately after their first equation appearance using a "where" clause:
  - "where *x_i* is the population share of strategy *i* and *f_i* is its fitness."
- Keep the "where" clause in running prose, not as a separate list (unless there are many variables).

### Referencing Equations

Venue-dependent:
- **PLOS:** "Eq 1", "Eq 3", "Eqs 9, 10" (abbreviated, no parentheses around number)
- **Springer:** "Equation (3)", "See Equation (3)"
- **PNAS:** "equation [1]", "the replicator equation 1"
- **Nature/Sci Reports:** Equations numbered (1), (2), ... but referenced inline as "formula 1"

### Equation Density

- Keep the main text **light on displayed equations**. Use inline math freely.
- Heavy derivations go to the supplement.
- Prefer prose explanations of mathematical relationships when the equation is simple enough.

---

## Figure Conventions

### Referencing Figures in Text

Venue-dependent formatting:
- **PLOS:** "**Fig 1**" (bold, abbreviated, no period)
- **Springer:** "Fig. 1" (abbreviated with period) or "Figure 1" at sentence start
- **PNAS:** "Fig. 1" (abbreviated with period)
- **Sci Reports:** "Fig. 1" (abbreviated with period)

Panel references: "Fig 7A and 7B", "panels C and D of Fig 7", "Fig. 1a", "Figs 5c-d"

### Figure Captions

- **Bold lead sentence** summarizing what the figure shows.
- Followed by **detailed explanatory text** in normal weight, describing panels and parameter values.
- Captions should be **self-contained** enough to partially interpret the figure without the main text.

Example:
> **Fig 5. Simulation results.** Panel A reflects average cooperation levels for a range of benefit-to-cost ratios *b* and continuation probabilities *delta* without the option to leave. Panel B does the same, but with the option to leave...

### Integrating Figures into Prose

- Figures are **woven into analytical discussion**, not just pointed at.
- Describe what the reader should observe:
  - "As is illustrated in Fig 10, the average time it takes..."
  - "A close examination of the figure reveals that..."
  - "Fig 1 depicts an example of an FSA."
- Use parenthetical references for supporting evidence: "(see Fig 6)"

### Figure Types (common in Julian's papers)

- Heatmaps of parameter sweeps
- Simplex / replicator dynamics plots
- Finite state automata diagrams
- Time-series / frequency evolution plots
- Schematic/flow diagrams of model processes
- Multi-panel comparison figures (with/without a mechanism)

---

## Table Conventions

- Referenced as "**Table 1**" (bold in PLOS) or "Table 1" (other venues).
- Captions are descriptive, often multi-sentence.
- Tables are used for: parameter values, comparison of conditions, classification results, strategy definitions.
- Parameter tables can be placed in Supporting Information to avoid cluttering the main text.

---

## Citation Integration

### Format by Venue

| Venue | Format | Example |
|-------|--------|---------|
| PLOS | Numbered, square brackets | [1], [41], [1--19] |
| PNAS | Numbered, parentheses | (1, 2), (6--8), (14, 15) |
| Springer | Numbered, square brackets | [1], [2--4], [6, 10] |
| Sci Reports | Numbered, superscript | ^1, ^{2,3}, ^{14,15} |

### Placing Citations

1. **End of clause** (most common): "this allows for reciprocity and cooperation to evolve together [1--19]."
2. **With "see":** "([41], see also [31, 35, 36])"
3. **With "cf.":** "(cf. [25--29])"
4. **Author-named** (selectively, for specific attributions): "as shown by Tuyls and Nowe [34]", "Perry et al. [10] induced precocious foraging..."

### Citation Density

- **Dense in Introduction and Discussion** (many sentences have 1--3 citations).
- **Sparse in Methods and Results** (citations mainly for methodological precedents).
- Use **citation clusters** for broad claims: [1--19] for general literature on a topic.

### When to Name Authors

- When **attributing a specific idea, model, or finding** to particular researchers.
- When **engaging in detailed comparison** with specific prior studies (especially in Discussion).
- Not for routine background citations.

---

## Venue-Specific Adaptations

### PLOS Computational Biology
- Methods before Results
- Author Summary box (accessible, no equations, vivid language)
- Numbered sections
- Bold figure/table references
- Numbered citations in square brackets
- Supporting Information label: "S1 Text", "S1 Table"

### PNAS
- Methods placement flexible (often after Discussion for short-format)
- Significance Statement may be required
- Numbered citations in parentheses
- Equation numbers in square brackets
- "Fig." abbreviated in text

### Springer (Neural Computing and Applications, etc.)
- Standard IMRaD with numbered sections (up to 3 levels)
- Methods before Results
- Numbered citations in square brackets
- "Fig." abbreviated, "Figure" at sentence start
- Appendix sections with A.1, A.2 numbering

### Nature Portfolio (Scientific Reports)
- Results before Methods
- No explicit "Introduction" heading
- Superscript numbered citations
- "Ref.^X" for specific attributions
- Italic run-in sub-headings for sub-subsections

### arXiv / General Submission
- Flexible structure; follow target journal conventions
- Background section can replace Introduction
- Methods (Analytic methods) can come after Discussion
