---
name: enrichment-analysis
description: "Run enrichment analysis workflows with the installed rmatt package. Use when users ask for gsea_analysis, rna_enrichment, save_gse outputs, custom gene sets, pathway enrichment, overrepresentation, or DE result enrichment reporting."
---

# Enrichment Analysis (rmatt)

Load rmatt and produce pathway enrichment outputs from ranked genes or DE tables.

## Execute Workflow
1. Prepare input signal.
- Build a named numeric ranked vector from DE output with get_fc_list when needed.
- Validate fold-change column and gene identifier names.

2. Choose enrichment mode.
- Use gsea_analysis for ranked-list GSEA across GO, Hallmark, Reactome, and KEGG.
- Use rna_enrichment for GO-style enrichment with default gseGO behavior.
- Use stratified_overrepresentation for directional up-versus-down overrepresentation.

3. Resolve identifier strategy.
- Detect keyType automatically when keyType is missing.
- Confirm keyType compatibility before running.
- Include custom gene sets only when keyType supports SYMBOL mapping.

4. Save outputs consistently.
- Create outpath before running.
- Save tables as CSV and objects as RDS.
- Save visual outputs through save_gse.

## Decision Rules
- Choose function path by input shape: ranked vector versus directional gene table.
- Use species and ontology settings explicitly when the user requests non-default biology scope.
- Treat empty-significance outputs as informative results, not hard failures.

## Completion Checks
- Confirm CSV and RDS outputs exist in outpath.
- Confirm expected collection subfolders exist for gsea_analysis runs.
- Confirm plotting output is compatible with returned enrichment object class.

## Failure Handling
- Report unsupported object classes without crashing the session.
- Continue writing available outputs when individual plot renders fail.
