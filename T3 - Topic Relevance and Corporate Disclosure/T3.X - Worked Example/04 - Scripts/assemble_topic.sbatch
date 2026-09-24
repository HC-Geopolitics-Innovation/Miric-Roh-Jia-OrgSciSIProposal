#!/bin/bash
#SBATCH --account=mmiric_1435
#SBATCH --partition=main
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=00:30:00
#SBATCH --job-name=privacy_assemble

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
/project2/njia_1089/acroh/envs/llm_method/bin/python -u \
  "T3 - Topic Relevance and Corporate Disclosure/T3.2 - Process Execution/T3.2.2 - Panel Assembly and Empirical Descriptives.py" \
  --run-root "$1"
/project2/njia_1089/acroh/envs/llm_method/bin/python -u \
  "T3 - Topic Relevance and Corporate Disclosure/T3.X - Worked Example/04 - Scripts/export_example.py" \
  export --run-root "$1"
/project2/njia_1089/acroh/envs/llm_method/bin/python -u \
  "T3 - Topic Relevance and Corporate Disclosure/T3.2 - Process Execution/T3.2.3 - Similarity-Weighted Directional Scores.py" \
  --run-root "$1"
