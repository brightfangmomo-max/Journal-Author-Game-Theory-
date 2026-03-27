---
name: data-analysis
description: End-to-end Python data analysis workflow from exploration through analysis to publication-ready tables and figures
argument-hint: "[dataset path or description of analysis goal]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task"]
---

# Data Analysis Workflow

Run an end-to-end data analysis in Python: load, explore, analyze, and produce publication-ready output.

**Input:** `$ARGUMENTS` -- a dataset path (e.g., `data/panel.csv`) or a description of the analysis goal.

---

## Constraints

- **Follow Python code conventions** in `.claude/rules/python-code-conventions.md`
- **Save all scripts** to `scripts/python/` with descriptive names
- **Save all outputs** (figures, tables, data) to `output/`
- **Use publication-quality figures** (PDF vector format, proper fonts)
- **Run python-reviewer** on the generated script before presenting results

---

## Workflow Phases

### Phase 1: Setup and Data Loading

1. Read `.claude/rules/python-code-conventions.md` for project standards
2. Create Python script with proper header (title, author, purpose, inputs, outputs)
3. Import required packages at top
4. Set seed: `rng = np.random.default_rng(42)`
5. Load and inspect the dataset

### Phase 2: Exploratory Data Analysis

Generate diagnostic outputs:
- **Summary statistics:** `.describe()`, missingness rates, variable types
- **Distributions:** Histograms for key continuous variables
- **Relationships:** Scatter plots, correlation matrices
- **Time patterns:** If panel data, plot trends over time
- **Group comparisons:** If treatment/control, compare pre-treatment means

Save all diagnostic figures to `output/diagnostics/`.

### Phase 3: Main Analysis

Based on the research question:
- **Statistical analysis:** Use scipy.stats, statsmodels, or sklearn as appropriate
- **Simulation:** Use numpy for Monte Carlo, set seed for reproducibility
- **Multiple specifications:** Start simple, progressively add complexity

### Phase 4: Publication-Ready Output

**Tables:**
- Use pandas for formatting
- Export as `.tex` for LaTeX inclusion and `.csv` for portability

**Figures:**
- Use matplotlib with publication defaults
- Set explicit dimensions: `fig, ax = plt.subplots(figsize=(6, 4))`
- Include proper axis labels (sentence case, units)
- Save as PDF (vector) and PNG (raster backup, 300 DPI)

### Phase 5: Save and Review

1. Save all key results to `output/`
2. Run the python-reviewer agent on the generated script
3. Address any Critical or High issues from the review

---

## Script Template

```python
#!/usr/bin/env python3
"""
[Descriptive Title]

Author: Julian Garcia
Purpose: [What this script does]
Inputs: [Data files]
Outputs: [Figures, tables, data files]
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuration
SEED = 42
rng = np.random.default_rng(SEED)
OUTPUT_DIR = Path("output/analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Data Loading
# ...

# 2. Exploratory Analysis
# ...

# 3. Main Analysis
# ...

# 4. Tables and Figures
# ...

# 5. Export
# ...
```

---

## Important

- **Reproduce, don't guess.** If the user specifies an analysis, run exactly that.
- **Show your work.** Print summary statistics before jumping to analysis.
- **Use relative paths.** All paths relative to repository root.
- **No hardcoded values.** Use variables for parameters.
