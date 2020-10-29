#!/bin/sh

#SBATCH --partition=short
#SBATCH --time=3:00:00
#SBATCH --mem-per-cpu=4G
#SBATCH --job-name=short_submit
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err
#SBATCH --ntasks=1

cd ${SLURM_SUBMIT_DIR}

python short_submit.py $1 $2 $3 $4 $5 $6
