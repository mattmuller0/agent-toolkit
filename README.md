# Agent Toolkit

Reusable agent, prompt, and skill definitions for bioinformatics and cardiovascular multiomics workflows.

This repository is a lightweight toolkit for configuring AI coding and analysis assistants in VS Code style environments.

## Repository Layout

```text
agents/
  bioinformatics.agent.md
  code-reviewer.md
  code.agent.md
  phd-bioinformatics-mentor.md
  statistics.agent.md
  writing.agent.md

instructions/
  bigpurple.instructions.md

prompts/
  simplify.prompt.md
  write_report.prompt.md

skills/
  rmatt/
    skills/
      deseq-analysis/SKILL.md
      enrichment-analysis/SKILL.md
      hazard-ratios-table/SKILL.md
```

## What Each Folder Contains

### `agents/`

Specialized agent profiles for common research tasks.

- `bioinformatics.agent.md`: Method selection and biological interpretation for multiomics analyses.
- `code.agent.md`: Implementation-focused coding agent for R/Python pipelines and debugging.
- `code-reviewer.md`: Post-change quality review agent (correctness, security, maintainability).
- `phd-bioinformatics-mentor.md`: Senior research strategy mentor for PhD-level planning.
- `statistics.agent.md`: Biostatistics and epidemiology modeling support.
- `writing.agent.md`: Scientific writing and editing support for manuscripts and grants.

### `prompts/`

Reusable task prompts.

- `simplify.prompt.md`: Refactor and simplify code while preserving behavior.
- `write_report.prompt.md`: Generate collaborator-friendly analysis summaries from workspace outputs.

### `skills/rmatt/skills/`

Domain-specific procedural skills for `rmatt` workflows.

- `deseq-analysis`: Differential expression workflows and expected outputs.
- `enrichment-analysis`: GSEA and enrichment result generation patterns.
- `hazard-ratios-table`: Cox model hazard ratio table generation and checks.

### `instructions/`

Project-level operating instructions.

- `bigpurple.instructions.md`: BigPurple HPC conventions, environment modules, interpreter paths, and SLURM templates.

## Quick Start

```bash
git clone https://github.com/mattmuller0/agent-toolkit
cd agent-toolkit
bash setup.sh
```

This symlinks agents, commands, and skills into `~/.claude/` and appends the BigPurple instructions to `~/.claude/CLAUDE.md`. Safe to re-run. To update after pulling changes, just `git pull` — symlinks pick up changes automatically.

**Resolving conflicts:** If `setup.sh` reports `[conflict]` for an existing agent file, compare the two versions and delete the one in `~/.claude/agents/` if you want the repo version, then re-run.

### Manual usage (without setup.sh)

1. Choose an agent file from `agents/` that matches your task.
2. Add a reusable prompt from `prompts/` when you want a structured request format.
3. Attach a relevant skill from `skills/rmatt/skills/` for repeatable analysis workflows.
4. Follow `instructions/bigpurple.instructions.md` when running analyses on BigPurple HPC.

## BigPurple HPC Notes

The included BigPurple instruction profile emphasizes:

- Loading modules explicitly (`slurm`, `git`) after `module purge`.
- Using absolute interpreter paths for R and Python.
- Organizing projects with standard folders (`config`, `data`, `output`, `logs`, `src`, `workflows`).
- Running production jobs through SLURM with consistent logging to `logs/`.

## Extending This Toolkit

To add a new capability:

1. Add a new agent profile in `agents/` with clear boundaries and handoff rules.
2. Add prompt templates in `prompts/` for repeatable request styles.
3. Add skill definitions under `skills/<namespace>/skills/<skill-name>/SKILL.md`.
4. Document any environment assumptions under `instructions/`.

Keep files focused, explicit about scope, and consistent with existing frontmatter fields (`name`, `description`, `tools`, `model` where applicable).
