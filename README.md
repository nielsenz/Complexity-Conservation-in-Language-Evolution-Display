# Latin–Spanish Complexity Display (Distribution)

This directory is the distributable artifact bundle for the paper “Complexity Conservation in Language Evolution: Quantitative Evidence from Latin to Spanish”. It contains the generated figures/tables, processed data, minimal code to regenerate displays, and conversion instructions for building the manuscript.

Contents
- code/: plotting helpers to regenerate figures
- data/
  - processed/stanza_output.json (all summary stats and tests)
  - raw_texts/ (study excerpts used for processing)
- results/
  - figures/figure1_articles.(pdf|png)
  - figures/figure2_constructions.(pdf|png)
  - tables/statistical_summary.csv
- paper/
  - PANDOC_CONVERSION.md (commands to build PDF/HTML from paper.md)
  - manuscript.(pdf|html) — optional; can be rebuilt from paper.md
- requirements.txt — minimal deps for figure regeneration

Provenance
- Source repository: https://github.com/nielsenz/Complexity-Conservation-in-Language-Evolution
- Source version: tag v0.1.0 (commit SHA to build this release is recorded in the main repo tag)

Reproduce Figures
- Python >=3.9, install `requirements.txt`
- Run `python display/latin-spanish-complexity/code/03_create_figures.py`
- Outputs written to `display/latin-spanish-complexity/results/figures/`

Build Manuscript (optional)
- See `display/latin-spanish-complexity/paper/PANDOC_CONVERSION.md`
- Requires Pandoc + XeLaTeX. If `paper.md` is not present here, use the manuscript PDF/HTML from the source repo tag v0.1.0.

Citation
- If sharing this distribution alone, cite the source repo and this display bundle.
- Consider minting a DOI (e.g., Zenodo) for the display-only repo release.

