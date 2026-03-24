# Git Commit Message Skill

Write clear, informative Git commit messages that follow the Conventional Commits specification and the project's existing conventions.

## Commit Message Format

```
<type>(<scope>): <short summary>

[optional body]

[optional footer(s)]
```

### Types
- `feat` – a new feature
- `fix` – a bug fix
- `docs` – documentation changes only
- `style` – formatting, missing semicolons, etc. (no logic change)
- `refactor` – code restructuring without feature or fix
- `perf` – performance improvement
- `test` – adding or correcting tests
- `chore` – build process, dependency updates, tooling

### Scope (optional)
A noun describing the section of the codebase affected (e.g., `auth`, `api`, `ui`).

### Short Summary
- Imperative mood, present tense: "add feature" not "added feature"
- Start with a lowercase letter
- No period at the end
- 72 characters or fewer

### Body (optional)
- Explain *what* changed and *why*, not *how*
- Wrap lines at 72 characters
- Separate from the summary with a blank line

### Footer (optional)
- Reference issues: `Closes #123`, `Fixes #456`
- Note breaking changes: `BREAKING CHANGE: <description>`

## Process
1. Review the staged diff to understand what changed.
2. Identify the primary type and scope.
3. Write a concise summary that answers "what does this commit do?"
4. Add a body if the change is non-obvious or the reasoning needs explanation.
5. Add footers for issue references or breaking changes.

## Examples

```
feat(auth): add OAuth2 login via GitHub

Users can now authenticate using their GitHub account in addition to
email/password. The OAuth2 flow stores a short-lived session token.

Closes #42
```

```
fix(api): handle empty response body in fetch helper

fetch() resolves with an empty body for 204 No Content responses.
Calling .json() on an empty body threw a SyntaxError. Now we check
the Content-Length header before attempting to parse.
```
