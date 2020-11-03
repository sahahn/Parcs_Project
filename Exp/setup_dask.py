from dask_jobqueue import SLURMCluster
from dask.distributed import Client
import os
import shutil

def setup_paths(name):

    # Get temp paths paths
    temp_dask = '/users/s/a/sahahn/scratch/dask/'
    temp_dr = os.path.join(temp_dask, name)

    # Try first remove existing
    try:
        shutil.rmtree(temp_dr)
    except FileNotFoundError:
        pass
    
    os.makedirs(temp_dr, exist_ok=True)
    output = ['--output=' + str(os.path.join(temp_dr, '%x_%j.out'))]

    return output

def setup_dask(args):

    # Get output
    output = setup_paths(args['name'])

    # Create dask slurm cluster
    cluster = SLURMCluster(
        cores=args['cores'],
        memory=str(args['memory']) + ' GB',
        processes=1,
        queue=args['partition'],
        walltime=args['time'],
        local_directory='/tmp/' + args['name'],
        job_extra=output)

    # Setup rest of dask to run
    cluster.scale(jobs=args['scale'])
    dask_ip = cluster.scheduler_address

    client = Client(dask_ip)
    
    return client, dask_ip