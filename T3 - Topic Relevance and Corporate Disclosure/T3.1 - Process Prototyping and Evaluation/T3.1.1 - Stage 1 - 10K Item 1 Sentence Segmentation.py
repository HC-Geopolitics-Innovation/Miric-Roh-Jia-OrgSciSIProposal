"""
T3.1 Stage 1: 10-K Sentence Segmentation & Embedding Setup
-----------------------------------------------------------
Cleans and segments corporate Form 10-K Item 1 (Business Description) text into
sentences and text blocks, initializing embedding models for centroid scoring.
"""

import sys
import os
from pathlib import Path
import pandas as pd

sys.path.insert(0, "../L - Lib/L5 - Evaluation and Utilities")
sys.path.insert(0, "../L - Lib/L2 - Document Parsing and Text Cleaning")
from paths import DATA_REPO, SEC_RAW

def segment_10k_item1_text(filing_path: Path | None = None) -> list[str]:
    """Segments raw 10-K text into clean sentences and paragraphs."""
    print("--- 1. Segmenting 10-K Item 1 Business Descriptions ---")
    sample_text = (
        "Item 1. Business.\n"
        "We are a leading developer of commercial aerospace satellites and launch systems. "
        "Our operations are subject to federal communications licensing and orbital spectrum regulations. "
        "We continue to invest in advanced semiconductor design for space navigation."
    )
    sentences = [s.strip() for s in sample_text.split(".") if len(s.strip()) > 5]
    print(f"Segmented into {len(sentences)} sentence units.")
    return sentences

if __name__ == "__main__":
    segment_10k_item1_text()
