---
name: code-review
description: Conduct thorough, actionable code reviews that improve code quality and knowledge sharing. Use when reviewing a pull request, a set of changed files, or any code submitted for feedback.
license: MIT
allowed-tools: Read Grep Glob Bash
---

# Code Review Skill

Conduct thorough, actionable code reviews that improve code quality and knowledge sharing.

## Review Checklist

### Correctness
- [ ] Does the code do what it claims to do?
- [ ] Are all edge cases handled (empty collections, null/undefined, overflow)?
- [ ] Are errors caught and handled appropriately?
- [ ] Are there off-by-one errors in loops or index operations?
- [ ] Is concurrent code free of race conditions?

### Security
- [ ] Is all external input validated and sanitised?
- [ ] Are secrets kept out of logs and source code?
- [ ] Does the code avoid known vulnerable patterns (SQL injection, XSS, path traversal)?
- [ ] Are permissions and access controls applied correctly?

### Readability & Maintainability
- [ ] Are variable, function, and class names clear and consistent with the codebase?
- [ ] Is the code free of unnecessary comments that just restate the code?
- [ ] Are complex sections explained with a *why* comment?
- [ ] Does the code follow the project's style guide?

### Design
- [ ] Is the change small and focused, or does it mix unrelated concerns?
- [ ] Is there unnecessary duplication that should be extracted?
- [ ] Are abstractions at the right level (not over-engineered, not under-engineered)?
- [ ] Are dependencies on external services or heavy modules minimised?

### Tests
- [ ] Are new features covered by tests?
- [ ] Do existing tests still pass?
- [ ] Do tests cover the most important edge cases?

## Feedback Tone
- Be specific: point to line numbers or file names.
- Explain *why* something is an issue, not just that it is.
- Distinguish between blocking issues and suggestions.
- Acknowledge good work where you see it.

## Severity Labels
Use these prefixes when commenting to signal urgency:
- `[blocking]` – must be fixed before merge
- `[suggestion]` – would improve the code but is optional
- `[nit]` – minor style or cosmetic issue
- `[question]` – genuine uncertainty; requires clarification
