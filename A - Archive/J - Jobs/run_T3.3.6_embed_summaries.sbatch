#!/bin/bash
# T3.3.6: embed the 22,923 filing summaries and the 1,899 firm summaries with bge-large-en-v1.5, about six
# minutes on one A40. Rerun on 2026-10-31 on an interactive allocation (job 13632230); the vectors equal the
# October run. The embedding notebook of T3.2.5 runs the same way and takes seconds.
#
#   sbatch "J - Jobs/run_T3.3.6_embed_summaries.sbatch"
#
#SBATCH --account=njia_1089
#SBATCH --partition=gpu
#SBATCH --constraint="a40|l40s|a100"
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=1:00:00
#SBATCH --job-name=T3.3.6_embed_summaries
#SBATCH --output="/project2/njia_1089/acroh/projects/OS_LLM_TEMP/J - Jobs/log/%x_%j.out"

set -euo pipefail
module purge
module load conda

PROJECT_FOLDER="/project2/njia_1089/acroh/projects/OS_LLM_TEMP"
SCRATCH_FOLDER="/scratch1/acroh/projects/LLM-Text-Analysis-and-Synthesis"
ENV_PREFIX="/project2/njia_1089/acroh/envs/llm_method"

export TMPDIR="/scratch1/acroh/tmp"
export HF_HOME="${SCRATCH_FOLDER}/cache/huggingface"
mkdir -p "$TMPDIR" "$HF_HOME"

echo "node $(hostname) | gpu $(nvidia-smi --query-gpu=name --format=csv,noheader) | $(date -u +%Y-%m-%dT%H:%M:%SZ)"
cd "${PROJECT_FOLDER}/T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.3 - Firm Side - Summaries of the 10-K Item 1 Filings"
"${ENV_PREFIX}/bin/jupyter" nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 \
  "T3.3.6 - Embed - The Filing and Firm Summary Vectors.ipynb"
echo "finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
