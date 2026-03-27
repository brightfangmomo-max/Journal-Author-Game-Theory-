---
paths:
  - "**/*.jl"
---

# Julia Code Conventions

## Script Structure

```julia
#!/usr/bin/env julia
#=
[Descriptive Title]

Author: Julian Garcia
Purpose: [What this script does]
Inputs: [Data files]
Outputs: [Figures, tables, data files]
=#

using Random
using Statistics
using Plots
using CSV, DataFrames

# Configuration
const SEED = 42
Random.seed!(SEED)
const OUTPUT_DIR = joinpath(@__DIR__, "..", "..", "output")
mkpath(OUTPUT_DIR)

# Analysis functions
# ...

# Main execution
function main()
    # ...
end

main()
```

## Project Management

- Use `Project.toml` for dependencies
- Activate project with `--project` flag
- Pin versions in `[compat]` section

## Type Stability

- Functions in hot loops MUST be type-stable
- Use `@code_warntype` to check
- Avoid containers with abstract element types in performance code
- Use concrete types: `Vector{Float64}` not `Vector{Real}`

## Monte Carlo Simulations

```julia
function run_simulation(; n_reps::Int=10_000, seed::Int=42)
    rng = MersenneTwister(seed)
    results = Vector{Float64}(undef, n_reps)

    for i in 1:n_reps
        results[i] = single_run(rng)
    end

    return results
end
```

- Pass `rng` explicitly to functions
- Preallocate result arrays
- Use `@inbounds` for inner loops when safe
- Document convergence: report standard error of the mean

## Paths

- Use `joinpath()` for all path construction
- All paths relative to repository root
- Create directories with `mkpath()`
- Never hardcode absolute paths

## Figures

**Full standards:** `julian-figure-standards.md` (repo root). Use `/review-figure` to check quality.

```julia
using CairoMakie

# Publication-quality theme (apply at top of every figure script)
publication_theme = Theme(
    fontsize = 11,
    Axis = (
        xlabelsize = 11, ylabelsize = 11,
        xticklabelsize = 10, yticklabelsize = 10,
        topspinevisible = false, rightspinevisible = false,
    ),
    Legend = (labelsize = 10, framevisible = false),
    palette = (color = [
        colorant"#4477AA", colorant"#EE6677", colorant"#228833",
        colorant"#CCBB44", colorant"#66CCEE", colorant"#AA3377", colorant"#BBBBBB",
    ],),
)
set_theme!(publication_theme)

# Save as PDF (vector)
save(joinpath(OUTPUT_DIR, "figure_name.pdf"), fig)
```

- **Palette:** Paul Tol (primary), ColorBrewer (secondary). Never rainbow/jet.
- **Format:** PDF vector primary. Never JPEG.
- **Accessibility:** no colour-only encoding; combine colour with shape/line style.
- **Uncertainty:** always show error bars, confidence bands, or distributions.

## Reproducibility

- Every analysis directory must have a `run_all.jl` driver script (see `reproducibility-protocol.md`).
- Long-running scripts must be **restartable**: check `isfile(output)` before re-computing.
- Use **atomic file creation**: write to `tempname()`, then `mv()` to final path.
- Never hand-edit data files. All transformations must be scripted.
- Standalone scripts should print usage when called with `--help` (use `ArgParse.jl` or a simple check on `ARGS`).

## Data Storage

- Binary results: JLD2 format (`@save`, `@load`)
- Portable results: CSV format
- Always save both when practical
