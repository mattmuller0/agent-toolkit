---
name: sbatch-analysis
description: Submit R or Python scripts to SLURM on NYU BigPurple HPC using sbatch. Use this skill whenever the user says "sbatch", "submit to HPC", "run on the cluster", "queue this", or asks to run one or more scripts as a batch job — even casual phrasings like "sbatch both", "submit these", or "now run it" in an HPC context. Also trigger when the user completes an implementation task on BigPurple and immediately asks to run the resulting script(s).
---

## User environment

**User:** `mm12865`

**Lab base paths:**
- `/gpfs/data/bergerlab/mm12865/`
- `/gpfs/data/ruggleslab/mm12865/`
- `/gpfs/data/ischemialab/workspace/mm12865/`

**Conda init:**
```bash
source /gpfs/data/ruggleslab/mm12865/mm12865_miniconda/etc/profile.d/conda.sh
```

**Conda environments:**
- `r` — all R scripts (`Rscript`)
- `main` — Python scripts (`python`)

## Default SLURM resources

| Setting | Default | When to change |
|---------|---------|----------------|
| `--mem` | 32GB | Increase for large data loads, network analysis, or if the user says the job is memory-heavy |
| `--cpus-per-task` | 4 | Match to `mc.cores` / parallel workers if known |
| `-p` | `cpu_medium` | Use `cpu_dev` for ≤30 min / ≤16 GB jobs; `gpu4_long` only if user requests GPU |
| `--time` | `12:00:00` | Long jobs → `24:00:00` or `3-00:00:00` |

## Command pattern

Use `--wrap` for individual script submissions:

```bash
sbatch \
  --job-name=<short_name> \
  --mem=32GB \
  --cpus-per-task=4 \
  -p cpu_medium \
  --time=12:00:00 \
  --output=logs/%x_%j.log \
  --wrap="module purge && module load slurm git && \
    source /gpfs/data/ruggleslab/mm12865/mm12865_miniconda/etc/profile.d/conda.sh && \
    conda activate <env> && \
    Rscript <path/to/script.R>"
```

For Python, replace `conda activate r && Rscript` with `conda activate main && python`.

The `--output` path assumes a `logs/` directory exists in the current working directory. If it doesn't, create it first with `mkdir -p logs`.

## Job naming

Derive a short, readable `--job-name` from the script filename (keep under ~15 chars):
- `incremental_value.R` → `incval`
- `protein_mediation.R` → `prot_med`
- `train_model.py` → `train_model`

## Procedure

1. Identify every script the user wants to submit.
2. Determine the conda environment for each (`r` for R, `main` for Python).
3. Pick resources — use defaults unless the script is known to be heavy or the user specifies otherwise.
4. Run each `sbatch` call. Submit all scripts in the same turn; each gets its own independent `sbatch` command (don't chain with `&&`).
5. Report back with: script name → job ID and log path.

## After submitting

Report job IDs and log paths. No need to suggest monitoring commands unless the user asks.
