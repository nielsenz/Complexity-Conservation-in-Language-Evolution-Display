# Complexity Conservation in Language Evolution: Latin to Spanish

**Replication code for 'Complexity Conservation in Language Evolution: Preliminary Quantitative Evidence from Latin to Spanish'**

This repository contains the complete replication package for our computational linguistics study testing the complexity conservation hypothesis through analysis of Latin-to-Spanish grammatical evolution.

## Quick Start

```bash
# 1. Clone and setup environment
git clone <repository-url>
cd latin-spanish-complexity

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download Stanza NLP models
python -c "import stanza; stanza.download('la'); stanza.download('es')"

# 4. Run complete analysis pipeline
python code/02_nlp_analysis.py

# 5. Generate figures
python code/03_create_figures.py
```

## Study Overview

This computational study provides quantitative evidence for complexity conservation during Latin-to-Spanish evolution. We analyzed 16 historical texts across three periods:

- **Classical Latin** (7 texts): Caesar, Cicero, Livy, Sallust
- **Medieval Latin** (5 texts): Gregory of Tours, Bede, Isidore, Peregrinatio  
- **Early Spanish** (4 texts): Auto de los Reyes Magos, El Cid, Berceo, Fuero de Peñafiel

### Key Findings

1. **Article Development** (p = 0.0007): Spanish developed systematic article usage (107.018 ± 22.970 per 1000 words) from complete absence in Latin
2. **Analytical Construction Shift** (p = 0.0001): Complete transition from synthetic Latin forms (6,182 instances) to analytical Spanish constructions (22 instances)
3. **Dependency Complexity**: Non-significant patterns across periods (p = 0.1140)

## Repository Structure

```
latin-spanish-complexity/
├── README.md                    # This file
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── data/
│   ├── raw_texts/              # Original historical texts
│   │   ├── classical_latin/    # 7 Classical Latin texts
│   │   ├── medieval_latin/     # 5 Medieval Latin texts
│   │   └── early_spanish/      # 4 Early Spanish texts
│   └── processed/
│       └── stanza_output.json  # NLP processing results
├── code/
│   ├── 01_download_texts.py    # Text collection from web sources
│   ├── 02_nlp_analysis.py      # Main analysis pipeline with statistics
│   └── 03_create_figures.py    # Generate publication figures
├── results/
│   ├── figures/
│   │   ├── figure1_articles.pdf      # Article development chart
│   │   └── figure2_constructions.pdf # Construction shift visualization
│   └── tables/
│       └── statistical_summary.csv   # Key statistical results
└── paper/
    └── manuscript.pdf          # Published manuscript
```

## Requirements

### System Requirements
- Python 3.8+
- 8GB+ RAM (for NLP processing)
- 2GB+ free disk space

### Python Dependencies
```
stanza>=1.5.0        # NLP processing for Latin and Spanish
pandas>=1.3.0        # Data manipulation
numpy>=1.20.0        # Numerical computing  
matplotlib>=3.3.0    # Plotting
seaborn>=0.11.0      # Statistical visualization
scipy>=1.7.0         # Statistical tests
requests>=2.25.0     # Web scraping (for text collection)
beautifulsoup4>=4.9.0 # HTML parsing
```

## Detailed Usage Instructions

### 1. Environment Setup

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download required NLP models (one-time setup)
python -c "import stanza; stanza.download('la'); stanza.download('es')"
```

### 2. Text Collection (Optional)

The repository includes all texts, but you can re-download them:

```bash
python code/01_download_texts.py
```

This script collects historical texts from:
- Perseus Digital Library (Classical Latin)
- Latin Library (Medieval Latin)
- Cervantes Virtual (Early Spanish)

### 3. Main Analysis Pipeline

```bash
python code/02_nlp_analysis.py
```

This comprehensive script:
1. Loads all 16 historical texts
2. Processes texts with Stanza NLP (Latin 'la' and Spanish 'es' models)
3. Extracts complexity metrics:
   - Article development rates (per 1000 words)
   - Analytical vs synthetic construction counts
   - Dependency complexity measures
4. Performs statistical analysis:
   - Kruskal-Wallis H tests for period comparisons
   - Mann-Whitney U tests for pairwise analysis  
   - Fisher's exact tests for categorical data
   - Bootstrap confidence intervals (n=1000)
5. Generates detailed results report

**Expected runtime:** 15-30 minutes (depending on hardware)

### 4. Generate Figures

```bash
python code/03_create_figures.py
```

Creates publication-ready figures:
- **Figure 1**: Article development across periods with error bars and significance
- **Figure 2**: Analytical vs synthetic construction shift
- **Statistical summary table**: Key results in CSV format

## Key Results Replication

The analysis should reproduce these core findings:

### Article Development Analysis
- Classical Latin: 0.000 ± 0.000 articles per 1000 words
- Medieval Latin: 0.000 ± 0.000 articles per 1000 words
- Early Spanish: 107.018 ± 22.970 articles per 1000 words
- **Kruskal-Wallis H = 14.619, p = 0.0007**

### Analytical Construction Shift  
- Classical Latin: 6,182 synthetic, 0 analytical constructions
- Early Spanish: 0 synthetic, 22 analytical constructions
- **Fisher's Exact Test p = 0.0001**

### Statistical Validation
All findings remain significant under Bonferroni correction (α = 0.017):
- Article development: p = 0.0007 < 0.017 ✓
- Construction shift: p = 0.0001 < 0.017 ✓

## Troubleshooting

### Common Issues

**1. Stanza Model Loading Errors**
```bash
# Manually download models if automatic download fails
python -c "import stanza; stanza.download('la', verbose=True)"
python -c "import stanza; stanza.download('es', verbose=True)"
```

**2. Memory Issues**  
- Ensure 8GB+ RAM available
- Close other applications during NLP processing
- Consider processing texts individually if needed

**3. File Encoding Issues**
- All texts are UTF-8 encoded
- If encoding errors occur, check locale settings:
```bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

**4. Missing Dependencies**
```bash
# Update pip and reinstall if packages missing
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Performance Notes

- **NLP Processing**: Latin model trained on Classical texts may show limitations with Medieval Latin
- **Statistical Tests**: Non-parametric methods used due to small historical sample sizes
- **Memory Usage**: Peak memory usage ~6GB during full corpus analysis

## Methodology Validation

### Reproducibility Checklist
- [ ] All 16 texts successfully loaded
- [ ] Stanza models ('la' and 'es') properly initialized  
- [ ] Article detection shows 0 for all Latin texts, >0 for Spanish texts
- [ ] Construction analysis finds 6,182→22 transition pattern
- [ ] Statistical results match published values (±0.001)
- [ ] Figures generate without errors

### Expected Warnings
- Non-parametric test warnings for small samples (expected)
- Medieval Latin processing limitations (documented in paper)
- Bootstrap resampling notifications (normal)

## Data Availability

### Text Sources
All historical texts are sourced from established digital libraries:
- **Classical Latin**: Perseus Digital Library, Latin Library
- **Medieval Latin**: Monumenta Germaniae Historica, Latin Library
- **Early Spanish**: Biblioteca Virtual Miguel de Cervantes, CORDE

### Processing Pipeline
Complete data flow:
1. **Raw texts** → Stanza NLP processing
2. **Linguistic annotations** → Complexity feature extraction  
3. **Feature matrices** → Statistical analysis
4. **Results** → Publication figures and tables

## Citation

If you use this code or data in your research, please cite:

```bibtex
@article{your_paper_2024,
  title={Complexity Conservation in Language Evolution: Preliminary Quantitative Evidence from Latin to Spanish},
  author={Your Name},
  journal={Journal Name},
  year={2024},
  note={Code and data available at: https://github.com/your-repo}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Stanza NLP library developers (Stanford NLP Group)
- Perseus Digital Library and Latin Library for historical texts
- Biblioteca Virtual Miguel de Cervantes for Spanish texts
- CORDE (Real Academia Española) for linguistic data

## Contact

For questions about replication or methodology:
- Email: [your-email]  
- GitHub Issues: [repository-url]/issues

---

**Data last updated:** [Current Date]  
**Analysis version:** 1.0  
**Python version tested:** 3.8-3.11