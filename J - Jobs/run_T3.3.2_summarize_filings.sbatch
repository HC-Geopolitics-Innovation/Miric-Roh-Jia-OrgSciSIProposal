#!/bin/bash
# The jobs that ran T3.3.2 in October 2026: one summary per 10-K filing with Qwen3.5-4B, map-collapse-reduce
# over the Item 1 segments. Two arrays of eight tasks, one per shard: the three-year set (about 4.6 GPU hours
# in all) and the remaining filings (about 37 GPU hours in all), both with the summary_lines_of_business family.
# Kept as the record of how the production run was launched. It is not rerun: a new run would sample new texts.
#
#   sbatch --export=ALL,SET=three_years,FAMILY=summary_lines_of_business "J - Jobs/run_T3.3.2_summarize_filings.sbatch"
#   sbatch --export=ALL,SET=remaining,FAMILY=summary_lines_of_business --time=14:00:00 "J - Jobs/run_T3.3.2_summarize_filings.sbatch"
#
# Each task executes its own copy of the notebook, so eight tasks never write the same file. A task that runs
# out of time is submitted again, not restarted: the notebook skips every filing already in its shard file.
#
#SBATCH --account=njia_1089
#SBATCH --partition=gpu
#SBATCH --constraint="a40|l40s|a100"
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --array=0-7
#SBATCH --mem=32G
#SBATCH --time=4:00:00
#SBATCH --job-name=T3.3.2_summarize_filings
#SBATCH --output="/project2/njia_1089/acroh/projects/OS_LLM_TEMP/J - Jobs/log/%x_%A_%a.out"

set -euo pipefail
module purge
module load conda

PROJECT_FOLDER="/project2/njia_1089/acroh/projects/OS_LLM_TEMP"
SCRATCH_FOLDER="/scratch1/acroh/projects/LLM-Text-Analysis-and-Synthesis"
ENV_PREFIX="/project2/njia_1089/acroh/envs/llm_method"

export TMPDIR="/scratch1/acroh/tmp"
export HF_HOME="${SCRATCH_FOLDER}/cache/huggingface"
mkdir -p "$TMPDIR" "$HF_HOME"

export SET="${SET:-three_years}"
export FAMILY="${FAMILY:-summary_lines_of_business}"
export SHARD="${SLURM_ARRAY_TASK_ID:-0}"

echo "node $(hostname) | gpu $(nvidia-smi --query-gpu=name --format=csv,noheader) | set ${SET} | family ${FAMILY} | shard ${SHARD} | $(date -u +%Y-%m-%dT%H:%M:%SZ)"
cd "${PROJECT_FOLDER}/T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.3 - Firm Side - Summaries of the 10-K Item 1 Filings"
OUT_FOLDER="${SCRATCH_FOLDER}/nb_runs/T3.3.2_Qwen3.5-4B"
mkdir -p "$OUT_FOLDER"
"${ENV_PREFIX}/bin/jupyter" nbconvert --to notebook --execute \
  --output "${OUT_FOLDER}/T3.3.2_${SET}_shard${SHARD}.ipynb" --ExecutePreprocessor.timeout=50400 \
  "T3.3.2 - Production - Summarize Each Filing.ipynb"
echo "finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
