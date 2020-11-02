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
    output = '--output=' + str(os.path.join(temp_dr, '%x_%j.out'))

    return temp_dr, output

def setup_dask(name, cores, memory, scale):

    temp_dr, output = setup_paths(name)

    # Create dask slurm cluster
    cluster = SLURMCluster(
        cores=cores,
        memory=memory,
        processes=1,
        queue='bluemoon',
        walltime='30:00:00',
        local_directory='/tmp/' + name,
        job_extra=[output])

    # Setup rest of dask to run
    cluster.scale(jobs=scale)
    dask_ip = cluster.scheduler_address
    
    # Make client
    client = Client(dask_ip)
    
    return client, dask_ip

def setup_ib(name, cores, memory, scale):

    temp_dr, output = setup_paths(name)

    # Create dask slurm cluster
    cluster = SLURMCluster(
        cores=cores,
        memory=memory,
        processes=1,
        queue='ib',
        walltime='30:00:00',
        local_directory='/tmp/' + name,
        job_extra=[output])

    # Setup rest of dask to run
    cluster.scale(jobs=scale)
    dask_ip = cluster.scheduler_address
    
    # Make client
    client = Client(dask_ip)
    
    return client, dask_ip
    
    
def setup_short(args):

    # Setup temp dr + output
    temp_dr, output = setup_paths(args['name'])

    # Create dask slurm cluster
    cluster = SLURMCluster(
        cores=args['cores'],
        memory=str(args['memory']) + ' GB',
        processes=1,
        queue='short',
        walltime='3:00:00',
        local_directory='/tmp/' + args['name'],
        job_extra=[output])

    # Setup rest of dask to run
    cluster.scale(jobs=args['scale'])
    dask_ip = cluster.scheduler_address

    client = Client(dask_ip)
    
    return client, dask_ip


def setup_bluemoon(args):

    # Setup temp dr + output
    temp_dr, output = setup_paths(args['name'])

     # Create dask slurm cluster
    cluster = SLURMCluster(
        cores=args['cores'],
        memory=str(args['memory']) + ' GB',
        processes=1,
        queue='bluemoon',
        walltime='30:00:00',
        local_directory='/tmp/' + args['name'],
        job_extra=[output])

    # Setup rest of dask to run
    cluster.scale(jobs=args['scale'])
    dask_ip = cluster.scheduler_address

    client = Client(dask_ip)
    
    return client, dask_ip