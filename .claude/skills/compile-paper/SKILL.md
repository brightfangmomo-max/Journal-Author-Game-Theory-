---
name: compile-paper
description: Compile a LaTeX research paper with XeLaTeX (3 passes + bibtex). Use when compiling papers in the Papers/ directory.
argument-hint: "[filename without .tex extension]"
allowed-tools: ["Read", "Bash", "Glob"]
---

# Compile LaTeX Paper

Compile a research paper using XeLaTeX with full citation resolution.

## Steps

1. **Navigate to Papers/ directory** and compile with 3-pass sequence:

```bash
cd Papers
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode $ARGUMENTS.tex
BIBINPUTS=..:$BIBINPUTS bibtex $ARGUMENTS
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode $ARGUMENTS.tex
TEXINPUTS=../Preambles:$TEXINPUTS xelatex -interaction=nonstopmode $ARGUMENTS.tex
```

**Alternative (latexmk):**
```bash
cd Papers
TEXINPUTS=../Preambles:$TEXINPUTS BIBINPUTS=..:$BIBINPUTS latexmk -xelatex -interaction=nonstopmode $ARGUMENTS.tex
```

2. **Check for warnings:**
   - Grep output for `Overfull \\hbox` warnings
   - Grep for `undefined citations` or `Label(s) may have changed`
   - Report any issues found

3. **Open the PDF** for visual verification:
   ```bash
   open Papers/$ARGUMENTS.pdf          # macOS
   # xdg-open Papers/$ARGUMENTS.pdf    # Linux
   ```

4. **Report results:**
   - Compilation success/failure
   - Number of overfull hbox warnings
   - Any undefined citations
   - PDF page count

## Why 3 passes?
1. First xelatex: Creates `.aux` file with citation keys
2. bibtex: Reads `.aux`, generates `.bbl` with formatted references
3. Second xelatex: Incorporates bibliography
4. Third xelatex: Resolves all cross-references with final page numbers

## Important
- **Always use XeLaTeX**, never pdflatex
- **TEXINPUTS** is required: preamble files live in `Preambles/`
- **BIBINPUTS** is required: `.bib` file lives in the repo root
