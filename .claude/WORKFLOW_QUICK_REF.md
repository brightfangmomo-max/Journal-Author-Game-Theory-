# Workflow Quick Reference

**Model:** Contractor (you direct, Claude orchestrates)

---

## The Loop

```
Your instruction
    |
[PLAN] (if multi-file or unclear) -> Show plan -> Your approval
    |
[EXECUTE] Implement, verify, done
    |
[REPORT] Summary + what's ready
    |
Repeat
```

---

## I Ask You When

- **Design forks:** "Option A (fast) vs. Option B (robust). Which?"
- **Model ambiguity:** "Spec unclear on X. Assume Y?"
- **Scope question:** "Also refactor Y while here, or focus on X?"
- **Venue choice:** "This affects citation style, formalism level, and structure."

---

## I Just Execute When

- Code fix is obvious (bug, pattern application)
- Verification (compilation, script execution, tolerance checks)
- Documentation (logs, commits)
- Plotting (per established standards)

---

## Quality Gates (No Exceptions)

| Score | Action |
|-------|--------|
| >= 80 | Ready to commit |
| < 80  | Fix blocking issues |

---

## Non-Negotiables

- **Voice:** First person plural "we" throughout. Active voice for contributions.
- **Style:** Contrastive framing ("While..., ..."). No bullet lists in prose.
- **Hedging:** Direct on results, cautious on interpretations.
- **Equations:** Natural language lead-in + "where" definitions after.
- **Figures:** PDF vector format. Woven into analytical prose.
- **Seeds:** `numpy.random.default_rng(42)` (Python), `Random.seed!(42)` (Julia).
- **Paths:** Always relative. Never hardcoded absolute paths.

---

## Preferences

**Writing:** Follow `julian-style-guide.md` and companion files.
**Reporting:** Concise summaries. Details on request.
**Session logs:** Always (post-plan, incremental, end-of-session).
**Default venue:** Biology/general-science register (unless specified).

---

## Exploration Mode

For experimental work, use the **Fast-Track** workflow:
- Work in `explorations/` folder
- 60/100 quality threshold (vs. 80/100 for production)
- No plan needed -- just a research value check
- See `.claude/rules/exploration-fast-track.md`

---

## Next Step

You provide task -> I plan (if needed) -> Your approval -> Execute -> Done.
