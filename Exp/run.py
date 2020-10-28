import os
import sys
from helpers import get_choice, get_name

# Main directory
dr = '/users/s/a/sahahn/Parcs_Project/'

# Get parcel, model, target to run
parcel, model, target, save_loc = get_choice(dr)

args = list(sys.argv)[1:]

if len(args) == 0:
    base = 'sbatch dask_submit.sh '
elif args[0] == 'dask':
    base = 'sbatch dask_submit.sh '
elif args[0] == 'ib':
    base = 'sbatch ib_submit.sh '
elif args[0] == 'mp':
    base = 'sbatch mp_submit.sh '
else:
    base = 'sbatch dask_submit.sh '

# Submit the job
os.system(base + parcel + ' ' + model + ' ' + target + ' ' + save_loc)

# Print info
print('Submitted selected choice: ', get_name(parcel, model, target), flush=True)