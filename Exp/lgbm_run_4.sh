#!/bin/sh
#SBATCH --partition=bluemoon
#SBATCH --time=30:00:00
#SBATCH --mem=4G
#SBATCH --job-name=4_lgbm_4G
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1 
#SBATCH --cpus-per-task=4

#SBATCH --array=1-200

export OMP_NUM_THREADS=1
source /users/s/a/sahahn/.bashrc

cd ${SLURM_SUBMIT_DIR}

srun python alt_run.py 4 1
