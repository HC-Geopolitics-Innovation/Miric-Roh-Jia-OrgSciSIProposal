#!/bin/bash
#SBATCH --job-name=T3.5.1_embed_topic_definition
#SBATCH --account=njia_1089
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --constraint="a40|l40s|a100"
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=0:20:00
#SBATCH --output="/project2/njia_1089/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3 - Topic Relevance and Corporate Disclosure/TEMP/jobs/log/%x_%j.out"

# Runs T3.5.1 (embed the topic definition) on a GPU whose architecture the env's torch build supports.
module purge
module load conda
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate /project2/njia_1089/acroh/envs/llm_method
export TMPDIR=/scratch1/acroh/tmp
mkdir -p "$TMPDIR"

NOTEBOOK_FOLDER="/project2/njia_1089/acroh/projects/LLM-Text-Analysis-and-Synthesis/T3 - Topic Relevance and Corporate Disclosure/TEMP/T3.5 - Topic Representations"
cd "$NOTEBOOK_FOLDER"
nvidia-smi --query-gpu=name --format=csv,noheader
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=900 \
    "T3.5.1 - Topic - Embed the Topic Definition.ipynb"
