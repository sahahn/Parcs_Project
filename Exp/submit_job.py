# sinfo -o"%P %C %c %m" -e

import os
from joblib import parallel_backend
import numpy as np

from helpers import unpack_args
from setup_dask import setup_dask
from submit import evaluate


def main():

    # Unpack args
    args = unpack_args()

    # Setup dask
    client, dask_ip, cluster = setup_dask(args)

    # Submit with dask back-end, waiting for workers to connect
    with parallel_backend('dask', wait_for_workers_timeout=args['wait_time']):

        # Run evaluate
        evaluate(args, args['n_jobs'], dask_ip=dask_ip)
        print('', flush=True)

    # Once done - re-submit
    os.system('python run.py')

    # Close cluster and client
    cluster.close()
    client.close()
   
# Only call when run
if __name__ == "__main__":
    main()

