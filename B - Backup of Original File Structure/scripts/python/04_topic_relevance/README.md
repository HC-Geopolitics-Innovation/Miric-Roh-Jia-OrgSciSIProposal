# Stage 4 — Firm–Hearing Topic Relevance

Two **independent instruments** measure the same object — is hearing $i$'s
topic $k$ related to firm $c$'s business at that time? — and their agreement
is itself a result:

- **Layer 1, the deterministic rail**: no inference. Sentence embeddings,
  topic centroids from Stage-3 evidence sentences, top-$k$ mean cosine per
  (filing, topic). Replicable to the byte.
- **Layer 2, sentence-block tagging**: a small LLM reads Item 1 sentences in
  document-order blocks (numbered, index-cited — the Track-2 discipline) and
  tags (sentence, codebook topic, direction) records. Direction
  (opportunity / threat / neutral) and intensity (counted tagged sentences)
  are the dimensions Layer 1 cannot see.

**Independence is the design** (ratified 2026-08-22). No Layer-1 output —
cosine, ranking, centroid, top-$k$ selection — enters any Layer-2 prompt;
Layer 2's sampling frame (regimes, blocks) is built from plain text hashing.
If the two layers point at the same distribution, Layer 1's noise is bounded
and Layer 2's added dimensions inherit credibility. A witness-testimony
anchor was **deliberately rejected**: calibrating on observed participation
would bias the instrument against exactly the invisible relatedness (same
industry, unobserved routes) the paper exists to catch. Witness firms remain
available as a *post-hoc descriptive* check only, like CAP in Stage 3.

## Data flow

```
[01] Item 1 -> sentences (pysbd, boilerplate rule) -> embeddings   (GPU, done once)
      |                                   |
      |                                   v
      |            [02] topic centroids (Stage-3 evidence sentences)
      |                 (filing, topic) top-k scores + evidence      = LAYER 1
      v
[03] text regimes (sentence-hash Jaccard, no model)
     representative filings -> document-order blocks (<= 40 sentences)
      |
      v
[04] tagging promptbook (dev):  Pass A theme gate -> Pass B
     (sentence, topic, direction) tags; researcher reads every round = LAYER 2 dev
      |
      v
[05, planned] no-gate audit (Pass A miss rate, measured) + human gold
[06, planned] production sbatch -> aggregate to (firm-regime, topic) cells:
     related (>=1 tag), intensity (tag counts), direction (tag shares)
      |
      v
hearing join (INV-25: most recent 10-K filed BEFORE the hearing date;
regime representative = the regime's FIRST filing, so judged text always
predates the hearing) -> Layer-1 vs Layer-2 agreement analysis
```

## Notebooks

| # | Notebook | Consumes | Produces | Gate |
|---|---|---|---|---|
| 01 | `01_item1_sentences` | `sp500_10k_item1.parquet` | `item1/sentences.parquet`, `emb_*.npy` | counts, removal rates, alignment |
| 02 | `02_topic_centroids_scores` | 01 + frozen codebook + Track-2 assigned evidence | `scores/{topic_index, firm_topic_scores, evidence_sentences}` | length-decile diagnostic, on-topic spot-check |
| 03 | `03_firm_regimes_blocks` | 01 sentences + Item 1 filedAt | `tagging/{filing_regimes, regimes, blocks}` | threshold sensitivity, partition asserts, timeline read |
| 04 | `04_tagging_promptbook` | 03 + codebook | dev CallLogs; frozen `item1-topic-tagging-1.0` (3 rounds) | researcher reads every dev round |
| 05 | `05_gate_audit_gold` | 04 (frozen prompt) | `tagging/audit/*`, gold candidate CSV | Pass-A miss rate (measured), gold coding |
| 06 | `06_tagging_production` | 03 + frozen prompt (`jobs/tag_item1.sbatch`, array 0-9) | `tagging/shards/*` | gated share 20-60%, parse ≥95%, resumable |
| 07 | `07_layer1_descriptives` | 02 scores + NAICS3 (CRSP-Compustat link) | 4 face-validity figures (`fig_relevance_*`) | reader-predictable industries surface unprompted |
| 08 | *planned* — aggregation + hearing join | 06 shards | (firm, fyear, topic) cells; INV-25 join | related/intensity/direction sensitivity |

## Shared libraries

- `lib/relevance.py` — Layer 1: pinned segmenter, boilerplate normalizer
  (also the regime hash in 03), `encode`, `topk_mean`.
- `lib/tagging.py` — Layer 2: block numbering, theme/topic prompt rendering
  from the frozen codebook, index-validating parsers, `PROMPT_VERSION`.
- `lib/evalmetrics.py` — Cohen's kappa, rank AUC (for 05's gold).

## Parameter Registry — PROVISIONAL defaults awaiting ratification

| Parameter | Value | Where | Why this default | Status |
|---|---|---|---|---|
| Encoder (primary / alt) | `BAAI/bge-large-en-v1.5` / `all-mpnet-base-v2` | `lib/relevance.py` | strong open-weights pair | PROVISIONAL |
| Item-1 min sentence length | 30 chars | `lib/relevance.py` | drops headings/fragments | PROVISIONAL |
| Boilerplate threshold | ≥20 distinct firms | `lib/relevance.py` | sensitivity at 10/20/50 printed in 01 | PROVISIONAL |
| TOP_K (Layer-1 score) | 5 | `02` | plan §3, frozen at dev | PROVISIONAL |
| Centroid placement floor | τ = 0.68 | `02` | Stage-3 ratified value reused | matches Stage 3 |
| REGIME_MIN_JACCARD | 0.6 | `03` | sensitivity at 0.5/0.7 printed | PROVISIONAL |
| BLOCK_SENTENCES | 40 | `lib/tagging.py` | context always fits; paragraph-scale context | PROVISIONAL |
| related threshold | ≥1 tagged sentence (≥2 as sensitivity) | 06 aggregation | reported both ways | PROVISIONAL |
| Sampling + per-call seeds | Stage-2 `GENERATION` (temp 0.1), content-hash seeds | via `summarize.py` | continuity with Stages 2–3 | matches Stage 2 |

Superseded (removed 2026-08-22, recoverable from git): witness-gold anchor
(03), screening calibration / judge_list (04), whole-document judgment
promptbook/gold/production (05–07) and `lib/judgment.py`,
`jobs/judge_firm_topic.sbatch` — replaced by the independent sentence-block
tagging design above.
