# Claude Code Platform Reference

This document covers Claude Code-specific details for skill creation and testing.

> **Note**: This is the legacy reference for Claude Code. The skill-creator now supports multiple platforms. See the main SKILL.md for the platform-agnostic workflow.

## Skill Locations

Claude Code reads skills from:

| Scope | Location | Use |
|-------|----------|-----|
| REPO | `$CWD/.claude/skills` | Skills for the current working folder |
| USER | `$HOME/.claude/skills` | Personal skills across all repos |

## Skill Format

Standard SKILL.md with YAML frontmatter:

```markdown
---
name: skill-name
description: When and how to use this skill.
---

Skill instructions here.
```

## Spawning Test Runs

Claude Code supports subagents for parallel execution.

### Using claude -p

For non-interactive test runs:

```bash
claude -p "Execute this task: <prompt>" \
  --skill <path-to-skill>
```

### Using Subagents

From within Claude Code, spawn subagent tasks for parallel test execution.

## Capturing Timing Data

Subagent task completions include `total_tokens` and `duration_ms`. Capture immediately:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

## Description Optimization

Claude Code uses `claude -p` for triggering tests:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id> \
  --max-iterations 5 \
  --verbose
```

## Claude.ai (Web)

In Claude.ai without CLI access:

- No subagents — run test cases sequentially yourself
- Skip baseline runs
- Present results inline in conversation
- Skip quantitative benchmarking
- Skip description optimization (requires CLI)

## Cowork Environment

In Cowork:

- Subagents work, but may timeout — run in series if needed
- No browser — use `--static` for eval viewer
- Feedback downloads as `feedback.json` file
- Description optimization works via `claude -p`

## Updating Existing Skills

1. Preserve the original `name`
2. Copy to `/tmp/skill-name/` if path is read-only
3. Edit and package:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```
