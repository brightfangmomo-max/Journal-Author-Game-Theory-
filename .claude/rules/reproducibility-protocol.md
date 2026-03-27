---
paths:
  - "scr/**"
  - "explorations/**"
---

# Reproducibility Protocol

Based on Noble (2009), "A Quick Guide to Organizing Computational Biology Projects."
Two core principles: (1) someone unfamiliar with the project should understand what was done and why; (2) everything you do, you will probably have to do over again.

## Driver Scripts

Every analysis directory must have a top-level driver script that reproduces all outputs from raw data.

- Name it `run_all.py` (Python) or `run_all.jl` (Julia).
- The driver script is the single entry point: running it regenerates every figure, table, and data file.
- Call subscripts in order; do not duplicate logic.
- Centralise all file paths and key parameters at the top of the driver.
- Comment generously — the driver is documentation, not just code.

```python
# run_all.py
"""Reproduce all results for [Paper/Experiment Name]."""
from pathlib import Path

# === Configuration ===
DATA_DIR = Path("../../data")
OUTPUT_DIR = Path("../../output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
N_REPS = 10_000

# === Pipeline ===
# Step 1: Process raw data
exec(open("01_preprocess.py").read())  # or use subprocess/import

# Step 2: Run simulations
exec(open("02_simulate.py").read())

# Step 3: Generate figures
exec(open("03_figures.py").read())
```

## Restartability

Long-running scripts must check for existing output before re-running.

```python
output_file = OUTPUT_DIR / "simulation_results.npz"
if not output_file.exists():
    results = run_simulation(n_reps=N_REPS, seed=SEED)
    np.savez(output_file, results=results)
else:
    results = np.load(output_file)["results"]
```

```julia
output_file = joinpath(OUTPUT_DIR, "simulation_results.jld2")
if !isfile(output_file)
    results = run_simulation(n_reps=N_REPS, seed=SEED)
    @save output_file results
else
    @load output_file results
end
```

## Atomic File Creation

Never write directly to the final output path. Write to a temporary file, then rename on completion. This prevents half-written files from being mistaken for valid results.

```python
import tempfile, shutil

with tempfile.NamedTemporaryFile(dir=OUTPUT_DIR, suffix=".csv", delete=False) as tmp:
    df.to_csv(tmp.name, index=False)
    shutil.move(tmp.name, OUTPUT_DIR / "results.csv")
```

```julia
tmp = tempname()
CSV.write(tmp, df)
mv(tmp, joinpath(OUTPUT_DIR, "results.csv"), force=true)
```

## No Manual Data Editing

All data transformations must be scripted. Never hand-edit CSVs, Excel files, or intermediate outputs. If a dataset needs cleaning, write a preprocessing script. The pipeline from raw data to final output must be fully automated.

## Script Interface

Every standalone script must respond to `--help` (or `-h`) with a usage message describing inputs, outputs, and key parameters.

```python
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Run cooperation simulations under varying selection."
    )
    parser.add_argument("--n-reps", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("../../output"))
    args = parser.parse_args()
```

## Verification

After running a driver script, confirm:
- All expected output files exist
- File sizes are non-zero
- Key summary statistics match expected ranges
- Figures render correctly (spot-check PDFs)
