# OpenCode Platform Reference

This document covers OpenCode-specific details for skill creation and testing.

## Skill Locations

OpenCode reads skills from:

| Scope | Location | Use |
|-------|----------|-----|
| REPO | `$CWD/.agents/skills` | Skills for the current working folder |
| USER | `$HOME/.agents/skills` | Personal skills across all repos |
| USER | `$HOME/.opencode/skills` | Alternative personal location |

Skills use the standard SKILL.md format with YAML frontmatter.

## Skill Format

OpenCode uses the same format as the [Agent Skills standard](https://agentskills.io):

```markdown
---
name: skill-name
description: When and how to use this skill.
allowed-tools:  # optional OpenCode extension
  - Read
  - Bash
---

Skill instructions here.
```

`name` and `description` are the portable core. OpenCode also supports the
optional `allowed-tools` extension when a skill should advertise the workspace
tools it expects to use.

## OpenCode Frontmatter Extension

`allowed-tools` may be written as either:

- a single string: `allowed-tools: Read Bash`
- a YAML list of strings

For readability in docs, prefer Title Case names. Validation also accepts the
canonical lowercase ids used by the runtime.

### Supported Tool Names

| Human-readable | Canonical id |
|----------------|--------------|
| `Read` | `read` |
| `Glob` | `glob` |
| `Grep` | `grep` |
| `Bash` | `bash` |
| `Task` | `task` |
| `WebFetch` | `webfetch` |
| `Skill` | `skill` |
| `Question` | `question` |
| `ApplyPatch` | `apply_patch` |
| `TodoWrite` | `todowrite` |

### Accepted Aliases

- `AskUserQuestion` is accepted as a compatibility alias for `Question`
- Lowercase forms such as `read` or `apply_patch` are also valid

Do not use Claude-specific tool names like `create_file` or `str_replace` in
OpenCode skills. They are not OpenCode tools.

## Spawning Test Runs

OpenCode uses the Task tool for subagent-style parallel execution.

### Using the Task Tool

From within OpenCode, spawn test runs using the Task tool with `subagent_type: general`:

**With-skill run:**
```
Task(
  description="Run eval with skill",
  prompt="Execute this task:
    - Skill path: <path-to-skill>
    - Task: <eval prompt>
    - Input files: <eval files if any>
    - Save outputs to: <workspace>/iteration-N/eval-ID/with_skill/outputs/
    - Outputs to save: <what the user cares about>",
  subagent_type="general"
)
```

**Baseline run:**
```
Task(
  description="Run eval without skill",
  prompt="Execute this task:
    - Task: <eval prompt>
    - Input files: <eval files if any>
    - Save outputs to: <workspace>/iteration-N/eval-ID/without_skill/outputs/
    - Outputs to save: <what the user cares about>",
  subagent_type="general"
)
```

Launch both in the same turn for parallel execution.

### Specialized Agents

OpenCode provides specialized agent types:

- `general` — General-purpose agent for multi-step tasks
- `explore` — Fast codebase exploration

Use `general` for skill test runs.

## Capturing Timing Data

Task tool completions include timing info. When a task completes, save to `timing.json`:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

## Loading Skills

OpenCode loads skills via the `skill` tool:

```
<invoke name="skill">
  <parameter name="name">skill-name</parameter>
</invoke>
```

Skills are loaded automatically when they match the task based on description.

## Headless / No Display

When no browser is available, generate static HTML:

```bash
python <skill-creator-path>/eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-N/benchmark.json \
  --static <output_path>
```

User clicks "Submit All Reviews" to download `feedback.json`.

## Description Optimization

If OpenCode has CLI/non-interactive mode, use it for description testing. Otherwise, test triggering manually by presenting queries and checking if the skill loads.

Manual approach:
1. Create test queries (should-trigger and should-not-trigger)
2. For each query, note whether the skill was loaded
3. Adjust description based on misses

## Updating Existing Skills

1. Preserve the original `name` field
2. Copy to a writable location if needed
3. Edit, test, then package:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

## OpenCode-Specific Features

OpenCode provides these tools that may be useful during skill creation:

- **Read** — Read files
- **Glob** — Find files by pattern
- **Grep** — Search file contents
- **Bash** — Run shell commands
- **Task** — Spawn subagents
- **WebFetch** — Fetch web content
- **Skill** — Load another skill
- **Question** — Ask the user a short structured question
- **ApplyPatch** — Edit files safely
- **TodoWrite** — Track multi-step work

When creating skills that use these tools, prefer the Title Case names above in
docs and `allowed-tools`.
