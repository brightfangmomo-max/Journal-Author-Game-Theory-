---
paths:
  - "scr/**/*.py"
---

# Replication-First Protocol

**Core principle:** Every computational result must be reproducible from source.

---

## Phase 1: Environment & Setup

Before writing any script:

- [ ] Document the language version (Python 3.x, Julia 1.x)
- [ ] Pin package versions (requirements.txt, Project.toml)
- [ ] Set random seeds explicitly at the top of every script
- [ ] Use relative paths from repo root

---

## Phase 2: Script Standards

### Python Scripts

```python
# Header: title, author, purpose, inputs, outputs
import numpy as np

# Set seed once at top
RNG = np.random.default_rng(42)

# Use pathlib for all paths
from pathlib import Path
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

### Julia Scripts

```julia
# Header: title, author, purpose, inputs, outputs
using Random

# Set seed once at top
Random.seed!(42)

# Use project-relative paths
output_dir = joinpath(@__DIR__, "..", "..", "output")
mkpath(output_dir)
```

---

## Phase 3: Verification

### Tolerance Thresholds

| Type | Tolerance | Rationale |
|------|-----------|-----------|
| Integers (N, counts) | Exact match | No reason for difference |
| Point estimates | < 1e-6 | Numerical precision |
| Standard errors | < 1e-4 | MC variability |
| Coverage rates | +/- 0.01 | MC with B reps |

### If Results Change

**Do NOT silently accept.** Investigate which step introduced the change:
- Check random seed consistency
- Check package version changes
- Check data preprocessing steps
- Document the investigation even if unresolved

---

## Phase 4: Outputs

- [ ] Save all generated figures to `doc/tex/`
- [ ] Save all computed results to `output/`
- [ ] Every figure in the paper has a script that generates it
- [ ] Every table in the paper has a script or computation trail
- [ ] Commit the generating script alongside the output
