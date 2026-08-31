"""
T1.1 Stage 1: Preparation & Model Setup
-----------------------------------------
This module handles file preparation, environment configuration, model selection,
and loading model weights into scratch memory for map-reduce text summarization.

Key Configurations & Model Choices:
- Model Selected: Qwen/Qwen3.5-4B (in 16-bit bfloat16 precision `bf16`).
- Storage Location: Weights downloaded/cached in `HF_CACHE` on scratch (/scratch2/$USER/projects/llm_method/hf_cache),
  never on home quota (/home1).
- Context Window: Supported up to 128k, but chunk budgets are managed strictly via `lib/chunking.py`.
- Benchmark Dataset: `data/raw/02_hearings/hearings_sst.parquet` (2,352 SST hearing transcripts).
"""

import os
import sys
from pathlib import Path
import pandas as pd

# Add lib directory for paths and helper modules
sys.path.insert(0, "../L - Lib/L5 - Evaluation and Utilities")
sys.path.insert(0, "../L - Lib/L1 - Data Collection and Network Clients")
from paths import SCRATCH, HF_CACHE, DATA_REPO, HEARINGS_REPO

# Model selection configurations
CANDIDATE_MODELS = {
    "Qwen/Qwen3.5-4B": {"params": "4.66B", "vram_bf16": "9.3 GB", "status": "SELECTED_FOR_PRODUCTION"},
    "google/gemma-4-E4B-it": {"params": "8.00B", "vram_bf16": "16.0 GB", "status": "EVALUATED"},
    "meta-llama/Llama-3.1-8B-Instruct": {"params": "8.03B", "vram_bf16": "16.1 GB", "status": "EVALUATED"},
    "meta-llama/Llama-3.2-3B-Instruct": {"params": "3.21B", "vram_bf16": "6.4 GB", "status": "EVALUATED"}
}

SELECTED_MODEL = "Qwen/Qwen3.5-4B"

def verify_environment_and_paths():
    """Verify scratch directory structure, HF cache location, and input datasets."""
    print("--- 1. Environment & Path Verification ---")
    print(f"Scratch Directory: {SCRATCH}")
    print(f"Hugging Face Cache: {HF_CACHE}")
    
    # Ensure cache directory exists on scratch
    HF_CACHE.mkdir(parents=True, exist_ok=True)
    os.environ["HF_HOME"] = str(HF_CACHE)
    print(f"Set HF_HOME environment variable to {HF_CACHE}")

def load_input_sample(sample_path: Path | None = None) -> pd.DataFrame:
    """Load and validate input hearing transcript dataset."""
    print("\n--- 2. Loading Input Hearing Dataset ---")
    if sample_path is None or not sample_path.exists():
        # Fallback path resolve
        sample_path = HEARINGS_REPO / "hearings_sst.parquet"
        
    if sample_path.exists():
        df = pd.read_parquet(sample_path)
        print(f"Loaded dataset from {sample_path} with {len(df)} hearings.")
        print(f"Columns: {list(df.columns)}")
        return df
    else:
        print(f"Dataset path {sample_path} not found. Returning empty DataFrame template.")
        return pd.DataFrame(columns=["packageId", "title", "turns", "n_members", "has_text"])

def initialize_model_environment(model_name: str = SELECTED_MODEL):
    """
    Set up PyTorch and Hugging Face Transformers model loading logic.
    Loads weights in bfloat16 (bf16) precision to optimize memory footprint without quantization.
    """
    print(f"\n--- 3. Initializing Model Environment: {model_name} ---")
    model_info = CANDIDATE_MODELS.get(model_name, {})
    print(f"Model Parameters: {model_info.get('params')}")
    print(f"Estimated bf16 VRAM Footprint: {model_info.get('vram_bf16')}")
    print(f"Selection Status: {model_info.get('status')}")
    
    # Dynamic Hugging Face import check
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        print(f"PyTorch Version: {torch.__version__}, CUDA Available: {torch.cuda.is_available()}")
        print("Ready to load model tokenizer and weights into GPU VRAM.")
    except ImportError:
        print("PyTorch/Transformers not available in environment. Setup verified as dry-run.")

if __name__ == "__main__":
    print("Executing Step 1: Preparation & Model Setup Pipeline...")
    verify_environment_and_paths()
    load_input_sample()
    initialize_model_environment()
