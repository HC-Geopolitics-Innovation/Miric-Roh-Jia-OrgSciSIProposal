"""Small, dependency-free evaluation metrics used across Stage 3 and 4.

Implemented here rather than imported from scikit-learn so the environment
stays minimal and the formulas are visible in the replication package: a
chance-corrected agreement statistic and a rank-based AUC are each a dozen
lines, and a dozen lines that a referee can read beat a dependency pin.
"""

from __future__ import annotations

from collections import Counter

import numpy as np


def cohen_kappa(a: list, b: list) -> float:
    """Cohen's kappa between two label sequences of equal length."""
    if len(a) != len(b) or not a:
        raise ValueError("kappa needs two equal-length, non-empty sequences")
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    if expected == 1.0:
        return 1.0
    return (observed - expected) / (1.0 - expected)


def percent_agreement(a: list, b: list) -> float:
    if len(a) != len(b) or not a:
        raise ValueError("agreement needs two equal-length, non-empty sequences")
    return sum(x == y for x, y in zip(a, b)) / len(a)


def auc(positive_scores, negative_scores) -> float:
    """Rank-based AUC (Mann-Whitney): P(random positive > random negative),
    ties counted half. Exact, no binning, no curve construction."""
    pos = np.asarray(positive_scores, dtype=np.float64)
    neg = np.asarray(negative_scores, dtype=np.float64)
    if pos.size == 0 or neg.size == 0:
        raise ValueError("auc needs at least one score on each side")
    combined = np.concatenate([pos, neg])
    ranks = combined.argsort().argsort().astype(np.float64) + 1
    # midranks for ties
    order = np.argsort(combined, kind="mergesort")
    sorted_scores = combined[order]
    midranks = np.empty_like(ranks)
    i = 0
    while i < len(sorted_scores):
        j = i
        while j + 1 < len(sorted_scores) and sorted_scores[j + 1] == sorted_scores[i]:
            j += 1
        midranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    r_pos = midranks[: pos.size].sum()
    return float((r_pos - pos.size * (pos.size + 1) / 2.0) / (pos.size * neg.size))


def recall_at_threshold(positive_scores, threshold: float) -> float:
    pos = np.asarray(positive_scores, dtype=np.float64)
    if pos.size == 0:
        raise ValueError("no positive scores")
    return float((pos >= threshold).mean())
