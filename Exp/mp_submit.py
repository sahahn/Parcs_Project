import os

from helpers import unpack_args
from submit import evaluate

import lightgbm
print('LIGHT GBM VERSION:', lightgbm.__version__)

n_jobs = 16

# Unpack args
args = unpack_args()

# Run evaluate
evaluate(args, n_jobs, dask_ip=None)

print('mp_submit finished, starting new job.', flush=True)
os.system('python run.py mp')