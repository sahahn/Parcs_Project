import os
from joblib import parallel_backend

from helpers import unpack_args
from setup_dask import setup_bluemoon
from submit import evaluate


def main():

    # Unpack args
    args = unpack_args()

    # Setup dask
    client, dask_ip = setup_bluemoon(args)

    # Wait up to an hour lets say - for dask to connect before starting
    with parallel_backend('dask', wait_for_workers_timeout=7200):

        # Run evaluate
        evaluate(args, args['n_jobs'], dask_ip=dask_ip)

    # Close client
    client.close()

    # Once done with no errors, re-submit on original parition
    os.system('python run.py ' + args['original_partition'])

# Only call when run
if __name__ == "__main__":
    main()

