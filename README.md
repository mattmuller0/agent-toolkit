# Agent Toolkit

Reusable agent, prompt, and skill definitions for bioinformatics and cardiovascular multiomics workflows.

This repository is a lightweight toolkit for configuring AI coding and analysis assistants in VS Code style environments.

## Repository Layout

```text
agents/
  bioinformatician.md
  code-reviewer.md
  coder.md
  phd-bioinformatics-mentor.md
  statistician.md
  writer.md

instructions/
  bigpurple.md
  project-organization.md

prompts/
  debug.md
  simplify.md
  write_report.md
  write_reviewer_response.md

skills/
  rmatt/
    deseq-analysis/SKILL.md
    enrichment-analysis/SKILL.md
    hazard-ratios-table/SKILL.md
    multiomics-integration/SKILL.md
```

## What Each Folder Contains

### `agents/`

Specialized agent profiles for common research tasks.

- `bioinformatician.md`: Method selection and biological interpretation for multiomics analyses.
- `coder.md`: Implementation-focused coding agent for R/Python pipelines and debugging.
- `code-reviewer.md`: Post-change quality review agent (correctness, security, maintainability).
- `phd-bioinformatics-mentor.md`: Senior research strategy mentor for PhD-level planning.
- `statistician.md`: Biostatistics and epidemiology modeling support.
- `writer.md`: Scientific writing and editing support for manuscripts and grants.

### `prompts/`

Reusable task prompts.

- `debug.md`: Structured debugging workflow prompt.
- `simplify.md`: Refactor and simplify code while preserving behavior.
- `write_report.md`: Generate collaborator-friendly analysis summaries from workspace outputs.
- `write_reviewer_response.md`: Draft reviewer response letters in a consistent format.

### `skills/rmatt/`

Domain-specific procedural skills for `rmatt` workflows.

- `deseq-analysis`: Differential expression workflows and expected outputs.
- `enrichment-analysis`: GSEA and enrichment result generation patterns.
- `hazard-ratios-table`: Cox model hazard ratio table generation and checks.
- `multiomics-integration`: MOFA+/DIABLO-style multiomics integration workflows.

### `instructions/`

Project-level operating instructions.

- `bigpurple.md`: BigPurple HPC conventions, environment modules, interpreter paths, and SLURM templates.
- `project-organization.md`: Reproducible scientific project structure and documentation requirements.

## Quick Start

```bash
git clone https://github.com/mattmuller0/agent-toolkit
cd agent-toolkit
```

No installer script is required. You can use the files directly from this repository, or create symlinks for your local assistant setup.

### Optional: link files for Copilot

```bash
PROMPTS_DIR="${VSCODE_USER_PROMPTS_FOLDER:-$HOME/Library/Application Support/Code/User/prompts}"
mkdir -p "$PROMPTS_DIR"

ln -sf "$PWD"/agents/*.md "$PROMPTS_DIR"/
ln -sf "$PWD"/prompts/*.md "$PROMPTS_DIR"/
ln -sf "$PWD"/instructions/*.md "$PROMPTS_DIR"/

for skill_dir in "$PWD"/skills/rmatt/*; do
  skill_name="$(basename "$skill_dir")"
  mkdir -p "$HOME/.copilot/skills/$skill_name"
  ln -sf "$skill_dir/SKILL.md" "$HOME/.copilot/skills/$skill_name/SKILL.md"
done
```

### Optional: link files for Claude

```bash
mkdir -p "$HOME/.claude/agents" "$HOME/.claude/prompts" "$HOME/.claude/instructions"

ln -sf "$PWD"/agents/*.md "$HOME/.claude/agents"/
ln -sf "$PWD"/prompts/*.md "$HOME/.claude/prompts"/
ln -sf "$PWD"/instructions/*.md "$HOME/.claude/instructions"/
```

Safe to re-run. To update after pulling changes, run `git pull`; symlinked files will reflect the latest repo state.

### Manual Usage

1. Choose an agent file from `agents/` that matches your task.
2. Add a reusable prompt from `prompts/` when you want a structured request format.
3. Attach a relevant skill from `skills/rmatt/` for repeatable analysis workflows.
4. Follow `instructions/bigpurple.md` when running analyses on BigPurple HPC.

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
3. Add skill definitions under `skills/<namespace>/<skill-name>/SKILL.md`.
4. Document any environment assumptions under `instructions/`.

Keep files focused, explicit about scope, and consistent with existing frontmatter fields (`name`, `description`, `tools`, `model` where applicable).
