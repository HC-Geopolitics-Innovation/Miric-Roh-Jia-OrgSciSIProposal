#!/bin/bash
# The job that ran T3.2.3 on 2026-10-25: the policy summary of consumer data privacy legislation,
# 26 map calls (one per hearing year) and one reduce call with Qwen3.5-4B, about three minutes on one A40.
# Kept as the record of how the run was launched. It is not rerun: a new run would sample a new text.
#
#   sbatch "J - Jobs/run_T3.2.3_policy_summary.sbatch"
#
#SBATCH --account=njia_1089
#SBATCH --partition=gpu
#SBATCH --constraint="a40|l40s|a100"
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=0:30:00
#SBATCH --job-name=T3.2.3_policy_summary
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
cd "${PROJECT_FOLDER}/T - Three Step Text Analysis Pipeline/T3 - Topic Relevance and Corporate Disclosure/T3.2 - Topic Side - Policy Summary of the Legislator Statements"
"${ENV_PREFIX}/bin/jupyter" nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1800 \
  "T3.2.3 - Production - Summarize by Year and Reduce to the Policy Summary.ipynb"
echo "finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
