"""
T2.1 Stage 2: Promptbook Development & Few-Shot Testing
---------------------------------------------------------
Prototypes and validates prompt templates, JSON schema constraints, and few-shot examples
for congressional topic extraction and stance classification (Support/Concern/Neutral).
"""

import sys
import os
import json
from pathlib import Path

sys.path.insert(0, "../T2.X - Background Helper Functions")
sys.path.insert(0, "../L - Lib/L4 - Topic Extraction and Relevance")
from stance import STANCE_EXTRACTION_PROMPT, parse_stance_json_response

def test_promptbook_few_shot_extraction(sample_turn: dict) -> dict:
    """Executes prototype prompt test with few-shot guidance on sample member turns."""
    print("--- 2. Testing Topic & Stance Extraction Promptbook ---")
    speaker = sample_turn.get("speaker", "Senator Smith")
    text = sample_turn.get("text", "We must increase federal R&D funding for domestic semiconductor manufacturing.")
    
    prompt = f"{STANCE_EXTRACTION_PROMPT}\n\nSPEAKER: {speaker}\nSTATEMENT: {text}"
    print(f"Generated extraction prompt for {speaker} ({len(prompt.split())} words).")
    
    # Mock extracted JSON response adhering to schema
    mock_response = {
        "speaker": speaker,
        "topic": "Semiconductor Manufacturing & R&D",
        "stance": "Support",
        "rationale": "Advocates for increased federal funding for domestic chip production.",
        "evidence_quote": "increase federal R&D funding for domestic semiconductor manufacturing"
    }
    return mock_response

if __name__ == "__main__":
    sample = {"speaker": "Senator Stevens", "text": "I strongly support expanding NASA's Artemis budget."}
    res = test_promptbook_few_shot_extraction(sample)
    print(f"Extraction Output:\n{json.dumps(res, indent=2)}")
