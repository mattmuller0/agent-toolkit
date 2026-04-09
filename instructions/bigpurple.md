# Copilot Instructions for BigPurple HPC

## System Overview
This guide defines the standard operating procedures for running analysis code on the NYU BigPurple HPC (SLURM managed). Agents and users should follow these patterns to ensure correct environment configuration and job execution.

### System Specifications
- **OS**: Linux (RHEL/CentOS compatible)
- **Scheduler**: SLURM Workload Manager
- **User Identity**: `$USER`
- **Lab Base Paths**: `/gpfs/data/ruggleslab/$USER`
- **Lab Base Paths**: `/gpfs/data/ischemialab/workspace/$USER`
- **Lab Base Paths**: `/gpfs/data/bergerlab/$USER`

## Environment Configuration
The environment is managed via LMOD modules and a centralized Conda installation. **Do not rely on default system paths.**

### 1. Required Modules
Every execution script (interactive or batch) must load these modules:
```bash
module purge
module load slurm
module load git
```

### 2. Interpreter Paths
Use these **absolute paths** for all code execution. Do not use `python` or `Rscript` from the PATH unless explicitly activated.

- **R**:
  ```bash
  /gpfs/data/ruggleslab/$USER/conda_envs/r/bin/Rscript
  ```
- **Python**:
  ```bash
  /gpfs/data/ruggleslab/$USER/${USER}_miniconda/envs/main/bin/python
  ```

### 3. Conda Environment (Reference)
- **Base Path**: `/gpfs/data/ruggleslab/$USER/${USER}_miniconda`
- **Activation**: `source /gpfs/data/ruggleslab/$USER/${USER}_miniconda/etc/profile.d/conda.sh`
- **Default Env**: `r`

## Repository Standards
All projects in this environment follow a strict directory structure.

| Directory | Purpose | Access Strategy |
|-----------|---------|-----------------|
| `config/` | Configuration files (YAML). | **Source of Truth**. Read `config.yml` for all file paths. |
| `data/` | Input data. | **Read-Only**. Split into `raw/` and `processed/`. |
| `output/` | Generated results. | **Write-Only**. Structure by experiment or date. |
| `logs/` | SLURM logs. | Check `*.err` files here for debugging. |
| `src/` | Source code. | Contains all `.R` and `.py` scripts. |
| `workflows/`| Job submission scripts. | Contains `main.sh` and other `sbatch` entry points. |

## Execution Protocols

### Interactive Execution (Short Tasks)
For debugging, data exploration, or tasks under 10 minutes, run directly on the login node using the absolute interpreter path.

```bash
# R Example
/gpfs/data/ruggleslab/$USER/conda_envs/r/bin/Rscript src/my_script.R

# Python Example
/gpfs/data/ruggleslab/$USER/${USER}_miniconda/envs/main/bin/python src/my_script.py
```

### Batch Execution (Production)
For main pipeline steps, long-running analyses, or parallel jobs, use SLURM.

#### Standard Analysis Template (`cpu_medium`)
Use for standard analysis scripts (up to 64GB RAM, 24 hours).

```bash
#!/bin/bash
#SBATCH --job-name=analysis_task
#SBATCH -p cpu_medium
#SBATCH --mem=64GB
#SBATCH --cpus-per-task=4
#SBATCH --time=24:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

set -e

# Load Modules
module purge
module load slurm git

# Execution
# Note: Use absolute path to interpreter
/gpfs/data/ruggleslab/$USER/conda_envs/r/bin/Rscript src/analysis_script.R
```

#### Grid Search / Array Template (`cpu_short`)
Use for many small parallel tasks (up to 16GB RAM, 30 mins).

```bash
#!/bin/bash
#SBATCH --job-name=grid_search
#SBATCH -p cpu_short
#SBATCH --mem=16GB
#SBATCH --cpus-per-task=4
#SBATCH --time=00:30:00
#SBATCH --array=1-100%50
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err

set -e

# Load Modules
module purge
module load slurm git
# Execution
# Pass the array task ID to the script if needed
/gpfs/data/ruggleslab/$USER/conda_envs/r/bin/Rscript src/grid_task.R --task-id $SLURM_ARRAY_TASK_ID
```
