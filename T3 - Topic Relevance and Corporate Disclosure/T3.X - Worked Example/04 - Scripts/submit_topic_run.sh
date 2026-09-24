#!/bin/bash
# Submit four resumable GPU shards (at most two GPUs concurrently), then assemble.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd -- "$SCRIPT_DIR/../../.." && pwd)"
RUN_DIR="${1:-/project2/njia_1089/acroh/data/output/topic68_relevance_20180410}"
cd "$REPO_DIR"
/project2/njia_1089/acroh/envs/llm_method/bin/python \
  "T3 - Topic Relevance and Corporate Disclosure/T3.2 - Process Execution/T3.2.1 - Production Batch Tagging Pipeline.py" \
  prepare --run-root "$RUN_DIR"
GPU_JOB=$(sbatch --parsable --output="$RUN_DIR/logs/tag_%A_%a.log" \
  "$SCRIPT_DIR/run_example.sbatch" "$RUN_DIR")
GPU_JOB="${GPU_JOB%%;*}"
printf '%s\n' "$GPU_JOB" > "$RUN_DIR/gpu_job_id.txt"
ASSEMBLY_JOB=$(sbatch --parsable --dependency="afterok:$GPU_JOB" \
  --output="$RUN_DIR/logs/assemble_%j.log" \
  "$SCRIPT_DIR/assemble_topic.sbatch" "$RUN_DIR")
ASSEMBLY_JOB="${ASSEMBLY_JOB%%;*}"
printf '%s\n' "$ASSEMBLY_JOB" > "$RUN_DIR/assembly_job_id.txt"
printf 'GPU array: %s\nAssembly: %s\nResults: %s/outputs\n' "$GPU_JOB" "$ASSEMBLY_JOB" "$RUN_DIR"
