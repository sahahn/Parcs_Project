from BPt import *
from helpers import get_choice, get_name, clean_cache
from submit import evaluate
import time
import sys
import random
import numpy as np
import os
import time

print('Start', flush=True)

# Get n_jobs
passed_args = list(sys.argv)
n_jobs = int(passed_args[1])

try:
    c = int(passed_args[2])

# Default to choice 0 if not passed
except IndexError:
    c = 0

# Choice of only by passed choice
if c == 0:
    only = ['elastic', 'svm']
elif c == 1:
    only = ['lgbm']
elif c == 2:
    only = ['elastic']
elif c == 3:
    only = ['svm']
else:
    only = ['elastic', 'svm', 'lgbm']

# Stagger jobs a little
time.sleep(random.random() * 30)

dr = '/users/s/a/sahahn/Parcs_Project/'

# Select a choice
parcel, model, target, split, save_loc = get_choice(dr, only=only)

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
except:
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
