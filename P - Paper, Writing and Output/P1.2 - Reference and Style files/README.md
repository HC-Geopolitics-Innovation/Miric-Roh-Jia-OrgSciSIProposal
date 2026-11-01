# Reference & Style Files

This folder contains supporting style files, the master BibTeX database, automated compilation utilities, and typography/formatting documentation for building the proposal and technical appendix submission documents.

## Contents

1. **`P3_References.md`**: Master BibTeX database containing structured citation entries (`@article`, `@techreport`, `@book`) for all works cited across `P1`, `P2`, and `P3`.
2. **`compile_latex.py`**: Automated two-pass LaTeX compiler that compiles `P2`, `main`, and `appendix`, deposits the output PDFs in `P1.1 - PDFs for Submission/`, and immediately cleans up all intermediate auxiliary files.
3. **`README.md`**: This guide describing typography, required packages, compilation instructions, and formatting rules.

---

## Documents Managed

1. **`P2. Org Sci Proposal [Miric, Roh and Jia][PDF].tex`**: Complete merged proposal (Main text + Technical Appendix), formatted in accordance with INFORMS *Organization Science* submission guidelines.
2. **`main.tex`**: Standalone main proposal document (Sections 1–4 and References).
3. **`appendix.tex`**: Standalone technical appendix with empirical demonstration figures and methodological tables.

Compiled output PDFs are automatically generated and deposited into `P - Paper, Writing and Output/P1.1 - PDFs for Submission/`.

---

## Submission Formatting & Typography Rules

The LaTeX documents adhere to the following publication and submission rules:

### 1. Typography & Fonts
- **Font Family**: Garamond-type typeface via `\usepackage{ebgaramond}` (accompanied by `amsmath` and `amssymb` for mathematical notation).
- **Line Spacing**: Set to 1.15 line pitch via `\usepackage{setspace}` and `\setstretch{1.15}`.
- **Margins**: Strictly set to 1-inch (72pt) margins on all sides via `\usepackage[margin=1in]{geometry}`.

### 2. Paper Titles & Structure
- **Main Document Title**: Formatted in unbolded Small Caps (`\LARGE \textsc{...}`), without bolding (`\bfseries` omitted).
- **Omission of Table of Contents**: The LaTeX submission documents strictly **omit the Table of Contents (TOC)** and the standalone Abstract block. The document opens directly into Section 1 on the title page, adhering to the 10-page text limit. (The interactive Table of Contents and Executive Abstract are reserved exclusively for the GitHub repository markdown version `P1.md`).
- **Technical Appendix Header**: Centered banner with `{\huge \textsc{Technical Appendix}\par}` placed in a larger font directly above the paper title. The paper title below it retains the exact same small-caps font style (`\Large \textsc{...}`) as used throughout the rest of the document.

### 3. Major Section Numbering Alignment
- For major section titles (`\section`), the section numbering (e.g., `1.`, `2.`, `3.`, `4.`) is placed before the text using a hanging outdent into the margin (`\llap{\thesection.\hspace{0.8em}}`).
- This guarantees that the title text itself aligns perfectly with the start of the body text column (flush with the left margin).

### 4. Figure Rendering & Styling Rules
All figures in the manuscript and technical appendix strictly conform to three rendering standards:
1. **Title Above Figure**: Every figure title (`\caption{...}`) is placed **above** the graphic, not below it.
2. **Unbolded Captions**: Caption labels and titles are unbolded (`\captionsetup[figure]{labelfont=normalfont,textfont=normalfont,position=top,skip=6pt}`).
3. **Thin Black Border**: Every figure and sub-panel graphic is framed with a thin black box outline:
   ```latex
   \setlength{\fboxsep}{0pt}%
   \setlength{\fboxrule}{0.4pt}%
   \fbox{\includegraphics[...]{...}}
   ```
4. **Figure Notes**: Placed immediately below the boxed image in footnotesize italicized text (`{\footnotesize\textit{Notes: ...}\par}`).

---

## Complete Figure Catalog

All figures are organized in `R - Results/R1.1 - Figures/` by pipeline stage and dynamically resolved via `\graphicspath`:

| Figure | Description | Panels & Canonical Source Files (in `R - Results/R1.1 - Figures/`) |
| :--- | :--- | :--- |
| **Figure 1** | Cosine Similarity across Committees | `R1.1.2 - T - Three Step Text Analysis Pipeline/R1.1.2.1 - T1 - Text Summarization/1 - Figure 1 - Cosine Similarity Between Hand-Coded and LLM Summaries.png` |
| **Figure 2** | Topics and Policymaker Stance (4-Panel) | `R1.1.2 - T - Three Step Text Analysis Pipeline/R1.1.2.2 - T2 - Classification/1 - Figure 2 - Topics and Overview of Stance 4-Panel.png` |
| **Figure 3** | Topic Relevance Scores for Public Firms | Panel A: `R1.1.2 - T - Three Step Text Analysis Pipeline/R1.1.2.3 - T3 - Topic Relevance/2 - Figure 3 Panel A - Sector Relevance (NAICS 2-Digit).png`<br>Panel B: `R1.1.2 - T - Three Step Text Analysis Pipeline/R1.1.2.3 - T3 - Topic Relevance/3 - Figure 3 Panel B - Top 10 Relevant Firms.png` |
| **Figure 4** | Relevance & Privacy Patenting Pre/Post-2016 | Panel A: `R1.1.3 - X1 - Validation (Patents)/1 - Figure 4 Panel A - Distribution of Firm Topic Relevance and Privacy Patents.png`<br>Panel B: `R1.1.3 - X1 - Validation (Patents)/2 - Figure 4 Panel B - Annual Privacy Patent Filings by Relevance Quartile.png`<br>Panel C: `R1.1.3 - X1 - Validation (Patents)/3 - Figure 4 Panel C - Annual Privacy Patent Filings by Subclass.png` |
| **Figure 5** | Long-Term Trends & Top Patenting Firms | Panel A: `R1.1.3 - X1 - Validation (Patents)/1 - Figure 5 Panel A - Aggregate Filing Trends across Privacy CPC Codes.png`<br>Panel B: `R1.1.3 - X1 - Validation (Patents)/2 - Figure 5 Panel B - Top 20 Patent Assignees by Privacy Technology Group.png` |
| **Figure 6** | Event Study of Patenting Probability | Panel A: `R1.1.3 - X1 - Validation (Patents)/1 - Figure 6 Panel A - Event Study of Patenting Probability - Anonymizing Data.png`<br>Panel B: `R1.1.3 - X1 - Validation (Patents)/2 - Figure 6 Panel B - Event Study of Patenting Probability - Tracking User Activity.png` |

---

## Required Packages

The documents compile with standard `pdflatex` using the following packages:

| Package | Purpose |
| :--- | :--- |
| `geometry` | 1-inch page margins (`margin=1in`) |
| `ebgaramond` | Garamond font family typography |
| `setspace` | Line spacing (`\setstretch{1.15}`) |
| `graphicx` | Figure inclusion and scaling |
| `booktabs` | Professional publication-quality tables |
| `amsmath`, `amssymb` | Mathematical formatting |
| `caption` | Unbolded figure caption positioning (`position=top`) |
| `xcolor` | Hyperlink styling |
| `hyperref` | Clickable URLs and document metadata |

---

## Automated Compilation & Cleanup

To compile all submission documents in two passes (resolving all cross-references) and automatically purge all intermediate auxiliary files (`*.aux`, `*.log`, `*.out`, `*.toc`, `*.nav`, `*.snm`, `*.vrb`, `missfont.log`), run:

```bash
python3 compile_latex.py
```

Or compile a single document directly:

```bash
python3 compile_latex.py "main.tex"
```
