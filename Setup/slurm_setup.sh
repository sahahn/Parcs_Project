#!/bin/sh
#SBATCH --partition=bluemoon
#SBATCH --time=30:00:00
#SBATCH --mem-per-cpu=4G
#SBATCH --job-name=Setup
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1 
#SBATCH --cpus-per-task=16

cd ${SLURM_SUBMIT_DIR}
mkdir -p Job_Logs

python process_parcs.py
python process_random_parcels.py
python process_derivatives.py
python process_targets.py
python setup_ML.py
python setup_alt_ML.py

