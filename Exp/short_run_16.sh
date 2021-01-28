#!/bin/sh
#SBATCH --partition=short
#SBATCH --time=3:00:00
#SBATCH --mem=16G
#SBATCH --job-name=16_short
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1 
#SBATCH --cpus-per-task=16

#SBATCH --array=1-1000

export OMP_NUM_THREADS=1
source /users/s/a/sahahn/.bashrc

cd ${SLURM_SUBMIT_DIR}

srun python alt_run.py 16 5
