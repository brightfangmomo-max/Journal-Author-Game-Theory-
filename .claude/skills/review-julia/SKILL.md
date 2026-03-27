---
name: review-julia
description: Launch the julia-reviewer agent on Julia scripts. Produces a quality report covering style, type stability, performance, and Monte Carlo best practices.
argument-hint: "[script path or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review Julia Code

Launch the julia-reviewer agent to review Julia scripts for quality, performance, and simulation best practices.

**Input:** `$ARGUMENTS` -- a script path (e.g., `scripts/julia/simulation.jl`) or "all" to review all Julia scripts.

## Steps

1. **Identify files to review:**
   - If `$ARGUMENTS` is a specific file: review that file only
   - If `$ARGUMENTS` is "all": find all `.jl` files in `scripts/julia/`

2. **For each file, delegate to the julia-reviewer agent:**

   ```
   Delegate to the julia-reviewer agent:
   "Review the script at [path]"
   ```

3. **Collect and present results:**
   - Summary of issues per file
   - Critical issues highlighted
   - Overall assessment

4. **Save report** to `quality_reports/[SCRIPT_NAME]_julia_review.md`
