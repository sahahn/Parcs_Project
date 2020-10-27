import sys
import os
import time
import numpy as np
from BPt import Load
from dask_jobqueue import SLURMCluster
from dask.distributed import Client
from joblib import parallel_backend
from BPt import Problem_Spec, CV

from models import get_pipe
from utils import get_name

# Unpack args
args = list(sys.argv)[1:]

# First three, make name
parcel = args[0]
model = args[1]
target = args[2]

# Get name
name = get_name(parcel, model, target)
print('Running dask_submit for: ', name, flush=True)

# Unpack save loc
save_loc = args[3]

# Save current time to indicate job is started
np.save(save_loc, np.array([time.time()]))

# Job params
cores = 4
scale = 6
memory = "10 GB"
n_jobs = int(cores * scale)

# Get temp paths paths
temp_dask = '/users/s/a/sahahn/scratch/dask/'
temp_dr = os.path.join(temp_dask, name)
os.makedirs(temp_dr, exist_ok=True)
output = '--output=' + str(os.path.join(temp_dr, '%x_%j.out'))

# Create dask slurm cluster
cluster = SLURMCluster(
    cores=cores,
    memory=memory,
    processes=1,
    queue='bluemoon',
    walltime='30:00:00',
    local_directory=temp_dr,
    job_extra=[output])

# Setup rest of dask to run
cluster.scale(jobs=scale)
dask_ip = cluster.scheduler_address
client = Client(dask_ip)

# Load the ML object
ML = Load('/users/s/a/sahahn/Parcs_Project/data/Base.ML',
           log_dr=None, notebook=False)
ML.n_jobs = n_jobs

# Create the CV group preserve by family id
cv = CV(groups='rel_family_id')

# Get the pipeline to evaluate
pipeline = get_pipe(model_str=model,
                    parcel=parcel,
                    cv=cv,
                    dask_ip=dask_ip)

# Get the problem spec
ps = Problem_Spec(target=target)

# Wait up to an hour lets say - for dask to connect before starting
with parallel_backend('dask', wait_for_workers_timeout=3600):

    # Evaluate this combination with 5 fold CV, two repeats
    results = ML.Evaluate(model_pipeline=pipeline,
                          problem_spec=ps,
                          splits=5,
                          n_repeats=2,
                          CV=cv)

    # Save scores, indicating this job is done
    scores = np.array(results['summary_scores'])
    np.save(save_loc, scores)

print('dask_submit finished, starting new job.', flush=True)

# Try Submit new job
os.system('python run.py')