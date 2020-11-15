#!/bin/sh
#SBATCH --partition=bluemoon
#SBATCH --time=30:00:00
#SBATCH --mem=8G
#SBATCH --job-name=alt_run_8
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1 
#SBATCH --cpus-per-task=8

#SBATCH --array=1-10

export OMP_NUM_THREADS=1

cd ${SLURM_SUBMIT_DIR}

srun python alt_run.py 8