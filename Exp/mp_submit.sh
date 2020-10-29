#!/bin/sh

#SBATCH --partition=ib
#SBATCH --time=30:00:00
#SBATCH --mem-per-cpu=3G
#SBATCH --job-name=mp_submit
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1 
#SBATCH --cpus-per-task=16

export OMP_NUM_THREADS=1

cd ${SLURM_SUBMIT_DIR}

python mp_submit.py $1 $2 $3 $4