#!/bin/sh
#SBATCH --partition=bigmem
#SBATCH --time=30:00:00
#SBATCH --mem=64G
#SBATCH --job-name=test_64_2
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1 
#SBATCH --cpus-per-task=2

export OMP_NUM_THREADS=1
source /users/s/a/sahahn/.bashrc

cd ${SLURM_SUBMIT_DIR}

srun python vertex_wise.py
