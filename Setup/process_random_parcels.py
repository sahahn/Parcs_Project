from BPt.extensions import RandomParcels
from numpy import random
from helpers import load_geo, load_medial_wall
import numpy as np
import os

# Load geometry
geo = load_geo(standard_mesh_loc='../raw/standard_mesh_atlases/')

# Load medial wall mask
medial_wall_mask =\
    load_medial_wall(annot_loc='../raw/fs_LR_32k_label/medialwall.annot')

# Set save dir
#save_dr = '../parcels/'
save_dr = '../extra_random_parcels/'
os.makedirs(save_dr, exist_ok=True)

sizes = []
sizes += list(np.linspace(100, 1000, 3).astype('int'))
sizes += list(np.linspace(100, 1000, 5).astype('int'))
sizes += list(np.linspace(100, 1000, 8).astype('int'))
sizes += list(np.linspace(100, 1000, 10).astype('int'))

sizes += list(np.linspace(50, 500, 3).astype('int'))
sizes += list(np.linspace(50, 500, 5).astype('int'))
sizes += list(np.linspace(50, 500, 8).astype('int'))
sizes += list(np.linspace(50, 500, 10).astype('int'))

for size in set(sizes):
#for size in [10, 20, 30, 40, 50, 60, 70, 80, 90, 2000, 3000]:
    for random_state in range(0, 5):

        # Set save name
        save_name = os.path.join(save_dr, 'random_' + str(size) + '_' + str(random_state) + '.npy')

        # Only generate if it doesn't already exist
        # Though random state should ensure that it is the same anyway
        if not os.path.exists(save_name):
        
            # Generate this random parcel
            parc = RandomParcels(geo, n_parcels=size,
                                 medial_wall_mask=medial_wall_mask,
                                 random_state=random_state).get_parc()
            
            # Save
            np.save(save_name, parc)
            print('Generated:', save_name, flush=True)

        else:
            print('Skip Generate:', save_name, flush=True)
