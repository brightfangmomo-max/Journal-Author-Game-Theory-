---
name: devils-advocate
description: Challenge a paper's argument structure, assumptions, and presentation with 5-7 critical questions. Checks logical gaps, missing alternatives, and potential referee objections.
argument-hint: "[Paper filename]"
allowed-tools: ["Read", "Grep", "Glob"]
---

# Devil's Advocate Review

Critically examine a research paper and challenge its argument with 5-7 specific questions.

**Philosophy:** "We arrive at the strongest possible paper through active challenge."

---

## Setup

1. **Read the target file** (the paper being challenged)
2. **Read the style guides** (`julian-rhetoric-playbook.md`) for argumentation patterns
3. **Read any related papers** in `master_supporting_docs/` for context

---

## Challenge Categories

Generate 5-7 challenges from these categories:

### 1. Assumption Challenges
> "What happens to your main result if assumption X is relaxed?"

### 2. Alternative Explanation Challenges
> "Could mechanism Y produce the same pattern without your proposed explanation?"

### 3. Identification Challenges
> "How do you rule out that the effect is driven by Z rather than your proposed mechanism?"

### 4. Scope Challenges
> "Your model assumes X -- how sensitive are results to this?"

### 5. Literature Gap Challenges
> "Author (Year) found the opposite in a related setting. How do you reconcile?"

### 6. Presentation Challenges
> "A referee might read Section X as claiming Y -- is that your intent?"

### 7. Contribution Challenges
> "How does this advance beyond what was already known from Prior Work?"

---

## Output Format

```markdown
# Devil's Advocate: [Paper Title]

## Challenges

### Challenge 1: [Category] -- [Short title]
**Question:** [The specific critical question]
**Why it matters:** [Why a referee would care]
**Suggested resolution:** [How to address it]
**Section affected:** [Section name/number]
**Severity:** [High / Medium / Low]

[Repeat for 5-7 challenges]

## Summary Verdict
**Strengths:** [2-3 things done well]
**Critical changes:** [0-2 changes before submission]
**Suggested improvements:** [2-3 nice-to-have changes]
```

---

## Principles

- **Be specific:** Reference exact sections, equations, claims
- **Be constructive:** Every challenge has a suggested resolution
- **Be honest:** If the paper is strong, say so
- **Think like a top-journal referee:** What would make them reject?
- **Prioritize:** Logic gaps > missing robustness > presentation issues
