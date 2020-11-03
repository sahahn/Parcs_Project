import os
import sys
from helpers import get_choice, get_name

# Main directory
dr = '/users/s/a/sahahn/Parcs_Project/'

# Get parcel, model, target to run
parcel, model, target, save_loc = get_choice(dr)

# Base parcs that need high mem
hi_mem = set(['icosahedron-1002_dlab',
              'icosahedron-1442_dlab',
              'schaefer_800',
              'schaefer_900',
              'schaefer_1000'])

# Add random
for size in [800, 900, 1000]:
    for random_state in range(0, 50):
        hi_mem.add('random_' + str(size) + '_' + str(random_state))

# If lgbm or svm
if model in set(['lgbm', 'svm']):
    hi_mem.add('icosahedron-642_dlab')
    hi_mem.add('schaefer_500')
    hi_mem.add('schaefer_600')
    hi_mem.add('schaefer_700')

    for size in [500, 600, 700]:
        for random_state in range(0, 50):
            hi_mem.add('random_' + str(size) + '_' + str(random_state))

# Base parcs that can run short
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
             'desikan_abox',
             'gordon_abox',
             ])

# Add random
for size in [100, 200, 300, 400]:
    for random_state in range(0, 50):
        short.add('random_' + str(size) + '_' + str(random_state))

# If elastic, extra short
if model == 'elastic':
    short.add('schaefer_500')
    short.add('schaefer_600')
    short.add('schaefer_700')
    short.add('icosahedron-642_dlab')
    short.add('icosahedron-362_dlab')

    for size in [500, 600, 700]:
        for random_state in range(0, 50):
            short.add('random_' + str(size) + '_' + str(random_state))

# Fixed
job_name = ''
cores = 4
scale = 6

# Set job memory
if parcel in hi_mem:
    mem_per_cpu = '8G'
    mem = int(cores * 5)
    job_name += 'high_'
    
else:
    mem_per_cpu = '4G'
    mem = int(cores * 2)
    job_name += 'low_'

# Set parition
if parcel in short:
    partition = 'short'
    time = '3:00:00'
    job_name += 'short'
else:
    partition = 'bluemoon'
    time = '30:00:00'
    job_name += 'bluemoon'

# Sbatch commands
cmd = 'sbatch --mem-per-cpu=' + mem_per_cpu + ' '
cmd += '--job-name=' + job_name + ' '
cmd += '--partition=' + partition + ' ' 
cmd += '--time=' + time + ' '

# Job commands
cmd += 'submit_job.sh '
cmd += parcel + ' '
cmd += model + ' '
cmd += target + ' '
cmd += save_loc + ' '
cmd += str(mem) + ' '
cmd += partition + ' '
cmd += str(cores) + ' '
cmd += str(scale)

# Submit job and print
os.system(cmd)
print('Submitted: ', cmd, flush=True)
