#!/bin/sh
#SBATCH --partition=bigmemwk
#SBATCH --time=7-00:00:00
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1 

#SBATCH --array=1-4

#SBATCH --mem=256G
#SBATCH --job-name=long_256_8
#SBATCH --cpus-per-task=8

export OMP_NUM_THREADS=1
source /users/s/a/sahahn/.bashrc
cd ${SLURM_SUBMIT_DIR}

srun python vertex_wise.py 8
