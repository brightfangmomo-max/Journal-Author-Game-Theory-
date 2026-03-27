---
name: research-ideation
description: Generate structured research questions, testable hypotheses, and methodological strategies from a topic or mechanism
argument-hint: "[topic, phenomenon, or mechanism description]"
allowed-tools: ["Read", "Grep", "Glob", "Write"]
---

# Research Ideation

Generate structured research questions, testable hypotheses, and methodological strategies from a topic, phenomenon, or mechanism.

**Input:** `$ARGUMENTS` -- a topic (e.g., "partner choice in repeated games"), a phenomenon (e.g., "why does cooperation persist despite temptation to defect?"), or a model description.

---

## Steps

1. **Understand the input.** Read `$ARGUMENTS` and any referenced files. Check `master_supporting_docs/` for related papers.

2. **Generate 3-5 research questions** ordered from descriptive to mechanistic:
   - **Descriptive:** What are the patterns? (e.g., "What equilibria arise under partner choice?")
   - **Comparative:** How do mechanisms compare? (e.g., "Is partner choice more powerful than reciprocity?")
   - **Mechanistic:** Why does the effect exist? (e.g., "Through what channel does leaving promote cooperation?")
   - **Robustness:** How sensitive are results? (e.g., "Does the result hold with heterogeneous populations?")
   - **Applied:** What are the implications? (e.g., "Can these insights inform multi-agent system design?")

3. **For each research question, develop:**
   - **Hypothesis:** A testable prediction
   - **Model/Method:** How to investigate (analytical, simulation, or both)
   - **Key parameters:** What to vary and expected ranges
   - **Comparison:** What baseline or alternative to compare against
   - **Related literature:** 2-3 papers using similar approaches

4. **Rank the questions** by feasibility and contribution.

5. **Save the output** to `quality_reports/research_ideation_[sanitized_topic].md`

---

## Output Format

```markdown
# Research Ideation: [Topic]

**Date:** [YYYY-MM-DD]
**Input:** [Original input]

## Overview

[1-2 paragraphs situating the topic]

## Research Questions

### RQ1: [Question] (Feasibility: High/Medium/Low)

**Type:** Descriptive / Comparative / Mechanistic / Robustness / Applied

**Hypothesis:** [Testable prediction]

**Methodology:**
- **Approach:** [Analytical / Simulation / Both]
- **Model:** [Game type, dynamics, population structure]
- **Key parameters:** [What to vary]
- **Comparison:** [Baseline scenario]

**Related Work:** [Author (Year)], [Author (Year)]

---

[Repeat for RQ2-RQ5]

## Ranking

| RQ | Feasibility | Contribution | Priority |
|----|-------------|-------------|----------|

## Suggested Next Steps

1. [Most promising direction]
2. [Model to build first]
3. [Literature to review deeper]
```
