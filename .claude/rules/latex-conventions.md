---
paths:
  - "doc/tex/**/*.tex"
---

# LaTeX Conventions

Modern LaTeX best practices, based on l2tabu and current community standards.

## Source Formatting

- **One sentence per line.** Never join sentences on a single line.
- Indent environments by 2 spaces.
- Blank line between paragraphs (never `\\` or `\newline` for paragraph breaks).
- Keep lines under 120 characters where possible; break long sentences at clause boundaries.
- Use `%` comments sparingly — the text should be self-explanatory.

## Obsolete Commands (Never Use)

| Obsolete | Modern Replacement |
|----------|-------------------|
| `\bf`, `\it`, `\sc`, `\rm` | `\textbf{}`, `\textit{}`, `\textsc{}`, `\textrm{}` |
| `\over` | `\frac{}{}` |
| `\centerline{}` | `\centering` (inside environment) |
| `\begin{center}` inside floats | `\centering` at top of float |
| `$$...$$` | `\[...\]` or `equation` environment |
| `\def\macroname` | `\newcommand{\macroname}` |
| `\hline` in tables | `\toprule`, `\midrule`, `\bottomrule` (booktabs) |
| `\usepackage{epsfig}` | `\usepackage{graphicx}` |
| `\usepackage{subfigure}` | `\usepackage{subcaption}` |
| `eqnarray` environment | `align` from amsmath |

## Preferred Packages

| Task | Package | Why |
|------|---------|-----|
| Tables | `booktabs` | Clean horizontal rules, no vertical lines |
| Cross-references | `cleveref` | Auto-prefixed refs: `\cref{fig:x}` produces "Figure 1" |
| Units and numbers | `siunitx` | Consistent formatting: `\num{10000}`, `\SI{3.5}{\micro\metre}` |
| Subfigures | `subcaption` | Modern replacement for subfigure/subfig |
| Maths | `amsmath`, `amssymb` | Standard maths environments and symbols |
| Algorithms | `algorithm2e` or `algorithmicx` | Pseudocode |
| Hyperlinks | `hyperref` | Load last (with few exceptions like `cleveref`) |
| Colours | `xcolor` | Preferred over `color` |
| Code listings | `minted` or `listings` | `minted` preferred if pygments available |

## Tables

- Use `booktabs` exclusively. No vertical rules. No `\hline`.
- Structure: `\toprule`, `\midrule` (after header), `\bottomrule`.
- Align numeric columns on the decimal point with `siunitx` S columns.
- Keep tables narrow; use abbreviations in headers if needed.

```latex
\begin{table}[t]
  \centering
  \caption{Summary of results.}
  \label{tab:results}
  \begin{tabular}{lSS}
    \toprule
    Method & {Accuracy} & {Runtime (s)} \\
    \midrule
    Baseline & 0.72 & 3.2 \\
    Ours     & 0.89 & 4.1 \\
    \bottomrule
  \end{tabular}
\end{table}
```

## Figures

- Use `\centering` inside the float, not `\begin{center}`.
- Vector formats (PDF, SVG) for plots; PNG only for raster images (photos, screenshots).
- Set width relative to text: `width=0.8\textwidth` or `width=\columnwidth`.
- Label immediately after caption: `\caption{...}\label{fig:...}`.

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=0.8\textwidth]{cooperation.pdf}
  \caption{\textbf{Cooperation levels under varying selection.}
    Detailed explanation of what the reader should observe.}
  \label{fig:cooperation}
\end{figure}
```

## Cross-References

- Use `cleveref` with `\cref{}` (lowercase) and `\Cref{}` (start of sentence).
- Define labels immediately after the object: `\caption{...}\label{...}`.
- Label naming convention: `fig:`, `tab:`, `eq:`, `sec:`, `thm:`, `alg:`.
- Never write "Figure~\ref{fig:x}" manually — let `cleveref` handle it.

## Mathematics

- Display maths: `equation` (numbered) or `\[...\]` (unnumbered). Never `$$...$$`.
- Multi-line: `align` (numbered) or `align*`. Never `eqnarray`.
- Define macros for repeated notation: `\newcommand{\E}{\mathbb{E}}`.
- Use `\DeclareMathOperator` for custom operators: `\DeclareMathOperator{\argmax}{arg\,max}`.
- Punctuate displayed equations as part of the sentence.

## Spacing

- Tie references to preceding text with `~`: `in~\cref{fig:x}`, `see~\cref{tab:y}`.
- Use `~` before `\cite`: `shown previously~\cite{Smith2020}`.
- Thin space in maths where appropriate: `\,` (e.g., `\mathrm{d}\,x`).
- Use `\,` for digit grouping in text only if not using `siunitx`.

## Dashes

- Hyphen `-`: compound words (e.g., "well-known").
- En-dash `--`: ranges (e.g., "pages 1--10", "2020--2025").
- Em-dash `---`: parenthetical (use sparingly; prefer commas or semicolons).

## Package Load Order

Load packages in this order (where applicable):
1. Font/encoding packages
2. `amsmath`, `amssymb`
3. `graphicx`, `xcolor`
4. `booktabs`, `siunitx`, `subcaption`
5. `algorithm2e` / `algorithmicx`
6. `hyperref` (near last)
7. `cleveref` (after `hyperref`)

## Things to Avoid

- No vertical rules in tables.
- No manual spacing hacks (`\vspace`, `\hspace`, `\\[12pt]`) unless absolutely necessary.
- No `\newpage` or `\clearpage` in drafts — let LaTeX handle float placement.
- No bitmap figures for plots or diagrams.
- No `\label` before `\caption` (the label will point to the wrong thing).
- No bare `\ref` when `cleveref` is available.
- No `\usepackage[utf8]{inputenc}` with XeLaTeX (it handles UTF-8 natively).
