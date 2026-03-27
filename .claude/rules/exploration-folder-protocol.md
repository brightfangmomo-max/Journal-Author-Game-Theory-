---
paths:
  - "explorations/**"
---

# Exploration Folder Protocol

**All experimental work goes into `explorations/` first.** Never directly into production folders.

## Naming Convention

Use **chronological naming**: `YYYY-MM-DD_short-description`. Experiments evolve unpredictably — date-based names avoid misleading logical groupings and sort naturally.

Examples: `2026-03-24_selection-strength-sweep`, `2026-04-01_network-reciprocity-test`.

## Folder Structure

```
explorations/
├── ACTIVE_PROJECTS.md
├── YYYY-MM-DD_description/
│   ├── README.md          # Goal, status, findings
│   ├── run_all.py         # Driver script (see reproducibility-protocol)
│   ├── python/            # Python scripts
│   ├── julia/             # Julia scripts
│   ├── output/            # Results
│   └── SESSION_LOG.md     # Progress notes
└── ARCHIVE/
    ├── completed_YYYY-MM-DD_description/
    └── abandoned_YYYY-MM-DD_description/
```

## Lifecycle

1. **Create** -- `mkdir -p explorations/YYYY-MM-DD_name/{python,julia,output}` + README from `templates/exploration-readme.md`
2. **Develop** -- work entirely within the exploration folder
3. **Decide:**

   - **Graduate to production** -- copy to `scr/`; requires quality >= 80, code runs, code clear. Move to `ARCHIVE/completed_[project]/`
   - **Keep exploring** -- document next steps in README
   - **Abandon** -- move to `ARCHIVE/abandoned_[project]/` with explanation (use `templates/archive-readme.md`)

## Graduate Checklist

- [ ] Quality score >= 80
- [ ] All scripts run without errors
- [ ] Results replicate with same seed
- [ ] Code is clear without deep context
- [ ] README explains approach and findings
