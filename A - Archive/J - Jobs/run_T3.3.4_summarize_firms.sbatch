#!/bin/bash
# The job that ran T3.3.4 in October 2026: one firm summary per firm with Qwen3.5-4B from the firm's yearly
# summaries, once for the all-years set (1,058 firms, about 90 GPU minutes) and once for the three-year set
# (841 firms, about 28 GPU minutes). Kept as the record of how the run was launched. It is not rerun.
#
#   sbatch --export=ALL,SET=all_years "J - Jobs/run_T3.3.4_summarize_firms.sbatch"
#   sbatch --export=ALL,SET=three_years "J - Jobs/run_T3.3.4_summarize_firms.sbatch"
#
#SBATCH --account=njia_1089
#SBATCH --partition=gpu
#SBATCH --constraint="a40|l40s|a100"
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=4:00:00
#SBATCH --job-name=T3.3.4_summarize_firms
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

export SET="${SET:-all_years}"
export FAMILY="${FAMILY:-summary_lines_of_business}"
export VERSION="${VERSION:-item1-mapreduce-1.3}"

echo "node $(hostname) | gpu $(nvidia-smi --query-gpu=name --format=csv,noheader) | set ${SET} | family ${FAMILY} | version ${VERSION} | $(date -u +%Y-%m-%dT%H:%M:%SZ)"
cd "${PROJECT_FOLDER}/T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.3 - Firm Side - Summaries of the 10-K Item 1 Filings"
OUT_FOLDER="${SCRATCH_FOLDER}/nb_runs/T3.3.4_Qwen3.5-4B"
mkdir -p "$OUT_FOLDER"
"${ENV_PREFIX}/bin/jupyter" nbconvert --to notebook --execute \
  --output "${OUT_FOLDER}/T3.3.4_${SET}.ipynb" --ExecutePreprocessor.timeout=14400 \
  "T3.3.4 - Production - Summarize Each Firm.ipynb"
echo "finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
