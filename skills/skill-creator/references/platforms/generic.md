# Generic Platform Reference

This document covers using skill-creator with any agent platform that supports markdown-based instructions, or when creating skills following the [Agent Skills standard](https://agentskills.io).

## The Agent Skills Standard

The Agent Skills standard (agentskills.io) defines a portable format for agent instructions that works across multiple platforms:

- **Codex CLI** (OpenAI)
- **OpenCode**
- **Claude Code** (Anthropic)
- **Any LLM with file access**

## Skill Format

A skill is a directory with a `SKILL.md` file:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
└── assets/           # Optional: templates, resources
```

### SKILL.md Structure

```markdown
---
name: skill-name
description: A description of what this skill does and when to use it.
license: Apache-2.0  # optional
compatibility: Requires Python 3.10+  # optional
metadata:  # optional
  author: your-name
  version: "1.0"
---

# Skill Name

Instructions for the agent to follow.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase, hyphens only, 1-64 chars, must match directory name |
| `description` | Yes | What it does and when to trigger, max 1024 chars |
| `license` | No | License name or reference |
| `compatibility` | No | Environment requirements, max 500 chars |
| `metadata` | No | Arbitrary key-value pairs |

## Without Subagent Support

If your platform doesn't support parallel agents:

1. **Run test cases sequentially** — Execute each test prompt yourself
2. **Skip baseline comparisons** — Focus on whether the skill works, not relative improvement
3. **Present results inline** — Show outputs directly in conversation
4. **Get feedback conversationally** — Ask "How does this look?" instead of using the viewer

## Manual Testing Workflow

1. Write the skill
2. Load the SKILL.md into context
3. Execute a test prompt following the skill's instructions
4. Show the result to the user
5. Iterate based on feedback

## Portable Skills

To make skills work across platforms:

1. **Use standard frontmatter** — `name` and `description` only
2. **Avoid platform-specific features** — No `claude -p`, no platform-specific tools
3. **Keep scripts generic** — Python, Bash, or JavaScript that runs anywhere
4. **Document dependencies** — Use `compatibility` field for requirements

## Validation

Use the reference library to validate skills:

```bash
# Install the validator
pip install skills-ref

# Validate a skill
skills-ref validate ./my-skill
```

## Converting to Other Formats

Skills can be adapted to other agent instruction formats:

### OpenAI Assistants / GPTs

Extract the SKILL.md body and use as "Instructions" in the Assistant/GPT configuration. The frontmatter `description` becomes the assistant description.

### Cursor / Windsurf Rules

Copy the SKILL.md body to `.cursorrules` or equivalent. These tools use plain markdown instructions.

### Raw System Prompt

For any LLM, prepend the SKILL.md content to the system prompt.

## Packaging

Package skills as `.skill` files for distribution:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

This creates a portable archive that can be installed on any compatible platform.
