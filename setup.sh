#!/bin/sh
#SBATCH --partition=bluemoon
#SBATCH --time=6:00:00
#SBATCH --mem-per-cpu=2G
#SBATCH --job-name=setup
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err
#SBATCH -n 32

cd ${SLURM_SUBMIT_DIR}

# Process the raw parcellations
python process_parcs.py

# Generate the targets df
python process_targets.py

# Re-save / process the main surface data
python process_derivatives.py

# Setup / save the base ML object
python setup_ML.py
