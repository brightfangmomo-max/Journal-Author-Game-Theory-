---
paths:
  - "doc/tex/**/*.tex"
  - "scr/**"
---

# Task Completion Verification Protocol

**At the end of EVERY task, Claude MUST verify the output works correctly.** This is non-negotiable.

## For LaTeX Papers:
1. Compile with xelatex and check for errors
2. Open the PDF to verify it renders (`open` on macOS, `xdg-open` on Linux)
3. Check for overfull hbox warnings
4. Check for undefined citations

## For Python Scripts:
1. Run `python3 scr/filename.py`
2. Verify output files (PDF, CSV, NPZ) were created with non-zero size
3. Spot-check results for reasonable magnitude

## For Figures:
1. Verify figure files exist and have non-zero size
2. Check format is PDF (vector) for publication
3. Open to verify visual appearance

## Common Pitfalls:
- **Relative paths**: Scripts should use paths relative to repo root
- **Assuming success**: Always verify output files exist AND contain correct content
- **Missing seeds**: Stochastic scripts must set random seed

## Verification Checklist:
```
[ ] Output file created successfully
[ ] No compilation/execution errors
[ ] Figures display correctly
[ ] Reported results to user
```
