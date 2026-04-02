---
name: hazard-ratios-table
description: "Build survival hazard ratio tables with the installed rmatt package. Use when users ask for hazard_ratios_table, Cox models, one-vs-rest hazard ratios, subgroup hazard ratios, per-SD standardization, or multi-censor survival summaries."
---

# Hazard Ratios Table (rmatt)

Load rmatt and produce robust Cox hazard ratio summaries with hazard_ratios_table.

## Execute Workflow
1. Confirm inputs and required columns.
- Require a data.frame in data.
- Require condition and censors as character vectors.
- Confirm all listed condition and censor columns exist.

2. Derive and validate time columns.
- Build time variables from censor_prefix and time_prefix.
- Confirm all derived time columns exist before fitting.

3. Apply preprocessing options.
- Standardize numeric predictors when per_sd is true.
- Include controls in the model when controls are supplied.

4. Branch analysis mode.
- Run subgroup recursion first when subgroups is supplied.
- Otherwise run one-vs-rest encoding when ovr is true.
- Otherwise run direct univariate condition-by-censor analyses.

5. Fit and aggregate models.
- Fit Cox models per censor-condition pair.
- Compute hazard ratio, confidence intervals, and p-values.
- Keep proportional hazards test output when available.

## Decision Rules
- Give subgroup logic priority over ovr logic.
- Require numeric conditions for per_sd standardization.
- Use controls only when explicit confounder adjustment is requested.

## Completion Checks
- Confirm output includes: censor, condition, term, n_total, n_event, hazard.ratio, ci.lower, ci.upper, p.value, zph.
- Confirm no missing censor-time pairings.
- Confirm subgroup_var and subgroup_val are present for subgroup analyses.
- Confirm encoded condition terms are present for one-vs-rest analyses.

## Failure Handling
- Continue other subgroup levels when one subgroup fit fails.
- Surface model-fit errors clearly with affected subgroup or term names.
