# Session Log: Deep Audit

**Date:** 2026-03-27
**Goal:** Run /deep-audit to find and fix infrastructure inconsistencies across the repository.

## Key Context

- The `claude_bones` academic workflow scaffold was overlaid onto a project with a different directory structure
- Template defaults (`Papers/`, `scripts/python/`, `Bibliography.bib`, `Figures/`) didn't match actual structure (`doc/tex/`, `scr/`, `doc/tex/references.bib`)

## Decisions & Progress

- Found 18 genuine issues (10 critical, 6 major, 2 minor)
- Root cause: 10 of 18 rules had path triggers pointing to empty/wrong directories and never fired
- Fixed all rule paths: `Papers/**` → `doc/tex/**`, `scripts/**` → `scr/**`
- Fixed CLAUDE.md: folder structure, script table (added 10 missing scripts), dead references
- Fixed protect-files.sh: `Bibliography.bib` → `references.bib`
- Fixed single-source-of-truth.md references
- Fixed latex-conventions.md typo (`\end{figure>`)
- Verification sweep confirmed all stale path references eliminated

## Agent Results (Round 2)

After initial fixes, 5 parallel audit agents returned additional findings:

### Triaged as genuine (not yet fixed — require user decision):
- `scr/fig8_heatmap_outcomes.py:134` — uses `cmap='RdYlGn'` (not colorblind-safe). Recommend replacing with `viridis` or Paul Tol diverging palette. **Deferred: changes figure output.**
- `doc/tex/main.tex:1354,1366,1516` — 3 captions missing `\textbf{}` bold lead sentence. **Deferred: paper content change.**

### Triaged as false alarms:
- 4 rules missing YAML frontmatter (orchestrator-protocol, plan-first-workflow, session-logging, single-source-of-truth) — these are **global rules** that should always load; no `paths:` trigger needed
- "Missing closing `---`" in frontmatter — false alarm; all rules with paths have proper frontmatter
- `protect-files.sh` exit code 2 — actually correct for PreToolUse hooks (2 = block)
- Hook "late hashlib import" — acceptable pattern for conditional imports

## Status

Infrastructure fixes: 18/18 CLEAN.
Paper content issues flagged: 4 (deferred to user).

