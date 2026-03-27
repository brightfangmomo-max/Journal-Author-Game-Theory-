---
name: review-paper
description: Comprehensive manuscript review covering argument structure, model validity, literature positioning, writing quality, and potential referee objections
argument-hint: "[paper filename in master_supporting_docs/ or path to .tex/.pdf]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Manuscript Review

Produce a thorough, constructive review of an academic manuscript -- the kind of report a top-journal referee would write.

**Input:** `$ARGUMENTS` -- path to a paper (.tex or .pdf), or a filename in `master_supporting_docs/`.

---

## Steps

1. **Locate and read the manuscript.** Check:
   - Direct path from `$ARGUMENTS`
   - `master_supporting_docs/supporting_papers/$ARGUMENTS`
   - Glob for partial matches

2. **Read the full paper** end-to-end. For long PDFs, read in chunks (5 pages at a time).

3. **Evaluate across 6 dimensions** (see below).

4. **Generate 3-5 "referee objections"** -- the tough questions a top referee would ask.

5. **Produce the review report.**

6. **Save to** `quality_reports/paper_review_[sanitized_name].md`

---

## Review Dimensions

### 1. Argument Structure
- Is the research question clearly stated?
- Does the introduction motivate the question effectively?
- Is the logical flow sound (question -> model -> results -> conclusion)?
- Are the conclusions supported by the evidence?

### 2. Model Validity
- Are the assumptions clearly stated and justified?
- Is the model appropriate for the research question?
- Are there important factors left out?
- Are equilibrium/dynamics analyses correct?

### 3. Computational/Analytical Methods
- Are simulations well-designed (sufficient replications, parameter sweeps)?
- Are analytical results verified computationally?
- Are robustness checks adequate?

### 4. Literature Positioning
- Are the key papers cited?
- Is prior work characterized accurately?
- Is the contribution clearly differentiated from existing work?

### 5. Writing Quality
- Clarity and concision
- Academic tone (aligned with Julian's style guide)
- Consistent notation throughout
- Tables and figures are self-contained

### 6. Presentation
- Are figures well-designed?
- Is the paper the right length for the contribution?
- Any formatting issues?

---

## Output Format

```markdown
# Manuscript Review: [Paper Title]

**Date:** [YYYY-MM-DD]
**Reviewer:** review-paper skill
**File:** [path to manuscript]

## Summary Assessment

**Overall recommendation:** [Strong Accept / Accept / Revise & Resubmit / Reject]

[2-3 paragraph summary]

## Strengths

1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

## Major Concerns

### MC1: [Title]
- **Dimension:** [Model / Methods / Argument / Literature / Writing / Presentation]
- **Issue:** [Specific description]
- **Suggestion:** [How to address]

## Minor Concerns

### mc1: [Title]
- **Issue:** [Description]
- **Suggestion:** [Fix]

## Referee Objections

### RO1: [Question]
**Why it matters:** [Why this could be fatal]
**How to address it:** [Suggested response]

## Summary Statistics

| Dimension | Rating (1-5) |
|-----------|-------------|
| Argument Structure | [N] |
| Model Validity | [N] |
| Methods | [N] |
| Literature | [N] |
| Writing | [N] |
| Presentation | [N] |
| **Overall** | **[N]** |
```
