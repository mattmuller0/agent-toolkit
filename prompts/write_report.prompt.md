---
mode: agent
description: Write a concise, collaborator-friendly report of the analysis performed in the current workspace
---

Write a clear, well-organized analysis report for the project in the current workspace. The audience is **non-computational collaborators** (e.g., wet-lab scientists, clinicians, or PIs) who are familiar with the biology or domain but not with code or computational methods. The report should be **simple, concise, and self-contained**.

## Instructions

1. **Understand the project first** — gather context by reading:
   - Any `README.md` or top-level documentation files
   - Notes, lab notebooks, or changelogs (e.g., `docs/notes.md`, `CHANGELOG.md`)
   - Configuration files that define analysis parameters
   - Any available results files (CSVs, TSVs, summary tables)
   - Directory structure to understand what outputs have been generated

2. **Identify the key elements** before writing:
   - What is the biological or scientific question?
   - What input data were used (sources, formats, conditions/groups)?
   - What methods or tools were applied?
   - What outputs were generated?
   - What are the main findings (even if preliminary)?

3. **Write the report** following the structure below.

---

## Report Structure

### Title
A short, descriptive title reflecting the project's core question and system (e.g., organism, tissue, disease model).

### 1. Overview (2–3 sentences)
What is the biological question? What data were used and what approach was taken? No computational detail — frame it as a scientific hypothesis or goal.

### 2. Data
A short plain-language table or bulleted list covering:
- Each input dataset: who generated it, what it measures, how many samples/cells/subjects, what conditions or groups are present
- Any reference databases or prior networks used

### 3. Approach
One short paragraph per major analysis step or pipeline stage, described in plain language. Focus on **what** was done and **why**, not **how** (no function names, package names, or code). Include the logic behind key design choices (e.g., why two comparison groups, why a particular filtering threshold matters biologically).

### 4. Key Results
Summarize findings organized by the main analysis outputs or biological questions. For each:
- What was found (top hits, clusters, signatures, interactions, etc.)
- Whether results were strong, weak, or pending (be honest about preliminary status)
- Any notable biological interpretation — flag it clearly as interpretation vs. observation

If results files are not yet available, state that the pipeline is pending and describe what outputs will be generated.

### 5. Output Files
A concise table of the main deliverables:

| File | Description |
|------|-------------|
| (list key output files with plain-language descriptions) | |

Pull file names from the actual output directories in the workspace. Group by type if helpful (tables, figures, etc.).

### 6. Interpretation & Next Steps
3–5 bullet points:
- What the results suggest biologically (flag uncertainty where results are preliminary)
- What follow-up experiments or validation steps could be prioritized
- What additional computational analyses are planned or would strengthen the conclusions

### 7. Methods (brief)
One short paragraph suitable for inclusion in a Methods section or grant. Cover:
- Core analytical framework/tool(s) used and their purpose
- Statistical tests and thresholds applied (e.g., DE method, FDR cutoff, fold-change threshold)
- Key filtering criteria and why they matter
- Any quality control steps performed

Write this paragraph in past tense, third person, as it would appear in a manuscript.

---

## Style Guidelines

- Use plain English; spell out acronyms on first use
- Keep each section to 1–3 short paragraphs or a compact table — **brevity is valued**
- Where actual numbers from results files are available, include them; otherwise say "pending"
- Format as **Markdown** so it can be shared as a `.md` file or converted to PDF/Word
- Do **not** include code blocks, function names, or file paths in the main body (only in the Output Files table)
- Avoid hedging language unless genuinely uncertain; be crisp and direct
- End with a one-sentence summary suitable for a collaborator email, prefixed with `> **TL;DR:**`
