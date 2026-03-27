---
name: review-python
description: Launch the python-reviewer agent on Python scripts. Produces a quality report covering PEP 8, scientific computing practices, reproducibility, and figure quality.
argument-hint: "[script path or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review Python Code

Launch the python-reviewer agent to review Python scripts for quality, scientific computing best practices, and reproducibility.

**Input:** `$ARGUMENTS` -- a script path (e.g., `scripts/python/simulation.py`) or "all" to review all Python scripts.

## Steps

1. **Identify files to review:**
   - If `$ARGUMENTS` is a specific file: review that file only
   - If `$ARGUMENTS` is "all": find all `.py` files in `scripts/python/`

2. **For each file, delegate to the python-reviewer agent:**

   ```
   Delegate to the python-reviewer agent:
   "Review the script at [path]"
   ```

3. **Collect and present results:**
   - Summary of issues per file
   - Critical issues highlighted
   - Overall assessment

4. **Save report** to `quality_reports/[SCRIPT_NAME]_python_review.md`
