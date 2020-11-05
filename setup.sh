#!/bin/sh
#SBATCH --partition=bluemoon
#SBATCH --time=3:00:00
#SBATCH --mem-per-cpu=1G
#SBATCH --job-name=setup
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err
#SBATCH -n 32

cd ${SLURM_SUBMIT_DIR}

#python process_parcs.py
#python process_derivatives.py
#python process_targets.py
python process_random_parcels.py
#python setup_ML.py
#python setup_alt_ML.py

