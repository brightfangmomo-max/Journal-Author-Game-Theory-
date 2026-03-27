---
name: deep-audit
description: |
  Deep consistency audit of the entire repository infrastructure.
  Launches parallel specialist agents to find factual errors, code bugs,
  count mismatches, and cross-document inconsistencies. Then fixes all issues
  and loops until clean.
  Use when: after making broad changes, before releases, or when user says
  "audit", "find inconsistencies", "check everything".
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Task"]
---

# /deep-audit -- Repository Infrastructure Audit

Run a comprehensive consistency audit across the entire repository, fix all issues found, and loop until clean.

## When to Use

- After broad changes (new skills, rules, agents)
- Before major commits
- When the user asks to "find inconsistencies", "audit", or "check everything"

## Workflow

### PHASE 1: Launch Parallel Audit Agents

#### Agent 1: CLAUDE.md Accuracy
Focus: `CLAUDE.md`
- All numeric claims match reality (skill count, agent count, rule count)
- All file paths mentioned actually exist on disk
- All skill/agent/rule names match actual directory names
- Skills table matches actual skill directories 1:1

#### Agent 2: Hook Code Quality
Focus: `.claude/hooks/*.py` and `.claude/hooks/*.sh`
- Proper error handling (fail-open pattern)
- JSON input/output correctness
- Exit code correctness
- `from __future__ import annotations` for compatibility

#### Agent 3: Skills and Rules Consistency
Focus: `.claude/skills/*/SKILL.md` and `.claude/rules/*.md`
- Valid YAML frontmatter in all files
- `allowed-tools` values are sensible
- Rule `paths:` reference existing directories
- No contradictions between rules
- All templates referenced in rules exist in `templates/`

#### Agent 4: Style Guide Consistency
Focus: `julian-*.md` files and `.claude/rules/paper-writing-protocol.md`
- Paper writing protocol rule accurately reflects the 5 style guide files
- No contradictions between rule summary and full guides
- Notation conventions are consistent

#### Agent 5: Figure Quality
Focus: `Figures/**`, `scripts/python/fig_*`, `scripts/julia/fig_*`, `Papers/**/*.tex` (caption checks)
- Colourblind-safe palettes used (Paul Tol or ColorBrewer, no rainbow/jet)
- PDF vector output exists for every figure
- Font sizes within recommended ranges
- Consistent colour mapping across figures within the same paper
- Captions have bold lead sentences
- No colour-only encoding
- Cross-reference `julian-figure-standards.md` for full checklist

### PHASE 2: Triage and Fix

Categorize each finding as genuine bug or false alarm. Fix all genuine bugs.

Common false alarms to watch for:
- `allowed-tools` linter warning -- known linter bug, field IS valid
- Counts in old session logs -- historical records, not user-facing docs

### PHASE 3: Re-verify

Launch fresh agents to confirm fixes. Max 5 loops.

## Key Lessons from Past Audits

| Bug Pattern | Where to Check | What Went Wrong |
|-------------|---------------|-----------------|
| Stale counts ("19 skills" -> "21") | CLAUDE.md, README | Added skills but didn't update all mentions |
| Hook exit codes | All Python hooks | Wrong exit code silently discards output |
| Hook field names | post-compact-restore.py | SessionStart uses `source`, not `type` |
| Missing fail-open | Python hooks `__main__` | Unhandled exception -> exit 1 -> confusing behavior |
| Python 3.10+ syntax | Type hints like `dict \| None` | Need `from __future__ import annotations` |
| Missing directories | quality_reports/specs/ | Referenced in rules but never created |
| macOS-only commands | Skills, rules | `open` without `xdg-open` fallback |
| Protected file blocking | settings.json edits | protect-files.sh blocks Edit/Write |

## Output Format

```
## Round N Audit Results

### Issues Found: X genuine, Y false alarms

| # | Severity | File | Issue | Status |
|---|----------|------|-------|--------|
| 1 | Critical | file:42 | Description | Fixed |

### Result: [CLEAN | N issues remaining]
```
