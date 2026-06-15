---
name: multiomics-integration
description: Multi-omics factor analysis and integration workflows using MOFA+, DIABLO, and rmatt
tools: read_file, execute_code, Context7
---

# Multiomics Integration Skill

Use this skill when the user wants to integrate two or more omics data types (e.g., RNA-seq + proteomics + metabolomics) to identify shared latent factors or co-varying features across modalities.

---

## Step 1: Confirm inputs and modalities

Before starting, clarify:
- How many modalities? (2 = DIABLO appropriate; 2+ = MOFA+ appropriate)
- Are samples matched across modalities? (required for both methods)
- Is there a supervised outcome (e.g., case/control, survival)? → DIABLO preferred
- Is discovery/unsupervised the goal? → MOFA+ preferred
- What is the sample size per modality? (<50 → careful with DIABLO; MOFA+ more robust)

---

## Step 2: Choose integration method

| Condition | Method |
|-----------|--------|
| Supervised, 2 modalities, group comparison | DIABLO (mixOmics) |
| Unsupervised, 2+ modalities, factor discovery | MOFA+ |
| Weighted gene co-expression across modalities | WGCNA (within-modality first) |
| rmatt integration wrapper available | Use `rmatt::run_mofa()` or `rmatt::run_diablo()` if available |

---

## Step 3: Preprocess each modality

For each modality:
1. Filter low-variance features (bottom 10–20% by MAD or IQR)
2. Scale/normalize per modality (VST for RNA; log2 + quantile for proteomics/metabolomics)
3. Confirm no batch effects within modality (PCA visual check)
4. Align sample IDs exactly across modalities — mismatches cause silent errors

```r
# Check sample alignment
stopifnot(identical(colnames(rna_mat), colnames(prot_mat)))
```

---

## Step 4: Run integration

### MOFA+ (R interface)

```r
library(MOFA2)

mofa_obj <- create_mofa(list(
  RNA = rna_mat,       # features x samples
  Protein = prot_mat,
  Metabolites = metab_mat
))

mofa_opts <- get_default_model_options(mofa_obj)
mofa_opts$num_factors <- 10  # start with 10, inspect variance explained

mofa_obj <- prepare_mofa(mofa_obj, model_options = mofa_opts)
mofa_obj <- run_mofa(mofa_obj, use_basilisk = TRUE)
```

### DIABLO (mixOmics)

```r
library(mixOmics)

# Tune number of components first
tune_diablo <- tune.block.splsda(
  X = list(RNA = t(rna_mat), Protein = t(prot_mat)),
  Y = outcome_factor,
  ncomp = 3,
  validation = "Mfold", folds = 5, nrepeat = 10
)

diablo_res <- block.splsda(
  X = list(RNA = t(rna_mat), Protein = t(prot_mat)),
  Y = outcome_factor,
  ncomp = tune_diablo$choice.ncomp$WeightedVote["Overall.ER",],
  keepX = tune_diablo$choice.keepX
)
```

---

## Step 5: Evaluate and interpret factors

### For MOFA+:
```r
# Variance explained per factor per modality
plot_variance_explained(mofa_obj, max_r2 = 15)

# Top weights (feature loadings)
get_weights(mofa_obj, views = "RNA", factors = 1, abs = TRUE) |>
  sort(decreasing = TRUE) |> head(20)

# Factor scores per sample (for downstream analysis)
factors_df <- get_factors(mofa_obj, factors = "all")$group1
```

### For DIABLO:
```r
plotIndiv(diablo_res)         # Sample separation
plotVar(diablo_res)            # Variable correlation circle
plotLoadings(diablo_res, comp = 1, contrib = "max")  # Top contributors
```

---

## Step 6: Save outputs

```r
# MOFA+
saveRDS(mofa_obj, "output/mofa_model.rds")
write.csv(factors_df, "output/mofa_factors.csv")
write.csv(get_weights(mofa_obj)$RNA, "output/mofa_weights_rna.csv")

# DIABLO
saveRDS(diablo_res, "output/diablo_model.rds")
write.csv(selectVar(diablo_res, comp = 1)$RNA$value, "output/diablo_loadings_rna.csv")
```

---

## Completion Checks

- [ ] Sample alignment confirmed across modalities before running
- [ ] Variance explained plot reviewed (MOFA+: no single factor dominates unexpectedly)
- [ ] Top-weight features biologically interpretable (cross-check with known CVD markers)
- [ ] Model RDS saved to `output/`
- [ ] Factor/loading CSVs saved to `output/`
- [ ] Integration method choice documented in analysis notes

---

## Failure Handling

- **Mismatched sample IDs**: Stop and fix alignment — do not proceed with partial matches
- **MOFA+ convergence failure**: Reduce `num_factors`, check for modalities with extreme sparsity
- **DIABLO poor classification**: Check `tune_diablo` output; reduce `keepX`; consider whether supervised signal is present at all
- **Too few samples for DIABLO** (<30/group): Default to MOFA+ unsupervised; note limitation
