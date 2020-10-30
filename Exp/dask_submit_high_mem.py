import os
from joblib import parallel_backend

from helpers import unpack_args
from setup_dask import setup_dask
from submit import evaluate

# Base Params
cores = 4
scale = 6
memory = "18 GB"
n_jobs = int(cores * scale)

# Unpack args
args = unpack_args()

# Setup dask
client, dask_ip = setup_dask(args['name'], cores, memory, scale)

# Wait up to two hours for high mem
with parallel_backend('dask', wait_for_workers_timeout=7200):

    # Run evaluate
    evaluate(args, n_jobs, dask_ip=dask_ip)

print('dask_submit finished, starting new job.', flush=True)

# Submit base
os.system('python run.py dask')