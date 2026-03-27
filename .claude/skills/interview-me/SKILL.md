---
name: interview-me
description: Interactive interview to formalize a research idea into a structured specification with hypotheses and methodology
argument-hint: "[brief topic or 'start fresh']"
allowed-tools: ["Read", "Write"]
---

# Research Interview

Conduct a structured interview to help formalize a research idea into a concrete specification.

**Input:** `$ARGUMENTS` -- a brief topic description or "start fresh" for an open-ended exploration.

---

## How This Works

This is a **conversational** skill. Instead of producing a report immediately, you conduct an interview by asking questions one at a time, probing deeper based on answers, and building toward a structured research specification.

**Do NOT use AskUserQuestion.** Ask questions directly in your text responses, one or two at a time. Wait for the user to respond before continuing.

---

## Interview Structure

### Phase 1: The Big Picture (1-2 questions)
- "What phenomenon or puzzle are you trying to understand?"
- "Why does this matter? Who should care about the answer?"

### Phase 2: Theoretical Motivation (1-2 questions)
- "What's your intuition for why X happens / what drives Y?"
- "What would standard theory predict? Do you expect something different?"

### Phase 3: Model and Method (1-2 questions)
- "What kind of model are you thinking? (evolutionary dynamics, repeated game, agent-based, etc.)"
- "What's the key mechanism or deviation from the standard setup?"

### Phase 4: Computational Approach (1-2 questions)
- "Are you thinking analytical results, simulations, or both?"
- "What parameters would you sweep over? What's the main comparison?"

### Phase 5: Expected Results (1-2 questions)
- "What would you expect to find? What would surprise you?"
- "What would the results imply for the field?"

### Phase 6: Contribution (1 question)
- "How does this differ from what's already been done? What's the gap you're filling?"

---

## After the Interview

Once you have enough information (typically 5-8 exchanges), produce a **Research Specification Document**:

```markdown
# Research Specification: [Title]

**Date:** [YYYY-MM-DD]
**Researcher:** Julian Garcia

## Research Question

[Clear, specific question in one sentence]

## Motivation

[2-3 paragraphs: why this matters, theoretical context, broader relevance]

## Model

[Description of the model or theoretical framework]

## Methodology

- **Approach:** [Analytical / Simulation / Both]
- **Key mechanism:** [What varies]
- **Parameters:** [Main parameters and ranges]
- **Comparison:** [What scenarios are being compared]

## Expected Results

[What the researcher expects to find and why]

## Contribution

[How this advances the literature -- 2-3 sentences]

## Open Questions

[Issues raised during the interview that need further thought]
```

**Save to:** `quality_reports/research_spec_[sanitized_topic].md`

---

## Interview Style

- **Be curious, not prescriptive.** Draw out the researcher's thinking.
- **Probe weak spots gently.** "What would a skeptic say about...?"
- **Build on answers.** Each question should follow from the previous response.
- **Know when to stop.** If the researcher has a clear vision after 4-5 exchanges, move to the specification.
