# T3 - Topic Relevance and Corporate Disclosure (TEMP)

Relevance of each S&P 500 firm's 10-K Item 1 to Topic 68, consumer data privacy legislation. One notebook or script per step. Small outputs in `output/<notebook id>/`; large files on scratch at `/scratch1/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3-TEMP/`.

```
TEMP
├── README.md                                                    this file
├── jobs
│   ├── run_T3.5.1_embed_topic_definition.sbatch                 SLURM wrapper for T3.5.1
│   ├── run_T3.6.3_embed_sentence_shards.sbatch                  SLURM array wrapper for T3.6.3 (one task per shard)
│   ├── run_T3.7.2_summarize_filings.sbatch                      SLURM array wrapper for T3.7.2 (one task per shard; SET and FAMILY from the environment)
│   └── log/                                                     SLURM job logs
├── T3.4 - Sample
│   └── T3.4.1 - Sample - Select Firms and Filings.ipynb         firm universe and the two filing samples (all years; fiscal 2010, 2015, 2020); one filing per firm-year
├── T3.5 - Topic Representations
│   ├── T3.5.1 - Topic - Embed the Topic Definition.ipynb        embed the Topic 68 label and definition (bge) -> definition vector
│   ├── T3.5.2 - Topic - Rebuild the Stance Statements.ipynb     collect the 374 hearing statements coded to Topic 68
│   ├── T3.5.3 - Topic - Embed the Statements and Take the Centroid.ipynb   embed the statements; unit-length mean -> centroid vector
│   ├── T3.5.4 - Topic - Prepare the Policy Summary Inputs.ipynb prompts and per-year statement chunks for the policy summary
│   ├── T3.5.5 - Topic - Summarize the Statements.py             GPU: Qwen3.5-4B map (by hearing year) and reduce -> policy summary
│   ├── T3.5.6 - Topic - Check the Policy Summary.ipynb          trace the summary's claims to statements
│   └── T3.5.7 - Topic - Embed the Policy Summary.ipynb          embed the policy summary -> policy summary vector
├── T3.6 - Firm Sentences
│   ├── T3.6.1 - Firm - Split Item 1 into Sentences.ipynb        split every sampled Item 1 into sentences (pysbd)
│   ├── T3.6.2 - Firm - Prepare the Embedding Shards.ipynb       cut the sentences into eight shards
│   ├── T3.6.3 - Firm - Embed the Sentence Shards.py             GPU: embed one shard with bge
│   ├── T3.6.4 - Firm - Check the Sentence Embeddings.ipynb      assemble the shards into one array; recheck
│   ├── T3.6.5 - Firm - Compute Sentence Similarities.ipynb      cosine of every sentence with the definition and centroid vectors; thresholds fixed by hand (0.67, 0.75)
│   ├── T3.6.6 - Firm - Sentence Share with the Definition Vector.ipynb   share of a firm's sentences at or above 0.67
│   └── T3.6.7 - Firm - Sentence Share with the Centroid Vector.ipynb     share of a firm's sentences at or above 0.75
├── T3.7 - Firm Summaries
│   ├── T3.7.1 - Firm - Prepare the Summary Inputs.ipynb         segment Item 1 texts; write the prompts (version 1.3) and settings
│   ├── T3.7.2 - Firm - Summarize Each Filing.py                 GPU: Qwen3.5-4B map and reduce -> one paragraph per filing
│   ├── T3.7.3 - Firm - Check the Filing Summaries.ipynb         assemble and check the filing summaries
│   ├── T3.7.4 - Firm - Summarize Each Firm.py                   GPU: one call per firm over its yearly summaries -> one paragraph per firm
│   ├── T3.7.5 - Firm - Check the Firm Summaries.ipynb           assemble and check the firm summaries
│   └── T3.7.6 - Firm - Embed the Summaries.ipynb                embed the filing and firm summaries with bge
├── T3.8 - Relevance Scores
│   ├── T3.8.1 - Score - Relevance from Sentences.ipynb          per firm: binary and share of sentences at or above the threshold (definition, centroid); Meta example
│   ├── T3.8.2 - Score - Relevance from Summaries.ipynb          per firm: cosine of the firm summary and mean cosine of the yearly summaries with each topic vector; Meta example
│   └── T3.8.3 - Score - Assemble All Methods.ipynb              one table of all ten measures; what each measure is; correlations
├── T3.9 - Relevance Figures
│   ├── T3.9.1 - Figure - Distribution of Relevance Scores.ipynb histogram per measure
│   ├── T3.9.2 - Figure - Most and Least Relevant Firms.ipynb    ten most and ten least relevant firms per measure
│   └── T3.9.3 - Figure - Most and Least Relevant Industries.ipynb   NAICS two-digit sector means relative to the sample mean, with within-sector variation
└── output
    ├── T3.4.1/filings.csv                                       one row per filing with sample flags
    ├── T3.5.1/topic_definition.csv, topic_definition_embedding.npy
    ├── T3.5.2/topic68_statements.csv
    ├── T3.5.3/statement_embeddings.npy, topic_centroid_embedding.npy, nearest_statements.csv
    ├── T3.5.4/policy_summary_input.json, policy_summary_prompt.md
    ├── T3.5.5/policy_summary.md, yearly_summaries.csv, policy_summary_meta.json
    ├── T3.5.6/policy_summary_check.md
    ├── T3.5.7/policy_summary_text.csv, policy_summary_embedding.npy
    ├── T3.6.1/sentence_counts.csv
    ├── T3.6.2/manifest.csv
    ├── T3.6.4/embedding_check.csv
    ├── T3.6.5/similarity_threshold.csv, similarity_quantiles.csv, share_above_cutoffs.csv, statement_similarities.csv, fig_similarity_*.{png,svg,pdf}
    ├── T3.6.6/score_sentence_share_definition.csv, example_sentences_above_threshold.csv
    ├── T3.6.7/score_sentence_share_centroid.csv, example_sentences_above_threshold.csv
    ├── T3.7.1/settings.json, prompts.md (version 1.3); settings_<version>.json, prompts_<version>.md (1.1, 1.2); manifest.csv; token_counts.csv
    ├── T3.7.3/filing_summary_check_*.csv, example_summaries_*.csv (per version)
    ├── T3.7.5/firm_summary_check_*.csv, example_firm_summaries_*.csv
    ├── T3.7.6/embedding_record.json
    ├── T3.8.1/score_sentences.csv
    ├── T3.8.2/score_summaries.csv, filing_similarities.csv
    ├── T3.8.3/firm_relevance_scores.csv (long), firm_relevance_scores_wide.csv, measure_correlations.csv
    ├── T3.9.1/fig_distribution_<measure>.{png,svg,pdf}
    ├── T3.9.2/fig_firms_<measure>.{png,svg,pdf}
    └── T3.9.3/fig_industries_<measure>.{png,svg,pdf}, firm_industries.csv, sector_means.csv
```

Scratch (`/scratch1/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3-TEMP/`):

```
T3.6 - Firm Sentences/Processed/      sentences.parquet, sentence_embeddings.npy, sentence_similarities.parquet
T3.7 - Firm Summaries/Interim/        filing_inputs/<set>/, filing_summaries/<set>/<family>/<version>/, firm_summaries/<set>/<family>/<version>/
T3.7 - Firm Summaries/Processed/      filing_summaries.parquet, firm_summaries.parquet, *_embeddings.npy with *_embedding_keys.parquet
```

Sources: Item 1 texts and firm list from `/project2/mmiric_1435/acroh/llm_method/data`; models `BAAI/bge-large-en-v1.5` and `Qwen/Qwen3.5-4B` from `/scratch2/acroh/projects/llm_method/hf_cache`.
