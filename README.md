# ai-tools

A curated collection of AI agents, skills, and tools for use with [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenCode](https://opencode.ai), and other AI coding assistants.

Agents and skills conform to the standards expected by each tool and can be installed into your local environment with a single command using symbolic links, so updates to this repository are picked up automatically.

---

## Contents

### Agents (`agents/`)

Sub-agents in [Claude Code format](https://docs.anthropic.com/en/docs/claude-code/sub-agents) (Markdown with YAML frontmatter). Each agent has a focused role and a restricted tool set.

| Agent | Description |
|---|---|
| `code-reviewer` | Reviews code for quality, style, and best practices |
| `test-writer` | Writes unit, integration, and end-to-end tests |
| `docs-writer` | Creates and updates technical documentation |
| `security-auditor` | Audits code for security vulnerabilities |

### Skills (`skills/`)

Reusable instruction sets in [OpenCode SKILL.md format](https://opencode.ai/docs/config/). Each skill lives in its own subdirectory.

| Skill | Description |
|---|---|
| `git-commit` | Writes Conventional Commits–style commit messages |
| `code-review` | Checklist and guidance for thorough code reviews |
| `explain-code` | Explains code clearly to different audiences |

---

## Installation

Run the install script from the repository root:

```bash
./install.sh
```

This installs all agents and skills for **both Claude Code and OpenCode** at the **user level** (the default).

### Options

| Option | Values | Default | Description |
|---|---|---|---|
| `--tool` | `claude`, `opencode`, `all` | `all` | Which AI tool to install for |
| `--scope` | `user`, `project` | `user` | User-level or current-project-level install |
| `--dry-run` | – | – | Preview changes without applying them |

### Examples

```bash
# Install only Claude Code agents for the current user
./install.sh --tool claude

# Install everything for the current project only
./install.sh --scope project

# Preview what would be installed for OpenCode
./install.sh --tool opencode --dry-run
```

### Install locations

| Tool | Scope | Agents | Skills |
|---|---|---|---|
| Claude Code | user | `~/.claude/agents/` | – |
| Claude Code | project | `.claude/agents/` | – |
| OpenCode | user | `~/.config/opencode/agents/` | `~/.config/opencode/skills/` |
| OpenCode | project | `.opencode/agents/` | `.opencode/skills/` |

Symbolic links are used, so any future changes you pull from this repository are reflected immediately without re-running the installer.

---

## Adding your own agents or skills

1. **Agent**: create a new `.md` file in `agents/` with the required YAML frontmatter (`name`, `description`) and a Markdown system-prompt body. Re-run `./install.sh` to link it.
2. **Skill**: create a new subdirectory under `skills/` containing a `SKILL.md` file. Re-run `./install.sh` to link it.

---

## License

MIT