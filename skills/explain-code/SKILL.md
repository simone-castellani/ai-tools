---
name: explain-code
description: Explain code clearly to different audiences, from beginners to experienced engineers. Use when a user asks what a piece of code does, how an algorithm works, or wants to understand an unfamiliar codebase.
license: MIT
allowed-tools: Read Grep Glob
---

# Explain Code Skill

Explain code clearly to different audiences, from beginners to experienced engineers.

## Process

1. **Read the code carefully** before explaining it—understand what it does, not just what it looks like.
2. **Identify the audience** and adjust vocabulary and depth accordingly.
3. **Start with the big picture**: what does this code accomplish at a high level?
4. **Walk through the details**: describe each significant step in plain language.
5. **Highlight non-obvious parts**: point out tricky logic, performance trade-offs, or subtle bugs.
6. **Use analogies** when they make abstract concepts concrete.
7. **Provide examples** showing the code in action with sample inputs and outputs where helpful.

## Structure for Explanations

### Overview
One or two sentences describing what the code does and why it exists.

### How It Works
Step-by-step walkthrough of the important logic, avoiding line-by-line narration of obvious code.

### Key Concepts
Explain any language features, algorithms, or design patterns that a reader might not be familiar with.

### Edge Cases & Gotchas
Note any surprising behavior, performance characteristics, or limitations.

### Example
If applicable, show a concrete example with input, execution path, and output.

## Audience Guidance

| Audience | Vocabulary | Depth |
|---|---|---|
| Beginner | Plain English, define jargon | High-level + key steps |
| Intermediate | Standard technical terms | Full walkthrough |
| Expert | Domain-specific shorthand | Focus on non-obvious parts |

## Constraints
- Never fabricate behavior that isn't present in the code.
- If the code is unclear or appears buggy, say so explicitly.
- Prefer short, focused explanations over exhaustive line-by-line commentary.
