# Converting to PDF with Pandoc

To generate the professional manuscript PDF, run the following command in this directory:

```bash
pandoc paper.md -o manuscript.pdf \
  --pdf-engine=xelatex \
  --variable geometry:margin=1in \
  --variable fontsize=12pt \
  --variable linestretch=1.5
```

**Note**: Removed `--number-sections` to avoid double numbering since sections are already numbered in the markdown.

## Prerequisites

1. Install Pandoc: https://pandoc.org/installing.html
2. Install XeLaTeX (part of TeX Live or MacTeX)

## Alternative Options

If you don't have XeLaTeX, you can try:

```bash
# Using default LaTeX engine
pandoc paper.md -o manuscript.pdf \
  --variable geometry:margin=1in \
  --variable fontsize=12pt \
  --variable linestretch=1.5 \
  --number-sections

# Or as HTML (then print to PDF from browser)
pandoc paper.md -o manuscript.html \
  --self-contained \
  --css=https://cdn.jsdelivr.net/gh/sindresorhus/github-markdown-css/github-markdown.css
```

The paper.md file is ready for conversion with all corrections applied.