#!/bin/bash
#SBATCH --job-name=T3.7.2_summarize_filings
#SBATCH --account=njia_1089
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --constraint="a40|l40s|a100"
#SBATCH --array=0-7
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=4:00:00
#SBATCH --output="/project2/njia_1089/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3 - Topic Relevance and Corporate Disclosure/TEMP/jobs/log/%x_%A_%a.out"

# One array task per shard of one input set and one summary family (T3.7.2). Submit with both in the environment:
#   sbatch --export=ALL,SET=three_years,FAMILY=summary_lines_of_business run_T3.7.2_summarize_filings.sbatch
#   sbatch --export=ALL,SET=remaining,FAMILY=summary_lines_of_business --time=14:00:00 run_T3.7.2_summarize_filings.sbatch
SET="${SET:-three_years}"
FAMILY="${FAMILY:-summary_lines_of_business}"
module purge
module load conda
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate /project2/njia_1089/acroh/envs/llm_method
export TMPDIR=/scratch1/acroh/tmp
mkdir -p "$TMPDIR"

STAGE_FOLDER="/project2/njia_1089/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3 - Topic Relevance and Corporate Disclosure/TEMP/T3.7 - Firm Summaries"
cd "$STAGE_FOLDER"
nvidia-smi --query-gpu=name --format=csv,noheader
echo "input set: $SET; family: $FAMILY; shard: $SLURM_ARRAY_TASK_ID"
python "T3.7.2 - Firm - Summarize Each Filing.py" --set "$SET" --family "$FAMILY" --shard "$SLURM_ARRAY_TASK_ID"
