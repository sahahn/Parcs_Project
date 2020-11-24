#!/bin/sh

cd "$(dirname "$0")"
mkdir -p Job_Logs

python process_parcs.py
python process_random_parcels.py
python process_derivatives.py
python process_targets.py
python setup_ML.py
python setup_alt_ML.py
