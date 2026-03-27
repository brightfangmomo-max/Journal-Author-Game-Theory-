---
name: run-simulation
description: Execute Monte Carlo simulations or computational experiments in Python or Julia. Supports parameter sweeps, convergence checks, and result visualization.
argument-hint: "[script path] [optional: --sweep param=start:step:end]"
allowed-tools: ["Read", "Bash", "Write", "Edit", "Glob"]
---

# Run Simulation

Execute Monte Carlo simulations or computational experiments with proper verification.

**Input:** `$ARGUMENTS` -- path to a simulation script, optionally with parameter sweep specification.

---

## Steps

### 1. Pre-flight Checks

Before running:
- [ ] Script exists and has no syntax errors
- [ ] Random seed is set at the top
- [ ] Output directory exists or will be created
- [ ] Required dependencies are available

### 2. Execute

**For Python:**
```bash
python3 $SCRIPT_PATH 2>&1
```

**For Julia:**
```bash
julia --project=scripts/julia $SCRIPT_PATH 2>&1
```

### 3. Parameter Sweep (if requested)

If `--sweep` is specified, run the script multiple times with varying parameters:

```bash
# Example: sweep benefit parameter from 1 to 5
for b in 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5 5.0; do
    python3 script.py --benefit $b 2>&1 | tail -5
done
```

### 4. Verification

After execution:
- [ ] Script completed without errors
- [ ] Output files created with non-zero size
- [ ] Results are numerically reasonable (no NaN, no inf)
- [ ] If stochastic: re-run with same seed produces identical results
- [ ] If Monte Carlo: check standard error of mean estimates

### 5. Convergence Check (for Monte Carlo)

```python
# Check if results have converged
import numpy as np
results = np.load("output/results.npz")
values = results["cooperation_levels"]
running_mean = np.cumsum(values) / np.arange(1, len(values) + 1)
se = np.std(values) / np.sqrt(len(values))
print(f"Mean: {np.mean(values):.4f} +/- {se:.4f}")
```

### 6. Generate Summary Figures

If the simulation produces data, generate quick visualization:
- Time series of key quantities
- Parameter sweep heatmap (if applicable)
- Distribution of outcomes

Save to `output/` or `Figures/`.

### 7. Report Results

```markdown
## Simulation Report

**Script:** [path]
**Date:** [YYYY-MM-DD]
**Seed:** [seed value]

### Parameters
| Parameter | Value |
|-----------|-------|
| ... | ... |

### Results
| Metric | Value | SE |
|--------|-------|----|
| ... | ... | ... |

### Output Files
- [list of generated files]

### Convergence
- [converged / not converged / N/A]
```
