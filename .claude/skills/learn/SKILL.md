---
name: learn
description: |
  Extract reusable knowledge from the current session into a persistent skill.
  Use when you discover something non-obvious, create a workaround, or develop
  a multi-step workflow that future sessions would benefit from.
argument-hint: "[skill-name (kebab-case)]"
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep"]
---

# /learn -- Skill Extraction Workflow

Extract non-obvious discoveries into reusable skills that persist across sessions.

## When to Use This Skill

Invoke `/learn` when you encounter:

- **Non-obvious debugging** -- Investigation that took significant effort
- **Misleading errors** -- Error message was wrong, found the real cause
- **Workarounds** -- Found a limitation with a creative solution
- **Tool integration** -- Undocumented API usage or configuration
- **Repeatable workflows** -- Multi-step task you'd do again

## Workflow Phases

### PHASE 1: Evaluate (Self-Assessment)

Before creating a skill, answer:

1. "What did I just learn that wasn't obvious before starting?"
2. "Would future-me benefit from this being documented?"
3. "Was the solution non-obvious from documentation alone?"

**Continue only if YES to at least one question.**

### PHASE 2: Check Existing Skills

```bash
ls .claude/skills/ 2>/dev/null
```

### PHASE 3: Create Skill

Create the skill file at `.claude/skills/[skill-name]/SKILL.md`:

```yaml
---
name: descriptive-kebab-case-name
description: |
  [Include specific triggers in the description]
argument-hint: "[expected arguments]"
allowed-tools: [...]
---

# Skill Name

## Problem
[What situation triggers this skill]

## Solution
[Step-by-step solution]

## Verification
[How to verify it worked]
```

### PHASE 4: Quality Gates

- [ ] Description has specific trigger conditions
- [ ] Solution was verified to work
- [ ] Content is specific enough to be actionable
- [ ] Content is general enough to be reusable
- [ ] No sensitive information

## Output

```
Skill created: .claude/skills/[name]/SKILL.md
  Trigger: [when to use]
  Problem: [what it solves]
```
