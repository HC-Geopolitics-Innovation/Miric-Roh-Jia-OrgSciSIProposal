"""The deterministic rail of Stage 4: Item 1 sentences and their embeddings.

Everything in this module is computation, not inference — the layer of the
Stage-4 plan (`quality_reports/plans/20260820_ plan/
20260820_topic_relevance_plan.tex` §3) whose entire purpose is to be
replicable: same inputs, same bytes out. Three commitments follow:

* **One segmenter for both sides.** Item 1 sentences are produced by the same
  pinned pysbd segmenter as the hearing evidence sentences
  (`stance.segment_sentences`), so firm sentences and topic centroids are
  units of the same kind — the plan's like-compared-with-like defense against
  cross-genre cosine incomparability.
* **Boilerplate removal by rule, not by model.** A sentence appearing
  near-verbatim across many different firms' filings is legal boilerplate;
  the normalizer here makes that detectable with a hash count, and the
  notebook reports what was removed at which threshold.
* **Pooling and normalization are our code.** The encoder is a pinned
  open-weights checkpoint, but pooling and L2 normalization are implemented
  here rather than inherited from a library whose defaults can drift between
  versions.
"""

from __future__ import annotations

import hashlib
import re

import numpy as np
import torch

from stance import segment_sentences

#: Primary encoder and the alternative used for the sensitivity re-run
#: (plan §3: one alternative encoder reported). Pooling per checkpoint: BGE
#: publishes CLS-token embeddings, MPNet mean-pooled ones — applying the
#: wrong pooling silently degrades both, so it is looked up, never assumed.
ENCODER = "BAAI/bge-large-en-v1.5"
ENCODER_ALT = "sentence-transformers/all-mpnet-base-v2"
POOLING = {ENCODER: "cls", ENCODER_ALT: "mean"}

#: Sentences shorter than this are headings, list fragments, and table
#: residue, not business description. Higher than the hearing-side threshold
#: because Item 1 fragments are typically section labels ("Item 1.
#: Business.") rather than short speech.
MIN_SENTENCE_CHARS = 30

#: A normalized sentence form appearing in at least this many distinct firms
#: is treated as boilerplate. The notebook prints removal rates at
#: neighboring thresholds so the choice is visibly not load-bearing.
BOILERPLATE_MIN_FIRMS = 20


def segment_item1(text: str) -> list[str]:
    """Item 1 text to sentences: blocks first, then the pinned segmenter.

    Filings arrive as long strings with paragraph breaks. Splitting on blank
    lines before pysbd keeps the segmenter fast on 40k-character documents
    and stops a stray heading from gluing itself to the next paragraph's
    first sentence.
    """
    sentences: list[str] = []
    for block in re.split(r"\n\s*\n|\r\n\s*\r\n", text or ""):
        block = block.strip()
        if block:
            sentences.extend(segment_sentences(block))
    return sentences


def keep_sentence(sentence: str) -> bool:
    """Length gate: drop headings and fragments before any counting."""
    return len(sentence) >= MIN_SENTENCE_CHARS


def normalize_for_dedup(sentence: str) -> str:
    """Canonical form for cross-document boilerplate detection.

    Lowercased, digits collapsed (dollar amounts and years differ between
    firms even when the sentence is the same template), punctuation and
    whitespace stripped. Two filings' "our common stock is listed on the New
    York Stock Exchange under the symbol X" then collide, which is the point.
    """
    s = sentence.lower()
    s = re.sub(r"\d+", "#", s)
    s = re.sub(r"[^a-z#]+", "", s)
    return s


def dedup_key(sentence: str) -> str:
    """Stable short hash of the normalized form, for corpus-wide counting."""
    return hashlib.sha1(normalize_for_dedup(sentence).encode()).hexdigest()[:16]


@torch.no_grad()
def encode(texts: list[str], model, tokenizer, encoder_name: str,
           batch_size: int = 256, max_length: int = 512) -> np.ndarray:
    """Embed texts with the pinned pooling for the named encoder.

    Returns L2-normalized float16 vectors, so cosine similarity downstream is
    a plain dot product and the 5.5M-sentence matrix stays around 11 GB.
    """
    pooling = POOLING[encoder_name]
    out = np.empty((len(texts), model.config.hidden_size), dtype=np.float16)
    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        enc = tokenizer(batch, padding=True, truncation=True,
                        max_length=max_length, return_tensors="pt").to(model.device)
        hidden = model(**enc).last_hidden_state
        if pooling == "cls":
            vec = hidden[:, 0]
        else:
            mask = enc["attention_mask"].unsqueeze(-1)
            vec = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1)
        vec = torch.nn.functional.normalize(vec, dim=-1)
        out[start:start + len(batch)] = vec.float().cpu().numpy().astype(np.float16)
    return out


def topk_mean(scores: np.ndarray, k: int) -> float:
    """Mean of the k largest entries — the plan's aggregation (§3), chosen
    over max (one noisy sentence decides; length-biased) and over the full
    mean (dilution)."""
    if scores.size == 0:
        return float("nan")
    k = min(k, scores.size)
    return float(np.sort(scores)[-k:].mean())
