# LaTeX Style Files & Compilation Environment

This folder contains supporting style files, compilation utilities, and documentation for building the proposal and appendix PDF documents.

## Documents Managed

1. **`P2. Org Sci Proposal [Miric, Roh and Jia][PDF].tex`**: Complete merged proposal (Main text + Technical Appendix), formatted in accordance with INFORMS *Organization Science* submission guidelines.
2. **`main.tex`**: Standalone main proposal document (Sections 1–4).
3. **`appendix.tex`**: Standalone technical appendix with empirical demonstration figures and methodological tables.

Compiled output PDFs are automatically generated and deposited into `P - Paper, Writing and Output/P1.1 - PDFs for Submission/`.

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
