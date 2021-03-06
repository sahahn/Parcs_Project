#!/bin/sh
#SBATCH --partition=bluemoon
#SBATCH --time=30:00:00
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1

#SBATCH --array=1-4

#SBATCH --mem=256G
#SBATCH --job-name=elastic_256_8
#SBATCH --cpus-per-task=8


export OMP_NUM_THREADS=1
source /users/s/a/sahahn/.bashrc

cd ${SLURM_SUBMIT_DIR}

srun python elastic_vertex_wise.py 8
