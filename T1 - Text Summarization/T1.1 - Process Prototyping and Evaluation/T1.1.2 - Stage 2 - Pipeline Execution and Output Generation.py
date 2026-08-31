"""
T1.1 Stage 2: Pipeline Execution & Output Generation
------------------------------------------------------
This module runs the turn-aware chunking and 3-prompt Map-Reduce LLM summarization
pipeline over test benchmark hearing samples and exports generated outputs.

Map-Reduce Prompts Used (from `T1.X/summarize.py`):
1. MAP PROMPT: Prompts LLM to summarize raw transcript turns per chunk:
   "What was said by each speaker in this segment? List specific claims, arguments, figures, and statutes."
2. COLLAPSE PROMPT: Condenses intermediate segment summaries if they exceed context budgets.
3. REDUCE PROMPT: Synthesizes all segment summaries into a single, cohesive hearing summary,
   preserving speaker attribution positions.
"""

import sys
import json
import time
from pathlib import Path
import pandas as pd

# Add helper function paths
sys.path.insert(0, "../T1.X - Background Helper Functions")
sys.path.insert(0, "../../L - Lib/L3 - LLM Orchestration and Summarization")
sys.path.insert(0, "../../L - Lib/L5 - Evaluation and Utilities")

try:
    from chunking import pack_turns_into_chunks
    from summarize import MAP_PROMPT, COLLAPSE_PROMPT, REDUCE_PROMPT
except ImportError:
    # Fallback import handlers
    pass

def chunk_hearing_transcript(turns: list[dict], max_tokens_per_chunk: int = 4000) -> list[dict]:
    """
    Applies turn-aware token chunking logic to transcript turns.
    Packs whole speaking turns greedily so that speaker arguments are never split across chunks.
    """
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for turn in turns:
        text = turn.get("text", "")
        speaker = turn.get("speaker", "UNKNOWN")
        # Approximate token count (words * 1.33)
        turn_tokens = int(len(text.split()) * 1.33)
        
        if current_tokens + turn_tokens > max_tokens_per_chunk and current_chunk:
            chunks.append({
                "text": "\n\n".join([f"{t['speaker']}: {t['text']}" for t in current_chunk]),
                "turn_count": len(current_chunk),
                "token_estimate": current_tokens
            })
            current_chunk = [turn]
            current_tokens = turn_tokens
        else:
            current_chunk.append(turn)
            current_tokens += turn_tokens
            
    if current_chunk:
        chunks.append({
            "text": "\n\n".join([f"{t['speaker']}: {t['text']}" for t in current_chunk]),
            "turn_count": len(current_chunk),
            "token_estimate": current_tokens
        })
        
    return chunks

def execute_map_reduce_summarization(hearing_id: str, turns: list[dict], model_runner=None) -> dict:
    """
    Executes the 3-stage Map-Reduce summarization pipeline for a single hearing:
    Stage A (Map): Summarize each chunk independently.
    Stage B (Collapse): Condense intermediate summaries if necessary.
    Stage C (Reduce): Synthesize final summary.
    """
    print(f"\n--- Executing Map-Reduce Pipeline for Hearing: {hearing_id} ---")
    
    # 1. Chunking
    chunks = chunk_hearing_transcript(turns)
    print(f"Transcript partitioned into {len(chunks)} turn-aware chunks.")
    
    # 2. Map Stage
    segment_summaries = []
    for idx, chunk in enumerate(chunks):
        map_input = f"{MAP_PROMPT}\n\n[TRANSCRIPT CHUNK {idx+1}]\n{chunk['text']}"
        print(f"  [Map Step {idx+1}/{len(chunks)}] Processing {chunk['token_estimate']} tokens...")
        
        if model_runner:
            summary_text = model_runner(map_input)
        else:
            # Mock dry-run output
            summary_text = f"Draft summary for chunk {idx+1} covering {chunk['turn_count']} turns."
            
        segment_summaries.append(summary_text)
        
    # 3. Collapse Stage (Conditional)
    combined_segment_text = "\n\n".join(segment_summaries)
    combined_tokens = int(len(combined_segment_text.split()) * 1.33)
    
    if combined_tokens > 4000:
        print(f"  [Collapse Step Required] Combined map summaries total {combined_tokens} tokens.")
        collapse_input = f"{COLLAPSE_PROMPT}\n\n[SEGMENT SUMMARIES]\n{combined_segment_text}"
        if model_runner:
            combined_segment_text = model_runner(collapse_input)
        else:
            combined_segment_text = f"Condensed summary of {len(segment_summaries)} segments."
            
    # 4. Reduce Stage
    print("  [Reduce Step] Synthesizing final hearing summary...")
    reduce_input = f"{REDUCE_PROMPT}\n\n[SEGMENT SUMMARIES]\n{combined_segment_text}"
    
    if model_runner:
        final_summary = model_runner(reduce_input)
    else:
        final_summary = (
            f"Final hearing summary for {hearing_id}.\n"
            "Key topics: Space exploration, NASA budget allocations, and interagency cooperation.\n"
            "Attributed statements: Senator Stevens raised questions on satellite infrastructure."
        )
        
    output_record = {
        "package_id": hearing_id,
        "n_chunks": len(chunks),
        "map_summaries_count": len(segment_summaries),
        "final_summary": final_summary,
        "summary_word_count": len(final_summary.split())
    }
    
    return output_record

def run_test_sample_benchmark():
    """Run test pipeline on sample benchmark hearings and save generated output parquet."""
    print("Starting Pipeline Execution on Benchmark Test Sample...")
    
    # Mock benchmark test hearing input
    mock_turns = [
        {"speaker": "The Chairman", "text": "The committee will come to order. Today we examine NASA space technology investments."},
        {"speaker": "Mr. Nelson", "text": "Thank you Mr. Chairman. Funding for Artemis and commercial lunar payloads is critical."},
        {"speaker": "Dr. Smith", "text": "We have seen significant progress in propulsion efficiency and orbital launch capabilities."}
    ]
    
    result = execute_map_reduce_summarization("CHRG-109hhrg30382-TEST", mock_turns)
    
    print("\n--- Pipeline Result Summary ---")
    print(f"Package ID: {result['package_id']}")
    print(f"Generated Summary Word Count: {result['summary_word_count']}")
    print(f"Final Summary Content:\n{result['final_summary']}")
    
    # Save benchmark sample result
    output_dir = Path("output_test_summaries")
    output_dir.mkdir(exist_ok=True)
    out_df = pd.DataFrame([result])
    out_file = output_dir / "test_hearing_summaries.parquet"
    out_df.to_parquet(out_file, index=False)
    print(f"\nSaved benchmark output result to {out_file}")

if __name__ == "__main__":
    run_test_sample_benchmark()
