# GitHub Copilot Instructions: Project Organization

## Purpose

Use these rules for scientific codebases to keep analyses reproducible, understandable, and easy to maintain.

## Core Principles

- Keep project structure predictable and consistent across workflows.
- Treat configuration as the source of truth for parameters and paths.
- Prefer reproducibility over convenience.
- Keep analysis code modular, testable, and well documented.
- Update documentation as part of the same change that updates code.

## Canonical Repository Structure

| Directory | Purpose | Rule |
|-----------|---------|------|
| `config/` | Parameters and file paths | Source of truth. Avoid hardcoded values in scripts. |
| `data/raw/` | Original input data | Read-only. Never overwrite. |
| `data/processed/` | Derived/intermediate data | Rebuildable artifacts; document transformations. |
| `src/` | Analysis and utility code | Keep orchestration separate from reusable functions. |
| `workflows/` | Pipeline runners (batch or local) | Entry points for major workflows. |
| `output/` | Figures, tables, model results | Regenerated artifacts; do not hand-edit. |
| `logs/` | Runtime logs and errors | Capture stdout/stderr for every workflow run. |
| `docs/` | Code and workflow documentation | Required for all analysis code and major workflows. |

## Code Organization Standards

- Keep top-level analysis scripts focused on orchestration.
- Place reusable functions in `src/utils/` or language-appropriate modules.
- Use descriptive, stable naming (`01_qc`, `02_modeling`, `03_reporting` if step-ordered).
- Separate I/O, transformation, modeling, and plotting logic where practical.
- Avoid hidden side effects; return explicit objects and write outputs in one place.
- Never hardcode external paths, thresholds, or cohort-specific constants in code.

## Scientific Coding Best Practices

- Record package and interpreter versions for every reproducible run.
- Set and document random seeds for stochastic methods.
- Store all analysis parameters in config files and persist run metadata with outputs.
- Validate key assumptions early (sample counts, required columns, missingness, value ranges).
- Fail fast with informative error messages when assumptions are violated.
- Keep provenance clear: identify input data source, processing date, and code version.

## Testing Requirements

- Add tests for all reusable functions and critical workflow logic.
- Cover at minimum: input validation, expected output shape/content, and failure behavior.
- Add regression tests when fixing bugs so the same issue cannot silently reappear.
- Keep tests deterministic (fixed seeds, stable fixtures, explicit tolerances for numeric checks).
- Run affected tests before merge and include test command(s) in the pull request description.
- If a workflow is not test-automated yet, document manual validation steps in `docs/` and add a follow-up task for automation.

## Documentation Requirements

All analysis code must have corresponding documentation in `docs/`.

Minimum expectation:

- One docs page per major workflow script or module group.
- Each docs page includes:
	- Purpose and scientific question
	- Inputs and expected schema
	- Parameters and defaults (with config references)
	- Outputs (files/tables/figures) and where they are written
	- Assumptions, limitations, and failure modes
	- How to run and how to validate success

Code-level documentation:

- Add docstrings for reusable functions.
- Add short comments only where logic is non-obvious.
- Keep function signatures and argument names aligned with docs.

## Workflow Change Policy

When a major workflow changes (new pipeline, removed script, changed outputs, renamed config keys, or reordered execution), update these in the same pull request:

- `instructions/` files affected by the workflow logic
- `README.md` project overview, run instructions, and structure summary
- `docs/` pages for impacted code/workflows

Do not defer documentation updates to a later change.

## Pre-Merge Checklist

- Directory usage follows the canonical structure.
- New or changed code paths are config-driven, not hardcoded.
- Reproducibility details (versions, seeds, parameters) are captured.
- Relevant automated tests pass, or manual validation is documented when automation is not yet available.
- `docs/` contains up-to-date coverage for all touched analysis code.
- `README.md` reflects the current workflow and repository organization.
- Any relevant instruction files are synchronized with new workflow behavior.
