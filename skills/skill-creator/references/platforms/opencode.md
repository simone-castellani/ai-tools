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
---

Skill instructions here.
```

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
- **Write** — Create/overwrite files
- **Edit** — Make targeted edits
- **Bash** — Run shell commands
- **Task** — Spawn subagents
- **WebFetch** — Fetch web content

When creating skills that use these tools, reference them by their OpenCode names.
