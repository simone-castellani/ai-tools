# Codex CLI Platform Reference

This document covers Codex CLI-specific details for skill creation and testing.

## Skill Locations

Codex reads skills from these locations (in order of precedence):

| Scope | Location | Use |
|-------|----------|-----|
| REPO | `$CWD/.agents/skills` | Skills for the current working folder |
| REPO | `$CWD/../.agents/skills` | Skills in parent folders (within repo) |
| REPO | `$REPO_ROOT/.agents/skills` | Root skills for the entire repo |
| USER | `$HOME/.agents/skills` | Personal skills across all repos |
| USER | `$HOME/.codex/skills` | Alternative personal location |
| ADMIN | `/etc/codex/skills` | Machine-wide admin skills |
| SYSTEM | Bundled with Codex | Built-in skills |

Codex follows symlinks when scanning skill directories.

## Skill Format

Codex uses the [Agent Skills standard](https://agentskills.io). Additionally, Codex supports an optional `agents/openai.yaml` file for UI metadata:

```yaml
interface:
  display_name: "User-Facing Name"
  short_description: "Brief user description"
  icon_small: "./assets/small-logo.svg"
  icon_large: "./assets/large-logo.png"
  brand_color: "#3B82F6"
  default_prompt: "Optional prompt wrapper"

policy:
  allow_implicit_invocation: false  # default: true

dependencies:
  tools:
    - type: "mcp"
      value: "some-mcp-server"
      description: "MCP server description"
      transport: "streamable_http"
      url: "https://example.com/mcp"
```

## Spawning Test Runs

Codex supports subagents for parallel test execution.

### Using the Codex CLI

For non-interactive test runs:

```bash
codex -p "Execute this task: <prompt>" \
  --skill <path-to-skill> \
  --output-dir <workspace>/iteration-N/eval-ID/with_skill/outputs/
```

### Using Subagents (from within Codex)

If you're running inside Codex and have subagent support:

```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about>
```

Launch with-skill and baseline runs in the same turn for parallel execution.

## Capturing Timing Data

When a subagent task completes, Codex provides `total_tokens` and `duration_ms` in the task notification. Save immediately — this data isn't persisted elsewhere:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

## Description Optimization

Codex uses `codex -p` for description optimization. Run the optimization loop:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id> \
  --max-iterations 5 \
  --verbose
```

Use the model ID powering your current session so triggering tests match actual behavior.

## Installing and Managing Skills

```bash
# Install a skill
$skill-installer <skill-name>

# List available skills
codex /skills

# Invoke a skill explicitly
$<skill-name>
```

## Enable/Disable Skills

In `~/.codex/config.toml`:

```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

Restart Codex after config changes.

## Headless / No Display

If running without a browser:

```bash
python <skill-creator-path>/eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-N/benchmark.json \
  --static <output_path>
```

This generates a standalone HTML file. User clicks "Submit All Reviews" to download `feedback.json`.

## Updating Existing Skills

1. Preserve the original `name` field — don't rename
2. Copy to a writable location if the installed path is read-only
3. Edit, test, then package:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```
