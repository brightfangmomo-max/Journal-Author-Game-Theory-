# Julian's Figure Standards

Comprehensive reference for publication-quality figures in game theory, evolutionary dynamics, and AI research. Grounded in Rougier et al. "Ten Simple Rules for Better Figures", Tufte's principles, Nature/Science specs, WCAG accessibility standards, and Paul Tol palettes.

---

## Composition

### Data-Ink Ratio
- Maximise data-ink ratio (Tufte): every non-data element must justify its presence.
- Remove chartjunk: no background fills, no 3D effects, no unnecessary gridlines.
- Use light grey gridlines only when readers need to read precise values.

### Chart Type Selection

| Data Type | Recommended | Avoid |
|-----------|------------|-------|
| Time series | Line plot | Bar chart |
| Comparisons (few categories) | Grouped bar, dot plot | Pie chart |
| Distributions | Violin, box, histogram | Bar chart of means |
| Correlations | Scatter plot | Bubble chart |
| Heatmaps / matrices | Sequential colourmap | Rainbow colourmap |
| Ternary / simplex | Simplex triangle | 3D bar chart |
| Strategy frequencies | Stacked area, simplex | Pie chart |

### Panel Arrangement
- Read left-to-right, top-to-bottom.
- Label panels **(a)**, **(b)**, **(c)** in bold, upper-left corner.
- Align axes across panels that share a variable.
- Share axes where appropriate (`sharex`, `sharey`).

### Aspect Ratios
- Time series: wide (3:1 to 2:1).
- Scatter/comparison: near-square (4:3 to 1:1).
- Simplex plots: equilateral triangle.
- Heatmaps: match data dimensions.

---

## Colour and Accessibility

### Primary Palette: Paul Tol

Use Paul Tol's colourblind-safe palettes as the default. These are designed for up to 7-8 distinguishable colours.

```python
# Paul Tol bright palette (up to 7 colours)
PAUL_TOL_BRIGHT = [
    '#4477AA',  # blue
    '#EE6677',  # red
    '#228833',  # green
    '#CCBB44',  # yellow
    '#66CCEE',  # cyan
    '#AA3377',  # purple
    '#BBBBBB',  # grey
]

# Paul Tol vibrant palette (up to 7 colours)
PAUL_TOL_VIBRANT = [
    '#EE7733',  # orange
    '#0077BB',  # blue
    '#33BBEE',  # cyan
    '#EE3377',  # magenta
    '#CC3311',  # red
    '#009988',  # teal
    '#BBBBBB',  # grey
]
```

```julia
# Paul Tol bright palette (Julia)
const PAUL_TOL_BRIGHT = [
    colorant"#4477AA",  # blue
    colorant"#EE6677",  # red
    colorant"#228833",  # green
    colorant"#CCBB44",  # yellow
    colorant"#66CCEE",  # cyan
    colorant"#AA3377",  # purple
    colorant"#BBBBBB",  # grey
]
```

### Secondary Palette: ColorBrewer

Use ColorBrewer palettes when Paul Tol does not suit the data type (e.g., sequential or diverging data).

- Sequential: `YlOrRd`, `Blues`, `Greens`
- Diverging: `RdBu`, `PiYG`
- Qualitative: `Set2`, `Dark2` (both colourblind-safe)

### Strict Rules

- **Never use rainbow/jet.** Not colourblind-safe, introduces perceptual artefacts.
- **Never encode information by colour alone.** Combine colour with shape, line style, or direct labelling.
- **WCAG contrast:** text and annotations must have contrast ratio >= 4.5:1 against background.
- **Test colourblindness:** simulate deuteranopia, protanopia, tritanopia before finalising.
- When more than 7 categories are needed, use shape/marker variation in addition to colour.

---

## Typography

### Font Sizes

| Element | Minimum | Recommended | Maximum |
|---------|---------|-------------|---------|
| Axis labels | 10pt | 11pt | 14pt |
| Tick labels | 9pt | 10pt | 12pt |
| Legend text | 9pt | 10pt | 12pt |
| Panel labels | 10pt | 12pt | 14pt |
| Annotations | 8pt | 9pt | 11pt |

### Font Family
- Use the same font family as the paper body (typically serif for journals).
- For matplotlib: `'serif'` family or match the journal template.
- LaTeX-rendered math labels are mandatory for any mathematical expression ($b$, $\sigma$, etc.).

### Rules
- All text must be legible at the figure's printed size (check at actual column width).
- Avoid rotated text where possible (especially y-axis labels rotated 90 degrees -- consider horizontal placement).
- Panel labels: bold, sans-serif, upper-left corner.

---

## Data Representation

### Tufte Principles
1. Show the data.
2. Maximise the data-ink ratio.
3. Erase non-data-ink.
4. Erase redundant data-ink.
5. Revise and edit.

### Rougier Rules (Key Subset)
- Know your audience.
- Identify the message (one figure = one message).
- Adapt the figure to the medium (print vs. screen).
- Do not trust defaults.
- Use colour effectively.
- Avoid misleading the reader.

### Specific Guidance
- **No 3D plots for 2D data.** Use heatmaps, contour plots, or colour-coded 2D plots instead.
- **Direct labelling over legends** when feasible (fewer than 4-5 series).
- **Error representation:** show uncertainty (error bars, confidence bands, violin plots). Never plot means without dispersion.
- **Axis starts at zero** only when the zero point is meaningful. Do not distort by forcing zero.
- **Consistent axis ranges** across panels comparing the same quantity.
- **Avoid broken axes** unless the data genuinely requires it.

---

## Technical Specifications

### File Formats
- **Primary:** PDF (vector). All figures must be available as PDF.
- **Backup:** PNG at 300 DPI minimum (for raster-only venues or supplementary web display).
- **Never:** JPEG for scientific figures (lossy compression creates artefacts).

### Venue Dimension Table

| Venue | Single Column | Double Column | Notes |
|-------|--------------|---------------|-------|
| Nature | 89 mm | 183 mm | Max height 247 mm |
| Science | 9 cm | 18.4 cm | Max height 23 cm |
| PNAS | 8.7 cm | 17.8 cm | Max height 23 cm |
| PLoS | 13.2 cm | 17.1 cm | -- |
| PRSB | 8.4 cm | 17.0 cm | Proc. R. Soc. B |
| AAMAS/IJCAI | 3.25 in | 6.875 in | CS conferences |
| Default | 8.5 cm | 17.0 cm | When no venue specified |

### Resolution
- Vector (PDF/SVG): resolution-independent -- always preferred.
- Raster (PNG): 300 DPI minimum, 600 DPI for line art.
- Embedded fonts: all fonts must be embedded in PDF output.

---

## Caption Standards

Cross-reference `julian-notation-formatting.md` for full LaTeX formatting rules.

- **Bold lead sentence:** first sentence of every caption is a standalone summary in bold (`\textbf{...}`).
- **Self-contained:** a reader should understand the figure from caption alone, without reading main text.
- **Panel descriptions:** describe each panel explicitly: "(a) Shows the cooperation frequency as a function of $b$."
- **Statistical details:** report sample sizes, error bar definitions, number of replicates.
- **No redundancy:** do not repeat axis labels verbatim in the caption.

### Example

```latex
\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{Figures/cooperation_dynamics.pdf}
\caption{\textbf{Cooperation declines sharply as the benefit-to-cost ratio falls below the critical threshold.}
(a) Cooperation frequency over 1000 generations for $b/c \in \{1.5, 2.0, 3.0\}$.
(b) Equilibrium cooperation level as a function of $b/c$ ($n = 10{,}000$ replicates per point; error bars show 95\% confidence intervals).
Parameters: population size $N = 100$, mutation rate $\mu = 0.01$.}
\label{fig:cooperation_dynamics}
\end{figure}
```

---

## Domain-Specific Figure Types

### Heatmaps (Parameter Sweeps)
- Use sequential colourmap (e.g., `YlOrRd`, `viridis`).
- Include colourbar with label and units.
- Annotate cells with values when the matrix is small (< 10x10).
- Axis labels should show parameter names and values.

### Simplex Plots (3-Strategy Evolutionary Dynamics)
- Equilateral triangle with vertices labelled by strategy names.
- Interior points represent population compositions.
- Use arrows or colour to show dynamics (gradient field or trajectories).
- Mark fixed points clearly (filled = stable, open = unstable).

### Finite State Automata (FSA) Diagrams
- Use `tikz` or `graphviz` for clean node-edge layouts.
- States as circles, transitions as labelled arrows.
- Start state marked with incoming arrow from nowhere.
- Use consistent positioning (initial state left, accepting states right).

### Time Series (Evolutionary Dynamics)
- X-axis: generation or time step.
- Y-axis: frequency or payoff.
- Use semi-transparent bands for confidence intervals.
- Multiple runs: show mean with individual trajectories in light colour.

### Multi-Panel Comparisons
- Consistent colour mapping across all panels.
- Shared legends (one legend for the entire figure, not per-panel).
- Align axes and use consistent ranges.
- Panel labels: **(a)**, **(b)**, **(c)** in bold.

---

## Implementation Checklists

### Python rcParams Block

```python
import matplotlib.pyplot as plt
import matplotlib as mpl

# Publication-quality defaults
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
    'axes.grid': False,
    'text.usetex': True,
    'text.latex.preamble': r'\usepackage{amsmath}',
    'pdf.fonttype': 42,  # TrueType fonts in PDF
    'ps.fonttype': 42,
}
mpl.rcParams.update(RCPARAMS)

# Paul Tol bright palette
PALETTE = ['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377', '#BBBBBB']
```

### Julia Makie Theme Block

```julia
using CairoMakie

# Publication-quality theme
publication_theme = Theme(
    fontsize = 11,
    Axis = (
        xlabelsize = 11,
        ylabelsize = 11,
        xticklabelsize = 10,
        yticklabelsize = 10,
        spinewidth = 0.8,
        xtickwidth = 0.8,
        ytickwidth = 0.8,
        topspinevisible = false,
        rightspinevisible = false,
    ),
    Legend = (
        labelsize = 10,
        framevisible = false,
    ),
    palette = (
        color = [
            colorant"#4477AA",
            colorant"#EE6677",
            colorant"#228833",
            colorant"#CCBB44",
            colorant"#66CCEE",
            colorant"#AA3377",
            colorant"#BBBBBB",
        ],
    ),
)
set_theme!(publication_theme)
```

### Pre-Submission Checklist

Before declaring a figure complete, verify:

1. [ ] PDF vector output exists and is non-zero size
2. [ ] All text legible at printed column width
3. [ ] Colourblind-safe palette used (Paul Tol or ColorBrewer)
4. [ ] No colour-only encoding (shapes/lines also differentiate)
5. [ ] Axis labels include units where applicable
6. [ ] Font sizes within recommended ranges
7. [ ] Panel labels present and consistent
8. [ ] Caption has bold lead sentence
9. [ ] Error bars / uncertainty shown where applicable
10. [ ] No 3D effects, chartjunk, or rainbow colourmaps
