# Results & Figures Index

This folder contains all evaluation figures and architectural diagrams organized by their corresponding section in the analysis pipeline (`D1`, `T1`, `T2`, `T3`).

---

## Directory & File Organization

### `D1 - Data Collection and Overview`
- **`fig_dataset_construction.pdf`** / **`.png`** / **`.tex`**: The three collection rails of D1 on one page: GovInfo hearings, the C-SPAN reference abstracts, and the SEC 10-K filings, with the measured counts at each step. Same visual language as the T1, T2, and T3 flowcharts.

### `T1 - Text Summarization`
- **`fig_text_summarization_flowchart.pdf`** / **`.png`** / **`.tex`**: The text summarization pipeline on one page: transcript to speaker turns to chunks, then the map, collapse, and reduce calls to the hearing summary, with the counts of the production run.
- **`T1.3 - Validation of Summaries/T1.3.2 - Validation - Compare Summaries with C-SPAN Abstracts/fig_cosine_similarity_by_pair_type.pdf`** / **`.png`** / **`.svg`**: Cosine similarity between a hearing's generated summary and C-SPAN's abstract of the same hearing, of other hearings of the same committee, and of hearings of other committees. Drawn by notebook T1.3.2 from the stored pair table; replaces `cosine_similarity_averages`.

### `T2 - Topic Extraction and Stance Analysis`
- **`fig_topic_extraction_flowchart.pdf`** / **`.png`** / **`.tex`**: The T2 workflow on one page: Track 1 from the summaries to the codebook and the 26 groups, Track 2 from the legislator turns to the placed stance records, and the aggregation to the support share by Congress, with the measured counts.
- **`T2.3 - Validation of Topics/T2.3.2 - Validation - Compare the Codebook with CAP Codes/fig_cap_crosswalk.pdf`** / **`.png`** / **`.svg`**: Crosswalk heatmap of the 26 topic groups against CAP's human-coded major topics; each cell the share of the group's hearings under that CAP topic.
- **`T2.4 - Stance by Topic over Time/T2.4.1 - Grouped Stance Volume/fig_select_volume_balance_groups.pdf`** / **`.png`** / **`.svg`**: Concern and support speech turns for each of the 26 topic groups.
- **`T2.4 - Stance by Topic over Time/T2.4.2 - Privacy Group Stance over Time/fig_privacy_support_share_by_congress_panel_a.pdf`** / **`.png`** / **`.svg`**: Share of supportive legislator statements by Congress on consumer data privacy legislation; `..._panel_b` for the group's other four topics pooled; `..._both_panels` for the two side by side.
- **`T2.4 - Stance by Topic over Time/T2.4.4 - Privacy Topic Stance Volume/fig_privacy_topic_stance_volume.pdf`** / **`.png`** / **`.svg`**: Concern and support for each of the five topics of the privacy group.

### `T3 - Topic Relevance and Corporate Disclosure`
- **`fig_relevance_industry_exposure.pdf`** / **`.svg`**: Industry-level policy exposure distributions from 10-K Item 1 text.
- **`fig_relevance_industry_topics.pdf`** / **`.svg`**: Heatmap of topic relevance intensity across 2-digit SIC industries.
- **`fig_relevance_industry_trends.pdf`** / **`.svg`**: Longitudinal trends in corporate policy disclosure relevance (1993–present).
- **`fig_relevance_top_pairs.pdf`** / **`.svg`**: Top firm-topic relevance pair distributions.
