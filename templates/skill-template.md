# Skill Creation Template

**Use this template to create domain-specific skills for your workflow.**

---

## When to Create a Custom Skill

Create a skill when you find yourself:
- Repeatedly explaining the same 3+ step workflow to Claude
- Needing domain-specific quality checks (notation consistency, citation style)
- Enforcing field-specific output formats (journal templates, figure standards)
- Coordinating multi-tool workflows (simulation -> analysis -> figure -> paper)

**Don't create a skill for:**
- One-time tasks
- Workflows that change frequently
- Simple 1-2 step operations

---

## Template Structure

Copy the structure below to `.claude/skills/[your-skill-name]/SKILL.md`:

```markdown
---
name: your-skill-name
description: [What it does] + [When to use it] + [Key capabilities]. Use when user asks for "[trigger phrase 1]", "[trigger phrase 2]", or "[context]".
argument-hint: "[brief hint for user]"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# [Skill Name]

[One sentence: what this skill accomplishes and why it exists]

## Steps

Step 1: [First major action with clear explanation]
   - Detail: [Important consideration]
   - Example: [Concrete example]

Step 2: [Second major action]
   - Detail: [Important consideration]

Step 3: [Final action and verification]
   - Verify: [What to check]
   - Output: [What user receives]

## Examples

### Example 1: [Common Scenario Name]
**Context:** [When this occurs]
**User says:** "[Typical user request]"
**Actions:**
1. [What skill does first]
2. [What skill does second]
3. [Final output]
**Result:** [What user receives]

## Troubleshooting

**Error:** [Common error message or symptom]
**Cause:** [Why this happens]
**Solution:** [How to fix it]
```

---

## Advanced Frontmatter Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `effort` | Override reasoning effort level | `high` (for review skills), `low` (for formatting) |
| `context` | Set to `fork` to run in isolated subagent context | Protects main conversation from verbose output |
| `agent` | Link to an agent definition in `.claude/agents/` | `proofreader` |
| `model` | Force a specific model | `haiku` (cheaper), `opus` (smarter) |

**Dynamic content** -- skills can include live data using string substitutions:

- `$ARGUMENTS` -- full argument string (e.g., `/skill-name arg` -> `arg`)
- `$0`, `$1` -- positional arguments (0-based)
- `${CLAUDE_SKILL_DIR}` -- path to the skill's directory
- `` `!git log --oneline -5` `` -- dynamic command output injected when skill loads

---

## Writing Effective Descriptions

The `description` field determines when Claude loads your skill. Use this structure:

```
[What it does] + [When to use it] + [Key capabilities]
```

### Good Examples

```yaml
description: Reviews Python scripts for scientific computing quality. Use when user asks to "review script", "check code quality", or after writing Python scripts. Checks PEP 8, reproducibility, and figure quality.
```

### Bad Examples

```yaml
description: Helps with code  # Too vague, no trigger phrases
```

---

## Testing Your Skill

1. Create skill directory: `mkdir -p .claude/skills/your-skill-name`
2. Copy SKILL.md template and customize
3. Skills hot-reload automatically -- changes are detected without restarting
4. Trigger skill: Use one of your trigger phrases
5. Verify: Skill loads, instructions are clear, output is correct

### Success Criteria
- Skill triggers on 90%+ of relevant queries
- Complete workflow in expected number of steps
- Same task yields consistent outputs across sessions

---

## Allowed Tools Reference

| Tool | Use For |
|------|---------|
| `Read` | Reading file contents (scripts, papers, data) |
| `Write` | Creating new files (reports, tables, outputs) |
| `Edit` | Modifying existing files in place |
| `Grep` | Searching file contents (citations, function names) |
| `Glob` | Finding files by pattern (*.py, *.tex, *.csv) |
| `Bash` | Running commands (Python, Julia, LaTeX compilation, git) |

**Security note:** Only grant `Bash` access if your skill needs to execute code or compile documents.

---

## Where This Template Lives

- **File:** `templates/skill-template.md`
- **Purpose:** Starter for domain-specific skills
- **Usage:** Copy to `.claude/skills/[name]/SKILL.md`, customize for your domain
