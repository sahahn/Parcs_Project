# sinfo -o"%P %C %c %m" -e

import os
from joblib import parallel_backend

from helpers import unpack_args
from setup_dask import setup_dask
from submit import evaluate


def main():

    # Unpack args
    args = unpack_args()

    try:

        # Setup dask
        client, dask_ip = setup_dask(args)

        # Submit with dask back-end, waiting for workers to connect
        with parallel_backend('dask', wait_for_workers_timeout=args['wait_time']):

            # Run evaluate
            evaluate(args, args['n_jobs'], dask_ip=dask_ip)

        # Close client
        client.close()

        # Once done with no errors, re-submit
        os.system('python run.py')

    # If any errors
    except Exception as e:

        # Append to errors file
        with open('errors.txt', 'a') as f:
            f.write('Error with: ' + args['name'] + ' ' + repr(e) + '\n')
   
# Only call when run
if __name__ == "__main__":
    main()

