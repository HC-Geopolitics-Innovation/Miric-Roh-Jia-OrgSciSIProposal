#!/bin/bash
# The job that ran T1.2.1 in August 2026: map-reduce summarization of the 2,352 hearings, ten shards.
# Kept as the record of how the production run was launched. It is not rerun: about 121 GPU hours.
#
#   sbatch "J - Jobs/run_T1.2.1_summarize_sst.sbatch"
#
# Each task executes its own copy of the notebook, so ten tasks never write the same file.
# A task that runs out of time is submitted again, not restarted: the notebook skips every
# hearing whose call log already holds a reduce line.
#
#SBATCH --account=mmiric_1435
#SBATCH --partition=gpu
#SBATCH --constraint="l40s|a40|a100"
#SBATCH --gres=gpu:1
#SBATCH --array=0-9
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=20:00:00
#SBATCH --job-name=T1.2.1_summarize_sst
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

export MODEL="Qwen/Qwen3.5-4B"
export SHARD="${SLURM_ARRAY_TASK_ID:-0}"
export N_SHARDS=10
export CHUNK_TOKENS=6144
export RUN_NAME="sst_Qwen3.5-4B"

echo "node $(hostname) | gpu $(nvidia-smi --query-gpu=name --format=csv,noheader) | shard ${SHARD} of ${N_SHARDS} | $(date -u +%Y-%m-%dT%H:%M:%SZ)"

cd "${PROJECT_FOLDER}/T - Three Step Text Analysis Pipeline/T1 - Text Summarization/T1.2 - Process Entire Sample Congressional Hearings"
OUT_FOLDER="${SCRATCH_FOLDER}/nb_runs/${RUN_NAME}"
mkdir -p "$OUT_FOLDER"
"${ENV_PREFIX}/bin/jupyter" nbconvert --to notebook --execute \
  --output "${OUT_FOLDER}/T1.2.1_shard${SHARD}.ipynb" --ExecutePreprocessor.timeout=72000 \
  "T1.2.1 - Production - Summarize the Sample in Shards.ipynb"
echo "finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
