from BPt import *
from helpers import get_choice, get_name, clean_cache
from submit import evaluate
import time
import sys
import random

# Get n_jobs
n_jobs = int(list(sys.argv)[1])

# Stagger jobs a little
time.sleep(random.random() * 30)

dr = '/users/s/a/sahahn/Parcs_Project/'

# Select a choice
parcel, model, target, save_loc = get_choice(dr)

args = {'name': get_name(parcel, model, target),
        'save_loc': save_loc,
        'parcel': parcel,
        'model': model,
        'target': target}

# Run evaluate
evaluate(args, n_jobs, dask_ip=None)

# Clean cache when done
clean_cache(dr=dr, scratch_dr='/users/s/a/sahahn/scratch/')