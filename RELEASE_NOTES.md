# Display v0.1.0 — Latin–Spanish Complexity Bundle

This release packages the distributable artifacts for the paper “Complexity Conservation in Language Evolution: Quantitative Evidence from Latin to Spanish”. It includes generated figures and tables, processed results, and the manuscript with an appendix of sanity checks.

Highlights
- Figures: article development (fig 1), analytical construction shift (fig 2)
- Tables: statistical summary (CSV)
- Processed results: `data/processed/stanza_output.json`
- Manuscript: `paper/manuscript.pdf` and `paper/manuscript.html`
- Build instructions: `paper/PANDOC_CONVERSION.md`
- Minimal code for figures: `code/03_create_figures.py`

What’s Included
- `results/figures/figure1_articles.(pdf|png)`
- `results/figures/figure2_constructions.(pdf|png)`
- `results/tables/statistical_summary.csv`
- `data/processed/stanza_output.json`
- `paper/manuscript.(pdf|html)`
- `paper/PANDOC_CONVERSION.md`
- `code/03_create_figures.py`

Reproduce Figures
1) Python >= 3.9
2) `pip install -r requirements.txt`
3) `python display/latin-spanish-complexity/code/03_create_figures.py`

Key Results (Summary)
- Articles: Latin = 0 → Spanish ≈ 107/1000 words (Kruskal–Wallis p = 0.0007)
- Analytical shift: synthetic (Latin) → analytical (Spanish) (Fisher’s exact 2×2, p = 0.0001)
- Dependency depth: no significant period differences (p = 0.1140)

Cite This Release
- Title: Complexity Conservation in Language Evolution — Latin–Spanish Display Bundle
- Version: display-v0.1.0
- Author: Zach Nielsen
- DOI: (to be minted via Zenodo after enabling GitHub integration)

Related
- Main analysis code repo: https://github.com/nielsenz/Complexity-Conservation-in-Language-Evolution

Notes
- Medieval Latin analytical forms are underdetected by the Classical-trained model; inference for the categorical test is restricted to Classical vs Spanish.
- See the manuscript Appendix A for sanity checks and reproducibility metadata.
