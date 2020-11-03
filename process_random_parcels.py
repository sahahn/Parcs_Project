from BPt.extensions import RandomParcels
from numpy import random
from helpers import load_geo, load_medial_wall
import numpy as np

# Load geometry
geo = load_geo(standard_mesh_loc='raw/standard_mesh_atlases/')

# Load medial wall mask
medial_wall_mask =\
    load_medial_wall(annot_loc='raw/fs_LR_32k_label/medialwall.annot')

for size in [800]:
#for size in [100, 200, 300, 400, 500]:

    for random_state in range(0, 3):
        
        # Generate this random parcel
        parc = RandomParcels(geo, n_parcels=size,
                             medial_wall_mask=medial_wall_mask,
                             random_state=random).get_parc()

        # Save the parcel under random _ size _ unique random state
        save_name = 'parcels/random_' + str(size) + '_' + str(random_state)
        np.save(save_name, parc)
