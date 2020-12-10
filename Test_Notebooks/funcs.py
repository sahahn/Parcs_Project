import os
import numpy as np

# Get helpers from Exp directory
import sys
sys.path.append("../Exp/")
from helpers import get_stacked_options


def get_parc_sizes(parc_dr='../parcels', fs=False, stacked=False,
                   voted=False, identity=False, everything=False):

    if everything:
        fs = True
        stacked = True
        voted = True
        identity = True

    parc_sizes = {}
    
    # Add all the base parcels 
    parcels = os.listdir(parc_dr)
    for p in parcels:
        
        name = p.replace('.npy', '')
        parc = np.load(os.path.join(parc_dr, p))
        
        if len(parc.shape) == 2:
            sz = parc.shape[1]
        else:
            sz = len(np.unique(parc))
        
        parc_sizes[name] = sz
    
    # If extra freesurfer requested
    if fs:
        parc_sizes['freesurfer_destr'] = 150
        parc_sizes['freesurfer_desikan'] = 68
    
    # If stacked requested
    if stacked:
        for p in get_stacked_options():
            
            base_sz = int(p.split('_')[2])
            num = int(p.split('_')[3])
            adj_sz = base_sz * num
            parc_sizes[p] = adj_sz

    if voted:
        pass

    if identity:
        parc_sizes['identity'] = 64984

    return parc_sizes