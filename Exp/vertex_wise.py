from submit import evaluate
from helpers import get_choice, get_name
import os
import numpy as np
import time
import sys

dr = '/users/s/a/sahahn/Parcs_Project/'

# Get n_jobs
n_jobs = int(list(sys.argv)[1])

# Select a choice
parcel, model, target, split, save_loc = get_choice(dr, parcs='identity')

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

# Set args
args = {'name': get_name(parcel, model, target, split=split),
        'save_loc': save_loc,
        'parcel': parcel,
        'model': model,
        'target': target,
        'split': split}

# Run evaluate
evaluate(args=args, n_jobs=n_jobs)