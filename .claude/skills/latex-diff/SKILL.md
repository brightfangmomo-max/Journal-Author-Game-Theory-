---
name: latex-diff
description: Generate a PDF showing tracked changes between two git revisions of a LaTeX paper using git-latexdiff. Use after editing sessions to review what changed.
argument-hint: "[filename without .tex] [OLD_REV (default: HEAD~1)] [NEW_REV (default: working dir)]"
allowed-tools: ["Read", "Bash", "Glob"]
---

# LaTeX Diff

Generate a colour-coded PDF showing additions and deletions between two revisions of a paper, using `git-latexdiff`.

## Parse Arguments

`$ARGUMENTS` may be:
- `paper` — diff the last commit against the working directory
- `paper HEAD~3` — diff 3 commits ago against working directory
- `paper HEAD~5 HEAD` — diff between two specific commits
- `paper abc123 def456` — diff between two commit hashes

Defaults: OLD = `HEAD~1`, NEW = `--` (working directory).

## Steps

1. **Identify the file and revisions:**

```bash
# Parse arguments (adapt from $ARGUMENTS)
FILE="$1"       # e.g. "paper" (without .tex)
OLD="${2:-HEAD~1}"
NEW="${3:---}"   # "--" means working directory
```

2. **Run git-latexdiff from the repo root:**

```bash
cd /path/to/repo/root

# If comparing against working directory (NEW is "--"):
TEXINPUTS=Preambles:$TEXINPUTS BIBINPUTS=.:$BIBINPUTS \
  git-latexdiff \
    --xelatex \
    --run-bibtex \
    --main Papers/${FILE}.tex \
    --ln-untracked \
    -o Papers/${FILE}_diff.pdf \
    "$OLD" --

# If comparing two commits:
TEXINPUTS=Preambles:$TEXINPUTS BIBINPUTS=.:$BIBINPUTS \
  git-latexdiff \
    --xelatex \
    --run-bibtex \
    --main Papers/${FILE}.tex \
    -o Papers/${FILE}_diff.pdf \
    "$OLD" "$NEW"
```

Key flags:
- `--xelatex`: match our standard compiler
- `--run-bibtex`: ensure bibliography resolves
- `--main`: specify the paper file explicitly
- `--ln-untracked`: include uncommitted files (figures, preambles)
- `-o`: save the diff PDF alongside the paper

3. **Open the diff PDF:**

```bash
open Papers/${FILE}_diff.pdf    # macOS
```

4. **Report results:**
   - Confirm diff PDF was generated
   - Report the revisions compared (show `git log --oneline` for the range)
   - Note the output file location
   - Flag if compilation produced warnings

## Troubleshooting

- If compilation fails, try without `--run-bibtex` (bibliography changes can confuse latexdiff).
- If preamble files are not found, check that `TEXINPUTS` is set correctly relative to the temp directory. Use `--verbose` to debug.
- If the diff is too noisy (e.g., after reformatting), use `--whole-tree` to ensure all files are available.

## Important

- **Always use `--xelatex`** — never pdflatex.
- **TEXINPUTS and BIBINPUTS must be set** so preambles and bibliography resolve.
- The diff PDF is not committed — it is a transient review artifact.
- Add `*_diff.pdf` to `.gitignore` if not already present.
