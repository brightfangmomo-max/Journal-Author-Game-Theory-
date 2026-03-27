---
paths:
  - "scr/**/*.py"
  - "**/*.py"
---

# Python Code Conventions

## Script Structure

```python
#!/usr/bin/env python3
"""
[Descriptive Title]

Author: Julian Garcia
Purpose: [What this script does]
Inputs: [Data files]
Outputs: [Figures, tables, data files]
"""

# 0. Imports
import os
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 1. Configuration
SEED = 42
rng = np.random.default_rng(SEED)
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 2. Data Loading
# ...

# 3. Analysis
# ...

# 4. Figures
# ...

# 5. Save Results
# ...
```

## Random Number Generation

- Use `numpy.random.default_rng(seed)` (NOT legacy `numpy.random.seed()`)
- Pass `rng` explicitly to functions that need randomness
- Set seed once at the top of the script

## Paths

- Use `pathlib.Path` for all path operations
- All paths relative to repository root
- Create output directories with `mkdir(parents=True, exist_ok=True)`
- Never hardcode absolute paths

## Figures (Publication Quality)

**Full standards:** `julian-figure-standards.md` (repo root). Use `/review-figure` to check quality.

```python
import matplotlib as mpl

# Publication-quality defaults (apply at top of every figure script)
RCPARAMS = {
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.figsize': (6, 4),
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'text.usetex': True,
    'pdf.fonttype': 42,
}
mpl.rcParams.update(RCPARAMS)

# Paul Tol bright palette (colourblind-safe, up to 7 colours)
PALETTE = ['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377', '#BBBBBB']

# Standard figure setup
fig, ax = plt.subplots(figsize=(6, 4))
ax.set_xlabel("Parameter $b$", fontsize=11)
ax.set_ylabel("Cooperation level", fontsize=11)
ax.tick_params(labelsize=10)
fig.tight_layout()

# Save as PDF (vector) + PNG (raster backup)
fig.savefig(OUTPUT_DIR / "figure_name.pdf", bbox_inches="tight")
fig.savefig(OUTPUT_DIR / "figure_name.png", dpi=300, bbox_inches="tight")
plt.close(fig)
```

- **Palette:** Paul Tol (primary), ColorBrewer (secondary). Never rainbow/jet.
- **Format:** PDF vector primary, PNG 300 DPI backup. Never JPEG.
- **Accessibility:** no colour-only encoding; combine colour with shape/line style.
- **Uncertainty:** always show error bars, confidence bands, or distributions.

## Data Storage

- Arrays: `.npz` format (`np.savez()`)
- Tables: `.csv` format (`pd.DataFrame.to_csv()`)
- Pickle (`.pkl`) only for complex objects, with a CSV fallback

## Dependencies

- Maintain `requirements.txt` in project root or `scr/`
- Pin major versions: `numpy>=1.24,<2.0`

## Reproducibility

- Every analysis directory must have a `run_all.py` driver script (see `reproducibility-protocol.md`).
- Long-running scripts must be **restartable**: check if output exists before re-computing.
- Use **atomic file creation**: write to a temp file, rename on completion.
- Never hand-edit data files. All transformations must be scripted.
- Standalone scripts must support `--help` via `argparse`.

## Type Hints

- Add type hints to all function signatures
- Use `from __future__ import annotations` for modern syntax
