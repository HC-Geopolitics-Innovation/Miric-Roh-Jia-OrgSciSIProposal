# Example of Research Enabled by the LLM Pipeline

An empirical application of the pipeline's output. T3 gives every S&P 500 firm a topic relevance score: the cosine between a summary of the firm's 10-K business description and the policy summary of the congressional debate on consumer data privacy legislation. This section asks whether the firms the debate concerns are also the firms that patent privacy technology, and how their patenting changed around 2016, when the debate intensified. The patents come from the extended data of Kogan, Papanikolaou, Seru, and Stoffman (2017); a privacy patent is a sample-firm patent that carries one of 72 privacy-related CPC codes, and five of those codes are the focal technologies of the figures.

| Folder | What it holds |
|---|---|
| [Data](<Data/README.md>) | The five input files of the X1.2 notebooks: the privacy patent file and the firm relevance file written by X1.1.2, and the three privacy code lists. |
| [X1.1 - Patent Data - Sample Firm Patents and Privacy Codes](<X1.1 - Patent Data - Sample Firm Patents and Privacy Codes>) | How the data files are built: the link from the sample firms to their KPSS patents, then the CPC code match. Needs the KPSS download and the CRSP-Compustat link on scratch. |
| [X1.2 - Privacy Patents and Topic Relevance - 5 Codes by MM](<X1.2 - Privacy Patents and Topic Relevance - 5 Codes by MM>) | The figures: descriptive counts, the five focal topic groups over time and by firm, the four cluster groups, and the pre- and post-2016 comparison by relevance quartile. Runs from the `Data` folder alone. |

## Notebooks

| Notebook | What it does | Output |
|---|---|---|
| [X1.1.1 - Patents - Link Sample Firms to KPSS Patents](<X1.1 - Patent Data - Sample Firm Patents and Privacy Codes/X1.1.1 - Patents - Link Sample Firms to KPSS Patents.ipynb>) | Links the 1,058 sample firms to their CRSP permnos and keeps every KPSS patent filed by a sample firm in 1999 to 2025, attributed by the link in force on the filing date. | `sample_firm_patents.parquet` on scratch; the link and count tables under `R - Results/tables`. |
| [X1.1.2 - Patents - Match the Privacy CPC Codes and Build the Data Files](<X1.1 - Patent Data - Sample Firm Patents and Privacy Codes/X1.1.2 - Patents - Match the Privacy CPC Codes and Build the Data Files.ipynb>) | Attaches the CPC codes to every sample-firm patent, keeps the patents filed in 1999 to 2021 that carry a listed privacy code, and copies the T3.4.1 scores of the sample firms. | `Data/sample_firm_privacy_patents.csv`, `Data/firm_topic_relevance.csv`; `sample_firm_patent_cpc_codes.parquet` on scratch; the code count table under `R - Results/tables`. |
| [X1.2.1 - Descriptive - Privacy Patents of the Sample Firms, 1999 to 2021](<X1.2 - Privacy Patents and Topic Relevance - 5 Codes by MM/X1.2.1 - Descriptive - Privacy Patents of the Sample Firms, 1999 to 2021.ipynb>) | The five focal codes by patent count, the firms, sectors, and subsectors with the most privacy patents, firms that ever filed, and the yearly counts by topic group, normalized and raw, with the 20 largest patenters split by group. | Eight figures and nine tables; Figures 8A and 9 are Figure 5 of the proposal. |
| [X1.2.2 - Figure - Privacy Patents by Topic Group](<X1.2 - Privacy Patents and Topic Relevance - 5 Codes by MM/X1.2.2 - Figure - Privacy Patents by Topic Group.ipynb>) | The four-group version of the yearly trend and of the top-20 stacked bars, each patent weighted equally across its groups. | Two figures and two tables. |
| [X1.2.3 - Figure - Privacy CPC Codes by Group](<X1.2 - Privacy Patents and Topic Relevance - 5 Codes by MM/X1.2.3 - Figure - Privacy CPC Codes by Group.ipynb>) | The 72 codes read through four cluster groups and four focal privacy issues: the yearly trend by group and the ten largest patenters split by group and by issue. | Three figures. |
| [X1.2.4 - Figure - Firm Topic Relevance and Privacy Patent Changes Pre-Post 2016](<X1.2 - Privacy Patents and Topic Relevance - 5 Codes by MM/X1.2.4 - Figure - Firm Topic Relevance and Privacy Patent Changes Pre-Post 2016.ipynb>) | The distribution of the relevance score with average privacy patents per quartile overlaid, the annual filing rate before and after 2016 by quartile and by focal group, and the event studies of patenting probability by quartile. | Five figures and six tables; Figure 4, Panels A to C, and Figure 6 of the proposal. |

## Where the files are

- Figures and tables: `R - Results/figures/X1 - Example of Research Enabled by LLM Pipeline/<subfolder>/<notebook name>/` and the same path under `R - Results/tables`, as for the T sections.
- Raw and processed data on the cluster: `/scratch1/acroh/projects/LLM-Text-Analysis-and-Synthesis/X1 - Example of Research Enabled by LLM Pipeline/<subfolder>/{Raw, Interim, Processed}`. The X1.1 `Raw` folder holds the KPSS repository (`KPSS_2025.zip`, `Match_patent_cpc_2025.zip`) and `crsp_compustat_link.dta`; the `Processed` folders hold the patent tables as Parquet.
- Inputs from the pipeline: `table_sample_filings.csv` of T3.1.1 and `table_firm_relevance_scores.csv` of T3.4.1, both under `R - Results/tables`, so the section runs from the committed results of T3.

## How to run

The X1.2 notebooks need only the `Data` folder and run in a few minutes on a CPU. The X1.1 notebooks rebuild the `Data` files and need two inputs that are not in the repository: the KPSS extended data, downloaded from the authors' GitHub repository into the X1.1 `Raw` folder, and the CRSP-Compustat link table from WRDS, which is licensed. Each notebook derives the clone root from its own location and names the scratch root in one line of its Step 2 cell. The figures keep the styles their author set; the colors of the X1.2 notebooks are not the S3 palette of the T sections.

The KPSS data are to be cited as Kogan, L., Papanikolaou, D., Seru, A., and Stoffman, N. (2017), Technological Innovation, Resource Allocation, and Growth, *Quarterly Journal of Economics*, 132(2), 665 to 712.
