"""
T3.1 Stage 2: Promptbook Development & Centroid Distance Prototyping
----------------------------------------------------------------------
Prototypes prompt templates for LLM corporate relevance tagging (relevance score,
opportunity/threat direction) and computes embedding distance to topic centroids.
"""

import sys
import os
import json
from pathlib import Path

sys.path.insert(0, "../T3.X - Background Helper Functions")
sys.path.insert(0, "../L - Lib/L4 - Topic Extraction and Relevance")
from tagging import TAGGING_PROMPT

def prototype_relevance_tagging(text_block: str, topic_name: str) -> dict:
    """Prototypes relevance tagging on sample 10-K sentence block."""
    print(f"--- 2. Prototyping Relevance Tagging for Topic: {topic_name} ---")
    prompt = f"{TAGGING_PROMPT}\n\nTOPIC: {topic_name}\nTEXT: {text_block}"
    
    mock_tag_response = {
        "topic": topic_name,
        "is_relevant": True,
        "relevance_score": 0.92,
        "direction": "Opportunity",
        "evidence_quote": "advanced semiconductor design for space navigation"
    }
    return mock_tag_response

if __name__ == "__main__":
    block = "We continue to invest in advanced semiconductor design for space navigation."
    res = prototype_relevance_tagging(block, "Semiconductors & Microelectronics")
    print(f"Tagging Output:\n{json.dumps(res, indent=2)}")
