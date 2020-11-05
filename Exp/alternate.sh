#!/bin/sh
#SBATCH --partition=bluemoon
#SBATCH --time=3:00:000
#SBATCH --mem-per-cpu=3G
#SBATCH --job-name=alternate
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1 
#SBATCH --cpus-per-task=8

export OMP_NUM_THREADS=1
srun python alternate.py