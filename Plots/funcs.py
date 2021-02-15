import os
import numpy as np

# Get helpers from Exp directory
import sys
sys.path.append("../Exp/")
from helpers import get_stacked_options, get_voted_options, get_grid_options

def get_adj_size(parcel_str, grid=False):

    n_parcels = int(parcel_str.split('_')[3])
    parcel_size = parcel_str.split('_')[2]

    # If parcel size is a range
    if '-' in parcel_size:

        min_size = int(parcel_size.split('-')[0])
        max_size = int(parcel_size.split('-')[1])
        
        # In case of grid, lets go with max size... ?
        if grid:
            return max_size

        # Generate sizes as points between either end,
        sizes = np.linspace(min_size, max_size, n_parcels).astype('int')
        return np.sum(sizes)
    
    # If fixed just multiply size by base size
    else:
        base_sz = int(parcel_size)

        if grid:
            return base_sz

        return base_sz * n_parcels


def get_parc_sizes(parc_dr='../parcels',
                   base=False,
                   prob=False,
                   ico=False,
                   random=False,
                   fs=False,
                   stacked=False,
                   voted=False,
                   grid=False,
                   identity=False,
                   everything=False,
                   size_min=None,
                   size_max=None):

    if everything:
        base = True
        prob = True
        ico = True
        random = True
        fs = True
        stacked = True
        voted = True
        grid = True
        identity = True

    parc_sizes = {}
    
    # Get list of all parcels
    all_parcels = os.listdir(parc_dr)
    parcels = []

    for p in all_parcels:

        if p.startswith('random_'):
            if random:
                parcels.append(p)
        elif p.startswith('icosahedron'):
            if ico:
                parcels.append(p)
        elif '_prob.npy' in p:
            if prob:
                parcels.append(p)
        else:
            if base:
                parcels.append(p)

    # Add all requested parcels
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
    
    # If different requested
    if stacked:
        for p in get_stacked_options():
            parc_sizes[p] = get_adj_size(p)

    if voted:
        for p in get_voted_options():
            parc_sizes[p] = get_adj_size(p)
    
    if grid:
        for p in get_grid_options():
            parc_sizes[p] = get_adj_size(p, grid=True)
    
    # Force identity off
    #if identity:
    #    parc_sizes['identity'] = 64984

    keys = list(parc_sizes)
    for key in keys:
        d = False

        if size_min is not None:
            if parc_sizes[key] < size_min:
                d = True
        if size_max is not None:
            if parc_sizes[key] > size_max:
                d = True

        if d:
            del parc_sizes[key]

    return parc_sizes


def extract_run_info(txt):
    
    run_ind = 'Running for:'

    if run_ind in txt[1]:
        run_info = txt[1]
    elif run_ind in txt[2]:
        run_info = txt[2]
    elif run_ind in txt[3]:
        run_info = txt[3]
    else:
        run_info = ''
        
    return run_info.replace(run_ind, '').strip()


def get_n_jobs(file):

    # Determine how job was run
    if file.startswith('test_') or file.startswith('8_'):
        n_jobs = 8
    elif file.startswith('2_'):
        n_jobs = 2
    elif file.startswith('4_'):
        n_jobs = 4
    elif file.startswith('12_'):
        n_jobs = 12
    elif file.startswith('16_'):
        n_jobs = 16
    elif file.startswith('24_'):
        n_jobs = 24
    elif file.startswith('20_'):
        n_jobs = 20
    elif file.startswith('32_'):
        n_jobs = 32
    elif file.startswith('elastic_'):
        n_jobs = int(file.split('_')[2])
    elif file.startswith('low_') or file.startswith('high_'):
        if '_extra' in file:
            n_jobs = 48
        else:
            n_jobs = 24
    elif file.startswith('long_'):
        n_jobs = 1

    else:
        print('error:', file)

    return n_jobs
