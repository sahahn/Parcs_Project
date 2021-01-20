#!/bin/sh
#SBATCH --partition=short
#SBATCH --time=3:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=Setup
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1 
#SBATCH --cpus-per-task=4

cd ${SLURM_SUBMIT_DIR}
mkdir -p Job_Logs

#python process_parcs.py
python process_random_parcels.py
#python process_derivatives.py
#python process_targets.py
#python setup_ML.py
#python setup_alt_ML.py

