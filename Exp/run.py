import os
from utils import get_choice, get_name

# Main directory
dr = '/users/s/a/sahahn/Parcs_Project/'

# Get parcel, model, target to run
parcel, model, target, save_loc = get_choice(dr)

# Submit the job
os.system('sbatch dask_submit.sh ' + parcel + ' ' + model + ' ' + target + ' ' + save_loc)

# Print info
print('Submitted selected choice: ', get_name(parcel, model, target), flush=True)