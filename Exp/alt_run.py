from BPt import *
from helpers import get_choice, get_name, clean_cache
from submit import evaluate
import time
import sys
import random
import numpy as np
import os
import time

# Get n_jobs
n_jobs = int(list(sys.argv)[1])

# Stagger jobs a little
time.sleep(random.random() * 30)

dr = '/users/s/a/sahahn/Parcs_Project/'

# Select a choice
parcel, model, target, split, save_loc = get_choice(dr)

if parcel is None:
    sys.exit()

# Save current time to indicate job is started
# This also saves in run, but want to make sure earlier
# less chance of repeat...
np.save(save_loc, np.array([time.time()]))
os.chmod(save_loc, 0o777) 

# Process split
try:
    split = int(split)
except ValueError:
    split = None


args = {'name': get_name(parcel, model, target, split=split),
        'save_loc': save_loc,
        'parcel': parcel,
        'model': model,
        'target': target,
        'split': split}

# Run evaluate
evaluate(args, n_jobs, dask_ip=None)

# Clean cache when done
clean_cache(dr=dr, scratch_dr='/users/s/a/sahahn/scratch/')
