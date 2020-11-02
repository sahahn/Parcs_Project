#!/bin/sh

#SBATCH --partition=ib
#SBATCH --time=30:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=ib_submit_high_mem
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err
#SBATCH --ntasks=1

cd ${SLURM_SUBMIT_DIR}

python ib_submit_high_mem.py $1 $2 $3 $4 $5 $6
