# Global Claude Instructions

## Core Principles
- Treat `config/` as the source of truth for all parameters and paths — no hardcoded values in scripts.
- Keep orchestration scripts separate from reusable functions.
- Update docs in the same PR that changes code — never defer.

## Canonical Directory Structure

| Directory        | Purpose                        | Rule                                      |
|------------------|-------------------------------|-------------------------------------------|
| `config/`        | Parameters and file paths      | Source of truth. No hardcoded values.     |
| `data/raw/`      | Original input data            | Read-only. Never overwrite.               |
| `data/processed/`| Intermediate/derived data      | Rebuildable; document transformations.    |
| `src/`           | Analysis and utility code      | Separate I/O, transforms, modeling, plots.|
| `workflows/`     | Pipeline entry points          | Batch or local runners for major steps.   |
| `output/`        | Figures, tables, model results | Generated artifacts; never hand-edit.     |
| `logs/`          | Runtime logs and errors        | Capture stdout/stderr for every run.      |
| `docs/`          | Workflow and code documentation| Required for all analysis code.           |

## Scientific Coding
- Validate key assumptions early (sample counts, required columns, value ranges).
- Set and document random seeds for all stochastic methods.
- Keep provenance clear: input source, processing date, and code version in output metadata.
- Use step-ordered naming where applicable (`01_qc`, `02_modeling`, `03_reporting`).

## Documentation
Each major workflow needs a `docs/` page covering: purpose, inputs/schema, parameters, outputs, assumptions, and how to run/validate. Add docstrings to reusable functions; inline comments only where logic is non-obvious.

## Pre-Merge Checklist
- Directory usage follows canonical structure
- All new paths/parameters are config-driven
- Reproducibility details captured (versions, seeds, parameters)
- Tests pass or manual validation is documented
- `docs/` is current for all touched workflows
- `README.md` reflects current structure and run instructions