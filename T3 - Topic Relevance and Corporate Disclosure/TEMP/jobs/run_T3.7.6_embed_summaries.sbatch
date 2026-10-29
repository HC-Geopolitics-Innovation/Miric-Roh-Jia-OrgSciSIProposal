#!/bin/bash
#SBATCH --job-name=T3.7.6_embed_summaries
#SBATCH --account=njia_1089
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --constraint="a40|l40s|a100"
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=1:00:00
#SBATCH --output="/project2/njia_1089/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3 - Topic Relevance and Corporate Disclosure/TEMP/jobs/log/%x_%j.out"

# Execute the T3.7.5 check (CPU) and then the T3.7.6 notebook (embed every filing and firm summary with bge) on a GPU node, in place.
#   sbatch run_T3.7.6_embed_summaries.sbatch
#   sbatch --dependency=afterok:<T3.7.4 job id> run_T3.7.6_embed_summaries.sbatch
module purge
module load conda
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate /project2/njia_1089/acroh/envs/llm_method
export TMPDIR=/scratch1/acroh/tmp
mkdir -p "$TMPDIR"

STAGE_FOLDER="/project2/njia_1089/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3 - Topic Relevance and Corporate Disclosure/TEMP/T3.7 - Firm Summaries"
cd "$STAGE_FOLDER"
nvidia-smi --query-gpu=name --format=csv,noheader
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1800 "T3.7.5 - Firm - Check the Firm Summaries.ipynb" || exit 1
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3000 "T3.7.6 - Firm - Embed the Summaries.ipynb"
