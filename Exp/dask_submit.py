import os
from joblib import parallel_backend

from helpers import unpack_args
from setup_dask import setup_dask
from submit import evaluate

try:

    # Base Params
    cores = 4
    scale = 6
    memory = "8 GB"
    n_jobs = int(cores * scale)

    # Unpack args
    args = unpack_args()

    # Setup dask
    client, dask_ip = setup_dask(args['name'], cores, memory, scale)

    # Wait up to an hour lets say - for dask to connect before starting
    with parallel_backend('dask', wait_for_workers_timeout=3600):

        # Run evaluate
        evaluate(args, n_jobs, dask_ip=dask_ip)

    print('dask_submit finished, starting new job.', flush=True)

    # Try Submit new job
    os.system('python run.py dask')

# Any problems, submit high memory version of same params
except:
    print('Re-submit with high mem !', flush=True)
    os.system('sbatch dask_submit_high_mem.sh ' + args['parcel'] + ' '+ args['model'] + ' ' + args['target'] + ' ' + args['save_loc'])