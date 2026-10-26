#!/bin/bash
#SBATCH --job-name=T3.6.3_embed_sentence_shards
#SBATCH --account=njia_1089
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --constraint="a40|l40s|a100"
#SBATCH --array=0-7
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=24G
#SBATCH --time=1:30:00
#SBATCH --output="/project2/njia_1089/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3 - Topic Relevance and Corporate Disclosure/TEMP/jobs/log/%x_%A_%a.out"

# Embeds one shard of Item 1 sentences per array task (T3.6.3); shards and manifest come from T3.6.2.
module purge
module load conda
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate /project2/njia_1089/acroh/envs/llm_method
export TMPDIR=/scratch1/acroh/tmp
mkdir -p "$TMPDIR"

STAGE_FOLDER="/project2/njia_1089/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3 - Topic Relevance and Corporate Disclosure/TEMP/T3.6 - Firm Sentences"
cd "$STAGE_FOLDER"
nvidia-smi --query-gpu=name --format=csv,noheader
python "T3.6.3 - Firm - Embed the Sentence Shards.py" --shard "$SLURM_ARRAY_TASK_ID"
