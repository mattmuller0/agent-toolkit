# .github/prompts/simplify.prompt.md

---
description: Simplify and refactor code for readability and maintainability
---

Simplify this code following these principles:

## Remove Complexity
- Extract repeated logic into named functions
- Replace nested conditionals with early returns or guard clauses
- Convert complex boolean expressions into descriptively-named variables
- Remove dead code and unused variables

## Improve Readability
- Rename variables to reflect their purpose, not their type
- Break long functions (>30 lines) into smaller, single-purpose functions
- Replace magic numbers with named constants
- Use list comprehensions only when they remain readable (one level of nesting max)

## Prefer Standard Patterns
- Use built-in functions over manual implementations
- Prefer pandas/tidyverse idioms over explicit loops
- Use context managers for resource handling
- Apply vectorized operations instead of row-wise iteration

## Preserve Behavior
- Do not change function signatures or return types
- Maintain all edge case handling
- Keep error messages and logging intact
- Preserve type hints and docstrings (improve if unclear)

Show the simplified version with brief inline comments explaining non-obvious changes.

$ARGUMENTS