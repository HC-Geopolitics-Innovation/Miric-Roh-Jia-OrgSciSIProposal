"""T3.6.3 - Firm - Embed the Sentence Shards.

GPU batch stage of the topic-relevance rebuild: embed one shard of Item 1 sentences with
BAAI/bge-large-en-v1.5, CLS pooling, L2-normalized, exactly as the topic vectors were embedded
(T3.5.1, T3.5.3, T3.5.7), and save the vectors in float16 in the shard's row order. One SLURM
array task runs one shard. Run only on a card the environment's torch build supports (A40,
L40S, A100).

Usage   python "T3.6.3 - Firm - Embed the Sentence Shards.py" --shard 3
Reads   <scratch>/T3.6 - Firm Sentences/Interim/shards/shard_<k>.parquet
Writes  <scratch>/T3.6 - Firm Sentences/Interim/embeddings/shard_<k>.npy  (n_rows × 1024, float16)
        <scratch>/T3.6 - Firm Sentences/Interim/embeddings/shard_<k>.json (run record)
"""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from transformers import AutoModel, AutoTokenizer

SCRATCH_FOLDER = Path("/scratch1/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3-TEMP")
SHARDS_FOLDER = SCRATCH_FOLDER / "T3.6 - Firm Sentences" / "Interim" / "shards"
EMBEDDINGS_FOLDER = SCRATCH_FOLDER / "T3.6 - Firm Sentences" / "Interim" / "embeddings"
MODEL_FOLDER = Path(
    "/scratch2/acroh/projects/llm_method/hf_cache/hub/models--BAAI--bge-large-en-v1.5"
    "/snapshots/d4aa6901d3a41ba39fb536a557fa166f842b0e09"
)

MAX_TOKENS = 512  # the encoder's input limit; longer sentences are cut at it
BATCH_SIZE = 256  # sentences per forward pass
PROGRESS_EVERY = 100_000  # rows between progress lines in the log

parser = argparse.ArgumentParser()
parser.add_argument("--shard", type=int, required=True, help="shard id from the manifest")
args = parser.parse_args()

# Step 1. Read the shard and sort its sentences by length so each batch pads little.
manifest = pd.read_csv(SHARDS_FOLDER / "manifest.csv")
shard_info = manifest.loc[manifest["shard_id"].eq(args.shard)].iloc[0]
shard = pd.read_parquet(SHARDS_FOLDER / shard_info["file"])
assert len(shard) == shard_info["n_rows"]
assert shard["row"].is_monotonic_increasing
order = np.argsort(shard["sentence"].str.len().to_numpy(), kind="stable")
sentences_by_length = shard["sentence"].to_numpy()[order]
print(f"Shard {args.shard}: {len(shard):,} sentences, rows {shard_info['row_start']:,}–{shard_info['row_end']:,}", flush=True)

# Step 2. Load the encoder on the GPU in float32, the same precision as the topic vectors.
assert torch.cuda.is_available(), "run this stage on a GPU node"
tokenizer = AutoTokenizer.from_pretrained(MODEL_FOLDER, local_files_only=True)
model = AutoModel.from_pretrained(MODEL_FOLDER, local_files_only=True).to("cuda").eval()
assert model.config.max_position_embeddings == MAX_TOKENS
gpu_name = torch.cuda.get_device_name(0)
print(f"Encoder {MODEL_FOLDER.parent.parent.name} on {gpu_name}, {next(model.parameters()).dtype}", flush=True)

# Step 3. Embed in length-sorted batches: CLS token of the last layer, unit length, float16.
started = time.time()
embeddings_sorted = np.empty((len(shard), model.config.hidden_size), dtype=np.float16)
n_truncated = 0
with torch.no_grad():
    for start in range(0, len(shard), BATCH_SIZE):
        batch = sentences_by_length[start:start + BATCH_SIZE].tolist()
        encoded = tokenizer(batch, padding=True, truncation=True, max_length=MAX_TOKENS, return_tensors="pt").to("cuda")
        n_truncated += int((encoded["attention_mask"].sum(dim=1) == MAX_TOKENS).sum())
        last_layer = model(**encoded).last_hidden_state
        cls_vectors = torch.nn.functional.normalize(last_layer[:, 0], dim=-1)
        embeddings_sorted[start:start + len(batch)] = cls_vectors.cpu().numpy().astype(np.float16)
        if (start // BATCH_SIZE) % (PROGRESS_EVERY // BATCH_SIZE) == 0:
            print(f"  {start:,} / {len(shard):,} rows, {time.time() - started:.0f}s", flush=True)
seconds = time.time() - started

# Step 4. Restore the shard's row order and save.
embeddings = np.empty_like(embeddings_sorted)
embeddings[order] = embeddings_sorted
norms = np.linalg.norm(embeddings.astype(np.float32), axis=1)
assert np.allclose(norms, 1, atol=1e-2)
EMBEDDINGS_FOLDER.mkdir(parents=True, exist_ok=True)
embeddings_file = EMBEDDINGS_FOLDER / f"shard_{args.shard}.npy"
np.save(embeddings_file, embeddings)
(EMBEDDINGS_FOLDER / f"shard_{args.shard}.json").write_text(json.dumps({
    "shard_id": args.shard, "n_rows": int(len(shard)), "row_start": int(shard_info["row_start"]),
    "row_end": int(shard_info["row_end"]), "n_truncated_at_max_tokens": n_truncated,
    "model": str(MODEL_FOLDER), "pooling": "cls", "normalized": True, "model_dtype": "float32",
    "saved_dtype": "float16", "max_tokens": MAX_TOKENS, "batch_size": BATCH_SIZE, "gpu": gpu_name,
    "torch": torch.__version__, "seconds": round(seconds, 1),
    "finished": datetime.now(timezone.utc).isoformat(timespec="seconds"),
}, indent=2), encoding="utf-8")
print(f"Saved {embeddings_file} ({len(shard):,} × {model.config.hidden_size}) in {seconds / 60:.1f} minutes; "
      f"{n_truncated:,} sentences cut at {MAX_TOKENS} tokens", flush=True)
