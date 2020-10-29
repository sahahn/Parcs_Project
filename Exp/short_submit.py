import os
from joblib import parallel_backend

from helpers import unpack_args
from setup_dask import setup_short
from submit import evaluate


def main():

    # Unpack args
    args = unpack_args()

    try:

        # Setup dask
        client, dask_ip = setup_short(args)

        # Wait up to an hour lets say - for dask to connect before starting
        with parallel_backend('dask', wait_for_workers_timeout=3600):

            # Run evaluate
            evaluate(args, args['n_jobs'], dask_ip=dask_ip)

        # Close client
        client.close()

        # Once done with no errors, re-submit on original parition
        os.system('python run.py ' + args['original_partition'])

    # If any errors -
    except:

        # If error when running low mem, resubmit as high mem
        if args['memory'] == '8':

            print('Re-submit with high memory!', flush=True)

            cmd = 'sbatch --mem-per-cpu=8G short_submit.sh '
            cmd += args['parcel'] + ' '+ args['model'] + ' '
            cmd += args['target'] + ' ' + args['save_loc'] + ' '
            cmd += '18 ' + args['original_partition']
            os.system(cmd)

# Only call when run
if __name__ == "__main__":
    main()

