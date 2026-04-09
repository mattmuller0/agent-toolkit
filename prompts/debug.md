---
description: "Explain a runtime error from logs and propose a concrete, minimal fix"
name: "Explain Error And Propose Fix"
---
Analyze the provided error context and explain what failed, why it failed, and how to fix it.

User input (arguments):
- Log file path, error snippet, or both
- Optional: command used to run the pipeline/script
- Optional: expected behavior

Instructions:
1. Find the primary failure in the log and quote the key exception message.
2. Trace where the failure originates in the code and configuration.
3. Explain root cause in plain language.
4. Propose the smallest safe fix first.
5. If there are viable alternatives, list them briefly with tradeoffs.
6. Provide exact verification steps and commands to confirm the fix.

Output format:
- Error Summary
- Root Cause
- Proposed Fix
- Verification Steps
- Risks/Follow-ups

Quality bar:
- Prefer evidence from real files in the workspace.
- Reference concrete files and symbols when available.
- Avoid speculative fixes unless clearly labeled as assumptions.
- Keep recommendations aligned with existing project conventions and run environment.