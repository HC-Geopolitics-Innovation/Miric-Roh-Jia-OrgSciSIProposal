# Results & Figures Index

This folder contains all evaluation figures and architectural diagrams organized by their corresponding section in the analysis pipeline (`D1`, `T1`, `T2`, `T3`).

---

## Directory & File Organization

### `D1 - Data Collection and Overview`
- **`fig_dataset_construction.pdf`** / **`.png`** / **`.tex`**: The three collection rails of D1 on one page: GovInfo hearings, the C-SPAN reference abstracts, and the SEC 10-K filings, with the measured counts at each step. Same visual language as the T1, T2, and T3 flowcharts.

### `T1 - Text Summarization`
- **`fig_text_summarization_flowchart.pdf`** / **`.png`** / **`.tex`**: The text summarization pipeline on one page: transcript to speaker turns to chunks, then the map, collapse, and reduce calls to the hearing summary, with the counts of the production run.
- **`cosine_similarity_averages.pdf`** / **`.png`**: Cosine similarity between a hearing's generated summary and C-SPAN's abstract of the same hearing, of other hearings of the same committee, and of hearings of other committees.

### `T2 - Topic Extraction and Stance Analysis`
- **`fig_topic_extraction.pdf`** / **`.tex`**: Diagram of the member turn topic extraction and stance classification pipeline.
- **`fig_taxonomy_criteria.pdf`** / **`.svg`**: Taxonomic clustering criteria and consensus evaluation figures.
- **`fig_cap_crosswalk.pdf`** / **`.svg`**: Comparative Agendas Project (CAP) topic crosswalk alignment plots.
- **`fig_cap_rank_percentile.pdf`** / **`.svg`**: Rank percentile distribution of extracted topics vs CAP categories.
- **`fig_cap_retrieval.pdf`** / **`.svg`**: Information retrieval precision/recall metrics against CAP benchmarks.
- **`fig_cap_subtopic_boxes.pdf`** / **`.svg`**: Subtopic distribution boxplots.
- **`fig_cap_subtopic_pairs.pdf`** / **`.svg`**: Subtopic pairwise co-occurrence distributions.
- **`fig_stance_attention.pdf`** / **`.svg`**: Congressional stance attention distribution curves over time.
- **`fig_stance_net.pdf`** / **`.svg`**: Net sentiment/stance polarization network diagrams across topics.
- **`fig_stance_topics.pdf`** / **`.svg`**: Primary policy topic distribution across congressional speaker turns.

### `T3 - Topic Relevance and Corporate Disclosure`
- **`fig_relevance_industry_exposure.pdf`** / **`.svg`**: Industry-level policy exposure distributions from 10-K Item 1 text.
- **`fig_relevance_industry_topics.pdf`** / **`.svg`**: Heatmap of topic relevance intensity across 2-digit SIC industries.
- **`fig_relevance_industry_trends.pdf`** / **`.svg`**: Longitudinal trends in corporate policy disclosure relevance (1993–present).
- **`fig_relevance_top_pairs.pdf`** / **`.svg`**: Top firm-topic relevance pair distributions.
