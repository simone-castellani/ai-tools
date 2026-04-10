# AI Skills Collection

This repository hosts a curated collection of reusable agent skills for other projects, compatible with OpenCode, Claude Code, and the standard [Agent Skills](https://agentskills.io) format.

Each skill lives in `skills/<skill-name>/` and includes at least one `SKILL.md` file.

## Available Skills

| Skill | Description |
|---|---|
| `c4-architecture` | Generates architecture documentation with Mermaid C4 diagrams. |
| `code-review` | Runs structured, actionable code reviews on changed files or pull requests. |
| `commit-work` | Helps prepare clean Git commits with clear boundaries and Conventional Commit messages. |
| `difficult-workplace-conversations` | Provides a framework for handling difficult workplace conversations. |
| `doc-coauthoring` | Guides collaborative writing for documentation, RFCs, proposals, and technical specs. |
| `docx` | Creates, reads, edits, and converts Word `.docx` documents. |
| `explain-code` | Explains code and codebases clearly, adapting depth and language to the audience. |
| `humanizer` | Rewrites text to make it sound less artificial and more natural. |
| `msg-to-md` | Converts Outlook `.msg` emails to Markdown with metadata and attachments. |
| `pptx` | Creates, reads, and edits PowerPoint `.pptx` presentations. |
| `skill-creator` | Helps create, improve, and evaluate new skills. |
| `writing-clearly-and-concisely` | Improves technical and non-technical writing by making it clearer and more concise. |

## Install With npx

The recommended way to install these skills is with [`npx skills`](https://www.npmjs.com/package/skills), so you can install them directly from the repository without cloning it manually.

To list the available skills first:

```bash
npx skills add simone-castellani/ai-tools --list
```

### Install All Skills

```bash
# Claude Code, project scope
npx skills add simone-castellani/ai-tools --skill '*' -a claude-code

# Claude Code, user scope
npx skills add simone-castellani/ai-tools --skill '*' -a claude-code -g

# OpenCode, project scope
npx skills add simone-castellani/ai-tools --skill '*' -a opencode

# OpenCode, user scope
npx skills add simone-castellani/ai-tools --skill '*' -a opencode -g

# Both agents
npx skills add simone-castellani/ai-tools --skill '*' -a claude-code -a opencode
```

Non-interactive installation:

```bash
npx skills add simone-castellani/ai-tools --skill '*' -a claude-code -a opencode -y
```

### Install A Specific Skill

To install a single skill, use `--skill <skill-name>`. Valid names match the directories under `skills/`.

```bash
# A specific skill for Claude Code
npx skills add simone-castellani/ai-tools --skill code-review -a claude-code

# A specific skill for OpenCode
npx skills add simone-castellani/ai-tools --skill docx -a opencode

# A specific skill at user scope
npx skills add simone-castellani/ai-tools --skill humanizer -a claude-code -g

# The same skill on multiple agents
npx skills add simone-castellani/ai-tools --skill writing-clearly-and-concisely -a claude-code -a opencode
```

## Manual Installation

If you prefer to keep a local clone of the repository and use symbolic links, you can install a skill manually by linking to its directory.

### Claude Code

User scope:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/<nome-skill>" ~/.claude/skills/<nome-skill>
```

Project scope:

```bash
mkdir -p .claude/skills
ln -s "$(pwd)/skills/<nome-skill>" .claude/skills/<nome-skill>
```

### OpenCode

User scope:

```bash
mkdir -p ~/.config/opencode/skills
ln -s "$(pwd)/skills/<nome-skill>" ~/.config/opencode/skills/<nome-skill>
```

Project scope:

```bash
mkdir -p .agents/skills
ln -s "$(pwd)/skills/<nome-skill>" .agents/skills/<nome-skill>
```

## Updates

If you use `npx skills`, you can check for and apply updates with:

```bash
npx skills check
npx skills update
```

If you use symbolic links to a local clone of the repository, updates are picked up automatically after a `git pull`.

## Add A New Skill

1. Create a new directory under `skills/`.
2. Add a `SKILL.md` file.
3. Include YAML frontmatter with at least `name` and `description`.

Minimal example:

```md
---
name: my-skill
description: When and why to use this skill.
---

Skill instructions.
```

## Repository Structure

```text
skills/
  <skill-name>/
    SKILL.md
    README.md
    references/
    scripts/
    assets/
```

## Resources

- [Agent Skills Specification](https://agentskills.io)
- [skills](https://www.npmjs.com/package/skills)
- [OpenCode Skills Documentation](https://opencode.ai/docs/skills)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)

## License

MIT
