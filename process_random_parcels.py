from BPt.extensions import RandomParcels
from numpy import random
from helpers import load_geo
import numpy as np

# Load geometry
geo = load_geo()

# Load medial wall mask
medial_wall_mask = load_medial_wall()

for size in [100, 200, 300, 400, 500]:
    for random_state in range(1):
        
        # Generate this random parcel
        parc = RandomParcels(geo, n_parcels=size,
                             medial_wall_mask=medial_wall_mask,
                             random_state=random).get_parc()

        # Save the parcel under random _ size _ unique random state
        np.save('parcels/random_' + str(size) + '_' + str(random_state))