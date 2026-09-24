#!/bin/bash
# Submitted by submit_topic_run.sh from the repository root.
#SBATCH --account=mmiric_1435
#SBATCH --partition=gpu
#SBATCH --constraint="l40s|a40|a100"
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=06:00:00
#SBATCH --array=0-3%2
#SBATCH --job-name=privacy_topic68

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
export HF_HUB_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
/project2/njia_1089/acroh/envs/llm_method/bin/python -u \
  "T3 - Topic Relevance and Corporate Disclosure/T3.2 - Process Execution/T3.2.1 - Production Batch Tagging Pipeline.py" \
  run --run-root "$1"
