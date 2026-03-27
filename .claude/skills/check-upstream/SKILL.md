---
name: check-upstream
description: "Check upstream pedrohcgs/claude-code-my-workflow for new features and bug fixes to selectively incorporate"
argument-hint: "[optional: --since YYYY-MM-DD]"
allowed-tools: ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "AskUserQuestion"]
---

# Check Upstream for Updates

Compare local infrastructure against `pedrohcgs/claude-code-my-workflow` and selectively adopt changes.

## Constants

- **Upstream repo:** `pedrohcgs/claude-code-my-workflow`
- **Tracking file:** `quality_reports/upstream-sync.md`
- **Infrastructure paths filter:** `.claude/`, `CLAUDE.md`, `templates/`

## Steps

### 1. Read tracking file

Read `quality_reports/upstream-sync.md` to get the last-checked commit SHA and date.

- If the file does not exist, this is the first run. Set `LAST_SHA=""` and `LAST_DATE=""`.
- If `$ARGUMENTS` contains `--since YYYY-MM-DD`, use that date instead of the stored one.

### 2. Query upstream commits

Fetch recent commits from the upstream repo:

```bash
# If we have a date to filter by:
gh api "repos/pedrohcgs/claude-code-my-workflow/commits?since=${LAST_DATE}&per_page=100" --jq '.[].sha'

# If first run with no date:
gh api "repos/pedrohcgs/claude-code-my-workflow/commits?per_page=30" --jq '.[].sha'
```

If no new commits since last check, report "No new upstream changes" and stop.

Record the **newest commit SHA** as `NEW_SHA` for the tracking update.

### 3. Get changed files

For each new commit (commits after `LAST_SHA`), get the list of changed files:

```bash
gh api "repos/pedrohcgs/claude-code-my-workflow/commits/${SHA}" --jq '.files[].filename'
```

- Deduplicate the file list across all commits.
- **Filter to infrastructure paths only:** keep files matching `.claude/**`, `CLAUDE.md`, `templates/**`. Discard everything else (paper content, scripts, data).

If no infrastructure files changed, report "No infrastructure changes upstream" and stop.

### 4. Fetch upstream content

For each changed infrastructure file, fetch the current upstream version:

```bash
gh api "repos/pedrohcgs/claude-code-my-workflow/contents/${FILE_PATH}" --jq '.content' | base64 -d
```

Store the decoded content for comparison.

### 5. Compare with local

For each upstream file, check the local state:

- **New file** (no local equivalent): mark as `NEW`
- **Modified file** (local exists and differs): mark as `MODIFIED`
- **Identical** (local exists and matches): mark as `UNCHANGED` — skip from report
- **Deleted upstream** (file was removed): mark as `DELETED`

### 6. Generate report

Build a summary table and present it. Example format:

```
## Upstream Changes Since [date]

| # | File | Status | Conflict Risk | Summary |
|---|------|--------|--------------|---------|
| 1 | .claude/rules/new-rule.md | NEW | None | New rule for X |
| 2 | .claude/skills/foo/SKILL.md | MODIFIED | High (local edits) | Updated argument handling |
| 3 | templates/bar.md | MODIFIED | Low (no local edits) | Added new section |
```

For MODIFIED files with local differences, prepare a brief diff summary showing key changes.

### 7. Present interactive selection

Use `AskUserQuestion` with `multiSelect: true` to let the user choose which changes to incorporate.

- List each changed file as an option with its status and summary as description.
- Group by risk level if there are many changes.

### 8. Apply selected changes

For each selected item:

- **NEW files:** Write the upstream content directly using `Write`.
- **MODIFIED files (no local version or local matches old upstream):** Write directly.
- **MODIFIED files (local has custom edits):**
  1. Show the user a side-by-side comparison of key differences.
  2. Ask whether to: overwrite with upstream, keep local, or merge manually.
  3. If overwrite: write upstream content. If merge: insert conflict markers at divergent sections.
- **DELETED files:** Ask user whether to delete locally too.

### 9. Update tracking file

Write/update `quality_reports/upstream-sync.md`:

```markdown
# Upstream Sync Tracking

**Upstream:** pedrohcgs/claude-code-my-workflow
**Last checked:** YYYY-MM-DD
**Last commit SHA:** <NEW_SHA>

## History

| Date | Commits checked | Adopted | Skipped |
|------|----------------|---------|---------|
| YYYY-MM-DD | N | X files (list) | Y files (list) |
```

Prepend new entries to the history table (newest first).

### 10. Summary

Report what was done:
- How many commits were checked
- Which files were adopted
- Which files were skipped
- Any conflicts that need manual resolution
