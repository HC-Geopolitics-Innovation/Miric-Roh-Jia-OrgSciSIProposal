# Reference & Style Files

This folder contains supporting style files, the central bibliography database, compilation utilities, and documentation for building the proposal and appendix documents.

## Contents

1. **`P3_References.md`**: Master BibTeX database containing structured citation entries (`@article`, `@techreport`, `@book`) for all works cited across `P1`, `P2`, and `P3`.
2. **`compile_latex.py`**: Automated two-pass LaTeX compiler that compiles `P2`, `main`, and `appendix`, places the output PDFs in `P1.1 - PDFs for Submission/`, and immediately cleans up intermediate auxiliary files.
3. **`README.md`**: This guide describing typography, required packages, and compilation instructions.

---

## Documents Managed

1. **`P2. Org Sci Proposal [Miric, Roh and Jia][PDF].tex`**: Complete merged proposal (Main text + Technical Appendix), formatted in accordance with INFORMS *Organization Science* submission guidelines.
2. **`main.tex`**: Standalone main proposal document (Sections 1–4).
3. **`appendix.tex`**: Standalone technical appendix with empirical demonstration figures and methodological tables.

Compiled output PDFs are automatically generated and deposited into `P - Paper, Writing and Output/P1.1 - PDFs for Submission/`.

---

## Formatting Rule: GitHub Markdown (`P1`) vs. LaTeX Submission (`P2`, `main`, `appendix`)

> [!IMPORTANT]
> **Do NOT replicate the Table of Contents (TOC) or the standalone Abstract from `P1.md` into the LaTeX files.**

- **GitHub Markdown (`P1. Org Sci Proposal [Miric, Roh and Jia][Github Version].md`)**: Features a top-level Executive Abstract and an interactive Table of Contents with hyperlinked section anchors specifically designed for web-based browsing and repository navigation.
- **LaTeX Submission Documents (`P2.tex`, `main.tex`, `appendix.tex`)**: Must strictly follow INFORMS *Organization Science* submission format. The title page immediately opens into Section 1 without a standalone abstract block or Table of Contents, preserving the strict 10-page text limit for the main proposal.

---

## Required Packages

The LaTeX documents compile with standard `pdflatex` (TeX Live / MacTeX) using the following CTAN packages:

| Package | Purpose |
| :--- | :--- |
| `geometry` | Page geometry (1-inch margins) |
| `times` | Standard Times Roman typography |
| `setspace` | Line spacing (`\setstretch{1.15}`) |
| `graphicx` | Figure inclusion and scaling |
| `booktabs` | Professional publication-quality tables (`\toprule`, `\midrule`, `\bottomrule`) |
| `amsmath`, `amssymb` | Mathematical formatting |
| `caption`, `subcaption` | Figure and subfigure caption styling |
| `xcolor` | Hyperlink and alert styling |
| `hyperref` | Embedded hyperlinks and document metadata |

---

## Automated Compilation & Cleanup

To compile all submission documents in two passes (resolving references) and automatically purge all intermediate auxiliary files (`*.aux`, `*.log`, `*.out`, `missfont.log`), run:

```bash
python3 compile_latex.py
```

Or compile a single document directly:

```bash
python3 compile_latex.py "main.tex"
```
