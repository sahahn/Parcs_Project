import os
import sys
from helpers import get_choice, get_name

# Main directory
dr = '/users/s/a/sahahn/Parcs_Project/'

# Get parcel, model, target to run
parcel, model, target, save_loc = get_choice(dr)

hi_mem = set(['icosahedron-1002_dlab',
              'icosahedron-1442_dlab',
              'schaefer_800',
              'schaefer_900',
              'schaefer_1000'])

short = set(['schaefer_100',
             'schaefer_200',
             'schaefer_300',
             'schaefer_400',
             'icosahedron-42_dlab',
             'vdg11b',
             'brodmann',
             'power2011_dlab',
             'fan_abox',
             'dextrieux_dlab',
             'destrieux_abox',
             'glasser_abox',
             'gordon',
             'baldassano_abox',
             'yeo_abox',
             'aal_abox',
             'shen_abox',
             'desikan_dlab',
             'desikan_abox'
             ])

# Changes to hi and short based on model
if model == 'lgbm':
    hi_mem.add('icosahedron-642_dlab')

args = list(sys.argv)[1:]

if len(args) == 0:
    base = 'sbatch dask_submit.sh '

else:
    
    # Check for parcel in hi_mem
    if parcel in hi_mem and args[0] == 'ib':
        print('Changing to ib_high', flush=True)
        args[0] = 'ib_high'

    if parcel in hi_mem and args[0] == 'dask':
        print('Changing to dask_high', flush=True)
        args[0] = 'dask_high'

    # Check for parcel in short
    if parcel in short:
        print('Changing to short queue', flush=True)
        base = 'sbatch short_submit.sh '

    # Otherwise, proc by arg name
    elif args[0] == 'dask':
        base = 'sbatch dask_submit.sh '
    elif args[0] == 'ib':
        base = 'sbatch ib_submit.sh '
    elif args[0] == 'ib_high':
        base = 'sbatch ib_submit_high_mem.sh '
    elif args[0] == 'dask_high':
        base = 'sbatch dask_submit_high_mem.sh '

# Submit the job
os.system(base + parcel + ' ' + model + ' ' + target + ' ' + save_loc + ' 8 ' + args[0])

# Print info
print('Submitted selected choice: ', get_name(parcel, model, target), flush=True)


# sbatch --partition=ib --mem-per-cpu=4G --jobname=ib_submit --time=30:00:00