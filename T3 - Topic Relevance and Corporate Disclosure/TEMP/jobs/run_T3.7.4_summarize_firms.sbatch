#!/bin/bash
#SBATCH --job-name=T3.7.4_summarize_firms
#SBATCH --account=njia_1089
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --constraint="a40|l40s|a100"
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=4:00:00
#SBATCH --output="/project2/njia_1089/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3 - Topic Relevance and Corporate Disclosure/TEMP/jobs/log/%x_%j.out"

# One firm summary per firm for one input set, one family, and one prompt version (T3.7.4). Submit with the three in the environment:
#   sbatch --export=ALL,SET=all_years,FAMILY=summary_lines_of_business,VERSION=item1-mapreduce-1.3 run_T3.7.4_summarize_firms.sbatch
SET="${SET:-all_years}"
FAMILY="${FAMILY:-summary_lines_of_business}"
VERSION="${VERSION:-item1-mapreduce-1.3}"
module purge
module load conda
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate /project2/njia_1089/acroh/envs/llm_method
export TMPDIR=/scratch1/acroh/tmp
mkdir -p "$TMPDIR"

STAGE_FOLDER="/project2/njia_1089/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3 - Topic Relevance and Corporate Disclosure/TEMP/T3.7 - Firm Summaries"
cd "$STAGE_FOLDER"
nvidia-smi --query-gpu=name --format=csv,noheader
echo "input set: $SET; family: $FAMILY; version: $VERSION"
python "T3.7.4 - Firm - Summarize Each Firm.py" --set "$SET" --family "$FAMILY" --version "$VERSION"
