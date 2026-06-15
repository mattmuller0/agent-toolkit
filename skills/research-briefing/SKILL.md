---
name: research-briefing
description: >
  Generate a curated PDF research briefing of recently published papers from high-impact journals,
  with 2-3 sentence summaries per paper. Trigger whenever the user asks to run their research
  briefing, find recent papers, create a literature digest, summarize new publications, update
  their reading list, or catch up on cardiovascular/computational biology research. Also trigger
  when journals like Circulation, JACC, JAHA, Nature, Nature Medicine, or Cell are mentioned
  alongside "what's new", "recent papers", or "latest publications". Works as a scheduled
  recurring task. Searches PubMed across multiple journals in parallel, curates the most relevant
  papers, and produces a formatted multi-page PDF with two sections: Cardiovascular Research
  and Methodology Developments.
---

# Research Briefing Skill

## What this skill does

Generates a curated, formatted PDF digest of recently published papers tailored to cardiovascular
and computational biology research. Papers are organized into two sections and accompanied by
2–3 sentence summaries that highlight relevance to the user's research profile.

**User profile (Matt, PhD candidate — computational biology & bioinformatics, NYU):**
- Core focus: cardiovascular genomics, single-cell omics, multi-omics integration, machine learning
  applied to clinical/genomic data, precision medicine
- Adjacent interests: spatial transcriptomics, deep learning for clinical signals (ECG, imaging),
  GWAS/polygenic risk, microbiome-cardiometabolic links, computational methods development
- Journals of primary interest: Circulation family, JACC family, JAHA, Nature, Nature Medicine,
  Nature Cardiovascular Research, Circulation Research, Cell, Science, Nature Genetics

---

## Workflow

### Step 1 — Parallel PubMed Searches

Run all of the following searches **simultaneously** (they are independent). Use a date range of
the past 3–4 months from today's date. Request 8–12 results per search, sorted by pub_date.

```
Search A:  Circulation[journal] AND (cardiovascular OR heart failure OR atrial fibrillation OR coronary)
Search B:  JACC[journal] AND (machine learning OR genomics OR single cell OR computational OR deep learning OR proteomics)
Search C:  "Journal of the American Heart Association"[journal] AND (genomics OR transcriptomics OR multiomics OR bioinformatics OR machine learning)
Search D:  Nature[journal] AND (cardiovascular OR cardiac OR heart) AND (single cell OR genomics OR proteomics OR machine learning)
Search E:  "Nature Medicine"[journal] AND (cardiovascular OR cardiac OR heart failure OR atrial fibrillation OR dyslipidemia OR atherosclerosis)
Search F:  "Nat Cardiovasc Res"[journal] OR "Circ Res"[journal] AND (single cell OR RNA-seq OR multiomics OR GWAS OR proteomics)
Search G:  (cardiovascular OR cardiac OR heart) AND (single cell RNA-seq OR spatial transcriptomics OR scRNA-seq)
Search H:  (deep learning OR transformer OR foundation model) AND (ECG OR electrocardiogram OR cardiac OR cardiovascular) AND (JACC[journal] OR Circulation[journal] OR "Nature Medicine"[journal])
Search I:  (cardiovascular OR cardiac) AND (multiomics OR proteomics OR metabolomics) AND ("Nat Cardiovasc Res"[journal] OR JACC[journal] OR Circulation[journal])
```

Collect all unique PMIDs from all searches.

### Step 2 — Fetch Metadata

Call `get_article_metadata` on all collected PMIDs (batch them in groups of 10–15 to avoid
oversized responses). From each article record, extract:
- Title, journal, first author + last author, publication date
- Abstract (skip papers with `[Abstract not available]`)
- DOI, keywords

### Step 3 — Curate and Categorize

From all fetched papers, select **8–10 for Section I (Cardiovascular Research)** and
**5–7 for Section II (Methodology Developments)**. Prioritize:

**Cardiovascular Research — good candidates:**
- Papers with full abstracts describing novel mechanisms, clinical trials, or translational findings
- Multi-omic or genomic characterizations of cardiac disease (HF, AF, CAD, PAH, cardiomyopathy)
- Papers that use sequencing, proteomics, or computational approaches to study cardiovascular biology
- Review articles in Circulation or JACC that synthesize an important topic relevant to the user's work

**Methodology Developments — good candidates:**
- New computational or experimental methods (sequencing, ML, imaging analysis, statistical frameworks)
- Papers describing novel tools directly applicable to cardiovascular or genomic research
- Foundation models, large-scale atlas papers, or multi-modal integration approaches
- Bias/fairness frameworks for clinical AI or genomics

**Deprioritize:**
- Letters to the editor, errata, and case reports (unless scientifically exceptional)
- Purely clinical procedural studies (device approval postmarketing, surgical technique papers)
  unless they incorporate significant computational or genomic components
- Papers with no abstract available

### Step 4 — Write Summaries

For each selected paper, write a **2–3 sentence summary** that:
1. States the core finding or contribution in specific, technical language appropriate for a
   computational biology PhD audience (use precise terminology — RNA-seq, Mendelian randomization,
   polygenic risk score, scATAC-seq, etc.)
2. Highlights what makes this paper methodologically or biologically significant
3. Notes any direct relevance to the user's research area (multi-omics, cardiovascular genomics,
   ML for clinical data, etc.) — but only if genuinely relevant, not forced

Write summaries as dense, informative prose — not bullet points. Aim for the tone of a
well-written journal club abstract.

### Step 5 — Generate the PDF

Use the bundled script at `scripts/generate_pdf.py`. Call it like this:

```python
python3 <skill_dir>/scripts/generate_pdf.py \
  --output <output_path>/research_briefing_<YYYYMMDD>.pdf \
  --data <path_to_papers_json>
```

The script expects a JSON file with this structure — build it from your curated papers:

```json
{
  "date": "May 06, 2026",
  "section1": [
    {
      "title": "Paper title here",
      "journal_info": "Authors et al.  Journal Name, Month Year  |  Vol. X, No. Y",
      "summary": "2-3 sentence summary here.",
      "doi": "https://doi.org/10.XXXX/XXXXX"
    }
  ],
  "section2": [
    {
      "title": "Paper title here",
      "journal_info": "Authors et al.  Journal Name, Month Year",
      "summary": "2-3 sentence summary here.",
      "doi": "https://doi.org/10.XXXX/XXXXX"
    }
  ]
}
```

For `journal_info`, format it as:
`"LastName A, LastName B et al.  Journal Full Name, Month Year  |  Vol. X, No. Y"`

Omit volume/issue if not available. Use the last author's name too when the senior author
is recognizable (e.g., Broad/MGH lab heads).

### Step 6 — Save and Present

Save the PDF to the outputs folder and present it to the user with a brief summary of what's
inside — how many papers, date range covered, any particularly notable findings.

---

## Handling edge cases

**If PubMed returns no results for a search:** Skip it silently — other searches will cover the
field.

**If metadata batches return oversized outputs:** Fetch in smaller batches of 5–8 PMIDs.

**If very few papers meet the curation criteria:** Lower the bar slightly rather than padding
with poor papers. A shorter, higher-quality briefing is better than a long mediocre one.

**If running as a scheduled task (no user present):** Make all curatorial decisions autonomously.
Prefer papers with full abstracts, prioritize the Broad/MGH/Nature family groups the user follows,
and default to the most recent 90 days.

---

## Output filename convention

`research_briefing_YYYYMMDD.pdf` — use today's date.

---

## Important: PubMed citation requirements

PubMed's terms require that all uses of their data include:
1. Attribution: "Based on articles retrieved from PubMed"
2. DOI links for every paper cited

The PDF generation script handles both automatically. Make sure every paper entry in your JSON
includes a valid `doi` field.
