#!/bin/bash
# The job that ran T2.2.3 in August 2026 (array 11261709): stance extraction over 220,160 legislator turns, five shards.
# Kept as the record of how the production run was launched. It is not rerun: about 42 GPU hours, and a new
# run would sample new records.
#
#   sbatch "J - Jobs/run_T2.2.3_extract_stances.sbatch"
#
# Each task executes its own copy of the notebook, so five tasks never write the same file.
# A task that runs out of time is submitted again, not restarted: the notebook skips every
# turn already in its shard file.
#
#SBATCH --account=mmiric_1435
#SBATCH --partition=gpu
#SBATCH --constraint="l40s|a40|a100"
#SBATCH --gres=gpu:1
#SBATCH --array=0-4
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=12:00:00
#SBATCH --job-name=T2.2.3_extract_stances
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
export N_SHARDS=5

echo "node $(hostname) | gpu $(nvidia-smi --query-gpu=name --format=csv,noheader) | shard ${SHARD} of ${N_SHARDS} | $(date -u +%Y-%m-%dT%H:%M:%SZ)"

cd "${PROJECT_FOLDER}/T2 - Topic Extraction and Stance Analysis/T2.2 - Track 2 - Legislator Stance Extraction"
OUT_FOLDER="${SCRATCH_FOLDER}/nb_runs/track2_Qwen3.5-4B"
mkdir -p "$OUT_FOLDER"
"${ENV_PREFIX}/bin/jupyter" nbconvert --to notebook --execute \
  --output "${OUT_FOLDER}/T2.2.3_shard${SHARD}.ipynb" --ExecutePreprocessor.timeout=43200 \
  "T2.2.3 - Production - Extract Stances from Every Turn in Shards.ipynb"
echo "finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
