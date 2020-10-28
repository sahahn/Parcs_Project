import nibabel as nib
import numpy as np
from scipy.io import loadmat
from nibabel import GiftiImage

def merge(lh, rh):
    
    ul = np.unique(lh)
    ur = np.unique(rh)
    intersect = len(np.intersect1d(ul, ur))
    
    if intersect > 0:
        if intersect / len(ul) > .75:
            rh += max(ul)
        
    data = np.concatenate([lh, rh])
    return data

def extract(surf, data):
    
    to_fill = np.zeros(surf.surface_number_of_vertices)
    verts = data[surf.index_offset:surf.index_offset + surf.index_count]
    to_fill[surf.vertex_indices._indices] = verts
    
    return to_fill

def conv_to_array_32k_space(data_loc):
    
    raw = nib.load(data_loc)
    
    # Check if GiftiImage
    if isinstance(raw, GiftiImage):
        data = raw.darrays[0].data

        if data.shape == (32492,):
            return data
        else:
            print('GIFTI found with shape', data.shape)

    data = raw.get_fdata().squeeze()
    
    index_map = raw.header.get_index_map(1) 
    shape = data.shape[0]
    
    if shape == 91282:
        
        lh_surf = index_map[1]
        rh_surf = index_map[2]
        
        lh = extract(lh_surf, data)
        rh = extract(rh_surf, data)
        
        return merge(lh, rh)
        
    elif shape == 64984 or shape == 59412:
        
        lh_surf = index_map[0]
        rh_surf = index_map[1]
        
        lh = extract(lh_surf, data)
        rh = extract(rh_surf, data)
        
        return merge(lh, rh)
    
    elif shape == 29696 or shape == 32492 or shape == 29716:
        
        surf = index_map[0]
        return extract(surf, data)
    
    else: 
        print('Warning shape =', shape)

def conv_matlab(lh_loc, rh_loc, lh_map, rh_map):

    lh_d = loadmat(lh_loc)['parcels'].squeeze()
    rh_d = loadmat(rh_loc)['parcels'].squeeze()

    lh = extract(lh_map, lh_d)
    rh = extract(rh_map, rh_d)

    return merge(lh, rh)

def extract_destr_rois(loc):
    
    if loc.split('/')[-1].startswith('rh'):
        prepend = 'rh.'
    else:
        prepend = 'lh.'
    
    header = None
    with open(loc, 'r') as f:
        d = {}
        
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('# ColHeaders'):
                header = line.replace('# ', '')
                header = header.split(' ')[2:]
            if not line.startswith('#'):
                line = [l for l in line.split() if len(l) > 0]
                feat = line[0]
                values = line[1:]
                for i in range(len(values)):
                    nm = prepend + feat+'_'+header[i]
                    d[nm.lower()] = values[i]
        return d