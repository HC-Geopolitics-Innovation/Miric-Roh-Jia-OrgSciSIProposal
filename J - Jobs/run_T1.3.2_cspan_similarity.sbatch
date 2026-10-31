#!/bin/bash
# T1.3.2: embed the 351 matched summaries and the 3,812 C-SPAN abstracts with bge-large-en-v1.5,
# store the pairwise cosines, and draw the figure. One GPU, a few minutes; the wall clock is margin.
#
#   sbatch "J - Jobs/run_T1.3.2_cspan_similarity.sbatch"
#
#SBATCH --account=mmiric_1435
#SBATCH --partition=gpu
#SBATCH --constraint="l40s|a40|a100"
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=0:30:00
#SBATCH --job-name=T1.3.2_cspan_similarity
#SBATCH --output="/project2/njia_1089/acroh/projects/OS_LLM_TEMP/J - Jobs/log/%x_%j.out"

set -euo pipefail
module purge
module load conda

PROJECT_FOLDER="/project2/njia_1089/acroh/projects/OS_LLM_TEMP"
SCRATCH_FOLDER="/scratch1/acroh/projects/LLM-Text-Analysis-and-Synthesis"
ENV_PREFIX="/project2/njia_1089/acroh/envs/llm_method"

export TMPDIR="/scratch1/acroh/tmp"
export HF_HOME="${SCRATCH_FOLDER}/cache/huggingface"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
mkdir -p "$TMPDIR"

echo "node $(hostname) | gpu $(nvidia-smi --query-gpu=name --format=csv,noheader) | $(date -u +%Y-%m-%dT%H:%M:%SZ)"

cd "${PROJECT_FOLDER}/T1 - Text Summarization/T1.3 - Validation of Summaries"
"${ENV_PREFIX}/bin/jupyter" nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1800 \
  "T1.3.2 - Validation - Compare Summaries with C-SPAN Abstracts.ipynb"
echo "finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
