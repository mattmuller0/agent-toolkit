---
name: deseq-analysis
description: "Run and interpret DESeq2 workflows with the installed rmatt package. Use when users ask for deseq_analysis, run_deseq, differential expression, one-vs-rest RNA-seq contrasts, DE summary tables, volcano plots, PCA, or DE-driven GSEA."
---

# DESeq Analysis (rmatt)

Load rmatt and run a reproducible differential expression workflow with deseq_analysis.

## Execute Workflow
1. Confirm the package and objects are ready.
- Load rmatt and confirm DESeq2 class support is available.
- Require dds, conditions, and outpath.
- Treat controls as optional.

2. Validate model variables before fitting.
- Verify each condition column exists in colData(dds).
- Verify each control column exists when controls are provided.
- Remove rows with missing values in model variables before analysis.

3. Branch per condition by level count.
- Use run_deseq path for 2-level conditions.
- Use one-vs-rest path for conditions with more than 2 levels.
- Skip and report conditions with fewer than 2 valid levels.

4. Run optional diagnostics and enrichment.
- Generate PCA only when run_pca is true.
- Trigger enrichment only when run_gsea is true.

5. Persist outputs.
- Ensure outpath and condition subfolders exist.
- Write condition-level result tables and plots.
- Write deseq_analysis_summary.csv at the root outpath.

## Decision Rules
- Choose two-group versus one-vs-rest based on factor level count.
- Use pvalue, pCutoff, and fcCutoff consistently for thresholds and summaries.
- Use normalize_method consistently across PCA and any downstream summaries.

## Completion Checks
- Confirm deseq_analysis_summary.csv exists and is non-empty.
- Confirm each analyzed condition has DE result output.
- Confirm pca_plot.pdf files exist when run_pca is true.
- Confirm enrichment output exists when run_gsea is true.

## Failure Handling
- Report skipped conditions and why they were skipped.
- Report plotting or enrichment failures without dropping successful DE outputs.
