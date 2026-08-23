# LLM Text Analysis and Synthesis

How a researcher extracts low-dimensional, meaningful measures from
high-dimensional text with small open-weights language models — demonstrated
end to end on U.S. congressional science-committee hearings (House Science,
Senate Commerce; 2,352 hearings, 1995–2025) and S&P 500 10-K Business
sections (21,966 filings, 1993–2025). Every model call is logged, every
prompt is versioned and frozen before production, and every judgment is
index-cited back to a specific sentence.

## Pipeline

| Stage | Directory | What it does |
|---|---|---|
| 1. Dataset construction | `scripts/python/01_dataset_construction` | Enumerate-then-download hearing corpus (GovInfo), C-SPAN reference abstracts, bulk 10-K archive and Item 1 extraction (SEC), with every gap measured against a manifest |
| 2. Text summarization | `scripts/python/02_text_summarization` | Map-reduce hearing summaries (chunk → map → collapse → reduce), model comparison, quality evaluation against the independent C-SPAN reference |
| 3. Topic extraction | `scripts/python/03_topic_extraction` | Two independent tracks — hearing-level topics and speaker-level stance records (support/concern with index-cited evidence) — consensus clustering into a ratified, frozen 111-topic codebook, validated post hoc against the Comparative Agendas Project |
| 4. Topic relevance | `scripts/python/04_topic_relevance` | Two independent instruments for firm-topic relevance: a deterministic embedding rail (no inference) and a sentence-block LLM tagging layer (relevance + opportunity/threat direction), designed so their agreement is evidence |

`scripts/python/lib/` holds the shared modules the notebooks import
(prompts, parsers, call logging, paths). `paper/figures/` holds the
generated figures, including the pipeline schematics.

## Notes

- Notebooks are committed with their executed outputs; they run top to
  bottom in a fresh kernel. Heavy steps run as SLURM array jobs on USC
  CARC (job scripts not included here).
- Large inputs and intermediates (corpora, embeddings, per-call logs) are
  not in this repository; they are archived on institutional project
  storage.
- API credentials are read from a gitignored `.env`
  (see `scripts/python/01_dataset_construction/.env.example`). No key
  appears in code or output.
- Models: Qwen3.5-4B for generation, BAAI/bge-large-en-v1.5 for
  embeddings; greedy-adjacent sampling (temperature 0.1) with per-document
  content-hash seeds for reproducibility.
